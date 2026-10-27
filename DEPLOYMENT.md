# Deployment instructions and current status

## Current status: BLOCKED / prepared only

No AWS resources were created. The inspected workspace has no AWS CLI, Docker CLI, AWS environment credentials or `~/.aws` profiles. The owner selected preparation only and declined resource creation. There is no live endpoint, remote OpenCV execution or AWS verification. The app currently runs locally; this does not satisfy the competition's AWS component or public endpoint requirement.

## Prepared AWS architecture

- Build a Python 3.11 container with pinned `requirements-lock.txt`.
- Push to a private ECR repository with image scanning and AES-256 repository encryption.
- Use CloudFormation `deployment/stack.yaml` to create an internet-facing App Runner service that runs this FastAPI application and OpenCV 5 on CPU (0.5 vCPU/1 GB, one to two instances, five concurrent requests per instance).
- The CloudFormation template creates a private, versioned S3 evidence bucket with all public access blocked and SSE-S3, plus a least-privilege App Runner instance role scoped to `evidence/*` objects. Current versions expire after 30 days and noncurrent versions after seven days. The service sets `ALLOW_USER_UPLOADS=false` and exposes only synthetic scenarios. App Runner `/health` is the health check; service logs are available through CloudWatch.
- The deployment script applies `deployment/ecr-lifecycle-policy.json` to retain at most the newest three container images.
- App Runner publishes HTTPS suitable for judges. The API writes a ZIP bundle to S3 and returns an expiring presigned download URL.

## Cost and authorization boundary

App Runner, ECR and S3 may incur charges. The region and account are not configured, so no price is asserted. App Runner capacity and request concurrency are capped, ECR retains three images, S3 evidence has a retention lifecycle, and real-image uploads are disabled. Before deployment, an owner must select a region, inspect AWS Pricing Calculator estimates and current credit terms, provide authenticated AWS CLI access, and explicitly approve resource creation. The deployment script additionally requires `-ApprovedForBillableDeployment`. No approval was given for actual deployment, and no workaround was attempted.

## Prerequisites after authorization

1. Docker Engine, AWS CLI v2, PowerShell 7 or Windows PowerShell, Python 3.11+ and the pinned local tests must be available.
2. Use an authorized role permitted to create ECR repositories/images, CloudFormation stacks, IAM roles, App Runner services and S3 buckets, plus `sts:GetCallerIdentity`.
3. From this project directory, inspect and validate `deployment/stack.yaml`; review IAM actions, selected region, public HTTPS exposure, retention, service scaling and current price.
4. After explicit approval only, run:

```powershell
./deployment/deploy.ps1 -Region <approved-region> -ApprovedForBillableDeployment
```

5. The script builds/pushes the container, deploys the stack, checks the public `/health` response for OpenCV 5, runs `clear_change`, checks for the investigation trace and writes `deployment-manifest.json`. Review the AWS CloudFormation events and App Runner logs. A script error or local Docker build is not deployment evidence.
6. Preserve the returned live URL and sanitized manifest. Re-run the tests and an actual HTTP investigation. Add the URL to the Devpost entry and video only after the response is verified.

The deployment template/script have not been validated by AWS CloudFormation or Docker in this environment. Teardown is intentionally not automated; preserve evidence and ask the resource owner before deleting data or stacks.

