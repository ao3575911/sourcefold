# raw/ — source corpus

This directory is the **only** input the wiki compiler may use. Pages
under `wiki/` are compiled from files here, per the rules in
`AGENTS.md`; nothing may appear in the wiki that is not supported by a
file in `raw/`.

## Rules

- Humans add material here; the compiler never writes here.
- Any plain-text format is fine (Markdown, notes, transcripts, data).
- To graft in outside knowledge, add it here first — with a licence
  compatible with CC-BY-4.0 — then recompile the wiki.
- Removing a file from `raw/` obliges the next compile run to remove or
  trim every wiki page that cited it.

## Layout

Free-form. Suggested convention: one topic per file, kebab-case names,
e.g. `raw/graft-protocol-notes.md`.
