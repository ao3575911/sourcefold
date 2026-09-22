"""Dataclass models for sources, creases, claims, and sheets."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Source:
    origin: str
    raw: str
    sha256: str


@dataclass
class Crease:
    id: str
    text: str
    origin: str
    sha256: str
    class_: str
    source: str

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["class"] = d.pop("class_")
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Crease:
        payload = dict(data)
        if "class" in payload and "class_" not in payload:
            payload["class_"] = payload.pop("class")
        return cls(**payload)


# Claim is identical to Crease for v0.
Claim = Crease


@dataclass
class Sheet:
    name: str
    claims: list[Claim] = field(default_factory=list)
    pockets: list[str] = field(default_factory=list)
    seams: list[dict[str, Any]] = field(default_factory=list)
