from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "artifacts" / "fortifiers-incident-memory-source.zip"
PUBLIC_REPOSITORY_URL = "https://github.com/axfrgo/fortifiers-incident-memory"
PUBLIC_ARCHIVE_URL = f"{PUBLIC_REPOSITORY_URL}/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip"
IGNORED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}
IGNORED_ARTIFACT_PREFIXES = ("lambda-package-build", "lambda-package-py", "aws-wheel-check")
IGNORED_FILES = {"fortifiers-incident-memory-source.zip", "fortifiers-incident-memory-lambda-cp314.zip", "source-archive-manifest.json", "source-archive-validation.json", "recording-smoke-frame.png"}
NON_SOURCE_MEDIA_SUFFIXES = {".mp4", ".mov"}


def included_files():
    demo_manifest = json.loads((ROOT / "artifacts" / "demo-cases.json").read_text(encoding="utf-8"))
    demo_ids = {case["run_storage_id"] for case in demo_manifest["cases"]}
    if demo_manifest.get("review_example"):
        demo_ids.add(demo_manifest["review_example"]["run_id"])
    live_check_path = ROOT / "artifacts" / "live-http-check.json"
    if live_check_path.exists():
        demo_ids.add(json.loads(live_check_path.read_text(encoding="utf-8"))["run_storage_id"])
    final_check_path = ROOT / "artifacts" / "final-local-verification.json"
    if final_check_path.exists():
        final_check = json.loads(final_check_path.read_text(encoding="utf-8"))
        for case in final_check.get("scenarios", []):
            if case.get("run_id"):
                demo_ids.add(case["run_id"])
        for case in final_check.get("dashboard_runs", []):
            if case.get("run_id"):
                demo_ids.add(case["run_id"])

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if len(relative.parts) >= 2 and relative.parts[0] == "artifacts" and relative.parts[1].startswith(IGNORED_ARTIFACT_PREFIXES):
            continue
        if len(relative.parts) >= 3 and relative.parts[:2] == ("artifacts", "demo") and relative.parts[2] not in demo_ids:
            continue
        if path.name in IGNORED_FILES or path.suffix == ".pyc":
            continue
        # Large presentation recordings are hosted as separate release assets.
        # Keep the portable source bundle focused on code, fixtures and reports.
        if path.suffix.lower() in NON_SOURCE_MEDIA_SUFFIXES:
            continue
        if path.name == ".env" or path.name.startswith(".env."):
            continue
        yield path, relative


def main() -> None:
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    files = list(included_files())
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path, relative in files:
            zf.write(path, Path("fortifiers-incident-memory") / relative)
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    manifest = {"created_at_utc": datetime.now(timezone.utc).isoformat(),
                "archive": ARCHIVE.name, "sha256": digest, "file_count": len(files),
                "includes_virtual_environment": False,
                "judge_accessible_public_url": PUBLIC_REPOSITORY_URL,
                "judge_accessible_archive_url": PUBLIC_ARCHIVE_URL}
    validation_path = ROOT / "artifacts" / "source-archive-validation.json"
    if validation_path.exists():
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        if validation.get("source_archive_sha256") == digest:
            manifest["validation"] = validation
    (ARCHIVE.parent / "source-archive-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({**manifest, "path": str(ARCHIVE), "size_bytes": ARCHIVE.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
