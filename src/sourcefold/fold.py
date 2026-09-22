"""Fold sources onto a sheet: claims, TRACE, crease-map, seams."""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from sourcefold.crease import make_creases, read_source
from sourcefold.models import Claim, Sheet
from sourcefold.seam import detect_seams, format_seams_md
from sourcefold.sheet import ensure_sheet_dir, load_crease_map


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_sheet_md(path: Path, sheet: Sheet) -> None:
    lines = [f"# Sheet: {sheet.name}", ""]
    lines.append("## Claims")
    lines.append("")
    for c in sheet.claims:
        lines.append(f"### {c.id}")
        lines.append("")
        lines.append(c.text)
        lines.append("")
        lines.append(f"- origin: `{c.origin}`")
        lines.append(f"- sha256: `{c.sha256}`")
        lines.append(f"- class: `{c.class_}`")
        lines.append(f"- source: `{c.source}`")
        lines.append("")
    if sheet.pockets:
        lines.append("## Pockets")
        lines.append("")
        for p in sheet.pockets:
            lines.append(f"- `{p}` (class D, not folded)")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_trace_md(
    path: Path,
    sheet_name: str,
    claims: list[Claim],
    seams: list[dict],
    sources: list[str],
) -> None:
    utc = _utc_now()
    claim_lines = []
    for c in claims:
        claim_lines.append(
            f"- id: {c.id}; text: {c.text}; origin: {c.origin}; "
            f"sha256: {c.sha256}; class: {c.class_}"
        )
    plan_lines = [
        "- read UTF-8 sources",
        "- split sentence-level claims",
        "- assign ids and hashes",
        "- write SHEET.md, TRACE.md, crease-map.json",
        "- run naive seam check",
    ]
    unc = [
        "- sentence split may mis-bound claims",
        "- seam detection is naive noun-phrase negation only",
    ]
    if seams:
        unc.append(f"- {len(seams)} seam(s) flagged; human review required")
    kill = (
        "Abort if any source is not readable UTF-8, or if --fetch is requested."
    )
    decision = (
        f"Folded {len(claims)} claim(s) from {len(sources)} source(s) "
        f"onto sheet '{sheet_name}'."
    )
    body = f"""# TRACE

schema: sourcefold/v0
mode: fold
not: summary; search index; web fetch
utc: {utc}
task: fold sources onto sheet {sheet_name}
lens: provenance-preserving claim extraction

claims[]:
{chr(10).join(claim_lines) if claim_lines else '- (none)'}

plan[]:
{chr(10).join(plan_lines)}

uncertainties[]:
{chr(10).join(unc)}

kill_checks: {kill}

decision: {decision}
"""
    path.write_text(body, encoding="utf-8")


def write_crease_map(path: Path, sheet: Sheet) -> None:
    payload = {
        "name": sheet.name,
        "claims": [c.to_dict() for c in sheet.claims],
        "pockets": list(sheet.pockets),
        "seams": list(sheet.seams),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def fold_files(
    files: list[Path],
    sheet_name: str,
    base: Path | None = None,
) -> Path:
    sdir = ensure_sheet_dir(sheet_name, base)
    existing = load_crease_map(sheet_name, base)
    next_id = 1
    if existing:
        nums = []
        for c in existing:
            if c.id.startswith("C") and c.id[1:].isdigit():
                nums.append(int(c.id[1:]))
        if nums:
            next_id = max(nums) + 1

    # Fresh fold for named sheet in v0: replace claims from this invocation
    all_claims: list[Claim] = []
    origins: list[str] = []
    for fpath in files:
        source = read_source(fpath)
        origins.append(source.origin)
        creases = make_creases(source, start_id=next_id)
        all_claims.extend(creases)
        next_id += len(creases)

    # Preserve existing pocket list if crease-map exists
    pockets: list[str] = []
    cmap = sdir / "crease-map.json"
    if cmap.is_file():
        data = json.loads(cmap.read_text(encoding="utf-8"))
        pockets = list(data.get("pockets", []))

    seams = detect_seams(all_claims)
    sheet = Sheet(
        name=sheet_name,
        claims=all_claims,
        pockets=pockets,
        seams=seams,
    )

    write_sheet_md(sdir / "SHEET.md", sheet)
    write_trace_md(sdir / "TRACE.md", sheet_name, all_claims, seams, origins)
    write_crease_map(sdir / "crease-map.json", sheet)
    (sdir / "SEAMS.md").write_text(format_seams_md(seams), encoding="utf-8")

    return sdir / "SHEET.md"


def pocket_file(
    file: Path,
    sheet_name: str,
    base: Path | None = None,
) -> Path:
    sdir = ensure_sheet_dir(sheet_name, base)
    pocket_dir = sdir / "pocket"
    dest = pocket_dir / file.name
    shutil.copy2(file, dest)

    # Update crease-map / SHEET pockets without folding claims
    existing_claims = load_crease_map(sheet_name, base)
    pockets: list[str] = []
    seams: list[dict] = []
    cmap = sdir / "crease-map.json"
    if cmap.is_file():
        data = json.loads(cmap.read_text(encoding="utf-8"))
        pockets = list(data.get("pockets", []))
        seams = list(data.get("seams", []))
    rel = f"pocket/{file.name}"
    if rel not in pockets:
        pockets.append(rel)

    sheet = Sheet(
        name=sheet_name,
        claims=existing_claims,
        pockets=pockets,
        seams=seams,
    )
    write_crease_map(cmap, sheet)
    if (sdir / "SHEET.md").is_file() or existing_claims:
        write_sheet_md(sdir / "SHEET.md", sheet)
    else:
        # Minimal sheet noting pocket only
        write_sheet_md(sdir / "SHEET.md", sheet)

    return dest
