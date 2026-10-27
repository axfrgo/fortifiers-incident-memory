from __future__ import annotations

import cv2
import numpy as np
import pytest

from incident_memory.scenarios import fixture
from incident_memory.vision import ImageInputError, align_and_compare, assess_quality, decode_image, redact_detected_faces, require_opencv5


def test_runtime_is_opencv_5():
    require_opencv5()
    assert cv2.__version__.startswith("5.")


def test_clear_change_has_opencv_region_and_measurements():
    item = fixture("clear_change")
    result = align_and_compare(item["baseline"], item["current"])
    assert result.comparable
    assert result.mask.dtype == np.uint8
    assert result.candidate_regions
    assert result.candidate_regions[0]["pixel_area"] > 300
    assert len(result.candidate_regions[0]["normalized_bbox"]) == 4
    assert result.elapsed_ms >= 0


def test_global_illumination_change_is_normalized():
    item = fixture("lighting_shift")
    result = align_and_compare(item["baseline"], item["current"])
    assert result.comparable
    assert result.illumination_gain < 1
    assert result.candidate_regions == []


def test_blur_quality_gate_rejects_unusable_frame():
    item = fixture("poor_image")
    quality = assess_quality(item["current"])
    assert not quality.usable
    assert any("blur" in reason for reason in quality.reasons)


def test_resolution_mismatch_is_fail_closed():
    item = fixture("clear_change")
    smaller = cv2.resize(item["baseline"], (320, 240))
    result = align_and_compare(smaller, item["current"])
    assert not result.comparable
    assert result.registration_method == "rejected_resolution_mismatch"
    assert result.candidate_regions == []


def test_feature_registration_failure_falls_back_and_downgrades_comparability():
    blank = np.zeros((240, 320, 3), dtype=np.uint8)
    result = align_and_compare(blank, blank.copy())
    assert result.registration_method == "identity_low_feature_fallback"
    assert result.reliability_score < 0.45
    assert not result.comparable


@pytest.mark.parametrize("payload", [b"", b"not an image", b"\x89PNG\r\n"])
def test_corrupt_and_missing_image_data_rejected(payload):
    with pytest.raises(ImageInputError):
        decode_image(payload)


def test_image_size_limit_rejected_before_decode():
    with pytest.raises(ImageInputError, match="8 MiB"):
        decode_image(b"x" * 100, max_bytes=10)


def test_face_redaction_adapter_is_available_and_preserves_dimensions():
    frame = fixture("dry_normal")["current"]
    redacted, metadata = redact_detected_faces(frame)
    assert redacted.shape == frame.shape
    assert metadata["method"] == "OpenCV 5 DNN FaceDetectorYN with YuNet"
    assert metadata["complete_redaction"] is False


def test_face_redaction_fails_closed_if_model_is_missing(monkeypatch):
    from pathlib import Path

    monkeypatch.setattr(Path, "is_file", lambda self: False)
    with pytest.raises(ImageInputError, match="upload processing is disabled"):
        redact_detected_faces(fixture("dry_normal")["current"])
