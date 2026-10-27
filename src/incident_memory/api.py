from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
import base64
import io
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import cv2
from fastapi import FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from .agent import InvestigationAgent
from .cloud import persist_evidence
from .memory import TimestampValidationError, require_aware
from .reports import render_html_report
from .scenarios import SCENARIOS, fixture
from .vision import ImageInputError, assess_quality, decode_image, encode_png_data_uri, redact_detected_faces, require_opencv5


require_opencv5()
app = FastAPI(title="Fortifiers Incident Memory", version="0.1.0",
              description="Synthetic mechanical-room visual investigations with operator review")


class RequestSizeLimitMiddleware:
    """Bound upload request memory before multipart parsing (individual images are limited too)."""

    def __init__(self, application, max_bytes: int = 17 * 1024 * 1024):
        self.application = application
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope.get("path") != "/api/investigate/upload":
            await self.application(scope, receive, send)
            return

        headers = {key.lower(): value for key, value in scope.get("headers", [])}
        content_length = headers.get(b"content-length")
        if content_length is not None:
            try:
                if int(content_length) > self.max_bytes:
                    response = JSONResponse({"detail": "Upload request exceeds the 17 MiB total limit"}, status_code=413)
                    await response(scope, receive, send)
                    return
            except ValueError:
                response = JSONResponse({"detail": "Invalid Content-Length"}, status_code=400)
                await response(scope, receive, send)
                return

        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            if message["type"] != "http.request":
                continue
            body.extend(message.get("body", b""))
            if len(body) > self.max_bytes:
                response = JSONResponse({"detail": "Upload request exceeds the 17 MiB total limit"}, status_code=413)
                await response(scope, receive, send)
                return
            if not message.get("more_body", False):
                break

        sent = False
        async def replay_body():
            nonlocal sent
            if sent:
                return {"type": "http.disconnect"}
            sent = True
            return {"type": "http.request", "body": bytes(body), "more_body": False}

        await self.application(scope, replay_body, send)


app.add_middleware(RequestSizeLimitMiddleware)
ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = Path(os.getenv("INCIDENT_ARTIFACTS_DIR", str(ROOT / "artifacts" / "demo")))
ASSETS = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=ASSETS), name="static")
upload_events: dict[str, str] = {}


def _png_bytes(image):
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("Unable to encode PNG evidence")
    return encoded.tobytes()


def _save_artifacts(run_id: str, report: dict, fixture_data: dict, agent: InvestigationAgent) -> dict:
    from zipfile import ZIP_DEFLATED, ZipFile

    folder = ARTIFACTS / run_id
    folder.mkdir(parents=True, exist_ok=True)
    baseline = fixture_data["baseline"]
    current = fixture_data["current"]
    overlay = agent.comparison.overlay if agent.comparison is not None else current.copy()
    mask = agent.comparison.mask if agent.comparison is not None else current[:, :, 0] * 0
    images = {"baseline": _png_bytes(baseline), "event": _png_bytes(current),
              "overlay": _png_bytes(overlay), "change-mask": _png_bytes(mask)}
    for name, content in images.items():
        (folder / f"{name}.png").write_bytes(content)
    (folder / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (folder / "report.html").write_text(render_html_report(report), encoding="utf-8")
    zip_path = folder / "evidence.zip"
    with ZipFile(zip_path, "w", ZIP_DEFLATED) as zf:
        for name, content in images.items():
            zf.writestr(f"{name}.png", content)
        zf.writestr("report.json", (folder / "report.json").read_bytes())
        zf.writestr("report.html", (folder / "report.html").read_bytes())
    cloud = None
    try:
        cloud = persist_evidence(run_id, report, images)
    except Exception as exc:
        # A remote storage failure is observable and never silently reported as success.
        report["cloud_persistence_error"] = type(exc).__name__
        (folder / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    report_data = "data:application/json;base64," + __import__('base64').b64encode(json.dumps(report, ensure_ascii=False).encode("utf-8")).decode("ascii")
    html_report_data = "data:text/html;base64," + base64.b64encode(render_html_report(report).encode("utf-8")).decode("ascii")
    return {"run_storage_id": run_id, "report_url": report_data, "html_report_url": f"/artifacts/{run_id}/report.html",
            "html_report_data": html_report_data,
            "evidence_url": cloud["download_url"] if cloud else f"/artifacts/{run_id}/evidence.zip", "cloud_evidence": cloud,
            "baseline_data": encode_png_data_uri(baseline), "event_data": encode_png_data_uri(current),
            "overlay_data": encode_png_data_uri(overlay), "mask_data": encode_png_data_uri(mask)}


@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse(ASSETS / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "fortifiers-incident-memory", "opencv_version": cv2.__version__,
            "opencv5": cv2.__version__.split(".", 1)[0] == "5",
            "aws_s3_artifacts_enabled": bool(os.getenv("ARTIFACT_BUCKET")),
            "deployment_mode": os.getenv("DEPLOYMENT_MODE", "local"),
            "build_id": os.getenv("DEPLOYED_BUILD_ID", "local"),
            "git_commit": os.getenv("DEPLOYED_GIT_COMMIT", "unknown"),
            "user_uploads_enabled": os.getenv("ALLOW_USER_UPLOADS", "true").lower() == "true"}


@app.get("/api/scenarios")
def scenarios():
    return {"synthetic": True, "items": [{"id": key, "description": value} for key, value in SCENARIOS.items()]}


@app.get("/api/investigate/{scenario_id}")
def investigate(scenario_id: str):
    if scenario_id not in SCENARIOS:
        raise HTTPException(status_code=404, detail="Unknown demonstration scenario")
    data = fixture(scenario_id)
    data["event_id"] = f"{scenario_id}-{uuid.uuid4().hex[:12]}"
    agent = InvestigationAgent(data)
    report = agent.run()
    artifacts = _save_artifacts(data["event_id"], report, data, agent)
    return {**report, **artifacts}


@app.post("/api/investigate/upload")
async def investigate_upload(
    baseline: UploadFile = File(...), event: UploadFile = File(...),
    camera_id: str = Form("uploaded-camera"), event_id: str | None = Form(None),
    sensor_active: bool = Form(False), sensor_type: str = Form("water_contact"),
    baseline_time: str | None = Form(None), event_time: str | None = Form(None),
):
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if os.getenv("ALLOW_USER_UPLOADS", "true").lower() != "true":
        raise HTTPException(status_code=403, detail="User image uploads are disabled on this deployment")
    if baseline.content_type not in allowed or event.content_type not in allowed:
        raise HTTPException(status_code=415, detail="Upload PNG, JPEG, or WebP images only")
    baseline_bytes = await baseline.read(8 * 1024 * 1024 + 1)
    event_bytes = await event.read(8 * 1024 * 1024 + 1)
    payload_fingerprint = hashlib.sha256(baseline_bytes + event_bytes).hexdigest()
    try:
        baseline_image = decode_image(baseline_bytes)
        event_image = decode_image(event_bytes)
    except ImageInputError as exc:
        raise HTTPException(status_code=413 if "limit" in str(exc) else 400, detail=str(exc)) from exc
    if baseline_image.shape[:2] != event_image.shape[:2]:
        raise HTTPException(status_code=422, detail="Baseline and event frames must have matching dimensions")
    try:
        baseline_image, baseline_redaction = redact_detected_faces(baseline_image)
        event_image, event_redaction = redact_detected_faces(event_image)
    except ImageInputError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    event_id = event_id or uuid.uuid4().hex
    if event_id in upload_events:
        if upload_events[event_id] == payload_fingerprint:
            raise HTTPException(status_code=409, detail="Duplicate alarm event was not reprocessed")
        raise HTTPException(status_code=409, detail="Event ID conflicts with a previously received payload")
    upload_events[event_id] = payload_fingerprint
    try:
        when = require_aware(datetime.fromisoformat((event_time or datetime.now(timezone.utc).isoformat()).replace("Z", "+00:00")))
        before = require_aware(datetime.fromisoformat((baseline_time or (when - __import__('datetime').timedelta(minutes=15)).isoformat()).replace("Z", "+00:00")))
    except (ValueError, TimestampValidationError) as exc:
        upload_events.pop(event_id, None)
        raise HTTPException(status_code=422, detail="Timestamps must be valid ISO 8601 values with timezone offsets") from exc
    if before >= when:
        upload_events.pop(event_id, None)
        raise HTTPException(status_code=422, detail="Baseline must precede the event timestamp")
    quality = assess_quality(baseline_image)
    data = {"scenario": "uploaded_image", "description": "User-supplied image pair", "camera_id": camera_id,
            "event_id": event_id, "event_time": when, "baseline_time": before, "older_time": before,
            "baseline": baseline_image, "current": event_image, "older": None,
            "sensor": {"type": sensor_type, "active": sensor_active, "timestamp": when.isoformat(), "source": "uploaded-sensor-event"},
            "synthetic": False, "privacy_redaction": {"method": "OpenCV 5 DNN FaceDetectorYN with YuNet",
              "baseline": baseline_redaction, "event": event_redaction,
              "notice": "Frontal face detection is not exhaustive; manually inspect and redact screens, badges and other identifiers."}}
    agent = InvestigationAgent(data)
    report = agent.run()
    artifacts = _save_artifacts(uuid.uuid4().hex, report, data, agent)
    return {**report, **artifacts}


@app.get("/artifacts/{run_id}/{filename}")
def artifact(run_id: str, filename: str):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", run_id) or filename not in {"report.json", "report.html", "evidence.zip", "baseline.png", "event.png", "overlay.png", "change-mask.png"}:
        raise HTTPException(status_code=404, detail="Artifact not found")
    target = ARTIFACTS / run_id / filename
    if not target.is_file():
        raise HTTPException(status_code=404, detail="Artifact not found")
    return FileResponse(target, filename=filename)


class ReviewAction(BaseModel):
    action: str = Field(pattern="^(approve|reject|request_more_evidence)$")
    note: str = Field(default="", max_length=500)


@app.post("/api/review/{run_id}")
def record_review(run_id: str, review: ReviewAction, authorization: str | None = Header(default=None)):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,100}", run_id):
        raise HTTPException(status_code=404, detail="Run not found")
    folder = ARTIFACTS / run_id
    report_path = folder / "report.json"
    report = None
    if report_path.is_file():
        report = json.loads(report_path.read_text(encoding="utf-8"))
    elif os.getenv("ARTIFACT_BUCKET"):
        try:
            obj = __import__("boto3").client("s3").get_object(Bucket=os.getenv("ARTIFACT_BUCKET"), Key=f"evidence/{run_id}.zip")
            with zipfile.ZipFile(io.BytesIO(obj["Body"].read())) as archive:
                report = json.loads(archive.read("report.json"))
        except Exception as exc:
            raise HTTPException(status_code=404, detail="Run evidence is unavailable for review") from exc
    if report is None:
        raise HTTPException(status_code=404, detail="Run not found")
    required_key = os.getenv("REVIEW_API_KEY")
    if not report.get("synthetic_demo") and (not required_key or authorization != f"Bearer {required_key}"):
        raise HTTPException(status_code=401, detail="Authenticated operator review is required")
    record = {"action": review.action, "note": review.note, "recorded_at": datetime.now(timezone.utc).isoformat(),
              "scope": "acknowledgement only; no equipment or alarm control is performed"}
    stored_in_s3 = False
    if os.getenv("ARTIFACT_BUCKET"):
        review_key = f"evidence/{run_id}/reviews/{record['recorded_at'].replace(':', '-')}-{uuid.uuid4().hex[:8]}.json"
        try:
            __import__("boto3").client("s3").put_object(Bucket=os.getenv("ARTIFACT_BUCKET"), Key=review_key,
                Body=json.dumps(record, ensure_ascii=False).encode("utf-8"), ContentType="application/json", ServerSideEncryption="AES256")
            stored_in_s3 = True
        except Exception as exc:
            raise HTTPException(status_code=503, detail="Review could not be durably recorded in S3") from exc
    if folder.exists():
        with (folder / "human-review.jsonl").open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return {"recorded": True, "review": record, "stored_in_s3": stored_in_s3}

