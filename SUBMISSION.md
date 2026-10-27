# Devpost submission wording — prepared, not submitted

**Readiness warning (checked 2026-10-27):** the local OpenCV 5 app, synthetic evaluation and public source repository are verified. The AWS workload and endpoint are not deployed, and no video is recorded or hosted. The signed-in Devpost account is registered, but the project's submission list is empty; draft creation is blocked by a Devpost reCAPTCHA connection error. These remain mandatory gaps. Do not claim cloud execution, and do not submit this entry until the AWS, video, team identity and eligibility gaps are resolved and the owner gives final approval.

## Project name

**Fortifiers Incident Memory**

## One-sentence pitch

An event-triggered visual investigation system that compares an alarm-time mechanical-room image with its history, uses sensor timing to guide the next evidence check, and creates a human-reviewable record of what visibly changed.

## Inspiration

Facility alarms announce an event but often leave operators to hunt through footage to learn what looks different. We explored whether camera history could serve as environmental memory: retrieve the relevant pre-event state, compare it to the alarm frame, and actively seek additional evidence when the images or conclusions are weak.

## What it does

The demo focuses on an industrial mechanical room and a simulated water-contact alarm. It checks frame quality, selects a same-camera pre-event baseline, aligns and compares images with OpenCV 5, draws candidate regions, checks an active sensor timestamp and can fetch an older image to determine whether an appearance was already present. Image-quality failures request a retake. A possible water-like visual change with sensor correlation becomes a hypothesis and asks a human to review. A visual comparison does not prove physical water or root cause.

All supplied rooms, frames, patches and sensor records are generated synthetic fixtures. They are not customer footage or real-world validation.

## How we built it

The local product is a Python 3.11+ FastAPI service, NumPy, OpenCV 5 and a lightweight responsive browser interface. OpenCV performs quality checks, ORB feature matching, RANSAC homography registration, ECC translation fallback, HSV illumination normalization, change masking, morphology, connected components and overlay/measurement generation. A deterministic bounded controller chooses subsequent tools from those observations and writes timestamped traces, image hashes, JSON and accessible HTML reports.

## OpenCV 5 and Agentic Vision

OpenCV outputs are inputs to later actions. Poor blur quality skips comparison and selects a retake request. A localized change selects ROI inspection and older-history retrieval. Historical similarity downgrades the novelty assessment. A region plus a time-aligned water-contact sensor selects a human-review request. Lighting normalization suppresses a global brightness-only change. The controller is bounded and has no actuator tools. See `AGENT_WORKFLOW.md` and `submission/agent-workflow.svg`.

## AWS

**Actual AWS use in this build: none.** A private ECR + App Runner + versioned S3 template and deployment script are prepared, but no AWS CLI, credentials or Docker are configured, and the owner directed preparation only. AWS says App Runner is closed to new customers; this account's access cannot be checked. No AWS resource, live endpoint or cloud processing response exists. The competition's meaningful AWS requirement and endpoint are not yet met. See `DEPLOYMENT.md` for the regional estimate and service restriction. Replace this section only after an AWS workload is live and independently verified.

## Challenges and solutions

- Uniform brightness changes looked like scene changes, so comparison normalizes the HSV value channel and separately inspects localized saturation differences.
- Camera movement and low-feature images can break pixel comparison, so the engine attempts ORB/RANSAC, falls back to ECC translation, lowers reliability on identity fallback and rejects weak comparisons.
- A mark can appear new relative to the nearest frame, so the controller can fetch older history and compare the ROI before deciding whether novelty is supported.
- A blue-looking patch and a sensor are not proof of a leak, so evidence classes distinguish observation, sensor correlation, hypothesis and unverified cause and stop at human review.
- The first positive fixture was blurred across the full frame and therefore correctly failed the quality gate; the synthetic patch generator was corrected to retain room detail and soften only patch edges.

## Measured results

On seven procedurally generated held-out scenario types with three runs each, the implemented workflow selected the expected scripted action in 7/7 and a simple no-history/no-quality one-pass rule in 4/7. On four pixel-labeled synthetic masks, precision was 0.99183, recall 0.99913, F1 0.99546 and mask IoU 0.99097. In the fresh 21-run controller benchmark, p50/p95 latency was 137.061/217.262 ms on Windows 10, Python 3.14, OpenCV 5.0.0. A separate local HTTP check returned four expected outcomes and verified a PNG overlay and ZIP report; see `artifacts/final-local-verification.json`. These measurements describe synthetic fixtures and local execution. They do not estimate field performance, AWS latency or real-water detection. Evaluation details and failure cases are in `EVALUATION.md`.

## What we learned

Image quality and historical context should change the investigation, not just decorate a static model result. The most useful contribution is the auditable path from an observation to the next tool call and a bounded human review request. Synthetic success is a useful controller test, but does not replace evaluation on authorized real environments.

## Roadmap

After a verified AWS deployment and operator feedback: gather consented and licensed mechanical-room footage, build a camera-specific baseline enrollment process, independently label conditions, study threshold calibration and domain shift, add authenticated camera/sensor connectors, review retention/access policies and measure cost/latency on AWS. Thermal, RTSP, predictive-maintenance and Graviton/COOL paths are out of scope for this submission build.

## Team, links and tags — verify before submission

- Project name: **Fortifiers Incident Memory**. Confirm the actual team name, roster and representative; no team bio or member list was supplied for this entry.
- Public code repository: https://github.com/axfrgo/fortifiers-incident-memory
- Working AWS endpoint: **none** — deployment blocked; do not substitute the local `127.0.0.1` address.
- Demo video (≤5 minutes): **none recorded or hosted**.
- Technical report and diagrams: `TECHNICAL_REPORT.md`, `ARCHITECTURE.md`, `submission/architecture.svg`, `AGENT_WORKFLOW.md`, and `submission/agent-workflow.svg` in the repository.
- Evaluation: `EVALUATION.md`, `artifacts/evaluation.json`, `artifacts/test-results.json`, and `artifacts/final-local-verification.json`.
- Technologies: OpenCV 5, Python, FastAPI, NumPy, responsive web UI; AWS deployment is prepared but not yet used.
- Agentic Vision: the local workflow has actual OpenCV observations changing later tool calls (retake, ROI inspection/history retrieval, or human review). This demonstrates the agentic mechanism. The project is not a complete eligible final entry while the meaningful AWS workload, judge endpoint and required video are missing.

## Competition entry checks

The signed-in Devpost account is registered for the competition. Its “My projects” page showed no project draft during finalization; the “Start project” control was blocked by a reCAPTCHA connection error. No project has been submitted. The official banner shows October 26, 2026 at 11:45 PM PDT (October 27, 2026 at 03:45 AM ADT in Halifax); the overview also mentions 11:59 PM Pacific, so this package targets the earlier deadline. The full rules require participants to be at least 13 and guardian permission/forms for participants below local legal majority; the overview separately says participants must be above local majority. Confirm the governing eligibility with the organizer, actual team's roster, representative, rights and declarations before submission.

