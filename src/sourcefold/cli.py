"""Sourcefold CLI entrypoint."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from sourcefold.fold import fold_files, pocket_file
from sourcefold.seam import detect_seams, format_seams_md
from sourcefold.sheet import find_claim, list_sheets, sheet_dir


FETCH_ERROR = "fetch disabled in v0"


def _refuse_fetch(ns: argparse.Namespace) -> None:
    if getattr(ns, "fetch", False):
        print(FETCH_ERROR, file=sys.stderr)
        raise SystemExit(1)


def cmd_fold(ns: argparse.Namespace) -> int:
    _refuse_fetch(ns)
    files = [Path(f) for f in ns.files]
    for f in files:
        if not f.is_file():
            print(f"error: not a file: {f}", file=sys.stderr)
            return 1
    sheet_path = fold_files(files, ns.sheet)
    print(sheet_path)
    return 0


def cmd_unfold(ns: argparse.Namespace) -> int:
    _refuse_fetch(ns)
    claim = find_claim(ns.sheet, ns.claim_id)
    if claim is None:
        print(f"error: claim {ns.claim_id} not found in sheet {ns.sheet}", file=sys.stderr)
        return 1
    print(claim.text)
    return 0


def cmd_seam(ns: argparse.Namespace) -> int:
    _refuse_fetch(ns)
    sdir = sheet_dir(ns.sheet)
    seams_path = sdir / "SEAMS.md"
    if seams_path.is_file():
        text = seams_path.read_text(encoding="utf-8")
        if text.strip():
            print(text, end="" if text.endswith("\n") else "\n")
        else:
            print("(no seams)")
        return 0
    # Recompute from crease-map
    from sourcefold.sheet import load_crease_map

    claims = load_crease_map(ns.sheet)
    seams = detect_seams(claims)
    text = format_seams_md(seams)
    if text.strip():
        print(text, end="" if text.endswith("\n") else "\n")
    else:
        print("(no seams)")
    return 0


def cmd_pocket(ns: argparse.Namespace) -> int:
    _refuse_fetch(ns)
    fpath = Path(ns.file)
    if not fpath.is_file():
        print(f"error: not a file: {fpath}", file=sys.stderr)
        return 1
    dest = pocket_file(fpath, ns.sheet)
    print(dest)
    return 0


def cmd_sheet(ns: argparse.Namespace) -> int:
    _refuse_fetch(ns)
    if ns.list:
        names = list_sheets()
        if not names:
            print("(no sheets)")
        else:
            for n in names:
                print(n)
        return 0
    print("error: use --list", file=sys.stderr)
    return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sourcefold",
        description="Fold heterogeneous sources onto one auditable sheet.",
    )
    p.add_argument(
        "--fetch",
        action="store_true",
        default=False,
        help="disabled in v0",
    )
    sub = p.add_subparsers(dest="command", required=True)

    fold_p = sub.add_parser("fold", help="Fold files onto a sheet")
    fold_p.add_argument("files", nargs="+", metavar="FILE")
    fold_p.add_argument("--sheet", required=True, dest="sheet")
    fold_p.add_argument("--fetch", action="store_true", default=False)
    fold_p.set_defaults(func=cmd_fold)

    unfold_p = sub.add_parser("unfold", help="Restore claim text by id")
    unfold_p.add_argument("claim_id", metavar="CLAIM_ID")
    unfold_p.add_argument("--sheet", required=True, dest="sheet")
    unfold_p.add_argument("--fetch", action="store_true", default=False)
    unfold_p.set_defaults(func=cmd_unfold)

    seam_p = sub.add_parser("seam", help="Report seams for a sheet")
    seam_p.add_argument("--sheet", required=True, dest="sheet")
    seam_p.add_argument("--fetch", action="store_true", default=False)
    seam_p.set_defaults(func=cmd_seam)

    pocket_p = sub.add_parser("pocket", help="Store unverified material without folding")
    pocket_p.add_argument("file", metavar="FILE")
    pocket_p.add_argument("--sheet", required=True, dest="sheet")
    pocket_p.add_argument("--fetch", action="store_true", default=False)
    pocket_p.set_defaults(func=cmd_pocket)

    sheet_p = sub.add_parser("sheet", help="Sheet utilities")
    sheet_p.add_argument("--list", action="store_true", dest="list")
    sheet_p.add_argument("--fetch", action="store_true", default=False)
    sheet_p.set_defaults(func=cmd_sheet)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    # Detect --fetch before subcommand parsing edge cases
    args_list = list(sys.argv[1:] if argv is None else argv)
    if "--fetch" in args_list:
        print(FETCH_ERROR, file=sys.stderr)
        raise SystemExit(1)
    ns = parser.parse_args(args_list)
    code = ns.func(ns)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
