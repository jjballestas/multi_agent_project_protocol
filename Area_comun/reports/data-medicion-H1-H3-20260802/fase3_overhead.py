#!/usr/bin/env python3
"""FASE 3 -- H2 sobrecoste acotado de #4 vs baseline sin #4 (misma carga).

Mide el COSTE MARGINAL por evento del aparato #4 (firma actor_auth Ed25519 + encadenado prev_hash +
event_auth HMAC) contra un baseline identico SIN #4, sobre la MISMA carga submit_intent en instancias
FRESCAS (log pequeno, para aislar el coste marginal de #4 y no la verificacion O(n) del log ya sellado).

Umbrales s.5: latencia mediana <= 50 ms/ev AND p95 <= 200 ms/ev ; almacenamiento <= 4 KB/ev.
Tokens: #4 firma HASHES (campos de tamano fijo anadidos por el runtime al events.jsonl, fuera del
contexto que el agente lee/escribe) -> Delta tokens = 0% por construccion (DECISION-0033/0040); umbral <= 5%.
"""
from __future__ import annotations
import base64, json, statistics, sys, time, tempfile, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cryptography.hazmat.primitives import serialization  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ed25519  # noqa: E402
from runtime.submit_intent import submit_intent  # noqa: E402

PRIV = ed25519.Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))


def pub_b64(k):
    return base64.b64encode(k.public_key().public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)).decode("ascii")


def priv_pem(k):
    return k.private_bytes(encoding=serialization.Encoding.PEM,
                           format=serialization.PrivateFormat.PKCS8,
                           encryption_algorithm=serialization.NoEncryption()).decode("ascii")


def wj(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="ascii", newline="\n")


def config(*, four: bool):
    return {
        "schema_version": "1.0", "protocol_version": "1.14.0", "adoption_tier": "runtime",
        "event_auth": ({"enabled": True, "method": "hmac-sha256", "issuer": "bench", "audience": "bench",
                        "keys": {"Codex": {"key_id": "bench-codex", "secret": "codex-secret"}}}
                       if four else {"enabled": False}),
        "event_state": {
            "enabled": True, "materialize": True, "enforce": True, "authoritative": True,
            "slim_views_enabled": False,
            "chain_enabled": four, "agent_signatures_enabled": False,
            "signature_config": {"backend": "local-ed25519", "public_keys": {"codex:v1": pub_b64(PRIV)}},
            "anchor_enabled": False,
        },
        "agent_registry": {"enabled": True, "agents": [{"id": "Codex", "enabled": True, "capabilities": ["implementer"]}]},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def override_on(root: Path):
    wj(root / "event-state.runtime.json", {"event_state": {
        "actor_auth_enforce": True,
        "actor_auth_config": {"private_key_files": {"Codex": "secrets/codex.pem"}, "keyids": {"Codex": "codex:v1"}},
    }})


def seed(root: Path, *, four: bool):
    wj(root / "protocol.config.json", config(four=four))
    if four:
        override_on(root)
        (root / "secrets").mkdir(parents=True, exist_ok=True)
        (root / "secrets/codex.pem").write_text(priv_pem(PRIV), encoding="ascii")
    wj(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    wj(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active", "decisions": [], "active_tasks": []})
    wj(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": []})


def intent(i: int):
    return {"type": "claim", "op": "acquire", "claim": {
        "claim_id": f"CLAIM-BENCH-{i:04d}", "task_id": f"TASK-{i:04d}", "owner": "Codex", "status": "active",
        "started_at": "2026-06-27T00:00:00Z", "updated_at": "2026-06-27T00:00:00Z",
        "expires_at": "2026-06-28T00:00:00Z", "scope": ["runtime/"], "notes": "bench"}}


def run_arm(*, four: bool, K: int):
    root = Path(tempfile.mkdtemp(prefix="bench4_" if four else "benchbase_", dir=str(ROOT / "_measure")))
    try:
        seed(root, four=four)
        lat = []
        for i in range(K):
            t0 = time.perf_counter()
            submit_intent(root, "Codex", intent(i), timestamp=f"2026-06-27T00:00:{i % 60:02d}Z")
            lat.append((time.perf_counter() - t0) * 1000.0)
        log = root / "runtime/state/events.jsonl"
        lines = [l for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
        applied = [l for l in lines if '"intent.applied"' in l]
        avg_bytes = statistics.mean(len(l.encode("utf-8")) for l in applied) if applied else 0
        # drop first op (warm-up: imports/materialize init) from latency stats
        warm = lat[1:] if len(lat) > 1 else lat
        return {"lat_ms": warm, "avg_event_bytes": avg_bytes, "n_events": len(applied)}
    finally:
        shutil.rmtree(root, ignore_errors=True)


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return 0.0
    k = (len(xs) - 1) * p / 100.0
    lo = int(k)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


K = 120
on = run_arm(four=True, K=K)
base = run_arm(four=False, K=K)
d_med = statistics.median(on["lat_ms"]) - statistics.median(base["lat_ms"])
d_p95 = pct(on["lat_ms"], 95) - pct(base["lat_ms"], 95)
d_bytes = on["avg_event_bytes"] - base["avg_event_bytes"]
out = {
    "schema": "fase3_overhead.v1", "K_ops_per_arm": K,
    "latency_ms_per_event": {
        "four_median": round(statistics.median(on["lat_ms"]), 3), "base_median": round(statistics.median(base["lat_ms"]), 3),
        "four_p95": round(pct(on["lat_ms"], 95), 3), "base_p95": round(pct(base["lat_ms"], 95), 3),
        "delta_median": round(d_med, 3), "delta_p95": round(d_p95, 3),
        "threshold_median_ms": 50, "threshold_p95_ms": 200,
        "pass_median": d_med <= 50, "pass_p95": d_p95 <= 200,
    },
    "storage_bytes_per_event": {
        "four_avg": round(on["avg_event_bytes"], 1), "base_avg": round(base["avg_event_bytes"], 1),
        "delta_bytes": round(d_bytes, 1), "threshold_bytes": 4096, "pass": d_bytes <= 4096,
    },
    "tokens": {
        "delta_pct": 0.0, "threshold_pct": 5,
        "justification": "#4 adds fixed-size cryptographic fields (actor_auth sig ~88B b64, keyid, prev_hash "
                         "64 hex, event_auth HMAC) to runtime/state/events.jsonl, which is NOT loaded into agent "
                         "context (agents read materialized state + mailbox, not the raw event log). Runtime signs "
                         "HASHES, not text (DECISION-0033/0040) -> 0% token overhead on the agent coordination path.",
        "pass": True,
    },
}
(ROOT / "_measure" / "fase3_overhead_result.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="ascii")
print(json.dumps(out, indent=2, sort_keys=True))
