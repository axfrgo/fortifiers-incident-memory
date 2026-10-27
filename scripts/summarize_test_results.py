from __future__ import annotations

import json
import platform
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import cv2
import fastapi
import numpy
import pytest

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    xml_path = ROOT / "artifacts" / "test-results.xml"
    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    total = sum(int(suite.attrib.get("tests", 0)) for suite in suites)
    failures = sum(int(suite.attrib.get("failures", 0)) + int(suite.attrib.get("errors", 0)) for suite in suites)
    skipped = sum(int(suite.attrib.get("skipped", 0)) for suite in suites)
    test_cases = []
    for suite in suites:
        test_cases.extend({"name": f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}",
                           "status": "failed" if case.find("failure") is not None or case.find("error") is not None
                           else ("skipped" if case.find("skipped") is not None else "passed")}
                          for case in suite.findall("testcase"))
    result = {"generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "command": ".\\.venv\\Scripts\\python.exe -m pytest -q --junitxml=artifacts/test-results.xml",
              "exit_code": 0 if failures == 0 else 1,
              "summary": {"tests": total, "passed": total - failures - skipped,
                          "failed": failures, "skipped": skipped},
              "environment": {"python": platform.python_version(), "opencv": cv2.__version__,
                              "numpy": numpy.__version__, "fastapi": fastapi.__version__,
                              "pytest": pytest.__version__, "platform": platform.platform()},
              "tests": test_cases,
              "cloud_services_tested": False,
              "docker_build_tested": False}
    output = ROOT / "artifacts" / "test-results.json"
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "summary": result["summary"], "environment": result["environment"]}, indent=2))


if __name__ == "__main__":
    main()
