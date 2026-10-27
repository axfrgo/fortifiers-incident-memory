from __future__ import annotations

import io
import json
import os
import zipfile

import boto3

from .reports import render_html_report


def persist_evidence(run_id: str, report: dict, images: dict[str, bytes]) -> dict | None:
    """Store an encrypted-at-rest-by-S3-default-configuration evidence bundle when configured."""
    bucket = os.getenv("ARTIFACT_BUCKET")
    if not bucket:
        return None
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("report.json", json.dumps(report, indent=2, sort_keys=True))
        bundle.writestr("report.html", render_html_report(report))
        for name, content in images.items():
            bundle.writestr(f"images/{name}.png", content)
    key = f"evidence/{run_id}.zip"
    boto3.client("s3").put_object(Bucket=bucket, Key=key, Body=buf.getvalue(),
                                   ContentType="application/zip", ServerSideEncryption="AES256")
    url = boto3.client("s3").generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600)
    return {"bucket": bucket, "key": key, "server_side_encryption": "AES256", "download_url": url}

