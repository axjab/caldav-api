#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"

cd "${PROJECT_ROOT}"

DEFAULT_IMAGE="ghcr.io/axjab/caldav-api"

# IMAGE can be supplied externally:
#   IMAGE=caldav-api ./srv/build.sh
if [[ -z "${IMAGE:-}" ]]; then
    read -r -p "Image [${DEFAULT_IMAGE}]: " INPUT_IMAGE
    IMAGE="${INPUT_IMAGE:-${DEFAULT_IMAGE}}"
fi

if [[ -z "${IMAGE}" ]]; then
    echo "ERROR: image cannot be empty." >&2
    exit 1
fi

echo
echo "Image: ${IMAGE}"

# VERSION can be supplied externally:
#   VERSION=1.2.3 ./srv/build.sh
if [[ -z "${VERSION:-}" ]]; then
    VERSION="$(git branch --show-current)"
    VERSION="${VERSION//\//-}"

    read -r -p "Version [${VERSION}]: " INPUT_VERSION
    VERSION="${INPUT_VERSION:-${VERSION}}"
fi

if [[ -z "${VERSION}" ]]; then
    echo "ERROR: version cannot be empty." >&2
    exit 1
fi

IMAGE_TAG="${IMAGE}:${VERSION}"

echo
echo "Image: ${IMAGE_TAG}"
echo

read -r -p "Build this image? [Y/n] " CONFIRM
CONFIRM="${CONFIRM:-Y}"

if [[ ! "${CONFIRM}" =~ ^[Yy]$ ]]; then
    echo "Build cancelled."
    exit 0
fi

sudo docker build \
    --build-arg "APP_VERSION=${VERSION}" \
    -t "${IMAGE_TAG}" \
    .

echo
echo "==================================="
echo " BUILD COMPLETE"
echo "==================================="
echo
echo "Image:"
echo "  ${IMAGE_TAG}"
echo

sudo docker image ls "${IMAGE}"
