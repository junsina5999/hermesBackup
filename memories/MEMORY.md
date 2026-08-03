Persian text rendering in Pillow: Vazirmatn fonts (Black/Bold/Medium) from cdn.jsdelivr.net (GitHub raw URLs return HTML error pages), plus arabic-reshaper + python-bidi, pattern reshaper.reshape(text) -> get_display() -> draw.text(). Test before batches; wrap at ~22 chars/line for 1080x1080 cards.
§
User works on a Windows environment using PowerShell for local CLI tools.
§
Global NPM installs for tools like claude-code or opencode-ai on the user's machine may require the --allow-scripts flag to avoid "not a valid application" errors caused by blocked post-install scripts.
§
Cron prompt validator blocks invisible Unicode (U+200C ZWNJ) common in Persian/Arabic/Urdu text. Workaround: write cron prompts in English, instruct agent to output in target language. See cron-orchestration skill.
§
Agent Reach installed from source at /data/workspace/Agent-Reach (pip install -e). Zero-config channels: GitHub, YouTube, V2EX, RSS, Jina Reader, Bilibili search. Twitter/Reddit/XHS/Facebook/Instagram need cookies or desktop OpenCLI. Run `agent-reach doctor` to check.
§
Tech digest cron job 6e3a37165521 delivers a Persian tech-news post daily at 09:00 Tehran (30 5 * * * UTC). Repeat-protection log lives at /data/workspace/tech-channel-history.txt. Workflow details in telegram-content skill, references/tech-news-curation.md.
§
The /data partition is small (~434MB) and fills up, breaking npm installs with ENOSPC. /data/.cache is the usual culprit; clearing it frees ~290MB.
§
AI image generators still render Farsi text broken inside images (detached, malformed glyphs). Keep image prompts in English and overlay Farsi text afterward in an editor.
§
skill_manage(action='create') rejects skill descriptions over ~60 chars (index truncates at 57). One short trigger sentence; detail goes in the body.
§
Image editing: user works in Google AI Studio Playground on Android. Gemini image models copy style well but reinterpret real faces (slimmer/younger) — for identity preservation use Flux Kontext Max on fal.ai or face-swap tools (InstantID/PuLID, remaker.ai). Prompt pattern: make the real photo the BASE image and change only wardrobe/background/lighting.