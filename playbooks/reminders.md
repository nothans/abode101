# Playbook: reminders

**When:** on demand, and as part of the overnight pass.
**Goal:** tell Hans what house tasks are due or coming up — filters, batteries, seasonal.

## Steps
1. **Read** `maintenance/schedule.md` and scan `items/` for consumables with intervals.
2. **Compute due dates:** `next due = last done + interval`. Flag overdue and due-soon
   (within ~2 weeks).
3. **Report** newest/most-urgent first: task, where, due date, the item to buy if any.
4. **On completion:** when Hans says a task is done, update `last done`, recompute
   `next due`, and log it.

## Output shape
- **Overdue:** … (link item)
- **Due soon:** … (link item)
- **Buy now:** replacement parts for the above, with links.

## Notes
- Only remind on intervals that have a cited source. An uncited interval is a `TODO`,
  not a reminder.
- Later: these can fan out to real notifications / calendar; for now it's a report.
