---
type: playbook
title: ingest
description: Abode 101 playbook, ingest
status: stable
generated: { by: human:owner, at: 2026-08-26T12:00:00-04:00 }
---

# Playbook: ingest (any resource → knowledge)

**When:** there's something in `resource_intake/`, or Hans hands you a URL / forwards an
email / pastes a listing. Sources are heterogeneous by design, don't assume PDF.
**Goal:** convert any raw resource into citable facts in the right files, each fact carrying
its source and confidence (see "Exact facts & provenance" in `AGENTS.md`). Then clear intake.

## The pipeline (same for every resource)
1. **Identify the resource type** (table below) and how to read it.
2. **Read it** with the right tool.
3. **Identify the thing(s)** it documents → find or create the `items/` / `systems/` file.
4. **Register the source, then extract facts → Specs rows.** Add a `sources` entry to the
   file's frontmatter (`id`, `resource` path or URL, `title`, `author`, `last_modified` if the
   document states a revision date). Then, for each exact-fact field (manufacturer, model,
   serial, battery, filter, dimensions, compatibility, purchase date, price, warranty…), write
   a row with **value · confidence · `<source id>` + locator**. Set confidence by the
   resource's trust tier.
   Also pull, when the source has them: the **error-code / troubleshooting table** → the item's
   `## Error codes`; **replacement parts + part numbers** → `## Parts` (with tagged buy-links);
   and **warranty terms** → the `Warranty` Specs row.
5. **Keep the artifact** as a reference (leave in `resource_intake/` or move under
   `references/`) and add a `references/` index line pointing to the item.
6. **Link, log, index** (as in `capture.md`; the log verb is **Ingested**).
7. **Stamp trust:** set `generated` (you, now). Add a `verified` entry when the extracted
   values were checked against the artifact (a tier-1 manual read end to end counts; a
   listing does not). Set `stale_after` if the resource is perishable (a web page, a price,
   a listing): 90 days for prices/listings, up to a year for a manufacturer page.
8. **Resolve status:** flip `draft` → `stable` as exact fields fill; anything still
   `unknown`/ambiguous stays `TODO` and goes to `overnight-research.md` to confirm.

## Resource types & how to handle each
| Type | Examples | Read with | Trust tier | Pull (best-for) |
|---|---|---|---|---|
| Manual / spec sheet | install guide PDF, datasheet | `pdftotext -layout`, or web fetch | 1 (mfr) | model, battery, filter, dimensions, compatibility, intervals, **error codes**, **parts** |
| Manufacturer web page | product/support/spec page | WebFetch (record URL+date) | 1 | authoritative specs, firmware, official accessories |
| Authorized retailer page | Home Depot, Lowe's, brand store | WebFetch | 2 | price, what's-in-box, model confirmation |
| Marketplace listing | Amazon (esp. third-party), eBay | WebFetch / pasted text | 3 | purchase candidate, rough specs, **verify against tier 1/2** |
| Receipt / order confirmation | PDF, photo, forwarded email | pdftotext / read image / read email | 2 (purchase facts) | **purchase date, price, seller, qty, model**: the facts only a receipt has |
| Photo of label/plate | model plate, serial sticker, filter end-cap | read the image | 1–2 | serial no., model, filter size printed on the part |
| Note / observation | Hans says "the air filter is 16x25x1" | - | per Hans | facts Hans states directly; source = "Hans, observed <date>" |

Notes:
- **Receipts and listings are the purchase-fact source** (date/price/seller) that manuals lack,
  but for *specs*, a manual/mfr page outranks a listing. Use each for what it's authoritative on.
- A marketplace spec ("battery included: CR2032") is `reported`, not `verified`, until a tier‑1
  source confirms it. Conflicts: keep the higher tier, note the other, flag it.
- Always record a **locator**: manual page, URL **+ date fetched**, receipt, or photo filename.
  No locator → not `verified`.

## Worked example (the shape of a good ingest)
Drop a manual PDF into `resource_intake/` → identify the product → create
`items/<slug>.md` → extract the exact fields (model, battery, compatibility) as Specs
rows, each `verified` with a page citation (`manual p.10`, where `manual` is the
`sources[].id`) → keep the PDF as the reference → link, log, index → flip the item to
`stable`. A device's battery type, model number, and compatibility should now be
answerable with a source, straight from the manual.
