# Final submission status

**Checked:** 2026-10-27 06:22:27 UTC. **Official deadline target:** 2026-10-27 06:45 UTC (02:45 EDT / 03:45 ADT).

## Release states

| State | Status | Evidence |
|---|---|---|
| LOCAL_VERIFIED | PASS | Python 3.14.0 and OpenCV 5.0.0. The latest recorded full suite is 37 passed, 0 failed, 0 skipped; the extracted portable archive also passed 37/37. See `artifacts/test-results.xml`, `artifacts/test-results.json`, and `artifacts/source-archive-validation.json`. |
| GITHUB_PUBLISHED | PASS | Public repository: https://github.com/axfrgo/fortifiers-incident-memory. The public source archive is available at the release URL below. Finalization status and ledger updates are published to master; anonymous GitHub API verification confirms the PASS states are present. |
| AWS_DEPLOYED | PASS | Public AWS Lambda Function URL: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/. It runs the actual FastAPI/OpenCV workload. Deployed app commit: `b851290df9e99aca1a232c018e53bff48b8f559d`; OpenCV 5.0.0. |
| REMOTE_TESTED | PASS | Anonymous HTTP health and all seven built-in synthetic investigations succeeded with distinct expected outcomes. Evidence ZIP download and CloudWatch executions were verified. See `artifacts/aws-remote-results.json`, `artifacts/aws-verification/current-smoke.json`, and `artifacts/aws-verification/cloudwatch-observation.json`. |
| VIDEO_RECORDED | PASS | Genuine silent/captioned application capture, 220.4 s (3:40), 1920×1080; `artifacts/video/video-manifest.json`. |
| VIDEO_ACCESSIBLE | PASS | Unlisted video: https://youtu.be/_k0J1XHyVyA. |
| VIDEO_CONTENT_COMPLIANCE | BLOCKED | Video was recorded before AWS deployment, so it does not show the live AWS endpoint and does not identify the solo entrant. The submitted project page discloses this limitation. |
| DEVPOST_PREPARED | PASS | Entry contains project narrative, live AWS URL, public repo and archive, demo video, technical claims with synthetic-data limitations, and Agentic Vision selection. |
| DEVPOST_SUBMITTED | PASS | Devpost displayed “Project submitted!” after the authorized Submit project action. Public project URL: https://devpost.com/software/fortifiers-incident-memory. |
| SUBMISSION_CONFIRMED | PASS | Devpost showed its Project submitted confirmation and the resulting project page displayed the AWS endpoint, repository, archive, video, and competition. Confirmation was captured in the active browser session on 2026-10-27. A direct unauthenticated script request was met by Devposts Cloudflare JavaScript challenge, so no separate anonymous HTTP check is claimed. |

## Competition evidence

| Criterion | Status | Evidence and limits |
|---|---|---|
| OpenCV 5 | PASS | OpenCV 5.0.0 verified locally and in AWS runtime. Registration, illumination normalization, difference masks, morphology, connected components, region measurements, and overlays are implemented. |
| Agentic Vision | PASS | Actual traces show observations changing later calls/actions: poor image → request another frame; candidate region → ROI inspection/history retrieval; older matching frame → downgrade novelty; sensor-correlated candidate → human review. See remote traces in `artifacts/aws-remote-results.json`. |
| Automated tests | PASS | 37/37 tests in the latest recorded local run and 37/37 from extracted source archive. This suite is not an AWS service test suite. One existing Starlette/AnyIO deprecation warning. |
| Evaluation | PASS, synthetic only | Seven generated held-out scenario types: expected policy action 7/7 vs one-pass 4/7. Four generated masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller p50/p95 137.061/217.262 ms over 21 local runs. These are fixture/controller measurements, not real-world leak detection. |
| Public demo | PASS | Unauthenticated public AWS endpoint processes only built-in synthetic scenarios; arbitrary user uploads are disabled. |
| Repository/archive | PASS | Public repository and downloadable source archive are linked from the submitted Devpost entry. |
| Documentation | PASS | README, technical report, architecture and agent diagrams, evaluation, responsible use, deployment, scorecard, submission wording, demo script, and machine-readable test results are in the repository. |
| Video requirement | BLOCKED | Video is public/unlisted and below five minutes, but lacks the live AWS walkthrough and entrant identification as disclosed above. |
| Solo entry | PASS | Devpost shows Alexander Ferguson as the sole listed teammate. |
| Final submission | PASS | Devpost confirmation banner and public submitted project page were verified. |

## Links, deployment, and costs

- Devpost project: https://devpost.com/software/fortifiers-incident-memory
- Public repository: https://github.com/axfrgo/fortifiers-incident-memory
- Public portable source archive: https://github.com/axfrgo/fortifiers-incident-memory/releases/download/demo-2026-10-27/fortifiers-incident-memory-source.zip
- AWS demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/
- AWS health: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/health
- Video: https://youtu.be/_k0J1XHyVyA (Unlisted, 3:40; predates AWS deployment)
- AWS region/runtime: us-east-2; Python 3.14 ZIP Lambda; OpenCV 5.0.0; 512 MiB memory; 90-second timeout; no reserved concurrency.
- AWS controls: private S3 evidence with SSE-S3 and seven-day expiry; CloudWatch logs retained 14 days; uploads disabled. The account remained on the Free Plan. Billing is not fully reconciled, AWS usage reporting may lag, and credits are not a hard spending cap; no claim of zero cost is made.
- AWS resources: CloudFormation app stack `fortifiers-incident-memory-demo-free-3`; supporting Lambda, private S3 evidence bucket, CloudWatch logs, and deployment bootstrap resources. CodeBuild/ECR were provisioned, but CodeBuild could not start because the account build quota was zero. The current running vision service is ZIP-based Lambda.
- The approved CodeConnections setup was unnecessary: the verified Lambda deployment was already live, so no additional repository access connection was created.

## Remaining user actions

1. If time remains before the deadline, record and replace the video with an AWS-inclusive version that identifies the entrant, then verify its public link.
2. Review AWS billing after usage has fully posted; disable public invocation after judging if no longer needed.

