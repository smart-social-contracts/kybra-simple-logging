#!/bin/bash
set -e
set -x

IMAGE_ADDRESS="ghcr.io/smart-social-contracts/icp-dev-env:latest"

echo "Running tests..."
docker run --rm \
    -v "${PWD}/src:/app/src" \
    -v "${PWD}/dfx.json:/app/dfx.json" \
    -v "${PWD}/entrypoint.sh:/app/entrypoint.sh" \
    -v "${PWD}/..:/app/kybra-simple-logging-source" \
    -v "${PWD}/example:/app/example" \
    --entrypoint "bash" \
    $IMAGE_ADDRESS \
    -c "cd /app && ./entrypoint.sh" || {
    echo "❌ Tests failed"
    exit 1
}

echo "✅ All tests passed successfully!"