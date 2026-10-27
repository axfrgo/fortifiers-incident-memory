# Judging scorecard and readiness

This is an evidence map, not a prediction of judging outcomes. Rules were checked on 2026-10-27 UTC. The Devpost overview banner shows **October 26, 2026 at 11:45 PM PDT** (October 27 03:45 ADT in Halifax). The same overview/rules text also gives **11:59 PM Pacific Time** (03:59 ADT). This package uses the earlier 11:45 PM banner cutoff. [Devpost overview](https://opencv26.devpost.com/) · [rules](https://opencv26.devpost.com/rules)

| Published criterion | Weight | Evidence in this package | Status / gap |
|---|---:|---|---|
| Technical execution | 30% | OpenCV 5.0.0.93 verified; ORB/RANSAC registration, ECC fallback, HSV normalization, morphology, connected regions, masks and quality gate in `src/incident_memory/vision.py`; fresh 36/36 test run; four local HTTP scenarios and evidence downloads | **PASS locally**; Python 3.11/Docker and AWS runtime not verified |
| Innovation | 20% | Environmental history, sensor timing, active older-frame retrieval and uncertainty-aware trace | **Implemented conceptually**; no customer or field validation |
| Real-world impact | 20% | Industrial incident-triage use case and manual-control boundary | **Potential only**; no measured operator benefit or real facility images |
| UX | 10% | Responsive dashboard, slider, traces, timeline, labels, status, review controls | **PASS locally**; no accessibility audit or user study |
| Documentation and presentation | 10% | Technical report, diagrams, scorecard, measured synthetic evaluation, public source repo, real 3:40 Unlisted video | **PASS for materials**; AWS endpoint is absent and the video does not name/show the entrant |
| Cloud delivery, reproducibility, responsible operation | 10% | Locked dependencies, CloudFormation, deployment script, privacy/operations docs | **BLOCKED for AWS delivery**; no AWS resources, live URL, Docker build or endpoint test |

## Agentic Vision Special Award map

| Criterion | Weight | Evidence | Status |
|---|---:|---|---|
| OpenCV 5-agent integration | 30% | Real OpenCV APIs provide quality/registration/mask/region outputs to `InvestigationAgent` | **PASS locally** |
| Orchestration and appropriate autonomy | 25% | Four distinct traces, bounded call budget, adaptive history/retake/review paths | **PASS locally** |
| Task effectiveness and evaluation | 20% | Seven synthetic scenarios; 21 runs; 7/7 expected policy actions; simple one-pass 4/7 | **Measured, synthetic-only** |
| Failure handling, observability, security and human control | 15% | Quality fail-closed path, timestamps/dedup/security validation, audit review, no actuator | **Implemented locally**; cloud authentication/deployment not verified |
| UX, documentation and demonstration | 10% | Interface, trace diagram, report and public 3:40 Unlisted video | **PASS for demo materials**; no AWS endpoint and no named/visible entrant |

The workflow demonstrates the technical pattern described for Agentic Vision: OpenCV-derived observations actually alter a subsequent tool call or review request. The public repository and Unlisted video are accessible. The mandatory meaningful AWS component and judge-accessible endpoint remain unfulfilled, and the video does not name/show the entrant. This is not a claim of a complete eligible final entry or award eligibility. [Official Agentic Vision description](https://opencv.org/opencv-ai-competition-2026/)

## Official materials and eligibility notes

The Devpost final-submission list calls for a technical report, judge-accessible repository/archive, pinned dependencies and instructions, architecture diagram, working endpoint or arranged live demo, public/unlisted video ≤5 minutes showing team/application/architecture/results, and evaluation evidence including failures. This package covers source/docs/tests/evaluation, public source access and a hosted demo. The AWS endpoint/live-demo arrangement and entrant identification in video remain gaps. [Final submission requirements](https://opencv26.devpost.com/)

The full rules require participants to be at least 13; anyone below the local age of majority needs guardian permission and required forms. The overview banner separately says participants must be above local majority, so confirm the governing rule with the organizer. The signed-in Devpost account is registered, but its project list is empty; actual team roster and representative remain unknown. [Rules and eligibility](https://opencv26.devpost.com/rules)

No COOL claim is made. The required Arm/Graviton COOL deployment and measured comparison are absent.

