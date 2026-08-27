---
type: maintenance
name: Maintenance schedule
tags: [maintenance, reminders]
description: Master list of recurring house tasks, filters, batteries, seasonal
status: stable
generated: { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
sources:
  - id: owner
    resource: "owner-stated dates and house rules"
    author: human:owner
---

# Maintenance schedule

Copy this to `schedule.md` and fill it in. `next due = last done + interval`.

| Task | Where / item | Interval | Last done | Next due | Source |
|---|---|---|---|---|---|
| _e.g. HVAC air filter_ | [[hvac]] | <cited> | YYYY-MM-DD | (computed) | manual / mfr page |
| _e.g. smoke/heat alarm (whole unit)_ | [[safety]] | 10 years | YYYY-MM-DD | (computed) | mfr |
| _e.g. water/spa filter_ | [[some-item]] | TODO (confirm) | - | TODO | needs research |
| _e.g. appliance warranty expiry_ | [[some-item]] | one-time (expiry) | - | 2029-01-01 | receipt / mfr |
| _e.g. order <consumable> (stock runs out after cycle N)_ | [[some-item]] | as needed (each cycle uses <n>) | stock: <n> on hand, YYYY-MM-DD | (derived from stock ÷ use) | owner / receipt |

> Intervals marked `TODO` are not yet cited, confirm from a manual/manufacturer source
> before they become real reminders. Don't invent intervals.
> **Warranties** use an expiry date, not an interval, the `reminders` playbook flags them
> as they approach (default ~60 days out).
> **Order tasks** (consumables) also aren't interval tasks: the due date is derived from
> the item's `## Stock` (on hand vs use per cycle), and moves when stock or usage changes.
> Give the order date lead time before the cycle that would run dry.
> The Source column cites the item's own `sources[].id` where the interval came from; the
> schedule file's own `sources` only covers owner-set house rules.
