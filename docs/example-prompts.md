# Example prompts — how to use the base

Point an LLM/agent at the folder (it reads `AGENTS.md` + `index.md` first), then talk to
your house. These show the *shape* of good behavior — exact answers with a source, honest
refusals, ranges, and tagged buy-links. (Values below are placeholders; your real base
answers from your own files.)

## Exact-fact lookup
> **You:** What's the battery for the entry dimmer?
> **Base:** `<battery type>` — per the manual (`items/<dimmer>.md`, manual p.10). Cited, exact.

> **You:** What vent size is the office?
> **Base:** `4×10`. [`systems/hvac.md`]

## Honest refusal (the guardrail)
> **You:** What size is the kitchen toe-kick vent?
> **Base:** Not recorded — it's marked `TODO` (needs measuring). I won't guess. [`systems/hvac.md`]

> **You:** What's my fridge's model number?
> **Base:** That's not captured yet. Drop a photo of the model plate in `resource_intake/`
> and I'll add it.

## Range / derived
> **You:** How old is the water heater?
> **Base:** Installed `<date>`, so about `<N>` years. [`items/<heater>.md`]

> **You:** What maintenance is coming up?
> **Base:** From `maintenance/schedule.md`: `<item>` (`<interval>`), … Intervals still marked
> `TODO` aren't shown as due until confirmed from a source.

## Capture (write path)
> **You:** I just bought a `<product>`, model `<X>`. It's in the `<room>`.
> **Base:** Filed `items/<slug>.md` (Specs: model `<X>`, installed `<room>`), linked it,
> logged it, and flagged it for the overnight loop to fill specs + a reminder.

## Buy-link (affiliate policy)
> **You:** Where do I buy the replacement filter?
> **Base:** `<part>` — `<amazon link carrying the owner's affiliate tag>`. (Existing short
> links are preserved as-is.)

## Ingest from any source
Drop a manual PDF, a receipt photo, or an Amazon listing into `resource_intake/` and say
"ingest this." The base extracts the exact fields (model, battery, filter, price, date),
cites each, keeps the artifact as a reference, and updates the schedule.
