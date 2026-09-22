"""Tests for unfold."""

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


def test_unfold_c001_returns_first_file_text(workspace):
    r = _run(
        "fold",
        str(ALPHA),
        str(BETA),
        "--sheet",
        "demo",
        cwd=workspace,
    )
    assert r.returncode == 0, r.stderr
    u = _run("unfold", "C001", "--sheet", "demo", cwd=workspace)
    assert u.returncode == 0, u.stderr
    expected = ALPHA.read_text(encoding="utf-8").strip()
    assert u.stdout.strip() == expected
