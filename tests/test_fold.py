"""Tests for fold and pocket behaviour."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
ALPHA = EXAMPLES / "alpha.txt"
BETA = EXAMPLES / "beta.txt"


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "sourcefold.cli", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def test_fold_two_examples_writes_sheet_with_origins(workspace):
    result = _run(
        "fold",
        str(ALPHA),
        str(BETA),
        "--sheet",
        "demo",
        cwd=workspace,
    )
    assert result.returncode == 0, result.stderr
    sheet = workspace / "artifacts" / "demo" / "SHEET.md"
    assert sheet.is_file()
    text = sheet.read_text(encoding="utf-8")
    assert str(ALPHA.resolve()) in text or ALPHA.name in text
    assert str(BETA.resolve()) in text or BETA.name in text
    # Both origins must appear (resolved absolute paths from fold)
    assert "alpha.txt" in text
    assert "beta.txt" in text


def test_pocket_does_not_add_claims_to_sheet(workspace):
    # Fold first so sheet exists
    r1 = _run("fold", str(ALPHA), "--sheet", "pock", cwd=workspace)
    assert r1.returncode == 0, r1.stderr
    sheet = workspace / "artifacts" / "pock" / "SHEET.md"
    before = sheet.read_text(encoding="utf-8")
    claim_count_before = before.count("### C")

    r2 = _run("pocket", str(BETA), "--sheet", "pock", cwd=workspace)
    assert r2.returncode == 0, r2.stderr
    after = sheet.read_text(encoding="utf-8")
    claim_count_after = after.count("### C")
    assert claim_count_after == claim_count_before
    assert "pocket/beta.txt" in after or "beta.txt" in after
    pocket_copy = workspace / "artifacts" / "pock" / "pocket" / "beta.txt"
    assert pocket_copy.is_file()


def test_fetch_disabled(workspace):
    result = _run(
        "--fetch",
        "fold",
        str(ALPHA),
        "--sheet",
        "x",
        cwd=workspace,
    )
    assert result.returncode != 0
    assert "fetch disabled in v0" in result.stderr

    result2 = _run(
        "fold",
        str(ALPHA),
        "--sheet",
        "x",
        "--fetch",
        cwd=workspace,
    )
    assert result2.returncode != 0
    assert "fetch disabled in v0" in result2.stderr
