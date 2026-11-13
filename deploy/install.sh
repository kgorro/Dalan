#!/usr/bin/env bash
# One-time Sugbo Guide setup on a fresh Ubuntu or Debian VPS. Run as a sudo user:
#   bash deploy/install.sh
set -euo pipefail
REPO_URL=${REPO_URL:-https://github.com/kgorro/Dalan.git}
DIR=${DIR:-$HOME/sugboguide}

if ! command -v docker >/dev/null; then
  echo "Installing Docker"
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker "$USER"
fi

if [ ! -f docker-compose.yml ] || ! grep -q sugboguide docker-compose.yml; then
  [ -d "$DIR/.git" ] || git clone "$REPO_URL" "$DIR"
  cd "$DIR"
fi
[ -f .env ] || cp .env.example .env
. deploy/compose-args.sh

if [ "$SHARE" = "yes" ]; then echo "Sharing PoultryBot's local model"; else echo "Running Sugbo Guide's own local model"; fi
$COMPOSE up -d --build

echo "Making sure the model ${LLM_MODEL:-qwen2.5:3b-instruct} is downloaded (a few GB, first run only)"
$OLLAMA ollama pull "${LLM_MODEL:-qwen2.5:3b-instruct}"

sleep 5
$COMPOSE exec -T sugboguide python -c "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"
if [ -n "${DOMAIN:-}" ]; then echo "Sugbo Guide: https://$DOMAIN"; else echo "Sugbo Guide: http://$(curl -fsS https://ifconfig.me || echo '<server-ip>'):${BOT_PORT:-8001}"; fi
