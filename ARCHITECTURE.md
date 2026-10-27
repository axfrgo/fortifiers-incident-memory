# Architecture

Fortifiers Incident Memory is an event-triggered, bounded visual investigation service. The verified runtime in this workspace is local Python 3.14.0 with OpenCV 5.0.0.93. The App Runner and S3 portion shown in purple is prepared infrastructure only; it has not been deployed. AWS currently says App Runner is closed to new customers, and this account's eligibility is unknown. See [deployment-manifest.json](deployment-manifest.json) and [DEPLOYMENT.md](DEPLOYMENT.md).

![Architecture showing verified local OpenCV 5 processing and planned App Runner/S3 components](submission/architecture.svg)

## Data and trust boundaries

1. A synthetic water-contact event selects a camera and alarm frame. The optional local upload API checks media type, total request size (17 MiB), per-image size (8 MiB), decoded dimensions (maximum 12 megapixels), color decoding and resolution compatibility. Decoding/re-encoding removes source metadata. OpenCV 5 DNN FaceDetectorYN uses the included YuNet model to blur detected faces. If the model or inference fails, upload processing stops; detection can still miss faces and other identifiers. The prepared cloud deployment disables user uploads.
2. `IncidentMemory` indexes frames by camera, context and timezone-aware timestamp. It picks the nearest usable pre-event frame and excludes frames marked as incidents from baseline selection.
3. OpenCV 5 evaluates blur/exposure, attempts ORB feature matching and a RANSAC homography, falls back to ECC translation, normalizes global brightness in HSV, thresholds localized chromatic change, applies morphology and extracts connected-component regions.
4. The bounded controller uses these measurements to choose what it does next. A new region can trigger region inspection and older-frame retrieval. Poor quality requests a retake. A similar older region downgrades novelty. A sensor is considered correlated only if active and within the time window.
5. The report labels observations separately from sensor correlation, hypothesis and unverified cause. It includes trace records, PNGs, SHA-256 hashes and operator review controls. Review records are acknowledgements only; no physical-control interface exists.
6. Locally, files are saved under `artifacts/demo/`. The prepared AWS version would run the same FastAPI/OpenCV process in App Runner, write synthetic evidence bundles to a private, versioned S3 bucket, and serve a public demo endpoint. CloudWatch would receive application/service logs. AWS resource creation and live verification remain blocked by missing tools/credentials and the user's instruction to prepare only. The template may be used only if the account already has App Runner access; the recommended alternative for new AWS customers has not been implemented.

## Components

| Component | Location | Responsibility |
|---|---|---|
| Ingestion and HTTP API | `src/incident_memory/api.py` | Health, scenarios, safe image upload, investigation, downloadable artifacts, review capture |
| Environmental memory | `src/incident_memory/memory.py` | Time/camera/context filtering, duplicate event detection, incident exclusion |
| OpenCV 5 perception | `src/incident_memory/vision.py` | Decode, quality, registration, illumination normalization, candidate masks and geometry |
| Agent controller | `src/incident_memory/agent.py` | Bounded observation-driven tool routing and fail-closed reports |
| Reports | `src/incident_memory/reports.py` | Accessible HTML evidence report |
| Cloud | `src/incident_memory/cloud.py`, `deployment/stack.yaml` | Optional S3 evidence persistence and App Runner/IAM resources |
| Frontend | `src/incident_memory/static/` | Responsive scenario dashboard, image slider, trace and human review |
| Evaluation | `scripts/evaluate.py`, `data/synthetic/` | Labeled procedural fixture set and measured comparator |

## API

- `GET /health` — reports service and OpenCV version.
- `GET /api/scenarios` — lists clearly synthetic test cases.
- `GET /api/investigate/{scenario_id}` — runs the actual OpenCV and agent path.
- `POST /api/investigate/upload` — local-only default for authorized images; disabled in the prepared cloud template.
- `POST /api/review/{run_id}` — records an acknowledgement, rejection or request for more evidence; it does not actuate equipment.
- `GET /artifacts/{run_id}/{filename}` — local run artifacts.

