# Devpost submission wording — prepared, not submitted

**Status:** The solo entrant has a saved private Devpost draft. The AWS endpoint and source repository are live. This document is ready-to-paste material, not evidence that the final form has been submitted. The entrant must review eligibility declarations and confirm the final entry before submission.

## Project title

Fortifiers Incident Memory

## Tagline

Give the Physical World a Memory.

## One-sentence pitch

An agentic visual investigation system that reconstructs environmental changes around alarms using OpenCV 5, historical evidence, sensor context and an observation-driven investigation workflow.

## Inspiration

Traditional alarms announce an event but leave operators to hunt through footage for context. We explored whether a camera's visual history could act as environmental memory: retrieve the relevant pre-event state, compare it with the alarm-time image, and actively seek more evidence when the images or conclusions are weak.

## What it does

The demonstrator focuses on a mechanical room and a simulated water-contact alarm. It checks frame quality, selects a same-camera pre-event baseline, aligns and compares images with OpenCV 5, proposes visible change regions, checks synthetic sensor timing, and can retrieve an older frame to determine whether an appearance was already present. Poor image quality requests another frame. A possible water-like visual change correlated with a simulated sensor becomes a hypothesis and asks a human to review. Images do not prove physical water or root cause.

All supplied scenes, frames, visual changes and sensor events are procedurally generated synthetic fixtures. They are not customer footage or real-world validation.

## How we built it

The application uses FastAPI, NumPy, OpenCV 5 and a lightweight responsive web interface. OpenCV performs image validation and quality assessment, ORB feature matching with RANSAC homography, ECC translation fallback, HSV illumination normalization, difference masking, morphology, connected components, region measurements and annotation. A bounded deterministic controller routes tools from the actual observations and writes timestamped traces, evidence hashes, JSON and accessible HTML reports.

## How OpenCV 5 is used

The application requires OpenCV major version 5 at runtime. OpenCV derives the image-quality, alignment, illumination, mask and candidate-region observations that guide subsequent tools. The same pinned OpenCV workload runs in the AWS Lambda service.

## How AWS is used

The API and OpenCV processing run on AWS Lambda in us-east-2, not only in the browser or on S3. The Python 3.14 ZIP package is served through a public Lambda Function URL and writes synthetic evidence to a private, encrypted S3 bucket with seven-day retention. CloudWatch logs record Lambda execution. The AWS health endpoint reports OpenCV 5.0.0 and deployed commit b851290df9e99aca1a232c018e53bff48b8f559d.

Live synthetic demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/

The endpoint is publicly reachable and unauthenticated, but only exposes seven fixed synthetic scenarios; arbitrary image uploads are disabled. It is not a production service, and billing after deployment has not yet been reconciled.

## How Agentic Vision changes later actions

This is a software controller, not an AI coding assistant. OpenCV results directly change the next action:
- Poor blur/occlusion quality selects a retake request and stops diagnosis.
- A localized candidate selects ROI inspection and older-frame retrieval.
- A similar older region changes the novelty conclusion to no_new_change_supported.
- A visible candidate plus a time-aligned simulated water sensor leads to human review.

The deployed clear-change trace has nine actual steps and ends in human review. The poor-image trace requests a retake; the historical-match trace retrieves older evidence and downgrades the candidate. Full traces are in artifacts/aws-remote-results.json.

## Challenges and solutions

- Uniform brightness changes can resemble scene changes. HSV illumination normalization reduces this effect.
- Low-feature frames and camera motion can break direct pixel comparison. The pipeline tries ORB/RANSAC and ECC translation and reduces confidence or rejects weak comparisons.
- A region can look new against the nearest frame but already exist in older history. The controller can retrieve and inspect older evidence.
- A colored patch and a sensor are not proof of a leak. Evidence classes separate observed change, sensor correlation, hypothesis and unverified cause, and the system stops at human review.
- Deploying OpenCV under the account's Lambda limits required a compact ZIP package. CodeBuild could not start because the account build-queue quota was zero; the tested workload was deployed through a pinned Lambda ZIP package instead.

## Measured accomplishments

The local held-out synthetic controller selected the test-authored expected action on 7/7 scenario types, compared with 4/7 for a simple one-pass reference. Across 21 local runs, controller p50/p95 latency was 137.061/217.262 ms. Four generated pixel masks yielded precision 0.99183, recall 0.99913, F1 0.99546 and IoU 0.99097. These are synthetic pixel-change metrics, not leak-detection accuracy.

All seven AWS synthetic scenarios returned HTTP 200 with the expected materially different policy outcomes. An anonymous client downloaded and integrity-checked a 900,871-byte evidence ZIP. A CloudWatch investigation report recorded 2,922.8 ms duration and 218 MiB maximum used memory. See EVALUATION.md and deployment-manifest.json. No field performance is claimed.

## What we learned

Image quality and historical context should change the investigation rather than decorate a static score. The useful contribution is an auditable path from an OpenCV observation to the next evidence action and a bounded human-review request. Synthetic success validates controller branches, not real-world performance.

## Future roadmap

With authorized real facility footage and operator participation: build a camera-specific baseline enrollment flow, gather independently labeled cases, study threshold calibration and domain shift, add authenticated camera/sensor connectors, define retention/access policies and measure cost/latency at representative load. Thermal, RTSP, predictive maintenance and Graviton/COOL paths are not part of this submission.

## Team and links

- Project: Fortifiers Incident Memory; user reports a solo entry.
- Public code: https://github.com/axfrgo/fortifiers-incident-memory
- Portable source archive: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- Live AWS demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/
- Unlisted video, 3:40: https://youtu.be/_k0J1XHyVyA
- Technical report: TECHNICAL_REPORT.md
- Architecture: ARCHITECTURE.md and submission/architecture.svg
- Agent workflow: AGENT_WORKFLOW.md and submission/agent-workflow.svg
- Evaluation: EVALUATION.md and artifacts/evaluation.json
- Tags: OpenCV 5, AWS Lambda, AWS, FastAPI, Python, Computer Vision, Agentic Vision.

The video was recorded before AWS deployment; it shows the local application and includes a then-accurate end card saying AWS was not deployed. It does not show or name the entrant. The live AWS endpoint and verified remote traces/results are separately linked above; do not imply the current video captured cloud execution.

## Agentic Vision award explanation

OpenCV 5 performs substantive image analysis. Its quality, alignment, mask, region and historical-similarity observations are consumed by a bounded tool-routing controller. The next action changes across clear-change, poor-image, lighting-only and historical-match cases, as shown in the remote traces. Failures stop or request more evidence, reports preserve hashes and classifications, and consequential actions require a human. Evaluation includes positive and negative synthetic fixtures and a one-pass comparison. No award eligibility or ranking is guaranteed.

## Final entrant checks

The user reports entering solo and the account is registered. The entrant must review official age/location/team eligibility and data/IP declarations personally. The deadline banner's earlier displayed cutoff was October 27, 2026 at 06:45 UTC. The Devpost draft is not submitted and must be reviewed and submitted by the entrant before the platform closes. Do not claim submission confirmation until Devpost displays it.
