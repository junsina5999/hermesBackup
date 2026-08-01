# Tech News Curation for Persian Telegram Channels

Workflow for a daily/recurring tech digest aimed at a general (non-developer)
Persian-speaking Telegram audience: practical apps, trending GitHub tools, free
AI sites, Windows/Android customization software, and major launch news.

## Data sources (all work without login)

```bash
# New trending repos, last N days
curl -s -m 25 "https://api.github.com/search/repositories?q=created:%3E$(date -d '10 days ago' +%Y-%m-%d)+stars:%3E150&sort=stars&order=desc&per_page=20"

# "Hidden gem" slot — created in the last year, still actively pushed
curl -s -m 25 "https://api.github.com/search/repositories?q=created:%3E$(date -d '1 year ago' +%Y-%m-%d)+stars:%3E3000&sort=updated&order=desc&per_page=20"

# Hacker News, score-filtered
curl -s -m 25 "https://hn.algolia.com/api/v1/search_by_date?tags=story&numericFilters=points%3E100&hitsPerPage=25"

# Per-repo detail for a deep-dive post
curl -s -m 25 "https://api.github.com/repos/OWNER/NAME"
curl -s -m 25 "https://raw.githubusercontent.com/OWNER/NAME/main/README.md"

# Vendor newsroom (Samsung/Apple/etc.) when the API route doesn't exist
curl -s -m 25 "https://r.jina.ai/https://news.samsung.com/global/" | grep -iE "keyword" | head -20
```

Parse JSON with `python3 -c` reading stdin. Twitter and Reddit need login
cookies — treat them as optional enrichment, never as the backbone.

## Filtering rules

Drop before selection:
- Crypto / MEV / arbitrage "bot" repos (these rank high and are always spam)
- Academic papers or benchmark repos with no runnable tool
- Developer-only libraries with no end-user surface
- Anything already logged in the history file

## Repeat protection

Keep a plain-text log and read it before every run:

```
/data/workspace/tech-channel-history.txt
# Format: YYYY-MM-DD | item name | source
```

Append one line per selected item at the end of the run. Without this, the
same trending repo gets posted three days running.

## Two-tier post structure (important)

The user runs a **digest → deep dive** pattern, not one-shot posts.

1. **Daily digest** (cron, 4–5 items): one emoji headline + 2–4 sentences +
   link per item. 250–400 Persian words total. This is a menu, not the meal.
2. **Deep-dive post** (on request, one item): the user replies asking to
   "open" an item. Fetch the repo API + README, then write a full standalone
   post: what problem it solves → feature list with emoji bullets → who it's
   for → technical specs line (size, license, stars, OS support) → install
   caveats → link.

When writing a deep dive, always pull the real README. Star counts and feature
lists from the digest run go stale and the digest's 2-sentence summary is not
enough material.

## Rules learned from user corrections

- **Always state free vs paid explicitly, and separate the two layers.** For an
  AI tool, the repo/library may be free while the underlying model needs a paid
  subscription. Say both. The user pushed back on an item precisely because
  "is this free or paid?" was unanswered.
- **Mention Iran accessibility** when a service needs a VPN (ChatGPT, Gemini,
  Claude). The audience will hit this immediately.
- **A prompt library / awesome-list is not a tool.** Do not post it as if the
  reader can click and use something. Either reframe it as an educational post
  ("why your AI images look amateur" → teach 3 principles → cite the library as
  a learning source) or skip it. Explain the analogy plainly: it is a cookbook,
  it does not cook.
- **Teach, don't just link.** For anything abstract, the post should leave the
  reader with a transferable principle, then the link as a resource. Add a
  closing question to invite comments.
- **Set expectations on hardware.** For giant open-weight models, state that
  local execution is not realistic and give the hosted free URL instead.

## Cron wiring

- Schedule in UTC: 09:00 Tehran = `30 5 * * *`
- `enabled_toolsets: ["terminal", "file", "web"]`
- Write the cron prompt in **English** (the validator blocks U+200C in Persian
  text) and instruct Persian output inside it
- Pin a model explicitly, or the job fails with "no model configured"
- End the prompt with: the FINAL RESPONSE is the delivered message; do not end
  with tool calls only
- Verify with `cronjob action=run` once after creating

## Slow-news-day fallbacks

In priority order: a flagship phone launch with real specs, a major software
feature release, a "hidden gem" repo from the past year, or one Hermes Agent
capability framed as something impressive the audience could set up themselves
(daily automated reports, image generation, cron scheduling, YouTube transcript
summaries).
