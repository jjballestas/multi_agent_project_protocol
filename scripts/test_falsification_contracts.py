#!/usr/bin/env python3
"""Negative controls for the falsification-contract checker."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-FALSIFICATION-GUARDIAN",
        "negative": "A convention-marked negative outside the former examples/run_*.py glob is inventoried.",
        "mutation": ".replace(marker_line, \"\")",
        "boundaries": (
            "assert off_glob.returncode != 0",
            "assert invisible.returncode == 0",
            "assert nested.returncode != 0",
            "assert shallow.returncode == 0",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-FALSIFICATION-RUNNER-WIRING",
        "negative": "A declared contract must have a direct, failure-gating invocation inside a real workflow job.",
        "mutation": '.replace("run: python examples/orphan/run_orphan.py", "run: echo python examples/orphan/run_orphan.py")',
        "boundaries": (
            "assert wired.returncode == 0",
            "assert orphan.returncode != 0",
            'assert "runner is not executed by workflow" in orphan.stdout',
            "assert healed.returncode == 0",
            "assert continued.returncode != 0",
            "assert echoed.returncode != 0",
            "assert removed_job.returncode != 0",
        ),
        "exercised_by": "main",
    },
)


def run(root: Path, workflow: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, str(ROOT / "scripts/check_falsification_contracts.py"), "--root", str(root)]
    if workflow is not None:
        command.extend(("--workflow", str(workflow)))
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def run_with_checker(checker: Path, root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(checker), "--root", str(root)],
        cwd=checker.parent,
        text=True,
        capture_output=True,
    )


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-FALSIFICATION-GUARDIAN, NEG-FALSIFICATION-RUNNER-WIRING"""
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
    with tempfile.TemporaryDirectory(prefix="falsification-workflow-") as temp:
        fixture = Path(temp)
        runner = fixture / "examples/cases/run_cases.py"
        runner.parent.mkdir(parents=True)
        runner.write_text(
            "FALSIFICATION_CONTRACTS = ({'id':'NEG-WIRED','negative':'n','mutation':'MUTATE',"
            "'boundaries':('ASSERT_OLD','ASSERT_NEW'),'exercised_by':'case_negative'},)\n"
            "def case_negative():\n    '''PERMANENT_NEGATIVE: NEG-WIRED'''\n"
            "    candidate = 'MUTATE'\n    assert 'ASSERT_OLD'\n    assert 'ASSERT_NEW'\n",
            encoding="ascii",
        )
        workflow = fixture / ".github/workflows/validate.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            "jobs:\n"
            "  falsification-runners:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: python examples/cases/run_cases.py\n",
            encoding="ascii",
        )
        wired = run(fixture, workflow)
        assert wired.returncode == 0, wired.stdout + wired.stderr
        orphan_runner = fixture / "examples/orphan/run_orphan.py"
        orphan_runner.parent.mkdir(parents=True)
        orphan_runner.write_text(
            "FALSIFICATION_CONTRACTS = ({'id':'NEG-ORPHAN','negative':'n','mutation':'MUTATE',"
            "'boundaries':('ASSERT_OLD','ASSERT_NEW'),'exercised_by':'case_negative'},)\n"
            "def case_negative():\n    '''PERMANENT_NEGATIVE: NEG-ORPHAN'''\n"
            "    candidate = 'MUTATE'\n    assert 'ASSERT_OLD'\n    assert 'ASSERT_NEW'\n",
            encoding="ascii",
        )
        orphan = run(fixture, workflow)
        assert orphan.returncode != 0, orphan.stdout + orphan.stderr
        assert "runner is not executed by workflow" in orphan.stdout, orphan.stdout
        workflow.write_text(
            workflow.read_text(encoding="ascii") + "      - run: python examples/orphan/run_orphan.py\n",
            encoding="ascii",
        )
        healed = run(fixture, workflow)
        assert healed.returncode == 0, healed.stdout + healed.stderr
        continued_workflow = workflow.with_name("continued.yml")
        continued_workflow.write_text(
            workflow.read_text(encoding="ascii").replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - continue-on-error: true\n        run: python examples/orphan/run_orphan.py\n",
            ),
            encoding="ascii",
        )
        continued = run(fixture, continued_workflow)
        assert continued.returncode != 0, continued.stdout + continued.stderr
        echoed_workflow = workflow.with_name("echoed.yml")
        echoed_workflow.write_text(
            workflow.read_text(encoding="ascii").replace("run: python examples/orphan/run_orphan.py", "run: echo python examples/orphan/run_orphan.py"),
            encoding="ascii",
        )
        echoed = run(fixture, echoed_workflow)
        assert echoed.returncode != 0, echoed.stdout + echoed.stderr
        removed_job_workflow = workflow.with_name("removed-job.yml")
        removed_job_workflow.write_text(
            "jobs:\n"
            "  decoy:\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: python examples/cases/run_cases.py\n"
            "      - run: echo python examples/orphan/run_orphan.py\n",
            encoding="ascii",
        )
        removed_job = run(fixture, removed_job_workflow)
        assert removed_job.returncode != 0, removed_job.stdout + removed_job.stderr
    with tempfile.TemporaryDirectory(prefix="falsification-off-glob-") as temp:
        fixture = Path(temp)
        outside_old_glob = fixture / "scripts/test_outside_old_glob.py"
        outside_old_glob.parent.mkdir(parents=True)
        marker_line = "    '''PERMANENT_NEGATIVE: NEG-OFF-GLOB'''\n"
        outside_old_glob.write_text(
            "def test_real_negative():\n" + marker_line + "    assert False\n",
            encoding="ascii",
        )
        off_glob = run(fixture)
        assert off_glob.returncode != 0, off_glob.stdout + off_glob.stderr
        assert "permanent_negatives=1 declared=0 missing=1" in off_glob.stdout, off_glob.stdout
        assert "NEG-OFF-GLOB" in off_glob.stdout, off_glob.stdout

        outside_old_glob.write_text(
            outside_old_glob.read_text(encoding="ascii").replace(marker_line, ""),
            encoding="ascii",
        )
        invisible = run(fixture)
        assert invisible.returncode == 0, invisible.stdout + invisible.stderr
        assert "permanent_negatives=0 declared=0 missing=0" in invisible.stdout, invisible.stdout
    with tempfile.TemporaryDirectory(prefix="falsification-nested-") as temp:
        fixture = Path(temp) / "fixture"
        nested_source = fixture / "scripts/test_nested_negative.py"
        nested_source.parent.mkdir(parents=True)
        nested_source.write_text(
            "class NegativeSuite:\n"
            "    def test_nested_negative(self):\n"
            "        '''PERMANENT_NEGATIVE: NEG-CLASS-METHOD'''\n"
            "        assert False\n",
            encoding="ascii",
        )
        nested = run(fixture)
        assert nested.returncode != 0, nested.stdout + nested.stderr
        assert "permanent_negatives=1 declared=0 missing=1" in nested.stdout, nested.stdout
        assert "NEG-CLASS-METHOD" in nested.stdout, nested.stdout

        tool_dir = Path(temp) / "mutant_tools"
        tool_dir.mkdir()
        checker_source = (ROOT / "scripts/check_falsification_contracts.py").read_text(encoding="utf-8")
        shallow_source = checker_source.replace("for node in ast.walk(tree):", "for node in tree.body:")
        assert shallow_source != checker_source
        shallow_checker = tool_dir / "check_falsification_contracts.py"
        shallow_checker.write_text(shallow_source, encoding="utf-8")
        shutil.copy2(ROOT / "scripts/falsification_contracts.py", tool_dir / "falsification_contracts.py")
        shallow = run_with_checker(shallow_checker, fixture)
        assert shallow.returncode == 0, shallow.stdout + shallow.stderr
        assert "permanent_negatives=0 declared=0 missing=0" in shallow.stdout, shallow.stdout
    print(
        "OK: guardian rejects relaxed boundaries and marked undeclared negatives; "
        "complete AST discovery and the marker's static-source limit are proved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
