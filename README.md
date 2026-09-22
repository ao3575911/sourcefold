# Sourcefold

Sourcefold folds heterogeneous sources onto one auditable sheet without destroying provenance.

## Name law

| Term | Meaning |
|------|---------|
| **source** | Origin (file path, URL recorded but not fetched unless `--fetch`, or stdin) |
| **crease** | Normalized span + hash + origin |
| **fold** | Collapse of creases onto a sheet |
| **seam** | Detected contradiction between two atomic claims |
| **pocket** | Class-D / unverified material so it does not contaminate the sheet |
| **unfold** | Restore original span from a claim id |

No web UI. No cloud sync. Local-first CLI only.

## Install

```bash
cd sourcefold
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Requires Python 3.11+. Stdlib only in v0.

## Commands

```bash
# Fold local files onto a named sheet
sourcefold fold FILE [FILE ...] --sheet SHEET_NAME

# Restore claim text by id
sourcefold unfold CLAIM_ID --sheet SHEET_NAME

# Report seams (contradictions)
sourcefold seam --sheet SHEET_NAME

# Pocket unverified material (no claims folded into SHEET.md)
sourcefold pocket FILE --sheet SHEET_NAME

# List sheets under artifacts/
sourcefold sheet --list
```

`--fetch` is refused in v0 with: `fetch disabled in v0`.

## What a fold is not

- **Not a summary.** Claims are preserved spans, not paraphrases.
- **Not a search index.** The sheet is an auditable ledger of provenance, not a retrieval engine.

## Artifacts

Each fold writes under `artifacts/<sheet>/`:

- `SHEET.md` — claims with origin and hash
- `TRACE.md` — schema, mode, utc, task, lens, claims, plan, uncertainties, kill_checks, decision
- `crease-map.json` — machine-readable map
- `SEAMS.md` — contradiction report (empty if none)
- `pocket/` — class-D copies not folded into claims
