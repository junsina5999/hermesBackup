User works on a Windows environment using PowerShell for local CLI tools.
§
Cron prompt validator blocks invisible Unicode (U+200C ZWNJ) common in Persian/Arabic/Urdu text. Workaround: write cron prompts in English, instruct agent to output in target language. See cron-orchestration skill.
§
Agent Reach at /data/workspace/Agent-Reach (pip install -e). Zero-config: GitHub, YouTube, V2EX, RSS, Jina Reader, Bilibili. Twitter/Reddit/XHS/FB/IG need cookies. `agent-reach doctor`.
§
Tech digest cron job 6e3a37165521 delivers a Persian tech-news post daily at 09:00 Tehran (30 5 * * * UTC). Repeat-protection log lives at /data/workspace/tech-channel-history.txt. Workflow details in telegram-content skill, references/tech-news-curation.md.
§
Host: Hermes venv /opt/venv, source /opt/hermes-agent; `hermes` not on PATH (export PATH=/opt/venv/bin:$PATH). /data small (~434MB); clear /data/.cache for ~290MB. User API proxy: 9router (OPENAI_BASE_URL in .env); cron jobs use openai-api + opencode.
§
User runs Persian Telegram channels: @abasmanesh222 and @GoldPackFree2. Bot: @GoldPackFree_PosterBot, chat_id: -1001378242402. Post script: /data/workspace/post_to_channel.py.
§
User prefers Hermes cron posts WITHOUT header/footer — cron.wrap_response=false, use Bot API directly via post_to_channel.py.
§
Content: motivational posts (emoji+quote+name OR emoji+short_text+name), tech digest 9am (GitHub tools, free AI tools, free AI APIs, Windows/Android apps, phone launches). Style: no markdown headers, minimal bold, natural tone.
§
User prefers quick direct answers, gets frustrated by slow responses. Wants practical content for general Persian audience. No excessive research rounds.