---
name: cron-orchestration
description: "Build Hermes cron jobs: timezone, chaining, state tracking."
version: 1.0.0
author: Hermes Agent
tags: [cron, scheduling, orchestration, timezone, recurring-jobs]
---

# Cron Job Orchestration

Patterns for building reliable, coordinated cron job systems in Hermes.

## Timezone Conversion

Hermes cron uses **UTC**. Convert user local time before creating jobs.

| City | UTC Offset | Example: 8:00 local |
|------|-----------|---------------------|
| Tehran (IRST) | +3:30 | 4:30 UTC |
| Dubai (GST) | +4 | 4:00 UTC |
| IST (India) | +5:30 | 2:30 UTC |
| PST (US West) | -8 | 16:00 UTC (prev day) |

Formula: `UTC = local - offset`. For :30 offsets, the cron minute becomes `30`.

```python
# Tehran example: 8:00 IRST = 4:30 UTC
cron: "30 4 * * *"
# 16:00 IRST = 12:30 UTC
cron: "30 12 * * *"
# 22:00 IRST = 18:30 UTC
cron: "30 18 * * *"
```

## Unicode Blocking Pitfall

**The cron prompt validator blocks invisible Unicode characters** (U+200C ZWNJ, etc.) common in Persian, Arabic, and Urdu text. This causes creation failures with: `Blocked: prompt contains invisible unicode U+200C (possible injection)`.

**Workaround**: Write cron prompts entirely in **English**, and instruct the agent inside the prompt to output in the target language. Example:

```
# WRONG - will be blocked for Persian/Arabic scripts:
prompt: "هر روز یک فصل خلاصه کن..."

# CORRECT - English prompt, Farsi output instruction:
prompt: "Write a chapter summary in fluent Farsi. ..."
```

This applies to ALL non-Latin scripts, not just Farsi.

## Cron Job Chaining with `context_from`

When job B needs to reference job A's output (e.g., evening homework reminder referencing afternoon assignment):

```json
{
  "job_id": "B",
  "context_from": ["A"]
}
```

- Injects A's most recent completed output into B's prompt as context
- B's prompt must explicitly instruct the agent to use that context
- Does NOT wait for A if both run in the same tick — uses the most recent *completed* output
- Only works between jobs in the same Hermes instance

**Best practice**: Always add an explicit instruction in the dependent job's prompt:
```
"You will receive the previous job's output as context. Reference the
specific content from it. If context is missing or unclear, use a
sensible default."
```

## File-Based State Tracking

For sequential content delivery (e.g., one chapter per day), use files to track progress:

1. **Progress file** (`chapter-progress.txt`): Single integer, current index
2. **Content reference file** (`burns-chapters.txt`): Numbered list of topics
3. **Output file** (`burns-summaries.md`): Growing document of completed work

Cron prompt pattern:
```
1. read_file the progress file to get current index
2. read_file the reference file to find that index's topic
3. Generate the content (summary, exercise, etc.)
4. read_file the output file, append new content, write_file it back
5. write_file the progress file with index + 1
6. If index == max, reset to 1
```

**Requires**: `enabled_toolsets: ["file"]` (and optionally `"terminal"` for shell access).

## Model Assignment

Cron jobs pin a model at creation. Without it, jobs fail with "no model configured".

```json
{
  "model": {"model": "gemini", "provider": "openai-api"}
}
```

Models can be changed after creation with `cronjob action=update, model={...}`.
The model is NOT permanently fixed — update it when the user changes their
provider setup, API keys, or default model.

### Provider Migration

When the user switches infrastructure (e.g. drops one API provider for another),
existing cron jobs keep pointing at the old provider and fail silently or with
HTTP 403/401. Steps:

1. `cronjob action=list` — find jobs using the old provider
2. For each job, check `model` and `provider` fields
3. `cronjob action=update, job_id=X, model={"model":"...","provider":"..."}`
4. Run each job once (`cronjob action=run`) to verify the new provider works
5. Watch for: 401 (auth expired), 403 (provider blocked), 404 (model not found
   on that provider)

**Common pitfall**: The `openai-api` provider uses `OPENAI_API_KEY` and
`OPENAI_BASE_URL` from `.env`. If those point to a proxy (9router, etc.), the
proxy must be reachable and have credits. Custom providers (under
`custom_providers:` in config.yaml) use their own `key_env` — check both the
provider config and the `.env` key it references.

**Quick diagnosis**: If a cron job fails with "HTTP 401/403/404", the model or
provider is wrong — not the prompt. Update the model, don't rewrite the prompt.

### 9Router Multi-Provider Quirks (Troubleshooting)

When using 9Router (or similar multi-provider proxies) as the OpenAI-compatible
endpoint, the same API key can serve multiple upstream "providers" (e.g.,
`multiai`, `multiai2`, `tokenrouter`, `gorouter`, `llmtr`, `ar`, `gemini`,
`groq`). **Each upstream provider has its own API key status and validity.**

**Key discovery from debugging:**
- A single 9Router key can work for `multiai2/*` models (Anthropic-style
  upstream) but fail with 401 for `multiai/*` models (OpenAI-style upstream).
- The `/v1/models` endpoint lists ALL models from all upstreams, but doesn't
  validate which upstream keys are actually working.
- **Error pattern**: `[multiai/...] [401]: "The provided API Key is invalid or
  has been revoked"` while `multiai2/...` streams successfully.

**Diagnosis steps:**
```bash
# 1. List all available models
KEY=$(grep OPENAI_API_KEY ~/.hermes/.env | cut -d= -f2)
curl -s -H "Authorization: Bearer $KEY" "$OPENAI_BASE_URL/models" | jq '.data[].id'

# 2. Test a specific model (streaming endpoint catches upstream errors better)
curl -s -X POST -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{"model":"multiai/mimo-v2.5-free","messages":[{"role":"user","content":"test"}],"max_tokens":10}' \
  "$OPENAI_BASE_URL/chat/completions"

# 3. Compare with multiai2 variant
curl -s -X POST ... -d '{"model":"multiai2/mimo-v2.5-free",...}' ...
```

**Resolution:**
- If a model family (e.g., all `multiai/*`) fails, regenerate the upstream key
  in the 9Router dashboard for that specific provider.
- Or switch to the working family (`multiai2/*`, `llmtr/*`, `tokenrouter/*`, etc.)
- Add the working model aliases to `model_aliases` in `config.yaml` for easy access.

**Best practice for cron jobs**: Test the exact model string from the cron
config via the API first. If it returns 401/403, the cron will fail — fix the
model or the upstream key before scheduling.

## Multi-Job Coordination Patterns

### Daily Routine (3x/day)
```
Morning  (8:00)  → Motivation + daily task
Afternoon (16:00) → Technique/exercise + homework assignment
Evening  (22:00) → Homework reminder + reflection + relaxation
```

Evening chains to afternoon via `context_from`.

### Content Series (daily at fixed time)
```
One chapter/lesson per day
State file tracks position in series
Output file accumulates for PDF generation
```

### Alert/Watchdog (script-based, no agent)
```
no_agent: true, script: "check-something.sh"
Empty stdout = silent (nothing sent)
Non-empty stdout = delivered as message
```

## Disk Space Awareness

Cron jobs run on the same filesystem. On small disks (<1GB), be cautious about:
- Downloading large files (PDFs, datasets) for processing
- Accumulating output files over time
- PDF generation that creates large files

Check with `df -h` before downloading. Clean up temp files after processing.

## Cron Job Delivery: Final Response = Delivered Message

**Critical pattern**: What the agent outputs as its final assistant text IS the message delivered to the user. If the agent only calls tools (write_file, read_file) and produces no text response, nothing gets delivered.

This causes silent failures: the cron runs successfully (status: ok), files are written, but the user sees nothing.

**Fix**: Always include an explicit instruction in the cron prompt:
```
CRITICAL: Your FINAL RESPONSE (the assistant text you output at the end)
IS the message delivered to the user. Put the user-facing content there.
Writing to files is secondary. Do NOT end with just tool calls.
```

**Verification**: After creating a cron job, run it once (`cronjob action=run`) and confirm the user received the message, not just that files were updated.

## Model Provider Matching

Models must match their provider. Setting `{"model": "gemini", "provider": "openai-api"}` will fail with HTTP 404 because gemini models are not available through the OpenAI-compatible API endpoint.

Check which models are available on each provider:
- `openai-api`: GPT models, opencode
- `anthropic`: Claude models
- `openrouter`: Most models including gemini
- Use `hermes models` to see available model/provider combinations

When in doubt, use the current session's model as a safe default.

## Telegram MEDIA: File Format

When delivering files via `MEDIA:/path/to/file` on Telegram:
- **`.txt` files work** — sent as document attachments
- **`.md` files may fail silently** — Telegram sometimes rejects markdown files via MEDIA:
- Always use `.txt` extension for file delivery on Telegram
- If you need markdown content, save as `.txt` and send that

Pattern for cron jobs that deliver files:
```
1. Generate content
2. Save to /data/workspace/chapter-N.txt  (NOT .md)
3. In final response: MEDIA:/data/workspace/chapter-N.txt
4. Clean up file after user confirms receipt
```

## Telegram Channel Delivery (Cron → Channel)

When a cron job delivers to a Telegram channel via `deliver: "telegram:-100CHATID"`,
Hermes wraps the message with a header (`Cronjob Response: ...`) and footer
(`To stop or manage this job...`).

**Key config**: Set `cron.wrap_response: false` in `config.yaml` to deliver raw
agent output WITHOUT header/footer:
```bash
hermes config set cron.wrap_response false
```
This is the cleanest way to post to channels — no header, no footer, no extra
script needed.

**Pitfall**: Hermes's own Telegram bot must be an admin of the target channel
for `deliver: "telegram:-100CHATID"` to work. If you can't add Hermes's bot,
use direct Bot API posting instead (see `telegram-content` skill).

### Clean delivery (no header/footer) — Alternative approach
If `cron.wrap_response` isn't an option, use a custom bot + direct Bot API.
The cron prompt writes content to a file, then a script posts it:
```python
# In cron prompt:
# 1. Generate post text
# 2. write_file to /tmp/channel-post.txt
# 3. terminal: python3 post_to_channel.py "$(cat /tmp/channel-post.txt)"
```
See `references/channel-delivery.md` in the `telegram-content` skill for
the full `post_to_channel.py` pattern.

## Verification Checklist

Before declaring cron setup complete:
- [ ] Timezone converted correctly (test with known UTC time)
- [ ] No Unicode/ZWNJ in prompts (or written in English)
- [ ] Model assigned to every LLM-driven job
- [ ] Model matches its provider (e.g. gemini needs openrouter, not openai-api)
- [ ] Provider is reachable — run `cronjob action=run` and check for 401/403/404
- [ ] `context_from` chains are correct and prompts reference context
- [ ] State files initialized (chapter-progress.txt, etc.)
- [ ] `enabled_toolsets` includes "file" if job reads/writes files
- [ ] Disk space sufficient for any downloads or output files
- [ ] Agent prompt instructs it to output user-facing content as final response (not just tool calls)
- [ ] File delivery uses `.txt` extension for Telegram MEDIA: (not `.md`)
- [ ] Test file delivery manually to confirm MEDIA: works
