from __future__ import annotations

import pytest

from incident_memory.cloud import persist_evidence


def test_cloud_storage_is_optional_without_bucket(monkeypatch):
    monkeypatch.delenv("ARTIFACT_BUCKET", raising=False)
    assert persist_evidence("run-test", {"synthetic_demo": True}, {}) is None


def test_s3_write_failure_propagates_instead_of_claiming_saved(monkeypatch):
    class BrokenS3:
        def put_object(self, **kwargs):
            raise RuntimeError("simulated S3 denial")

    monkeypatch.setenv("ARTIFACT_BUCKET", "demo-bucket")
    monkeypatch.setattr("incident_memory.cloud.boto3.client", lambda service, **kwargs: BrokenS3())
    with pytest.raises(RuntimeError, match="S3 denial"):
        persist_evidence("run-test", {"synthetic_demo": True}, {})


def test_s3_presigned_artifact_uses_explicit_regional_endpoint(monkeypatch):
    calls = []

    class RecordingS3:
        def put_object(self, **kwargs):
            calls.append(("put", kwargs))

        def generate_presigned_url(self, operation, **kwargs):
            calls.append(("presign", operation, kwargs))
            return "https://example.invalid/evidence.zip?signature=redacted"

    monkeypatch.setenv("ARTIFACT_BUCKET", "demo-bucket")
    monkeypatch.setenv("AWS_REGION", "us-east-2")
    monkeypatch.setattr("incident_memory.cloud.boto3.client", lambda service, **kwargs: (calls.append((service, kwargs)) or RecordingS3()))

    result = persist_evidence("run-test", {"synthetic_demo": True}, {})

    client_call = calls[0]
    assert client_call[0] == "s3"
    assert client_call[1]["region_name"] == "us-east-2"
    assert client_call[1]["endpoint_url"] == "https://s3.us-east-2.amazonaws.com"
    assert client_call[1]["config"].s3 == {"addressing_style": "virtual"}
    assert result["download_url"].startswith("https://example.invalid/")
