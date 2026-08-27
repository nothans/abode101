---
type: playbook
title: capture
description: Abode 101 playbook, capture
status: stable
generated: { by: human:owner, at: 2026-08-26T12:00:00-04:00 }
---

# Playbook: capture

**When:** Hans says "I bought X", "I learned X about the house", or "remember that X".
**Goal:** turn one thing into clean, linked files. Fast, lossless, no fabrication.

## Steps
1. **Classify** the thing: device/appliance/fixture/tool → `items/`; a house system →
   `systems/`; a room → `areas/`; a recurring task → `maintenance/`.
2. **Create or update** the file with the frontmatter contract (see `AGENTS.md`).
   - Record only what Hans told you / what a source supports. Everything unknown → `TODO`.
   - If it's a purchase, capture: what, model/brand if known, where installed, date, cost/source.
   - Stamp it: `generated: { by: <you>, at: <now> }`; add a `sources` entry for what Hans
     said (`id: owner`, resource "Hans, stated <date>") or the artifact he handed over; add a
     `verified` entry only if the content was actually checked against a source.
3. **Link** it: add `[[slug]]` links to related files (the area it's in, the system it's part of).
4. **Log** it: add a **Captured** bullet under today's `## YYYY-MM-DD` heading at the top of `log.md`.
5. **Index** it: add/refresh its line in `index.md`.
6. **Flag for the loop:** if there are `TODO`s or it's a new purchase, set
   `status: draft` so `overnight-research.md` picks it up. If anything perishable went in
   (price, buy-link, web-sourced fact), set `stale_after`.

## Don't
- Don't invent specs (battery, model, filter size, intervals). Leave `TODO`, cite when filled.
- Don't create empty area/system files speculatively, create on first real fact.
