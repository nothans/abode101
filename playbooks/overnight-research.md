# Playbook: overnight-research (the daily offline pass)

**When:** nightly (eventually a scheduled cloud routine; for now, run on demand).
**Goal:** augment the day's additions and keep the base from going stale — the AI
maintenance loop OKF left out. Offline-friendly: queue web lookups, run them, write back.

## Steps
1. **Find today's deltas.** Read the recent `log.md` entries and anything with
   `status: needs-research` or `TODO`s.
2. **Web-augment each.** For new purchases / unresolved `TODO`s, research the web:
   - Confirm model/spec details (battery part + life, filter size + part number, bulb
     base/wattage, firmware/app, pairing steps).
   - Find the official manual/spec page; record the **URL + date** in `source:`.
   - **Verify before writing.** Prefer manufacturer sources. If sources conflict or
     it's a guess, leave `TODO` and note the conflict — don't launder a guess as fact.
3. **Derive maintenance.** If an item has a consumable (filter, battery, water, blade),
   add/confirm a row in `maintenance/schedule.md` with the cited interval.
4. **Recommend.** Where useful, note what to buy (replacement filter/battery, compatible
   accessory) with a link — as a suggestion, flagged, not an auto-action.
5. **Write back + log.** Update files, flip `needs-research` → `active` when resolved,
   and append a single `log.md` summary of what the loop did tonight.

## Guardrails
- Cite every web-added fact (URL + date). Tag machine-added content as such.
- Recommendations and reminders are proposals for Hans to accept — never silent.
- No fabrication. `TODO` is always better than a confident wrong spec.
