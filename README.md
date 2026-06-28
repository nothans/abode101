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
