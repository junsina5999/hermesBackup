---
name: ticktick-mcp
description: "Task management in TickTick via MCP integration."
version: 1.0.0
author: Hermes
tags: [ticktick, mcp, task-management, productivity]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ticktick, mcp, task-management]
---

# TickTick MCP Integration

Connect Hermes to TickTick for natural-language task management via MCP.

## Setup

```yaml
mcp_servers:
  ticktick:
    url: https://mcp.ticktick.com
    headers:
      Authorization: Bearer ${MCP_TICKTICK_API_KEY}
    enabled: true
```

Token: from TickTick web → Settings → Account → API Token. Store in `~/.hermes/.env` as `MCP_TICKTICK_API_KEY`.

## Auth workaround

`hermes mcp add --auth header` stores literal prompt string, not env var value. Fix: run with placeholder, then manually rewrite value in .env via terminal.

## Task creation (nested object required)

```python
# WRONG — fails with "Field required"
await s.call_tool('create_task', {"title": "...", "projectId": "..."})

# CORRECT
await s.call_tool('create_task', {"task": {
    "title": "Task name",
    "projectId": "list_id",
    "startDate": "2026-08-09T08:00:00.000+0330",
    "dueDate": "2026-08-09T08:30:00.000+0330",
    "repeatFlag": "RRULE:FREQ=DAILY"
}})
```

## Dates and repeats

Iran timezone: `+0330`. RRULE examples:
- Daily: `RRULE:FREQ=DAILY`
- Weekly Mon: `RRULE:FREQ=WEEKLY;BYDAY=MO`
- Biweekly Mon: `RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=MO`

## Reminders

The `reminders` field accepts ISO-8601 duration strings:
- `TRIGGER:PT0S` — notify at exact due time
- `TRIGGER:-PT5M` — 5 minutes before
- `TRIGGER:-PT15M` — 15 minutes before
- `TRIGGER:-PT60M` — 1 hour before

Combine with `repeatFlag: "RRULE:FREQ=DAILY"` for recurring daily reminders. The app sends a notification at the trigger time every day.

## Direct HTTP fallback

If MCP tools are not available as native hermes tools (e.g. in execute_code or terminal), call the MCP endpoint directly:

```bash
source ~/.hermes/.env
curl -s -X POST \
  -H "Authorization: Bearer $MCP_TICKTICK_API_KEY" \
  -H "Content-Type: application/json" \
  "https://mcp.ticktick.com" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_projects","arguments":{}}}'
```

List all available tools via `method: "tools/list"`. The REST API (`api.ticktick.com`) uses different auth — do NOT mix them.

## Recurring daily tasks pattern

For daily routines (exercise, study, meditation, etc.):
- `startDate` / `dueDate`: first occurrence in Tehran time (`+0330`)
- `timeZone`: `"Asia/Tehran"`
- `reminders`: `["TRIGGER:PT0S"]` (notify at due time)
- `repeatFlag`: `"RRULE:FREQ=DAILY"`

## Key tools

`list_projects`, `create_task`, `complete_task`, `delete_task`, `list_habits`, `create_habit`,
`get_project_with_undone_tasks`, `batch_add_tasks`, `batch_update_tasks`,
`list_columns`, `create_column`, `list_tags`, `create_tag`,
`list_countdowns`, `list_project_groups`, `get_user_preference`
