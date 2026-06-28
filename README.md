# Abode 101

A knowledge base for your house. Capture what you buy, learn, or discover about your
home; chat with it for exact details ("what's the battery for the dimmer?"); let an
overnight loop research new purchases and surface maintenance reminders.

> **This repo is the framework, not anyone's house.** The structure, the agent contract,
> and the playbooks are public and reusable. Your actual house data (items, systems,
> schedules, logs, manuals) is **gitignored** and stays on your machine — see
> [`.gitignore`](.gitignore). Fork it and fill it with your own home.

## The shape
Abode 101 is an **OKF folder** (Open Knowledge Format / Karpathy "LLM Wiki" style) —
plain Markdown, one thing per file, an `index.md` map, and an AI that *maintains* it. No
app and no database: the front end is chat (any LLM / agent CLI), the storage is this
folder. A friendly read-only app over the folder can come later.

Read [`AGENTS.md`](AGENTS.md) for how an agent reads and writes this base — including the
**exact-facts & provenance model** that makes answers trustworthy, and the Amazon
affiliate-link rule.

## Background: the OKF / LLM-wiki pattern
Abode 101 is a home-specific take on a pattern that emerged in 2026:

- **Andrej Karpathy's "LLM wiki"** (April 2026) — instead of RAG over chunked documents,
  keep a folder of Markdown the LLM itself writes and maintains (`raw/` sources, a `wiki/`
  of generated interlinked pages, a schema file). Connections are built once at write time,
  not re-derived per query. → [the original gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- **Google Cloud's Open Knowledge Format (OKF)** (v0.1, June 12 2026) — a vendor-neutral
  spec that formalizes the pattern: a directory of UTF-8 Markdown files, each a single
  concept with YAML frontmatter (only `type` is required; `title`/`description`/`tags`/
  `timestamp` optional), readable by humans and any agent with no database or SDK.
  → [OKF SPEC.md](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
  · [Google Cloud blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

**How Abode 101 relates.** It follows the OKF shape (one concept per file, frontmatter, an
`index.md`, links) and Karpathy's "the AI maintains it" loop — and adds the two things the
bare format leaves out:
1. **The maintenance loop** (`playbooks/`) — capture, ingest from *any* source, an overnight
   web-research pass, and reminders. OKF standardizes the *files*; the playbooks keep them *fresh*.
2. **A provenance & trust model** (`AGENTS.md`) — every exact fact carries a source and a
   confidence tier, so the base answers "what battery?" with a citation and **refuses to
   guess**. Home facts have to be right.

Abode 101's frontmatter is OKF-aligned (`type` + `description` + `tags`) and extends it with
`source` and `status` for provenance. See [`docs/`](docs/) for scaffold ideas and example prompts.

## Layout
| Path | What's in it | Tracked? |
|---|---|---|
| `AGENTS.md` | The contract: how to read/write, the trust model, link rules | ✅ public |
| `playbooks/` | Procedures: capture, ingest (any source), overnight-research, reminders | ✅ public |
| `areas/` `systems/` `items/` | Your house, one thing per file (`_EXAMPLE.md` shows the format) | examples only |
| `maintenance/` | Filter/battery/seasonal schedule (`schedule.template.md` to start) | template only |
| `references/` | Manuals, spec sheets, links, warranties | README only |
| `resource_intake/` | Raw inbox — drop PDFs/photos/receipts; `ingest.md` files them | README only |
| `index.md` / `log.md` | Your live map + event stream (start from the `*.template.md`) | gitignored |

## Quick start
1. Fork / clone. Copy `index.template.md` → `index.md` and `log.template.md` → `log.md`.
2. Create `OWNER.local.md` with your name and Amazon Associates tag (gitignored).
3. Drop a manual/receipt/photo into `resource_intake/`, or just tell your agent "I bought X".
4. Run the `playbooks/` — point your LLM at `AGENTS.md` and ask it to capture/ingest.
5. Ask your house things: *"what filter does the fridge take?"*, *"what's due this month?"*

## Why a folder, not a database
One concept per file, links between files, an index the model reads first. Connections
are built once at capture time, not re-derived per query. It's portable, diffable, model-
agnostic, and you own it. See `AGENTS.md` for the data contract.
