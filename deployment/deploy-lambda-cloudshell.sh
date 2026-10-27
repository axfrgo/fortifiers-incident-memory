#!/usr/bin/env bash
set -euo pipefail

REGION="${AWS_REGION:-us-east-2}"
BOOTSTRAP_STACK="fortifiers-incident-memory-bootstrap"
APP_STACK="fortifiers-incident-memory-demo"
SOURCE_REPO="https://github.com/axfrgo/fortifiers-incident-memory.git"
REPO_NAME="fortifiers-incident-memory"

echo "Region: ${REGION}; account details are intentionally not printed."
aws sts get-caller-identity --query '{Authenticated:Account != `null`}' --output json

mkdir -p "$HOME/fortifiers-deploy"
cd "$HOME/fortifiers-deploy"
if [ ! -d fortifiers-incident-memory/.git ]; then
  git clone --depth 1 "$SOURCE_REPO" fortifiers-incident-memory
fi
cd fortifiers-incident-memory
git fetch --depth 1 origin master
git checkout --detach origin/master
COMMIT="$(git rev-parse HEAD)"
SHORT_COMMIT="$(printf '%s' "$COMMIT" | cut -c1-12)"
echo "Source commit: ${COMMIT}"

aws cloudformation deploy \
  --region "$REGION" \
  --stack-name "$BOOTSTRAP_STACK" \
  --template-file deployment/aws-bootstrap.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ImageRepositoryName="$REPO_NAME" SourceRepository="$SOURCE_REPO"

stack_value() {
  aws cloudformation describe-stacks --region "$REGION" --stack-name "$BOOTSTRAP_STACK" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue | [0]" --output text
}

BUILD_PROJECT="$(stack_value ContainerBuildProjectName)"

BUILD_ID="$(aws codebuild start-build --region "$REGION" --project-name "$BUILD_PROJECT" \
  --source-version "$COMMIT" --query 'build.id' --output text)"
echo "CodeBuild started. Build identifier: ${BUILD_ID}"
while true; do
  BUILD_STATUS="$(aws codebuild batch-get-builds --region "$REGION" --ids "$BUILD_ID" \
    --query 'builds[0].buildStatus' --output text)"
  echo "CodeBuild status: ${BUILD_STATUS}"
  case "$BUILD_STATUS" in
    SUCCEEDED) break ;;
    FAILED|FAULT|STOPPED|TIMED_OUT) echo "See CloudWatch group /aws/codebuild/fortifiers-incident-memory-lambda" >&2; exit 1 ;;
    *) sleep 15 ;;
  esac
done

aws ecr describe-images --region "$REGION" --repository-name "$REPO_NAME" \
  --image-ids imageTag="$SHORT_COMMIT" --query 'imageDetails[0].imageDigest' --output text

aws cloudformation deploy \
  --region "$REGION" \
  --stack-name "$APP_STACK" \
  --template-file deployment/aws-app.yaml \
  --parameter-overrides ImageTag="$SHORT_COMMIT" GitCommit="$COMMIT"

FUNCTION_URL="$(aws cloudformation describe-stacks --region "$REGION" --stack-name "$APP_STACK" \
  --query "Stacks[0].Outputs[?OutputKey=='FunctionUrl'].OutputValue | [0]" --output text)"
echo "PUBLIC_FUNCTION_URL=${FUNCTION_URL}"
echo "DEPLOYED_GIT_COMMIT=${COMMIT}"
echo "BUILD_ID=${BUILD_ID}"
curl --fail --silent --show-error "${FUNCTION_URL}health"
echo
