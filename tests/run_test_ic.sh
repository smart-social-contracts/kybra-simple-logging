#!/bin/bash
set -e
set -x

IMAGE_ADDRESS="ghcr.io/smart-social-contracts/icp-dev-env:latest"

echo "Running tests..."
docker run --rm \
    -v "${PWD}/src:/app/src" \
    -v "${PWD}/../kybra_simple_logging:/app/src/kybra_simple_logging" \
    -v "${PWD}/../setup.py:/app/setup.py" \
    -v "${PWD}/../README.md:/app/README.md" \
    -v "${PWD}/dfx.json:/app/dfx.json" \
    -v "${PWD}/entrypoint.sh:/app/entrypoint.sh" \
    --entrypoint "bash" \
    $IMAGE_ADDRESS \
    -c "cd /app && pip install -e . && /app/entrypoint.sh" || {
    echo "❌ Tests failed"
    exit 1
}

echo "✅ All tests passed successfully!"