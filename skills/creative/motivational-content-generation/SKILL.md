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

## Daily Text-Only Quote Delivery (Cron)

For automated daily motivational quotes via cron (no image, just text post):

### Cron setup pattern
- Schedule: `30 4 * * *` for 8:00 AM Tehran (UTC+3:30)
- `enabled_toolsets: ["terminal", "file"]`
- Prompt must be in English (cron validator blocks Persian ZWNJ/Unicode)
- **Disable header/footer:** Set `cron.wrap_response: false` in `config.yaml` via `hermes config set cron.wrap_response false`
- Pin a model explicitly (e.g. `{"model":"opencode","provider":"openai-api"}`)

### Quote selection strategy
- Rotate between: Rumi, Hafez, Saadi, Socrates, Marcus Aurelius, Einstein,
  Viktor Frankl, Maya Angelou, Nassim Taleb, Iranian literary greats
- Avoid overposted cliches — prefer quotes that make someone stop and think
- Track posted quotes in `/data/workspace/quotes-history.txt`
  Format: `YYYY-MM-DD | author | first 5 words of quote`

### Text post format
- 1 evocative opening line with 1 emoji
- The quote in Persian quotation marks
- Author name + brief 5-word identifier ("فیلسوف یونانی", "شاعر ایرانی")
- No markdown headers, no excessive bold, warm and human tone

### Prompt template (English, for cron)
```
You are a curator of motivational quotes for an Iranian Telegram channel.
Read /data/workspace/quotes-history.txt to avoid repeats. Pick ONE profound
quote from a famous thinker. Write the post in fluent Persian with author
attribution. Your FINAL RESPONSE is the delivered message.
```

### Model provider migration
When the user switches infrastructure (e.g. drops one API provider for another),
existing cron jobs keep pointing at the old provider and fail silently or with
HTTP 403/401. Steps:
1. `cronjob action=list` — find jobs using the old provider
2. For each job, check `model` and `provider` fields
3. `cronjob action=update, job_id=X, model={"model":"...","provider":"..."}`
4. Run each job once (`cronjob action=run`) to verify the new provider works
5. Watch for: 401 (auth expired), 403 (provider blocked), 404 (model not found
   on that provider)

**Quick diagnosis**: If a cron job fails with "HTTP 401/403/404", the model or
provider is wrong — not the prompt. Update the model, don't rewrite the prompt.
