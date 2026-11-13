# Sourced by install.sh and update.sh: sets COMPOSE to the right docker compose command for this VPS.
SUDO=""; docker info >/dev/null 2>&1 || SUDO="sudo"
set -a; . ./.env; set +a
SHARE=${SHARE_LLM:-auto}
if [ "$SHARE" = "auto" ]; then
  if $SUDO docker network inspect poultrybot_default >/dev/null 2>&1; then SHARE=yes; else SHARE=no; fi
fi
if [ "$SHARE" = "yes" ]; then
  COMPOSE="$SUDO docker compose -f docker-compose.yml -f deploy/compose.shared.yml"
  OLLAMA="$SUDO docker exec poultrybot-ollama-1"
else
  COMPOSE="$SUDO docker compose --profile llm"
  OLLAMA="$SUDO docker compose exec -T ollama"
fi
[ -n "${DOMAIN:-}" ] && COMPOSE="$COMPOSE --profile https"
