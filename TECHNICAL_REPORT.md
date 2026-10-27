# Technical report — Fortifiers Incident Memory

## Problem and users

Industrial maintenance and facility teams can receive a binary sensor alarm without an easy account of what visibly changed at the location. Fortifiers Incident Memory is a decision-support prototype that compares an alarm-time RGB frame to visual history, relates it to a timestamped sensor event, and records evidence and uncertainty. Intended users are facility operators and maintenance staff. The demonstrator is limited to procedurally generated mechanical-room frames and a simulated water-contact sensor.

## System design

The workflow is event/frame retrieval → image-quality gate → camera/context/time baseline selection → registration and comparison → region inspection → optional older-history retrieval → sensor correlation → review or retake recommendation → hashed evidence report. The architecture and agent workflow SVGs show the service boundaries.

The Python modules expose independent vision, memory, agent, report, API and cloud interfaces. FastAPI serves a responsive dashboard, health endpoint, synthetic scenario API, validated local image-pair API, reports and audit-only human review. The browser UI shows synthetic provenance, a before/after slider, timeline, annotations, evidence classifications and the actual tool trace.

## OpenCV 5 implementation

Runtime startup rejects a non-5 major version. The pinned wheel is opencv-python-headless==5.0.0.93; the local runtime reports cv2.__version__ == 5.0.0. The deployed Lambda health endpoint independently reports OpenCV 5.0.0.

The engine uses imdecode for validation, Laplacian variance and exposure statistics for quality assessment, ORB descriptors with Hamming ratio matching and findHomography(..., RANSAC, ...) for registration, ECC translation fallback, HSV V-channel gain normalization, saturation/value differences, ROI masking, opening/closing morphology, connected components, geometry, overlays and PNG encoding. A weak cool-tone fraction is only a visual descriptor. Reliability and quality values are heuristics, not calibrated probabilities.

Resolution mismatches fail closed. Low-feature registration retains an identity fallback only with reduced reliability. Incident-marked frames are excluded from baseline selection. Image quality gates comparison. An older image can change the novelty assessment based on OpenCV similarity in the candidate crop.

## Observation-driven agent

The controller is deterministic, bounded and driven by OpenCV outputs. A blur/occlusion observation requests another frame or a retake and stops before diagnosis. A localized change prompts ROI inspection and historical retrieval. A match to older history downgrades the novelty decision. A visible candidate correlated with the timestamp of a simulated water sensor produces a hypothesis and human-review request. No agent tool can shut down machinery, disable alarms, open doors or dispatch responders.

The real remote clear-change trace has nine tool steps and ends in human review. The remote poor-image case ends in retake_requested. The remote historical-match case ends in no_new_change_supported. Full traces are in artifacts/aws-remote-results.json.

## AWS implementation and verified state

The deployed service is AWS Lambda in us-east-2, using a Python 3.14 ZIP package, FastAPI through Mangum, and OpenCV 5.0.0. The public Function URL serves the actual dashboard and performs real OpenCV processing on AWS. It is pinned to source commit b851290df9e99aca1a232c018e53bff48b8f559d. CloudFormation stack fortifiers-incident-memory-demo-free-3 is UPDATE_COMPLETE; bootstrap stack fortifiers-incident-memory-bootstrap is CREATE_COMPLETE.

Anonymous remote checks verified root and health HTTP 200, OpenCV 5, seven scenario HTTP 200 responses, 404 for an unknown scenario, 403 for disabled image uploads, and a downloadable evidence ZIP. The clear-change ZIP was downloaded without AWS credentials, checked for ZIP integrity, and contains JSON/HTML reports, baseline and event images, annotated overlay and change mask. CloudWatch records actual Lambda invocations; a sample investigation used 218 MiB maximum memory and ran for 2,922.8 ms. Another invocation incurred a 2,205.78 ms initialization and used 145 MiB. These are individual observations, not an AWS latency benchmark.

The runtime has 512 MiB memory, a 90-second timeout and 512 MiB temporary storage; reserved concurrency is not set because the account quota requires at least five unreserved executions. The public Function URL has no authentication, so the API exposes only seven built-in synthetic scenarios and disables arbitrary user uploads. Evidence is stored in a private SSE-S3 bucket and expires after seven days; logs expire after 14 days. No account identifier or presigned bearer URL is included in the repository. Billing after deployment has not been reconciled; Free Plan credits are not a hard cost cap. See DEPLOYMENT.md and deployment-manifest.json for detailed evidence and teardown.

A CodeBuild/ECR image build path was prepared but CodeBuild could not start because the account's build-queue quota was zero. The working deployment uses the reproducible ZIP Lambda path instead. Local Docker was unavailable and is not claimed as verified.

## Evaluation

scripts/build_dataset.py generates 14 fixture sets: seven scenario types in tuning seed 26025 and held-out seed 26026. The fixtures are procedural drawings with no external photos. scripts/evaluate.py runs three controller repeats for each of seven held-out scenario types (21 investigations), records a same-detector one-pass reference, and writes results to artifacts/evaluation.json.

The held-out run selected the test-authored expected action in 7/7 scenario types; the one-pass rule did so in 4/7. Four pixel-labeled 640×480 generated cases (1,228,800 total pixel positions) produced mask precision 0.99183, recall 0.99913, F1 0.99546 and pixel IoU 0.99097. Controller latency excluding fixture creation, API response encoding, storage and network was p50 137.061 ms and p95 217.262 ms over 21 local runs. Mean tool calls were 6.714. Unnecessary retake requests were 0/7. Process RSS changed from 34.35 MiB to 60.29 MiB; this is not peak memory. The test suite passed 37/37 after the AWS regional S3 signing regression test was added.

The actual AWS remote run covered all seven built-in synthetic scenarios once. Their single-request client-observed times ranged from 1.206 to 2.384 seconds and include network/serialization/cold-start effects. CloudWatch provides an individual 2.923-second investigation report at 218 MiB maximum memory used. The remote runs are functional checks, not a statistical performance study.

These results describe a small generated fixture family with policy labels defined by the test author and a shared scene generator. They do not establish field accuracy, physical water detection, cause inference, operator benefit, or safety. The mask score is pixel-change overlap, not real leak segmentation. See EVALUATION.md for case-level results and failure cases.

## Failure handling and responsible operation

The system requests a retake for blurred/occluded frames, rejects incompatible resolutions, records missing sensor correlation as unverified, filters duplicate event IDs, validates timezone-aware timestamps, enforces local upload limits, and fails closed on weak registration or missing baseline. Cloud uploads are disabled. Significant safety/maintenance decisions require a human operator. See RESPONSIBLE_USE.md.

## Limitations and next work

There is no real-world licensed mechanical-room dataset, field evaluation, calibrated probability, independent threshold review, user study, live camera adapter, production identity provider, or Python 3.11 runtime check. The current 3:40 silent video shows the authentic local app and explicitly states AWS was not deployed at recording time; AWS has since been deployed and that video has not been updated to show the endpoint. The video also does not show or name the solo entrant. YuNet face blurring can miss faces and other identifiers; it is not comprehensive redaction. Future work should use authorized camera data, independent labels, a protected operator interface, and cost/latency measurements under representative load.
