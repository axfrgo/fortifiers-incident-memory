from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient
from incident_memory.api import app
from incident_memory.scenarios import SCENARIOS


def main() -> None:
    manifest = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "synthetic": True, "cases": []}
    with TestClient(app) as client:
        for scenario_id in SCENARIOS:
            response = client.get(f"/api/investigate/{scenario_id}")
            response.raise_for_status()
            report = response.json()
            run_id = report["run_storage_id"]
            manifest["cases"].append({
                "scenario": scenario_id,
                "description": SCENARIOS[scenario_id],
                "outcome": report["outcome"],
                "run_storage_id": run_id,
                "trace": [{"iteration": step["iteration"],
                           "observation_inputs": step["observation_inputs"],
                           "thresholds": step["thresholds"],
                           "selected_action": step["selected_action"],
                           "evidence_references": step["evidence_references"],
                           "result": step["result"], "error": step["error"],
                           "stopping_condition": step["stopping_condition"]}
                          for step in report["trace"]],
                "evidence_sha256": report["sha256"],
                "artifact_directory": f"artifacts/demo/{run_id}",
                "report_url_local": report["html_report_url"],
            })
    output = ROOT / "artifacts" / "demo-cases.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"manifest": str(output), "synthetic_cases": len(manifest["cases"]),
                      "outcomes": {case["scenario"]: case["outcome"] for case in manifest["cases"]}}, indent=2))


if __name__ == "__main__":
    main()
