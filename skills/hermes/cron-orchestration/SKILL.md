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

The model is fixed at creation time — changing the default model later does NOT update existing cron jobs. Always set explicitly.

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

## Verification Checklist

Before declaring cron setup complete:
- [ ] Timezone converted correctly (test with known UTC time)
- [ ] No Unicode/ZWNJ in prompts (or written in English)
- [ ] Model assigned to every LLM-driven job
- [ ] `context_from` chains are correct and prompts reference context
- [ ] State files initialized (chapter-progress.txt, etc.)
- [ ] `enabled_toolsets` includes "file" if job reads/writes files
- [ ] Disk space sufficient for any downloads or output files
- [ ] Test one job manually via `cronjob action=run` to verify
