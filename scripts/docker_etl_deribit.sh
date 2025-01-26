#!/bin/bash

cd ..
IMAGE_NAME=deribit_etl
VERSION=$(grep -m1 -P -o "(?<=version\s=\s\")[0-9]+?\.[0-9]+?\.[0-9]+?(?=\")" ./pyproject.toml)
if docker images | grep -Eo "${IMAGE_NAME}\slatest"
then
    docker image remove ${IMAGE_NAME}:latest
fi
if docker images | grep -Eo "${IMAGE_NAME}\s${VERSION}"
then
    docker image remove ${IMAGE_NAME}:${VERSION}
fi
docker build --platform=linux/amd64 --target etl_deribit -t ${IMAGE_NAME}:${VERSION} -t ${IMAGE_NAME}:latest  .
