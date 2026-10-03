# graft-wiki

A **catalogue-not-merge** protocol for LLM-compiled wikis.

Knowledge lives in many independent forks ("grafts"). Each fork keeps
full editorial sovereignty over its own wiki; the origin repository
never merges content from forks — it only **catalogues** them.

## How it works

1. **Graft, don't branch.** Fork this repository to create a new,
   permanently independent instance. You inherit the protocol, not the
   content.
2. **Compile, don't retrieve.** Add source material to `raw/`, then let
   a local LLM compile it into pages under `wiki/`, following the rules
   in [`AGENTS.md`](AGENTS.md). Every page cites its `raw/` sources.
3. **Catalogue, don't merge.** The origin lists forks and their
   manifests in [`CATALOG.md`](CATALOG.md) / [`CATALOG.json`](CATALOG.json).
   Content pull requests from forks to origin are declined by design.

The full rules are in [`PROTOCOL.md`](PROTOCOL.md).

## Repository layout

| Path | Role |
|---|---|
| `PROTOCOL.md` | The protocol constitution (trimmed) |
| `AGENTS.md` | Compiler rules for the local LLM |
| `WIKI.yaml` / `WIKI.schema.json` | Instance manifest and its JSON Schema |
| `raw/` | Source corpus the LLM compiles from |
| `wiki/` | Compiled pages (`_index.md`, `_log.md`, `concepts/…`) |
| `scripts/` | `validate_manifest.py`, `build_catalog.py` |
| `registry/requests/` | Catalogue-inclusion requests (origin only) |
| `examples/` | Complete example instances (see below) |
| `.github/workflows/catalog.yml` | Daily catalogue rebuild |

## Example instances

Three complete, schema-valid example instances show what a grafted wiki
looks like. Each contains its own `WIKI.yaml`, `raw/` corpus, and
compiled `wiki/` pages, and is ready to be copied into a fork:

- [`examples/finite-math/`](examples/finite-math/wiki/_index.md) — sets
  and counting, finite probability, matrices and linear systems
- [`examples/linguistic-analysis/`](examples/linguistic-analysis/wiki/_index.md) —
  morphology, syntax and constituency, semantics and pragmatics
- [`examples/phonetic-science/`](examples/phonetic-science/wiki/_index.md) —
  consonant articulation, vowels, acoustic phonetics

## Quick start (grafting a new instance)

1. Fork this repository.
2. Edit `WIKI.yaml` (instance name, description, topics, maintainer).
3. Validate: `python scripts/validate_manifest.py`
4. Add source material to `raw/` and compile it into `wiki/` per
   `AGENTS.md`.
5. Your fork will be picked up by the origin's catalogue build; forks
   with a valid manifest are catalogued, invalid ones are listed as
   uncatalogued.

## Licence

Dual-licensed:

- **Code** (scripts, workflows, tooling): [MIT](LICENSE)
- **Content** (wiki text, documentation, catalogue entries): [CC-BY-4.0](LICENSE-CONTENT)
