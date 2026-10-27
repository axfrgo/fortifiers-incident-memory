# Final submission status

**Last checked:** 2026-10-27 02:17 UTC (October 26, 23:17 ADT). **Target deadline:** 2026-10-27 06:45 UTC (October 26, 11:45 PM PDT; October 27, 03:45 AM ADT), about 4 hours 28 minutes after this check. The official banner still shows the earlier time despite a conflicting 11:59 PM Pacific reference in the overview; target the banner time.

This is an evidence-based release status, not a claim that the entry is complete or eligible. Local verification and public source access are complete. AWS execution, public demo endpoint, video, complete Devpost form, team eligibility details, and final submission remain unresolved. No AWS resources were created because this environment has no authenticated AWS console/CLI identity, and no specific spend ceiling has been authorized.

## Requested release states

| State | Status | Supporting evidence |
|---|---|---|
| `LOCAL_VERIFIED` | **PASS** | OpenCV runtime reports 5.0.0; pinned `opencv-python-headless==5.0.0.93`; freshly rerun suite: 36 passed, 0 failed, 0 skipped in 10.86 s. JUnit and JSON evidence: [`artifacts/test-results-finalization.xml`](artifacts/test-results-finalization.xml) and [`artifacts/test-results-finalization.json`](artifacts/test-results-finalization.json). Latest local HTTP results for the dashboard, health and four real investigation scenarios are in [`artifacts/finalization-api-smoke.json`](artifacts/finalization-api-smoke.json). |
| `GITHUB_PUBLISHED` | **PASS** | Public repository: [github.com/axfrgo/fortifiers-incident-memory](https://github.com/axfrgo/fortifiers-incident-memory). Commit `c0e95ec5bf01a789ce124ae4396574c48f341439` was checked without GitHub credentials: the public API reported it as `master` HEAD, and anonymous Contents API requests for README, this status file, test results and project cover returned their file contents; this status file includes the PASS state. The separate `fortifiers` production repository was not changed. |
| `AWS_DEPLOYED` | **BLOCKED** | No AWS resources or endpoint exist. The in-app browser redirected to AWS IAM sign-in; no local AWS CLI, Docker, or credential profile is configured. No specific spend limit was authorized. App Runner eligibility for this account is unverified. See [`DEPLOYMENT.md`](DEPLOYMENT.md) and [`deployment-manifest.json`](deployment-manifest.json). |
| `REMOTE_TESTED` | **BLOCKED** | No AWS service URL exists, so no remote investigation, CloudWatch execution, anonymous browser test, or remote evidence ZIP test could be performed. Local `127.0.0.1` results are not remote evidence. |
| `VIDEO_RECORDED` | **BLOCKED** | No video file was recorded. OBS and FFmpeg are unavailable; although Windows Snipping Tool is installed, this session exposes no controllable desktop recording surface. [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md) is a timed storyboard only. The project cover at [`submission/project-cover.png`](submission/project-cover.png) is a static image assembled from authentic local synthetic fixtures and OpenCV output, not a video or screen recording. |
| `VIDEO_ACCESSIBLE` | **BLOCKED** | No hosted video or public/unlisted link exists. |
| `DEVPOST_PREPARED` | **BLOCKED** | A private draft now exists in the registered Devpost account. It contains the title, revised “Give the Physical World a Memory” pitch, story, public repository link, authentic synthetic OpenCV cover in the thumbnail and gallery, source ZIP, test instructions and Agentic Vision award selection. The required video link is blank; no public AWS endpoint exists; eligibility declarations are unverified. It is not ready for submission or public review. |
| `DEVPOST_SUBMITTED` | **BLOCKED** | No submission was made. The user has not given final approval for that irreversible action. |
| `SUBMISSION_CONFIRMED` | **BLOCKED** | There is no submitted project URL, confirmation state, or submission receipt. |

## Requirement evidence

| Requirement | Status | Evidence and limitation |
|---|---|---|
| OpenCV 5 visual processing | **PASS locally** | Runtime `cv2.__version__ == 5.0.0`; real image validation, quality checks, ORB/RANSAC registration, ECC fallback, HSV normalization, masks, connected regions and overlays. No AWS runtime verification. |
| Observation-driven Agentic Vision | **PASS locally** | Actual traces in [`artifacts/final-local-verification.json`](artifacts/final-local-verification.json): poor-image quality skips comparison and requests a retake (5 actions); clear candidate triggers ROI inspection, older-frame retrieval and sensor correlation before human review (9 actions); illumination-normalized lighting shift returns no visual change (6 actions). These are synthetic local fixtures. |
| Automated tests | **PASS locally** | Fresh run: 36 passed, 0 failed, 0 skipped; one Starlette/AnyIO deprecation warning. Raw JUnit XML: [`artifacts/test-results-finalization.xml`](artifacts/test-results-finalization.xml). Docker/AWS service tests were not run. |
| Evaluation | **PASS, synthetic-only** | Seven held-out scenario types × three runs: expected controller actions 7/7 vs 4/7 for the simple one-pass comparator. Across four synthetic pixel-labeled masks: precision 0.99183, recall 0.99913, F1 0.99546, IoU 0.99097. Controller latency p50/p95 137.061/217.262 ms. These are procedural fixtures, not real leak-detection performance. See [`EVALUATION.md`](EVALUATION.md) and [`artifacts/evaluation.json`](artifacts/evaluation.json). |
| Public source and reproducibility | **PASS** | Public GitHub repository above; pinned lockfile and build/test instructions. [`artifacts/source-archive-manifest.json`](artifacts/source-archive-manifest.json) records the rebuilt portable ZIP checksum; GitHub's public repository is the judge-accessible source/archive mechanism. Finalization commit `c0e95ec5bf01a789ce124ae4396574c48f341439` is anonymously accessible. |
| AWS workload and judge endpoint | **BLOCKED** | No resources were created; prepared App Runner template is conditional on account access and was not deployed or AWS-validated. The AWS browser page is at IAM sign-in. The workload therefore has no judge-accessible URL or cloud execution evidence. |
| Documentation and diagrams | **PASS** | [`README.md`](README.md), [`TECHNICAL_REPORT.md`](TECHNICAL_REPORT.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`submission/architecture.svg`](submission/architecture.svg), [`AGENT_WORKFLOW.md`](AGENT_WORKFLOW.md), [`submission/agent-workflow.svg`](submission/agent-workflow.svg), [`RESPONSIBLE_USE.md`](RESPONSIBLE_USE.md), [`DEPLOYMENT.md`](DEPLOYMENT.md), [`JUDGING_SCORECARD.md`](JUDGING_SCORECARD.md), [`SUBMISSION.md`](SUBMISSION.md), [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md), [`LICENSES_AND_DATA_PROVENANCE.md`](LICENSES_AND_DATA_PROVENANCE.md), and machine-readable test/evaluation artifacts. |
| Dataset and rights | **PASS for included fixtures** | Included incident frames and labels are project-generated synthetic data; YuNet provenance is documented. No real facility imagery or real-world validation is included. Project-level source redistribution license remains unselected; see `LICENSES_AND_DATA_PROVENANCE.md`. |
| Team eligibility and registration | **BLOCKED** | Devpost registration is confirmed; the account's draft team page shows the project creator only, and the user reports entering solo. Age/legal-majority eligibility and required declarations have not been confirmed by the entrant. |
| Final Devpost submission | **BLOCKED** | A private draft exists but has not been submitted. Its required video field is blank, and the AWS endpoint is missing. The legal-rules checkbox and final Submit action were not used. |

## Deployment and cost record

- AWS resources created: **none**. The browser is at an AWS IAM sign-in screen; no authenticated account or credits could be checked. App Runner eligibility: **unverified**. Live URL: **none**.
- Prepared plan (conditional on App Runner availability): `us-east-1` illustrative estimate, one 0.5-vCPU/1-GB instance at about **$5.11/month idle**, plus about **$0.032 per processing hour**. Eight processing hours/day estimates about **$12.79/month** of App Runner compute/memory; continuous processing estimates about **$28.47/month**, before ECR, S3, logs, transfer, taxes, scale-out, or other usage. These are not guaranteed caps or verified account quotes. Budget alerts do not cap spend.
- The user authorized continuing the other release steps, but the actual AWS console session is not authenticated and no spend ceiling was specified. A secure AWS identity, service eligibility, chosen architecture/region, and explicit spend approval are required before resource creation.

## Exact links and remaining actions

- Repository: https://github.com/axfrgo/fortifiers-incident-memory
- Verified finalization release commit: `c0e95ec5bf01a789ce124ae4396574c48f341439`
- AWS endpoint: none
- Demo video: none
- Devpost: private draft saved in the signed-in account; not published. Draft preview URL: https://devpost.com/software/fortifiers-incident-memory (may require account access).
- Fresh local test result: 36/36 passing; current local API returned HTTP 200 for `/`, `/health`, and clear-change, poor-image, lighting-shift and historical-match scenarios. See `artifacts/finalization-api-smoke.json` (the endpoint is localhost only, not public/AWS).
- Outstanding user/team actions: complete secure AWS console sign-in in the open tab, authorize a specific spend ceiling after reviewing the chosen service/region estimate, and provide a permitted deployment identity if AWS deployment is desired. Record and host a real sub-five-minute demonstration and provide its YouTube/Vimeo URL. Confirm solo-entry eligibility and declarations. Add the video, verify the endpoint, review the final draft, then provide action-time approval before final submission.

Official competition links: [Devpost overview](https://opencv26.devpost.com/) and [rules](https://opencv26.devpost.com/rules). Do not infer award eligibility from this local verification package.
