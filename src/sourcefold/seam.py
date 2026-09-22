"""Naive seam detection via explicit negation of a shared noun phrase."""

from __future__ import annotations

import re
from typing import Iterable

from sourcefold.models import Claim

_NEGATION = re.compile(
    r"\b(?:not|no|never|isn't|aren't|wasn't|weren't|doesn't|don't|didn't|"
    r"cannot|can't|won't|wouldn't|shouldn't|is not|are not|was not|"
    r"were not|does not|do not|did not)\b",
    re.IGNORECASE,
)

_NEG_WORDS = frozenset(
    {
        "not",
        "no",
        "never",
        "isn't",
        "aren't",
        "wasn't",
        "weren't",
        "doesn't",
        "don't",
        "didn't",
        "cannot",
        "can't",
        "won't",
        "wouldn't",
        "shouldn't",
        "doesn't",
    }
)

_STOP = frozenset(
    {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "should",
        "can",
        "could",
        "may",
        "might",
        "must",
        "shall",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "they",
        "them",
        "their",
        "he",
        "she",
        "his",
        "her",
        "we",
        "our",
        "you",
        "your",
        "i",
        "my",
        "me",
        "with",
        "from",
        "for",
        "into",
        "onto",
        "upon",
        "about",
        "over",
        "under",
        "between",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "to",
        "of",
        "in",
        "on",
        "at",
        "by",
        "as",
        "if",
        "than",
        "then",
        "so",
        "also",
        "only",
        "just",
        "very",
        "too",
        "all",
        "each",
        "every",
        "both",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "own",
        "same",
        "there",
        "here",
        "when",
        "where",
        "why",
        "how",
        "what",
        "which",
        "who",
        "whom",
        "contains",
        "contain",
        "containing",
    }
) | _NEG_WORDS


def content_tokens(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z]+", text.lower())
    return [w for w in words if w not in _STOP]


def extract_noun_phrases(text: str) -> set[str]:
    tokens = content_tokens(text)
    phrases: set[str] = set()
    for n in (1, 2, 3):
        for i in range(len(tokens) - n + 1):
            gram = " ".join(tokens[i : i + n])
            if n == 1 and len(gram) < 4:
                continue
            phrases.add(gram)
    return phrases


def has_negation(text: str) -> bool:
    return bool(_NEGATION.search(text))


def detect_seams(claims: Iterable[Claim]) -> list[dict]:
    """Flag pairs where one claim negates a noun phrase present in the other."""
    items = list(claims)
    seams: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for i, a in enumerate(items):
        for b in items[i + 1 :]:
            if a.origin == b.origin:
                continue
            nps_a = extract_noun_phrases(a.text)
            nps_b = extract_noun_phrases(b.text)
            shared = nps_a & nps_b
            # Prefer bigrams; else any multi-word; else single content words
            bigrams = {p for p in shared if len(p.split()) == 2}
            multi = {p for p in shared if " " in p}
            shared_use = bigrams or multi or shared
            if not shared_use:
                continue
            neg_a = has_negation(a.text)
            neg_b = has_negation(b.text)
            if neg_a == neg_b:
                continue
            pair = tuple(sorted([a.id, b.id]))
            if pair in seen:
                continue
            seen.add(pair)
            seams.append(
                {
                    "left": a.id,
                    "right": b.id,
                    "shared": sorted(shared_use),
                    "negated": a.id if neg_a else b.id,
                    "left_text": a.text,
                    "right_text": b.text,
                }
            )
    return seams


def format_seams_md(seams: list[dict]) -> str:
    if not seams:
        return ""
    lines = ["# Seams", ""]
    lines.append("| Left | Right | Shared | Negated |")
    lines.append("|------|-------|--------|---------|")
    for s in seams:
        shared = ", ".join(s["shared"])
        lines.append(
            f"| {s['left']} | {s['right']} | {shared} | {s['negated']} |"
        )
    lines.append("")
    for s in seams:
        lines.append(f"## {s['left']} ↔ {s['right']}")
        lines.append("")
        lines.append(f"- **{s['left']}**: {s['left_text']}")
        lines.append(f"- **{s['right']}**: {s['right_text']}")
        lines.append("")
    return "\n".join(lines)
