# Telegram Media Specs

## Image Dimensions
- **Channel/Group posts** (in-feed): 1080×1080 square → best for mobile feed
- **Stories**: 1080×1920 vertical (9:16 ratio)
- **Link previews**: 1200×630 (1.91:1 ratio)

## File Size Limits
- Photo: up to 10MB (PNG, JPEG, WEBP)
- File: up to 2GB (any format)
- Preferred: 50–500KB per image for fast loading

## Delivery Notes
- Send via MEDIA:/absolute/path/to/file.png — Hermes auto-detects format
- Telegram scales images to fit; 1080px wide is max display width
- Square 1080×1080 is displayed at ~1080×1080 on desktop, ~512×512 on mobile

## Text Formatting in Telegram Messages
- **Bold**: `**text**`
- *Italic*: `*text*`
- `Code`: `` `code` ``
- Spoiler: `||text||`
- Links: `[text](url)`
- Headers: `## Header`
- Lists: `- item`
