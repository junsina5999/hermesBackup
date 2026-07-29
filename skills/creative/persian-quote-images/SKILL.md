---
name: persian-quote-images
description: Persian quote images with Pillow and bidi font rendering.
version: 1.0.0
tags: [persian, farsi, image-generation, pillow, quotes, telegram, social-media, fonts]
---

# Persian Quote & Motivational Image Generation

Generate beautiful Persian (Farsi) quote/motivational images for Telegram, Instagram, or other social media using Python Pillow with proper Persian text rendering.

## Core Technique: Persian Text Rendering in Pillow

Pillow cannot render Persian/Arabic text correctly by itself — it connects letters in the wrong order. You need:

### Dependencies

```bash
pip3 install Pillow arabic-reshaper python-bidi
```

### Font: Vazirmatn

**Critical**: GitHub raw URLs serve HTML error pages, not font files. Always use **jsdelivr CDN**:

```bash
curl -L "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Bold.ttf" -o Vazirmatn-Bold.ttf
curl -L "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Black.ttf" -o Vazirmatn-Black.ttf
curl -L "https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/ttf/Vazirmatn-Medium.ttf" -o Vazirmatn-Medium.ttf
```

Three weights: Black (headings), Bold (authors/titles), Medium (body/subtext).

### Rendering pipeline

```python
import arabic_reshaper
from bidi.algorithm import get_display

def reshape_persian(text):
    reshaped = arabic_reshaper.reshape(text)
    return get_display(reshaped)

# Always use this before draw.text()
draw.text((x, y), reshape_persian("متن فارسی"), font=font, fill=color)
```

### Text wrapping for Persian

```python
def wrap_persian(text, max_chars=22):
    words = text.split()
    lines, cur, clen = [], [], 0
    for w in words:
        if clen + len(w) + 1 > max_chars and cur:
            lines.append(" ".join(cur))
            cur, clen = [w], len(w)
        else:
            cur.append(w)
            clen += len(w) + 1
    if cur:
        lines.append(" ".join(cur))
    return lines
```

| Image size | Max chars/line |
|------------|---------------|
| 1080x1080  | 20-24 |
| 1080x1920  | 30-36 |

## Design Guidelines

- **Canvas**: 1080x1080 PNG, quality=95
- **Layout**: gradient bg, accent line, opening quote, main text, closing quote, author, watermark
- **6 palettes**: deep_purple, warm_gold, ocean_blue, midnight, rose, dark_teal
- **Font sizing**: Quote marks 110pt, main text 50pt decreasing, author 38pt, subtext 32pt, watermark 26pt

## Workflow

1. Research topic aligned to channel theme
2. Write 2-4 quotes on the topic
3. Generate images with varied palettes
4. Deliver via MEDIA: paths + caption text

## Pitfalls

1. **Font sources**: GitHub raw = HTML errors. Use jsdelivr CDN.
2. **Verify fonts**: `head -c 10 font.ttf | cat -v` should be binary, not HTML.
3. **Bidi is mandatory**: Without `get_display()`, Persian text is mirrored.
4. **Test first**: Verify one image before batch generation.
