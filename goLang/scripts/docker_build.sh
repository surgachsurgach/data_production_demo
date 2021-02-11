#!/usr/bin/env bash
set -e

AWS_REGION=ap-northeast-2
AWS_ACCOUNT_ID=123455689101 # your aws_account_id
SERVICE="API" # $1
TAG="latest" # $2

if [ -z "${TAG}" ]; then
  echo "[ERROR] You should pass the tag number! (e.g. v1)"
  exit 1
fi

docker build --compress --rm --tag "${SERVICE}:${TAG}" --file ./build/DockerFile .

$(aws ecr get-login --no-include-email --region "${AWS_REGION}")

docker tag "${SERVICE}":"${TAG}" "${AWS_ACCOUNT_ID}".dkr.ecr.ap-northeast-2.amazonaws.com/"${SERVICE}":"${TAG}"
docker push "${AWS_ACCOUNT_ID}".dkr.ecr.ap-northeast-2.amazonaws.com/"${SERVICE}":"${TAG}"








