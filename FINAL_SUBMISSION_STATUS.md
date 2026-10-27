# Final submission status

**Checked:** 2026-10-27 05:45 UTC. **Target deadline:** 2026-10-27 06:45 UTC (the earlier Devpost time, in UTC).

## Required release states

| State | Status | Evidence |
|---|---|---|
| LOCAL_VERIFIED | PASS | Python 3.14.0, OpenCV 5.0.0; latest complete suite 37 passed, 0 failed, 0 skipped in 7.44 s. Final portable archive extraction also passed 37/37 (7.92 s in the latest validation). One Starlette/AnyIO deprecation warning. See `artifacts/test-results.xml`, `artifacts/test-results.json`, and `artifacts/source-archive-validation.json`. |
| GITHUB_PUBLISHED | PASS | Public repository https://github.com/axfrgo/fortifiers-incident-memory. Commit `e8230146d46383c15cc2f445dd476ffe68515599` and raw README/status returned anonymous HTTP 200 at 05:43 UTC. This status/ledger update is being published as a follow-up commit. |
| AWS_DEPLOYED | PASS | Public AWS Lambda Function URL https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/; anonymous `/health` reported OpenCV 5.0.0 and AWS Lambda mode. Deployment commit is `b851290df9e99aca1a232c018e53bff48b8f559d`; CloudFormation stack `fortifiers-incident-memory-demo-free-3` is `UPDATE_COMPLETE`. |
| REMOTE_TESTED | PASS | Anonymous homepage, health and all seven scenarios returned HTTP 200 with distinct expected outcomes; clear-change evidence ZIP downloaded and integrity-checked; CloudWatch confirms actual Lambda executions. Evidence: `artifacts/aws-remote-results.json`, `artifacts/aws-verification/current-smoke.json`, `artifacts/aws-verification/cloudwatch-observation.json`. |
| VIDEO_RECORDED | PASS | Existing silent/captioned local application capture is 220.4 s (3:40), 1920×1080. Manifest: `artifacts/video/video-manifest.json`. It predates AWS deployment. |
| VIDEO_ACCESSIBLE | PASS | Unlisted YouTube video https://youtu.be/_k0J1XHyVyA and public GitHub mirror are accessible. Video content is outdated for the deployed service. |
| DEVPOST_PREPARED | PASS | Private solo draft has AWS URL, repository, testing instructions, and Agentic Vision selection. The source archive is attached; page shows DRAFT and 4/5 steps. Management page: https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/finalization. |
| DEVPOST_SUBMITTED | BLOCKED | The entrant has not yet personally approved the rules/terms checkbox or the final Submit project action. |
| SUBMISSION_CONFIRMED | BLOCKED | Devpost has not displayed a submitted/success state. |

## Technical and presentation criteria

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 | PASS | Verified locally and on AWS as 5.0.0; actual image registration, normalization, difference masks, morphology, connected components and overlays. |
| Agentic Vision | PASS | OpenCV observations change subsequent calls: poor image → retake; candidate → ROI inspection/history retrieval; historical match → novelty downgrade; sensor-correlated candidate → human review. Seven remote traces are in `artifacts/aws-remote-results.json`. |
| Automated tests | PASS | 37/37 on Python 3.14/OpenCV 5; local and extracted-archive results are in `artifacts/test-results.xml`, `artifacts/test-results.json`, and `artifacts/source-archive-validation.json`. These are not AWS service tests. |
| Evaluation | PASS, synthetic only | Seven generated held-out scenario types: expected policy action 7/7 vs one-pass 4/7. Four generated masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller p50/p95 137.061/217.262 ms over 21 local runs. None estimates field leak-detection performance. |
| Public web demo | PASS | Public unauthenticated AWS endpoint runs the vision workload; arbitrary uploads are disabled and only synthetic demo scenarios are exposed. |
| Code and archive | PASS | Public GitHub source and release archive. At 05:43 UTC the archive URL returned 200 anonymously, and a downloaded copy matched the local SHA-256. A final package including this status/ledger update is being rebuilt and will replace the same asset. |
| Documentation | PASS | README, technical report, architecture and agent diagrams, evaluation, responsible-use, deployment, scorecard, submission wording, demo script, and machine-readable test results are in the public repository. |
| Video content compliance | BLOCKED | Existing video omits AWS, predates deployment, and does not show/identify the entrant. No replacement recording tool is available in this session. Do not describe the old video as an AWS demo. |
| Solo registration | PASS | User states they are entering solo; Devpost currently shows one teammate. Other eligibility and submission declarations remain for the entrant to review personally. |
| Final Devpost submission | BLOCKED | Draft saved; final terms declaration and submission action await explicit entrant authorization. |

## Links and deployment facts

- Repository: https://github.com/axfrgo/fortifiers-incident-memory
- Public source archive: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- AWS demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/
- AWS health: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/health
- Video: https://youtu.be/_k0J1XHyVyA (Unlisted, 3:40, local-only at recording time)
- Devpost preview: https://devpost.com/software/fortifiers-incident-memory (not submitted)
- Devpost draft management: https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/finalization
- AWS region: `us-east-2`; account stayed on the Free Plan; no paid-plan upgrade was performed.
- Runtime: Python 3.14 ZIP Lambda, OpenCV 5.0.0, 512 MiB memory, 90-second timeout, no reserved concurrency.
- Private S3 evidence uses SSE-S3 and seven-day expiry; CloudWatch log retention is 14 days; user uploads are disabled.
- Billing usage has not been reconciled; AWS reporting may lag and Free Plan credits are not a hard spending cap. No cost-free claim is made.
- CodeBuild/ECR were provisioned, but CodeBuild could not start because the account's queued-build quota is zero; the running workload is a ZIP Lambda deployment.

## Remaining actions

1. Rebuild, extract, test, and anonymously verify the final source archive containing this update; replace the public release asset and Devpost attachment.
2. The entrant may record a replacement AWS-inclusive video showing their own identity. The existing Unlisted video is genuine but outdated.
3. Review age/location/IP and official rules declarations personally.
4. Explicitly approve accepting the official rules/Devpost terms and submitting; verify Devpost success before marking submitted.
5. Monitor AWS billing after usage reporting updates and disable public invocation after judging if it is no longer needed.
