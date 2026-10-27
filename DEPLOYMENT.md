# Deployment instructions and current status

## Current status: BLOCKED / prepared only

No AWS resources were created. The workspace has no AWS CLI, Docker CLI, AWS environment credentials or `~/.aws` profiles. The open AWS browser tab remains in the account-signup flow rather than an authenticated console. No credits, billing state, spend ceiling or account-specific App Runner eligibility are confirmed. There is no live endpoint, remote OpenCV execution or AWS verification. The app currently runs locally; this does not satisfy the competition's AWS component or public endpoint requirement.

**Service availability caveat:** current AWS documentation says App Runner is closed to new customers; existing customers may continue using it. This AWS account's eligibility is unknown because no AWS identity is configured. The template below is usable only if that account can create App Runner services. AWS recommends ECS Express Mode for new customers, but that architecture has not been built or costed for this project. Do not assume the prepared App Runner template can be deployed in a new AWS account. [AWS availability notice](https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html)

## Prepared AWS architecture

- Build a Python 3.11 container with pinned `requirements-lock.txt`.
- Push to a private ECR repository with image scanning and AES-256 repository encryption.
- Use CloudFormation `deployment/stack.yaml` to create an internet-facing App Runner service that runs this FastAPI application and OpenCV 5 on CPU (0.5 vCPU/1 GB, one to two instances, five concurrent requests per instance).
- The CloudFormation template creates a private, versioned S3 evidence bucket with all public access blocked and SSE-S3, plus a least-privilege App Runner instance role scoped to `evidence/*` objects. Current versions expire after 30 days and noncurrent versions after seven days. The service sets `ALLOW_USER_UPLOADS=false` and exposes only synthetic scenarios. App Runner `/health` is the health check; service logs are available through CloudWatch.
- The deployment script applies `deployment/ecr-lifecycle-policy.json` to retain at most the newest three container images.
- App Runner publishes HTTPS suitable for judges. The API writes a ZIP bundle to S3 and returns an expiring presigned download URL.

## Cost and authorization boundary

Illustrative estimate **if App Runner is available to the account**, in **US East (N. Virginia), `us-east-1`**, using the template's one 0.5 vCPU / 1 GB minimum instance for 730 hours/month: provisioned memory is about **$5.11/month** at $0.007/GB-hour. Active CPU adds about **$0.032 per processing hour** at $0.064/vCPU-hour, so 8 processing hours/day adds about $7.68/month; continuous processing for 730 hours would add about $23.36/month, for roughly $28.47 total compute and provisioned memory. This estimate excludes ECR storage, S3 storage/requests, CloudWatch logs, data transfer, taxes and any second active instance; actual usage can be higher. See [AWS App Runner pricing](https://aws.amazon.com/apprunner/pricing/). The template caps scaling at two active instances but this is not a hard monthly spend limit.

No AWS account balance, Free Tier credit, competition grant, region setting or billing history could be checked. The competition page describes up to $100 in credits for eligible new AWS customers, but this account's eligibility and balance are unverified. App Runner capacity and request concurrency are capped, ECR retains three images, S3 evidence has a retention lifecycle, and real-image uploads are disabled. Before any deployment, the owner must verify account/service eligibility, select the architecture and region, review current estimates/credits, provide secure authenticated AWS access, and explicitly authorize billable resource creation with a spend ceiling. The script additionally requires `-ApprovedForBillableDeployment`. No resources were created.

## Prerequisites after authorization

1. Docker Engine, AWS CLI v2, PowerShell 7 or Windows PowerShell, Python 3.11+ and the pinned local tests must be available.
2. Use an authorized role permitted to create ECR repositories/images, CloudFormation stacks, IAM roles, App Runner services and S3 buckets, plus `sts:GetCallerIdentity`. Verify App Runner access in the account first; if it is a new AWS customer account, stop and select a supported alternative such as ECS Express Mode before proceeding.
3. From this project directory, inspect and validate `deployment/stack.yaml`; review IAM actions, selected region, public HTTPS exposure, retention, service scaling and current price.
4. After explicit approval only, run:

```powershell
./deployment/deploy.ps1 -Region <approved-region> -ApprovedForBillableDeployment
```

5. The script builds/pushes the container, deploys the stack, checks the public `/health` response for OpenCV 5, runs `clear_change`, checks for the investigation trace and writes `deployment-manifest.json`. Review the AWS CloudFormation events and App Runner logs. A script error or local Docker build is not deployment evidence.
6. Preserve the returned live URL and sanitized manifest. Re-run the tests and an actual HTTP investigation. Add the URL to the Devpost entry and video only after the response is verified.

The deployment template/script have not been validated by AWS CloudFormation or Docker in this environment. The template still requires review against account-specific App Runner availability. Teardown is intentionally not automated; preserve evidence and ask the resource owner before deleting data or stacks.

