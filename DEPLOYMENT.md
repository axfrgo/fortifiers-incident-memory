# AWS deployment

## Current deployment state

No project AWS resources have been created or billed yet. The authenticated account has an active Free Plan credit, but this document intentionally omits account identifiers and balances. Do not upgrade the account to a Paid Plan. The AWS CloudShell console currently reports that account verification is still in progress, so its CLI environment is unavailable; console-based deployment is being checked before declaring the endpoint blocked.

The deployment target is AWS Lambda because AWS App Runner no longer accepts new customers. `deployment/aws-bootstrap.yaml` defines a private ECR repository, a short-lived private S3 evidence bucket, a least-privilege Lambda role, and a one-off CodeBuild project. `deployment/aws-app.yaml` defines the actual public FastAPI/OpenCV Lambda and its Function URL. The OpenCV workload itself runs in the Lambda container; S3-only hosting is not used as a substitute for AWS processing.

## Architecture and safeguards

- Python 3.14 Lambda container uses the existing pinned `requirements-lock.txt`, OpenCV 5.0.0.93 and `mangum==0.22.0`. The Docker build fails unless OpenCV imports and reports major version 5.
- CodeBuild builds the published Git commit and pushes an immutable commit-tagged image to private ECR. The Docker platform is `linux/amd64`.
- Lambda has 2 GiB memory, a 90-second timeout, 1 GiB `/tmp` storage, and reserved concurrency of one. It runs on demand; it has no always-on instance charge.
- The public HTTPS Lambda Function URL serves the dashboard and synthetic investigation API. Only seven built-in synthetic scenarios are enabled in AWS; image uploads are disabled. No machinery, alarms, doors, or emergency-response controls exist.
- S3 blocks all public access, uses SSE-S3 encryption, and expires evidence under `evidence/` after seven days. The execution role can read and write only that prefix. The returned evidence URL is a one-hour presigned URL.
- Lambda logs are retained for 14 days; CodeBuild logs for seven days. Build and runtime identifiers appear at `/health`.
- The function is publicly callable, so any visitor can run the finite synthetic scenarios. Reserved concurrency limits simultaneous execution, not total request count. Monitor Free Plan credits and disable the function URL or delete the stack after judging. Credits and Free Plan eligibility are not a hard spending cap; no Paid Plan upgrade is authorized.

## Cost estimate

This is an estimate, not a spending limit. AWS's published Lambda rate is $0.0000166667 per GB-second plus $0.20 per million requests. At 2 GiB and a three-second invocation, compute is about $0.0001 per call; a 90-second invocation would be about $0.003. AWS CodeBuild publishes 100 monthly general1.small build minutes in its Free Tier; beyond that, the listed example rate is $0.005/minute, so a 20-minute build would be about $0.10. ECR, S3, CloudWatch, and data transfer depend on actual image size, retained evidence, log volume, and traffic. A small, low-traffic demo is expected to consume only a small amount of the account's existing credits, but public traffic can increase usage. Verify the billing page after deployment; its usage data may lag.

Sources: [Lambda pricing](https://aws.amazon.com/lambda/pricing/), [CodeBuild pricing](https://aws.amazon.com/codebuild/pricing/), [ECR pricing](https://aws.amazon.com/ecr/pricing/), [Lambda container images](https://docs.aws.amazon.com/lambda/latest/dg/python-image.html), and [Function URL access](https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html).

## Deployment procedure

Run from AWS CloudShell in `us-east-2` after account verification is complete and the public repository contains the final tested commit:

```bash
git clone https://github.com/axfrgo/fortifiers-incident-memory.git
cd fortifiers-incident-memory
bash deployment/deploy-lambda-cloudshell.sh
```

The script validates its identity without printing the account number, deploys the bootstrap stack, starts CodeBuild from the exact Git commit, deploys the Lambda stack from the immutable ECR image, and prints the HTTPS URL. It fails on a failed build or stack operation. Do not report a deployment from a local Docker result or an AWS health check alone.

## Remote acceptance checks

From a fresh unauthenticated browser session, verify the homepage and `/health`; confirm OpenCV 5, the build ID, commit hash, `deployment_mode=aws-lambda`, S3 enabled, and uploads disabled. Then run `clear_change`, `poor_image`, and `historical_match` or `lighting_shift`; inspect their different traces and findings; download the presigned ZIP; check a review action; confirm an upload returns 403; and check CloudWatch logs for the real invocation. Save sanitized responses in `artifacts/aws-remote-verification.json` and update `deployment-manifest.json` with the URL, commit, build, stack names, and measured usage. Never place AWS credentials, account IDs, or signed presigned URLs in public files.

## Teardown

After judging, disable public invocation first if the endpoint is no longer needed, then delete the app stack. The bootstrap template retains the private S3 bucket and ECR repository on stack deletion to prevent accidental evidence loss. To remove all resources, empty the named bucket, delete the repository images/repository, then delete the bootstrap stack. Review the resource names and region before running cleanup commands; CloudWatch groups, build project, and IAM roles are scoped to this project. Do not delete unrelated resources.
