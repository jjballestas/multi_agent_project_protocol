#!/usr/bin/env python3
"""Golden cases for the vendor-neutral LLM turn wrapper."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CASE_ROOT = Path(__file__).resolve().parent
FIXTURES = CASE_ROOT / "fixtures"
WRAPPER = ROOT / "runtime" / "llm_turn_wrapper.py"
FAKE_BACKEND = CASE_ROOT / "fake_backend.py"

sys.path.insert(0, str(ROOT))

from runtime import llm_turn_wrapper as wrapper_module  # noqa: E402


def command_arg(value: Path | str) -> str:
    text = str(value)
    if os.name == "nt":
        return '"' + text.replace('"', r'\"') + '"'
    return shlex.quote(text)


def fake_command(*, fixture: Path | None = None, exit_code: int = 0, sleep_seconds: float = 0.0, stderr: str = "") -> str:
    parts = [command_arg(sys.executable), command_arg(FAKE_BACKEND)]
    if fixture is not None:
        parts.extend(["--fixture", command_arg(fixture)])
    if exit_code:
        parts.extend(["--exit-code", str(exit_code)])
    if sleep_seconds:
        parts.extend(["--sleep-seconds", str(sleep_seconds)])
    if stderr:
        parts.extend(["--stderr", command_arg(stderr)])
    return " ".join(parts)


def run_wrapper(backend: str, *, timeout_seconds: float = 2.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(WRAPPER),
            "--backend",
            backend,
            "--timeout-seconds",
            str(timeout_seconds),
            "--root",
            str(ROOT),
        ],
        cwd=ROOT,
        input="fixture prompt",
        text=True,
        capture_output=True,
        check=False,
    )


def run_wrapper_from_env(backend: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["LLM_TURN_WRAPPER_BACKEND"] = backend
    return subprocess.run(
        [sys.executable, str(WRAPPER), "--timeout-seconds", "2", "--root", str(ROOT)],
        cwd=ROOT,
        input="fixture prompt",
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def read_fixture(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    payload = json.loads(text)
    return payload.get("report", payload)


def assert_success(name: str, fixture: Path) -> None:
    completed = run_wrapper(fake_command(fixture=fixture))
    assert completed.returncode == 0, {"case": name, "stderr": completed.stderr, "stdout": completed.stdout}
    assert completed.stderr == "", {"case": name, "stderr": completed.stderr}
    assert json.loads(completed.stdout) == read_fixture(fixture), {"case": name, "stdout": completed.stdout}
    assert "```" not in completed.stdout, {"case": name, "stdout": completed.stdout}


def case_clean_json() -> None:
    assert_success("clean", FIXTURES / "clean.json")


def case_fenced_prose_json() -> None:
    assert_success("fenced", FIXTURES / "fenced.md")


def case_wrapped_report_json() -> None:
    assert_success("wrapped", FIXTURES / "wrapped.json")


def case_backend_env_fallback() -> None:
    fixture = FIXTURES / "clean.json"
    completed = run_wrapper_from_env(fake_command(fixture=fixture))
    assert completed.returncode == 0, completed
    assert json.loads(completed.stdout) == read_fixture(fixture)


def case_backend_resolved_by_shutil_which() -> None:
    original_which = wrapper_module.shutil.which
    try:
        wrapper_module.shutil.which = lambda value: sys.executable if value == "fake-python-shim" else None
        backend = f"fake-python-shim {command_arg(FAKE_BACKEND)} --fixture {command_arg(FIXTURES / 'clean.json')}"
        stdout = wrapper_module.run_backend(backend=backend, prompt="fixture prompt", root=ROOT, timeout_seconds=2.0)
    finally:
        wrapper_module.shutil.which = original_which
    assert json.loads(stdout) == read_fixture(FIXTURES / "clean.json")


def case_backend_missing_fails_cleanly() -> None:
    completed = run_wrapper("definitely-missing-wrapper-backend-0090 --version")
    assert completed.returncode != 0, completed
    assert completed.stdout == "", completed.stdout
    assert "backend could not be started" in completed.stderr, completed.stderr


def case_schema_invalid_fails_cleanly() -> None:
    completed = run_wrapper(fake_command(fixture=FIXTURES / "invalid.json"))
    assert completed.returncode != 0, completed
    assert completed.stdout == "", completed.stdout
    assert "schema invalid" in completed.stderr, completed.stderr


def case_backend_failure_fails_cleanly() -> None:
    completed = run_wrapper(fake_command(exit_code=7, stderr="backend boom"))
    assert completed.returncode != 0, completed
    assert completed.stdout == "", completed.stdout
    assert "backend failed (7)" in completed.stderr, completed.stderr
    assert "backend boom" in completed.stderr, completed.stderr


def case_timeout_fails_before_invoker_timeout() -> None:
    started = time.monotonic()
    completed = run_wrapper(fake_command(sleep_seconds=5.0), timeout_seconds=0.5)
    elapsed = time.monotonic() - started
    assert completed.returncode != 0, completed
    assert completed.stdout == "", completed.stdout
    assert "timed out" in completed.stderr, completed.stderr
    assert elapsed < 4.0, elapsed


def case_live_preset_points_to_wrapper_and_stays_off_pilot() -> None:
    config = json.loads((ROOT / "protocol.config.json").read_text(encoding="utf-8-sig"))
    runtime = config["runtime"]
    command = runtime["llm_cli_presets"]["claude"]["command"]
    assert "runtime/llm_turn_wrapper.py" in command.replace("\\", "/"), command
    assert "--backend" in command and "claude -p" in command, command
    assert runtime["real_invoker"]["enabled"] is False
    assert runtime["supervised_autonomy"]["enabled"] is False


def main() -> int:
    cases = [
        case_clean_json,
        case_fenced_prose_json,
        case_wrapped_report_json,
        case_backend_env_fallback,
        case_backend_resolved_by_shutil_which,
        case_backend_missing_fails_cleanly,
        case_schema_invalid_fails_cleanly,
        case_backend_failure_fails_cleanly,
        case_timeout_fails_before_invoker_timeout,
        case_live_preset_points_to_wrapper_and_stays_off_pilot,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} LLM turn wrapper cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
