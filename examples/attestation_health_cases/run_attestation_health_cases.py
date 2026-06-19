#!/usr/bin/env python3
"""SPEC-0081 AC1/AC2/AC4/AC5 harness for #4 attestation activation."""

from __future__ import annotations

import base64
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives import serialization  # type: ignore
from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore

from runtime.eventlog import EventLogError, EventWriter, attestation_signing_payload, canonical_hash, verify_event_auth
from runtime.protocol_replay import validate_agent_signatures, validate_chain, verify_anchor_monotonicity
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


N_RUNS = 20
PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
PUBLIC_KEY_B64 = base64.b64encode(
    PRIVATE_KEY.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
).decode("ascii")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="ascii")


def config(root: Path, *, event_auth: bool = True, chain: bool = True, signatures: bool = True, anchor: bool = True) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {"implementer": "Codex"},
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True, "capabilities": ["implementer"]}]},
        "event_auth": {
            "enabled": event_auth,
            "method": "hmac-sha256",
            "issuer": "fixture-runtime",
            "audience": "fixture-event-log",
            "keys": {
                "runtime": {"key_id": "fixture-runtime", "secret": "runtime-test-secret"},
                "Codex": {"key_id": "fixture-codex", "secret": "codex-test-secret"},
            },
        },
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "chain_enabled": chain,
            "agent_signatures_enabled": signatures,
            "signature_config": {"backend": "local-ed25519", "public_keys": {"codex-test-key": PUBLIC_KEY_B64}},
            "anchor_enabled": anchor,
            "anchor_config": {
                "backend": "git-remote",
                "remote_url": str(root / "audit-remote"),
                "identity": "runtime-anchor-health",
                "interval_seconds": 0,
            },
        },
    }


def predicate(index: int) -> dict[str, Any]:
    return {
        "agent_id": "Codex",
        "agent_model": "golden-model",
        "task_id": "TASK-0117",
        "decision_id": "DECISION-0039",
        "role": "implementer",
        "inputs_trust_boundary": "internal",
        "outputs_scope": ["examples/attestation_health_cases"],
        "timestamp_claimed": f"2026-06-19T00:{index:02d}:00Z",
        "turn_index": index,
        "human_checkpoint": False,
    }


def signature(subject_digest: str, pred: dict[str, Any]) -> dict[str, Any]:
    raw = PRIVATE_KEY.sign(attestation_signing_payload(subject_digest, pred))
    return {"keyid": "codex-test-key", "algorithm": "ed25519", "sig": base64.b64encode(raw).decode("ascii")}


def append_attested_run(writer: EventWriter, index: int) -> dict[str, Any] | None:
    pred = predicate(index)
    subject = "sha256:" + canonical_hash({"run": index, "task_id": "TASK-0117", "agent": "Codex"})
    return writer.append_agent_attestation(
        agent_id="Codex",
        subject_digest=subject,
        subject_reference=f"RUN-{index:02d}",
        predicate=pred,
        signature=signature(subject, pred),
        idempotency_key=f"attestation-health:{index}",
        ts=f"2026-06-19T00:{index:02d}:01Z",
    )


def attestation_is_structured(event: dict[str, Any]) -> bool:
    payload = event.get("payload")
    if not isinstance(payload, dict):
        return False
    expected = {"agent_id", "subject_digest", "subject_reference", "predicate", "signature", "verification_backend"}
    if set(payload) != expected:
        return False
    return (
        str(payload.get("subject_digest") or "").startswith("sha256:")
        and isinstance(payload.get("predicate"), dict)
        and isinstance(payload.get("signature"), dict)
    )


def case_provisioning_smoke(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    write_json(tmp / "protocol.config.json", cfg)
    writer = EventWriter(tmp)
    event = writer.append_event(
        event_type="intent.applied",
        aggregate_id="TASK-0117",
        actor_id="Codex",
        payload={"transition": "provisioned"},
        idempotency_key="provisioning:ok",
        ts="2026-06-19T00:00:01Z",
    )
    anchor = writer.periodic_anchor_if_due(now="2026-06-19T00:00:02Z")
    assert verify_event_auth(event, cfg)["valid"] is True
    assert anchor is not None and verify_event_auth(anchor, cfg)["valid"] is True

    missing_key = config(tmp)
    missing_key["event_auth"]["keys"].pop("Codex")
    write_json(tmp / "protocol.config.json", missing_key)
    try:
        EventWriter(tmp).append_event(
            event_type="intent.applied",
            aggregate_id="TASK-0117",
            actor_id="Codex",
            payload={"transition": "missing-key"},
            idempotency_key="provisioning:missing-key",
            ts="2026-06-19T00:00:03Z",
        )
    except EventLogError as exc:
        assert "signing key missing" in str(exc)
    else:
        raise AssertionError("event_auth.enabled accepted missing Codex key")

    missing_remote = config(tmp)
    missing_remote["event_state"]["anchor_config"]["remote_url"] = ""
    write_json(tmp / "protocol.config.json", missing_remote)
    try:
        EventWriter(tmp).periodic_anchor_if_due(now="2026-06-19T00:00:04Z")
    except EventLogError as exc:
        assert "requires remote_url" in str(exc)
    else:
        raise AssertionError("anchor_enabled accepted missing remote_url")
    return {"case": "AC1-provisioning-smoke", "status": "pass"}


def case_health_report(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    write_json(tmp / "protocol.config.json", cfg)
    writer = EventWriter(tmp)
    for index in range(1, N_RUNS + 1):
        event = append_attested_run(writer, index)
        assert event is not None
        writer.periodic_anchor_if_due(now=f"2026-06-19T00:{index:02d}:02Z")
    events = writer.events()
    attestations = [event for event in events if event.get("type") == "agent.attestation"]
    chain = validate_chain(events, cfg, root=tmp)
    signatures = validate_agent_signatures(events, cfg)
    anchors = verify_anchor_monotonicity(events, cfg)
    auth_ok = all(verify_event_auth(event, cfg)["valid"] for event in events)
    anchored_head_seqs = {
        int((event.get("payload") or {}).get("head_seq") or 0)
        for event in events
        if event.get("type") == "chain.anchor" and isinstance(event.get("payload"), dict)
    }
    bad_signature_seqs = {int(item.get("seq") or 0) for item in signatures.get("findings") or []}
    numerator = sum(
        1
        for event in attestations
        if int(event.get("seq") or 0) not in bad_signature_seqs
        and int(event.get("seq") or 0) in anchored_head_seqs
        and attestation_is_structured(event)
    )
    denominator = len(attestations)
    report = {
        "schema_version": "attestation_health.v1",
        "n_runs": N_RUNS,
        "denominator_source": "event_log.agent.attestation",
        "denominator": denominator,
        "numerator": numerator,
        "health_rate": numerator / denominator if denominator else 0.0,
        "threshold": 0.99,
        "health_not_security": True,
        "statement": "This metric is health, not security; adversarial security is covered by AC3 negative cases.",
        "checks": {
            "chain_valid": chain["valid"],
            "signatures_valid": signatures["valid"],
            "anchors_valid": anchors["valid"],
            "event_auth_valid": auth_ok,
            "attestation_schema_structured": all(attestation_is_structured(event) for event in attestations),
        },
    }
    assert denominator == N_RUNS, report
    assert report["health_rate"] >= 0.99, report
    assert all(report["checks"].values()), report
    return {"case": "AC2-health-report", "status": "pass", "report": report}


def case_rollback_dormant(tmp: Path) -> dict[str, Any]:
    dormant = config(tmp, event_auth=False, chain=False, signatures=False, anchor=False)
    enabled = config(tmp, event_auth=True, chain=True, signatures=True, anchor=True)
    rolled_back = deepcopy(enabled)
    rolled_back["event_auth"]["enabled"] = False
    rolled_back["event_state"]["chain_enabled"] = False
    rolled_back["event_state"]["agent_signatures_enabled"] = False
    rolled_back["event_state"]["anchor_enabled"] = False
    assert canonical_hash(dormant["event_auth"]) == canonical_hash(rolled_back["event_auth"])
    for key in ("chain_enabled", "agent_signatures_enabled", "anchor_enabled"):
        assert dormant["event_state"][key] == rolled_back["event_state"][key]
    write_json(tmp / "protocol.config.json", rolled_back)
    writer = EventWriter(tmp)
    event = writer.append_event(
        event_type="intent.applied",
        aggregate_id="TASK-0117",
        actor_id="Codex",
        payload={"transition": "rollback-dormant"},
        idempotency_key="rollback:dormant",
        ts="2026-06-19T00:30:00Z",
    )
    assert "prev_hash" not in event and "event_auth" not in event
    assert append_attested_run(writer, 1) is None
    assert writer.periodic_anchor_if_due(now="2026-06-19T00:30:01Z") is None
    assert validate_chain(writer.events(), rolled_back, root=tmp)["reason"] == "chain_disabled"
    assert validate_agent_signatures(writer.events(), rolled_back)["checked"] == 0
    assert verify_anchor_monotonicity(writer.events(), rolled_back)["checked"] == 0
    return {"case": "AC5-rollback-dormant", "status": "pass"}


def main() -> int:
    tmp = make_root_temp_dir(ROOT, "attestation-health-")
    try:
        results = [case_provisioning_smoke(tmp / "provisioning"), case_health_report(tmp / "health"), case_rollback_dormant(tmp / "rollback")]
    finally:
        remove_root_temp_dir(tmp, strict=True)
    print(json.dumps({"schema_version": "attestation_health_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
