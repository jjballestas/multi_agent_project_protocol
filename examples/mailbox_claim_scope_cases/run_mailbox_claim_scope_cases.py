#!/usr/bin/env python3
"""Golden cases for mailbox claim file-scoping."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.submit_intent import IntentValidationError, validate_scope_authority
from scripts.validate_collaboration_state import Validation, validate_claims


def empty_state() -> dict:
    return {"claims": {"claims": []}}


def claim(scope: list[str], status: str = "active") -> dict:
    return {
        "claim_id": "CLAIM-MAILBOX-SCOPE-CASE",
        "task_id": "TASK-0001",
        "owner": "Codex",
        "status": status,
        "scope": scope,
    }


def submit_intent_rejects_mailbox_directory_scope() -> None:
    intent = {
        "kind": "claim",
        "op": "acquire",
        "owner": "Codex",
        "scope": ["Area_comun/mailbox/open/"],
    }
    try:
        validate_scope_authority(empty_state(), "Codex", intent)
    except IntentValidationError as exc:
        assert "mailbox claim must be file-scoped: Area_comun/mailbox/open/" in str(exc)
    else:
        raise AssertionError("mailbox directory scope was accepted")


def submit_intent_accepts_mailbox_file_scope() -> None:
    intent = {
        "kind": "claim",
        "op": "acquire",
        "owner": "Codex",
        "scope": ["Area_comun/mailbox/open/MSG-20260619-Codex-to-Arquitecto-ok.md"],
    }
    validate_scope_authority(empty_state(), "Codex", intent)


def validator_rejects_active_mailbox_directory_scope() -> None:
    validation = Validation()
    validate_claims({"claims": [claim(["Area_comun/mailbox/answered"])]}, validation)
    assert any("mailbox claim must be file-scoped: Area_comun/mailbox/answered" in error for error in validation.errors)


def validator_accepts_active_mailbox_file_scope() -> None:
    validation = Validation()
    validate_claims({"claims": [claim(["Area_comun/mailbox/archived/MSG-20260619-Codex-to-Operador-ok.md"])]}, validation)
    assert not validation.errors, validation.errors


def validator_does_not_break_released_history() -> None:
    validation = Validation()
    validate_claims({"claims": [claim(["Area_comun/mailbox/open/"], status="released")]}, validation)
    assert not any("mailbox claim must be file-scoped" in error for error in validation.errors)


def main() -> int:
    cases: list[Callable[[], None]] = [
        submit_intent_rejects_mailbox_directory_scope,
        submit_intent_accepts_mailbox_file_scope,
        validator_rejects_active_mailbox_directory_scope,
        validator_accepts_active_mailbox_file_scope,
        validator_does_not_break_released_history,
    ]
    for case in cases:
        case()
    print(f"OK: {len(cases)} mailbox claim scope cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
