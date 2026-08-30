
#!/usr/bin/env bash
set -euo pipefail

IMAGE="ghcr.io/axjab/caldav-api"

# VERSION can be supplied externally:
#   VERSION=1.2.3 ./srv/push.sh
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

echo "Image: ${IMAGE_TAG}"
echo

read -r -p "Push this image? [Y/n] " CONFIRM
CONFIRM="${CONFIRM:-Y}"

if [[ ! "${CONFIRM}" =~ ^[Yy]$ ]]; then
    echo "Push cancelled."
    exit 0
fi

echo
echo "Pushing image..."
sudo docker push "${IMAGE_TAG}"

echo
echo "==================================="
echo " PUSH COMPLETE"
echo "==================================="
echo
echo "Image:"
echo "  ${IMAGE_TAG}"
echo
