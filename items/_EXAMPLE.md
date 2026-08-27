---
type: item
name: Example Device (Model XYZ-123)
tags: [example]
category: appliance        # appliance | tool | fixture | device | system-part  (optional)
description: One-line description used by index.md and for relevance ranking
status: stable             # stable | draft (has TODOs) | deprecated (gone, kept for history)
generated: { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
verified:
  - { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
stale_after: 2027-01-01T00:00:00-05:00     # earliest perishable fact below (price / buy-link)
sources:
  - id: manual
    resource: resource_intake/ABC-001-manual.pdf
    title: Example Device owner's manual (ABC-001)
    author: Example Corp
  - id: plate-photo
    resource: resource_intake/xyz-123-plate.jpg
    title: Model-plate photo
    author: human:owner
  - id: receipt
    resource: resource_intake/receipt-2026-01-01.pdf
    title: Purchase receipt
    last_modified: 2026-01-01T00:00:00-05:00
not:
  - term: "XYZ-120"
    why: "the previous generation; same look, different filter"
    instead: "XYZ-123"
---

# Example Device

One or two sentences: what it is, where it lives, what it's for. Exact facts go in the
Specs table; the optional sections (Parts, Stock, Error codes, History) accrue over time.
(Delete this file in your own copy; it's here as a format reference.)

## Specs
| Field | Value | Confidence | Source |
|---|---|---|---|
| Category | appliance | verified | observed 2026-01-01 |
| Manufacturer | <brand> | verified | plate-photo |
| Model / part no. | XYZ-123 | verified | manual p.1 |
| Serial no. | <serial> | verified | plate-photo |
| Battery / consumable | <type/size> | verified | manual p.10 |
| Compatibility | <what it works with> | verified | manual p.2 |
| Location | [[some-area]] | verified | observed 2026-01-01 |
| Purchase date / price / seller | <from a receipt> | reported | receipt |
| Warranty | expires 2029-01-01 (3 yr parts) | reported | receipt / mfr terms |

- `Confidence`: verified · reported · inferred · unknown (see `AGENTS.md`).
- `Source`: a `sources[].id` from the frontmatter plus a locator (page / section / "observed <date>").
- **Serial no.** matters for warranty claims, recalls, and insurance/theft records.

## Parts (replacements & consumables)
What fits this device, with part numbers and a tagged buy-link (see the Amazon rule in `AGENTS.md`).
Buy-links and prices are perishable; they set the file's `stale_after`.

| Part | Part no. | Where to buy |
|---|---|---|
| <filter / belt / bulb / battery> | <part #> | `<amazon.com/...?tag=your-tag>` |

## Stock (consumables only)
How many are on hand, how fast they go, and when to reorder. Installing one (a `## History`
line) decrements this; the reminders playbook derives the order reminder from it.

- **On hand:** <n> as of <YYYY-MM-DD> (source: owner / receipt / order email)
- **Used per cycle:** <n> (e.g. one per system per change)
- **Reorder when:** on hand, minus the next cycle's use, is less than the cycle after
  that needs. Order task goes in [[schedule]] with a derived date, not an interval.

## Error codes
Codes the unit can show and what they mean. Pull these from the manual's troubleshooting table
so "the washer is flashing F21" becomes answerable.

| Code | Meaning | Fix | Source |
|---|---|---|---|
| E1 | <what it means> | <what to do> | manual p.12 |

## History
Running log of services, repairs, and part replacements, newest first. Feeds the schedule's
"last done".

- 2026-01-01, <what was done> (cost / who)

## Maintenance → [[schedule]]
- <consumable> replacement, interval <only if cited; else TODO>.
- Warranty expires <date>, surface as a reminder as it approaches.

## Links
- [[related-system-or-area]]
