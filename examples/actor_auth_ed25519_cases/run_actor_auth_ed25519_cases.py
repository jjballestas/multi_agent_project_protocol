#!/usr/bin/env python3
"""Golden cases for submit_intent actor_auth Ed25519."""

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

from runtime.eventlog import EventWriter, actor_auth_signable_event, canonical_hash, verify_actor_auth
from runtime.protocol_replay import protocol_state_drift
from runtime.submit_intent import IntentError, submit_intent
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
OTHER_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(2, 34)))


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


def config(*, enforce: bool, keyid: str = "codex-test-key", public_key: str | None = None) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "protocol_version": "1.14.0",
        "adoption_tier": "runtime",
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "slim_views_enabled": False,
            "chain_enabled": False,
            "actor_auth_enforce": enforce,
            "actor_auth_config": {
                "private_key_files": {"Codex": "secrets/codex.pem"},
                "keyids": {"Codex": keyid},
            },
            "agent_signatures_enabled": False,
            "signature_config": {
                "backend": "local-ed25519",
                "public_keys": {keyid: public_key or public_b64(PRIVATE_KEY)},
            },
            "anchor_enabled": False,
        },
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True, "capabilities": ["implementer"]}]},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def seed_repo(root: Path, *, enforce: bool, with_secret: bool = True, public_key: str | None = None) -> None:
    write_json(root / "protocol.config.json", config(enforce=enforce, public_key=public_key))
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "decisions": [], "active_tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})
    if with_secret:
        (root / "secrets").mkdir(parents=True, exist_ok=True)
        (root / "secrets/codex.pem").write_text(private_pem(PRIVATE_KEY), encoding="ascii")


def intent() -> dict[str, Any]:
    return {
        "type": "claim",
        "op": "acquire",
        "claim": {
            "claim_id": "CLAIM-ACTOR-AUTH",
            "task_id": "TASK-0001",
            "owner": "Codex",
            "status": "active",
            "started_at": "2026-06-27T00:00:00Z",
            "updated_at": "2026-06-27T00:00:00Z",
            "expires_at": "2026-06-28T00:00:00Z",
            "scope": ["runtime/"],
            "notes": "actor auth golden",
        },
    }


def case_submit_intent_signs() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-case-")
    try:
        seed_repo(root, enforce=True)
        result = submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        auth = result["event"]["actor_auth"]
        ok = auth.get("method") == "ed25519" and auth.get("keyid") == "codex-test-key"
        return "AC1-submit-intent-signs", ok and verify_actor_auth(result["event"], config(enforce=True))["valid"], str(auth)
    finally:
        remove_root_temp_dir(root)


def case_off_byte_identical() -> tuple[str, bool, str]:
    roots = [make_root_temp_dir(ROOT, ".actor-auth-off-a-"), make_root_temp_dir(ROOT, ".actor-auth-off-b-")]
    try:
        write_json(roots[0] / "protocol.config.json", {key: value for key, value in config(enforce=False).items() if key != "event_state"})
        cfg = config(enforce=False)
        cfg["event_state"].pop("actor_auth_enforce", None)
        cfg["event_state"].pop("actor_auth_config", None)
        write_json(roots[0] / "protocol.config.json", cfg)
        write_json(roots[1] / "protocol.config.json", config(enforce=False))
        event_a = EventWriter(roots[0]).append_event(event_type="intent.applied", aggregate_id="TASK-0001", actor_id="Codex", payload={"x": 1}, ts="2026-06-27T00:00:00Z")
        event_b = EventWriter(roots[1]).append_event(event_type="intent.applied", aggregate_id="TASK-0001", actor_id="Codex", payload={"x": 1}, ts="2026-06-27T00:00:00Z")
        return "AC2-off-byte-identical", canonical_hash(event_a) == canonical_hash(event_b), event_a["actor_auth"]["method"]
    finally:
        for root in roots:
            remove_root_temp_dir(root)


def case_cross_attribution_rejected() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-cross-")
    try:
        seed_repo(root, enforce=True, public_key=public_b64(OTHER_KEY))
        try:
            result = submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError:
            return "AC3-cross-attribution-rejected", True, "write rejected"
        auth_result = verify_actor_auth(result["event"], config(enforce=True, public_key=public_b64(OTHER_KEY)))
        return "AC3-cross-attribution-rejected", auth_result["valid"] is False, str(auth_result)
    finally:
        remove_root_temp_dir(root)


def case_secret_independent_verify() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-secretless-")
    clone = make_root_temp_dir(ROOT, ".actor-auth-secretless-clone-")
    try:
        seed_repo(root, enforce=True)
        submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        shutil.copytree(root, clone, dirs_exist_ok=True, ignore=shutil.ignore_patterns("secrets"))
        drift = protocol_state_drift(clone)
        return "AC4-secret-independent-verify", drift.get("has_drift") is False, json.dumps(drift, sort_keys=True)
    finally:
        remove_root_temp_dir(root)
        remove_root_temp_dir(clone)


def case_sign_without_secret_fails() -> tuple[str, bool, str]:
    root = make_root_temp_dir(ROOT, ".actor-auth-no-secret-")
    try:
        seed_repo(root, enforce=True, with_secret=False)
        try:
            submit_intent(root, "Codex", intent(), timestamp="2026-06-27T00:00:00Z")
        except IntentError as exc:
            return "AC4-sign-without-secret-fails", "private signing key missing" in str(exc), str(exc)
        return "AC4-sign-without-secret-fails", False, "unexpected success"
    finally:
        remove_root_temp_dir(root)


def main() -> int:
    cases = [
        case_submit_intent_signs,
        case_off_byte_identical,
        case_cross_attribution_rejected,
        case_secret_independent_verify,
        case_sign_without_secret_fails,
    ]
    results = [case() for case in cases]
    print(json.dumps({"actor_auth_ed25519_cases.v1": [{"name": name, "ok": ok, "detail": detail} for name, ok, detail in results]}, indent=2, sort_keys=True))
    return 0 if all(ok for _name, ok, _detail in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
