---
name: python-bot-deployment
description: "Use when deploying Python bots or troubleshooting APIs."
---

# Python Bot Deployment & API Troubleshooting

This skill covers common workflows and pitfalls when deploying Python-based Telegram bots, especially on resource-limited free/shared hosting (e.g., Alwaysdata), and general API troubleshooting for agent environments.

## 1. Deploying Python Telegram Bots

### 1.1. Resource-Limited Hosts (e.g., Alwaysdata)

**Problem**: `Disk quota exceeded` or `OSError: [Errno 122]` during `pip install`.
**Solution**: Clear old caches and install without caching:

```bash
rm -rf ~/.cache
rm -rf ~/.local/lib
pip install --no-cache-dir <package_name> # e.g., pyTelegramBotAPI yt-dlp
```

**Problem**: High RAM/CPU usage for video downloaders (e.g., YouTube videos).
**Solution**: Use direct download link generation instead of server-side download/transcoding. Libraries like `yt-dlp` can extract direct streaming links for various qualities and audio-only.

### 1.2. Managing Telegram Bot Tokens

**Problem**: Two bots respond to the same message, or intermittent failures.
**Solution**: A single Telegram bot token must only be active on one running instance at a time. Always create a *new, dedicated token* for each bot instance or deployment using `@BotFather` (`/newbot`).

## 2. API & Configuration Troubleshooting

### 2.1. `Invalid or disabled ClientApiKey` (401 Error on 9Router/AgentRouter)

**Problem**: API calls return `401 Unauthorized` or `Invalid/disabled ClientApiKey`.
**Cause**: The API key is incorrect, expired, revoked, or the associated account has run out of credit.
**Solution**:
1. Log in to the provider's dashboard (e.g., 9Router).
2. Navigate to the API Keys section.
3. Generate a *new API key*.
4. Update the corresponding `API_KEY` in the environment variable (`.env` file) or `config.yaml`.

### 2.2. `empty or malformed response (HTTP 200)` (Claude Code)

**Problem**: Claude Code (or similar Anthropic-compatible clients) returns `empty or malformed response (HTTP 200)`.
**Cause**:
1. **Typo in API Key**: Extra characters (e.g., `ssk-` instead of `sk-`).
2. **Incorrect Base URL**: Missing `/v1` endpoint or wrong domain for API gateway (e.g., `https://agentrouter.org` instead of `https://api.agentrouter.org/v1`).
3. **API Key format mismatch**: Key passed in an unexpected parameter (e.g., `apiKeyHelper` instead of `ANTHROPIC_API_KEY`).
4. **Invalid JSON syntax**: Missing curly braces or commas in `settings.json`.
**Solution**: Carefully verify `ANTHROPIC_API_KEY` and `ANTHROPIC_BASE_URL` in the client's `settings.json` or environment variables, ensuring correct format and values.

### 2.3. `hermes model` Configuration for Custom Providers

**Problem**: Custom models/combos from proxy services (e.g., 9Router) not recognized by `hermes model`.
**Cause**: Hermes defaults to standard model lists. Custom aliases need to be explicitly configured.
**Solution**: Ensure the `OPENAI_BASE_URL` in `.env` points to the proxy, and if specific custom names are desired, define them in `config.yaml` under `custom_providers`.

### 2.4. YAML Configuration Syntax Errors (`did not find expected '-' indicator`)

**Problem**: `config.yaml` fails to parse due to indentation or missing `-` characters.
**Cause**: YAML is sensitive to spacing (use spaces, not tabs) and list indicators (`-`).
**Solution**: Use `notepad <path_to_config.yaml>` to open and manually fix indentation and ensure list items start with a ` - `.

## 3. Integrating MCP Servers

**Problem**: Connecting new MCP servers like Parse.bot to Hermes.
**Solution**: Use `hermes config set` to add the MCP server details (URL, API Key header) to `mcp_servers` in `config.yaml`. Example:

```bash
hermes config set mcp_servers.parse.enabled true
hermes config set mcp_servers.parse.url "https://api.parse.bot/mcp"
hermes config set mcp_servers.parse.headers.X-API-Key "\${PARSE_BOT_API_KEY}" # Use environment variable
```

## 4. Backups for Persistent State

**Key Insight**: `config.yaml`, `skills/`, `memories/`, `sessions/`, `cron/` are included in the `hermes-daily-backup.sh` script. However, sensitive API keys (`.env` file) are explicitly excluded for security. When restoring, re-enter API keys in `.env`.
