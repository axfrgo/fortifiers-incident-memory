from __future__ import annotations

import csv
import json
import platform
import statistics
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import psutil

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from incident_memory.agent import InvestigationAgent
from incident_memory.scenarios import fixture
from incident_memory.vision import align_and_compare, require_opencv5


EXPECTED = {
    "dry_normal": "no_visual_change_supported", "clear_change": "human_review_required",
    "poor_image": "retake_requested", "lighting_shift": "no_visual_change_supported",
    "historical_match": "no_new_change_supported", "camera_movement": "no_visual_change_supported",
    "occlusion_blur": "retake_requested",
}


def f1_metrics(prediction: np.ndarray, truth: np.ndarray) -> dict:
    pred, actual = prediction > 0, truth > 0
    tp = int(np.sum(pred & actual)); fp = int(np.sum(pred & ~actual)); fn = int(np.sum(~pred & actual))
    precision = tp / (tp + fp) if tp + fp else 1.0
    recall = tp / (tp + fn) if tp + fn else 1.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    union = int(np.sum(pred | actual))
    return {"tp_pixels": tp, "fp_pixels": fp, "fn_pixels": fn,
            "precision": round(precision, 5), "recall": round(recall, 5), "f1": round(f1, 5),
            "iou": round(tp / union, 5) if union else 1.0}


def main() -> None:
    require_opencv5()
    cases = list(EXPECTED)
    rows, durations, full_correct, onepass_correct, benign_fp = [], [], 0, 0, 0
    pixel_predictions, pixel_truths = [], []
    process = psutil.Process()
    rss_before = process.memory_info().rss
    cpu_before = process.cpu_times().user + process.cpu_times().system
    for scenario in cases:
        data = fixture(scenario, seed=26026)
        scenario_times = []
        final_report = None
        for _ in range(3):
            run = dict(data)
            run["event_id"] = f"eval-{scenario}"
            started = time.perf_counter()
            final_report = InvestigationAgent(run).run()
            scenario_times.append((time.perf_counter() - started) * 1000)
        assert final_report is not None
        durations.extend(scenario_times)
        expected = EXPECTED[scenario]
        full_ok = final_report["outcome"] == expected
        full_correct += int(full_ok)
        direct = align_and_compare(data["baseline"], data["current"])
        onepass = "human_review_required" if direct.candidate_regions else "no_visual_change_supported"
        onepass_ok = onepass == expected
        onepass_correct += int(onepass_ok)
        if scenario in {"dry_normal", "lighting_shift", "camera_movement", "occlusion_blur"} and direct.candidate_regions:
            benign_fp += 1
        quality_rejected = final_report["outcome"] in {"retake_requested", "comparison_rejected", "baseline_missing"}
        rows.append({"scenario": scenario, "expected_outcome": expected, "agent_outcome": final_report["outcome"],
                     "agent_action_correct": full_ok, "one_pass_outcome": onepass,
                     "one_pass_action_correct": onepass_ok, "tool_calls": len(final_report["trace"]),
                     "p50_latency_ms_3_runs": round(float(np.median(scenario_times)), 3),
                     "candidate_regions": len(final_report.get("regions") or []),
                     "quality_rejected": quality_rejected})
        if scenario in {"clear_change", "historical_match", "dry_normal", "lighting_shift"} and final_report.get("comparison"):
            mask_path = ROOT / "data" / "synthetic" / "held_out" / scenario / "truth_mask.png"
            truth = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            if truth is not None and final_report.get("comparison"):
                # Re-run the detector to retain the actual OpenCV output mask for pixel metrics.
                pixel_predictions.append(direct.mask > 0)
                pixel_truths.append(truth > 0)

    aggregate_pred = np.concatenate([x.ravel() for x in pixel_predictions])
    aggregate_truth = np.concatenate([x.ravel() for x in pixel_truths])
    pixel_metrics = f1_metrics(aggregate_pred, aggregate_truth)
    rss_after = process.memory_info().rss
    cpu_after = process.cpu_times().user + process.cpu_times().system
    benign_count = 4
    result = {
        "title": "Held-out procedural synthetic mechanical-room evaluation",
        "run_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "environment": {"python": platform.python_version(), "opencv": cv2.__version__,
                        "numpy": np.__version__, "platform": platform.platform(), "cpu_count": psutil.cpu_count()},
        "dataset": {"split": "held_out", "seed": 26026, "scenario_count": len(cases),
                    "agent_runs": len(cases) * 3, "pixel_scored_scenarios": len(pixel_truths),
                    "provenance": "synthetic procedural drawings created by scripts/build_dataset.py"},
        "workflow": {"full_agent_action_correct": full_correct, "full_agent_action_accuracy": round(full_correct / len(cases), 5),
                     "one_pass_action_correct": onepass_correct, "one_pass_action_accuracy": round(onepass_correct / len(cases), 5),
                     "benign_scenarios_with_one_pass_candidate": benign_fp, "benign_scenario_count": benign_count,
                     "unnecessary_retake_requests": sum(r["quality_rejected"] and EXPECTED[r["scenario"]] != "retake_requested" for r in rows),
                     "mean_agent_tool_calls": round(statistics.mean(r["tool_calls"] for r in rows), 3)},
        "pixel_region_metrics": pixel_metrics,
        "latency_ms": {"n": len(durations), "p50": round(float(np.percentile(durations, 50)), 3),
                       "p95": round(float(np.percentile(durations, 95)), 3), "mean": round(statistics.mean(durations), 3)},
        "resource_observations": {"rss_before_mb": round(rss_before / 1024**2, 2),
                                  "rss_after_mb": round(rss_after / 1024**2, 2),
                                  "rss_delta_mb": round((rss_after-rss_before) / 1024**2, 2),
                                  "process_cpu_seconds": round(cpu_after-cpu_before, 3)},
        "cases": rows,
        "limitations": ["Synthetic fixtures share a procedural scene generator; results do not estimate field performance.",
                        "The one-pass comparator is a simple no-history/no-quality/no-sensor decision rule.",
                        "Pixel masks mark a staged color patch and are not labels for real water or leak cause."],
    }
    out = ROOT / "artifacts" / "evaluation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (ROOT / "artifacts" / "evaluation-cases.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    bars = []
    for i, row in enumerate(rows):
        y = 42 + i * 33
        width1 = 260 if row["agent_action_correct"] else 20
        width2 = 260 if row["one_pass_action_correct"] else 20
        bars.append(f'<text x="10" y="{y+12}" font-size="11">{row["scenario"]}</text><rect x="150" y="{y}" width="{width1}" height="10" fill="#7152c7"/><rect x="150" y="{y+13}" width="{width2}" height="8" fill="#b8b1c2"/>')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="450" height="290" viewBox="0 0 450 290"><text x="150" y="20" font-family="sans-serif" font-size="12">Task/action correctness by fixture (full bar = correct)</text>' + ''.join(bars) + '<rect x="150" y="270" width="12" height="8" fill="#7152c7"/><text x="168" y="278" font-size="10">Full workflow</text><rect x="255" y="270" width="12" height="8" fill="#b8b1c2"/><text x="273" y="278" font-size="10">One-pass</text></svg>'
    (ROOT / "artifacts" / "task-correctness.svg").write_text(svg, encoding="utf-8")
    print(json.dumps({"evaluation_json": str(out), "cases": len(cases), "agent_runs": len(durations),
                      "full_agent_accuracy": result["workflow"]["full_agent_action_accuracy"],
                      "one_pass_accuracy": result["workflow"]["one_pass_action_accuracy"],
                      "pixel_metrics": pixel_metrics, "latency_ms": result["latency_ms"]}, indent=2))


if __name__ == "__main__":
    main()
