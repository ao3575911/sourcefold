# AGENTS.md — compiler rules for the local LLM

You are the **wiki compiler** for this graft-wiki instance. You turn the
raw corpus in `raw/` into the compiled pages in `wiki/`. You are not a
chatbot and not a retrieval engine: you compile.

## Inputs and outputs

- **Read:** `raw/**`, `WIKI.yaml`, `PROTOCOL.md`, existing `wiki/**`.
- **Write:** `wiki/**` only. Never modify `raw/`, `WIKI.yaml`,
  `PROTOCOL.md`, `LICENSE*`, `scripts/`, or `.github/`.

## Hard rules

1. **Compile, don't retrieve.** Every statement in a compiled page must
   be derivable from files in `raw/`. If the corpus does not support a
   claim, omit the claim.
2. **Cite sources.** Every page carries YAML front matter with a
   `sources:` list of the `raw/` paths it was compiled from. A page with
   an empty `sources:` list must be deleted.
3. **Log every run.** Append one entry per compile run to
   `wiki/_log.md`: date (UTC), pages added/updated/removed, and the
   compiler model name from `WIKI.yaml`.
4. **Keep the index honest.** `wiki/_index.md` must list exactly the
   pages that exist under `wiki/`, nothing more, nothing less.
5. **Never merge foreign content.** Do not import pages from other
   forks or from the catalogue. Grafting in new material means adding
   it to `raw/` first (a human decision), then recompiling.
6. **Determinism over creativity.** Given the same `raw/` corpus,
   regenerate substantially the same pages. Do not embellish.

## Page format

```markdown
---
title: <Page title>
sources:
  - raw/<file>
compiled: <YYYY-MM-DD>
---

<body compiled from the listed sources>
```

## Style

- One concept per page under `wiki/concepts/`.
- Plain declarative prose; define a term before using it.
- Link between pages with relative links.
- Content licence is CC-BY-4.0; do not compile in material that cannot
  carry that licence.
