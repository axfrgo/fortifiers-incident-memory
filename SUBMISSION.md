# Devpost submission wording — prepared, not submitted

**Readiness warning (checked 2026-10-27):** the local OpenCV 5 app, synthetic evaluation, public source repository and real 3:40 Unlisted video are verified. A private Devpost draft has the title, pitch, story, cover, source archive, test instructions, video URL and Agentic Vision selection. The AWS workload and public endpoint are not deployed. The entrant must verify eligibility declarations and the video may not satisfy a strict requirement to show or name a team member. Do not claim cloud execution or field performance. This draft is not a submitted entry.

## Project name

**Fortifiers Incident Memory**

## Tagline

**Give the Physical World a Memory.**

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

**Actual AWS use in this build: none.** A private ECR + App Runner + versioned S3 template and deployment script are prepared. The open AWS tab remains at the account-signup flow; no AWS CLI, Docker, or credential profile is configured. The account, credits, service access, and account-specific cost eligibility could not be checked. No resources were created, no costs were incurred, and no spend limit or deployment approval is in place. AWS says App Runner is closed to new customers; account eligibility remains unknown. No live endpoint or cloud processing response exists. The competition's meaningful AWS requirement and endpoint are not met. See `DEPLOYMENT.md` for the illustrative cost estimate and service restriction. Replace this section only after an AWS workload is live and independently verified.

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

- Project name: **Fortifiers Incident Memory**. The entrant reports entering solo. The video identifies a solo entry but does not show or name the entrant; confirm whether a personal introduction is required.
- Public code repository: https://github.com/axfrgo/fortifiers-incident-memory
- Portable source archive: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- Working AWS endpoint: **none** — deployment blocked; do not substitute the local `127.0.0.1` address.
- Demo video (≤5 minutes): **published Unlisted**, 3:40 silent/captioned local demonstration: https://youtu.be/_k0J1XHyVyA. Public release mirror: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-demo.mp4. See [DEMO_SCRIPT.md](DEMO_SCRIPT.md) and [video-manifest.json](artifacts/video/video-manifest.json).
- Technical report and diagrams: `TECHNICAL_REPORT.md`, `ARCHITECTURE.md`, `submission/architecture.svg`, `AGENT_WORKFLOW.md`, and `submission/agent-workflow.svg` in the repository.
- Evaluation: `EVALUATION.md`, `artifacts/evaluation.json`, `artifacts/test-results.json`, and `artifacts/final-local-verification.json`.
- Technologies: OpenCV 5, Python, FastAPI, NumPy, responsive web UI; AWS deployment is prepared but not yet used.
- Agentic Vision: the local workflow has actual OpenCV observations changing later tool calls (retake, ROI inspection/history retrieval, or human review). This demonstrates the agentic mechanism. The project is not a complete eligible final entry while the meaningful AWS workload, judge endpoint and required video are missing.

## Competition entry checks

The Devpost account is registered and has a saved private draft at 4/5 steps. The user reports entering solo; the draft has no listed teammates. The saved project-details page contains the Unlisted demo URL. The draft has not been submitted or made public. The AWS tab remains at account signup; account access, credits and service eligibility remain unverified. The official Devpost banner shows October 26, 2026 at 11:45 PM PDT (October 27, 2026 at 03:45 AM ADT in Halifax); the overview also mentions 11:59 PM Pacific, so this package targets the earlier deadline. The entrant must review competition eligibility declarations and any platform terms before final submission.

