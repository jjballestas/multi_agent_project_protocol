#!/usr/bin/env python3
"""LLM adapter with pluggable invokers.

The default invoker for tests is recorded and reads local transcripts. A real
agent invocation is available only through an explicit subprocess invoker.
"""

from __future__ import annotations

import hashlib
import ctypes
import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

try:
    from .base import ContextPack, TurnReport
except ImportError:  # pragma: no cover - direct script execution
    from base import ContextPack, TurnReport


class Invoker(Protocol):
    name: str

    def run(self, *, prompt: str, root: Path) -> TurnReport:
        """Return one turn report produced for the prompt."""


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def context_file(root: Path, relative_path: str) -> str:
    path = root / relative_path
    if not path.exists() or not path.is_file():
        return f"[missing: {relative_path}]"
    return path.read_text(encoding="utf-8-sig")


def build_prompt(*, context: ContextPack, root: Path) -> str:
    task = context.task or {}
    unit = context.unit or {}
    task_id = str(task.get("id") or unit.get("task_id") or "none")
    owner = str(unit.get("owner") or task.get("owner") or "")
    status = str(task.get("status") or "ready")
    scope = task.get("relevant_files") or task.get("deliverables") or []
    sections = [
        f"You are agent {owner}, executing ONE protocol runtime turn for task {task_id}.",
        "Do the task's work NOW: edit ONLY the file(s) within the task scope to accomplish its objective;"
        " do not read or change anything outside that scope.",
        f"task scope (files you may edit): {json.dumps(list(scope), ensure_ascii=False)}",
        "When done, output ONLY a single JSON object (no prose, no markdown code fences) that is a turn report"
        " conforming to runtime/turn_schema.json, with these fields:",
        f'  "turn_id": any unique string; "task_id": "{task_id}"; "agent": "{owner}";',
        '  "outcome": "done" if you completed the work (else "blocked" with a one-line summary);',
        '  "summary": one sentence; "changed_paths": the EXACT list of files you edited;',
        '  "commit_message": a short conventional-commit line;',
        f'  "transitions": {{"task_status": {{"from": "{status}", "to": "in_review"}}}}.',
        'If you cannot complete the work within scope, make NO edits and return "outcome": "blocked" with'
        ' "changed_paths": [] and omit the task_status transition.',
        "Return only a JSON turn report conforming to runtime/turn_schema.json.",
        f"turn_index: {context.turn_index}",
        f"unit: {json.dumps(unit, ensure_ascii=False, sort_keys=True)}",
        f"task: {json.dumps(task, ensure_ascii=False, sort_keys=True)}",
        f"decision_ids: {json.dumps(list(context.decision_ids), ensure_ascii=False)}",
    ]
    for spec_path in context.spec_paths:
        sections.append(f"--- file: {spec_path} ---")
        sections.append(context_file(root, spec_path))
    return "\n".join(sections)


def split_command(command: str) -> tuple[str, ...]:
    if os.name != "nt":
        return tuple(shlex.split(command))

    argc = ctypes.c_int()
    ctypes.windll.shell32.CommandLineToArgvW.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_int)]
    ctypes.windll.shell32.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
    ctypes.windll.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    ctypes.windll.kernel32.LocalFree.restype = ctypes.c_void_p
    argv = ctypes.windll.shell32.CommandLineToArgvW(command, ctypes.byref(argc))
    if not argv:
        raise ValueError("could not parse --llm-command")
    try:
        return tuple(argv[index] for index in range(argc.value))
    finally:
        ctypes.windll.kernel32.LocalFree(argv)


@dataclass(frozen=True)
class ResolvedLLMCommand:
    command: str
    label: str


def runtime_config(config: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(config, dict):
        return {}
    runtime = config.get("runtime")
    return runtime if isinstance(runtime, dict) else {}


def configured_llm_presets(config: dict[str, Any] | None) -> dict[str, str]:
    runtime = runtime_config(config)
    raw = runtime.get("llm_cli_presets")
    if not isinstance(raw, dict):
        return {}

    presets: dict[str, str] = {}
    for name, value in raw.items():
        key = str(name or "").strip()
        if not key:
            continue
        if isinstance(value, str):
            command = value.strip()
        elif isinstance(value, dict):
            command = str(value.get("command") or "").strip()
        else:
            command = ""
        if command:
            presets[key] = command
    return presets


def resolve_llm_command(
    config: dict[str, Any] | None,
    *,
    command: str | None = None,
    preset: str | None = None,
) -> ResolvedLLMCommand | None:
    command_text = str(command or "").strip()
    preset_name = str(preset or "").strip()
    if command_text and preset_name:
        raise ValueError("choose either --llm-command or --llm-preset")
    if command_text:
        return ResolvedLLMCommand(command=command_text, label="command")
    if not preset_name:
        return None

    presets = configured_llm_presets(config)
    preset_command = presets.get(preset_name)
    if not preset_command:
        available = ", ".join(sorted(presets)) or "none"
        raise ValueError(f"unknown --llm-preset: {preset_name} (available: {available})")
    return ResolvedLLMCommand(command=preset_command, label=f"preset:{preset_name}")


def real_invoker_activation_error(config: dict[str, Any] | None) -> str | None:
    runtime = runtime_config(config)
    raw = runtime.get("real_invoker")
    if not isinstance(raw, dict) or raw.get("enabled") is not True:
        return "runtime.real_invoker.enabled is not true"

    decision_id = str(raw.get("activation_decision") or raw.get("decision_id") or "").strip()
    approved_by = str(raw.get("approved_by") or raw.get("approver") or "").strip()
    approved_at = str(raw.get("approved_at") or raw.get("ratified_at") or "").strip()
    missing = [
        name
        for name, value in (
            ("activation_decision", decision_id),
            ("approved_by", approved_by),
            ("approved_at", approved_at),
        )
        if not value
    ]
    if missing:
        return "runtime.real_invoker missing " + ", ".join(missing)
    return None


@dataclass(frozen=True)
class RecordedInvoker:
    transcript_path: Path
    name: str = "recorded"

    def run(self, *, prompt: str, root: Path) -> TurnReport:
        path = self.transcript_path
        if not path.is_absolute():
            path = root / path
        transcript = read_json(path)
        if transcript.get("format") not in {None, "recorded_invoker.v1"}:
            raise ValueError(f"unsupported recorded invoker format: {transcript.get('format')}")
        for expected in transcript.get("expected_prompt_contains") or []:
            if str(expected) not in prompt:
                raise ValueError(f"recorded prompt expectation not met: {expected}")
        report = transcript.get("report", transcript.get("turn_report"))
        if not isinstance(report, dict):
            raise ValueError(f"recorded invoker transcript has no report: {path}")
        return dict(report)


@dataclass(frozen=True)
class SubprocessInvoker:
    command: tuple[str, ...]
    timeout_seconds: int = 120
    name: str = "subprocess"

    @classmethod
    def from_command(cls, command: str, *, timeout_seconds: int = 120, name: str = "subprocess") -> "SubprocessInvoker":
        parts = split_command(command)
        if not parts:
            raise ValueError("--llm-command cannot be empty")
        return cls(command=parts, timeout_seconds=timeout_seconds, name=name)

    def run(self, *, prompt: str, root: Path) -> TurnReport:
        completed = subprocess.run(
            list(self.command),
            cwd=root,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=self.timeout_seconds,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"llm subprocess failed ({completed.returncode}): {completed.stderr.strip()}")
        payload = json.loads(completed.stdout)
        report = payload.get("report", payload) if isinstance(payload, dict) else None
        if not isinstance(report, dict):
            raise ValueError("llm subprocess stdout must be a JSON object or {report: object}")
        return report


@dataclass(frozen=True)
class LLMAdapter:
    invoker: Invoker
    name: str = "llm"

    def run_turn(self, *, context: ContextPack, root: Path) -> TurnReport:
        prompt = build_prompt(context=context, root=root)
        report = self.invoker.run(prompt=prompt, root=root)
        report.setdefault("adapter", {"name": self.name, "invoker": self.invoker.name})
        report.setdefault("prompt_sha256", hashlib.sha256(prompt.encode("utf-8")).hexdigest())
        return report
