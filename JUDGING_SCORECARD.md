# Judging scorecard and readiness

Evidence map against the official competition criteria, not a prediction of ranking. The earlier displayed deadline was October 27, 2026 at 06:45 UTC. The entrant must verify current submission availability and complete account declarations.

| Criterion | Weight | Verified evidence | Status and remaining limitation |
|---|---:|---|---|
| Technical execution | 30% | OpenCV 5.0.0 local and remote runtime; real ORB/RANSAC, ECC fallback, HSV normalization, masks, morphology, connected components, image-quality gates; 37 passing automated tests; seven remote scenario responses | PASS for demonstrated prototype; synthetic-only image domain and no Python 3.11 verification |
| Innovation | 20% | Environmental visual memory, historical retrieval, active evidence seeking, sensor correlation, uncertainty classification, auditable decisions | Demonstrated engineering concept; no customer or field validation |
| Real-world impact | 20% | Industrial incident-triage workflow with operator review and preservation of site alarms | Potential impact only; no measured operator benefit or real facility data |
| UX | 10% | Responsive dashboard, synthetic scenario selector, before/after comparison, overlays, evidence trace, downloadable report | Verified live; no formal accessibility audit or user study |
| Documentation and presentation | 10% | Technical report, architecture/workflow diagrams, measured evaluation, public repository/archive, accessible 3:40 Unlisted video | Documentation and links exist; video was recorded before AWS deployment, says AWS was not deployed, and does not identify the entrant |
| Cloud delivery, reproducibility, responsible operation | 10% | AWS Lambda actually runs OpenCV; public Function URL; seven remote cases; CloudWatch invocation records; private S3 evidence, short retention, disabled uploads; pinned package builder and teardown steps | PASS for a synthetic public prototype; unauthenticated endpoint and no hard spend cap, current billing not reconciled |

## Agentic Vision Special Award

| Criterion | Weight | Evidence | Status and limitation |
|---|---:|---|---|
| OpenCV-agent integration | 30% | Actual OpenCV quality, alignment, mask and region observations are passed to the controller; same code is deployed and invoked on AWS | PASS; scenario inputs are generated |
| Orchestration and autonomy | 25% | Different next actions: poor image requests retake; localized change triggers ROI inspection/history retrieval; historical match downgrades novelty; sensor-correlated candidate requests human review | PASS; bounded deterministic controller, no LLM |
| Task effectiveness and evaluation | 20% | Seven AWS scenarios returned expected policy outcomes; local held-out policy outcomes 7/7 versus one-pass 4/7 across seven scenario types; pixel scores explicitly labeled synthetic | PASS as a synthetic benchmark; expected actions are author-defined and not independent ground truth |
| Failure handling, observability, security and human control | 15% | Fail-closed image quality and registration paths; 403 uploads; 404 unknown scenario; CloudWatch logs; hashed evidence; private S3 with seven-day retention; human review; no actuator tools | PASS for current demo; public synthetic API can be invoked by anyone; no authentication or hard request/cost cap |
| UX, documentation and demonstration | 10% | Working public UI, diagrams, traces, reports, source and video link | Partial: video predates AWS deployment and omits named/visible entrant |

## Exact observation-driven example

The deployed synthetic clear-change investigation returns an observed localized candidate and correlated synthetic sensor event. The controller then chooses ROI inspection and evidence-report creation, with human review as the stopping action. In the poor-image case, the OpenCV quality assessment stops comparison and chooses a retake request. In historical_match, the candidate seen against the nearest frame is compared to an older frame; the history observation changes the outcome to no_new_change_supported. The full per-scenario traces are in artifacts/aws-remote-results.json.

The prototype distinguishes observed image change, sensor correlation, hypothesis and unverified cause. It does not claim that RGB images prove water or root cause. It has no machinery shutdown, alarm-disable, door or emergency-dispatch action.

## Eligibility and video gap

The account is registered and the user reports entering solo. Eligibility declarations still require the entrant to personally confirm. The published Unlisted video is accessible and under five minutes, but its recording-time end card says AWS is not deployed. That statement was true when recorded; the video has not been updated to show the later AWS deployment. It also does not show or name the entrant. See FINAL_SUBMISSION_STATUS.md.

No COOL/Graviton award claim is made. There is no qualifying Arm deployment or measured efficiency comparison.
