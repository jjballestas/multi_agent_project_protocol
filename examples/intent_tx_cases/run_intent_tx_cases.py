#!/usr/bin/env python3
"""Golden cases for transactional submit_intent and protocol re-genesis."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.eventlog import compute_event_prev_hash, read_jsonl_torn_safe  # noqa: E402
from runtime.protocol_replay import protocol_state_drift, validate_chain, write_genesis_reference  # noqa: E402
from runtime.regenesis import regenesis  # noqa: E402
from runtime.submit_intent import IntentApplyError, IntentError, submit_intent, submit_intents, verify_appended_events  # noqa: E402
from runtime.eventlog import EventWriter  # noqa: E402


TASK_ID = "TASK-9400"
NEXT_TASK_ID = "TASK-9401"
CLAIM_ID = f"CLAIM-{TASK_ID}-codex"
TIMESTAMP = "2026-06-08T00:00:00Z"
COMMIT = "txfixture123"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def protocol_config() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "runtime": {"enabled": True, "entrypoint": "runtime/orchestrator.py"},
        "agent_registry": {
            "enabled": True,
            "agents": [
                {
                    "id": "Codex",
                    "enabled": True,
                    "capabilities": ["implementer", "orchestrator", "reviewer", "test_engineer"],
                },
                {
                    "id": "Arquitecto",
                    "enabled": True,
                    "capabilities": ["implementer", "orchestrator", "reviewer", "test_engineer"],
                }
            ],
        },
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": False,
            "authoritative": False,
            "chain_enabled": True,
        },
        "domain_neutrality": {"enabled": True, "denylist": [], "scan_globs": [], "exempt_globs": []},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def task(task_id: str = TASK_ID, status: str = "in_progress", owner: str = "Codex") -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": owner,
        "status": status,
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "title": f"Intent tx fixture {task_id}",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "relates_to": [],
        "relevant_files": [],
        "deliverables": [],
        "blocked_by_questions": [],
        "updated_at": "2026-06-08",
    }


def claim(status: str = "active", claim_id: str = CLAIM_ID, task_id: str = TASK_ID, owner: str = "Codex") -> dict[str, Any]:
    return {
        "claim_id": claim_id,
        "task_id": task_id,
        "owner": owner,
        "status": status,
        "scope": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/TASK_INDEX.json#{NEXT_TASK_ID}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{NEXT_TASK_ID}",
            "Area_comun/state/CLAIMS.json",
            "Area_comun/state/PROJECT_STATE.json",
        ],
        "started_at": "2026-06-08",
        "updated_at": "2026-06-08",
        "expires_at": "2026-06-09",
        "notes": "intent tx fixture",
    }


def hot_docs(status: str = "in_progress", claim_status: str = "active") -> dict[str, Any]:
    task_payload = task(TASK_ID, status)
    return {
        "task_index": {"schema_version": "1.0", "tasks": [task_payload]},
        "project_state": {
            "status": "active",
            "decisions": ["DECISION-0001"],
            "active_tasks": [{"id": TASK_ID, "owner": "Codex", "status": status, "title": task_payload["title"]}],
        },
        "claims": {"schema_version": "1.0", "claims": [claim(claim_status)]},
    }


def write_hot_state(root: Path, docs: dict[str, Any], *, task_status: str = "in_progress") -> None:
    write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
    write_json(root / "Area_comun/state/PROJECT_STATE.json", docs["project_state"])
    write_json(root / "Area_comun/state/CLAIMS.json", docs["claims"])
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: {task_status}\n---\n\n# Fixture\n")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")


def build_fixture(root: Path, *, status: str = "in_progress", genesis: bool = True) -> None:
    write_json(root / "protocol.config.json", protocol_config())
    write_hot_state(root, hot_docs(status), task_status=status)
    write(root / "runtime/turn_schema.json", (ROOT / "runtime/turn_schema.json").read_text(encoding="utf-8-sig"))
    if genesis:
        write_genesis_reference(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)


def build_two_ready_fixture(root: Path) -> None:
    write_json(root / "protocol.config.json", protocol_config())
    task_a = task(TASK_ID, "ready", "Codex")
    task_b = task(NEXT_TASK_ID, "ready", "Arquitecto")
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [task_a, task_b]})
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {
            "status": "active",
            "decisions": [],
            "active_tasks": [
                {"id": TASK_ID, "owner": "Codex", "status": "ready", "title": task_a["title"]},
                {"id": NEXT_TASK_ID, "owner": "Arquitecto", "status": "ready", "title": task_b["title"]},
            ],
        },
    )
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: ready\n---\n\n# Fixture A\n")
    write(root / "Area_comun/tasks" / f"{NEXT_TASK_ID}.md", f"---\nid: {NEXT_TASK_ID}\nstatus: ready\n---\n\n# Fixture B\n")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")
    write(root / "runtime/turn_schema.json", (ROOT / "runtime/turn_schema.json").read_text(encoding="utf-8-sig"))
    write_genesis_reference(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)


def state_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.name != ".ledger.lock"
    }


def tx_intents() -> list[dict[str, Any]]:
    next_task = task(NEXT_TASK_ID, "ready")
    return [
        {
            "task_status": {
                "task_id": TASK_ID,
                "from": "in_progress",
                "to": "done",
                "idempotency_key": "tx-fixture:task-done",
            }
        },
        {"task_upsert": {"task": next_task, "idempotency_key": "tx-fixture:task-upsert"}},
        {"decision": {"decision_id": "DECISION-0099", "idempotency_key": "tx-fixture:decision"}},
        {"claim": {"op": "release", "claim_id": CLAIM_ID, "idempotency_key": "tx-fixture:claim-release"}},
    ]


def acquire_status_release_intents() -> list[dict[str, Any]]:
    new_claim = claim("active")
    return [
        {"claim": {"op": "acquire", "claim": new_claim, "idempotency_key": "tx-fixture:claim-acquire"}},
        {
            "task_status": {
                "task_id": TASK_ID,
                "from": "ready",
                "to": "in_progress",
                "idempotency_key": "tx-fixture:claim-then-status",
            }
        },
        {"claim": {"op": "release", "claim_id": CLAIM_ID, "idempotency_key": "tx-fixture:claim-release-after-acquire"}},
    ]


def acquire_and_start_intents(task_id: str, claim_id: str, owner: str) -> list[dict[str, Any]]:
    new_claim = claim("active", claim_id=claim_id, task_id=task_id, owner=owner)
    new_claim["scope"] = [
        f"Area_comun/state/CLAIMS.json#{claim_id}",
        f"Area_comun/state/TASK_INDEX.json#{task_id}",
        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
        f"Area_comun/tasks/{task_id}.md",
    ]
    return [
        {"claim": {"op": "acquire", "claim": new_claim, "idempotency_key": f"tx-fixture:{claim_id}:acquire"}},
        {
            "task_status": {
                "task_id": task_id,
                "from": "ready",
                "to": "in_progress",
                "idempotency_key": f"tx-fixture:{claim_id}:start",
            }
        },
    ]


def event_count(root: Path) -> int:
    return len(read_jsonl_torn_safe(root / "runtime/state/events.jsonl"))


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def case_transaction_closes_and_enqueues() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-close-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        assert len(result["events"]) == 4
        task_index = read_json(root / "Area_comun/state/TASK_INDEX.json")
        project_state = read_json(root / "Area_comun/state/PROJECT_STATE.json")
        claims = read_json(root / "Area_comun/state/CLAIMS.json")["claims"]
        tasks = {item["id"]: item for item in task_index["tasks"]}
        active = {item["id"]: item for item in project_state["active_tasks"]}
        assert tasks[TASK_ID]["status"] == "done", tasks
        assert active[TASK_ID]["status"] == "done", active
        assert tasks[NEXT_TASK_ID]["status"] == "ready", tasks
        assert active[NEXT_TASK_ID]["status"] == "ready", active
        assert "DECISION-0099" in project_state["decisions"]
        assert claims[0]["status"] == "released", claims
        assert protocol_state_drift(root)["has_drift"] is False


def case_validation_uses_intermediate_state() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-intermediate-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        docs = hot_docs("ready", "released")
        write_hot_state(root, docs, task_status="ready")
        regenesis(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)
        result = submit_intents(root, "Codex", acquire_status_release_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        assert len(result["events"]) == 3
        task_index = read_json(root / "Area_comun/state/TASK_INDEX.json")
        claims = read_json(root / "Area_comun/state/CLAIMS.json")["claims"]
        assert task_index["tasks"][0]["status"] == "in_progress"
        assert claims[0]["status"] == "released", claims
        assert protocol_state_drift(root)["has_drift"] is False


def case_transaction_rolls_back_on_materialization_failure() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-rollback-") as temp:
        root = Path(temp)
        build_fixture(root)
        before = state_bytes(root)
        try:
            submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT, fail_after_writes=1)
        except IntentError:
            pass
        else:
            raise AssertionError("transaction did not fail on simulated materialization failure")
        assert state_bytes(root) == before


def case_regenesis_clears_drift_and_allows_submit_intent() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-regenesis-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        docs = hot_docs("in_progress", "active")
        write_hot_state(root, docs, task_status="in_progress")
        assert protocol_state_drift(root)["has_drift"] is True
        before_count = event_count(root)
        result = regenesis(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)
        assert result["drift_after"]["has_drift"] is False
        assert event_count(root) == before_count + 1
        second = regenesis(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)
        assert second["deduped"] is True
        assert event_count(root) == before_count + 1
        submit_intent(
            root,
            "Codex",
            {
                "task_status": {
                    "task_id": TASK_ID,
                    "from": "in_progress",
                    "to": "done",
                    "idempotency_key": "tx-fixture:post-regenesis-status",
                }
            },
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        assert protocol_state_drift(root)["has_drift"] is False


def case_transaction_idempotent_retry_does_not_duplicate() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-idempotent-") as temp:
        root = Path(temp)
        build_fixture(root)
        first = submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        count_after_first = event_count(root)
        second = submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        assert second["deduped"] is True
        assert event_count(root) == count_after_first
        assert [event["seq"] for event in first["events"]] == [event["seq"] for event in second["events"]]


def case_idempotent_retry_repairs_divergent_materialized_state() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-idempotent-divergent-") as temp:
        root = Path(temp)
        build_fixture(root)
        submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        task_index = read_json(root / "Area_comun/state/TASK_INDEX.json")
        next(item for item in task_index["tasks"] if item["id"] == TASK_ID)["status"] = "in_progress"
        write_json(root / "Area_comun/state/TASK_INDEX.json", task_index)
        result = submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        assert result["deduped"] is True
        assert result["idempotency_reconciled"] is True
        repaired = read_json(root / "Area_comun/state/TASK_INDEX.json")
        assert next(item for item in repaired["tasks"] if item["id"] == TASK_ID)["status"] == "done"
        assert protocol_state_drift(root)["has_drift"] is False


def case_postwrite_verification_detects_injected_lost_event() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-tx-postwrite-lost-") as temp:
        root = Path(temp)
        build_fixture(root)
        result = submit_intents(root, "Codex", tx_intents(), timestamp=TIMESTAMP, commit=COMMIT)
        events = read_jsonl_torn_safe(root / "runtime/state/events.jsonl")
        lost = result["events"][1]
        kept = [event for event in events if int(event["seq"]) != int(lost["seq"])]
        (root / "runtime/state/events.jsonl").write_text(
            "".join(json.dumps(event, sort_keys=True, separators=(",", ":")) + "\n" for event in kept),
            encoding="utf-8",
            newline="\n",
        )
        try:
            verify_appended_events(EventWriter(root), result["events"])
        except IntentApplyError as exc:
            assert "own event missing" in str(exc)
            assert f"seq={lost['seq']}" in str(exc)
        else:
            raise AssertionError("post-write verification accepted an injected lost event")


def case_claim_rows_allow_distinct_and_reject_same() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-claim-rows-") as temp:
        root = Path(temp)
        build_two_ready_fixture(root)
        submit_intents(
            root,
            "Codex",
            acquire_and_start_intents(TASK_ID, "CLAIM-row-submit-A", "Codex"),
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        submit_intent(
            root,
            "Arquitecto",
            {
                "claim": {
                    "op": "acquire",
                    "claim": claim("active", "CLAIM-row-submit-B", NEXT_TASK_ID, "Arquitecto")
                    | {"scope": ["Area_comun/state/CLAIMS.json#CLAIM-row-submit-B"]},
                    "idempotency_key": "tx-fixture:claim-row-b",
                }
            },
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        try:
            submit_intent(
                root,
                "Arquitecto",
                {
                    "claim": {
                        "op": "acquire",
                        "claim": claim("active", "CLAIM-row-submit-C", NEXT_TASK_ID, "Arquitecto")
                        | {"scope": ["Area_comun/state/CLAIMS.json#CLAIM-row-submit-A"]},
                        "idempotency_key": "tx-fixture:claim-row-c",
                    }
                },
                timestamp=TIMESTAMP,
                commit=COMMIT,
            )
        except IntentError:
            pass
        else:
            raise AssertionError("claim acquire on an active claim row did not fail")


def case_concurrent_submit_intents_keep_linear_chain() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-concurrent-chain-") as temp:
        root = Path(temp)
        build_two_ready_fixture(root)
        envelopes = [
            {
                "actor_id": "Codex",
                "timestamp": TIMESTAMP,
                "commit": COMMIT,
                "intents": acquire_and_start_intents(TASK_ID, "CLAIM-concurrent-A", "Codex"),
            },
            {
                "actor_id": "Arquitecto",
                "timestamp": "2026-06-08T00:00:01Z",
                "commit": COMMIT,
                "intents": acquire_and_start_intents(NEXT_TASK_ID, "CLAIM-concurrent-B", "Arquitecto"),
            },
        ]
        paths = []
        for index, envelope in enumerate(envelopes):
            path = root / f"concurrent-{index}.json"
            write_json(path, envelope)
            paths.append(path)
        procs = [
            subprocess.Popen(
                [
                    sys.executable,
                    str(ROOT / "runtime/submit_intent.py"),
                    "--root",
                    str(root),
                    "--intents",
                    str(path),
                    "--output",
                    "-",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for path in paths
        ]
        outputs = [proc.communicate(timeout=20) for proc in procs]
        for proc, output in zip(procs, outputs):
            assert proc.returncode == 0, output[0] + output[1]
        events = read_jsonl_torn_safe(root / "runtime/state/events.jsonl")
        assert len(events) == 5, events
        config = read_json(root / "protocol.config.json")
        chain = validate_chain(events, config, root=root)
        assert chain["valid"] is True, chain
        for previous, current in zip(events, events[1:]):
            assert current["prev_hash"] == compute_event_prev_hash(current, str(previous["prev_hash"]))
        task_index = read_json(root / "Area_comun/state/TASK_INDEX.json")
        statuses = {item["id"]: item["status"] for item in task_index["tasks"]}
        assert statuses == {TASK_ID: "in_progress", NEXT_TASK_ID: "in_progress"}, statuses
        assert protocol_state_drift(root)["has_drift"] is False


def case_torn_jsonl_tail_is_repaired_before_append() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-torn-tail-") as temp:
        root = Path(temp)
        build_fixture(root)
        log_path = root / "runtime/state/events.jsonl"
        before = read_jsonl_torn_safe(log_path)
        assert len(before) == 1, before
        with log_path.open("ab") as handle:
            handle.write(b'{"seq":999,"type":"intent.applied"')

        result = submit_intent(
            root,
            "Codex",
            {"claim": {"op": "release", "claim_id": CLAIM_ID, "idempotency_key": "tx-fixture:torn-tail-release"}},
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )

        assert result["applied"] is True, result
        assert result["log_repair"], result
        events = read_jsonl_torn_safe(log_path)
        assert len(events) == 2, events
        assert events[-1]["idempotency_key"] == "tx-fixture:torn-tail-release", events[-1]
        config = read_json(root / "protocol.config.json")
        chain = validate_chain(events, config, root=root)
        assert chain["valid"] is True, chain
        assert events[-1]["prev_hash"] == compute_event_prev_hash(events[-1], str(events[-2]["prev_hash"]))
        assert protocol_state_drift(root)["has_drift"] is False


def case_middle_torn_jsonl_with_valid_after_fails_closed() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-middle-torn-") as temp:
        root = Path(temp)
        build_fixture(root)
        log_path = root / "runtime/state/events.jsonl"
        before_bytes = log_path.read_bytes()
        before_events = read_jsonl_torn_safe(log_path)
        assert len(before_events) == 1, before_events
        valid_after = {**before_events[0], "seq": 999, "idempotency_key": "tx-fixture:valid-after-torn"}
        with log_path.open("ab") as handle:
            handle.write(b'{"seq":998,"type":"intent.applied"\n')
            handle.write(json.dumps(valid_after, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n")
        corrupted_bytes = log_path.read_bytes()

        try:
            submit_intent(
                root,
                "Codex",
                {"claim": {"op": "release", "claim_id": CLAIM_ID, "idempotency_key": "tx-fixture:middle-torn"}},
                timestamp=TIMESTAMP,
                commit=COMMIT,
            )
        except Exception as exc:
            assert "invalid JSONL line" in str(exc), exc
            assert "refusing to truncate mid-file corruption" in str(exc), exc
        else:
            raise AssertionError("middle torn JSONL with valid event after it must fail closed")

        assert log_path.read_bytes() == corrupted_bytes
        assert event_count(root) == len(before_events)
        assert b"tx-fixture:middle-torn" not in log_path.read_bytes()
        assert before_bytes in corrupted_bytes


def case_powershell_wrappers_parity_if_available() -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return
    with tempfile.TemporaryDirectory(prefix="intent-tx-ps-") as temp:
        root = Path(temp)
        build_fixture(root)
        envelope = {
            "actor_id": "Codex",
            "timestamp": TIMESTAMP,
            "commit": COMMIT,
            "intents": tx_intents(),
        }
        envelope_path = root / "tx.json"
        write_json(envelope_path, envelope)
        result = run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "runtime/submit_intent.ps1"),
                "-Root",
                str(root),
                "-Intents",
                str(envelope_path),
            ]
        )
        assert result.returncode == 0, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        assert payload["transaction"]["intent_count"] == 4, result.stdout
        assert protocol_state_drift(root)["has_drift"] is False

    with tempfile.TemporaryDirectory(prefix="intent-tx-regenesis-ps-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        write_hot_state(root, hot_docs("in_progress", "active"), task_status="in_progress")
        result = run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "runtime/regenesis.ps1"),
                "-Root",
                str(root),
                "-ActorId",
                "Codex",
                "-Timestamp",
                TIMESTAMP,
                "-Commit",
                COMMIT,
            ]
        )
        assert result.returncode == 0, result.stdout + result.stderr
        payload = json.loads(result.stdout)
        assert payload["drift_after"]["has_drift"] is False


def main() -> int:
    cases = [
        case_transaction_closes_and_enqueues,
        case_validation_uses_intermediate_state,
        case_transaction_rolls_back_on_materialization_failure,
        case_regenesis_clears_drift_and_allows_submit_intent,
        case_transaction_idempotent_retry_does_not_duplicate,
        case_idempotent_retry_repairs_divergent_materialized_state,
        case_postwrite_verification_detects_injected_lost_event,
        case_claim_rows_allow_distinct_and_reject_same,
        case_concurrent_submit_intents_keep_linear_chain,
        case_torn_jsonl_tail_is_repaired_before_append,
        case_middle_torn_jsonl_with_valid_after_fails_closed,
        case_powershell_wrappers_parity_if_available,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} intent transaction golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
