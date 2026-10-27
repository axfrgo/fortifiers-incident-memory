from __future__ import annotations

import base64
import time
from dataclasses import asdict, dataclass
from pathlib import Path

import cv2
import numpy as np


class ImageInputError(ValueError):
    pass


@dataclass
class ImageQuality:
    width: int
    height: int
    blur_variance: float
    mean_luminance: float
    dark_fraction: float
    bright_fraction: float
    quality_score: float
    usable: bool
    reasons: list[str]


@dataclass
class VisionComparison:
    comparable: bool
    registration_method: str
    registration_inliers: int
    reliability_score: float
    illumination_gain: float
    changed_fraction: float
    candidate_regions: list[dict]
    mask: np.ndarray
    overlay: np.ndarray
    elapsed_ms: float
    notes: list[str]

    def public(self) -> dict:
        out = asdict(self)
        out.pop("mask")
        out.pop("overlay")
        return out


def require_opencv5() -> None:
    major = int(cv2.__version__.split(".", 1)[0])
    if major != 5:
        raise RuntimeError(f"OpenCV 5 is required; runtime reports cv2 {cv2.__version__}")


def decode_image(data: bytes, *, max_bytes: int = 8 * 1024 * 1024, max_pixels: int = 12_000_000) -> np.ndarray:
    if not data or len(data) > max_bytes:
        raise ImageInputError("Image is empty or exceeds the 8 MiB upload limit")
    arr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None or image.ndim != 3 or image.shape[2] != 3:
        raise ImageInputError("Image could not be decoded as a color image")
    if image.shape[0] * image.shape[1] > max_pixels:
        raise ImageInputError("Image exceeds the 12 megapixel limit")
    return image


def encode_png_data_uri(image: np.ndarray) -> str:
    ok, encoded = cv2.imencode(".png", image)
    if not ok:
        raise RuntimeError("OpenCV could not encode evidence image")
    return "data:image/png;base64," + base64.b64encode(encoded.tobytes()).decode("ascii")


def redact_detected_faces(image: np.ndarray) -> tuple[np.ndarray, dict]:
    """Blur YuNet-detected faces. Raise on model/runtime failure so uploads fail closed."""
    model = Path(__file__).resolve().parent / "assets" / "face_detection_yunet_2026may.onnx"
    if not model.is_file():
        raise ImageInputError("Privacy face-detector model is unavailable; upload processing is disabled")
    height, width = image.shape[:2]
    try:
        detector = cv2.FaceDetectorYN.create(
            str(model), "", (width, height), 0.6, 0.3, 5000,
        )
        _, faces = detector.detect(image)
    except Exception as exc:
        raise ImageInputError("Privacy face detector failed; upload processing is disabled") from exc

    redacted = image.copy()
    face_count = 0 if faces is None else len(faces)
    for face in faces if faces is not None else ():
        x, y, box_width, box_height = (int(round(value)) for value in face[:4])
        margin_x, margin_y = int(box_width * 0.15), int(box_height * 0.15)
        x0, y0 = max(0, x - margin_x), max(0, y - margin_y)
        x1, y1 = min(width, x + box_width + margin_x), min(height, y + box_height + margin_y)
        roi = redacted[y0:y1, x0:x1]
        kernel = max(15, (min(x1 - x0, y1 - y0) // 3) | 1)
        redacted[y0:y1, x0:x1] = cv2.GaussianBlur(roi, (kernel, kernel), 0)
    return redacted, {"method": "OpenCV 5 DNN FaceDetectorYN with YuNet", "faces_blurred": face_count,
                      "complete_redaction": False, "metadata_stripped_by_decode_reencode": True,
                      "notice": "Face detection can miss faces and does not detect names, badges, screens or other identifiers; inspect evidence manually."}


def assess_quality(image: np.ndarray) -> ImageQuality:
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    lum = float(np.mean(gray))
    dark = float(np.mean(gray < 18))
    bright = float(np.mean(gray > 244))
    reasons: list[str] = []
    if min(h, w) < 96:
        reasons.append("image is too small for reliable comparison")
    if blur < 24:
        reasons.append("frame is blurred or lacks usable detail")
    if lum < 28 or dark > 0.8:
        reasons.append("frame is underexposed")
    if lum > 232 or bright > 0.65:
        reasons.append("frame is overexposed")
    score = 1.0
    score -= min(0.55, max(0.0, (60.0 - blur) / 120.0))
    score -= min(0.35, dark * 0.5 + bright * 0.5)
    score = float(np.clip(score, 0.0, 1.0))
    return ImageQuality(w, h, round(blur, 2), round(lum, 2), round(dark, 4), round(bright, 4), round(score, 3), not reasons, reasons)


def _register(reference: np.ndarray, current: np.ndarray) -> tuple[np.ndarray, str, int, float, list[str]]:
    notes: list[str] = []
    if reference.shape[:2] != current.shape[:2]:
        return current, "rejected_resolution_mismatch", 0, 0.0, ["baseline and event frame resolutions differ"]
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    cur_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=1500, scaleFactor=1.2, nlevels=8, fastThreshold=8)
    k1, d1 = orb.detectAndCompute(ref_gray, None)
    k2, d2 = orb.detectAndCompute(cur_gray, None)
    if d1 is not None and d2 is not None and len(k1) >= 8 and len(k2) >= 8:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        pairs = matcher.knnMatch(d2, d1, k=2)
        good = [a for pair in pairs if len(pair) == 2 for a, b in [pair] if a.distance < 0.74 * b.distance]
        if len(good) >= 8:
            src = np.float32([k2[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst = np.float32([k1[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            homography, inlier_mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
            inliers = int(inlier_mask.sum()) if inlier_mask is not None else 0
            if homography is not None and inliers >= 7:
                h, w = reference.shape[:2]
                warped = cv2.warpPerspective(current, homography, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                ratio = inliers / max(1, len(good))
                return warped, "orb_ransac_homography", inliers, float(np.clip(ratio, 0, 1)), notes
    # ECC translation is a conservative fallback for scenes with too few ORB matches.
    try:
        ref_f = ref_gray.astype(np.float32) / 255.0
        cur_f = cur_gray.astype(np.float32) / 255.0
        warp = np.eye(2, 3, dtype=np.float32)
        score, warp = cv2.findTransformECC(ref_f, cur_f, warp, cv2.MOTION_TRANSLATION,
                                            (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5))
        dx, dy = float(warp[0, 2]), float(warp[1, 2])
        if float(score) > 0.72 and abs(dx) < reference.shape[1] * 0.08 and abs(dy) < reference.shape[0] * 0.08:
            aligned = cv2.warpAffine(current, warp, (reference.shape[1], reference.shape[0]),
                                     flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
            return aligned, "ecc_translation_fallback", 0, float(np.clip(score, 0, 1)), ["ORB was insufficient; ECC translation fallback used"]
    except cv2.error:
        pass
    notes.append("feature registration was insufficient; identity alignment retained with reduced reliability")
    return current.copy(), "identity_low_feature_fallback", 0, 0.35, notes


def align_and_compare(reference: np.ndarray, current: np.ndarray) -> VisionComparison:
    started = time.perf_counter()
    warped, method, inliers, reg_score, notes = _register(reference, current)
    if reference.shape[:2] != current.shape[:2]:
        blank = np.zeros(reference.shape[:2], dtype=np.uint8)
        return VisionComparison(False, method, inliers, 0.0, 1.0, 0.0, [], blank, reference.copy(),
                                (time.perf_counter() - started) * 1000, notes)

    # Normalize global brightness through HSV V before comparing. Saturation remains
    # available as an independent cue, making uniform lighting shifts less influential.
    ref_hsv = cv2.cvtColor(reference, cv2.COLOR_BGR2HSV)
    cur_hsv = cv2.cvtColor(warped, cv2.COLOR_BGR2HSV)
    ref_v = ref_hsv[:, :, 2].astype(np.float32)
    cur_v = cur_hsv[:, :, 2].astype(np.float32)
    ref_med = max(1.0, float(np.median(ref_v)))
    cur_med = max(1.0, float(np.median(cur_v)))
    gain = float(np.clip(ref_med / cur_med, 0.55, 1.8))
    normalized_v = np.clip(cur_v * gain, 0, 255).astype(np.uint8)
    normalized_sat = cur_hsv[:, :, 1]
    delta_v = cv2.absdiff(ref_hsv[:, :, 2], normalized_v)
    delta_sat = cv2.absdiff(ref_hsv[:, :, 1], normalized_sat)
    # Candidate regions emphasize localized chromatic change, not raw global motion.
    raw_mask = np.where((delta_sat > 42) | ((delta_v > 32) & (delta_sat > 24)), 255, 0).astype(np.uint8)
    h, w = raw_mask.shape
    floor_roi = np.zeros_like(raw_mask)
    floor_roi[int(h * 0.42):, :] = 255
    raw_mask = cv2.bitwise_and(raw_mask, floor_roi)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(raw_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

    count, labels, stats, centroids = cv2.connectedComponentsWithStats(mask, 8)
    regions: list[dict] = []
    min_area = max(300, int(h * w * 0.0025))
    max_area = int(h * w * 0.35)
    for i in range(1, count):
        x, y, rw, rh, area = map(int, stats[i])
        if area < min_area or area > max_area:
            continue
        component = labels[y:y + rh, x:x + rw] == i
        current_hsv_region = cur_hsv[y:y + rh, x:x + rw][component]
        # This is a weak visual descriptor, never a physical-cause classifier.
        water_tone_fraction = float(np.mean((current_hsv_region[:, 0] >= 82) &
                                            (current_hsv_region[:, 0] <= 125) &
                                            (current_hsv_region[:, 1] >= 50))) if len(current_hsv_region) else 0.0
        regions.append({
            "region_id": f"R{len(regions) + 1}", "bbox": [x, y, rw, rh], "pixel_area": area,
            "normalized_bbox": [round(x / w, 4), round(y / h, 4), round(rw / w, 4), round(rh / h, 4)],
            "cool_tone_fraction": round(water_tone_fraction, 4),
            "visual_cue": "localized cool-toned foreground change" if water_tone_fraction >= 0.25 else "localized chromatic foreground change",
        })
    regions.sort(key=lambda r: r["pixel_area"], reverse=True)
    changed_fraction = float(np.mean(mask > 0))
    overlay = warped.copy()
    tint = np.zeros_like(overlay)
    tint[:, :, 0] = 220
    tint[:, :, 2] = 180
    overlay[mask > 0] = cv2.addWeighted(overlay, 0.45, tint, 0.55, 0)[mask > 0]
    for region in regions:
        x, y, rw, rh = region["bbox"]
        cv2.rectangle(overlay, (x, y), (x + rw, y + rh), (190, 70, 250), 2)
        cv2.putText(overlay, region["region_id"], (x, max(18, y - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (190, 70, 250), 2)
    blur_scores = min(assess_quality(reference).quality_score, assess_quality(current).quality_score)
    reliability = float(np.clip((0.35 + 0.65 * reg_score) * blur_scores, 0, 1))
    if method == "identity_low_feature_fallback":
        reliability = min(reliability, 0.5)
    comparable = reliability >= 0.45
    if not comparable:
        notes.append("comparison validity is too low for confident region interpretation")
    return VisionComparison(comparable, method, inliers, round(reliability, 3), round(gain, 3),
                            round(changed_fraction, 5), regions, mask, overlay,
                            round((time.perf_counter() - started) * 1000, 3), notes)

