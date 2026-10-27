# Fortifiers Incident Memory

Environmental Incident Memory investigates what changed around a physical alarm. It retrieves a pre-event frame, runs real OpenCV 5 image analysis, chooses follow-up actions from those observations, checks older history and sensor timing, and creates a reviewable evidence record. The demo focuses on a synthetic industrial mechanical-room water-sensor event.

> **Honest build status:** the local application and OpenCV 5 workflow are implemented and tested. AWS and Docker are **not deployed or verified**: the workspace has no Docker/AWS CLI or configured AWS credentials, and the owner requested deployment preparation only. This means the build does not yet meet the competition's mandatory AWS component and judge-accessible endpoint requirement. See [deployment-manifest.json](deployment-manifest.json).

All included images and sensor events are procedurally generated synthetic fixtures. The blue/cool-toned patch is a staged visual cue, not actual water and not real-world validation.

## Run locally

Verified here with Python 3.14.0, OpenCV 5.0.0.93 and NumPy 2.5.4 on Windows 10. Python 3.11+ is specified in the container configuration, but a Python 3.11 or Docker build was not verified in this workspace.

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe -m uvicorn incident_memory.api:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000`. Select a synthetic scenario and choose **Run investigation**. The dashboard shows a draggable comparison, candidate overlays, time history, actual completed tool trace, evidence classes, report downloads and review controls. `GET /health` must report an OpenCV 5 version.

For a direct check from another PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/api/investigate/clear_change
```

Local authorized image uploads are available in the interface and limited to PNG/JPEG/WebP, 17 MiB total request size, 8 MiB per image and 12 MP decoded dimensions. OpenCV 5 DNN YuNet blurs detected faces; this does not find every face or other sensitive identifier. Upload processing fails closed if the model or inference is unavailable. Do not upload images without rights/consent or containing unredacted sensitive information. The prepared AWS configuration disables user image uploads.

## Rebuild data, evaluate, test

```powershell
$env:PYTHONPATH = 'src'
.\.venv\Scripts\python.exe scripts\build_dataset.py
.\.venv\Scripts\python.exe scripts\evaluate.py
.\.venv\Scripts\python.exe -m pytest -q --junitxml=artifacts/test-results.xml
.\.venv\Scripts\python.exe scripts\summarize_test_results.py
.\.venv\Scripts\python.exe scripts\export_demo_cases.py
.\.venv\Scripts\python.exe scripts\package_source.py
```

`artifacts/evaluation.json`, `artifacts/evaluation-cases.csv` and `artifacts/task-correctness.svg` are measured results from the recorded run, not production performance. The final test output is in `artifacts/test-results.xml` and `artifacts/test-results.json`; `artifacts/demo-cases.json` points to each actual synthetic report, trace and overlay. The portable archive is `artifacts/fortifiers-incident-memory-source.zip`. Detailed limitations are in [EVALUATION.md](EVALUATION.md).

## Deployment

The deployment package uses a Docker image in private ECR, App Runner to execute the same OpenCV 5 API, and a private versioned S3 bucket for synthetic evidence. The stack enables SSE-S3, public access blocking, scoped instance-role access, public HTTPS for judge access, and disables real-image uploads. **Nothing has been created in AWS.** A later authorized deployment requires Docker, AWS CLI/role, a selected region and explicit billable-resource approval. See [DEPLOYMENT.md](DEPLOYMENT.md) and `deployment/deploy.ps1`.

## Project map

- `src/incident_memory/vision.py` — OpenCV 5 validation, quality, registration, normalized difference, regions and overlays.
- `src/incident_memory/memory.py` — timestamped camera/context memory and baseline contamination safeguards.
- `src/incident_memory/agent.py` — bounded observation-driven tool policy, trace and evidence report.
- `src/incident_memory/api.py` — local FastAPI UI/API, validated uploads and review record.
- `src/incident_memory/static/` — accessible responsive dashboard.
- `data/synthetic/` — generated tuning/held-out fixtures, masks and manifest.
- `tests/` — vision, memory, agent, API and storage failure tests.
- `submission/` — architecture and workflow SVG diagrams.

See [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md), [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md), and [BUILD_LEDGER.md](BUILD_LEDGER.md). The submission wording and video storyboard contain explicit placeholders where actual team identity, hosted links and AWS verification are still needed.

