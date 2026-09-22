"""Sheet artifact paths and IO helpers."""

from __future__ import annotations

import json
from pathlib import Path

from sourcefold.models import Claim, Sheet


def artifacts_root(base: Path | None = None) -> Path:
    root = base if base is not None else Path.cwd()
    return root / "artifacts"


def sheet_dir(name: str, base: Path | None = None) -> Path:
    return artifacts_root(base) / name


def list_sheets(base: Path | None = None) -> list[str]:
    root = artifacts_root(base)
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if p.is_dir())


def load_crease_map(name: str, base: Path | None = None) -> list[Claim]:
    path = sheet_dir(name, base) / "crease-map.json"
    if not path.is_file():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    claims_raw = data.get("claims", data if isinstance(data, list) else [])
    return [Claim.from_dict(c) for c in claims_raw]


def find_claim(name: str, claim_id: str, base: Path | None = None) -> Claim | None:
    for c in load_crease_map(name, base):
        if c.id == claim_id:
            return c
    return None


def ensure_sheet_dir(name: str, base: Path | None = None) -> Path:
    d = sheet_dir(name, base)
    d.mkdir(parents=True, exist_ok=True)
    (d / "pocket").mkdir(exist_ok=True)
    return d
