# Scaffold ideas — what to capture & where it goes

Abode 101 starts minimal on purpose. Grow it as real facts arrive. This is a menu of
what's worth capturing and which folder it belongs in — not a required structure.

## A capture checklist (high-value, low-effort)
Things that pay off the first time you're at the store or on the phone with a tech:
- **Bulbs** — base/type, count, color temp, dimmable, per fixture → `systems/lighting.md`
- **Filters** — HVAC, fridge, water, range hood, vacuum: exact size/part + interval → item + `maintenance/`
- **Batteries** — what each remote/sensor/lock/thermostat takes → on each item's Specs row
- **Vent/register sizes** — per room, for covers → `systems/hvac.md`
- **Life-safety** — smoke/CO/heat alarms: model + manufacture date (10-yr clock) → `systems/safety.md`
- **Paint** — brand, color code, sheen, per room → the room's `areas/` file
- **Model & serial** — appliances, HVAC, water heater: photograph the plate → item Specs (serial matters for warranty/insurance)
- **Warranties & receipts** — purchase date, price, seller, expiry → item Specs + `references/`
- **Error codes** — the appliance's troubleshooting codes (washer F21, furnace lockout) → item `## Error codes`
- **Replacement parts** — what filter/belt/bulb/battery fits, with part numbers → item `## Parts`
- **Service contacts** — who to call, account #, last visit → on the relevant system/item
- **Hardware specs** — garage springs (color/weight), door/lock keyways, fasteners → `systems/`

## Folders you might add (create on first real fact)
- `systems/plumbing.md`, `systems/electrical.md`, `systems/networking.md`, `systems/exterior.md`
- `systems/appliances.md` or an `items/` file per appliance (with model/serial/warranty)
- `references/warranties/` for warranty PDFs
- `contacts.md` or `systems/vendors.md` — a contractor/vendor rolodex
- `areas/<room>.md` per room as you map the house

## Extension ideas (the roadmap, once the base earns it)
- **Overnight automation** — run `playbooks/overnight-research.md` on a schedule; commit results.
- **Reminders out** — surface `maintenance/` due-items to a calendar / notifications / a daily digest.
- **Photo intake** — snap a model plate or receipt into `resource_intake/`; ingest reads the label.
- **A read-only app** — a static site over the folder: a "story" view from `log.md`, item/area
  browse, a "what's due" page, buy-links. The folder stays the source of truth; the app just renders it.
- **Seasonal playbook** — a spring/fall checklist generated from what you own.

## Principles to keep (don't drift)
- One concept per file; link liberally; `index.md` is the map an agent reads first.
- Exact facts get a **Specs row with a cited source** — never approximate (see `AGENTS.md`).
- Don't invent intervals or specs; `TODO` is better than a confident wrong answer.
- Match the file's shape to the question: a lookup table for "what size/type?", an item file
  for a device, a schedule for "what's due?".
