# Judging scorecard and readiness

This is an evidence map, not a prediction of judging outcomes. Rules were checked on 2026-10-27 UTC. The Devpost overview banner shows **October 26, 2026 at 11:45 PM PDT** (October 27 03:45 ADT in Halifax). The same overview/rules text also gives **11:59 PM Pacific Time** (03:59 ADT). This package uses the earlier 11:45 PM banner cutoff. [Devpost overview](https://opencv26.devpost.com/) · [rules](https://opencv26.devpost.com/rules)

| Published criterion | Weight | Evidence in this package | Status / gap |
|---|---:|---|---|
| Technical execution | 30% | OpenCV 5.0.0.93 verified; ORB/RANSAC registration, ECC fallback, HSV normalization, morphology, connected regions, masks and quality gate in `src/incident_memory/vision.py`; 36/36 tests passed; evaluation report and live local HTTP check | **PASS locally**; Python 3.11/Docker and AWS runtime not verified |
| Innovation | 20% | Environmental history, sensor timing, active older-frame retrieval and uncertainty-aware trace | **Implemented conceptually**; no customer or field validation |
| Real-world impact | 20% | Industrial incident-triage use case and manual-control boundary | **Potential only**; no measured operator benefit or real facility images |
| UX | 10% | Responsive dashboard, slider, traces, timeline, labels, status, review controls | **PASS locally**; no accessibility audit or user study |
| Documentation and presentation | 10% | Technical report, diagrams, demo script, scorecard, measured evaluation | **PARTIAL**; no real-team video or public demo/repository links |
| Cloud delivery, reproducibility, responsible operation | 10% | Locked dependencies, CloudFormation, deployment script, privacy/operations docs | **BLOCKED for AWS delivery**; no AWS resources, live URL, Docker build or endpoint test |

## Agentic Vision Special Award map

| Criterion | Weight | Evidence | Status |
|---|---:|---|---|
| OpenCV 5-agent integration | 30% | Real OpenCV APIs provide quality/registration/mask/region outputs to `InvestigationAgent` | **PASS locally** |
| Orchestration and appropriate autonomy | 25% | Four distinct traces, bounded call budget, adaptive history/retake/review paths | **PASS locally** |
| Task effectiveness and evaluation | 20% | Seven synthetic scenarios; 21 runs; 7/7 expected policy actions; simple one-pass 4/7 | **Measured, synthetic-only** |
| Failure handling, observability, security and human control | 15% | Quality fail-closed path, timestamps/dedup/security validation, audit review, no actuator | **Implemented locally**; cloud authentication/deployment not verified |
| UX, documentation and demonstration | 10% | Interface, trace diagram, report and timed storyboard | **PARTIAL**; no hosted video/endpoint |

The workflow satisfies the technical pattern described for Agentic Vision: OpenCV-derived observations actually alter a subsequent tool call or review request. This does not constitute a claim of award eligibility or a complete eligible final entry. The mandatory meaningful AWS component, judge-accessible endpoint, video and repository/archive link are not yet fulfilled. [Official Agentic Vision description](https://opencv.org/opencv-ai-competition-2026/)

## Official materials and eligibility notes

The Devpost final-submission list calls for a technical report, judge-accessible repository/archive, pinned dependencies and instructions, architecture diagram, working endpoint or arranged live demo, public/unlisted video ≤5 minutes showing team/application/architecture/results, and evaluation evidence including failures. This local package covers source/docs/tests/evaluation preparation but not the live AWS endpoint, arranged screen share, hosted video or judge access. [Final submission requirements](https://opencv26.devpost.com/)

The Devpost overview says team members must be above local legal age of majority; the linked full rules state participants must be at least 13 and those below local majority must obtain guardian permission and complete required forms. Confirm the current account-side entry and legal eligibility of each actual team member. Team roster, registration status and acceptance are unknown here; no one was enrolled or submitted by this task. [Rules and eligibility](https://opencv26.devpost.com/rules)

No COOL claim is made. The required Arm/Graviton COOL deployment and measured comparison are absent.

