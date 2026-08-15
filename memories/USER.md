Iranian admin of @GoldPackFree2 (tech/AI) & @abasmanesh222 (motivation). Communicates only in Persian. Prefers direct, practical answers; hates research bloat. Uses Windows (PowerShell) & AgentRouter. IRST (UTC+3:30) time. Reads 'When Panic Attacks' for anxiety. Medical appts: every other Tue 19:30.
§
Model config: geminiM (primary) with opencode fallback (both via openai-api provider). Telegram Bot: @GoldPackFree_PosterBot (-1001378242402). RTL Formatting: every line must start with a Persian word or emoji; never English words/URLs at start. No ZWNJ characters in cron prompts (English prompts, Persian output).
§
Always express/display times in Tehran time (Iran Standard Time, UTC+3:30 or IRST) by default. Specify the timezone explicitly only when mentioning non-Iran time.
§
Workflow: Tech posts (AI news/models, editors, free gen/APIs) sent to DM for review/manual post. Motivational quotes sent directly to channel. Format: Single-subject, hook + 1-line intro + 4-5 emoji bullets + direct link, max 10 lines. Cron: 08:00 (Quote), 09:00 (AI News), 15:30 (Free AI/API), 20:30 (Hidden Gems). cron.wrap_response=false.