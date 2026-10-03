#!/usr/bin/env python3
"""Validate WIKI.yaml against WIKI.schema.json.

Usage:
    python scripts/validate_manifest.py [path/to/WIKI.yaml]

Exits 0 if the manifest is valid, 1 otherwise. Uses `jsonschema` when
installed; otherwise falls back to a built-in structural check covering
the same required fields and constant values.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "WIKI.schema.json"


def load(manifest_path: Path) -> tuple[dict, dict]:
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    with open(manifest_path, encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a YAML mapping")
    return schema, manifest


def validate_with_jsonschema(schema: dict, manifest: dict) -> list[str]:
    import jsonschema  # type: ignore

    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}"
        for e in sorted(
            validator.iter_errors(manifest),
            key=lambda e: ([str(p) for p in e.absolute_path], e.message),
        )
    ]


def validate_fallback(manifest: dict) -> list[str]:
    """Minimal structural validation mirroring WIKI.schema.json."""
    errors: list[str] = []

    def need(obj: dict, path: str, key: str) -> object:
        if not isinstance(obj, dict) or key not in obj:
            errors.append(f"{path}: missing required key '{key}'")
            return None
        return obj[key]

    protocol = need(manifest, "<root>", "protocol")
    instance = need(manifest, "<root>", "instance")
    compiler = need(manifest, "<root>", "compiler")
    license_ = need(manifest, "<root>", "license")

    if isinstance(protocol, dict):
        if protocol.get("name") != "graft-wiki":
            errors.append("protocol/name: must be 'graft-wiki'")
        version = protocol.get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+", version):
            errors.append("protocol/version: must match '<major>.<minor>'")

    if isinstance(instance, dict):
        name = instance.get("name")
        if not isinstance(name, str) or not re.fullmatch(
            r"[a-z0-9][a-z0-9-]{1,62}[a-z0-9]", name
        ):
            errors.append("instance/name: must be a kebab-case identifier")
        if not isinstance(instance.get("description"), str) or not instance["description"]:
            errors.append("instance/description: must be a non-empty string")
        origin = instance.get("origin")
        if not isinstance(origin, str) or not re.fullmatch(
            r"[A-Za-z0-9-]+/[A-Za-z0-9._-]+", origin
        ):
            errors.append("instance/origin: must be 'owner/repo'")
        topics = instance.get("topics")
        if not isinstance(topics, list) or not topics:
            errors.append("instance/topics: must be a non-empty list")

    if isinstance(compiler, dict):
        if not isinstance(compiler.get("model"), str) or not compiler["model"]:
            errors.append("compiler/model: must be a non-empty string")
        if compiler.get("rules") != "AGENTS.md":
            errors.append("compiler/rules: must be 'AGENTS.md'")

    if isinstance(license_, dict):
        if license_.get("code") != "MIT":
            errors.append("license/code: must be 'MIT'")
        if license_.get("content") != "CC-BY-4.0":
            errors.append("license/content: must be 'CC-BY-4.0'")

    return errors


def validate_data(schema: dict, manifest: dict) -> list[str]:
    """Validate a manifest mapping, preferring jsonschema when installed."""
    try:
        return validate_with_jsonschema(schema, manifest)
    except ImportError:
        return validate_fallback(manifest)


def validate(manifest_path: Path) -> list[str]:
    schema, manifest = load(manifest_path)
    return validate_data(schema, manifest)


def main() -> int:
    manifest_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "WIKI.yaml"
    try:
        errors = validate(manifest_path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if errors:
        print(f"INVALID: {manifest_path}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"OK: {manifest_path} conforms to WIKI.schema.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
