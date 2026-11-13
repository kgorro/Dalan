#!/usr/bin/env bash
# Pull the latest code and knowledge base, rebuild, and restart.
set -euo pipefail
cd "$(dirname "$0")/.."
git pull --ff-only
. deploy/compose-args.sh
$COMPOSE up -d --build
$SUDO docker image prune -f >/dev/null
