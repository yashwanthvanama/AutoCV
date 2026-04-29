#!/usr/bin/env bash
set -euo pipefail

IMAGE="claude-code-sandbox"
DOCKERFILE="Dockerfile.claude"

cd "$(dirname "$0")"

if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Image '$IMAGE' not found — building from $DOCKERFILE..."
  docker build -f "$DOCKERFILE" -t "$IMAGE" .
fi

exec docker run -it --rm \
  -v "$PWD":/workspace \
  -v "$HOME/.claude":/home/node/.claude \
  -v "$HOME/.claude.json":/home/node/.claude.json \
  "$IMAGE" "$@"
