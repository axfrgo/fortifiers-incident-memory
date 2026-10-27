from __future__ import annotations

import io
import json
import os
import zipfile

import boto3
from botocore.config import Config

from .reports import render_html_report


def _regional_s3_client():
    # Pin the regional endpoint so SigV4 presigned downloads use the same
    # region as the bucket instead of the legacy global S3 endpoint.
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    return boto3.client(
        "s3",
        region_name=region,
        endpoint_url=f"https://s3.{region}.amazonaws.com",
        config=Config(s3={"addressing_style": "virtual"}),
    )


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
    s3 = _regional_s3_client()
    s3.put_object(Bucket=bucket, Key=key, Body=buf.getvalue(),
                  ContentType="application/zip", ServerSideEncryption="AES256")
    url = s3.generate_presigned_url("get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600)
    return {"bucket": bucket, "key": key, "server_side_encryption": "AES256", "download_url": url}

