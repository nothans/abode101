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
| Manual / spec sheet | install guide PDF, datasheet | `tools/pdf-text/pdf_text.py` (search, dump); a scan gets `tools/pdf-ocr/` first; or web fetch | 1 (mfr) | model, battery, filter, dimensions, compatibility, intervals, **error codes**, **parts** |
| Manufacturer web page | product/support/spec page | WebFetch (record URL+date) | 1 | authoritative specs, firmware, official accessories |
| Authorized retailer page | Home Depot, Lowe's, brand store | WebFetch | 2 | price, what's-in-box, model confirmation |
| Marketplace listing | Amazon (esp. third-party), eBay | WebFetch / pasted text | 3 | purchase candidate, rough specs, **verify against tier 1/2** |
| Receipt / order confirmation | PDF, photo, forwarded email | `tools/pdf-text/` / read image / read email | 2 (purchase facts) | **purchase date, price, seller, qty, model**: the facts only a receipt has |
| Photo of label/plate | model plate, serial sticker, filter end-cap | read the image | 1–2 | serial no., model, filter size printed on the part |
| Note / observation | Hans says "the air filter is 16x25x1" | - | per Hans | facts Hans states directly; source = "Hans, observed <date>" |

Notes:
- **Receipts and listings are the purchase-fact source** (date/price/seller) that manuals lack,
  but for *specs*, a manual/mfr page outranks a listing. Use each for what it's authoritative on.
- A marketplace spec ("battery included: CR2032") is `reported`, not `verified`, until a tier‑1
  source confirms it. Conflicts: keep the higher tier, note the other, flag it.
- Always record a **locator**: manual page, URL **+ date fetched**, receipt, or photo filename.
  No locator → not `verified`.

## Filing the artifact: where it goes, what it is called, what it carries inside
The artifact outlives the conversation that filed it, so the file itself has to say what it is.
Three rules, applied before the log entry is written.

**1. Where.** Out of `resource_intake/` and into `references/<slug>/`, the slug of the item or system it supports.
A set that belongs together (a listing's photos, a receipt's pages, a manual plus its addendum) gets a subfolder named for the set: `references/<slug>/listing-<site>-<id>/`.
The inbox is empty when the ingest is done.

**2. Name.** The file name says what the file is, in words, not what the source called it:
`manual-<maker>-<year>.pdf`, `install-guide-<part-no>-<yyyy-mm>.pdf`, `box-photo-<yyyy-mm-dd>.png`, `receipt-<seller>-<yyyy-mm-dd>.pdf`.
A photo set is numbered in a sensible walk (`01-full-view.jpg`, `02-playfield-from-above.jpg`, ..., `13-backbox-boards.jpg`), two digits, then a short description, all lowercase with hyphens.
The original name never disappears: it goes into the file's comment field and the reference doc, so a copy found elsewhere can be matched.
Never rename the owner's original in his own folders; copy it in, and say where the original lives.

**3. Embedded metadata.** Every filed artifact carries the same seven fields, written with the bundle's `tools/artifact-meta/artifact_meta.py` so the mapping per format is consistent:

| Field | What to write | JPEG | PNG | PDF | MP4 / M4A / MOV | MP3 |
|---|---|---|---|---|---|---|
| title | one line, what this file is (`<item> listing photo 13: backbox boards`) | XPTitle | Title | Title | title | title |
| description | what is in it and what it proves, one to three sentences, plain ASCII if possible | ImageDescription, UserComment | Description | Subject | description | comment |
| subject | the thing it documents (`AprilAire 410 air filter, box label`) | XPSubject | Subject | (joined into Subject) | show | album |
| keywords | semicolon list: the item, the maker, the kind of artifact, the notable content | XPKeywords | Keywords | Keywords | keywords | (joined into comment) |
| author | who made the artifact: `human:<owner>`, the manufacturer, `seller, <marketplace> ad <id>`, `<maker> via human:<owner>` | Artist | Author | Author | artist | artist |
| comment | `Original file: <name>.` plus the source URL if there is one and the filing date | XPComment | Comment | (joined into Keywords) | comment | comment |
| date | the date the artifact was made, if known, only where the file has none | DateTimeOriginal | Creation Time | CreationDate | date | date |

Content is never re-encoded: EXIF is inserted, PNG chunks are added, the PDF info block is appended incrementally, audio and video are stream-copied with the tags.
A scanned PDF with no text layer gets one first (the bundle's `tools/pdf-ocr/`) so it is searchable, then its metadata.
For an MP4 or MP3 that is itself the knowledge (a recorded walkthrough, a service call), the same seven fields apply, `subject` becomes the show or album name, and the description says who is speaking and what is covered.
Check the result with `artifact_meta.py show <file>`; the reference doc's file table should read the same as the file's own title and description.

**Then the reference doc.** One Markdown file beside the folders, `references/<slug>-<what>.md` with `type: reference` frontmatter: what the set is, how it was made usable (OCR, page map), what it proves, and a table of the files with their descriptions.
Cite it from the item's `sources` and list it in the root `index.md` under References.

## Worked example (the shape of a good ingest)
Drop a manual PDF into `resource_intake/` → identify the product → create
`items/<slug>.md` → extract the exact fields (model, battery, compatibility) as Specs
rows, each `verified` with a page citation (`manual p.10`, where `manual` is the
`sources[].id`) → keep the PDF as the reference → link, log, index → flip the item to
`stable`. A device's battery type, model number, and compatibility should now be
answerable with a source, straight from the manual.
