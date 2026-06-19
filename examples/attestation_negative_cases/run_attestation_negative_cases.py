#!/usr/bin/env python3
"""SPEC-0081 AC3 binary negative goldens for #4 attestations."""

from __future__ import annotations

import base64
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives import serialization  # type: ignore
from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore

from runtime.eventlog import EventWriter, attestation_signing_payload, canonical_hash
from runtime.protocol_replay import validate_agent_signatures, validate_chain, verify_anchor_monotonicity
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


CODEX_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
CLAUDE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(2, 34)))


def public_b64(key: ed25519.Ed25519PrivateKey) -> str:
    return base64.b64encode(key.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode(
        "ascii"
    )


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="ascii")


def config(root: Path) -> dict[str, Any]:
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
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "chain_enabled": True,
            "agent_signatures_enabled": True,
            "signature_config": {
                "backend": "local-ed25519",
                "public_keys": {
                    "codex-test-key": public_b64(CODEX_KEY),
                    "claude-test-key": public_b64(CLAUDE_KEY),
                },
            },
            "anchor_enabled": True,
            "anchor_config": {
                "backend": "git-remote",
                "remote_url": str(root / "audit-remote"),
                "identity": "runtime-anchor-negative",
                "interval_seconds": 0,
            },
        },
    }


def predicate(index: int, agent_id: str = "Codex") -> dict[str, Any]:
    return {
        "agent_id": agent_id,
        "agent_model": "golden-model",
        "task_id": "TASK-0117",
        "decision_id": "DECISION-0039",
        "role": "implementer" if agent_id == "Codex" else "reviewer",
        "inputs_trust_boundary": "internal",
        "outputs_scope": ["examples/attestation_negative_cases"],
        "timestamp_claimed": f"2026-06-19T01:{index:02d}:00Z",
        "turn_index": index,
        "human_checkpoint": False,
    }


def signature(subject_digest: str, pred: dict[str, Any], key: ed25519.Ed25519PrivateKey = CODEX_KEY, keyid: str = "codex-test-key") -> dict[str, Any]:
    raw = key.sign(attestation_signing_payload(subject_digest, pred))
    return {"keyid": keyid, "algorithm": "ed25519", "sig": base64.b64encode(raw).decode("ascii")}


def append_attestation(writer: EventWriter, index: int) -> None:
    pred = predicate(index)
    subject = "sha256:" + canonical_hash({"run": index, "task_id": "TASK-0117", "agent": "Codex"})
    writer.append_agent_attestation(
        agent_id="Codex",
        subject_digest=subject,
        subject_reference=f"NEG-{index:02d}",
        predicate=pred,
        signature=signature(subject, pred),
        idempotency_key=f"attestation-negative:{index}",
        ts=f"2026-06-19T01:{index:02d}:01Z",
    )
    writer.periodic_anchor_if_due(now=f"2026-06-19T01:{index:02d}:02Z")


def valid_fixture(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    cfg = config(root)
    write_json(root / "protocol.config.json", cfg)
    writer = EventWriter(root)
    for index in range(1, 5):
        append_attestation(writer, index)
    events = writer.events()
    assert validate_chain(events, cfg, root=root)["valid"] is True
    assert validate_agent_signatures(events, cfg)["valid"] is True
    assert verify_anchor_monotonicity(events, cfg)["valid"] is True
    return cfg, events


def classify(events: list[dict[str, Any]], cfg: dict[str, Any], root: Path) -> tuple[str, str]:
    sigs = validate_agent_signatures(events, cfg)
    if sigs["valid"] is not True:
        return "A2", str(sigs["findings"][0]["error"])
    chain = validate_chain(events, cfg, root=root)
    if chain["valid"] is not True:
        return "A1", str(chain["reason"])
    anchors = verify_anchor_monotonicity(events, cfg)
    if anchors["valid"] is not True:
        return "A1", str(anchors["findings"][0]["error"])
    return "none", "accepted"


def attestations(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [event for event in events if event.get("type") == "agent.attestation"]


def mutate_payload(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated = deepcopy(events)
    attestations(mutated)[1]["payload"]["predicate"]["outputs_scope"] = ["tampered"]
    return mutated


def delete_event(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    victim_seq = attestations(events)[1]["seq"]
    return [event for event in deepcopy(events) if event.get("seq") != victim_seq]


def insert_event(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated = deepcopy(events)
    fake = deepcopy(attestations(mutated)[0])
    fake["idempotency_key"] = "forged:insert"
    fake["payload"]["subject_reference"] = "FORGED"
    mutated.insert(3, fake)
    return mutated


def reorder_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated = deepcopy(events)
    mutated[3], mutated[4] = mutated[4], mutated[3]
    return mutated


def unregistered_key(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated = deepcopy(events)
    attestations(mutated)[1]["payload"]["signature"]["keyid"] = "missing-key"
    return mutated


def cross_attribution(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    mutated = deepcopy(events)
    event = attestations(mutated)[1]
    event["actor"] = "Claude"
    event["payload"]["agent_id"] = "Claude"
    event["payload"]["predicate"]["agent_id"] = "Claude"
    event["payload"]["predicate"]["role"] = "reviewer"
    event["payload"]["signature"]["keyid"] = "claude-test-key"
    return mutated


Case = tuple[str, str, Callable[[list[dict[str, Any]]], list[dict[str, Any]]]]
CASES: list[Case] = [
    ("AC3-1-payload-alteration", "A2", mutate_payload),
    ("AC3-2-event-deletion", "A1", delete_event),
    ("AC3-3-event-insertion", "A1", insert_event),
    ("AC3-4-event-reordering", "A1", reorder_events),
    ("AC3-5-unregistered-key", "A2", unregistered_key),
    ("AC3-6-cross-attribution", "A2", cross_attribution),
]


def run_case(name: str, expected_class: str, mutator: Callable[[list[dict[str, Any]]], list[dict[str, Any]]]) -> dict[str, Any]:
    root = make_root_temp_dir(ROOT, f"attestation-negative-{name.lower()}-")
    try:
        cfg, events = valid_fixture(root)
        detected_class, reason = classify(mutator(events), cfg, root)
        passed = detected_class == expected_class
        return {"case": name, "status": "pass" if passed else "fail", "expected_class": expected_class, "detected_class": detected_class, "reason": reason}
    finally:
        remove_root_temp_dir(root, strict=True)


def main() -> int:
    results = [run_case(name, expected, mutator) for name, expected, mutator in CASES]
    print(json.dumps({"schema_version": "attestation_negative_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0 if all(result["status"] == "pass" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
