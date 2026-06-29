# Playbook: reminders

**When:** on demand, and as part of the overnight pass.
**Goal:** tell Hans what's due or coming up — maintenance (filters, batteries, seasonal),
**warranties about to expire**, and life-safety whole-unit replacements.

## Steps
1. **Gather** from `maintenance/schedule.md` and by scanning `items/`:
   - consumables with a cited interval,
   - `Warranty` Specs rows with an expiry date,
   - whole-unit replace deadlines (alarms).
2. **Compute dates:** `next due = last done + interval`; for warranties use the expiry date.
   Flag **overdue** and **due-soon** (within ~2 weeks for tasks, within ~60 days for warranties).
3. **Report** newest / most-urgent first: task, where, date, and the part to buy if any.
4. **On completion:** when Hans says a task is done, update `last done`, recompute `next due`,
   **append a dated line to that item's `## History`**, and log it.

## Output shape
- **Overdue:** … (link item)
- **Due soon:** … (link item)
- **Warranty expiring:** <item> — expires <date> (extend, replace, or note the serial no. for a claim)
- **Buy now:** replacement parts for the above, with tagged links (see `AGENTS.md`).

## Notes
- Only remind on intervals / expiries that have a cited source. An uncited interval is a `TODO`,
  not a reminder.
- Later: these can fan out to real notifications / calendar; for now it's a report.
