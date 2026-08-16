#!/usr/bin/env python3
"""Golden cases for agent signature attestations."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore
from cryptography.hazmat.primitives import serialization  # type: ignore

from runtime.eventlog import attestation_signing_payload, canonical_hash, compute_event_prev_hash, compute_genesis_prev_hash
from runtime.protocol_replay import validate_agent_signatures, validate_chain


PRIVATE_SEED = bytes(range(1, 33))
PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(PRIVATE_SEED)
PUBLIC_KEY = PRIVATE_KEY.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)
PUBLIC_KEY_B64 = base64.b64encode(PUBLIC_KEY).decode("ascii")


def config(*, enabled: bool = True, chain: bool = False) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {"implementer": "Codex", "architect": "Claude"},
        "agent_registry": {
            "enabled": True,
            "agents": [
                {"id": "Codex", "enabled": True, "capabilities": ["implementer"]},
                {"id": "Claude", "enabled": True, "capabilities": ["reviewer", "orchestrator"]},
            ],
        },
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "chain_enabled": chain,
            "agent_signatures_enabled": enabled,
            "signature_config": {
                "backend": "local-ed25519",
                "public_keys": {
                    "codex-test-key": PUBLIC_KEY_B64,
                    "claude-test-key": PUBLIC_KEY_B64,
                },
            },
        },
    }


def predicate(agent_id: str = "Codex", role: str = "implementer", task_id: str = "TASK-0102") -> dict[str, Any]:
    return {
        "agent_id": agent_id,
        "agent_model": "golden-model",
        "task_id": task_id,
        "decision_id": "DECISION-0029",
        "role": role,
        "inputs_trust_boundary": "internal",
        "outputs_scope": ["runtime/eventlog.py"],
        "timestamp_claimed": "2026-06-13T00:00:00Z",
        "turn_index": 1,
        "human_checkpoint": False,
    }


def sign(subject_digest: str, pred: dict[str, Any], keyid: str = "codex-test-key") -> dict[str, Any]:
    raw = PRIVATE_KEY.sign(attestation_signing_payload(subject_digest, pred))
    return {"keyid": keyid, "algorithm": "ed25519", "sig": base64.b64encode(raw).decode("ascii")}


def attestation_event(seq: int = 1, *, agent_id: str = "Codex", pred: dict[str, Any] | None = None) -> dict[str, Any]:
    pred = pred or predicate(agent_id=agent_id)
    subject = "sha256:" + canonical_hash({"turn_id": "TURN-1", "task_id": pred.get("task_id"), "agent": agent_id})
    return {
        "seq": seq,
        "event_schema_version": "1.0",
        "type": "agent.attestation",
        "aggregate_id": str(pred.get("task_id") or "TASK-0102"),
        "aggregate_version": seq,
        "actor": agent_id,
        "actor_auth": {"method": "not_enforced_phase2"},
        "idempotency_key": f"sig:{seq}:{agent_id}",
        "fencing_token": None,
        "payload": {
            "agent_id": agent_id,
            "subject_digest": subject,
            "subject_reference": "TURN-1",
            "predicate": pred,
            "signature": sign(subject, pred, "claude-test-key" if agent_id == "Claude" else "codex-test-key"),
            "verification_backend": "local-ed25519",
        },
        "applied": False,
        "ts": f"2026-06-13T00:00:{seq:02d}Z",
    }


def run_case(name: str, fn) -> dict[str, Any]:
    result = fn()
    passed = bool(result.pop("passed"))
    return {"case": name, "status": "pass" if passed else "fail", **result}


def case_off_by_default() -> dict[str, Any]:
    event = attestation_event()
    result = validate_agent_signatures([event], config(enabled=False))
    return {"passed": result["valid"] is True and result["checked"] == 0, "message": result["reason"]}


def case_valid_signature() -> dict[str, Any]:
    result = validate_agent_signatures([attestation_event()], config())
    return {"passed": result["valid"] is True and result["checked"] == 1, "message": result["reason"]}


def case_invalid_signature() -> dict[str, Any]:
    event = attestation_event()
    event["payload"]["signature"]["sig"] = "A" + event["payload"]["signature"]["sig"][1:]
    result = validate_agent_signatures([event], config())
    return {
        "passed": result["valid"] is False
        and result["findings"][0]["error"] == "invalid_signature"
        and result["invalid_signature"] == 1,
        "message": result["reason"],
    }


def case_unknown_agent() -> dict[str, Any]:
    event = attestation_event(agent_id="UnknownAgent", pred=predicate(agent_id="UnknownAgent"))
    result = validate_agent_signatures([event], config())
    return {"passed": result["valid"] is False and result["findings"][0]["error"] == "unknown_agent", "message": result["reason"]}


def case_reviewer_attestation() -> dict[str, Any]:
    pred = predicate(agent_id="Claude", role="reviewer", task_id="TASK-0102")
    pred["reviewed_work_agent"] = "Codex"
    pred["reviewed_task"] = "TASK-0102"
    pred["verdict"] = "approved"
    result = validate_agent_signatures([attestation_event(agent_id="Claude", pred=pred)], config())
    return {"passed": result["valid"] is True, "message": result["reason"]}


def case_predicate_incomplete() -> dict[str, Any]:
    pred = predicate()
    pred.pop("task_id")
    event = attestation_event(pred=pred)
    result = validate_agent_signatures([event], config())
    return {"passed": result["valid"] is False and "missing predicate field" in result["findings"][0]["error"], "message": result["reason"]}


def case_prev_hash_and_sig() -> dict[str, Any]:
    cfg = config(chain=True)
    events = [attestation_event(1), attestation_event(2)]
    previous = compute_genesis_prev_hash(ROOT / "protocol.config.json")
    for event in events:
        event["prev_hash"] = compute_event_prev_hash(event, previous)
        previous = event["prev_hash"]
    sigs = validate_agent_signatures(events, cfg)
    chain = validate_chain(events, cfg, root=ROOT)
    return {"passed": sigs["valid"] is True and chain["valid"] is True, "message": f"{sigs['reason']}; {chain['reason']}"}


def case_determinism() -> dict[str, Any]:
    event_a = attestation_event()
    event_b = attestation_event()
    return {
        "passed": event_a["payload"]["subject_digest"] == event_b["payload"]["subject_digest"]
        and event_a["payload"]["signature"]["sig"] == event_b["payload"]["signature"]["sig"],
        "message": "deterministic",
    }


def case_legacy_no_signatures() -> dict[str, Any]:
    legacy_event = {"seq": 1, "type": "intent.applied", "payload": {"value": "legacy"}}
    result = validate_agent_signatures([legacy_event], config())
    return {"passed": result["valid"] is True and result["checked"] == 0, "message": result["reason"]}


def case_enable_post_hoc() -> dict[str, Any]:
    legacy_event = {"seq": 1, "type": "intent.applied", "payload": {"value": "legacy"}}
    signed = attestation_event(seq=2)
    result = validate_agent_signatures([legacy_event, signed], config())
    return {"passed": result["valid"] is True and result["checked"] == 1, "message": result["reason"]}


CASES = [
    ("GC-1-off-by-default", case_off_by_default),
    ("GC-2-ed25519-valid", case_valid_signature),
    ("GC-3-invalid-signature", case_invalid_signature),
    ("GC-4-unknown-agent", case_unknown_agent),
    ("GC-5-reviewer-attestation", case_reviewer_attestation),
    ("GC-6-predicate-incomplete", case_predicate_incomplete),
    ("GC-7-prev-hash-and-sig", case_prev_hash_and_sig),
    ("GC-8-determinism", case_determinism),
    ("GC-9-legacy-no-signatures", case_legacy_no_signatures),
    ("GC-10-enable-post-hoc", case_enable_post_hoc),
]


def main() -> int:
    results = [run_case(name, fn) for name, fn in CASES]
    print(json.dumps({"schema_version": "agent_signature_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0 if all(item["status"] == "pass" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
