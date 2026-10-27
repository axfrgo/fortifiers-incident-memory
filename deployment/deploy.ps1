param(
  [Parameter(Mandatory=$true)][string]$Region,
  [string]$StackName = 'fortifiers-incident-memory',
  [string]$RepositoryName = 'fortifiers-incident-memory',
  [switch]$ApprovedForBillableDeployment
)
$ErrorActionPreference = 'Stop'
if (-not $ApprovedForBillableDeployment) {
  throw 'This script can create billable AWS resources. Obtain explicit owner authorization, then pass -ApprovedForBillableDeployment.'
}
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker CLI is required to build and push the OpenCV image.' }
if (-not (Get-Command aws -ErrorAction SilentlyContinue)) { throw 'AWS CLI is required; install/configure it with an authorized least-privilege role.' }
$account = aws sts get-caller-identity --query Account --output text --region $Region
if ($LASTEXITCODE -ne 0 -or -not $account) { throw 'AWS caller identity could not be verified.' }
$repo = aws ecr describe-repositories --repository-names $RepositoryName --query 'repositories[0].repositoryUri' --output text --region $Region 2>$null
if ($LASTEXITCODE -ne 0 -or -not $repo) {
  $repo = aws ecr create-repository --repository-name $RepositoryName --image-scanning-configuration scanOnPush=true --encryption-configuration encryptionType=AES256 --query 'repository.repositoryUri' --output text --region $Region
  if ($LASTEXITCODE -ne 0) { throw 'Could not create the private ECR repository.' }
}
$tag = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ')
$image = "${repo}:${tag}"
$policyPath = (Resolve-Path (Join-Path $PSScriptRoot 'ecr-lifecycle-policy.json')).Path -replace '\\','/'
aws ecr put-lifecycle-policy --repository-name $RepositoryName --lifecycle-policy-text "file://$policyPath" --region $Region | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Could not apply the ECR image-retention rule.' }
$registry = ($repo -split '/')[0]
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $registry
if ($LASTEXITCODE -ne 0) { throw 'ECR login failed.' }
docker build --pull -t $image -f Dockerfile .
if ($LASTEXITCODE -ne 0) { throw 'Docker image build failed.' }
docker push $image
if ($LASTEXITCODE -ne 0) { throw 'Docker image push failed.' }
aws cloudformation deploy --stack-name $StackName --template-file deployment/stack.yaml --parameter-overrides "ImageIdentifier=$image" "ServiceName=$RepositoryName" --capabilities CAPABILITY_IAM --region $Region
if ($LASTEXITCODE -ne 0) { throw 'CloudFormation deployment failed; inspect stack events before retrying.' }
aws cloudformation wait stack-create-complete --stack-name $StackName --region $Region 2>$null
if ($LASTEXITCODE -ne 0) { aws cloudformation wait stack-update-complete --stack-name $StackName --region $Region }
if ($LASTEXITCODE -ne 0) { throw 'CloudFormation did not reach a complete stack state.' }
$url = aws cloudformation describe-stacks --stack-name $StackName --query "Stacks[0].Outputs[?OutputKey=='ServiceUrl'].OutputValue | [0]" --output text --region $Region
$health = Invoke-RestMethod -Uri "$url/health" -Method Get -TimeoutSec 30
if (-not $health.opencv5) { throw "Live service health check did not report OpenCV 5 ($($health.opencv_version))." }
$case = Invoke-RestMethod -Uri "$url/api/investigate/clear_change" -Method Get -TimeoutSec 120
if ($case.outcome -ne 'human_review_required' -or -not $case.trace) { throw 'Live investigation did not return expected evidence and trace.' }
$manifest = [ordered]@{status='DEPLOYED_AND_VERIFIED';verified_at_utc=[DateTime]::UtcNow.ToString('o');region=$Region;aws_account_id=$account;service_url=$url;opencv_version=$health.opencv_version;scenario=$case.scenario;outcome=$case.outcome;trace_calls=$case.trace.Count;deployment_image=$image;evidence_bucket=$case.cloud_evidence.bucket;local_credentials_or_tokens='not recorded'}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath 'deployment-manifest.json' -Encoding utf8
Write-Output "Verified OpenCV 5 endpoint: $url"
Write-Output 'Deployment manifest written to deployment-manifest.json'
