#!/usr/bin/env python3
"""Normalize a non-interactive LLM CLI response into one clean turn report."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from json import JSONDecodeError
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised as a clean CLI failure.
    jsonschema = None  # type: ignore[assignment]

try:
    from .adapters.llm_adapter import split_command
except ImportError:  # pragma: no cover - direct script execution
    from adapters.llm_adapter import split_command


DEFAULT_TIMEOUT_SECONDS = 100.0
MAX_TIMEOUT_SECONDS = 119.0
REQUIRED_REPORT_KEYS = {
    "turn_id",
    "task_id",
    "agent",
    "outcome",
    "summary",
    "changed_paths",
    "commit_message",
}


class WrapperError(RuntimeError):
    """Expected wrapper failure that should be reported without a traceback."""


def default_schema_path() -> Path:
    return Path(__file__).resolve().with_name("turn_schema.json")


def clean_backend_from_env() -> str:
    return str(os.environ.get("LLM_TURN_WRAPPER_BACKEND") or "").strip()


def normalize_timeout(value: float) -> float:
    if value <= 0:
        raise WrapperError("--timeout-seconds must be greater than 0")
    if value >= 120:
        raise WrapperError("--timeout-seconds must be lower than the invoker timeout (120s)")
    return min(value, MAX_TIMEOUT_SECONDS)


def unwrap_report(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    report = payload.get("report")
    if isinstance(report, dict):
        return dict(report)
    return dict(payload)


def json_candidates(text: str) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    decoder = json.JSONDecoder()
    stripped = text.strip()
    if not stripped:
        return candidates

    try:
        direct = unwrap_report(json.loads(stripped))
        if direct is not None:
            candidates.append(direct)
    except JSONDecodeError:
        pass

    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            payload, _ = decoder.raw_decode(text[index:])
        except JSONDecodeError:
            continue
        report = unwrap_report(payload)
        if report is not None and report not in candidates:
            candidates.append(report)
    return candidates


def extract_report(text: str) -> dict[str, Any]:
    candidates = json_candidates(text)
    if not candidates:
        raise WrapperError("backend stdout did not contain a JSON object turn report")
    for candidate in candidates:
        if REQUIRED_REPORT_KEYS.issubset(candidate):
            return candidate
    return candidates[0]


def load_schema(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise WrapperError(f"turn schema not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except JSONDecodeError as exc:
        raise WrapperError(f"turn schema is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise WrapperError("turn schema must be a JSON object")
    return payload


def validate_report(report: dict[str, Any], schema_path: Path) -> None:
    if jsonschema is None:
        raise WrapperError("jsonschema package is required to validate turn reports")
    schema = load_schema(schema_path)
    try:
        jsonschema.Draft7Validator.check_schema(schema)
        errors = sorted(jsonschema.Draft7Validator(schema).iter_errors(report), key=lambda item: list(item.path))
    except jsonschema.SchemaError as exc:
        raise WrapperError(f"turn schema is invalid: {exc.message}") from exc
    if errors:
        details = []
        for error in errors[:3]:
            path = ".".join(str(part) for part in error.path) or "<root>"
            details.append(f"{path}: {error.message}")
        if len(errors) > 3:
            details.append(f"... {len(errors) - 3} more")
        raise WrapperError("turn report schema invalid: " + "; ".join(details))


def resolve_backend_command(command: tuple[str, ...]) -> list[str]:
    resolved = shutil.which(command[0])
    if resolved:
        return [resolved, *command[1:]]
    return list(command)


def run_backend(*, backend: str, prompt: str, root: Path, timeout_seconds: float) -> str:
    command = split_command(backend)
    if not command:
        raise WrapperError("--backend cannot be empty")
    resolved_command = resolve_backend_command(command)
    try:
        completed = subprocess.run(
            resolved_command,
            cwd=root,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise WrapperError(f"backend timed out after {timeout_seconds:g}s") from exc
    except OSError as exc:
        raise WrapperError(f"backend could not be started: {exc}") from exc
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip()
        suffix = f": {stderr}" if stderr else ""
        raise WrapperError(f"backend failed ({completed.returncode}){suffix}")
    return completed.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Emit a clean runtime turn-report JSON from a backend CLI.")
    parser.add_argument("--backend", help="Backend command to run non-interactively; env: LLM_TURN_WRAPPER_BACKEND.")
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=float(os.environ.get("LLM_TURN_WRAPPER_TIMEOUT_SECONDS") or DEFAULT_TIMEOUT_SECONDS),
        help="Backend timeout, lower than 120 seconds. Default: 100.",
    )
    parser.add_argument("--root", default=".", help="Working directory for the backend command.")
    parser.add_argument("--schema", default=str(default_schema_path()), help="Turn schema JSON path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        backend = str(args.backend or clean_backend_from_env()).strip()
        if not backend:
            raise WrapperError("--backend or LLM_TURN_WRAPPER_BACKEND is required")
        timeout_seconds = normalize_timeout(float(args.timeout_seconds))
        prompt = sys.stdin.read()
        stdout = run_backend(backend=backend, prompt=prompt, root=Path(args.root), timeout_seconds=timeout_seconds)
        report = extract_report(stdout)
        validate_report(report, Path(args.schema))
        sys.stdout.write(json.dumps(report, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n")
        return 0
    except WrapperError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
