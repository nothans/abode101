# Evals

Does the base actually answer house questions correctly, and, just as important, does it
**refuse to invent** what it doesn't know? These evals check both.

An eval is a `prompt` plus `expect` assertions. To run them, an agent answers each prompt
**cold**: fresh context, using only this folder per [`AGENTS.md`](../AGENTS.md), then each
answer is graded against the assertions. A pass means the right exact fact came back with a
source; a fail means a wrong/missing fact, a missing citation, or (worst) a fabrication.

- `cases.example.yaml`: generic examples on the `_EXAMPLE` data + every assertion type. **Public.**
- `house.local.yaml`: your real cases (gitignored; expected answers are your house). Copy the
  example to start your own.

## Case format
```yaml
- id: short-kebab-id
  prompt: "the question, exactly as a user would ask it"
  expect:
    must_include: ["CR2032"]                 # ALL must appear (case-insensitive)
    must_include_one_of: ["unknown","not measured"]  # at least ONE must appear
    should_include: ["Panasonic"]            # quality bonus, not required to pass
    must_not_include: ["AA","AAA","9V"]      # NONE may appear (catches wrong guesses)
    must_cite: true                          # answer must name a source (file/manual/page/"per owner")
    numeric_range: { min: 17, max: 18, unit: years }  # a number in range must appear
    affiliate_tag: "your-tag"                # any amazon.com link must carry tag=<value>; amzn.to ok as-is
    behavior: refuse_unknown                 # see vocabulary below
  source_of_truth: items/some-item.md        # where the answer lives (for the grader/human)
```

### `behavior` vocabulary
- `refuse_unknown`: the fact isn't in the base; the answer must say so (not known / not
  measured / not captured) and **must not** fabricate a value.
- `cite_source`: the answer must point to where the fact came from.
- `affiliate_tagged`: any Amazon link in the answer carries the owner's tag (see `AGENTS.md`).
- `lists_from_schedule`: answer is derived from `maintenance/` and flags uncited intervals
  as `TODO` rather than inventing them.

## Grading
- **Pass** = every `must_*` / `numeric_range` / `affiliate_tag` / `behavior` assertion holds.
- **Quality score** = fraction of `should_include` met (informational, doesn't fail a case).
- Report a table: `id · pass/fail · which assertion failed · the answer`.
- **Normalize before matching**, or you'll get false fails: case-insensitive; collapse
  whitespace; treat the `×` multiplication sign and the letter `x` as equivalent (vent/bulb
  sizes like `4×10` vs `4x10`); ignore thousands separators in numbers.

## How to run (no dependencies)
Point an agent at this folder and say: *"For each case in `evals/house.local.yaml`, answer the
prompt cold using only this folder per AGENTS.md, then grade your answer against `expect` and
output a pass/fail table."* Run cases in **separate fresh contexts** so the base, not chat
memory, is what's under test. (A scripted runner can be added later; the data format is ready.)

## What good coverage looks like
1. **Exact-fact retrieval**: battery, model, filter size, vent size, capacity (deterministic).
2. **Honesty on unknowns**: `refuse_unknown` cases; the anti-fabrication guardrail.
3. **Provenance**: `must_cite` on the facts that matter.
4. **Ranges/derived**: age from an install date, "what's due" from the schedule.
5. **Link policy**: Amazon answers carry the affiliate tag.
