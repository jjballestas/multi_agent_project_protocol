#!/usr/bin/env python3
"""Golden cases for event_auth keys in the runtime override."""

from __future__ import annotations

import base64
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives import serialization  # type: ignore
from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore

from runtime.eventlog import verify_actor_auth, verify_event_auth
from runtime.protocol_replay import protocol_state_drift
from runtime.submit_intent import IntentError, submit_intent
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


ANALISTA_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(3, 35)))


def public_b64(key: ed25519.Ed25519PrivateKey) -> str:
    raw = key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return base64.b64encode(raw).decode("ascii")


def private_pem(key: ed25519.Ed25519PrivateKey) -> str:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def config() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "protocol_version": "1.14.0",
        "adoption_tier": "runtime",
        "event_auth": {
            "enabled": True,
            "method": "hmac-sha256",
            "issuer": "fixture-runtime",
            "audience": "fixture-event-log",
            "keys": {"Codex": {"key_id": "codex:hmac", "secret_file": "secrets/eventauth-codex.key"}},
        },
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "slim_views_enabled": False,
            "chain_enabled": True,
            "agent_signatures_enabled": False,
            "signature_config": {
                "backend": "local-ed25519",
                "public_keys": {"analista:v1": public_b64(ANALISTA_KEY)},
            },
            "anchor_enabled": False,
        },
        "agent_registry": {
            "enabled": True,
            "agents": [
                {"id": "Codex", "enabled": True, "capabilities": ["implementer"]},
                {"id": "Analista", "enabled": True, "capabilities": ["reviewer"]},
            ],
        },
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def runtime_override(*, include_event_key: bool) -> dict[str, Any]:
    event_state: dict[str, Any] = {
        "actor_auth_enforce": True,
        "actor_auth_config": {
            "private_key_files": {"Analista": "secrets/analista-ed25519-private.pem"},
            "keyids": {"Analista": "analista:v1"},
        },
    }
    if include_event_key:
        event_state["event_auth"] = {
            "keys": {
                "Analista": {
                    "key_id": "analista-hmac:v1",
                    "secret_file": "secrets/eventauth-analista.key",
                }
            }
        }
    return {"event_state": event_state}


def seed_repo(root: Path, *, include_override: bool, include_event_key: bool = True) -> None:
    write_json(root / "protocol.config.json", config())
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "decisions": [], "active_tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    (root / "secrets").mkdir(parents=True, exist_ok=True)
    (root / "secrets/eventauth-codex.key").write_text("codex-hmac-secret\n", encoding="ascii")
    (root / "secrets/eventauth-analista.key").write_text("analista-hmac-secret\n", encoding="ascii")
    (root / "secrets/analista-ed25519-private.pem").write_text(private_pem(ANALISTA_KEY), encoding="ascii")
    if include_override:
        write_json(root / "event-state.runtime.json", runtime_override(include_event_key=include_event_key))


def intent() -> dict[str, Any]:
    return {
        "type": "claim",
        "op": "acquire",
        "claim": {
            "claim_id": "CLAIM-EVENT-AUTH-OVERRIDE",
            "task_id": "TASK-0001",
            "owner": "Analista",
            "status": "active",
            "started_at": "2026-06-27T00:00:00Z",
            "updated_at": "2026-06-27T00:00:00Z",
            "expires_at": "2026-06-28T00:00:00Z",
            "scope": ["Area_comun/reviews/"],
            "notes": "event auth override golden",
        },
    }


def case_override_signs_event_and_actor_auth() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-on-")
    try:
        seed_repo(root, include_override=True)
        result = submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        event = result["event"]
        event_auth = verify_event_auth(event, config(), root=root)
        actor_auth = verify_actor_auth(event, config(), root)
        ok = (
            event["event_auth"]["key_id"] == "analista-hmac:v1"
            and event_auth["valid"] is True
            and event["actor_auth"]["method"] == "ed25519"
            and actor_auth["valid"] is True
        )
        return "AC1-override-signs-event-and-actor-auth", ok, json.dumps({"event_auth": event_auth, "actor_auth": actor_auth}, sort_keys=True)
    finally:
        remove_root_temp_dir(root)


def case_config_and_chain_stay_intact() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-chain-")
    try:
        seed_repo(root, include_override=False)
        before = (root / "protocol.config.json").read_bytes()
        write_json(root / "event-state.runtime.json", runtime_override(include_event_key=True))
        submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        after = (root / "protocol.config.json").read_bytes()
        drift = protocol_state_drift(root)
        return "AC2-config-and-chain-intact", before == after and drift["has_drift"] is False, json.dumps(drift, sort_keys=True)
    finally:
        remove_root_temp_dir(root)


def case_without_override_fails_as_before() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-off-")
    try:
        seed_repo(root, include_override=False)
        try:
            submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError as exc:
            return "AC3-without-override-missing-key", "event auth signing key missing for actor: Analista" in str(exc), str(exc)
        return "AC3-without-override-missing-key", False, "unexpected success"
    finally:
        remove_root_temp_dir(root)


def case_rollback_removes_event_key() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-rollback-")
    try:
        seed_repo(root, include_override=True, include_event_key=False)
        try:
            submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError as exc:
            drift = protocol_state_drift(root)
            ok = "event auth signing key missing for actor: Analista" in str(exc) and drift["has_drift"] is False
            return "AC4-rollback-removes-event-key", ok, json.dumps({"error": str(exc), "drift": drift}, sort_keys=True)
        return "AC4-rollback-removes-event-key", False, "unexpected success"
    finally:
        remove_root_temp_dir(root)


def case_secret_independent_replay() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-secret-")
    clone = make_root_temp_dir(ROOT, ".event-auth-override-secret-clone-")
    try:
        seed_repo(root, include_override=True)
        submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        shutil.copytree(root, clone, dirs_exist_ok=True, ignore=shutil.ignore_patterns("secrets"))
        drift = protocol_state_drift(clone)
        return "AC5-secret-independent-replay", drift["has_drift"] is False, json.dumps(drift, sort_keys=True)
    finally:
        remove_root_temp_dir(root)
        remove_root_temp_dir(clone)


def case_malformed_override_fails_closed() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".event-auth-override-malformed-")
    try:
        seed_repo(root, include_override=False)
        write_json(root / "event-state.runtime.json", {"event_state": {"event_auth": {"method": "hmac-sha256"}}})
        try:
            submit_intent(root, "Analista", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError as exc:
            return "AC6-malformed-override-fails-closed", "unsupported keys" in str(exc), str(exc)
        return "AC6-malformed-override-fails-closed", False, "unexpected success"
    finally:
        remove_root_temp_dir(root)


def main() -> int:
    cases = [
        case_override_signs_event_and_actor_auth,
        case_config_and_chain_stay_intact,
        case_without_override_fails_as_before,
        case_rollback_removes_event_key,
        case_secret_independent_replay,
        case_malformed_override_fails_closed,
    ]
    results = [case() for case in cases]
    print(json.dumps({"event_auth_runtime_override_cases.v1": [{"name": name, "ok": ok, "detail": detail} for name, ok, detail in results]}, indent=2, sort_keys=True))
    return 0 if all(ok for _name, ok, _detail in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
