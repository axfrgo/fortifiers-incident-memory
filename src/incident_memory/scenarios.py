from __future__ import annotations

from datetime import datetime, timedelta, timezone

import cv2
import numpy as np


SCENARIOS = {
    "dry_normal": "No scene change; normal dry frame",
    "clear_change": "Localized new cool-toned floor change with an active water sensor",
    "poor_image": "Blurred alarm frame; no replacement frame is available",
    "lighting_shift": "Global illumination change without localized chromatic evidence; sensor inactive",
    "historical_match": "Alarm-time mark resembles a region in an older frame; latest prior frame is clear",
    "camera_movement": "Camera shifted slightly; registration should suppress global displacement",
    "occlusion_blur": "Blurred and partly occluded alarm frame",
}


def _base(seed: int = 26026) -> np.ndarray:
    h, w = 480, 640
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = (174, 184, 191)
    cv2.rectangle(img, (0, 255), (w, h), (118, 124, 127), -1)
    # Low-amplitude texture supplies realistic ORB correspondences without using assets.
    rng = np.random.default_rng(seed)
    noise = rng.integers(-5, 6, size=(h, w, 1), dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.line(img, (0, 255), (w, 255), (75, 82, 87), 4)
    for x in range(0, w, 80):
        cv2.line(img, (x, 260), (x, h), (101, 107, 111), 1)
    for y in range(300, h, 55):
        cv2.line(img, (0, y), (w, y), (104, 110, 113), 1)
    # Pipes, pump, valve and instrument cabinet form stable scene context.
    cv2.rectangle(img, (65, 75), (178, 250), (82, 91, 96), -1)
    cv2.rectangle(img, (76, 90), (166, 232), (119, 129, 134), 3)
    cv2.circle(img, (122, 153), 34, (196, 201, 203), 4)
    cv2.circle(img, (122, 153), 6, (49, 61, 69), -1)
    cv2.rectangle(img, (405, 56), (440, 255), (180, 182, 177), -1)
    cv2.rectangle(img, (400, 56), (445, 256), (93, 100, 101), 3)
    cv2.rectangle(img, (470, 112), (585, 252), (94, 103, 108), -1)
    cv2.rectangle(img, (480, 122), (575, 240), (157, 165, 168), 2)
    cv2.line(img, (0, 54), (405, 54), (73, 87, 93), 13)
    cv2.line(img, (190, 54), (190, 202), (67, 82, 88), 12)
    cv2.line(img, (186, 198), (284, 198), (68, 83, 89), 12)
    cv2.circle(img, (287, 198), 18, (62, 77, 84), -1)
    cv2.line(img, (276, 198), (298, 198), (210, 164, 48), 5)
    cv2.putText(img, "PUMP 01", (82, 222), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (30, 39, 43), 2)
    return img


def _spill(image: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    out = image.copy()
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    polygon = np.array([[227, 356], [254, 329], [300, 335], [332, 352], [370, 369], [365, 396],
                        [327, 411], [278, 405], [241, 386]], dtype=np.int32)
    cv2.fillPoly(mask, [polygon], 255)
    tint = np.zeros_like(out)
    tint[:] = (192, 143, 70)  # blue-green BGR cue; only synthetic fixture pixels.
    soft_mask = cv2.GaussianBlur(mask, (11, 11), 2.0)
    alpha = (soft_mask.astype(np.float32) / 255.0 * 0.72)[:, :, None]
    out = np.clip(out.astype(np.float32) * (1 - alpha) + tint.astype(np.float32) * alpha, 0, 255).astype(np.uint8)
    # Bright reflections are part of the visibly staged texture.
    cv2.ellipse(out, (292, 368), (23, 7), -8, 0, 360, (225, 203, 147), 2, cv2.LINE_AA)
    return out, mask


def fixture(scenario: str, *, seed: int = 26026) -> dict:
    if scenario not in SCENARIOS:
        raise KeyError(scenario)
    base = _base(seed)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    camera = "mechanical-room-cam-01"
    normal = base.copy()
    older = None
    truth = np.zeros(base.shape[:2], dtype=np.uint8)
    sensor_active = False
    sensor_type = "water_contact"
    event_image = base.copy()
    if scenario == "dry_normal":
        pass
    elif scenario == "clear_change":
        event_image, truth = _spill(base)
        sensor_active = True
    elif scenario == "poor_image":
        event_image = cv2.GaussianBlur(base, (41, 41), 0)
    elif scenario == "lighting_shift":
        event_image = np.clip(base.astype(np.int16) + 38, 0, 255).astype(np.uint8)
    elif scenario == "historical_match":
        older, truth = _spill(base)
        event_image, _ = _spill(base)
    elif scenario == "camera_movement":
        matrix = np.float32([[1, 0, 18], [0, 1, -9]])
        event_image = cv2.warpAffine(base, matrix, (base.shape[1], base.shape[0]), borderMode=cv2.BORDER_REFLECT)
    elif scenario == "occlusion_blur":
        event_image = cv2.GaussianBlur(base, (25, 25), 0)
        cv2.rectangle(event_image, (0, 280), (115, 479), (35, 40, 42), -1)
    return {
        "scenario": scenario, "description": SCENARIOS[scenario], "camera_id": camera,
        "event_id": f"demo-{scenario}", "event_time": now,
        "baseline_time": now - timedelta(minutes=15), "older_time": now - timedelta(days=7),
        "baseline": normal, "current": event_image, "older": older, "truth_mask": truth,
        "sensor": {"type": sensor_type, "active": sensor_active, "timestamp": now.isoformat(),
                   "source": "synthetic-demo-sensor"},
        "synthetic": True,
    }

