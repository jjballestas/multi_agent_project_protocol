#!/usr/bin/env python3
"""Replay every ``run`` step of one GitHub Actions job in workflow order.

The workflow is the only step inventory. Unsupported host shells are reported
explicitly and do not disappear from the result set.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--workflow", default=".github/workflows/validate.yml")
    parser.add_argument("--job", default="validate")
    parser.add_argument("--timeout", type=int, default=900, help="Seconds allowed per step.")
    parser.add_argument("--json-out", help="Optional path for the complete machine-readable report.")
    return parser.parse_args()


def load_job(workflow: Path, job_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = yaml.safe_load(workflow.read_text(encoding="utf-8-sig"))
    if not isinstance(document, dict) or not isinstance(document.get("jobs"), dict):
        raise ValueError(f"{workflow}: workflow must define a jobs mapping")
    job = document["jobs"].get(job_id)
    if not isinstance(job, dict) or not isinstance(job.get("steps"), list):
        raise ValueError(f"{workflow}: job {job_id!r} must define a steps list")
    run_steps = [step for step in job["steps"] if isinstance(step, dict) and "run" in step]
    return job, run_steps


def configured_shell(job: dict[str, Any], step: dict[str, Any]) -> str | None:
    shell = step.get("shell")
    if shell is None:
        defaults = job.get("defaults")
        if isinstance(defaults, dict) and isinstance(defaults.get("run"), dict):
            shell = defaults["run"].get("shell")
    return str(shell) if shell is not None else None


def shell_command(job: dict[str, Any], step: dict[str, Any]) -> tuple[list[str] | None, str]:
    declared = configured_shell(job, step)
    runs_on = job.get("runs-on")
    kind = declared
    if kind is None and isinstance(runs_on, str):
        if runs_on.startswith(("ubuntu-", "macos-")):
            kind = "bash"
        elif runs_on.startswith("windows-"):
            kind = "pwsh"
    command = step.get("run")
    if not isinstance(command, str):
        return None, "run value is not a string"
    if kind == "bash":
        executable = shutil.which("bash")
        if executable:
            return [executable, "-eo", "pipefail", "-c", command], "bash"
        return None, "workflow requires bash, but bash is unavailable on this host"
    if kind in {"pwsh", "powershell"}:
        executable = shutil.which(kind)
        if executable:
            return [executable, "-NoLogo", "-NonInteractive", "-Command", command], kind
        return None, f"workflow requires {kind}, but {kind} is unavailable on this host"
    return None, f"workflow shell {kind!r} is not supported by this replicator"


def execute_step(
    root: Path,
    job: dict[str, Any],
    step: dict[str, Any],
    number: int,
    total: int,
    timeout: int,
) -> dict[str, Any]:
    name = str(step.get("name") or f"run step {number}")
    argv, shell = shell_command(job, step)
    if argv is None:
        result = {
            "number": number,
            "name": name,
            "status": "UNSUPPORTED",
            "exit_code": None,
            "diagnostic": shell,
            "stdout": "",
            "stderr": "",
            "duration_seconds": 0.0,
        }
        print(
            f"STEP {number:02d}/{total:02d} UNSUPPORTED exit=- name={name} diagnostic={shell}",
            flush=True,
        )
        return result
    started = time.monotonic()
    environment = os.environ.copy()
    environment.update({"CI": "true", "GITHUB_ACTIONS": "true"})
    try:
        with tempfile.TemporaryFile(mode="w+t", encoding="utf-8", errors="replace") as stdout_file, tempfile.TemporaryFile(
            mode="w+t", encoding="utf-8", errors="replace"
        ) as stderr_file:
            completed = subprocess.run(
                argv,
                cwd=root,
                env=environment,
                text=True,
                stdout=stdout_file,
                stderr=stderr_file,
                timeout=timeout,
                check=False,
            )
            stdout_file.seek(0)
            stderr_file.seek(0)
            stdout = stdout_file.read()
            stderr = stderr_file.read()
        duration = time.monotonic() - started
        status = "PASS" if completed.returncode == 0 else "FAIL"
        combined = "\n".join(
            part.strip() for part in (stderr, stdout) if part.strip()
        )
        diagnostic = "" if status == "PASS" else combined
        if status == "FAIL" and not diagnostic:
            diagnostic = f"command exited {completed.returncode} with no stdout or stderr"
        print(
            f"STEP {number:02d}/{total:02d} {status} exit={completed.returncode} "
            f"name={name} diagnostic={json.dumps(diagnostic, ensure_ascii=True)}",
            flush=True,
        )
        return {
            "number": number,
            "name": name,
            "status": status,
            "exit_code": completed.returncode,
            "diagnostic": diagnostic,
            "stdout": stdout,
            "stderr": stderr,
            "duration_seconds": round(duration, 3),
        }
    except subprocess.TimeoutExpired as exc:
        duration = time.monotonic() - started
        diagnostic = f"command exceeded timeout of {timeout} seconds"
        print(
            f"STEP {number:02d}/{total:02d} FAIL exit=timeout name={name} diagnostic={diagnostic}",
            flush=True,
        )
        return {
            "number": number,
            "name": name,
            "status": "FAIL",
            "exit_code": None,
            "diagnostic": diagnostic,
            "stdout": "",
            "stderr": "",
            "duration_seconds": round(duration, 3),
        }


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    workflow = (root / args.workflow).resolve()
    try:
        job, steps = load_job(workflow, args.job)
    except (OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    results = [
        execute_step(root, job, step, number, len(steps), args.timeout)
        for number, step in enumerate(steps, start=1)
    ]
    counts = {status: sum(row["status"] == status for row in results) for status in ("PASS", "FAIL", "UNSUPPORTED")}
    report = {
        "workflow": workflow.relative_to(root).as_posix(),
        "job": args.job,
        "declared_run_steps": len(steps),
        "counts": counts,
        "steps": results,
    }
    if args.json_out:
        output = Path(args.json_out)
        if not output.is_absolute():
            output = root / output
        output.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="ascii")
    print(
        "SUMMARY "
        f"declared={len(steps)} pass={counts['PASS']} fail={counts['FAIL']} "
        f"unsupported={counts['UNSUPPORTED']}",
        flush=True,
    )
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
