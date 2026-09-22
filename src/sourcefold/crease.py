"""Crease creation: normalize spans, hash, and assign claim ids."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from sourcefold.models import Crease, Source

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_source(path: Path) -> Source:
    raw = path.read_text(encoding="utf-8")
    origin = str(path.resolve())
    return Source(origin=origin, raw=raw, sha256=sha256_text(raw))


def split_claims(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = _SENTENCE_RE.split(text)
    return [p.strip() for p in parts if p.strip()]


def make_creases(
    source: Source,
    start_id: int = 1,
    class_: str = "D",
) -> list[Crease]:
    claims = split_claims(source.raw)
    creases: list[Crease] = []
    for i, text in enumerate(claims):
        cid = f"C{start_id + i:03d}"
        creases.append(
            Crease(
                id=cid,
                text=text,
                origin=source.origin,
                sha256=sha256_text(text),
                class_=class_,
                source=source.origin,
            )
        )
    return creases
