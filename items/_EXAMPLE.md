---
type: item
name: Example Device (Model XYZ-123)
tags: [example, category]
description: One-line description used by index.md and for relevance ranking
source: where this came from (manual file / URL+date / receipt / observation)
status: active   # active | needs-research | retired
---

# Example Device

One or two sentences: what it is, where it lives, what it's for. Specs go in the table
below — that's what makes exact questions answerable. (Delete this file in your own copy;
it's here as a format reference.)

## Specs
| Field | Value | Confidence | Source |
|---|---|---|---|
| Model / part no. | XYZ-123 | verified | manual ABC-001 p.1 |
| Battery / consumable | <type/size> | verified | manual ABC-001 p.10 |
| Compatibility | <what it works with> | verified | manual ABC-001 p.2 |
| Installed in | [[some-area]] | verified | observed 2026-01-01 |
| Purchase date / price / seller | <from a receipt> | reported | receipt 2026-01-01 |

- `Confidence`: verified · reported · inferred · unknown (see `AGENTS.md`).
- `Source`: always include a locator (page / URL+date / receipt / "observed <date>").

## Where to buy (consumables)
- <part name> — <Amazon URL with the owner's affiliate tag> (see `AGENTS.md`).

## Maintenance → [[schedule]]
- <consumable> replacement — interval <only if cited; else TODO>.

## Links
- [[related-system-or-area]]
