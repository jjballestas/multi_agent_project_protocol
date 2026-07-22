#!/usr/bin/env python3
"""Negative controls for the falsification-contract checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_falsification_contracts.py"), "--root", str(root)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def main() -> int:
    clean = run(ROOT)
    assert clean.returncode == 0, clean.stdout + clean.stderr
    with tempfile.TemporaryDirectory(prefix="falsification-contract-") as temp:
        fixture = Path(temp)
        runner = fixture / "examples/cases/run_cases.py"
        runner.parent.mkdir(parents=True)
        runner.write_text(
            "FALSIFICATION_CONTRACTS = ({'id':'NEG-1','negative':'n','mutation':'MUTATE',"
            "'boundaries':('ASSERT_OLD','ASSERT_NEW'),'exercised_by':'case_negative'},)\n"
            "def case_negative():\n    '''PERMANENT_NEGATIVE: NEG-1'''\n"
            "    candidate = 'MUTATE'\n    assert 'ASSERT_OLD'\n    assert 'ASSERT_NEW'\n",
            encoding="ascii",
        )
        valid = run(fixture)
        assert valid.returncode == 0, valid.stdout + valid.stderr
        runner.write_text(runner.read_text(encoding="ascii").replace("    assert 'ASSERT_NEW'\n", ""), encoding="ascii")
        relaxed = run(fixture)
        assert relaxed.returncode != 0, relaxed.stdout + relaxed.stderr
        assert "assertion boundary not found" in relaxed.stdout, relaxed.stdout
        with runner.open("a", encoding="ascii") as stream:
            stream.write("\ndef shadow_negative():\n    '''PERMANENT_NEGATIVE: NEG-SHADOW'''\n    assert False\n")
        undeclared = run(fixture)
        assert undeclared.returncode != 0, undeclared.stdout + undeclared.stderr
        assert "permanent_negatives=2 declared=1 missing=1" in undeclared.stdout, undeclared.stdout
        assert "NEG-SHADOW" in undeclared.stdout, undeclared.stdout
    print("OK: falsification contracts reject relaxed boundaries and undeclared permanent negatives")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
