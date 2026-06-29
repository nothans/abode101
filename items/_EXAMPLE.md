---
type: item
name: Example Device (Model XYZ-123)
tags: [example]
category: appliance        # appliance | tool | fixture | device | system-part  (optional)
description: One-line description used by index.md and for relevance ranking
source: where this came from (manual file / URL+date / receipt / observation)
status: active   # active | needs-research | retired
---

# Example Device

One or two sentences: what it is, where it lives, what it's for. Exact facts go in the
Specs table; the optional sections (Parts, Error codes, History) accrue over time.
(Delete this file in your own copy; it's here as a format reference.)

## Specs
| Field | Value | Confidence | Source |
|---|---|---|---|
| Category | appliance | verified | observed |
| Manufacturer | <brand> | verified | model plate |
| Model / part no. | XYZ-123 | verified | manual ABC-001 p.1 |
| Serial no. | <serial> | verified | model-plate photo |
| Battery / consumable | <type/size> | verified | manual ABC-001 p.10 |
| Compatibility | <what it works with> | verified | manual ABC-001 p.2 |
| Location | [[some-area]] | verified | observed 2026-01-01 |
| Purchase date / price / seller | <from a receipt> | reported | receipt 2026-01-01 |
| Warranty | expires 2029-01-01 (3 yr parts) | reported | receipt / mfr terms |

- `Confidence`: verified · reported · inferred · unknown (see `AGENTS.md`).
- `Source`: always include a locator (page / URL+date / receipt / "observed <date>").
- **Serial no.** matters for warranty claims, recalls, and insurance/theft records.

## Parts (replacements & consumables)
What fits this device, with part numbers and a tagged buy-link (see the Amazon rule in `AGENTS.md`).

| Part | Part no. | Where to buy |
|---|---|---|
| <filter / belt / bulb / battery> | <part #> | `<amazon.com/...?tag=your-tag>` |

## Error codes
Codes the unit can show and what they mean. Pull these from the manual's troubleshooting table
so "the washer is flashing F21" becomes answerable.

| Code | Meaning | Fix | Source |
|---|---|---|---|
| E1 | <what it means> | <what to do> | manual ABC-001 p.12 |

## History
Running log of services, repairs, and part replacements, newest first. Feeds the schedule's
"last done".

- 2026-01-01, <what was done> (cost / who)

## Maintenance → [[schedule]]
- <consumable> replacement, interval <only if cited; else TODO>.
- Warranty expires <date>, surface as a reminder as it approaches.

## Links
- [[related-system-or-area]]
