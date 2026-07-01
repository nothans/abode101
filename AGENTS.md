# AGENTS.md, operating instructions for Abode 101

You are operating on **Abode 101**, a knowledge base about Hans's house. It is an
**OKF-style folder** (Open Knowledge Format / Karpathy "LLM Wiki"): plain-text
Markdown, one thing per file, links between files, an `index.md` as the map. The
folder *is* the database. Do not add a vector store or external DB, match
retrieval to the file shape (read `index.md`, follow links, open only what you need).

## The golden rule
**You maintain this knowledge base. Hans dumps raw material; you keep it organized.**
The piece Google's OKF spec dropped, the AI maintenance loop, is the whole point here.

## How to read (answering a question / chat)
1. Read `index.md` first. It is the navigation layer; do not load the whole folder.
2. Follow links to the specific `items/`, `systems/`, `areas/`, or `maintenance/`
   file(s) you need. Pull only those.
3. Answer with exact details and cite the file (and the source manual/URL inside it).
   If the answer isn't captured yet, say so, don't guess specs.

## How to write (capturing new info)
- **One thing per file.** A device/product → `items/<slug>.md`. A house system →
  `systems/<slug>.md`. A room/zone → `areas/<slug>.md`. A schedule → `maintenance/`.
- Use the frontmatter contract below. Link related files with `[[slug]]`.
- Every change gets a dated line at the top of `log.md` (newest first), this is
  the event stream the story view reads.
- Update `index.md` when you add a file.
- **Never fabricate specs** (battery type, model number, filter size, capacity).
  Only record what a source supports; cite it. Mark unknowns as `TODO` so the
  overnight loop can fill them.

## File contract (frontmatter)
```yaml
---
type: item | system | area | maintenance | reference
name: Human-readable name
tags: [smart-home, lighting, ...]
category: appliance | tool | fixture | device | system-part   # items only, optional
description: one line, used by index.md and for relevance
source: where this came from (manual file, URL, receipt, observation) + date
status: active | needs-research | retired
---
```
Body: a **Specs** table (for items, see below), then prose facts, then a `## Links`
section of `[[slug]]` references. Items may also carry **`## Parts`** (replacements, part
numbers, tagged buy-links), **`## Error codes`** (the manual's troubleshooting table, so
"the washer is flashing F21" is answerable), and **`## History`** (a dated log of services
and repairs, which feeds the schedule's "last done"). Add each when there's real content.

## Exact facts & provenance (the trust model)
Some questions demand an *exact* answer ("what battery?", "what filter size?", "what
model?", "when did I buy it?"). For those, prose isn't enough, store **structured
facts, each with its own source and confidence**, so retrieval returns one unambiguous
value you can trust. This is the heart of the base; treat it like a chain of custody.

**Exact-fact fields** (never approximate these): manufacturer, model / part number,
serial number, battery type, filter size / part, bulb base & wattage, dimensions, capacity,
voltage, compatibility, firmware/app, purchase date, price, seller, warranty term/expiry.

Record each as a row in the item's **Specs** table:

| Field | Value | Confidence | Source |
|---|---|---|---|
| Model | <model/part no.> | verified | manual <part no.> p.<n> |
| Battery | <battery type> | verified | manual <part no.> p.<n> |

- **Confidence:** `verified` (stated by an authoritative source, quote/locate it) ·
  `reported` (from a secondary source like a listing) · `inferred` (deduced, must be
  labeled, never presented as fact) · `unknown` (leave the row, value `TODO`).
- **Source:** the resource + a locator, manual page, URL **+ retrieval date**, receipt,
  photo, or "Hans, observed <date>". No locator → not `verified`.

**Source trust tiers** (higher wins on conflict):
1. Manufacturer manual / spec sheet / official product spec page
2. Authorized retailer / official store listing
3. Marketplace listing (e.g. Amazon third-party), customer reviews
4. Community / forum
5. Inference or model memory, **never** authoritative on its own

**Conflict rule:** if sources disagree, keep the higher-tier value, record the other in
a note, and flag it. Never silently overwrite a `verified` fact with a lower-tier one.
For an exact-fact field, only `verified`/`reported` values are answerable; an `inferred`
value must be labeled as such when you answer, and `unknown` stays `TODO`.

**Known edge: staleness & re-verification.** The tiers above handle *disagreement*, not *time*.
A `verified` fact is not expired on a timer yet, so it stays verified until a higher-tier source
contradicts it. That is fine for durable specs (a manual's filter size does not change) but
weaker for perishable facts (price, firmware, anything URL-sourced, which is why web facts carry
a retrieval date). Roadmap: confidence that decays with age, plus a re-verify trigger when a fact
is old or about to be used for something that matters. Until then, re-run `overnight-research` on
old `reported` / web facts rather than trusting them indefinitely.

## The loops (see `playbooks/`)
- `playbooks/capture.md`: turn a thing Hans bought/learned/found into clean files.
- `playbooks/ingest.md`: process `resource_intake/` (**any** resource: PDFs/manuals, web
  pages, retail/Amazon listings, receipts, order emails, photos of labels, notes) into
  items + references, mapping each fact to a Specs row with source + confidence.
- `playbooks/overnight-research.md`: the daily offline pass: research new purchases on
  the web, fill `TODO`s, propose maintenance reminders, recommend what to buy.
- `playbooks/reminders.md`: derive maintenance, battery, and warranty-expiry reminders from the corpus.

## Amazon links (affiliate, always)
**Every Amazon URL shown to the owner or stored in this base must carry the owner's
Amazon Associates tag.** The tag lives in `OWNER.local.md` (gitignored) as
`tag=<your-tag>`.
- Full URLs (`amazon.com/.../dp/<ASIN>`, `/gp/product/<ASIN>`): ensure `tag=<your-tag>`
  is present in the query string; if a different `tag=` is there, replace it.
  Example: `https://www.amazon.com/gp/product/<ASIN>?tag=<your-tag>`
- `amzn.to` short links the owner created already encode the tag, preserve them as-is,
  don't try to rewrite them.
- When you *recommend* a product (overnight loop / reminders), build the link as a full
  `amazon.com` URL with the owner's tag. Never show a bare, untagged Amazon link.

## Provenance
This base must be trustworthy. Tag machine-added facts and cite sources. When the
overnight loop adds something from the web, record the URL and date in `source:`.
