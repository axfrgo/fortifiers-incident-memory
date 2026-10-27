# Final submission status

**Last checked:** 2026-10-27 UTC. **Target deadline:** 2026-10-27 06:45 UTC (October 26, 11:45 PM PDT; October 27, 03:45 AM ADT). The earlier banner time is used because the competition page also contains a conflicting 11:59 PM Pacific reference. Recheck the live Devpost countdown before attempting submission.

This is an evidence-based release status, not a claim that the entry is complete or eligible. AWS execution, public demo endpoint, video, Devpost draft, team eligibility details, and final submission are unresolved. No AWS resources were created. The prior user instruction was to prepare deployment only, and no final submission approval has been given.

## Requested release states

| State | Status | Supporting evidence |
|---|---|---|
| `LOCAL_VERIFIED` | **PASS** | OpenCV runtime reports 5.0.0; pinned `opencv-python-headless==5.0.0.93`; fresh local suite 36 passed, 0 failed, 0 skipped in [`artifacts/test-results.xml`](artifacts/test-results.xml); extracted source archive rebuilt and retested; local HTTP and dashboard evidence in [`artifacts/final-local-verification.json`](artifacts/final-local-verification.json). |
| `GITHUB_PUBLISHED` | **PASS** | Public repository: [github.com/axfrgo/fortifiers-incident-memory](https://github.com/axfrgo/fortifiers-incident-memory). Anonymous Git `ls-remote` and unauthenticated GitHub API verified visibility `public`, branch `master`, initial public release commit `c76079bc6e79493d096e1d9eba9ff05d29ef7d1e`, and status/evidence commit `4c94d4803984aa92964637cd60b78d11640aaaa7`. The separate `fortifiers` repository was not changed. |
| `AWS_DEPLOYED` | **BLOCKED** | No AWS resources or AWS endpoint exist. Deployment was explicitly limited to preparation; AWS CLI, Docker and credentials were unavailable. Current AWS documentation says App Runner is closed to new customers, and this account's existing access is unverified. See [`DEPLOYMENT.md`](DEPLOYMENT.md) and [`deployment-manifest.json`](deployment-manifest.json). |
| `REMOTE_TESTED` | **BLOCKED** | No AWS service URL exists, so no remote investigation, CloudWatch execution, anonymous browser test, or remote evidence ZIP test could be performed. Local `127.0.0.1` results are not remote evidence. |
| `VIDEO_RECORDED` | **BLOCKED** | No video file was recorded. [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) is a timed storyboard only; an actual team member must provide the team identification segment. |
| `VIDEO_ACCESSIBLE` | **BLOCKED** | No hosted video or public/unlisted link exists. |
| `DEVPOST_PREPARED` | **BLOCKED** | Accurate offline wording is in [`SUBMISSION.md`](SUBMISSION.md), but there is no Devpost draft. The registered account's project list was empty; “Start project” returned a reCAPTCHA connection error. AWS/video links and verified team details are also missing. |
| `DEVPOST_SUBMITTED` | **BLOCKED** | No submission was made. The user has not given final approval for that irreversible action. |
| `SUBMISSION_CONFIRMED` | **BLOCKED** | There is no submitted project URL, confirmation state, or submission receipt. |

## Requirement evidence

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 visual processing | **PASS locally** | Runtime `cv2.__version__ == 5.0.0`; real image validation, quality checks, ORB/RANSAC registration, ECC fallback, HSV normalization, masks, connected regions and overlays. No AWS runtime verification. |
| Observation-driven Agentic Vision | **PASS locally** | Actual traces in [`artifacts/final-local-verification.json`](artifacts/final-local-verification.json): poor-image quality skips comparison and requests a retake (5 actions); clear candidate triggers ROI inspection, older-frame retrieval and sensor correlation before human review (9 actions); illumination-normalized lighting shift returns no visual change (6 actions). These are synthetic local fixtures. |
| Automated tests | **PASS locally** | Fresh run: 36 passed, 0 failed, 0 skipped; one Starlette/AnyIO deprecation warning. Raw JUnit XML: [`artifacts/test-results.xml`](artifacts/test-results.xml). Docker/AWS service tests were not run. |
| Evaluation | **PASS, synthetic-only** | Seven held-out scenario types × three runs: expected controller actions 7/7 vs 4/7 for the simple one-pass comparator. Across four synthetic pixel-labeled masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller latency p50/p95 137.061/217.262 ms. These are procedural fixtures, not real leak-detection performance. See [`EVALUATION.md`](EVALUATION.md) and [`artifacts/evaluation.json`](artifacts/evaluation.json). |
| Public source and reproducibility | **PASS** | Public GitHub repository above; pinned lockfile, build/test instructions, three prior commits and the finalization commit. [`artifacts/source-archive-manifest.json`](artifacts/source-archive-manifest.json) records a locally rebuilt portable ZIP checksum; GitHub's public repository is the judge-accessible source/archive mechanism. |
| AWS workload and judge endpoint | **BLOCKED** | No resources were created; prepared App Runner template is conditional on account access and was not deployed or AWS-validated. Current service availability may require a different AWS design for a new customer. |
| Documentation and diagrams | **PASS** | [`README.md`](README.md), [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`submission/architecture.svg`](submission/architecture.svg), [`AGENT_WORKFLOW.md`](AGENT_WORKFLOW.md), [`submission/agent-workflow.svg`](submission/agent-workflow.svg), [`RESPONSIBLE_USE.md`](RESPONSIBLE_USE.md), [`DEPLOYMENT.md`](DEPLOYMENT.md), [`JUDGING_SCORECARD.md`](JUDGING_SCORECARD.md), [`SUBMISSION.md`](SUBMISSION.md), [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md), [`LICENSES_AND_DATA_PROVENANCE.md`](LICENSES_AND_DATA_PROVENANCE.md), and machine-readable test/evaluation artifacts. |
| Dataset and rights | **PASS for included fixtures** | Included incident frames and labels are project-generated synthetic data; YuNet provenance is documented. No real facility imagery or real-world validation is included. Project-level source redistribution license remains unselected; see `LICENSES_AND_DATA_PROVENANCE.md`. |
| Team eligibility and registration | **BLOCKED** | Devpost account registration was observed, but the actual team roster, representative, ages/legal-majority status, and declarations are unknown. Rules and overview contain differing age wording; resolve with the organizer and actual team before submission. |
| Final Devpost submission | **BLOCKED** | No draft or submission exists; the form hit a reCAPTCHA connection error. Final user approval is still required after all mandatory fields/links are reviewed. |

## Deployment and cost record

- AWS resources created: **none**. AWS account/credits and App Runner eligibility: **unverified**. Live URL: **none**.
- Prepared plan (conditional on App Runner availability): `us-east-1` illustrative estimate, one 0.5-vCPU/1-GB instance at about **$5.11/month idle**, plus about **$0.032 per processing hour**. Eight processing hours/day estimates about **$12.79/month** of App Runner compute/memory; continuous processing estimates about **$28.47/month**, before ECR, S3, logs, transfer, taxes, scale-out, or other usage. These are not guaranteed caps or verified account quotes. Budget alerts do not cap spend.
- The user asked what AWS deployment would require and whether it costs money. No new deployment authorization was given; the earlier “prepare only” direction remains active. A secure AWS identity, service eligibility, chosen architecture/region, and explicit spend approval are required before resource creation.

## Exact links and remaining actions

- Repository: https://github.com/axfrgo/fortifiers-incident-memory
- AWS endpoint: none
- Demo video: none
- Devpost project: none
- Fresh local test result: 36/36 passing; synthetic-only evaluation as described above.
- Outstanding user/team actions: arrange an eligible and authorized AWS account/service plus secure local CLI/role access and a spend ceiling if AWS deployment is desired; otherwise acknowledge the AWS criterion remains unmet. Record and host the real sub-five-minute team/application demo. Resolve Devpost reCAPTCHA, provide/verify team and eligibility details, complete the mandatory project fields, review the final draft, and explicitly approve submission before it is submitted.

Official competition links: [Devpost overview](https://opencv26.devpost.com/) and [rules](https://opencv26.devpost.com/rules). Do not infer award eligibility from this local verification package.
