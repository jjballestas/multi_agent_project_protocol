#!/usr/bin/env python3
"""Deterministic work router for the protocol runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .context import load_state, priority_value, task_is_claimed_by_other, tasks_by_id
except ImportError:  # pragma: no cover - direct script execution
    from context import load_state, priority_value, task_is_claimed_by_other, tasks_by_id


def select_next(state: dict[str, Any]) -> dict[str, Any] | None:
    tasks = tasks_by_id(state)

    human_gate = select_human_gate(state, tasks)
    if human_gate:
        return human_gate

    mailbox = select_mailbox_response(state)
    if mailbox:
        return mailbox

    review = select_review(tasks)
    if review:
        return review

    ready = select_ready_task(state, tasks)
    if ready:
        return ready

    return None


def select_human_gate(state: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    for task_id in sorted(tasks):
        task = tasks[task_id]
        text = json.dumps(task, ensure_ascii=False).upper()
        if task.get("status") == "blocked" and ("DECISION_REQUIRED" in text or "HUMAN_REQUIRED" in text):
            return {
                "action": "escalate",
                "task_id": task_id,
                "owner": "operador humano",
                "reason": "blocked task requires human or decision gate",
            }

    for message in state.get("mailbox_open") or []:
        text = json.dumps(message, ensure_ascii=False).lower()
        if "human_required" in text:
            return {
                "action": "escalate",
                "task_id": message.get("task_id") or "none",
                "owner": "operador humano",
                "reason": f"mailbox human gate: {message.get('message_id')}",
            }
    return None


def select_mailbox_response(state: dict[str, Any]) -> dict[str, Any] | None:
    candidates = []
    for message in state.get("mailbox_open") or []:
        if message.get("requires_response") is True and message.get("response_owner") not in (None, "", "none"):
            candidates.append(message)
    if not candidates:
        return None
    message = sorted(candidates, key=lambda item: str(item.get("message_id") or item.get("_path") or ""))[0]
    return {
        "action": "answer_mailbox",
        "task_id": message.get("task_id") or "none",
        "owner": message.get("response_owner"),
        "reason": f"pending mailbox response: {message.get('message_id')}",
    }


def select_review(tasks: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [task for task in tasks.values() if task.get("status") == "in_review"]
    if not candidates:
        return None
    task = sorted(candidates, key=lambda item: str(item.get("id")))[0]
    return {
        "action": "review",
        "task_id": task.get("id"),
        "owner": "Claude",
        "reason": "task is in_review and requires architect ratification",
    }


def select_ready_task(state: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for task in tasks.values():
        if task.get("status") != "ready":
            continue
        dependencies = task.get("depends_on") or []
        if any(tasks.get(dep, {}).get("status") != "done" for dep in dependencies):
            continue
        if task_is_claimed_by_other(task, state):
            continue
        candidates.append(task)
    if not candidates:
        return None
    task = sorted(candidates, key=lambda item: (-priority_value(item), str(item.get("id"))))[0]
    return {
        "action": "execute",
        "task_id": task.get("id"),
        "owner": task.get("owner"),
        "reason": f"ready task selected by priority {task.get('priority', 'normal')}",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Select the next runtime action.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    result = select_next(load_state(Path(args.root)))
    print(json.dumps(result, indent=2, ensure_ascii=False) if result else "null")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
