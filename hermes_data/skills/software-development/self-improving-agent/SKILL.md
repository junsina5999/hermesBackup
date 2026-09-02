---
name: self-improving-agent
description: "Use when user corrects agent or tool fails to log learnings."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [self-learning, error-logging, continuous-improvement]
---

# Self-Improving Agent Skill

Use this skill to log learnings, command/tool errors, and user corrections so Hermes continuously learns and improves during session work.

## Trigger Conditions
- A command, script, or tool fails unexpectedly.
- The user corrects Hermes ("No, that's wrong...", "Actually, do it this way...").
- An API key or external service responds with an error.

## Actions
When errors occur or corrections are given, log them to `.learnings/LEARNINGS.md` or `.learnings/ERRORS.md`.
