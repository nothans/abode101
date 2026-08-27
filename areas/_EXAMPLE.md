---
type: area
name: Example Room (e.g. Kitchen, Garage, Primary Bath)
tags: [example, first-floor]
description: One room/zone, what's installed here and area-specific notes
status: stable
generated: { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
sources:
  - id: observed
    resource: "owner walkthrough, 2026-01-01"
    author: human:owner
  - id: can-label
    resource: resource_intake/paint-can-2026-01-01.jpg
    title: Paint can label photo
---

# Example Room

A room or zone. List what lives here (link `[[item]]`s and `[[system]]`s) and any
area-specific facts you'd want at hand. Create an area file on the first real fact,
don't pre-make empties. (Delete this example in your own copy.)

## What's here
- [[example-device]], what it is, where exactly
- Bulbs: see [[lighting]] for this room's base/type
- Vent: see [[hvac]] for this room's size

## Area notes
| Fact | Value | Confidence | Source |
|---|---|---|---|
| Paint color / sheen | <brand + code> | verified | can-label |
| Dimensions | <W×L> | reported | observed, measured 2026-01-01 |
| Flooring | <type> | reported | observed |

## Links
- [[related-system]]
