# graft-wiki Protocol (trimmed constitution)

> This is the trimmed, operational copy of the graft-wiki constitution.
> It defines the minimum rules an instance must follow to be catalogued.

## 1. Purpose

graft-wiki is a **catalogue-not-merge** protocol for LLM-compiled wikis.
Knowledge lives in many independent forks ("grafts"). The root repository
never merges content from forks — it only **catalogues** them, so every
instance keeps full editorial sovereignty over its own wiki.

## 2. Core principles

1. **Graft, don't branch.** A fork is a new, permanently independent
   instance. It inherits the protocol, not the content obligations.
2. **Compile, don't retrieve.** Wiki pages are compiled by a local LLM
   from the sources in `raw/`. Pages are build artifacts of the raw
   corpus, not hand-authored documents and not live retrieval output.
3. **Catalogue, don't merge.** The origin repository lists forks and
   their manifests in `CATALOG.*`. Content pull requests from forks to
   origin are out of protocol and must be declined.

## 3. Required instance layout

| Path | Role |
|---|---|
| `PROTOCOL.md` | This document (may be trimmed further, not altered in meaning) |
| `AGENTS.md` | Compiler rules for the local LLM |
| `WIKI.schema.json` | JSON Schema for the manifest |
| `WIKI.yaml` | Instance manifest (identity, topics, compiler, licence) |
| `raw/` | Source corpus the LLM compiles from |
| `wiki/` | Compiled pages (`_index.md`, `_log.md`, `concepts/…`) |
| `scripts/` | `validate_manifest.py`, `build_catalog.py` |
| `registry/requests/` | Catalogue-inclusion requests (origin only) |
| `.github/workflows/catalog.yml` | Catalogue build automation |

## 4. Manifest rules

- Every instance MUST keep a valid `WIKI.yaml` conforming to
  `WIKI.schema.json` (`scripts/validate_manifest.py` must pass).
- `instance.name` MUST be unique among catalogued forks.
- The manifest MUST declare the licence pair: MIT for code and
  CC-BY-4.0 for content.

## 5. Compilation rules

- Only material present in `raw/` may be compiled into `wiki/`.
- Every compiled page MUST cite its `raw/` sources in front matter.
- Every compile run MUST append an entry to `wiki/_log.md`.
- The compiler obeys `AGENTS.md`; a page that cannot cite a source is
  deleted, not kept.

## 6. Cataloguing rules

- The origin repository periodically runs `scripts/build_catalog.py`,
  which lists forks of the origin, reads each fork's `WIKI.yaml`, and
  writes `CATALOG.md` and `CATALOG.json`.
- A fork with a missing or invalid manifest is listed as
  `uncatalogued` and excluded from the catalogue body.
- Delisting requests go in `registry/requests/`.

## 7. Licence

Code is MIT (`LICENSE`); content is CC-BY-4.0 (`LICENSE-CONTENT`).
Forks MUST preserve this pair.
