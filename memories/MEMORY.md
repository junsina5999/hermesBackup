Persian text rendering in Pillow requires: Vazirmatn fonts (Black/Bold/Medium) from jsdelivr CDN, arabic-reshaper + python-bidi libraries, and the pattern: reshaper.reshape(text) -> get_display() -> draw.text(). GitHub raw URLs for fonts return HTML error pages; use cdn.jsdelivr.net instead. Test font rendering before generating batches. Farsi text needs proper bidi handling and word wrapping (max ~22 chars/line for 1080x1080 cards).
§
User works on a Windows environment using PowerShell for local CLI tools.
§
Global NPM installs for tools like claude-code or opencode-ai on the user's machine may require the --allow-scripts flag to avoid "not a valid application" errors caused by blocked post-install scripts.
§
Cron prompt validator blocks invisible Unicode (U+200C ZWNJ) common in Persian/Arabic/Urdu text. Workaround: write cron prompts in English, instruct agent to output in target language. See cron-orchestration skill.