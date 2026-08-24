---
name: telegram-content
description: Persian quote images and posts for Telegram channels.
version: 1.0.0
tags: [telegram, persian, farsi, rtl, image-generation, social-media, content-creation, pillow]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [telegram, persian, farsi, rtl, pillow, content, motivational]
    related_skills: [comfyui, claude-design, humanizer]
---

# Telegram Channel Content Generator

Create visually appealing Persian/Farsi quote images and text posts for Telegram channels. Combines image generation (Pillow + RTL text rendering) with structured text post writing.

## When To Use

- User wants to create posts for a Telegram channel or group
- User needs Persian/Farsi text images (quote cards, motivational graphics)
- User wants social media content in RTL languages
- User wants automated or semi-automated content creation for channels
- User wants a recurring tech-news / tool-discovery digest for a channel
  (see `references/tech-news-curation.md` for sources, filtering, and the
  digest → deep-dive two-tier post pattern)

## Universal content rules for this audience

These apply to every post type, not just quote cards:

1. **Free vs paid, always explicit.** Separate the layers: an open-source repo
   can be free while the service it depends on is paid. State both.
2. **Flag VPN/Iran accessibility** whenever a service is blocked or restricted.
3. **Teach a transferable principle, then link.** A bare link with a summary
   gets skipped; a post that leaves the reader knowing something gets saved.
4. **Never post a resource the reader cannot act on.** If an item is a
   reference/library/awesome-list rather than a usable tool, either reframe it
   as an educational post or drop it.
5. **End with a question** to invite comments.
6. **Deliver copy-paste-ready text.** No English commentary or meta-explanation
   wrapped around the post body — the user pastes it straight into the channel.
7. **Persian-First Lines.** Every line of a post must start with a Persian word
   (or emoji). Never start a line with English text or a raw URL, as it breaks
   RTL alignment in many clients.

## Three-Tier Daily Tech Workflow

The channel runs on a three-post-per-day schedule:
- **Morning (09:00 Tehran):** AI News & Frontier Models. Breakthroughs, new
  releases, and major launches.
- **Afternoon (15:30 Tehran):** Free AI Tools & APIs. Genuinely free (no-card)
  API tiers, free image/video generators, and prompt libraries reframed as lessons.
- **Evening (20:30 Tehran):** Hidden Gem Apps. Highly practical but
  lesser-known photo/video editors, system utilities, or mobile tools.

### Structured Post Template (The "Asha" Style)

All tech posts must follow this 8-10 line format:
```
💥 [Hook headline with emoji]
[1 sentence intro setting the stage]

🎯 [Feature 1 / Benefit]
⚡ [Feature 2 / Benefit]
🔗 [Feature 3 / Benefit]
🔒 [Feature 4 / Benefit]

[Punchy conclusion / status]
@GoldPackFree2
[Official DIRECT link URL]
```
Note: Emojis are allowed at the start of lines, but the first *text* must be Persian.

### Motivational Quotes

- **Morning (08:00 Tehran):** One profound quote from a thinker/leader/artist.
- **Format:** Emoji + Quote + Author (brief identifier). No translation notes or book blurbs.
- **Tone:** Human, warm, and poetic. Avoid cliches; prioritize depth.

## Pipeline

### Step 1: Understand the Brief

Gather from user:
- **Channel topic/niche** (e.g., motivation, psychology, business)
- **Target audience** and tone (formal, casual, inspirational)
- **Posting frequency** (daily, weekly, etc.)
- **Author/speaker attribution** (if any — e.g., a specific teacher or quote source)
- **Style preference** — ask if they want: text-only posts, image+text, or just images

### Step 2: Content Writing

For motivation/success channels, follow this structure:
- Short, punchy Persian text (2-5 lines max)
- Start with a hook or question
- Include a quote or key insight (attributed if applicable)
- End with a call-to-action (question, "save this", "share your thought")
- Use emoji sparingly but effectively (🌀, ✨, 💡, 🔥, 📌)

Text style rules:
- **Do NOT** over-explain — keep each post under 150 words
- Use short sentences and line breaks for readability
- Mix two styles: (a) reflective/philosophical + (b) actionable/tip-based
- Include hashtags at the end only if the user requests them

### Step 3: Image Generation (Quote Cards)

Use Pillow + Vazirmatn font + arabic-reshaper + python-bidi.

#### Dependencies

```bash
pip3 install Pillow arabic-reshaper python-bidi
```

#### Fonts

Download Vazirmatn (Persian font family). **CRITICAL**: GitHub raw URLs return HTML error pages, NOT font files. Always use **jsDelivr CDN**:
```bash
mkdir -p fonts
cd fonts
curl -sL "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf" -o Vazirmatn-Bold.ttf
curl -sL "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Black.ttf" -o Vazirmatn-Black.ttf
curl -sL "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Medium.ttf" -o Vazirmatn-Medium.ttf
```

#### RTL Text Rendering (Critical)

Persian/Arabic text MUST be reshaped before rendering in Pillow:

```python
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_persian(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)
```

Without this step, connected Arabic/Persian letters render disconnected and reversed.

#### Image Dimensions

- **Telegram channel posts**: 1080×1080 (square)
- **Telegram stories**: 1080×1920 (vertical)
- **Wide format**: 1200×630 (link previews)

#### Design Patterns

Use gradient backgrounds with color palettes:
- `deep_purple` — elegant, introspective
- `warm_gold` — wealth, success, prosperity
- `ocean_blue` — calm, wisdom
- `midnight` — premium, authoritative
- `rose` — emotional, relationship-focused
- `dark_teal` — growth, transformation

Layout (top to bottom):
1. Top accent line
2. Opening quote mark (decorative)
3. Main quote text (centered, large)
4. Closing quote mark
5. Separator line
6. Sub-text / explanation (smaller, muted)
7. Author attribution (accent color)
8. Bottom accent line
9. Channel watermark (@handle)

#### Text Wrapping

Persian text wrapping uses character count (not word width) because Arabic-script characters are roughly equal width:

```python
def wrap_persian_text(text, max_chars=22):
    words = text.split()
    lines, current_line, current_len = [], [], 0
    for word in words:
        if current_len + len(word) + 1 > max_chars and current_line:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_len = len(word)
        else:
            current_line.append(word)
            current_len += len(word) + 1
    if current_line:
        lines.append(" ".join(current_line))
    return lines
```

### Step 4: Delivery

- Generate images and send via MEDIA: path
- Also provide the text version (copy-pasteable) as a separate block
- Offer multiple image variants with different color palettes for variety

### Pitfalls

1. **RTL text rendering** — Never skip `arabic_reshaper` + `bidi`. Without it, Persian letters appear disconnected and backward. This is the #1 mistake.
2. **Font availability** — Vazirmatn fonts must be downloaded before running. Check with `ls fonts/Vazirmatn-*.ttf`.
3. **Small file sizes** — If generated PNGs are under 50KB for 1080×1080, something went wrong (likely text not rendering). Check font loading.
4. **Text overflow** — Persian text with many characters can overflow the image. Use `wrap_persian_text()` and adjust `max_chars` based on total quote length.
5. **Gradient banding** — For smooth gradients, use 1-pixel-wide horizontal lines rather than large filled rectangles.

### Telegram Channel Cloning (Telethon)

To clone an entire channel's history to another channel without forward tags (preserving media on Telegram servers, no download/upload):

```python
import asyncio
from telethon import TelegramClient

api_id = YOUR_API_ID
api_hash = 'YOUR_API_HASH'
source = 'source_channel_username'
target = 'target_channel_username'

client = TelegramClient('session_name', api_id, api_hash)

async def clone_channel(min_id=0):
    await client.start()
    async for msg in client.iter_messages(source, min_id=min_id, reverse=True):
        try:
            await client.send_message(target, msg)
            # Progress tracking
            with open('last_copied_id.txt', 'w') as f:
                f.write(str(msg.id))
            await asyncio.sleep(0.5)  # Rate limit safety
        except Exception as e:
            print(f"Error {msg.id}: {e}")
            await asyncio.sleep(5)

with client:
    client.loop.run_until_complete(clone_channel(min_id=LAST_COPIED_ID))
```

**Key points:**
- `send_message(target, message)` = server-side copy (no download, preserves file_ids)
- `min_id=N` starts from message N+1 (exclusive). Use last copied ID.
- `reverse=True` processes oldest→newest (chronological order).
- Save `last_copied_id.txt` every ~10 messages for resumability.
- **CRITICAL**: Don't name the script `copy.py` — conflicts with Python's `copy` stdlib module. Use `tg_copy.py`, `clone.py`, etc.
- Rate limit: 0.5-1s delay between messages to avoid FloodWait.
- If interrupted, re-run with same `min_id` from saved file.

## Verification

After generating images:
1. Check file size (should be 50-200KB for 1080×1080 PNG)
2. Verify image dimensions match expected size
3. Confirm Persian text is readable (not garbled/reversed)
4. Send via MEDIA: path to confirm Telegram renders it correctly

## Channel Delivery

### Direct bot API (preferred for clean posts)

To post directly to a Telegram channel without Hermes cron wrappers, use the
Telegram Bot API via a `post_to_channel.py` helper script. This avoids the
`Cronjob Response: ...` header and `To stop or manage this job...` footer that
Hermes appends to cron deliveries.

**Setup pattern (do once):**
1. Create bot via @BotFather
2. Add bot as admin of the channel (Post Messages only)
3. Get channel chat_id via `getChat?chat_id=@channelusername` → `result.id`
4. Create `post_to_channel.py` with BOT_TOKEN and CHANNEL_ID constants
5. Usage: `python3 post_to_channel.py "your HTML message"`

### Hermes cron delivery (has header/footer)

Hermes cron jobs deliver to channels via `deliver: "telegram:-100CHATID"`.
The message is automatically wrapped with:
- Header: `Cronjob Response: <job_name> (job_id: <id>)`
- Footer: `To stop or manage this job, send me a new message...`

**Removing Headers/Footers:**
User has explicitly asked these be removed. To deliver clean posts via cron:
1. **Built-in setting:** Run `hermes config set cron.wrap_response false`.
   This is the cleanest method and applies globally to all cron jobs.
2. **Bot API Fallback:** If the built-in setting is insufficient, use the
   `post_to_channel.py` script inside the cron prompt.
3. **Manual Review:** For high-quality channels, deliver to the user's origin
   session instead (`deliver: "origin"`). The agent generates the draft, and
   the user copy-pastes manually.

### Cron → channel workflow (header-free)

**Best option (Hermes built-in):** Set `cron.wrap_response: false` in `config.yaml`:
```bash
hermes config set cron.wrap_response false
```
This delivers raw agent output — NO header, NO footer, no extra script needed.

**Alternative — Script-only cron (no_agent=True):**
```bash
# Script generates content AND posts via Bot API
# Header/footer never appear because no LLM agent runs
```

**Alternative — LLM cron + post script:**
```python
# 1. LLM generates post text, writes to /tmp/channel-post.txt
# 2. Script reads file, posts via Bot API
# Both happen inside the cron prompt
```

## References

- `references/persian-fonts.md` — font alternatives and fallbacks
- `references/telegram-specs.md` — Telegram media size limits
- `references/tech-news-curation.md` — daily tech digest: GitHub/HN/newsroom
  sources, spam filtering, repeat-protection log, digest → deep-dive pattern,
  cron wiring for 09:00 Tehran, free AI API sources
- `references/channel-delivery.md` — bot API setup, chat_id lookup, posting
  script, cron header/footer limitation and workaround
- `scripts/generate-post.py` — CLI tool: `python3 scripts/generate-post.py --quote "..." --palette deep_purple --output post.png`
