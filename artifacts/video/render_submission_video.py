"""Render the recorded local UI capture into a silent, captioned demo MP4.

All live application footage comes from 01-live-demo.mp4. Cards and subtitles
are editorial labels; no demo output is synthesized or altered.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
VIDEO_DIR = ROOT / "artifacts" / "video"
SOURCE = VIDEO_DIR / "01-live-demo.mp4"
OUTPUT = VIDEO_DIR / "fortifiers-incident-memory-demo.mp4"
WIDTH, HEIGHT, FPS = 1920, 1080, 15
TOP, MAIN_H, BOTTOM = 78, 864, 138
BG = (20, 19, 27)
PURPLE = (125, 88, 216)
LAVENDER = (192, 172, 255)
WHITE = (248, 247, 252)
MUTED = (192, 189, 205)
GREEN = (81, 177, 141)
AMBER = (224, 169, 77)

FONT_REG = r"C:\Windows\Fonts\segoeui.ttf"
FONT_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
font_title = ImageFont.truetype(FONT_BOLD, 66)
font_subtitle = ImageFont.truetype(FONT_REG, 35)
font_heading = ImageFont.truetype(FONT_BOLD, 34)
font_body = ImageFont.truetype(FONT_REG, 27)
font_small = ImageFont.truetype(FONT_REG, 22)
font_metric = ImageFont.truetype(FONT_BOLD, 38)
font_step = ImageFont.truetype(FONT_BOLD, 25)


def rgb(color: tuple[int, int, int]) -> tuple[int, int, int]:
    return color[2], color[1], color[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
         max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and draw.textbbox((0, 0), candidate, font=font)[2] > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def text_lines(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
               font: ImageFont.FreeTypeFont, fill: tuple[int, int, int],
               max_width: int, line_gap: int = 11) -> int:
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def base_card(kicker: str) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, WIDTH, 10), fill=rgb(PURPLE))
    d.text((92, 55), kicker.upper(), font=font_small, fill=rgb(LAVENDER))
    d.line((92, 105, WIDTH - 92, 105), fill=(62, 59, 74), width=2)
    return im, d


def card_intro() -> Image.Image:
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 18, HEIGHT), fill=rgb(PURPLE))
    d.rounded_rectangle((108, 116, 1812, 966), radius=32,
                        fill=(27, 25, 38), outline=(69, 62, 94), width=2)
    d.text((178, 212), "OPENCV AI COMPETITION 2026", font=font_small,
           fill=rgb(LAVENDER))
    d.text((172, 298), "FORTIFIERS", font=font_title, fill=rgb(WHITE))
    d.text((172, 382), "INCIDENT MEMORY", font=font_title, fill=rgb(LAVENDER))
    d.text((178, 499), "Give the Physical World a Memory.", font=font_subtitle,
           fill=rgb(WHITE))
    d.rounded_rectangle((178, 610, 582, 672), radius=20,
                        fill=(44, 40, 60), outline=(86, 74, 122), width=2)
    d.text((205, 625), "SOLO ENTRY  ·  DEMO BUILD", font=font_small,
           fill=rgb(WHITE))
    d.text((178, 760), "All incidents and frames shown are synthetic test fixtures.",
           font=font_small, fill=rgb(MUTED))
    d.text((178, 801), "The recording shows the local application; AWS is not deployed.",
           font=font_small, fill=rgb(AMBER))
    return im


def card_architecture() -> Image.Image:
    im, d = base_card("System architecture · status disclosed")
    d.text((92, 136), "From alarm to reviewable evidence", font=font_heading,
           fill=rgb(WHITE))
    steps = [
        ("1  INPUT", "Camera frames\n+ sensor event"),
        ("2  MEMORY", "Camera + time\n+ baseline match"),
        ("3  OPENCV 5", "ORB / RANSAC\n+ normalized change"),
        ("4  AGENT", "Observation picks\n+ next tool"),
        ("5  REPORT", "Hashes + trace\n+ human review"),
    ]
    x0, y0, box_w, box_h, gap = 92, 248, 316, 224, 36
    for i, (label, body) in enumerate(steps):
        x = x0 + i * (box_w + gap)
        d.rounded_rectangle((x, y0, x + box_w, y0 + box_h), radius=22,
                            fill=(32, 30, 44), outline=rgb(PURPLE if i in (2, 3) else (82, 78, 97)), width=3)
        d.text((x + 22, y0 + 25), label, font=font_small,
               fill=rgb(LAVENDER if i in (2, 3) else MUTED))
        for n, line in enumerate(body.splitlines()):
            d.text((x + 22, y0 + 93 + n * 43), line, font=font_step,
                   fill=rgb(WHITE))
        if i < len(steps) - 1:
            yy = y0 + box_h // 2
            x1 = x + box_w + 6
            x2 = x + box_w + gap - 6
            d.line((x1, yy, x2, yy), fill=rgb(LAVENDER), width=4)
            d.polygon([(x2, yy), (x2 - 12, yy - 9), (x2 - 12, yy + 9)],
                      fill=rgb(LAVENDER))
    d.rounded_rectangle((92, 536, 1828, 726), radius=18,
                        fill=(31, 39, 38), outline=(59, 116, 94), width=2)
    d.text((124, 559), "VERIFIED IN THIS LOCAL CAPTURE", font=font_small,
           fill=rgb(GREEN))
    text_lines(d, 124, 600,
               "FastAPI + OpenCV 5.0.0 + bounded agent controller + local evidence reports.",
               font_body, rgb(WHITE), 1640)
    d.rounded_rectangle((92, 764, 1828, 948), radius=18,
                        fill=(41, 35, 30), outline=(133, 95, 48), width=2)
    d.text((124, 787), "AWS COMPONENTS PREPARED, NOT DEPLOYED", font=font_small,
           fill=rgb(AMBER))
    text_lines(d, 124, 828,
               "App Runner / S3 / CloudWatch are documented infrastructure only. No AWS request was run for this demo.",
               font_body, rgb(WHITE), 1640)
    return im


def card_evaluation() -> Image.Image:
    im, d = base_card("Measured local evaluation · synthetic only")
    d.text((92, 136), "What the fixtures show", font=font_heading,
           fill=rgb(WHITE))
    items = [
        ("7 / 7", "expected actions\nfull workflow"),
        ("4 / 7", "expected actions\none-pass reference"),
        ("0.99546", "pixel mask F1\n4 synthetic masks"),
        ("137 / 217 ms", "controller p50 / p95\n21 runs"),
    ]
    xs = [92, 526, 960, 1394]
    for (value, label), x in zip(items, xs):
        d.rounded_rectangle((x, 236, x + 390, 440), radius=22,
                            fill=(32, 30, 44), outline=(80, 72, 105), width=2)
        d.text((x + 25, 273), value, font=font_metric, fill=rgb(LAVENDER))
        for n, line in enumerate(label.splitlines()):
            d.text((x + 26, 340 + n * 35), line, font=font_small,
                   fill=rgb(MUTED))
    d.rounded_rectangle((92, 495, 1828, 689), radius=18,
                        fill=(31, 39, 38), outline=(59, 116, 94), width=2)
    d.text((124, 518), "AUTOMATED REGRESSION", font=font_small,
           fill=rgb(GREEN))
    text_lines(d, 124, 560,
               "36 tests passed in the recorded finalization run. See the repository for exact commands and machine-readable results.",
               font_body, rgb(WHITE), 1640)
    d.rounded_rectangle((92, 728, 1828, 948), radius=18,
                        fill=(41, 35, 30), outline=(133, 95, 48), width=2)
    d.text((124, 750), "LIMITS", font=font_small, fill=rgb(AMBER))
    text_lines(d, 124, 792,
               "Procedurally generated scenes only. No field images, real leak validation, customer study, or independent expert labels. Pixel F1 is not a water classifier score.",
               font_body, rgb(WHITE), 1640)
    return im


def card_close() -> Image.Image:
    im = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, WIDTH, 10), fill=rgb(PURPLE))
    d.text((112, 152), "FORTIFIERS INCIDENT MEMORY", font=font_small,
           fill=rgb(LAVENDER))
    text_lines(d, 112, 261,
               "An alarm tells you something happened. Incident Memory shows what changed, what the evidence supports, and what should happen next.",
               font_title, rgb(WHITE), 1650, 20)
    d.line((112, 673, 1808, 673), fill=(68, 64, 80), width=2)
    d.text((112, 725), "Synthetic local demo · human review required · AWS not deployed",
           font=font_subtitle, fill=rgb(AMBER))
    d.text((112, 856), "OpenCV AI Competition 2026  ·  Solo entry", font=font_small,
           fill=rgb(MUTED))
    return im


def as_bgr(im: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR)


def add_live_bars(frame: np.ndarray, second: float) -> np.ndarray:
    app = cv2.resize(frame, (WIDTH, MAIN_H), interpolation=cv2.INTER_AREA)
    canvas = np.full((HEIGHT, WIDTH, 3), BG, dtype=np.uint8)
    canvas[TOP:TOP + MAIN_H] = app
    rgb_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(rgb_image)
    d.text((54, 20), "FORTIFIERS INCIDENT MEMORY", font=font_small,
           fill=rgb(WHITE))
    d.text((WIDTH - 390, 20), "LOCAL DEMO  ·  OpenCV 5.0.0", font=font_small,
           fill=rgb(LAVENDER))
    d.line((54, TOP - 1, WIDTH - 54, TOP - 1), fill=(82, 76, 98), width=2)
    d.line((54, TOP + MAIN_H, WIDTH - 54, TOP + MAIN_H), fill=(82, 76, 98), width=2)
    if second < 20:
        label = "SYNTHETIC EVENT"
        caption = "Choose a scenario and trigger an alarm-associated visual investigation."
    elif second < 77:
        label = "VISIBLE CHANGE + SENSOR"
        caption = "OpenCV localizes a new region; a time-aligned sensor changes the agent's next action."
    elif second < 104:
        label = "INSUFFICIENT EVIDENCE"
        caption = "Blur fails the quality gate; the agent requests another image and withholds comparison."
    elif second < 143:
        label = "BENIGN LIGHTING SHIFT"
        caption = "Illumination-normalized comparison finds no qualifying localized change."
    elif second < 183.4:
        label = "HISTORICAL MEMORY"
        caption = "An older frame contains a similar mark, weakening the claim that it is new."
    else:
        label = "EVIDENCE REPORT"
        caption = "Reports include trace entries, evidence classifications and SHA-256 hashes."
    pill = (WIDTH - 54 - 28 - d.textbbox((0, 0), label, font=font_small)[2], 15,
            WIDTH - 54, 56)
    d.rounded_rectangle(pill, radius=18, fill=(48, 42, 67), outline=(95, 77, 143), width=1)
    d.text((pill[0] + 14, 23), label, font=font_small, fill=rgb(LAVENDER))
    text_lines(d, 54, TOP + MAIN_H + 28, caption, font_body, rgb(WHITE), WIDTH - 108, 6)
    # Subtle progress line, included only as an editorial guide.
    d.rectangle((54, HEIGHT - 10, WIDTH - 54, HEIGHT - 7), fill=(63, 59, 72))
    d.rectangle((54, HEIGHT - 10, 54 + int((WIDTH - 108) * min(second / 183.4, 1)), HEIGHT - 7),
                fill=rgb(PURPLE))
    return cv2.cvtColor(np.asarray(rgb_image), cv2.COLOR_RGB2BGR)


def write_still(writer: cv2.VideoWriter, image: Image.Image, seconds: float) -> None:
    frame = as_bgr(image)
    for _ in range(round(seconds * FPS)):
        writer.write(frame)


def main() -> None:
    capture = cv2.VideoCapture(str(SOURCE))
    if not capture.isOpened():
        raise SystemExit(f"Cannot open recorded source: {SOURCE}")
    source_fps = capture.get(cv2.CAP_PROP_FPS)
    source_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    source_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if round(source_fps) != FPS or source_width <= 0 or source_height <= 0:
        raise SystemExit("Unexpected source properties; inspect the recorded MP4 before editing.")
    writer = cv2.VideoWriter(str(OUTPUT), cv2.VideoWriter_fourcc(*"mp4v"),
                             FPS, (WIDTH, HEIGHT))
    if not writer.isOpened():
        raise SystemExit("OpenCV could not initialize the final MP4 writer.")
    write_still(writer, card_intro(), 7)
    for index in range(source_frames):
        ok, frame = capture.read()
        if not ok:
            raise SystemExit(f"Source decode stopped unexpectedly at frame {index}.")
        writer.write(add_live_bars(frame, index / source_fps))
    write_still(writer, card_architecture(), 12)
    write_still(writer, card_evaluation(), 12)
    write_still(writer, card_close(), 6)
    capture.release()
    writer.release()
    check = cv2.VideoCapture(str(OUTPUT))
    if not check.isOpened():
        raise SystemExit("Final MP4 could not be reopened for verification.")
    frame_count = int(check.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = check.get(cv2.CAP_PROP_FPS)
    width = int(check.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(check.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ok, sample = check.read()
    check.release()
    if not ok or (width, height, round(fps)) != (WIDTH, HEIGHT, FPS):
        raise SystemExit("Final MP4 failed dimensions/FPS/frame decode verification.")
    duration = frame_count / fps
    if duration > 300:
        raise SystemExit(f"Final video exceeds five minutes: {duration:.2f}s")
    result = {
        "source": SOURCE.name,
        "output": OUTPUT.name,
        "source_fps": source_fps,
        "source_frames": source_frames,
        "source_duration_seconds": round(source_frames / source_fps, 2),
        "output_fps": fps,
        "output_frames": frame_count,
        "output_width": width,
        "output_height": height,
        "duration_seconds": round(duration, 2),
        "silent": True,
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
        "output_bytes": OUTPUT.stat().st_size,
        "opencv_render_version": cv2.__version__,
        "claims": "Local synthetic demonstration; AWS deployment not verified; no real-world leak validation.",
    }
    (VIDEO_DIR / "video-manifest.json").write_text(json.dumps(result, indent=2) + "\n",
                                                   encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
