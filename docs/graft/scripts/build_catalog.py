#!/usr/bin/env python3
"""Build the graft-wiki catalogue.

Lists forks of the origin repository via the GitHub API, reads each
fork's WIKI.yaml, validates it, and writes CATALOG.md and CATALOG.json
(catalogue-not-merge: forks are listed, never merged).

Usage:
    python scripts/build_catalog.py [--repo owner/repo] [--out DIR]

Environment:
    GITHUB_TOKEN   optional; raises the API rate limit and allows
                   private-fork listing where permitted. Unauthenticated
                   listing works for public forks at 60 requests/hour.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate_manifest import validate_fallback  # noqa: E402

API = "https://api.github.com"
DEFAULT_REPO = "SM260845/graft-wiki"


def gh_get(url: str) -> object:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", "Bearer " + token)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def list_forks(repo: str) -> list[dict]:
    forks: list[dict] = []
    page = 1
    while True:
        batch = gh_get(f"{API}/repos/{repo}/forks?per_page=100&page={page}")
        if not batch:
            break
        forks.extend(batch)
        page += 1
    return forks


def fetch_manifest(fork: dict) -> dict | None:
    full_name = fork["full_name"]
    branch = fork.get("default_branch", "main")
    url = f"https://raw.githubusercontent.com/{full_name}/{branch}/WIKI.yaml"
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            manifest = yaml.safe_load(response.read())
    except (urllib.error.URLError, yaml.YAMLError):
        return None
    return manifest if isinstance(manifest, dict) else None


def catalog_entry(fork: dict) -> dict:
    entry = {
        "repo": fork["full_name"],
        "url": fork["html_url"],
        "default_branch": fork.get("default_branch", "main"),
        "pushed_at": fork.get("pushed_at"),
        "catalogued": False,
        "manifest": None,
        "errors": [],
    }
    manifest = fetch_manifest(fork)
    if manifest is None:
        entry["errors"] = ["WIKI.yaml missing or unreadable"]
        return entry
    errors = validate_fallback(manifest)
    if errors:
        entry["errors"] = errors
        return entry
    entry["catalogued"] = True
    entry["manifest"] = manifest
    return entry


def write_outputs(repo: str, entries: list[dict], out_dir: Path) -> None:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    catalogued = [e for e in entries if e["catalogued"]]
    uncatalogued = [e for e in entries if not e["catalogued"]]

    data = {
        "protocol": "graft-wiki",
        "origin": repo,
        "generated": generated,
        "forks_total": len(entries),
        "catalogued": catalogued,
        "uncatalogued": [
            {"repo": e["repo"], "url": e["url"], "errors": e["errors"]}
            for e in uncatalogued
        ],
    }
    (out_dir / "CATALOG.json").write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# graft-wiki catalogue",
        "",
        f"Origin: `{repo}` · Generated: {generated} · "
        f"Forks: {len(entries)} · Catalogued: {len(catalogued)} · "
        f"Uncatalogued: {len(uncatalogued)}",
        "",
        "Instances are listed, never merged (catalogue-not-merge).",
        "",
    ]
    if catalogued:
        lines += [
            "| Instance | Repository | Description | Topics |",
            "|---|---|---|---|",
        ]
        for e in catalogued:
            inst = e["manifest"]["instance"]
            topics = ", ".join(inst.get("topics", []))
            lines.append(
                f"| {inst['name']} | [{e['repo']}]({e['url']}) "
                f"| {inst['description']} | {topics} |"
            )
    else:
        lines.append("_No catalogued instances yet — fork the origin to graft one._")
    if uncatalogued:
        lines += ["", "## Uncatalogued forks", ""]
        for e in uncatalogued:
            lines.append(f"- [{e['repo']}]({e['url']}): {'; '.join(e['errors'])}")
    (out_dir / "CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO))
    parser.add_argument("--out", default=str(ROOT), help="output directory")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        forks = list_forks(args.repo)
    except urllib.error.URLError as exc:
        print(f"ERROR: cannot list forks of {args.repo}: {exc}", file=sys.stderr)
        return 1
    entries = [catalog_entry(fork) for fork in forks]
    write_outputs(args.repo, entries, out_dir)
    print(
        f"Wrote CATALOG.md and CATALOG.json: {len(entries)} fork(s), "
        f"{sum(e['catalogued'] for e in entries)} catalogued."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
