# AGENTS.md, operating instructions for Abode 101

You are operating on **Abode 101**, a knowledge base about the owner's house. It is an
**OKF bundle** (Open Knowledge Format v0.2 / Karpathy "LLM Wiki"): plain-text Markdown,
one thing per file, links between files, an `index.md` as the map. The folder *is* the
database. Do not add a vector store or external DB, match retrieval to the file shape
(read `index.md`, follow links, open only what you need).

## The golden rule
**You maintain this knowledge base. The owner dumps raw material; you keep it organized.**
The piece the OKF spec leaves to the producer, the AI maintenance loop, is the whole point here.

## How to read (answering a question / chat)
1. Read `index.md` first. It is the navigation layer; do not load the whole folder.
2. Follow links to the specific `items/`, `systems/`, `areas/`, or `maintenance/`
   file(s) you need. Pull only those.
3. Answer with exact details and cite the file (and the source manual/URL inside it).
   If the answer isn't captured yet, say so, don't guess specs.
4. Check freshness: if the file's `stale_after` has passed, say the fact may be stale and
   flag it for re-verification (see "Freshness" below). Still answer; never silently drop it.

## How to write (capturing new info)
- **One thing per file.** A device/product → `items/<slug>.md`. A house system →
  `systems/<slug>.md`. A room/zone → `areas/<slug>.md`. A schedule → `maintenance/`.
- Use the frontmatter contract below. Link related files with `[[slug]]`.
- Every change gets a dated entry at the top of `log.md` (newest first, format below), this
  is the event stream the story view reads.
- Update `index.md` when you add a file.
- **Never fabricate specs** (battery type, model number, filter size, capacity).
  Only record what a source supports; cite it. Mark unknowns as `TODO` so the
  overnight loop can fill them.
- Stamp what you did: set `generated` on a new file, and add a `verified` entry when you
  (or the owner) actually confirmed the content against its sources. Use the actor
  convention below. Being honest about who checked what is how the base stays trustable.

## File contract (frontmatter)
OKF v0.2's trust families, with the house-specific keys on top. Only `type` is required by
the spec; everything else is what makes an answer trustable.

```yaml
---
type: item | system | area | maintenance | reference
name: Human-readable name
tags: [smart-home, lighting, ...]
category: appliance | tool | fixture | device | system-part   # items only, optional
description: one line, used by index.md and for relevance
status: stable | draft | deprecated        # draft = needs research; deprecated = retired, kept for history
generated: { by: <actor>, at: <ISO 8601 datetime with offset> }   # who wrote the current content, when
verified:                                  # who confirmed it against its sources; list, newest last
  - { by: <actor>, at: <ISO 8601 datetime with offset> }
stale_after: <ISO 8601 datetime with offset>   # optional; when perishable content should be re-checked
sources:                                   # what this file derives from; ids are cited in Specs rows
  - id: manual                             # short, readable, stable; the join key for citations
    resource: resource_intake/<file>.pdf   # a URL, a bundle-relative path, or a scope descriptor
    title: <human label>
    author: <actor, e.g. Lutron, or human:<owner>>
    last_modified: <ISO 8601, when the source itself last changed, if known>
---
```

- **Actors** (`generated.by`, `verified[].by`, `sources[].author`) use OKF's convention:
  `human:<id>` for a person (the owner's id is in `OWNER.local.md`), `process:<id>` for an
  automated loop (`process:overnight-research`), `<agent>/<version>` for an AI agent
  (`claude-code/opus-4`). Trust tier follows from it: no `verified` = unverified; only
  non-human verifiers = machine-confirmed; any `human:` verifier = human-reviewed.
- **`status`** is the document's lifecycle in OKF vocabulary. `stable` = ready to answer from;
  `draft` = incomplete, has `TODO`s, the overnight loop should work on it; `deprecated` = the
  thing is gone (sold, replaced, removed) but the file stays for history, warranty, and links.
  Never delete a replaced device's file; deprecate it and link the replacement.
- **Timestamps** in frontmatter are ISO 8601 with an explicit offset
  (`2026-07-25T21:00:00-04:00`). Plain dates are fine in body prose and tables.
- **`sources[].id`** is what the Specs table's Source column cites (see below). Keep ids short
  and readable (`manual`, `box-photo`, `receipt-2026-07-02`, `owner`), matched case-insensitively.
  For a prose claim, use a markdown footnote with the same label: `...per the manual.[^manual]`.
- `index.md` carries `okf_version: "0.2"` in its frontmatter (the only index frontmatter OKF permits).

Body: a **Specs** table (for items, see below), then prose facts, then a `## Links`
section of `[[slug]]` references. Items may also carry **`## Parts`** (replacements, part
numbers, tagged buy-links), **`## Error codes`** (the manual's troubleshooting table, so
"the washer is flashing F21" is answerable), **`## History`** (a dated log of services
and repairs, which feeds the schedule's "last done"), and, for consumables, **`## Stock`**
(quantity on hand with an as-of date and source, consumption per cycle, and the reorder
rule stated as data: reorder when stock minus the next cycle's use can't cover the cycle
after it). Add each when there's real content.

**Stock is the most perishable fact in the base**, it changes every time a task is done
and every time a box arrives. Keep it honest: a History line that installs a consumable
also decrements its Stock, and the day-after check-in ("done, and I used 2") is the
stock-update moment. An order task's due date is *derived* from stock and consumption,
not periodic, see `maintenance/schedule.template.md`.

**`not:` anti-definitions (optional).** When a fact is easy to confuse with a near-miss (the
old filter size, the previous model, the look-alike part that doesn't fit the mounting
plate), record the wrong answer explicitly so retrieval can warn instead of guess:

```yaml
not:
  - term: "16x25x1"
    why: "that is the 1-inch pleated size the old unit took; the 410 is a 4-inch media filter"
    instead: "AprilAire 410, 16x25x4 nominal"
```

## Exact facts & provenance (the trust model)
Some questions demand an *exact* answer ("what battery?", "what filter size?", "what
model?", "when did I buy it?"). For those, prose isn't enough, store **structured
facts, each with its own source and confidence**, so retrieval returns one unambiguous
value you can trust. This is the heart of the base; treat it like a chain of custody.
OKF's `sources` / `verified` / `stale_after` work at the file level; the Specs table
carries the same idea down to the individual fact.

**Exact-fact fields** (never approximate these): manufacturer, model / part number,
serial number, battery type, filter size / part, bulb base & wattage, dimensions, capacity,
voltage, compatibility, firmware/app, purchase date, price, seller, warranty term/expiry.

Record each as a row in the item's **Specs** table:

| Field | Value | Confidence | Source |
|---|---|---|---|
| Model | <model/part no.> | verified | manual p.1 |
| Battery | <battery type> | verified | manual p.10 |

- **Confidence:** `verified` (stated by an authoritative source, quote/locate it) ·
  `reported` (from a secondary source like a listing) · `inferred` (deduced, must be
  labeled, never presented as fact) · `unknown` (leave the row, value `TODO`).
- **Source:** a `sources[].id` from the frontmatter **plus a locator**: manual page, URL
  section (the entry carries the URL and retrieval date), receipt, photo, or "observed <date>".
  No locator → not `verified`.

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

## Freshness (staleness & re-verification)
The tiers above handle *disagreement*; `stale_after` handles *time*. A `verified` fact is
not permanent: durable facts stay verified until contradicted, perishable ones expire.

- **Durable** (no `stale_after`, or years out): what a manual states about a fixed product,
  model and part numbers, dimensions, battery type, filter size, install dates, serials.
- **Perishable** (`stale_after` 90 days to 1 year out): price, availability and buy-links,
  warranty status, firmware/app versions, "what would I buy today" guidance, anything whose
  only source is a web page. Set it when you write the file; the horizon is the field's, not
  the file's, so a file with one perishable section gets the earliest horizon.
- **Re-verify triggers:** the overnight loop re-checks a file when `now >= stale_after`, or
  when a fact is about to matter (a purchase, a safety item). On re-check, add a `verified`
  entry (`process:overnight-research`), push `stale_after` forward, and log it. If the source
  has changed, apply the conflict rule; never quietly overwrite.
- When answering from a file past its `stale_after`, say so ("last verified <date>, may be
  stale"). Durable rows in the same file are still fine to answer with.

## The loops (see `playbooks/`)
- `playbooks/capture.md`: turn a thing the owner bought/learned/found into clean files.
- `playbooks/ingest.md`: process `resource_intake/` (**any** resource: PDFs/manuals, web
  pages, retail/Amazon listings, receipts, order emails, photos of labels, notes) into
  items + references, mapping each fact to a Specs row with source + confidence.
- `playbooks/overnight-research.md`: the daily offline pass: research new purchases on
  the web, fill `TODO`s, re-verify stale files, propose maintenance reminders, recommend what to buy.
- `playbooks/reminders.md`: derive maintenance, battery, and warranty-expiry reminders from the corpus.

## The log (`log.md`)
OKF's log shape: one `## YYYY-MM-DD` heading per day, newest first, and under it one bullet
per event starting with a bold verb, sub-bullets for detail. Verbs in use: **Captured**
(new thing in the base), **Updated**, **Verified** (a re-check with no change), **Ingested**
(a resource processed), **Deprecated**, **Framework** (a change to the public scaffold, no
house data). Link the files touched.

```markdown
## 2026-07-25
- **Captured** the office desktop from a live system query → [`items/office-pc.md`](items/office-pc.md).
  - Open TODOs: PSU wattage, case clearance.
- **Verified** the 128GB max RAM against the Gigabyte + Intel spec pages.
```

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
This base must be trustworthy. Tag machine-added facts (`generated.by` / `verified[].by` as
a `process:` or `<agent>/<version>` actor) and cite sources. When the overnight loop adds
something from the web, add a `sources` entry with the URL and retrieval date, and set
`stale_after` if the fact is perishable.

## OKF conformance notes
Abode 101 is a conformant OKF v0.2 bundle (spec: github.com/GoogleCloudPlatform/open-knowledge-format).
Two deliberate extensions a strict consumer should know about: `[[slug]]` wiki-links (an
OKF consumer can rewrite `[[x]]` to `[x](/items/x.md)` and friends), and the per-row
Confidence/Source table, which is body content the spec does not define. Everything in the
frontmatter contract above is either spec-defined or a producer extension the spec tells
consumers to preserve. Concept documents (`items/`, `systems/`, `areas/`, `maintenance/`,
`references/`, `playbooks/`, `docs/`) all carry `type`; the repo scaffolding (`README.md`,
`AGENTS.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `OWNER.local.md`, `evals/`) is not part of the
bundle and a consumer should skip it.
