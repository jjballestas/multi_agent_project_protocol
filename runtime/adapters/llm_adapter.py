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
    sections = [
        "You are running one protocol runtime turn.",
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
    def from_command(cls, command: str, *, timeout_seconds: int = 120) -> "SubprocessInvoker":
        parts = split_command(command)
        if not parts:
            raise ValueError("--llm-command cannot be empty")
        return cls(command=parts, timeout_seconds=timeout_seconds)

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
