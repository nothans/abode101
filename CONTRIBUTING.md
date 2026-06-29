# Contributing to Abode 101

Abode 101 is a **framework** for a house knowledge base, the structure, the agent contract,
and the playbooks. The house data is yours and stays local; what's shared here is the pattern.

## Good contributions
- **Playbook improvements**: sharper capture/ingest/research/reminders procedures.
- **New resource types** for `playbooks/ingest.md` (e.g. a better receipt or label-photo flow).
- **Templates & examples**: `_EXAMPLE.md` files that show a clean way to model something
  (appliances, vehicles, networking, paint, warranties).
- **Eval cases**: generic cases in `evals/cases.example.yaml` that test exact-answer and
  refuse-to-guess behavior.
- **Docs**: clearer `docs/ideas.md` capture ideas or `docs/example-prompts.md` patterns.

## Ground rules (keep the spirit)
- **The folder is the database.** No vector store, no external DB, match retrieval to the
  file shape (see [`AGENTS.md`](AGENTS.md)).
- **One concept per file**, frontmatter contract, `[[slug]]` links, `index.md` as the map.
- **No fabricated facts.** Exact facts carry a cited source and a confidence tier; `TODO`
  beats a confident wrong answer. This is the whole point, don't weaken it.
- **Never commit real house data.** Personal content lives in gitignored paths; only the
  framework (README, AGENTS, playbooks, `_EXAMPLE`/`*.template`, docs, eval harness) is tracked.
  If you add a framework file, whitelist it in `.gitignore`.

## How
Fork, branch, PR. Keep changes small and focused. For a new framework file, explain in the PR
why it belongs in the shared layer rather than a user's private copy.
