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
    event_signature,
    event_auth_verification_boundaries,
    replay_events,
    sign_event,
)
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir  # noqa: E402

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
    assert EVENT_AUTH_UNVERIFIABLE_REASONS == {"unresolved_key", "missing_key", "key_unavailable"}
    assert EVENT_AUTH_TAMPER_REASONS == {"invalid_signature", "missing_signature"}
    assert not (EVENT_AUTH_UNVERIFIABLE_REASONS & EVENT_AUTH_TAMPER_REASONS)
    return {"case": "AC-constants-partition", "status": "pass"}


def rotated_cfg(root: Path) -> dict[str, Any]:
    config = cfg()
    config["event_auth"]["keys"] = {
        "Codex": {"key_id": "codex:v2", "secret_file": "secrets/eventauth-codex-v2.key"}
    }
    path = root / "secrets/eventauth-codex-v2.key"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("b" * 64 + "\n", encoding="ascii")
    registry = root / "Area_comun" / "protocol" / "EVENT_AUTH_KEY_REGISTRY.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "keys": {
                    "codex:v1": {"actor": "Codex", "status": "retired", "valid_through_seq": 1009},
                    "codex:v2": {"actor": "Codex", "status": "active", "valid_through_seq": None},
                },
            }
        ),
        encoding="ascii",
    )
    return config


def sign_with(event: dict[str, Any], key_id: str, secret: str) -> dict[str, Any]:
    signed = deepcopy(event)
    signed["event_auth"] = {
        "method": "hmac-sha256",
        "key_id": key_id,
        "signature": event_signature(signed, secret),
    }
    return signed


def replay_exit(state: dict[str, Any]) -> int:
    return 1 if state.get("rejections") else 0


def case_attested_rotation_population() -> dict[str, Any]:
    root = make_root_temp_dir(ROOT, "replay-rotation-")
    try:
        config = rotated_cfg(root)
        population = [sign_with(mkevent(seq, f"v1-{seq}"), "codex:v1", "a" * 64) for seq in range(1, 1010)]
        declaration = mkevent(
            1010,
            "rotation-v2",
            {"unavailable_key_ids": ["codex:v1"], "replacement_key_id": "codex:v2"},
        )
        declaration["type"] = "event_auth.key_rotation_declared"
        declaration = sign_event(declaration, config, root=root)
        valid_v2 = [sign_event(mkevent(seq, f"v2-{seq}"), config, root=root) for seq in (1011, 1019)]
        state = replay_events(population + [declaration] + valid_v2, None, config, root)
        boundaries = event_auth_verification_boundaries(population + [declaration] + valid_v2, config, root=root)
        assert replay_exit(state) == 0, state.get("rejections")
        assert len(boundaries) == 1009
        assert {item.get("key_id") for item in boundaries} == {"codex:v1"}

        forged = mkevent(1, "forged", {"unavailable_key_ids": ["attacker:v9"]})
        forged["type"] = "event_auth.key_rotation_declared"
        forged = sign_with(forged, "attacker:v9", "not-a-real-key")
        forged_state = replay_events([forged], None, config, root)
        assert replay_exit(forged_state) == 1
        assert forged_state["rejections"][0]["reason"] == "unknown_key_id"

        bad_present = sign_event(mkevent(1, "bad-present"), config, root=root)
        bad_present["payload"] = {"tampered": True}
        bad_state = replay_events([bad_present], None, config, root)
        assert replay_exit(bad_state) == 1
        assert bad_state["rejections"][0]["reason"] == "invalid_signature"

        other_actor = sign_with(mkevent(1, "other-actor"), "codex:v2", "b" * 64)
        other_actor["actor"] = "Arquitecto"
        other_actor["event_auth"]["signature"] = event_signature(other_actor, "b" * 64)
        other_actor_state = replay_events([other_actor], None, config, root)
        assert replay_exit(other_actor_state) == 1
        assert other_actor_state["rejections"][0]["reason"] == "key_actor_mismatch"

        late_v1 = sign_with(mkevent(1010, "late-v1"), "codex:v1", "a" * 64)
        late_v1_state = replay_events([late_v1], None, config, root)
        assert replay_exit(late_v1_state) == 1
        assert late_v1_state["rejections"][0]["reason"] == "key_outside_validity"
        return {
            "case": "attested-rotation-population",
            "status": "pass",
            "population": 1009,
            "key_unavailable": len(boundaries),
            "invalid_signature": 0,
            "exit_codes": {
                "registered_v1": 0,
                "undeclared_unknown": 1,
                "bad_present": 1,
                "own_key_as_other_actor": 1,
                "retired_key_after_boundary": 1,
            },
        }
    finally:
        remove_root_temp_dir(root, strict=True)


def main() -> int:
    cases = [
        case_ac_constants(),
        case_ac1_secret_independent(),
        case_ac2_tamper_still_rejected(),
        case_attested_rotation_population(),
    ]
    report = {"schema_version": "replay_secret_independent_cases.v1", "cases": cases}
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if all(c["status"] == "pass" for c in cases) else 1


if __name__ == "__main__":
    raise SystemExit(main())
