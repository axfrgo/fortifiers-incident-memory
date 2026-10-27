# AWS deployment — live verification

## Current service

The OpenCV investigation API is deployed on AWS Lambda in us-east-2 and is publicly reachable at:

https://bxdbra2nzvrrchyig26xr274dm0cvzol.lambda-url.us-east-2.on.aws/

Open the root URL for the dashboard. The health endpoint is /health. AWS runs the actual Python API and OpenCV image-processing workload; the static demo is not hosted by S3 alone.

- Runtime: AWS Lambda Python 3.14 ZIP package, FastAPI through Mangum.
- OpenCV runtime: 5.0.0.
- Deployed source commit: b851290df9e99aca1a232c018e53bff48b8f559d.
- CloudFormation app stack: fortifiers-incident-memory-demo-free-3 (UPDATE_COMPLETE at 2026-10-27 05:17 UTC check).
- Bootstrap stack: fortifiers-incident-memory-bootstrap (CREATE_COMPLETE).
- Package: S3-hosted immutable ZIP, 101,602,882 compressed bytes; SHA-256 b06b10e6b86d85448d2fd931494908ce9884cf32b2ffd66e0bfd72be7bf17597.
- Lambda settings: 512 MiB memory, 90-second timeout, 512 MiB temporary storage, no reserved concurrency.
- Function URL access: public, unauthenticated (AuthType NONE). The endpoint is intended only for synthetic competition scenarios.
- User image uploads: disabled; upload route returns 403.
- Evidence: private S3 bucket, SSE-S3, seven-day lifecycle, time-limited presigned downloads.
- Logs: CloudWatch log group with 14-day retention.
- CloudWatch observed one cold-started invocation at 2,477 ms billed (2,205.78 ms init, 145 MiB max used) and a later investigation invocation at 2,923 ms billed (218 MiB max used). These are individual observations, not a latency distribution.
- Cost: account is on the AWS Free Plan. Credits and usage are not a hard spending cap. Current project spend after deployment has not been independently reconciled in Billing; do not claim zero cost.

The public API exposes seven fixed synthetic scenarios. It does not accept arbitrary images, control machinery, disable alarms, open doors, or dispatch responders. Do not send confidential or personal data to this unauthenticated endpoint.

## Remote verification evidence

Anonymous requests were run against the public endpoint after deployment:

- GET / and GET /health returned HTTP 200. Health reports OpenCV 5.0.0, deployment_mode aws-lambda, commit b851290df9e99aca1a232c018e53bff48b8f559d, S3 evidence enabled, and uploads disabled.
- All seven listed scenarios returned HTTP 200 with distinct outputs: dry_normal → no_visual_change_supported; clear_change → human_review_required; poor_image → retake_requested; lighting_shift → no_visual_change_supported; historical_match → no_new_change_supported; camera_movement → no_visual_change_supported; occlusion_blur → retake_requested.
- An unknown scenario returned 404. Upload endpoint returned 403 with user uploads disabled. Static JavaScript returned 200.
- A synthetic clear-change case produced a nine-step trace, a human-review-required result, and an evidence package. Its ZIP was downloaded without AWS credentials: 900,871 bytes, SHA-256 cb70a2d09ae03d04aba9ff639aff56c6a7087a91bb5e6214b56a6abb0c49f2b2. The bundle contains JSON/HTML reports, baseline/event frames, overlay and change mask, and passes ZIP integrity validation.
- The results are synthetic scenario checks. They do not establish field accuracy or physical leak detection.

Machine-readable evidence: artifacts/aws-remote-results.json, artifacts/aws-verification/verification.json, artifacts/aws-verification/clear-change-evidence.zip, and artifacts/lambda-package-build-manifest.json. The sanitized verification excludes AWS account identifiers and signed URLs. CloudWatch logs are visible in the signed-in AWS console under /aws/lambda/fortifiers-incident-memory-demo. A sample report showed 512 MiB configured memory and 218 MiB maximum used.

The package builder is deployment/package_lambda_zip.py. The Lambda template is deployment/aws-app-zip.yaml. CodeBuild and ECR were provisioned as a possible image path, but AWS denied CodeBuild starts because the account queue quota is zero. The verified workload instead uses the reproducible ZIP Lambda package. Earlier failed CloudFormation app attempts are retained as rollback history; the current stack is UPDATE_COMPLETE.

## Rebuild and redeploy

This deployment was prepared from Windows using the pinned lock and Linux-compatible wheels, then uploaded through the authenticated AWS console. For a repeat build, use Python and pip versions documented by the builder and run:

    .venv\Scripts\python.exe scripts\package_lambda_zip.py

The generated package includes a manifest with the source commit, runtime, dependency pins and checksum. Upload that ZIP to the project bootstrap bucket, set the app stack's PackageBucket and PackageKey parameters, and update stack fortifiers-incident-memory-demo-free-3 from deployment/aws-app-zip.yaml. Keep Python 3.14, 512 MiB memory, uploads disabled and S3 private. Then verify /health and at least clear_change, poor_image and historical_match with an unauthenticated client. The current deployed build is b851290df9e99aca1a232c018e53bff48b8f559d.

A current-stack update must be followed by a real remote investigation and CloudWatch inspection. A successful template deployment or health endpoint alone is not sufficient evidence.

## Cost and teardown

Lambda is billed per request and execution duration; S3 storage/requests, CloudWatch ingestion/retention and data transfer may also incur charges. The Free Plan credit may offset eligible charges but does not cap all service usage, and billing data can lag. Public access can be invoked by third parties; rate and traffic are not capped by the application. Monitor the Billing dashboard and disable the public Function URL after judging if continued access is not needed.

To stop new public invocations, remove the Function URL permission/configuration using the stack template or update the app stack to disable the URL. After the judging period, delete only fortifiers-incident-memory-demo-free-3. The bootstrap stack retains the private bucket and ECR repository on stack deletion to protect evidence. To remove all project resources, inspect and empty the named private bucket, delete only the project ECR repository, then delete fortifiers-incident-memory-bootstrap. Review resource names and region carefully; do not delete unrelated resources.
