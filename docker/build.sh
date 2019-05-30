#!/usr/bin/env bash
# build.sh - Script for building docker images

set -eux

PROJECT_ID=mcas-195423
BRANCH=master
IMAGE_TYPE=${1:-trackml} # trackml or kfp_kubectl
IMAGE_VERSION=${2:-1}

docker build \
  -t gcr.io/${PROJECT_ID}/trackml_${BRANCH}_${IMAGE_TYPE}:latest \
  -t gcr.io/${PROJECT_ID}/trackml_${BRANCH}_${IMAGE_TYPE}:${IMAGE_VERSION} \
  -f docker/Dockerfile_${IMAGE_TYPE} .

docker push gcr.io/${PROJECT_ID}/trackml_${BRANCH}_${IMAGE_TYPE}:${IMAGE_VERSION}
docker push gcr.io/${PROJECT_ID}/trackml_${BRANCH}_${IMAGE_TYPE}:latest

