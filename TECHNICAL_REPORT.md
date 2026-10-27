# Technical report — Fortifiers Incident Memory

## Problem and users

Industrial maintenance and facility teams often receive a binary sensor alarm without an easy account of what visibly changed at the location. Fortifiers Incident Memory is a decision-support prototype that compares an alarm-time RGB frame to the camera's visual history, relates it to a timestamped sensor event, and records observable evidence and uncertainty. Intended users are facility operators and maintenance staff. The demonstrator is restricted to synthetic mechanical-room frames and a simulated water-contact sensor.

## System design

The flow is: event/frame retrieval → image-quality gate → camera/context/time baseline selection → registration and comparison → region inspection → optional older-history retrieval → sensor correlation → a human review or retake recommendation → hashed report. [Architecture](ARCHITECTURE.md) and [agent workflow](AGENT_WORKFLOW.md) have exported SVG diagrams.

The Python modules have separately callable interfaces for vision, memory, agent decisions, reports, API and cloud persistence. FastAPI serves a local dashboard, health endpoint, synthetic scenario API, size/type-limited image-pair API, report files and audit-only human-review actions. The UI shows synthetic provenance, a before/after slider, timeline, annotation, evidence classifications and trace.

## OpenCV 5 implementation

Runtime startup rejects a non-5 major version. The pinned wheel is `opencv-python-headless==5.0.0.93`; the inspected Python runtime reports `cv2.__version__ == 5.0.0`.

The engine uses `imdecode` for validation, `Laplacian` variance and exposure statistics for image quality, ORB descriptors with Hamming ratio matching and `findHomography(..., RANSAC, ...)` for registration, ECC translation fallback, HSV V-channel gain normalization, saturation/value differences, ROI masking, opening/closing morphology, connected components, geometry, overlays and PNG encoding. A weak cool-tone fraction is a visual descriptor only. Reliability and quality values are heuristics, not calibrated probabilities.

Resolution mismatches fail closed. Low-feature registration retains an identity fallback only with reduced reliability. Incident-marked frames are excluded from baseline selection. The image quality check gates poor frames before the change detector. An older image may change the final novelty assessment based on OpenCV pixel similarity in the candidate crop.

## AWS implementation and status

The deployable design uses a Python 3.11 container in private ECR and AWS App Runner, where the actual FastAPI/OpenCV workload would run. App Runner has a health check and an instance role scoped to the evidence key prefix of a private versioned S3 bucket. S3 applies SSE-S3 and blocks public access. The application generates a presigned one-hour bundle URL after saving evidence. The public service is restricted to synthetic scenarios; `ALLOW_USER_UPLOADS=false` is set in the template. App Runner service logs would flow to CloudWatch.

No AWS resource or Docker image was created. Environment inspection found no AWS CLI, Docker CLI, AWS environment credentials, or local AWS profile. The owner chose “prepare the deployment only; do not create AWS resources.” Therefore there is no AWS execution evidence, public endpoint, remote health response or cloud cost measurement. This is a material unmet requirement, not an implied deployment.

## Evaluation

`scripts/build_dataset.py` generates 14 fixture sets: seven scenario types in tuning seed 26025 and seven in held-out seed 26026. Inputs and masks are procedural OpenCV drawings, with no external photos. `scripts/evaluate.py` runs three controller repeats for each of seven held-out scenario types (21 investigation runs), records a same-detector one-pass reference and writes measurements to `artifacts/evaluation.json`.

For this run, the full workflow selected the expected scripted action in 7/7 cases; the one-pass rule did so in 4/7. Four benign cases produced 0/4 candidate regions in the one-pass detector. On four pixel-labeled 640×480 cases (1,228,800 pixel positions; 16,170 pixels in the prediction/truth union), the binary change mask had precision 0.99183, recall 0.99913, F1 0.99546 and pixel IoU 0.99097. End-to-end controller latency (fixture creation excluded, API encoding/storage excluded) was p50 158.477 ms and p95 246.465 ms for 21 runs. Mean tool calls were 6.714. Unnecessary retake requests were 0/7. Process RSS changed from 34.38 MiB to 61.16 MiB; this is a before/after observation, not a peak-memory measure. The controller run used 6.000 process CPU seconds.

These scores describe a small generated fixture family with fixed policy labels and a shared scene generator. They do not establish field accuracy, water detection, incident-cause inference, customer impact or safety. See [EVALUATION.md](EVALUATION.md) for case-level results and limits.

## Failure handling and responsible operation

The system requests a retake for blurred/occluded frames, rejects incompatible resolutions, records missing sensor correlation as unverified, filters duplicate event IDs, checks timezone-aware timestamps, applies upload size/type/pixel limits, and fails closed on weak registration or missing baseline. It has no shutdown, alarm-disable, door, or dispatch tools. A possible water interpretation remains a hypothesis; a human must make significant decisions. See [RESPONSIBLE_USE.md](RESPONSIBLE_USE.md).

## Limitations and next work

There is no real-world licensed mechanical-room dataset, cloud deployment, public code URL, screen-recorded video, live camera adapter, calibrated probability, independently reviewed threshold study, or production identity provider. YuNet face blurring can miss faces and does not identify other sensitive content; it is not comprehensive redaction. Before competition submission, an owner must authorize and execute AWS setup, verify the public endpoint, arrange a judge-accessible repository/archive and video, fill in the real team identity and inspect the deployed security configuration.

