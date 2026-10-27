# Final submission status

**Checked:** 2026-10-27 05:39 UTC. **Earlier displayed deadline:** 2026-10-27 06:45 UTC. Competition submission availability should be checked in the signed-in Devpost page; this deadline may now be close.

## Required release states

| State | Status | Evidence |
|---|---|---|
| LOCAL_VERIFIED | PASS | Python 3.14.0, OpenCV 5.0.0; latest full suite 37 passed, 0 failed, 0 skipped in 7.44 s; extracted final archive suite 37/37 in 9.78 s, one Starlette/AnyIO deprecation warning. See artifacts/test-results.xml and artifacts/test-results.json. |
| GITHUB_PUBLISHED | PASS | Public repository https://github.com/axfrgo/fortifiers-incident-memory; deployed source commit b851290df9e99aca1a232c018e53bff48b8f559d is public. Current documentation/evidence updates are being packaged for a final push. |
| AWS_DEPLOYED | PASS | Public AWS Lambda URL https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/; health reports OpenCV 5.0.0 and commit b851290df9e99aca1a232c018e53bff48b8f559d. CloudFormation app stack UPDATE_COMPLETE. |
| REMOTE_TESTED | PASS | Anonymous root/health and seven scenarios; 7/7 HTTP 200; distinct expected outcomes; clear-change evidence ZIP downloaded and integrity-checked. CloudWatch shows real function invocations. See artifacts/aws-remote-results.json, artifacts/aws-verification/current-smoke.json, artifacts/aws-verification/cloudwatch-observation.json and deployment-manifest.json. |
| VIDEO_RECORDED | PASS | Existing actual silent/captioned local app screen capture is 220.4 s (3:40), 1920×1080. See artifacts/video/video-manifest.json. It predates AWS deployment and does not show the current cloud endpoint. |
| VIDEO_ACCESSIBLE | PASS | Unlisted YouTube URL https://youtu.be/_k0J1XHyVyA and public GitHub release mirror are accessible. The current video's AWS end card reflects the earlier recording date; the video has not been refreshed. |
| DEVPOST_PREPARED | PASS | Private solo draft saved; project details, live AWS endpoint, repository, synthetic test instructions and Agentic Vision selection are saved. Current page is the finalization step at 4/5. |
| DEVPOST_SUBMITTED | BLOCKED | No final submission has been made. The finalization page asks the entrant to accept the official rules/Devpost terms and click Submit. |
| SUBMISSION_CONFIRMED | BLOCKED | No success confirmation or submitted public project state has been observed. |

## Technical and presentation criteria

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 | PASS | Local and AWS health report major version 5; actual ORB/RANSAC, ECC, HSV normalization, masks, morphology and connected components. AWS build commit is b851290df9e99aca1a232c018e53bff48b8f559d. |
| Agentic Vision | PASS | Real OpenCV observations change the next tool call: poor image → retake; candidate → ROI/history retrieval; historical match → novelty downgrade; sensor-correlated candidate → human review. Seven remote traces are in artifacts/aws-remote-results.json. |
| Automated tests | PASS | 37/37 on Python 3.14 and OpenCV 5; artifacts/test-results.xml and artifacts/test-results.json. No AWS service or Docker tests are represented by this suite. |
| Evaluation | PASS, synthetic only | Seven held-out scenario types: expected policy action 7/7 vs one-pass 4/7. Four synthetic masks: precision 0.99183, recall 0.99913, F1 0.99546 and IoU 0.99097. Local controller p50/p95: 137.061/217.262 ms over 21 runs. These do not estimate field leak-detection performance. |
| Public web demo | PASS | Public unauthenticated AWS Function URL runs the OpenCV workload. Only seven synthetic scenarios are exposed; arbitrary uploads are disabled. |
| Code/archive | PASS, final docs push pending | Public repository is accessible. Current source archive is rebuilt with the AWS deployment evidence and Lambda ZIP exclusion fix; it has passed ZIP-integrity and extracted 37-test checks. Upload the refreshed asset to the public release and Devpost draft and verify anonymous access. |
| Architecture and reports | PASS, final docs push pending | TECHNICAL_REPORT.md, ARCHITECTURE.md, updated architecture SVG, agent workflow, evaluation, responsible-use notes, submission wording and ledger. |
| Video content compliance | BLOCKED | The accessible under-five-minute video demonstrates the local app and results but was recorded before deployment, says AWS was not deployed, does not show the cloud endpoint, and does not name/show the entrant. A new recording and the entrant's own identity introduction are still needed if required by the rules. |
| Solo eligibility | BLOCKED for entrant confirmation | User reports a solo entry and Devpost shows one teammate. Age/location/IP/terms declarations must be personally reviewed by the entrant. |
| Final Devpost submission | BLOCKED | Prepared draft is saved but the entrant must approve the legal declarations and final irreversible submit action. |

## Links and deployment facts

- Repository: https://github.com/axfrgo/fortifiers-incident-memory
- Deployed application commit: b851290df9e99aca1a232c018e53bff48b8f559d
- Live AWS demo: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/
- Health: https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/health
- Video: https://youtu.be/_k0J1XHyVyA (Unlisted, 3:40, local-only at recording time)
- Draft preview: https://devpost.com/software/fortifiers-incident-memory (not public/submitted)
- Draft management: https://devpost.com/submit-to/30984-opencv-ai-competition-2026-powered-by-aws/manage/submissions/1266641-fortifiers-incident-memory/finalization
- App stack: fortifiers-incident-memory-demo-free-3 (UPDATE_COMPLETE)
- Bootstrap stack: fortifiers-incident-memory-bootstrap (CREATE_COMPLETE)
- AWS region: us-east-2; Free Plan selected; no Paid Plan upgrade.
- Runtime: Python 3.14, OpenCV 5.0.0, Lambda ZIP package, 512 MiB memory, 90-second timeout, no reserved concurrency.
- S3 evidence is private, SSE-S3 encrypted and expires after seven days; CloudWatch logs expire after 14 days; user uploads are disabled.
- Account credit was active before deployment. Current project spend has not been reconciled in Billing; the Free Plan credit is not a hard spending cap. Do not claim the deployment was cost-free.
- Failed app-stack attempts remain as CloudFormation rollback history. CodeBuild/ECR were provisioned but CodeBuild could not start because the account queue quota is zero; the actual OpenCV workload runs from the ZIP Lambda package.

## Remaining actions

1. Upload the current validated source archive to the existing public GitHub release, replace the older archive attachment in the private Devpost draft, and verify the public download anonymously.
2. A human entrant should record an AWS-inclusive video using the real browser and their own name/identity if the competition requires team identification; replace the older video URL and verify it anonymously.
3. Review eligibility, intellectual-property declarations and official rules in Devpost.
4. Explicitly approve accepting the terms and submitting the project before the actual submission form closes. Submission remains unconfirmed until Devpost displays success.
5. Check billing usage in AWS after its reporting delay. After judging, disable public Function URL access or remove only this project's stacks/resources when no longer needed.


