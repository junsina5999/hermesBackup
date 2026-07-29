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

Download Vazirmatn (Persian font family):
```bash
mkdir -p fonts
cd fonts
curl -sL "https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Bold.ttf" -o Vazirmatn-Bold.ttf
curl -sL "https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Black.ttf" -o Vazirmatn-Black.ttf
curl -sL "https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Medium.ttf" -o Vazirmatn-Medium.ttf
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

## Pitfalls

1. **RTL text rendering** — Never skip `arabic_reshaper` + `bidi`. Without it, Persian letters appear disconnected and backward. This is the #1 mistake.
2. **Font availability** — Vazirmatn fonts must be downloaded before running. Check with `ls fonts/Vazirmatn-*.ttf`.
3. **Small file sizes** — If generated PNGs are under 50KB for 1080×1080, something went wrong (likely text not rendering). Check font loading.
4. **Text overflow** — Persian text with many characters can overflow the image. Use `wrap_persian_text()` and adjust `max_chars` based on total quote length.
5. **Gradient banding** — For smooth gradients, use 1-pixel-wide horizontal lines rather than large filled rectangles.

## Verification

After generating images:
1. Check file size (should be 50-200KB for 1080×1080 PNG)
2. Verify image dimensions match expected size
3. Confirm Persian text is readable (not garbled/reversed)
4. Send via MEDIA: path to confirm Telegram renders it correctly

## References

- `references/persian-fonts.md` — font alternatives and fallbacks
- `references/telegram-specs.md` — Telegram media size limits
- `scripts/generate-post.py` — CLI tool: `python3 scripts/generate-post.py --quote "..." --palette deep_purple --output post.png`
