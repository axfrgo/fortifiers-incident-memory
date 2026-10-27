"""Build the pinned Python 3.14 x86_64 ZIP used by the AWS Lambda deployment."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
BUILD_DIR = ARTIFACTS / "lambda-package-py314"
ZIP_PATH = ARTIFACTS / "fortifiers-incident-memory-lambda-cp314.zip"
MANIFEST_PATH = ARTIFACTS / "lambda-package-build-manifest.json"
MAX_UNCOMPRESSED_BYTES = 250 * 1024 * 1024


def main() -> None:
    if sys.version_info[:2] != (3, 14):
        raise SystemExit(f"Use Python 3.14 to build this pinned runtime package; found {sys.version.split()[0]}")
    artifacts_root = ARTIFACTS.resolve()
    if BUILD_DIR.resolve().parent != artifacts_root:
        raise SystemExit("Refusing to clean a build path outside this project's artifacts directory")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    command = [
        sys.executable, "-m", "pip", "install", "--disable-pip-version-check",
        "--only-binary=:all:", "--no-compile",
        "--platform=manylinux_2_28_x86_64", "--platform=manylinux2014_x86_64",
        "--implementation=cp", "--python-version=314", "--abi=cp314",
        "--target", str(BUILD_DIR), "-r", str(ROOT / "requirements-lock.txt"),
    ]
    subprocess.run(command, cwd=ROOT, check=True)

    files: list[tuple[Path, str]] = []
    for path in BUILD_DIR.rglob("*"):
        if path.is_file() and path.suffix != ".pyc":
            files.append((path, path.relative_to(BUILD_DIR).as_posix()))
    for path in (ROOT / "src").rglob("*"):
        if path.is_file() and path.suffix != ".pyc":
            files.append((path, (Path("src") / path.relative_to(ROOT / "src")).as_posix()))
    files.append((ROOT / "lambda_handler.py", "lambda_handler.py"))

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
        for path, archive_name in sorted(files, key=lambda item: item[1]):
            bundle.write(path, archive_name)

    with zipfile.ZipFile(ZIP_PATH) as bundle:
        names = set(bundle.namelist())
        required = {"lambda_handler.py", "src/incident_memory/api.py", "cv2/__init__.py"}
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"Lambda ZIP is missing required entries: {missing}")
        uncompressed_bytes = sum(item.file_size for item in bundle.infolist())
        if uncompressed_bytes > MAX_UNCOMPRESSED_BYTES:
            raise SystemExit(f"Uncompressed Lambda package exceeds 250 MiB: {uncompressed_bytes} bytes")

    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = None
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_commit": commit,
        "runtime": "python3.14",
        "architecture": "x86_64",
        "opencv_pin": "opencv-python-headless==5.0.0.93",
        "requirements_lock": "requirements-lock.txt",
        "wheel_platform_tags": ["manylinux_2_28_x86_64", "manylinux2014_x86_64"],
        "file_count": len(files),
        "uncompressed_bytes": uncompressed_bytes,
        "zip_bytes": ZIP_PATH.stat().st_size,
        "sha256": hashlib.sha256(ZIP_PATH.read_bytes()).hexdigest(),
        "zip_path": ZIP_PATH.relative_to(ROOT).as_posix(),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
