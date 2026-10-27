# Devpost submission wording — prepared, not submitted

**Readiness warning:** this wording is not a claim that the entry is complete. The core OpenCV 5 application and synthetic evaluation run locally. The AWS workload and endpoint are not deployed; no public/judge-accessible repository or video is linked. These are explicit mandatory gaps. Do not submit until AWS execution, public judge access, team identification and video are actually in place. The user asked not to publish or submit without authorization.

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

**Actual AWS use in this build: none.** An App Runner + private ECR + versioned S3 CloudFormation template and deployment script are prepared, but this environment lacked AWS CLI/credentials/Docker and the owner directed preparation only. No AWS resource, live endpoint, cloud processing response or cost result exists. Replace this paragraph only after the actual App Runner service is live and verified. The current entry does not yet meet the competition's mandatory AWS requirement.

## Challenges and solutions

- Uniform brightness changes looked like scene changes, so comparison normalizes the HSV value channel and separately inspects localized saturation differences.
- Camera movement and low-feature images can break pixel comparison, so the engine attempts ORB/RANSAC, falls back to ECC translation, lowers reliability on identity fallback and rejects weak comparisons.
- A mark can appear new relative to the nearest frame, so the controller can fetch older history and compare the ROI before deciding whether novelty is supported.
- A blue-looking patch and a sensor are not proof of a leak, so evidence classes distinguish observation, sensor correlation, hypothesis and unverified cause and stop at human review.
- The first positive fixture was blurred across the full frame and therefore correctly failed the quality gate; the synthetic patch generator was corrected to retain room detail and soften only patch edges.

## Measured results

On seven procedurally generated held-out scenario types with three runs each, the implemented workflow selected the expected scripted action in 7/7 and a simple no-history/no-quality one-pass rule in 4/7. On four pixel-labeled synthetic masks, precision was 0.99183, recall 0.99913, F1 0.99546 and mask IoU 0.99097. Controller p50/p95 latency was 158.477/246.465 ms for 21 runs on Windows 10, Python 3.14, OpenCV 5.0.0. These measurements describe synthetic fixtures and do not estimate field performance or detect real water. Evaluation details and failure cases are in `EVALUATION.md`.

## What we learned

Image quality and historical context should change the investigation, not just decorate a static model result. The most useful contribution is the auditable path from an observation to the next tool call and a bounded human review request. Synthetic success is a useful controller test, but does not replace evaluation on authorized real environments.

## Roadmap

After a verified AWS deployment and operator feedback: gather consented and licensed mechanical-room footage, build a camera-specific baseline enrollment process, independently label conditions, study threshold calibration and domain shift, add authenticated camera/sensor connectors, review retention/access policies and measure cost/latency on AWS. Thermal, RTSP, predictive-maintenance and Graviton/COOL paths are out of scope for this submission build.

## Team, links and tags — fill before submission

- Team name and real member names: **[insert actual team identity; not provided in this build]**
- Code/archive URL: **[insert judge-accessible URL after authorized hosting]**
- Working AWS endpoint: **[insert verified App Runner URL; currently none]**
- Demo video (≤5 minutes): **[insert public/unlisted judge-accessible video link; not recorded]**
- Technical report: `TECHNICAL_REPORT.md` (package path; upload/link after hosting)
- Technologies: OpenCV 5, Python, FastAPI, NumPy, AWS App Runner, Amazon S3, CloudWatch, computer vision, industrial IoT, Agentic Vision.
- Special award: the local workflow includes OpenCV-derived observations that change later calls/actions. Do not claim full award eligibility before completing the public AWS, endpoint, judge video and repository requirements.

## Competition entry checks

The Devpost banner currently shows the earlier target deadline October 26, 2026 at 11:45 PM PDT; the page also has a 11:59 PM Pacific Time reference. This package targets 11:45 PM PDT. The overview and full rules differ on age wording (overview says above local age of majority; rules say at least 13 and require guardian permission below majority). Confirm the account's current eligibility, team registration, any local legal requirements and the binding rules before entry. Nothing has been registered, published or submitted in this task.

