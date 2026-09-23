---
title: Catalog, not merge
sources:
  - raw/README.md
compiled: 2026-09-23
---

# Catalog, not merge

**Catalog-not-merge** is the federation rule of graft-wiki: the origin
repository never merges content from its forks. Instead it maintains a
**catalogue** — `CATALOG.md` and `CATALOG.json` — listing every fork
([graft](graft.md)) and the manifest it publishes in `WIKI.yaml`.

## How the catalogue is built

`scripts/build_catalog.py`, run by the `catalog.yml` workflow:

1. lists the forks of the origin repository via the GitHub API;
2. fetches each fork's `WIKI.yaml` and validates it against
   `WIKI.schema.json`;
3. writes `CATALOG.md` (human-readable) and `CATALOG.json`
   (machine-readable).

Forks with a missing or invalid manifest are counted as
`uncatalogued` but not described in the catalogue body.

## Why not merge

Merging would force a single editorial line onto every instance and
turn forks back into branches. Cataloguing instead keeps each graft
sovereign: readers discover instances through the catalogue and read
each wiki where it lives, compiled from that instance's own `raw/`
corpus per [compile-not-retrieve](compile-not-retrieve.md). Content
pull requests from forks to origin are out of protocol and are
declined; delisting requests go in `registry/requests/`.
