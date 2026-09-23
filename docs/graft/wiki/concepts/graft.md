---
title: Graft
sources:
  - raw/README.md
compiled: 2026-09-23
---

# Graft

A **graft** is a fork of a graft-wiki repository treated as a new,
permanently independent instance — the way a cutting grafted onto new
rootstock becomes its own tree. The graft inherits the *protocol*
(`PROTOCOL.md`, `AGENTS.md`, the manifest schema) but none of the
content obligations of its origin.

## Graft vs. branch

A branch exists to be merged back. A graft never merges back: content
flows into an instance only through its own `raw/` corpus, and the
origin repository relates to grafts solely by
[cataloguing them](catalog-not-merge.md).

## How to graft

1. Fork the origin repository.
2. Edit `WIKI.yaml`: pick a unique `instance.name`, describe your
   topics, name your compiler model.
3. Run `python scripts/validate_manifest.py` until it passes.
4. Replace the contents of `raw/` with your own corpus and recompile
   the wiki per [compile-not-retrieve](compile-not-retrieve.md).

The origin's catalogue build will discover the fork and list it once
its manifest is valid.
