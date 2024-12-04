#!/bin/bash
# Use to build your changes into a docker image and tag properly for cdk deploy to aws.
set -e  # Exit immediately if a command exits with a non-zero status.
aws sso login
export AWS_REGION="ap-northeast-1"
export DOCKER_REPOSITORY="533267214762.dkr.ecr.${AWS_REGION}.amazonaws.com"

#Tag and push the basis bot image.
docker login -u AWS -p $(aws ecr get-login-password --region ${AWS_REGION}) ${DOCKER_REPOSITORY}
export DOCKER_TAG=$(git rev-parse HEAD)
docker tag webhooks-server "${DOCKER_REPOSITORY}/webhooks-server:${DOCKER_TAG}"
docker tag webhooks-server "${DOCKER_REPOSITORY}/webhooks-server:testing"
docker push "${DOCKER_REPOSITORY}/webhooks-server:${DOCKER_TAG}"
