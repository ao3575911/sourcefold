---
title: Compile, not retrieve
sources:
  - raw/README.md
compiled: 2026-09-23
---

# Compile, not retrieve

In graft-wiki, wiki pages are **build artifacts**: a local LLM compiles
them from the source corpus in `raw/`, following the rules in
`AGENTS.md`. They are neither hand-authored documents nor live
retrieval output.

## Why compile

- **Provenance.** Every page cites the `raw/` files it was compiled
  from in its front matter; a claim with no source is deleted, not
  kept.
- **Reproducibility.** Given the same corpus, a recompile yields
  substantially the same pages, so the wiki can always be regenerated.
- **Offline sovereignty.** The compiler is local; no external index or
  retrieval service participates, and no run depends on another
  instance.

## Why not retrieve

Retrieval answers queries at read time from whatever the index holds;
its output is ephemeral and unauditable. Compilation fixes the
knowledge at build time, logs the run in [`_log.md`](../_log.md), and
leaves an artifact that can be reviewed, diffed and licensed
(CC-BY-4.0).

Grafting in new knowledge therefore always means: add sources to
`raw/`, then recompile — never paste into `wiki/` directly. See
[graft](graft.md).
