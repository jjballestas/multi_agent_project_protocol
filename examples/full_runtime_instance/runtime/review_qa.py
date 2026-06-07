#!/usr/bin/env python3
"""Review/QA state helpers for the protocol runtime."""

from __future__ import annotations

import re
from pathlib import PurePath
from typing import Any


REVIEW_QA_STATUSES = {
    "changes_requested",
    "review_approved",
    "qa_pending",
    "qa_failed",
    "architect_review",
}

REVIEW_QA_EVENTS = {
    ("in_review", "changes_requested"): "reject_review",
    ("in_review", "review_approved"): "approve_review",
    ("in_review", "qa_pending"): "approve_review",
    ("qa_pending", "qa_failed"): "fail_qa",
    ("qa_pending", "architect_review"): "fail_qa",
    ("qa_pending", "done"): "pass_qa",
    ("qa_failed", "claimed"): "assign_fix",
    ("changes_requested", "claimed"): "assign_fix",
}


def author_of_record(task: dict[str, Any] | None) -> str:
    task = task or {}
    return str(task.get("original_author") or task.get("owner") or "")


def task_author(task: dict[str, Any] | None, payload: dict[str, Any] | None = None) -> str:
    return author_of_record(task)


def normalize_error_class(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}[t ][0-9:.+-z]+\b", "<ts>", text)
    text = re.sub(r"\b[0-9a-f]{8,}\b", "<id>", text)
    text = re.sub(r"\s+", " ", text)
    return text or "unknown"


def normalize_artifact_path(value: str) -> str:
    text = str(value or "").replace("\\", "/").strip()
    text = re.sub(r"^[A-Za-z]:", "", text)
    text = re.sub(r"/+", "/", text).strip("/")
    if not text:
        return "unknown"
    parts = PurePath(text).parts
    return "/".join(parts[-4:]).lower()


def failure_signature(check: dict[str, Any]) -> str:
    check_id = str(check.get("check_id") or check.get("id") or "unknown").strip().lower()
    error_class = normalize_error_class(str(check.get("error_class") or check.get("class") or check.get("error") or "unknown"))
    artifact = normalize_artifact_path(str(check.get("artifact_path") or check.get("path") or check.get("artifact") or "unknown"))
    return f"{check_id}|{error_class}|{artifact}"


def checks_with_signatures(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    signed: list[dict[str, Any]] = []
    for check in checks:
        if not isinstance(check, dict):
            continue
        item = dict(check)
        item["failure_signature"] = failure_signature(item)
        signed.append(item)
    return signed


def expected_event(from_status: str, to_status: str) -> str | None:
    return REVIEW_QA_EVENTS.get((from_status, to_status))


def prior_defects(task: dict[str, Any] | None) -> list[dict[str, Any]]:
    task = task or {}
    return [item for item in task.get("defect_log") or [] if isinstance(item, dict)]


def has_consecutive_failure(task: dict[str, Any], signed_checks: list[dict[str, Any]]) -> bool:
    defects = prior_defects(task)
    if not defects or not signed_checks:
        return False
    last = defects[-1]
    if last.get("event") != "fail_qa":
        return False
    previous = {
        str(item.get("failure_signature"))
        for item in last.get("checks_failed") or []
        if isinstance(item, dict) and item.get("failure_signature")
    }
    current = {str(item.get("failure_signature")) for item in signed_checks if item.get("failure_signature")}
    return bool(previous & current)


def max_qa_cycles(config: dict[str, Any] | None) -> int:
    config = config or {}
    policy = config.get("quality_policy")
    if not isinstance(policy, dict):
        policy = (config.get("runtime") or {}).get("quality_policy")
    if not isinstance(policy, dict):
        policy = {}
    try:
        value = int(policy.get("max_qa_cycles", 3))
    except (TypeError, ValueError):
        value = 3
    return max(1, value)


def qa_attempts_after_failure(task: dict[str, Any] | None) -> int:
    task = task or {}
    try:
        return int(task.get("qa_attempts") or 0) + 1
    except (TypeError, ValueError):
        return 1
