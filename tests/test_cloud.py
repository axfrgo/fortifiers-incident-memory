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
    monkeypatch.setattr("incident_memory.cloud.boto3.client", lambda service: BrokenS3())
    with pytest.raises(RuntimeError, match="S3 denial"):
        persist_evidence("run-test", {"synthetic_demo": True}, {})
