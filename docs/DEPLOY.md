# Deploying Sugbo Guide on a VPS with Docker

Same setup as PoultryBot: the bot (FastAPI and the DALAN router) plus a local LLM through Ollama, with optional HTTPS through Caddy. Sugbo Guide listens on port 8001 so it can run next to PoultryBot on 8000.

## Install

SSH into the VPS and run:

    git clone https://github.com/kgorro/Dalan.git ~/sugboguide
    cd ~/sugboguide
    cp .env.example .env
    nano .env                      # LLM_MODEL, BOT_PORT, DOMAIN
    bash deploy/install.sh

install.sh installs Docker if needed, builds and starts the bot, makes sure the model is downloaded, and prints the URL and the /health check.

## Sharing PoultryBot's model

If PoultryBot is already running on the same VPS, Sugbo Guide uses PoultryBot's Ollama instead of starting a second copy of the model, which saves several GB of RAM. This happens automatically (SHARE_LLM=auto in .env). Set LLM_MODEL to the same model name PoultryBot uses. Set SHARE_LLM=no to give Sugbo Guide its own model.

If you later reinstall PoultryBot, run bash deploy/update.sh here so Sugbo Guide reconnects to its network.

## Open the port

    sudo ufw allow 8001/tcp

Also allow 8001 in your VPS provider's firewall if it has one. The bot is then at http://SERVER_IP:8001.

## HTTPS with a domain

Running Sugbo Guide alone: point a DNS A record to the VPS, set DOMAIN in .env, set BOT_PORT=127.0.0.1:8001, open ports 80 and 443, and run bash deploy/install.sh again.

If PoultryBot also has a domain on this VPS, only one Caddy can use ports 80 and 443. Leave DOMAIN empty here and add the Sugbo Guide domain to PoultryBot's Caddy instead.

## Everyday commands

    bash deploy/update.sh                          # pull new code or knowledge base, rebuild, restart
    docker compose logs -f sugboguide              # bot logs
    curl localhost:8001/health                     # is it up?
