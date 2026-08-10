User works on a Windows environment using PowerShell for local CLI tools.
§
Cron prompt validator blocks invisible Unicode (U+200C ZWNJ) common in Persian/Arabic/Urdu text. Workaround: write cron prompts in English, instruct agent to output in target language. See cron-orchestration skill.
§
Agent Reach at /data/workspace/Agent-Reach (pip install -e). Zero-config: GitHub, YouTube, V2EX, RSS, Jina Reader, Bilibili. Twitter/Reddit/XHS/FB/IG need cookies. `agent-reach doctor`.
§
Tech digest cron job 6e3a37165521 delivers a Persian tech-news post daily at 09:00 Tehran (30 5 * * * UTC). Repeat-protection log lives at /data/workspace/tech-channel-history.txt. Workflow details in telegram-content skill, references/tech-news-curation.md.
§
Host: /opt/venv (in PATH), /opt/hermes-agent; `hermes` not on PATH (export PATH=/opt/venv/bin:$PATH). /data ~434MB fills up (npm ENOSPC); clear .cache. mcp==1.29.0 pinned (2.0 breaks HTTP). Exa.ai configured with API key + agent_run. Cron jobs use openai-api + opencode via 9router.
§
User runs Persian Telegram channels: @abasmanesh222 (motivational/inspirational based on Seyed Hossein Abbasmanesh teachings) and @GoldPackFree2. Bot: @GoldPackFree_PosterBot, chat_id: -1001378242402. Post script: /data/workspace/post_to_channel.py. Cron posts: no header/footer, use Bot API directly. Style: no markdown headers, minimal bold, natural Persian tone. User has audio files from Abbasmanesh to post daily (one per day). Workflow: user sends audio → agent writes caption + generates cover → user posts manually. Always preview text before generating images.
§
User prefers quick direct answers, gets frustrated by slow responses. Wants practical content for general Persian audience. No excessive research rounds.
§
Premium image gen: /data/workspace/premium_generator.py, output: /data/workspace/posts_premium/. Palettes: luxury_gold, royal_purple, emerald_night. Vazirmatn font in /data/workspace/fonts/. Telegram format: short text on image + secondary text in caption. User is on Windows (PowerShell). API proxy: AgentRouter (agentrouter.org), default model set to geminiM.