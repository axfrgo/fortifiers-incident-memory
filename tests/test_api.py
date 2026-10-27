from __future__ import annotations

import io
import asyncio

import cv2
from fastapi.testclient import TestClient

from incident_memory.api import RequestSizeLimitMiddleware, app
from incident_memory.scenarios import fixture


client = TestClient(app)


def png_bytes(image):
    ok, encoded = cv2.imencode(".png", image)
    assert ok
    return encoded.tobytes()


def test_health_reports_opencv5():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["opencv5"] is True


def test_demo_endpoint_returns_report_trace_and_annotated_image():
    response = client.get("/api/investigate/clear_change")
    assert response.status_code == 200
    payload = response.json()
    assert payload["synthetic_demo"] is True
    assert payload["outcome"] == "human_review_required"
    assert payload["trace"]
    assert payload["overlay_data"].startswith("data:image/png;base64,")
    assert payload["sha256"]["baseline"]
    assert client.get(payload["html_report_url"]).status_code == 200


def test_review_action_is_recorded_without_actuating_equipment():
    result = client.get("/api/investigate/clear_change").json()
    response = client.post(f"/api/review/{result['run_storage_id']}", json={"action": "approve", "note": "reviewed"})
    assert response.status_code == 200
    assert response.json()["review"]["action"] == "approve"
    assert "no equipment" in response.json()["review"]["scope"]


def test_upload_accepts_images_and_deduplicates_alarm_id():
    item = fixture("clear_change")
    base = png_bytes(item["baseline"])
    event = png_bytes(item["current"])
    files = {"baseline": ("base.png", io.BytesIO(base), "image/png"),
             "event": ("event.png", io.BytesIO(event), "image/png")}
    first = client.post("/api/investigate/upload", data={"camera_id": "cam-test", "event_id": "api-test-1",
                                                        "sensor_active": "true"}, files=files)
    assert first.status_code == 200
    duplicate_files = {"baseline": ("base.png", io.BytesIO(base), "image/png"),
                       "event": ("event.png", io.BytesIO(event), "image/png")}
    duplicate = client.post("/api/investigate/upload", data={"camera_id": "cam-test", "event_id": "api-test-1",
                                                             "sensor_active": "true"}, files=duplicate_files)
    assert duplicate.status_code == 409


def test_upload_rejects_corrupt_input_and_incompatible_resolution():
    bad = {"baseline": ("bad.png", io.BytesIO(b"broken"), "image/png"),
           "event": ("bad.png", io.BytesIO(b"broken"), "image/png")}
    assert client.post("/api/investigate/upload", files=bad).status_code == 400
    item = fixture("clear_change")
    small = cv2.resize(item["baseline"], (320, 240))
    mismatch = {"baseline": ("base.png", io.BytesIO(png_bytes(small)), "image/png"),
                "event": ("event.png", io.BytesIO(png_bytes(item["current"])), "image/png")}
    assert client.post("/api/investigate/upload", files=mismatch).status_code == 422


def test_upload_rejects_unsupported_media_type():
    files = {"baseline": ("file.txt", io.BytesIO(b"x"), "text/plain"),
             "event": ("file.txt", io.BytesIO(b"x"), "text/plain")}
    assert client.post("/api/investigate/upload", files=files).status_code == 415


def test_upload_rejects_inconsistent_timestamps():
    item = fixture("dry_normal")
    files = {"baseline": ("base.png", io.BytesIO(png_bytes(item["baseline"])), "image/png"),
             "event": ("event.png", io.BytesIO(png_bytes(item["current"])), "image/png")}
    response = client.post("/api/investigate/upload", data={"baseline_time":"2026-10-27T01:00:00Z",
        "event_time":"2026-10-27T00:00:00Z"}, files=files)
    assert response.status_code == 422


def test_untrusted_event_id_cannot_escape_artifact_directory():
    item = fixture("dry_normal")
    files = {"baseline": ("base.png", io.BytesIO(png_bytes(item["baseline"])), "image/png"),
             "event": ("event.png", io.BytesIO(png_bytes(item["current"])), "image/png")}
    response = client.post("/api/investigate/upload", data={"event_id":"../../outside"}, files=files)
    assert response.status_code == 200
    assert response.json()["run_storage_id"] != "../../outside"


def test_non_synthetic_review_requires_authentication(monkeypatch):
    monkeypatch.delenv("REVIEW_API_KEY", raising=False)
    item = fixture("dry_normal")
    files = {"baseline": ("base.png", io.BytesIO(png_bytes(item["baseline"])), "image/png"),
             "event": ("event.png", io.BytesIO(png_bytes(item["current"])), "image/png")}
    result = client.post("/api/investigate/upload", files=files).json()
    response = client.post(f"/api/review/{result['run_storage_id']}", json={"action":"approve"})
    assert response.status_code == 401


def test_upload_request_body_has_total_size_limit():
    async def exercise():
        async def downstream(scope, receive, send):
            raise AssertionError("oversized request reached the application")

        messages = []
        async def receive():
            return {"type": "http.request", "body": b"x", "more_body": False}

        async def send(message):
            messages.append(message)

        scope = {"type": "http", "method": "POST", "path": "/api/investigate/upload",
                 "headers": [(b"content-length", str(17 * 1024 * 1024 + 1).encode())]}
        await RequestSizeLimitMiddleware(downstream)(scope, receive, send)
        return messages

    messages = asyncio.run(exercise())
    assert messages[0]["status"] == 413
