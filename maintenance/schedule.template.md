---
type: maintenance
name: Maintenance schedule
tags: [maintenance, reminders]
description: Master list of recurring house tasks — filters, batteries, seasonal
source: seeded from template
status: active
---

# Maintenance schedule

Copy this to `schedule.md` and fill it in. `next due = last done + interval`.

| Task | Where / item | Interval | Last done | Next due | Source |
|---|---|---|---|---|---|
| _e.g. HVAC air filter_ | [[hvac]] | <cited> | YYYY-MM-DD | (computed) | manual / mfr page |
| _e.g. smoke/heat alarm (whole unit)_ | [[safety]] | 10 years | YYYY-MM-DD | (computed) | mfr |
| _e.g. water/spa filter_ | [[some-item]] | TODO (confirm) | — | TODO | needs research |
| _e.g. appliance warranty expiry_ | [[some-item]] | one-time (expiry) | — | 2029-01-01 | receipt / mfr |

> Intervals marked `TODO` are not yet cited — confirm from a manual/manufacturer source
> before they become real reminders. Don't invent intervals.
> **Warranties** use an expiry date, not an interval — the `reminders` playbook flags them
> as they approach (default ~60 days out).
