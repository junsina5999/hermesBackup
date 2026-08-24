# Telegram Channel Delivery via Bot API

## Setup (one-time)

### 1. Create bot
Message @BotFather: `/newbot` → get token (format: `123456:ABC-DEF...`)

### 2. Add bot as channel admin
Channel Settings → Administrators → Add Administrator → search bot username
Grant only: **Post Messages** (disable all others)

### 3. Get channel chat_id
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getChat?chat_id=@channelusername"
# result.id is the numeric chat_id (e.g., -1001378242402)
```

### 4. Verify bot can post
```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d "chat_id=-100CHATID" \
  -d "text=Test post"
```

## Posting script pattern

```python
#!/usr/bin/env python3
import sys, urllib.request, urllib.parse, json

BOT_TOKEN = "<TOKEN>"
CHANNEL_ID = "<CHAT_ID>"

def post_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        if result.get("ok"):
            print(f"Posted (id: {result['result']['message_id']})")
        else:
            print(f"Error: {result.get('description')}")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 post_to_channel.py '<b>bold</b> text'")
        sys.exit(1)
    post_message(sys.argv[1])
```

Save as `post_to_channel.py` in workspace. Supports HTML: `<b>`, `<i>`, `<a href>`.

## Hermes cron header/footer limitation

When using Hermes cron `deliver: "telegram:-100CHATID"`, the message is wrapped:
- **Header**: `Cronjob Response: <job_name> (job_id: <id>)`
- **Footer**: `To stop or manage this job, send me a new message (e.g. "stop reminder <job_name>").`

These cannot be disabled in current Hermes versions. For clean channel posts,
use direct Bot API posting instead of Hermes cron delivery.

### Workaround: script-only cron (no_agent=True)
Set `no_agent=True` and `script` to a Python/bash script that:
1. Generates the content (or reads from a template)
2. Posts directly via Bot API
No LLM agent runs → no header/footer → clean post.

### Workaround: LLM cron + file handoff
1. Cron prompt tells LLM to write content to `/tmp/channel-post.txt`
2. Cron prompt ends with a terminal command that reads the file and posts via Bot API
The LLM output is the file write, not the final delivery.

## Posting photos/media

```bash
# Send photo with caption
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendPhoto" \
  -F "chat_id=<CHAT_ID>" \
  -F "photo=@/path/to/image.png" \
  -F "caption=Caption text" \
  -F "parse_mode=HTML"

# Send document/file
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/sendDocument" \
  -F "chat_id=<CHAT_ID>" \
  -F "document=@/path/to/file.pdf" \
  -F "caption=Download this"
```

## Edit a posted message

```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/editMessageText" \
  -d "chat_id=<CHAT_ID>" \
  -d "message_id=<MSG_ID>" \
  -d "text=Updated text" \
  -d "parse_mode=HTML"
```

## Delete a message

```bash
curl -s -X POST "https://api.telegram.org/bot<TOKEN>/deleteMessage" \
  -d "chat_id=<CHAT_ID>" \
  -d "message_id=<MSG_ID>"
```
