#!/usr/bin/env python3
"""Golden cases for external chain anchoring."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cryptography.hazmat.primitives import serialization  # type: ignore
from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore

from runtime.eventlog import EventLogError, EventWriter, attestation_signing_payload, canonical_hash
from runtime.protocol_replay import validate_agent_signatures, validate_chain, verify_anchor_monotonicity
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


PRIVATE_KEY = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
PUBLIC_KEY_B64 = base64.b64encode(
    PRIVATE_KEY.public_key().public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
).decode("ascii")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="ascii")


def config(root: Path, *, enabled: bool = True, chain: bool = False, signatures: bool = False, interval: int = 0) -> dict[str, Any]:
    cfg = {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {"implementer": "Codex"},
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True, "capabilities": ["implementer"]}]},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": True,
            "authoritative": True,
            "chain_enabled": chain,
            "agent_signatures_enabled": signatures,
            "signature_config": {"backend": "local-ed25519", "public_keys": {"codex-test-key": PUBLIC_KEY_B64}},
            "anchor_enabled": enabled,
            "anchor_config": {
                "backend": "git-remote",
                "remote_url": str(root / "audit-remote"),
                "branch": "audits/default",
                "identity": "runtime-anchor-test",
                "interval_seconds": interval,
            },
        },
    }
    write_json(root / "protocol.config.json", cfg)
    return cfg


def seed_event(writer: EventWriter, seq_label: str = "seed") -> dict[str, Any]:
    return writer.append_event(
        event_type="intent.applied",
        aggregate_id="TASK-ANCHOR",
        actor_id="Codex",
        payload={"value": seq_label},
        idempotency_key=f"seed:{seq_label}",
        ts=f"2026-06-13T00:00:0{len(writer.events())}Z",
    )


def run_case(name: str, fn) -> dict[str, Any]:
    tmp = make_root_temp_dir(ROOT, f"anchor-{name.lower()}-")
    try:
        outcome = fn(tmp)
        passed = bool(outcome.pop("passed"))
        return {"case": name, "status": "pass" if passed else "fail", **outcome}
    finally:
        remove_root_temp_dir(tmp, strict=True)


def case_off_by_default(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp, enabled=False)
    writer = EventWriter(tmp)
    seed_event(writer)
    anchor = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    result = verify_anchor_monotonicity(writer.events(), cfg)
    return {"passed": anchor is None and result["valid"] is True and result["checked"] == 0, "message": result["reason"]}


def case_git_remote_ok(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    writer = EventWriter(tmp)
    seed_event(writer)
    anchor = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    remote = tmp / "audit-remote"
    result = verify_anchor_monotonicity(writer.events(), cfg)
    return {
        "passed": anchor is not None and (remote / "HEAD").exists() and (remote / "anchors.log").exists() and result["valid"],
        "message": result["reason"],
    }


def case_remote_down(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    cfg["event_state"]["anchor_config"]["remote_url"] = "https://example.invalid/audit.git"
    write_json(tmp / "protocol.config.json", cfg)
    writer = EventWriter(tmp)
    seed_event(writer)
    try:
        writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    except EventLogError:
        pass
    anchors = [event for event in writer.events() if event.get("type") == "chain.anchor"]
    return {"passed": anchors == [], "message": "remote failure left local log intact"}


def case_interval_skip(tmp: Path) -> dict[str, Any]:
    config(tmp, interval=3600)
    writer = EventWriter(tmp)
    seed_event(writer)
    first = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    seed_event(writer, "second")
    second = writer.periodic_anchor_if_due(now="2026-06-13T00:02:00Z")
    anchors = [event for event in writer.events() if event.get("type") == "chain.anchor"]
    return {"passed": first is not None and second is None and len(anchors) == 1, "message": "interval respected"}


def case_reorder_detected(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    writer = EventWriter(tmp)
    seed_event(writer)
    first = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    seed_event(writer, "second")
    second = writer.periodic_anchor_if_due(now="2026-06-13T00:02:00Z")
    assert first and second
    events = writer.events()
    anchors = [event for event in events if event.get("type") == "chain.anchor"]
    anchors[1]["payload"]["head_seq"] = anchors[0]["payload"]["head_seq"]
    result = verify_anchor_monotonicity(events, cfg)
    return {"passed": result["valid"] is False and result["findings"][0]["error"] == "anchor_reordered", "message": result["reason"]}


def signed_attestation() -> dict[str, Any]:
    predicate = {
        "agent_id": "Codex",
        "role": "implementer",
        "task_id": "TASK-ANCHOR",
        "timestamp_claimed": "2026-06-13T00:00:00Z",
        "inputs_trust_boundary": "internal",
    }
    subject = "sha256:" + canonical_hash({"task_id": "TASK-ANCHOR"})
    sig = PRIVATE_KEY.sign(attestation_signing_payload(subject, predicate))
    return {
        "agent_id": "Codex",
        "subject_digest": subject,
        "subject_reference": "TASK-ANCHOR",
        "predicate": predicate,
        "signature": {"keyid": "codex-test-key", "algorithm": "ed25519", "sig": base64.b64encode(sig).decode("ascii")},
        "verification_backend": "local-ed25519",
    }


def case_chain_sig_anchor(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp, chain=True, signatures=True)
    writer = EventWriter(tmp)
    seed_event(writer)
    writer.append_event(
        event_type="agent.attestation",
        aggregate_id="TASK-ANCHOR",
        actor_id="Codex",
        payload=signed_attestation(),
        applied=False,
        ts="2026-06-13T00:00:30Z",
    )
    writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    events = writer.events()
    chain = validate_chain(events, cfg, root=tmp)
    sigs = validate_agent_signatures(events, cfg)
    anchors = verify_anchor_monotonicity(events, cfg)
    return {"passed": chain["valid"] and sigs["valid"] and anchors["valid"], "message": "chain+sig+anchor valid"}


def case_git_log_append(tmp: Path) -> dict[str, Any]:
    config(tmp)
    writer = EventWriter(tmp)
    for index in range(5):
        seed_event(writer, f"event-{index}")
        writer.periodic_anchor_if_due(now=f"2026-06-13T00:0{index}:00Z")
    lines = (tmp / "audit-remote" / "anchors.log").read_text(encoding="ascii").splitlines()
    return {"passed": len(lines) == 5 and all("runtime-anchor-test" in line for line in lines), "message": "append-only log"}


def case_determinism(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    writer = EventWriter(tmp)
    seed_event(writer)
    anchor = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    evidence = anchor["payload"]["anchor_evidence"] if anchor else {}
    expected = canonical_hash(
        {
            "head": anchor["payload"]["head_digest"],
            "identity": "runtime-anchor-test",
            "line": f"2026-06-13T00:01:00Z {anchor['payload']['head_digest']} runtime-anchor-test\n",
            "backend": "git-remote",
        }
    )
    return {"passed": cfg["event_state"]["anchor_enabled"] and evidence.get("proof") == expected, "message": "deterministic proof"}


def case_legacy_no_anchors(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp)
    result = verify_anchor_monotonicity([{"seq": 1, "type": "intent.applied"}], cfg)
    return {"passed": result["valid"] is True and result["checked"] == 0, "message": result["reason"]}


def case_enable_post_hoc(tmp: Path) -> dict[str, Any]:
    cfg = config(tmp, enabled=False)
    writer = EventWriter(tmp)
    seed_event(writer)
    cfg["event_state"]["anchor_enabled"] = True
    write_json(tmp / "protocol.config.json", cfg)
    seed_event(writer, "after-enable")
    anchor = writer.periodic_anchor_if_due(now="2026-06-13T00:01:00Z")
    result = verify_anchor_monotonicity(writer.events(), cfg)
    return {"passed": anchor is not None and result["valid"], "message": result["reason"]}


CASES = [
    ("GC-1-off-by-default", case_off_by_default),
    ("GC-2-git-remote-ok", case_git_remote_ok),
    ("GC-3-remote-down", case_remote_down),
    ("GC-4-interval-skip", case_interval_skip),
    ("GC-5-reorder-detected", case_reorder_detected),
    ("GC-6-chain-sig-anchor", case_chain_sig_anchor),
    ("GC-7-git-log-append", case_git_log_append),
    ("GC-8-determinism", case_determinism),
    ("GC-9-legacy-no-anchors", case_legacy_no_anchors),
    ("GC-10-enable-post-hoc", case_enable_post_hoc),
]


def main() -> int:
    results = [run_case(name, fn) for name, fn in CASES]
    print(json.dumps({"schema_version": "anchor_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0 if all(item["status"] == "pass" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
