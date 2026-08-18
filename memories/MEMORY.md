User works on a Windows environment using PowerShell for local CLI tools.
§
Cron prompt validator blocks invisible Unicode (U+200C ZWNJ) common in Persian/Arabic/Urdu text. Workaround: write cron prompts in English, instruct agent to output in target language. See cron-orchestration skill.
§
Agent Reach at /data/workspace/Agent-Reach (pip install -e). Zero-config: GitHub, YouTube, V2EX, RSS, Jina Reader, Bilibili. Twitter/Reddit/XHS/FB/IG need cookies. `agent-reach doctor`.
§
Host: /opt/venv (in PATH), /opt/hermes-agent; `hermes` not on PATH (export PATH=/opt/venv/bin:$PATH). /data ~434MB fills up (npm ENOSPC); clear .cache. mcp==1.29.0 pinned (2.0 breaks HTTP). Exa.ai configured with API key + agent_run. Cron jobs use openai-api + opencode via 9router.
§
User prefers quick direct answers, gets frustrated by slow responses. Wants practical content for general Persian audience. No excessive research rounds.
§
Premium image gen: /data/workspace/premium_generator.py, output: /data/workspace/posts_premium/. Palettes: luxury_gold, royal_purple, emerald_night. Vazirmatn font in /data/workspace/fonts/. Telegram format: short text on image + secondary text in caption. User is on Windows (PowerShell). API proxy: AgentRouter (agentrouter.org), default model set to geminiM.
§
User runs Persian Telegram channel @GoldPackFree2. Bot: @GoldPackFree_PosterBot (-1001378242402). 3 scheduled channel posts per day (morning AI news, afternoon free AI APIs/tools, evening hidden-gem photo/video apps), plus a morning motivational quote. Style: punchy hook + 1 sentence intro + 4 emoji bullets + conclusion + handle + direct URL. Every line must start with a Persian word (no leading English or raw URLs at the start of lines). Model: geminiM on openai-api (9router) with opencode fallback on openai-api.
§
Parse.bot MCP server configured with API key. Multiai2 provider on 9Router is active for combo models.