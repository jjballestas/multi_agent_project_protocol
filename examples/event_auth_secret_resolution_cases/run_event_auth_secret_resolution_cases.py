#!/usr/bin/env python3
"""Golden cases for SPEC-0082 event_auth secret resolution."""

from __future__ import annotations

import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.eventlog import (  # noqa: E402
    EventLogError,
    EventWriter,
    compute_event_prev_hash,
    sign_event,
    signable_event,
    verify_event_auth,
)
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir  # noqa: E402
from scripts.validate_collaboration_state import Validation, validate_event_auth_no_live_literal_secret  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="ascii")


def base_config(entry: dict[str, Any] | str, *, enabled: bool = True) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {"implementer": "Codex"},
        "event_auth": {
            "enabled": enabled,
            "method": "hmac-sha256",
            "issuer": "fixture-runtime",
            "audience": "fixture-event-log",
            "keys": {"Codex": entry},
        },
        "event_state": {"enabled": True, "materialize": True, "enforce": True, "authoritative": True},
    }


def event() -> dict[str, Any]:
    return {
        "seq": 1,
        "event_schema_version": "1.0",
        "type": "intent.applied",
        "aggregate_id": "TASK-0120",
        "aggregate_version": 1,
        "actor": "Codex",
        "actor_auth": {"method": "not_enforced_phase2"},
        "idempotency_key": "event-auth-secret-resolution",
        "fencing_token": None,
        "payload": {"transition": "fixture"},
        "applied": True,
        "ts": "2026-06-19T00:00:00Z",
    }


def append_fixture(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    write_json(root / "protocol.config.json", cfg)
    return EventWriter(root).append_event(
        event_type="intent.applied",
        aggregate_id="TASK-0120",
        actor_id="Codex",
        payload={"transition": "fixture"},
        idempotency_key="event-auth-secret-resolution",
        ts="2026-06-19T00:00:00Z",
    )


def case_keyfile(root: Path) -> dict[str, Any]:
    secret_file = root / "secrets" / "codex.key"
    secret_file.parent.mkdir(parents=True)
    secret_file.write_text("keyfile-secret\n", encoding="ascii")
    cfg = base_config({"key_id": "codex:keyfile", "secret_file": "secrets/codex.key"})
    signed = append_fixture(root, cfg)
    assert verify_event_auth(signed, cfg, root=root)["valid"] is True
    serialized = json.dumps(signed, sort_keys=True)
    assert "keyfile-secret" not in serialized
    assert "keyfile-secret" not in json.dumps(cfg, sort_keys=True)
    return {"case": "AC1-keyfile", "status": "pass"}


def case_env(root: Path) -> dict[str, Any]:
    old = os.environ.get("EVENTAUTH_CODEX_FIXTURE")
    os.environ["EVENTAUTH_CODEX_FIXTURE"] = "env-secret"
    try:
        cfg = base_config({"key_id": "codex:env", "secret_env": "EVENTAUTH_CODEX_FIXTURE"})
        signed = append_fixture(root, cfg)
        assert verify_event_auth(signed, cfg, root=root)["valid"] is True
        assert "env-secret" not in json.dumps(signed, sort_keys=True)
        return {"case": "AC2-env", "status": "pass"}
    finally:
        if old is None:
            os.environ.pop("EVENTAUTH_CODEX_FIXTURE", None)
        else:
            os.environ["EVENTAUTH_CODEX_FIXTURE"] = old


def case_fail_closed_file(root: Path) -> dict[str, Any]:
    cfg = base_config({"key_id": "codex:missing-file", "secret_file": "secrets/missing.key"})
    write_json(root / "protocol.config.json", cfg)
    try:
        EventWriter(root).append_event(
            event_type="intent.applied",
            aggregate_id="TASK-0120",
            actor_id="Codex",
            payload={"transition": "fixture"},
            idempotency_key="missing-file",
            ts="2026-06-19T00:00:00Z",
        )
    except EventLogError as exc:
        assert "unresolved_key" in str(exc)
    else:
        raise AssertionError("missing secret_file wrote an event")
    assert EventWriter(root).events() == []
    unsigned = event()
    unsigned["event_auth"] = {"method": "hmac-sha256", "key_id": "codex:missing-file", "signature": "bad"}
    assert verify_event_auth(unsigned, cfg, root=root)["reason"] == "unresolved_key"
    return {"case": "AC3-file-missing", "status": "pass"}


def case_fail_closed_env(root: Path) -> dict[str, Any]:
    os.environ.pop("EVENTAUTH_CODEX_MISSING", None)
    cfg = base_config({"key_id": "codex:missing-env", "secret_env": "EVENTAUTH_CODEX_MISSING"})
    write_json(root / "protocol.config.json", cfg)
    try:
        EventWriter(root).append_event(
            event_type="intent.applied",
            aggregate_id="TASK-0120",
            actor_id="Codex",
            payload={"transition": "fixture"},
            idempotency_key="missing-env",
            ts="2026-06-19T00:00:00Z",
        )
    except EventLogError as exc:
        assert "unresolved_key" in str(exc)
    else:
        raise AssertionError("missing secret_env wrote an event")
    assert EventWriter(root).events() == []
    unsigned = event()
    unsigned["event_auth"] = {"method": "hmac-sha256", "key_id": "codex:missing-env", "signature": "bad"}
    assert verify_event_auth(unsigned, cfg, root=root)["reason"] == "unresolved_key"
    return {"case": "AC3-env-missing", "status": "pass"}


def case_literal_gate() -> dict[str, Any]:
    validation = Validation()
    validate_event_auth_no_live_literal_secret(base_config({"key_id": "codex:inline", "secret": "literal"}), validation)
    assert validation.errors
    validation = Validation()
    validate_event_auth_no_live_literal_secret(base_config({"key_id": "codex:file", "secret_file": "secrets/codex.key"}), validation)
    assert validation.errors == []
    return {"case": "AC4-live-literal-gate", "status": "pass"}


def case_secret_not_in_hash(root: Path) -> dict[str, Any]:
    first = root / "secrets" / "first.key"
    second = root / "secrets" / "second.key"
    first.parent.mkdir(parents=True)
    first.write_text("first-secret\n", encoding="ascii")
    second.write_text("second-secret\n", encoding="ascii")
    cfg_a = base_config({"key_id": "codex:file", "secret_file": "secrets/first.key"})
    cfg_b = base_config({"key_id": "codex:file", "secret_file": "secrets/second.key"})
    signed_a = sign_event(deepcopy(event()), cfg_a, root=root)
    signed_b = sign_event(deepcopy(event()), cfg_b, root=root)
    assert signed_a["event_auth"]["signature"] != signed_b["event_auth"]["signature"]
    assert signable_event(signed_a) == signable_event(signed_b)
    assert compute_event_prev_hash(signed_a, "genesis") == compute_event_prev_hash(signed_b, "genesis")
    return {"case": "AC5-secret-outside-hash", "status": "pass"}


def case_path_safety(root: Path) -> dict[str, Any]:
    cases = [
        {"key_id": "codex:absolute", "secret_file": str((root / "secrets" / "codex.key").resolve())},
        {"key_id": "codex:traversal", "secret_file": "../outside.key"},
        {"key_id": "codex:outside", "secret_file": "tmp/codex.key"},
    ]
    for index, entry in enumerate(cases, start=1):
        cfg = base_config(entry)
        try:
            sign_event(deepcopy(event()), cfg, root=root)
        except EventLogError as exc:
            assert "unresolved_key" in str(exc)
        else:
            raise AssertionError(f"unsafe secret_file accepted: {index}")
    return {"case": "AC6-path-safety", "status": "pass"}


def case_literal_precedence(root: Path) -> dict[str, Any]:
    secret_file = root / "secrets" / "codex.key"
    secret_file.parent.mkdir(parents=True)
    secret_file.write_text("file-secret\n", encoding="ascii")
    cfg = base_config({"key_id": "codex:literal", "secret": "literal-secret", "secret_file": "secrets/codex.key"})
    signed = sign_event(deepcopy(event()), cfg, root=root)
    literal_cfg = base_config({"key_id": "codex:literal", "secret": "literal-secret"})
    assert signed["event_auth"]["signature"] == sign_event(deepcopy(event()), literal_cfg, root=root)["event_auth"]["signature"]
    return {"case": "AC7-literal-precedence", "status": "pass"}


CASES = [
    case_keyfile,
    case_env,
    case_fail_closed_file,
    case_fail_closed_env,
    lambda root: case_literal_gate(),
    case_secret_not_in_hash,
    case_path_safety,
    case_literal_precedence,
]


def main() -> int:
    results = []
    for index, case in enumerate(CASES, start=1):
        root = make_root_temp_dir(ROOT, f"event-auth-secret-resolution-{index}-")
        try:
            results.append(case(root))
        finally:
            remove_root_temp_dir(root, strict=True)
    print(json.dumps({"schema_version": "event_auth_secret_resolution_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0 if all(result["status"] == "pass" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
