#!/usr/bin/env python3
"""Golden cases for governed mailbox archive intents."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import build_fixture, read_json, write, write_json  # noqa: E402
from runtime.eventlog import events_in_log_order  # noqa: E402
from runtime.protocol_replay import protocol_state_drift, write_genesis_reference  # noqa: E402
from runtime.submit_intent import IntentError, submit_intent, submit_intents  # noqa: E402
from runtime.temp_paths import root_temp_dir  # noqa: E402


TASK_ID = "TASK-9200"
MESSAGE_ID = "MSG-mailbox-archive-case"
CLAIM_ID = "CLAIM-MAILBOX-ARCHIVE-CASE"
TIMESTAMP = "2026-06-20T00:00:00Z"
COMMIT = "mailboxcase123"
ACCOUNTABILITY = {"author": "Operador", "relayed_by": "Arquitecto", "endorsement": "none"}


def prepare_root(root: Path) -> None:
    build_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True, tier="runtime")
    for source in (ROOT / "runtime").glob("*.py"):
        target = root / "runtime" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    config = read_json(root / "protocol.config.json")
    config["agent_registry"] = {
        "enabled": True,
        "agents": [
            {"id": "Arquitecto", "enabled": True, "capabilities": ["orchestrator", "reviewer"]},
            {"id": "Codex", "enabled": True, "capabilities": ["implementer"]},
        ],
    }
    write_json(root / "protocol.config.json", config)
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/CLAIMS.slim.json", {"schema_version": "1.0", "view": "claims.slim", "claims": []})
    write_mailbox_message(root, MESSAGE_ID, "open")
    write_genesis_reference(root, actor_id="Arquitecto", timestamp=TIMESTAMP, commit=COMMIT)


def write_mailbox_message(root: Path, message_id: str, status: str) -> None:
    write(
        root / "Area_comun/mailbox/open" / f"{message_id}.md",
        "\n".join(
            [
                "---",
                f"message_id: {message_id}",
                "type: MESSAGE",
                "from: Arquitecto",
                "to: Codex",
                f"status: {status}",
                "requires_response: true",
                "one_line_summary: Mailbox archive case",
                "---",
                "",
                "# Mailbox archive case",
                "",
            ]
        ),
    )


def archive_intents(message_id: str = MESSAGE_ID) -> list[dict[str, Any]]:
    open_path = f"Area_comun/mailbox/open/{message_id}.md"
    archived_path = f"Area_comun/mailbox/archived/{message_id}.md"
    return [
        {
            "claim": {
                "op": "acquire",
                "claim": {
                    "claim_id": CLAIM_ID,
                    "task_id": TASK_ID,
                    "owner": "Arquitecto",
                    "scope": ["Area_comun/state/CLAIMS.json", open_path, archived_path],
                    "started_at": TIMESTAMP,
                    "updated_at": TIMESTAMP,
                    "expires_at": "2026-06-20T01:00:00Z",
                    "status": "active",
                    "notes": "Mailbox archive golden case.",
                },
                "idempotency_key": "mailbox-archive-case:claim-acquire",
            }
        },
        {
            "mailbox_archive": {
                "message_id": message_id,
                "idempotency_key": "mailbox-archive-case:archive",
                **ACCOUNTABILITY,
            }
        },
        {
            "claim": {
                "op": "release",
                "claim_id": CLAIM_ID,
                "task_id": TASK_ID,
                "owner": "Arquitecto",
                "idempotency_key": "mailbox-archive-case:claim-release",
            }
        },
    ]


def expect_error(fn, text: str) -> None:
    try:
        fn()
    except IntentError as exc:
        assert text in str(exc), str(exc)
        return
    raise AssertionError(f"expected error containing {text!r}")


def validator_stdout(root: Path) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_collaboration_state.py", "--root", "."],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def case_archive_happy_path_and_idempotent() -> None:
    with root_temp_dir(ROOT, ".mailbox-archive-positive-") as root:
        prepare_root(root)
        result = submit_intents(
            root,
            "Arquitecto",
            archive_intents(),
            timestamp=TIMESTAMP,
            commit=COMMIT,
            transaction_key="mailbox-archive-case:tx",
        )
        assert result["applied"] is True
        archive_event = next(event for event in result["events"] if event["payload"]["intent_type"] == "mailbox_archive")
        transition = archive_event["payload"]["transitions"]["mailbox_archive"]
        assert transition == {"message_id": MESSAGE_ID, "from": "open", "to": "archived", **ACCOUNTABILITY}
        assert not (root / "Area_comun/mailbox/open" / f"{MESSAGE_ID}.md").exists()
        archived = root / "Area_comun/mailbox/archived" / f"{MESSAGE_ID}.md"
        assert archived.exists()
        assert "\nstatus: archived\n" in archived.read_text(encoding="utf-8-sig")
        assert protocol_state_drift(root)["has_drift"] is False
        assert "OK: collaboration state is valid" in validator_stdout(root)

        before_count = len(events_in_log_order(root))
        repeated = submit_intents(
            root,
            "Arquitecto",
            archive_intents(),
            timestamp=TIMESTAMP,
            commit=COMMIT,
            transaction_key="mailbox-archive-case:tx",
        )
        assert repeated["deduped"] is True
        assert len(events_in_log_order(root)) == before_count
        assert "\nstatus: archived\n" in archived.read_text(encoding="utf-8-sig")
        assert protocol_state_drift(root)["has_drift"] is False


def case_archive_rejects_nonexistent_and_path_traversal() -> None:
    with root_temp_dir(ROOT, ".mailbox-archive-negative-paths-") as root:
        prepare_root(root)
        expect_error(
            lambda: submit_intent(
                root,
                "Arquitecto",
                {"mailbox_archive": {"message_id": "MSG-does-not-exist", **ACCOUNTABILITY}},
                timestamp=TIMESTAMP,
                commit=COMMIT,
            ),
            "mailbox message not found",
        )
        expect_error(
            lambda: submit_intent(
                root,
                "Arquitecto",
                {"mailbox_archive": {"message_id": "../MSG-escape", **ACCOUNTABILITY}},
                timestamp=TIMESTAMP,
                commit=COMMIT,
            ),
            "safe MSG-* id",
        )


def case_archive_rejects_extra_payload_and_missing_claim() -> None:
    with root_temp_dir(ROOT, ".mailbox-archive-negative-shape-") as root:
        prepare_root(root)
        expect_error(
            lambda: submit_intent(
                root,
                "Arquitecto",
                {"mailbox_archive": {"message_id": MESSAGE_ID, "task_status": {"task_id": TASK_ID}, **ACCOUNTABILITY}},
                timestamp=TIMESTAMP,
                commit=COMMIT,
            ),
            "unsupported fields",
        )
        expect_error(
            lambda: submit_intent(
                root,
                "Arquitecto",
                {"mailbox_archive": {"message_id": MESSAGE_ID, **ACCOUNTABILITY}},
                timestamp=TIMESTAMP,
                commit=COMMIT,
            ),
            "no active claim",
        )


def main() -> int:
    cases = [
        case_archive_happy_path_and_idempotent,
        case_archive_rejects_nonexistent_and_path_traversal,
        case_archive_rejects_extra_payload_and_missing_claim,
    ]
    failures: list[dict[str, Any]] = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2, sort_keys=True))
        return 1
    print(f"OK: {len(cases)} mailbox_archive golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
