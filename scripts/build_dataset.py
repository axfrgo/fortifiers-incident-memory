from __future__ import annotations

import csv
import sys
from pathlib import Path

import cv2

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from incident_memory.scenarios import SCENARIOS, fixture


def main() -> None:
    records = []
    for split, seed in (("tuning", 26025), ("held_out", 26026)):
        for scenario in SCENARIOS:
            item = fixture(scenario, seed=seed)
            folder = ROOT / "data" / "synthetic" / split / scenario
            folder.mkdir(parents=True, exist_ok=True)
            for name in ("baseline", "current", "truth_mask"):
                cv2.imwrite(str(folder / f"{name}.png"), item[name])
            if item["older"] is not None:
                cv2.imwrite(str(folder / "older.png"), item["older"])
            records.append({"split": split, "seed": seed, "scenario": scenario,
                            "baseline": f"{split}/{scenario}/baseline.png",
                            "alarm_frame": f"{split}/{scenario}/current.png",
                            "ground_truth_mask": f"{split}/{scenario}/truth_mask.png",
                            "older_frame": f"{split}/{scenario}/older.png" if item["older"] is not None else "",
                            "expected_visual_change": scenario in {"clear_change", "historical_match"},
                            "expected_agent_outcome": {
                                "clear_change": "human_review_required", "poor_image": "retake_requested",
                                "occlusion_blur": "retake_requested", "historical_match": "no_new_change_supported",
                                "lighting_shift": "no_visual_change_supported", "dry_normal": "no_visual_change_supported",
                                "camera_movement": "no_visual_change_supported"}[scenario],
                            "provenance": "procedurally generated synthetic OpenCV drawing; no third-party imagery"})
    with (ROOT / "data" / "synthetic" / "manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Wrote {len(records)} labeled synthetic fixture sets to data/synthetic/manifest.csv")


if __name__ == "__main__":
    main()
