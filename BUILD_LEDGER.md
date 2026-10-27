# Build Ledger

## 2026-10-27 00:04:13Z (2026-10-26 21:04:13 -03:00)

- Created isolated project directory: `C:\Users\Administrator\hackathon winners\fortifiers-incident-memory`. The workspace contained only `competition_tracker.md`; it was left untouched.
- Official Devpost page checked: displayed submission deadline is **October 26, 2026, 11:45 PM PDT**. Local Halifax time is October 27, 2026, 03:45 AM ADT. Earlier displayed deadline is the target.
- Workspace discovery: no existing Git repository; Python 3.14.0; Docker CLI unavailable; AWS CLI unavailable; `AWS_PROFILE` unset. A later presence-only check confirmed no AWS credential environment names or local profile files.
- Code skill read. OpenCV 5 and official competition rules research started.
- Initial discovery is complete. Current blockers and the remaining publication/deployment steps are recorded at the end of this ledger.

## Evidence and decisions

| Time (UTC) | Action / command | Result | Evidence / next step |
|---|---|---|---|
| 2026-10-27 00:04:13Z | `Get-ChildItem -Force`; `python --version`; `git status --short --branch`; `docker --version`; `aws --version`; `aws sts get-caller-identity` | Workspace has one unrelated tracker; no Git repo; Python 3.14.0; Docker and AWS commands not found; AWS identity could not be queried because CLI is absent. | No secrets printed. Probe SDK/env safely and prepare cloud deployment without claiming it. |
| 2026-10-27 00:04:13Z | Open official competition pages | Devpost deadline banner: Oct 26, 2026 @ 11:45pm PDT; OpenCV official overview confirms OpenCV 5 substantive vision plus meaningful AWS component and Agentic Vision requirement that image/video results affect a later action. | Exact eligibility, submission form requirements and rules to extract. |

## 2026-10-27 00:27:52Z — final implementation and verification update

| Time (UTC) | Action / command | Result | Evidence / next step |
|---|---|---|---|
| 2026-10-27 00:24:52Z | Fix compatibility issues exposed by a final test run | Five upload/redaction tests failed because OpenCV 5 lacks the OpenCV 4 `cv2.CascadeClassifier` call. Replaced it with OpenCV 5 `FaceDetectorYN` and YuNet model, fail-closed error handling and a 17 MiB request cap. | Model source/license and SHA in `LICENSES_AND_DATA_PROVENANCE.md`; user upload remains disabled in prepared AWS configuration. |
| 2026-10-27 00:25:04Z | `.venv\Scripts\python.exe -m pytest -q --junitxml=artifacts/test-results.xml` | **36 passed, 0 failed, 0 skipped**; one Starlette/AnyIO deprecation warning. | Raw test report `artifacts/test-results.xml`; summarized environment and case list `artifacts/test-results.json` (generated 00:27:14Z). No Docker/AWS service tests claimed. |
| 2026-10-27 00:25:35Z | `.venv\Scripts\python.exe scripts/build_dataset.py`; `.venv\Scripts\python.exe scripts/evaluate.py` | Rebuilt 14 fixed-seed synthetic fixture sets. Evaluation ran 21 controller cases: expected action 7/7; one-pass 4/7; pixel precision/recall/F1/IoU 0.99183/0.99913/0.99546/0.99097; p50/p95 158.477/246.465 ms. | `artifacts/evaluation.json`, `artifacts/evaluation-cases.csv`, `artifacts/task-correctness.svg`. Synthetic-only; this does not estimate field performance. |
| 2026-10-27 00:26:00Z | `.venv\Scripts\python.exe scripts/export_demo_cases.py` | Exported seven real API/vision runs and materially different outcomes/traces for clear change, retake, benign change, historical match and related cases. | `artifacts/demo-cases.json` and each `artifacts/demo/<run-id>/` contains PNGs, JSON/HTML report and evidence ZIP. |
| 2026-10-27 00:26:00Z | Correct demo exporter after its first run raised `KeyError: 'tool'`; rerun `.venv\Scripts\python.exe scripts/export_demo_cases.py` | Updated exporter to serialize the actual trace keys; exported all seven cases successfully. | `artifacts/demo-cases.json` and each `artifacts/demo/<run-id>/` contains PNGs, JSON/HTML report and evidence ZIP. |
| 2026-10-27 00:26:21Z | Start local Uvicorn and request `/`, `/health`, `/api/investigate/historical_match`, and its evidence ZIP over `127.0.0.1:8000` | App returned HTTP 200; runtime reported OpenCV 5.0.0; historical scenario returned `no_new_change_supported` after 10 action calls; downloadable local ZIP returned HTTP 200 (928,551 bytes). Root returned HTTP 200 after correcting a PowerShell variable-name collision in the check command. | Local service is available at `http://127.0.0.1:8000` while its process remains running. This is not a public/judge endpoint. |
| 2026-10-27 00:27:52Z | Final AWS environment check: inspect presence only for AWS environment-variable names; test `$USERPROFILE/.aws/credentials` and `config`; check `Get-Command docker` and `Get-Command aws` | No AWS credential environment names, AWS credentials/config files, Docker CLI or AWS CLI found. No secret values printed. User explicitly chose “Prepare the deployment only; do not create AWS resources.” | `deployment-manifest.json` stays `BLOCKED`; no account ID, service URL, image or costs. `deployment/deploy.ps1` requires an explicit billable-deployment switch. |

### Remaining blockers / exact next steps

- Do not create AWS resources: this is the user's explicit choice. A later authorized owner must supply a configured AWS identity and Docker, opt in to billing, run `deployment/deploy.ps1`, and inspect the deployed manifest and live health/investigation result.
- No public or private judge-accessible repository/archive link was created; no project/team roster or actual member identity was supplied. The portable source archive is being prepared locally, not published.
- No screen recording or hosting capability was used. Follow `DEMO_SCRIPT.md` with a real team member, record the running app, keep the video under five minutes and host it with judge access.
- Before a submission, the owner must confirm team eligibility/identity and add the actual AWS endpoint, repository/archive URL and video URL to `SUBMISSION.md` and Devpost. Do not claim the current package satisfies mandatory AWS/public demonstration requirements.
