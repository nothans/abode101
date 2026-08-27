---
type: system
name: Example System (e.g. HVAC, Lighting, Plumbing, Safety)
tags: [example]
description: A house system, the table shape that makes "what size / what type?" answerable
status: stable
generated: { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
verified:
  - { by: human:owner, at: 2026-01-01T10:00:00-05:00 }
sources:
  - id: observed
    resource: "owner walkthrough, 2026-01-01"
    author: human:owner
  - id: manual
    resource: resource_intake/system-manual.pdf
    title: Installer / owner's manual
---

# Example System

A house system groups related facts and devices. When the useful answer is a lookup
("what vent size in the office?", "what bulb in the foyer?"), a **table keyed by
location** is the right shape, match the structure to the question (see `AGENTS.md`).

## Facts by location
| Location | Value | Confidence | Source |
|---|---|---|---|
| Room A | <size / type / model> | verified | observed 2026-01-01 |
| Room B | <size / type / model> | unknown, TODO | - |

## Devices
- [[example-device]]

## Links
- [[related-area]]
