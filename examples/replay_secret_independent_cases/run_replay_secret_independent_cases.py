#!/usr/bin/env python3
"""Golden cases for SPEC-0084 / DECISION-0046: replay secret-independence.

AC1: replaying event_auth-signed events yields the SAME canonical_hash(state) whether the
     secret_file is resolvable (live, with secrets) or not (clean clone / CI, no secrets).
     unresolved_key / missing_key are environment conditions, NOT state-mutating rejections.
AC2: real tamper (invalid_signature) and missing_signature are STILL rejected
     (security.unauthenticated_event, event not applied) when the secret is resolvable.

Deterministic: fixed seqs / timestamps / idempotency keys. Exit 0 = all pass.
"""

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

from runtime.eventlog import (  # noqa: E402
    EVENT_AUTH_TAMPER_REASONS,
    EVENT_AUTH_UNVERIFIABLE_REASONS,
    UNAUTHENTICATED_EVENT,
    canonical_hash,
    replay_events,
    sign_event,
    attestation_signing_payload,
)
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir  # noqa: E402
from runtime.protocol_replay import validate_agent_signatures  # noqa: E402

KEY_REL = "secrets/eventauth-codex.key"
SECRET = "a" * 64  # deterministic fixture secret


def cfg() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {"implementer": "Codex"},
        "event_auth": {
            "enabled": True,
            "method": "hmac-sha256",
            "issuer": "fixture",
            "audience": "fixture",
            "keys": {"Codex": {"key_id": "codex:v1", "secret_file": KEY_REL}},
        },
        "event_state": {"enabled": True, "materialize": True, "enforce": True, "authoritative": True},
    }


def mkevent(seq: int, idk: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "seq": seq,
        "event_schema_version": "1.0",
        "type": "intent.applied",
        "aggregate_id": f"AGG-{seq}",
        "aggregate_version": 1,
        "actor": "Codex",
        "actor_auth": {"method": "not_enforced_phase2"},
        "idempotency_key": idk,
        "fencing_token": None,
        "applied": True,
        "ts": "2026-01-01T00:00:00Z",
        "payload": payload or {"n": seq},
    }


def write_key(root: Path) -> None:
    p = root / KEY_REL
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(SECRET + "\n", encoding="utf-8")


def case_ac1_secret_independent() -> dict[str, Any]:
    root_with = make_root_temp_dir(ROOT, "replay-si-with-")
    root_without = make_root_temp_dir(ROOT, "replay-si-without-")
    try:
        write_key(root_with)  # root_without deliberately has NO keyfile
        config = cfg()
        signed = [
            sign_event(mkevent(1, "k1"), config, root=root_with),
            sign_event(mkevent(2, "k2"), config, root=root_with),
        ]
        st_with = replay_events(deepcopy(signed), None, config, root_with)
        st_without = replay_events(deepcopy(signed), None, config, root_without)
        h_with = canonical_hash(st_with)
        h_without = canonical_hash(st_without)
        assert h_with == h_without, ("AC1 state hash differs with vs without secret", h_with, h_without)
        assert st_without.get("rejections") == [], ("AC1 unverifiable must NOT reject", st_without.get("rejections"))
        assert st_with.get("rejections") == [], ("AC1 valid must not reject", st_with.get("rejections"))
        assert st_with.get("events_applied") == 2 and st_without.get("events_applied") == 2
        assert st_with.get("aggregate_versions") == st_without.get("aggregate_versions")
        assert st_with.get("idempotency_keys") == st_without.get("idempotency_keys")
        return {"case": "AC1-secret-independent", "status": "pass", "state_hash": h_with}
    finally:
        remove_root_temp_dir(root_with, strict=True)
        remove_root_temp_dir(root_without, strict=True)


def case_ac2_tamper_still_rejected() -> dict[str, Any]:
    root = make_root_temp_dir(ROOT, "replay-si-tamper-")
    try:
        write_key(root)
        config = cfg()
        good = sign_event(mkevent(1, "k1"), config, root=root)
        tampered = deepcopy(good)
        tampered["payload"] = {"n": 999}  # alter signed content -> invalid_signature
        nosig = mkevent(2, "k2")  # event_auth enabled, no signature -> missing_signature
        valid = sign_event(mkevent(3, "k3"), config, root=root)
        st = replay_events([tampered, nosig, valid], None, config, root)
        rejections = st.get("rejections", [])
        reasons = {r.get("reason") for r in rejections}
        assert all(r.get("event") == UNAUTHENTICATED_EVENT for r in rejections), rejections
        assert "invalid_signature" in reasons, ("AC2 tamper not rejected", rejections)
        assert "missing_signature" in reasons, ("AC2 missing-signature not rejected", rejections)
        # the valid event applied; tampered/nosig NOT applied as aggregates
        assert "AGG-3" in (st.get("aggregate_versions") or {})
        assert "AGG-1" not in (st.get("aggregate_versions") or {})
        assert "AGG-2" not in (st.get("aggregate_versions") or {})
        # NOTE: invalid_signature is only distinguishable as tamper WITH the secret resolvable;
        # without the secret it is correctly classified unresolved_key (verification unavailable here).
        return {"case": "AC2-tamper-still-rejected", "status": "pass", "rejections": len(rejections)}
    finally:
        remove_root_temp_dir(root, strict=True)


def case_ac_constants() -> dict[str, Any]:
    assert EVENT_AUTH_UNVERIFIABLE_REASONS == {"unresolved_key", "missing_key"}
    assert EVENT_AUTH_TAMPER_REASONS == {"invalid_signature", "missing_signature"}
    assert not (EVENT_AUTH_UNVERIFIABLE_REASONS & EVENT_AUTH_TAMPER_REASONS)
    return {"case": "AC-constants-partition", "status": "pass"}


def agent_signature_cfg(public_keys: dict[str, str]) -> dict[str, Any]:
    return {
        "event_state": {
            "enabled": True,
            "agent_signatures_enabled": True,
            "signature_config": {"backend": "local-ed25519", "public_keys": public_keys},
        },
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True}]},
    }


def attestation_event(seq: int, keyid: str, sig: str) -> dict[str, Any]:
    predicate = {
        "agent_id": "Codex",
        "role": "implementer",
        "timestamp_claimed": "2026-01-01T00:00:00Z",
        "task_id": "TASK-FIXTURE",
    }
    return {
        "seq": seq,
        "type": "agent.attestation",
        "payload": {
            "agent_id": "Codex",
            "subject_digest": "sha256:" + "a" * 64,
            "predicate": predicate,
            "verification_backend": "local-ed25519",
            "signature": {"algorithm": "ed25519", "keyid": keyid, "sig": sig},
        },
    }


def case_agent_key_boundary_and_tamper() -> dict[str, Any]:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519

    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = base64.b64encode(
        private_key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    ).decode("ascii")
    event = attestation_event(1, "codex:v1", "")
    event["payload"]["signature"]["sig"] = base64.b64encode(
        private_key.sign(
            attestation_signing_payload(event["payload"]["subject_digest"], event["payload"]["predicate"])
        )
    ).decode("ascii")

    population = [deepcopy(event) for _ in range(1009)]
    for seq, item in enumerate(population, start=1):
        item["seq"] = seq
    unavailable_a = validate_agent_signatures(population, agent_signature_cfg({}))
    unavailable_b = validate_agent_signatures(deepcopy(population), agent_signature_cfg({}))
    assert unavailable_a["findings"] == unavailable_b["findings"] == [], "AC3 blind comparison precondition"
    assert unavailable_a["valid"] is True and unavailable_a["key_unavailable"] == 1009
    assert unavailable_a["invalid_signature"] == 0
    assert unavailable_a["boundaries"] == unavailable_b["boundaries"], "AC3 boundary must survive equal-artifact comparison"

    tampered = deepcopy(event)
    tampered["payload"]["signature"]["sig"] = base64.b64encode(b"0" * 64).decode("ascii")
    rejected = validate_agent_signatures([tampered], agent_signature_cfg({"codex:v1": public_key}))
    assert rejected["valid"] is False, "AC4 altered signature with available key must fail closed"
    assert rejected["invalid_signature"] == 1 and rejected["key_unavailable"] == 0
    assert rejected["findings"][0]["error"] == "invalid_signature"
    return {
        "case": "AC3-AC5-agent-key-boundary-and-tamper",
        "status": "pass",
        "population": 1009,
        "key_unavailable": unavailable_a["key_unavailable"],
        "invalid_signature": unavailable_a["invalid_signature"],
    }


def main() -> int:
    cases = [
        case_ac_constants(),
        case_ac1_secret_independent(),
        case_ac2_tamper_still_rejected(),
        case_agent_key_boundary_and_tamper(),
    ]
    report = {"schema_version": "replay_secret_independent_cases.v1", "cases": cases}
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if all(c["status"] == "pass" for c in cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
