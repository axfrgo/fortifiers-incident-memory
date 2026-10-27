# Final submission status

**Checked:** 2026-10-27 05:47 UTC. **Target deadline:** 2026-10-27 06:45 UTC (the earlier Devpost time, in UTC).

## Required release states

| State | Status | Evidence |
|---|---|---|
| LOCAL_VERIFIED | PASS | Python 3.14.0, OpenCV 5.0.0; latest complete suite 37 passed, 0 failed, 0 skipped in 7.44 s. The extracted portable package passed 37/37 in 7.91 s. One Starlette/AnyIO deprecation warning. See `artifacts/test-results.xml`, `artifacts/test-results.json`, and `artifacts/source-archive-validation.json`. |
| GITHUB_PUBLISHED | PASS | Public repository https://github.com/axfrgo/fortifiers-incident-memory. Anonymous HTTP 200 for repository, README, status and source-archive manifest at 05:48 UTC. Public source commit `46a4a02cc37b50baa99ca200815e61564ef0dbe1` contains the release/status update. |
| AWS_DEPLOYED | PASS | Public AWS Lambda Function URL https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/; anonymous `/health` reports OpenCV 5.0.0 and AWS Lambda mode. Deployed app commit is `b851290df9e99aca1a232c018e53bff48b8f559d`; CloudFormation stack `fortifiers-incident-memory-demo-free-3` is `UPDATE_COMPLETE`. |
| REMOTE_TESTED | PASS | Anonymous homepage, health and all seven synthetic scenarios returned HTTP 200 with distinct expected outcomes; clear-change evidence ZIP downloaded and integrity-checked; CloudWatch confirms actual Lambda executions. Evidence: `artifacts/aws-remote-results.json`, `artifacts/aws-verification/current-smoke.json`, `artifacts/aws-verification/cloudwatch-observation.json`. |
| VIDEO_RECORDED | PASS | Existing silent/captioned local application capture is 220.4 s (3:40), 1920×1080. Manifest: `artifacts/video/video-manifest.json`. It predates AWS deployment. |
| VIDEO_ACCESSIBLE | PASS | Unlisted YouTube video https://youtu.be/_k0J1XHyVyA and public GitHub mirror are accessible. |
| DEVPOST_PREPARED | PASS | Private solo draft has the AWS URL, repository, testing instructions, and Agentic Vision selection. Current source archive is attached; Devpost showed DRAFT and 4/5 steps at 05:47 UTC. |
| DEVPOST_SUBMITTED | BLOCKED | No final submission has been made. The entrant has not authorized the rules/terms declaration or Submit project action. |
| SUBMISSION_CONFIRMED | BLOCKED | Devpost has not displayed a submitted/success state. |

## Technical and presentation criteria

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 | PASS | Verified locally and on AWS as 5.0.0; actual registration, illumination normalization, difference masks, morphology, connected components and overlays. |
| Agentic Vision | PASS | OpenCV observations change later calls: poor image → retake; candidate → ROI inspection/history retrieval; historical match → novelty downgrade; sensor-correlated candidate → human review. Seven remote traces are in `artifacts/aws-remote-results.json`. |
| Automated tests | PASS | 37/37 on Python 3.14/OpenCV 5 locally and 37/37 from the extracted portable archive. The tests are not AWS service tests. |
| Evaluation | PASS, synthetic only | Seven generated held-out scenario types: expected policy action 7/7 vs one-pass 4/7. Four generated masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller p50/p95 137.061/217.262 ms over 21 local runs. None estimates field leak-detection performance. |
| Public web demo | PASS | Public unauthenticated AWS endpoint runs the vision workload; arbitrary uploads are disabled and only synthetic scenarios are exposed. |
| Code and archive | PASS | Public repository and release ZIP are anonymously accessible; the downloaded release matched its local checksum and passed ZIP integrity. The current checksum is in `artifacts/source-archive-manifest.json`. |
| Documentation | PASS | README, technical report, architecture and agent diagrams, evaluation, responsible-use, deployment, judging scorecard, submission wording, demo script, and machine-readable test results are included. |
| Video content compliance | BLOCKED | The existing video is genuine and under five minutes but predates AWS, does not demonstrate the deployed endpoint, and does not identify the entrant. No screen-recording tool is exposed in this session. |
| Solo registration | PASS | User says they are entering solo; Devpost shows one teammate. Other eligibility and submission declarations remain for the entrant to review personally. |
| Final Devpost submission | BLOCKED | The saved draft awaits personal review of the official rules and Devpost terms, plus explicit authorization for final submission. |

## Links and deployment facts

- Repository: https://github.com/axfrgo/fortifiers-incident-memory
- Public source archive: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- AWS demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/
- AWS health: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/health
- Video: https://youtu.be/_k0J1XHyVyA (Unlisted, 3:40; local-only when recorded)
- Devpost preview: https://devpost.com/software/fortifiers-incident-memory (not submitted)
- Devpost draft: https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/finalization
- AWS region: `us-east-2`; the account stayed on the Free Plan; no paid-plan upgrade was performed.
- Runtime: Python 3.14 ZIP Lambda, OpenCV 5.0.0, 512 MiB memory, 90-second timeout, no reserved concurrency.
- Private S3 evidence uses SSE-S3 and seven-day expiry; CloudWatch logs expire after 14 days; uploads are disabled.
- Billing usage has not been reconciled; AWS reporting may lag and Free Plan credits are not a hard spending cap. No cost-free claim is made.
- CodeBuild/ECR were provisioned, but CodeBuild could not start because the account's queued-build quota is zero; the running workload is the ZIP Lambda.

## Remaining actions

1. The entrant should record and publish an updated AWS-inclusive video using their own identity if required by the competition.
2. The entrant should personally review the official rules and eligibility declarations.
3. The entrant must explicitly authorize accepting the terms declaration and submitting the project; verify the success state before marking it submitted.
4. Check AWS usage after billing reports update, and disable public invocation after judging if it is no longer needed.
