---
name: motivational-content-generation
description: Create motivational Persian content for Telegram.
---

# Motivational Content Generation

Use this skill to generate success-themed content (Abbasmanesh-style) for Persian Telegram channels, consisting of visually-appealing quote cards and descriptive captions.

## Workflow

1. **Drafting (User Approval First)**
   - Provide the **Main Quote** (short, for image) and **Sub Text** (long, for caption) in text form.
   - Wait for user feedback/approval before generating the final image.

2. **Image Generation**
   - Use the `premium_generator.py` script for high-quality output.
   - **Technical Requirement:** Always use `arabic_reshaper` and `python-bidi` for Persian text.
   - **Assets:** Ensure Vazirmatn fonts (Black, Bold, Medium) are in the `fonts/` directory.

3. **Presentation**
   - Deliver the image via `MEDIA:/path/to/image.png`.
   - Provide the final text caption clearly for easy copying/forwarding.

## Style Guidelines (Premium)
- **Glassmorphism:** Use semi-transparent cards behind text for depth.
- **Color Palettes:** `luxury_gold` (Black/Gold), `royal_purple` (Deep Purple), `emerald_night` (Dark Teal).
- **Typography:** Bold fonts for the main message; medium for the subtext.

## Pitfalls
- **Font corruption:** Downloading directly from GitHub raw URLs can return HTML error pages. Use `cdn.jsdelivr.net` for reliable font downloads.
- **Rendering:** Persian characters must be reshaped and reordered before being drawn on canvas.
