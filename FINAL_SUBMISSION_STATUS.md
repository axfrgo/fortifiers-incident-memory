# Final submission status

**Checked:** 2026-10-27 04:32 UTC. **Target deadline:** 2026-10-27 06:45 UTC (earlier Devpost banner time). The project is being finalized against the earlier deadline.

## Required state report

| State | Status | Evidence |
|---|---|---|
| `LOCAL_VERIFIED` | **PASS** | Fresh run: 36 passed, 0 failed, 0 skipped in 8.17 seconds. Python 3.14.0; OpenCV 5.0.0; FastAPI 0.123.0. Fresh JUnit: [test-results-finalization.xml](artifacts/test-results-finalization.xml). Local Mangum smoke handled the health route and a `clear_change` investigation. |
| `GITHUB_PUBLISHED` | **PASS, latest edits pending** | Public repo: [github.com/axfrgo/fortifiers-incident-memory](https://github.com/axfrgo/fortifiers-incident-memory). Public HEAD before this AWS update was `96af50c520e8ceaa0f63adda66c107294311cb2c`. New Lambda files and updated deployment docs are not pushed yet. |
| `AWS_DEPLOYED` | **BLOCKED** | AWS billing shows an active Free Plan credit, but CloudShell reports account verification is still in progress. No project stack, image, function or public URL exists yet. See [deployment manifest](deployment-manifest.json) and [deployment notes](DEPLOYMENT.md). |
| `REMOTE_TESTED` | **BLOCKED** | There is no endpoint to test; no cloud investigation, evidence download or CloudWatch invocation has occurred. |
| `VIDEO_RECORDED` | **PASS, AWS narration outdated** | Actual local application recording: 220.4 seconds (3:40), 1920×1080, silent, synthetic-only. Its recording-time disclosure says AWS was not deployed. It must be replaced or supplemented if AWS becomes live. |
| `VIDEO_ACCESSIBLE` | **PASS** | Unlisted YouTube video: [youtu.be/_k0J1XHyVyA](https://youtu.be/_k0J1XHyVyA). Previously verified without authentication. |
| `DEVPOST_PREPARED` | **PASS, incomplete** | A private solo draft is saved at 4/5 steps with video/repository/story fields. It does not contain a live AWS endpoint. |
| `DEVPOST_SUBMITTED` | **BLOCKED** | The entry is not submitted. Entrant eligibility/legal declarations and explicit final submit approval remain required. |
| `SUBMISSION_CONFIRMED` | **BLOCKED** | No successful submission state or confirmation exists. |

## Technical criteria

| Requirement | Status | Evidence |
|---|---|---|
| OpenCV 5 | **PASS locally** | The local runtime reports 5.0.0; actual processing uses ORB/RANSAC, ECC fallback, HSV normalization, masks, morphology, connected components and evidence overlays. AWS container build and runtime still require verification. |
| Agentic Vision | **PASS locally** | Seven procedural policy scenarios produce observation-dependent traces; blurred input requests another frame, older history downgrades a candidate, and illumination-only change is rejected. No cloud trace yet. |
| Automated tests | **PASS locally** | Fresh test artifact shows 36/36 passed. The exact AWS image has not yet been built. |
| Evaluation | **PASS, synthetic only** | Seven held-out procedural scenario types: expected task action 7/7 vs one-pass 4/7. Four generated masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller p50/p95 137.061/217.262 ms from 21 local runs. These are not field leak-detection metrics. See [EVALUATION.md](EVALUATION.md). |
| Code/archive | **PASS / updating** | Public GitHub repository exists. New AWS templates and this status edit are pending push; source ZIP must be rebuilt, extracted, tested and uploaded to the public release after the final commit. |
| Public web demo | **BLOCKED** | No remote URL exists. The local server is not judge-accessible and does not satisfy AWS execution. |
| Documentation | **PASS / updating** | README, technical report, architecture, evaluation, responsible use, deployment, scorecard, submission wording and demo script exist. AWS deployment documentation now targets Lambda. |
| Video team-identification requirement | **PARTIAL** | Current video is silent and does not show or name the entrant. Do not fabricate an appearance or voice. If the rules require visible team identification, the solo entrant must record their own introduction. |
| Solo eligibility | **BLOCKED for verification** | The entrant reports entering solo. The entrant must personally confirm official age/location eligibility and rights declarations. |
| Devpost submission | **BLOCKED** | [Saved draft](https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/project_details/edit) is not a submitted entry. |

## Links and facts

- **Repository:** https://github.com/axfrgo/fortifiers-incident-memory
- **Last independently verified public commit:** `96af50c520e8ceaa0f63adda66c107294311cb2c`
- **Unlisted video:** https://youtu.be/_k0J1XHyVyA
- **AWS endpoint:** none.
- **AWS resources created for this project:** none. **Verified project spend:** $0.
- **Devpost draft:** https://devpost.com/software/fortifiers-incident-memory (private, not submitted).
- **Evaluation limitations:** procedural fixtures only; no licensed real-world leak dataset, field testing or calibrated probabilities.

## Remaining actions

1. AWS must finish account verification so CloudShell or another deployment route can run. The attempted CloudShell session was blocked before it could execute commands.
2. AWS CodeConnections approval is pending before linking CloudFormation to the public repository. If AWS asks for permissions beyond this repository or write access, stop and review them.
3. Deploy, call the live URL from an unauthenticated session, verify the three scenarios, S3 evidence bundle, review action and CloudWatch logs, and update the endpoint/build evidence.
4. Re-record or supplement the video with the real AWS endpoint if deployment succeeds. The solo entrant must supply any required personal introduction.
5. Update the Devpost draft with the live endpoint and finish the remaining page steps. Ask the entrant to review eligibility/legal declarations and explicitly approve the irreversible final submission.
