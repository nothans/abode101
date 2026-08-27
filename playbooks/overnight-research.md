---
type: playbook
title: overnight-research
description: Abode 101 playbook, overnight-research
status: stable
generated: { by: human:owner, at: 2026-08-26T12:00:00-04:00 }
---

# Playbook: overnight-research (the daily offline pass)

**When:** nightly (eventually a scheduled cloud routine; for now, run on demand).
**Goal:** augment the day's additions and keep the base from going stale, the AI
maintenance loop OKF leaves to the producer. Offline-friendly: queue web lookups, run
them, write back. Act as `process:overnight-research` in every stamp you leave.

## Steps
1. **Find tonight's work.** Three queues:
   - **Deltas:** recent `log.md` entries and anything with `status: draft` or `TODO`s.
   - **Stale:** every file whose `stale_after` has passed (`now >= stale_after`).
   - **High-stakes:** a fact about to matter (a purchase the owner mentioned, a safety item
     with a due date inside 60 days), even if not yet stale.
2. **Web-augment each delta.** For new purchases / unresolved `TODO`s, research the web:
   - Confirm model/spec details (battery part + life, filter size + part number, bulb
     base/wattage, firmware/app, pairing steps).
   - Find the official manual/spec page; add it as a `sources` entry with the URL, a title,
     and `last_modified` if the page states one. Cite its `id` in the Specs rows you fill.
   - **Verify before writing.** Prefer manufacturer sources. If sources conflict or
     it's a guess, leave `TODO` and note the conflict, don't launder a guess as fact.
3. **Re-verify each stale file.** Re-fetch its web sources and compare against the recorded
   values. Unchanged: append `verified: { by: process:overnight-research, at: <now> }`, push
   `stale_after` forward by the field's horizon, log a **Verified** bullet. Changed: apply the
   conflict rule in `AGENTS.md` (higher tier wins, note the other, flag it), update
   `generated`, log an **Updated** bullet with what moved.
4. **Derive maintenance.** If an item has a consumable (filter, battery, water, blade),
   add/confirm a row in `maintenance/schedule.md` with the cited interval.
5. **Recommend.** Where useful, note what to buy (replacement filter/battery, compatible
   accessory) with a tagged link, as a suggestion, flagged, not an auto-action. Buy-links
   are perishable: set `stale_after` about 90 days out.
6. **Write back + log.** Update files, flip `draft` → `stable` when resolved, and append
   one `log.md` entry for the night under today's date, one bullet per file touched.

## Guardrails
- Cite every web-added fact (a `sources` entry with URL + retrieval date). Machine-added
  content is stamped with the process actor, never with the owner's `human:` id.
- Recommendations and reminders are proposals for the owner to accept, never silent.
- No fabrication. `TODO` is always better than a confident wrong spec.
- Re-verification never downgrades a human-reviewed fact on its own: if the loop disagrees
  with something the owner verified, flag it for the owner instead of overwriting.
