"""Tests for seam detection on opposing examples."""

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


def test_seam_reports_at_least_one_row(workspace):
    r = _run(
        "fold",
        str(ALPHA),
        str(BETA),
        "--sheet",
        "demo",
        cwd=workspace,
    )
    assert r.returncode == 0, r.stderr
    seams = workspace / "artifacts" / "demo" / "SEAMS.md"
    assert seams.is_file()
    text = seams.read_text(encoding="utf-8")
    assert text.strip(), "SEAMS.md should not be empty for opposing examples"
    assert "C001" in text and "C002" in text

    s = _run("seam", "--sheet", "demo", cwd=workspace)
    assert s.returncode == 0, s.stderr
    assert "C001" in s.stdout or "C002" in s.stdout
