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
        "mutation": "run: echo python examples/orphan/run_orphan.py",
        "boundaries": (
            "assert multiline_pwsh.returncode != 0",
            "assert multiline_bash.returncode == 0",
            "assert step_if_false.returncode != 0",
            "assert step_if_event.returncode != 0",
            "assert bash_or_true.returncode != 0",
            "assert semicolon_exit.returncode != 0",
            "assert continued_expression.returncode != 0",
            "assert continued_string.returncode != 0",
            "assert continued_literal.returncode != 0",
            "assert echoed.returncode != 0",
            "assert job_needs.returncode != 0",
            "assert job_if_false.returncode != 0",
            "assert dispatch_only.returncode != 0",
            "assert multiline_set_plus_e.returncode != 0",
            "assert multiline_trap_err.returncode != 0",
            "assert job_continue_on_error.returncode != 0",
            "assert job_defaults_bash.returncode == 0",
            "assert workflow_defaults_bash.returncode == 0",
            "assert multiline_continuation_step_bash.returncode != 0",
            "assert multiline_continuation_ubuntu.returncode != 0",
            "assert multiline_continuation_job_bash.returncode != 0",
            "assert multiline_continuation_workflow_bash.returncode != 0",
            "assert multiline_comment_backslash.returncode == 0",
            "assert multiline_splice_step_bash.returncode != 0",
            "assert multiline_splice_ubuntu.returncode != 0",
            "assert multiline_splice_job_bash.returncode != 0",
            "assert multiline_splice_workflow_bash.returncode != 0",
            "assert multiline_unknown_command.returncode != 0",
            "assert current_step_always.returncode == 0",
            "assert \"FALSIFICATION_EXECUTION_GUARANTEED\" not in wired.stdout",
            "assert \"residuals=trigger_filters,working_directory,yaml_1_1_scalars\" in wired.stdout",
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
        orphan_runner = fixture / "examples/orphan/run_orphan.py"
        orphan_runner.parent.mkdir(parents=True)
        orphan_runner.write_text(
            "FALSIFICATION_CONTRACTS = ({'id':'NEG-ORPHAN','negative':'n','mutation':'MUTATE',"
            "'boundaries':('ASSERT_OLD','ASSERT_NEW'),'exercised_by':'case_negative'},)\n"
            "def case_negative():\n    '''PERMANENT_NEGATIVE: NEG-ORPHAN'''\n"
            "    candidate = 'MUTATE'\n    assert 'ASSERT_OLD'\n    assert 'ASSERT_NEW'\n",
            encoding="ascii",
        )
        baseline = (
            "on:\n"
            "  push:\n"
            "  pull_request:\n"
            "jobs:\n"
            "  falsification-runners:\n"
            "    runs-on: windows-latest\n"
            "    steps:\n"
            "      - run: python examples/cases/run_cases.py\n"
            "      - run: python examples/orphan/run_orphan.py\n"
        )

        def mutated(name: str, source: str) -> subprocess.CompletedProcess[str]:
            candidate = workflow.with_name(f"{name}.yml")
            candidate.write_text(source, encoding="ascii")
            return run(fixture, candidate)

        workflow.write_text(baseline, encoding="ascii")
        wired = run(fixture, workflow)
        assert wired.returncode == 0, wired.stdout + wired.stderr
        assert "FALSIFICATION_EXECUTION_GUARANTEED" not in wired.stdout, wired.stdout
        assert "residuals=trigger_filters,working_directory,yaml_1_1_scalars" in wired.stdout, wired.stdout

        multiline = baseline.replace(
            "      - run: python examples/orphan/run_orphan.py\n",
            "      - run: |\n"
            "          echo before\n"
            "          python examples/orphan/run_orphan.py\n"
            "          echo after\n",
        )
        multiline_pwsh = mutated("m1-multiline-pwsh", multiline)
        assert multiline_pwsh.returncode != 0, multiline_pwsh.stdout + multiline_pwsh.stderr

        multiline_bash = mutated(
            "m2-multiline-bash",
            multiline.replace("      - run: |\n", "      - shell: bash\n        run: |\n", 1),
        )
        assert multiline_bash.returncode == 0, multiline_bash.stdout + multiline_bash.stderr

        multiline_set_plus_e = mutated(
            "m14-multiline-set-plus-e",
            multiline.replace(
                "      - run: |\n",
                "      - shell: bash\n        run: |\n          set +e\n",
                1,
            ),
        )
        assert multiline_set_plus_e.returncode != 0, multiline_set_plus_e.stdout + multiline_set_plus_e.stderr

        multiline_trap_err = mutated(
            "m15-multiline-trap-err",
            multiline.replace(
                "      - run: |\n",
                "      - shell: bash\n        run: |\n          trap 'exit 0' ERR\n",
                1,
            ),
        )
        assert multiline_trap_err.returncode != 0, multiline_trap_err.stdout + multiline_trap_err.stderr

        job_defaults_bash = mutated(
            "job-defaults-bash",
            multiline.replace(
                "    runs-on: windows-latest\n",
                "    runs-on: windows-latest\n    defaults:\n      run:\n        shell: bash\n",
            ),
        )
        assert job_defaults_bash.returncode == 0, job_defaults_bash.stdout + job_defaults_bash.stderr

        workflow_defaults_bash = mutated(
            "workflow-defaults-bash",
            multiline.replace(
                "jobs:\n",
                "defaults:\n  run:\n    shell: bash\njobs:\n",
            ),
        )
        assert workflow_defaults_bash.returncode == 0, workflow_defaults_bash.stdout + workflow_defaults_bash.stderr

        continuation_block = multiline.replace(
            "          echo before\n", "          echo before \\\n", 1
        )
        multiline_continuation_step_bash = mutated(
            "multiline-continuation-step-bash",
            continuation_block.replace(
                "      - run: |\n", "      - shell: bash\n        run: |\n", 1
            ),
        )
        assert multiline_continuation_step_bash.returncode != 0, (
            multiline_continuation_step_bash.stdout + multiline_continuation_step_bash.stderr
        )

        multiline_continuation_ubuntu = mutated(
            "multiline-continuation-ubuntu",
            continuation_block.replace("runs-on: windows-latest", "runs-on: ubuntu-latest"),
        )
        assert multiline_continuation_ubuntu.returncode != 0, (
            multiline_continuation_ubuntu.stdout + multiline_continuation_ubuntu.stderr
        )

        multiline_continuation_job_bash = mutated(
            "multiline-continuation-job-bash",
            continuation_block.replace(
                "    runs-on: windows-latest\n",
                "    runs-on: windows-latest\n    defaults:\n      run:\n        shell: bash\n",
            ),
        )
        assert multiline_continuation_job_bash.returncode != 0, (
            multiline_continuation_job_bash.stdout + multiline_continuation_job_bash.stderr
        )

        multiline_continuation_workflow_bash = mutated(
            "multiline-continuation-workflow-bash",
            continuation_block.replace(
                "jobs:\n", "defaults:\n  run:\n    shell: bash\njobs:\n"
            ),
        )
        assert multiline_continuation_workflow_bash.returncode != 0, (
            multiline_continuation_workflow_bash.stdout
            + multiline_continuation_workflow_bash.stderr
        )

        multiline_comment_backslash = mutated(
            "multiline-bash-comment-backslash",
            multiline.replace(
                "      - run: |\n",
                "      - shell: bash\n        run: |\n          # comment \\\n",
                1,
            ).replace("          echo before\n", "", 1),
        )
        assert multiline_comment_backslash.returncode == 0, (
            multiline_comment_backslash.stdout + multiline_comment_backslash.stderr
        )

        splice_block = multiline.replace(
            "          echo before\n",
            "          echo before\\\n          #joined \\\n",
            1,
        ).replace("          echo after\n", "", 1)
        multiline_splice_step_bash = mutated(
            "multiline-splice-step-bash",
            splice_block.replace(
                "      - run: |\n", "      - shell: bash\n        run: |\n", 1
            ),
        )
        assert multiline_splice_step_bash.returncode != 0, (
            multiline_splice_step_bash.stdout + multiline_splice_step_bash.stderr
        )

        multiline_splice_ubuntu = mutated(
            "multiline-splice-ubuntu",
            splice_block.replace("runs-on: windows-latest", "runs-on: ubuntu-latest"),
        )
        assert multiline_splice_ubuntu.returncode != 0, (
            multiline_splice_ubuntu.stdout + multiline_splice_ubuntu.stderr
        )

        multiline_splice_job_bash = mutated(
            "multiline-splice-job-bash",
            splice_block.replace(
                "    runs-on: windows-latest\n",
                "    runs-on: windows-latest\n    defaults:\n      run:\n        shell: bash\n",
            ),
        )
        assert multiline_splice_job_bash.returncode != 0, (
            multiline_splice_job_bash.stdout + multiline_splice_job_bash.stderr
        )

        multiline_splice_workflow_bash = mutated(
            "multiline-splice-workflow-bash",
            splice_block.replace(
                "jobs:\n", "defaults:\n  run:\n    shell: bash\njobs:\n"
            ),
        )
        assert multiline_splice_workflow_bash.returncode != 0, (
            multiline_splice_workflow_bash.stdout
            + multiline_splice_workflow_bash.stderr
        )

        multiline_unknown_command = mutated(
            "multiline-unknown-command",
            multiline.replace(
                "      - run: |\n",
                "      - shell: bash\n        run: |\n          printf before\n",
                1,
            ),
        )
        assert multiline_unknown_command.returncode != 0, (
            multiline_unknown_command.stdout + multiline_unknown_command.stderr
        )

        current_step_always = mutated(
            "current-step-always",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - if: always()\n        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert current_step_always.returncode == 0, (
            current_step_always.stdout + current_step_always.stderr
        )

        step_if_false = mutated(
            "m3-step-if-false",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - if: false\n        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert step_if_false.returncode != 0, step_if_false.stdout + step_if_false.stderr

        step_if_event = mutated(
            "m4-step-if-event",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - if: github.event_name == 'schedule'\n"
                "        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert step_if_event.returncode != 0, step_if_event.stdout + step_if_event.stderr

        bash_or_true = mutated(
            "m5-bash-or-true",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - shell: bash\n"
                "        run: python examples/orphan/run_orphan.py || true\n",
            ),
        )
        assert bash_or_true.returncode != 0, bash_or_true.stdout + bash_or_true.stderr

        semicolon_exit = mutated(
            "m6-semicolon-exit",
            baseline.replace(
                "run: python examples/orphan/run_orphan.py",
                "run: python examples/orphan/run_orphan.py; exit 0",
            ),
        )
        assert semicolon_exit.returncode != 0, semicolon_exit.stdout + semicolon_exit.stderr

        continued_expression = mutated(
            "m7-continued-expression",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - continue-on-error: ${{ true }}\n"
                "        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert continued_expression.returncode != 0, continued_expression.stdout + continued_expression.stderr

        continued_string = mutated(
            "m8-continued-string",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - continue-on-error: 'true'\n"
                "        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert continued_string.returncode != 0, continued_string.stdout + continued_string.stderr

        continued_literal = mutated(
            "m9-continued-literal",
            baseline.replace(
                "      - run: python examples/orphan/run_orphan.py\n",
                "      - continue-on-error: true\n"
                "        run: python examples/orphan/run_orphan.py\n",
            ),
        )
        assert continued_literal.returncode != 0, continued_literal.stdout + continued_literal.stderr

        job_continue_on_error = mutated(
            "m16-job-continue-on-error",
            baseline.replace(
                "    runs-on: windows-latest\n",
                "    continue-on-error: true\n    runs-on: windows-latest\n",
            ),
        )
        assert job_continue_on_error.returncode != 0, job_continue_on_error.stdout + job_continue_on_error.stderr

        echoed = mutated(
            "m10-echoed",
            baseline.replace(
                "run: python examples/orphan/run_orphan.py",
                "run: echo python examples/orphan/run_orphan.py",
            ),
        )
        assert echoed.returncode != 0, echoed.stdout + echoed.stderr

        job_needs = mutated(
            "m11-job-needs",
            baseline.replace(
                "    runs-on: windows-latest\n",
                "    needs: validate\n    runs-on: windows-latest\n",
            ),
        )
        assert job_needs.returncode != 0, job_needs.stdout + job_needs.stderr

        job_if_false = mutated(
            "m12-job-if-false",
            baseline.replace(
                "    runs-on: windows-latest\n",
                "    if: false\n    runs-on: windows-latest\n",
            ),
        )
        assert job_if_false.returncode != 0, job_if_false.stdout + job_if_false.stderr

        dispatch_only = mutated(
            "m13-dispatch-only",
            baseline.replace("  push:\n  pull_request:\n", "  workflow_dispatch:\n"),
        )
        assert dispatch_only.returncode != 0, dispatch_only.stdout + dispatch_only.stderr

        no_op_help = mutated(
            "anchored-no-op-help",
            baseline.replace(
                "run: python examples/orphan/run_orphan.py",
                "run: python examples/orphan/run_orphan.py --help",
            ),
        )
        assert no_op_help.returncode != 0, no_op_help.stdout + no_op_help.stderr
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
