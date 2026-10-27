# Final submission status

**Checked:** 2026-10-27 04:05 UTC. **Target deadline:** 2026-10-27 06:45 UTC (the earlier official Devpost banner: Oct. 26, 2026 at 11:45 p.m. PDT = Oct. 27 at 03:45 a.m. ADT). About 2 hours 40 minutes remained at this check.

This report separates local proof from remote and entrant-controlled requirements. No AWS resources were created and no AWS cost was incurred. The Devpost draft remains unsubmitted.

## Requested release states

| State | Status | Supporting evidence |
|---|---|---|
| `LOCAL_VERIFIED` | **PASS** | OpenCV 5.0.0 and FastAPI app verified locally. Fresh pytest run: 36 passed, 0 failed, 0 skipped in 8.61 s. The portable ZIP extracted and the extracted source passed 36/36 tests in 8.16 s under the pinned clean environment. One Starlette/AnyIO deprecation warning. See [JUnit output](artifacts/test-results-finalization.xml), [machine-readable summary](artifacts/test-results.json), and exact archive digest/evidence in [source archive manifest](artifacts/source-archive-manifest.json). |
| `GITHUB_PUBLISHED` | **PASS** | Public repository: [github.com/axfrgo/fortifiers-incident-memory](https://github.com/axfrgo/fortifiers-incident-memory). Anonymous Git/API check before this final documentation update showed `master` at `855ce2a115dd43e500ed94b15313e3b03bf72e31`. Final docs/archive still need a commit and push; verify the new public HEAD before closeout. |
| `AWS_DEPLOYED` | **BLOCKED** | No AWS resources or endpoint exist. The open AWS tabs are at sign-in/account signup; identity, billing, credits and service access remain unknown. AWS CLI, Docker and credential profile are unavailable locally. |
| `REMOTE_TESTED` | **BLOCKED** | There is no live service URL, cloud OpenCV investigation, CloudWatch execution evidence or remote test. |
| `VIDEO_RECORDED` | **PASS** | Actual local UI capture: `artifacts/video/fortifiers-incident-memory-demo.mp4`, 220.4 s (3:40), 1920×1080, silent, SHA-256 `a662dd0bd82bbb31df5396b0dc83754ac1b80c553ed61dd27733f29e0a741002`. The film shows four real synthetic app outcomes and discloses no AWS deployment/no field validation. It does not name or show the entrant. |
| `VIDEO_ACCESSIBLE` | **PASS** | YouTube Studio displayed “Video published”; Unlisted was selected. A no-credential HTTP GET to [the video](https://youtu.be/_k0J1XHyVyA) returned HTTP 200 and the expected title. An unauthenticated HEAD request to the [GitHub release asset](https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-demo.mp4) returned HTTP 200 and 49,804,378 bytes. |
| `DEVPOST_PREPARED` | **PASS** | Authenticated Devpost page shows a saved solo draft at **4/5 steps**. The project story, YouTube URL, public repository, source archive, test instructions and Agentic Vision selection are saved. No working endpoint is listed because none exists; the entry remains incomplete until AWS execution/public endpoint or an organizer-approved live-demo arrangement is available. |
| `DEVPOST_SUBMITTED` | **BLOCKED** | Not submitted. No final submission authorization or final rule/eligibility declaration was provided. The working endpoint/AWS requirement is also unresolved. |
| `SUBMISSION_CONFIRMED` | **BLOCKED** | No submitted state, project confirmation or public Devpost submission exists. |

## Requirement evidence

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 visual processing | **PASS locally** | Runtime and tests identify OpenCV 5.0.0. ORB/RANSAC registration, ECC fallback, HSV normalization, change masks, morphology, components, measurements and overlays are implemented and exercised locally. No AWS runtime verification. |
| Observation-driven Agentic Vision | **PASS locally** | Actual trace: poor blur quality selects a retake; candidate regions cause ROI/history/sensor tools; older history downgrades a pre-existing change; illumination normalization rejects a lighting-only shift; supported visual/sensor evidence stops for human review. See [workflow](AGENT_WORKFLOW.md), generated traces, and the video. Synthetic data only. |
| Automated tests | **PASS locally** | 36/36 fresh run passed. AWS and Docker tests were not run. |
| Evaluation | **PASS, synthetic only** | Seven procedural scenario types, three runs each: expected action 7/7 vs 4/7 for one-pass. Four pixel-labeled masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller p50/p95 137.061/217.262 ms in 21 local runs. These are not field or leak-detection performance. See [EVALUATION.md](EVALUATION.md). |
| Judge-accessible source | **PASS** | Public GitHub repository above. Current package was extracted and tested from a clean pinned virtualenv. Latest documentation changes still require public push and anonymous HEAD verification. A ZIP archive is attached to the saved Devpost draft (35 MB upload limit). |
| Meaningful AWS workload/public endpoint | **BLOCKED** | No deployment, endpoint, CloudWatch evidence, or AWS investigation. See [DEPLOYMENT.md](DEPLOYMENT.md). |
| Demo video | **PASS** | Unlisted link and public release asset are live. Duration is 3:40. It identifies the entry as solo but does not show/name the entrant; add the entrant's own introduction if required by judging. |
| Documentation | **PASS** | README, technical report, architecture and workflow diagrams, evaluation, responsible use, deployment instructions, judging scorecard, submission copy, demo notes, data provenance, build ledger, test results and status report are present. |
| Solo eligibility | **BLOCKED** | User says the entry is solo and Devpost shows one creator. The entrant still needs to personally verify all eligibility declarations and intellectual-property/data-rights attestations. |
| Devpost submission | **BLOCKED** | Saved draft URL: [Devpost project draft](https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/project_details/edit). The video URL is saved. No endpoint is supplied, no legal declaration was accepted, and no final submission was made. |

## Exact links and deployment/cost facts

- **Public repository:** https://github.com/axfrgo/fortifiers-incident-memory
- **Current public Git commit before finalization push:** `855ce2a115dd43e500ed94b15313e3b03bf72e31`; update after pushing these finalization files.
- **Unlisted demo video:** https://youtu.be/_k0J1XHyVyA
- **Public video release mirror:** https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-demo.mp4
- **Portable source archive:** https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- **AWS endpoint:** none.
- **Devpost draft/preview:** https://devpost.com/software/fortifiers-incident-memory (draft is not publicly submitted); authenticated edit link is in the requirement table above.
- **AWS resources created:** none. **Project AWS costs:** $0 incurred. Account credits/free-tier status are unknown because the browser remains at AWS sign-in/account signup.
- **Potential App Runner cost:** prepared configuration is not free at list pricing. Prior illustrative `us-east-1` estimate: about $5.11/month idle plus $0.032 per active vCPU-hour, before ECR/S3/logging/data transfer/taxes/scale-out; this is not an account quote or spending cap. App Runner is closed to new customers; existing-account eligibility is unknown.
- **Tests:** 36 passed / 0 failed / 0 skipped in 8.61 s locally; extracted archive 36/36 in 8.16 s with pinned dependencies. **Evaluation limits:** synthetic data only; no field, AWS, or real-world validation.

## Entrant actions still needed

1. Complete AWS console sign-in/account setup in the open AWS tab. Do not accept financial/billing terms or create resources unless you intend to and the account's credits and cost exposure are clear. A live AWS workload and endpoint remain mandatory for the strongest eligible package.
2. Personally verify solo eligibility and any required legal/data-rights declarations.
3. Review whether the silent video satisfies the rule to show team identification; if not, record a short genuine introduction yourself and replace the video.
4. Review the Devpost draft. Do not treat its draft page as a submitted project. Final submission still requires the entrant's explicit authorization and a confirmation receipt.

Official references: [competition overview](https://opencv26.devpost.com/) and [official rules](https://opencv26.devpost.com/rules). Use the earlier deadline displayed on the Devpost banner.
