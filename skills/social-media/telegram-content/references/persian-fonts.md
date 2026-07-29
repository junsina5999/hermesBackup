# Persian Font Sources for Quote Images

## Vazirmatn (Recommended)
- GitHub: https://github.com/rastikerdar/vazirmatn
- TTF direct URLs (version v33.003):
  - Bold: https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Bold.ttf
  - Black: https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Black.ttf
  - Medium: https://github.com/rastikerdar/vazirmatn/raw/main/fonts/ttf/Vazirmatn-Medium.ttf

## Fallback Options
- **Noto Naskh Arabic** — `apt install fonts-noto` (good for Nastaliq-style)
- **IRANSans** — proprietary, widely used in Iran
- **Tahoma** — built-in on Windows, renders Persian well

## Font Size Guidelines (1080×1080 image)
| Font Weight | Use | Size (pt) |
|---|---|---|
| Black | Main quote (title) | 42–52 |
| Bold | Author name | 36 |
| Medium | Sub-text | 28–32 |
| Medium | Watermark | 24 |

## Verification
```bash
# List installed Persian/Arabic fonts
fc-list :lang=fa 2>/dev/null | head -10
fc-list :lang=ar 2>/dev/null | head -10
```
