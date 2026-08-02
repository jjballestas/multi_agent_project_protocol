#!/usr/bin/env python3
"""FASE 1 -- H1 deteccion: inyeccion PROGRAMATICA de ataques sobre copias del corpus sellado N=500.

Reglas de integridad (PLAN-EJECUCION-MEDICION-H1-H3):
- Inyeccion programatica y reproducible: harness con conteos, JAMAS juicio de un agente.
- Detector = pipeline de verificacion (#4): validate_chain (A1) + verify_actor_auth por evento (A2)
  + verify_anchor_monotonicity (A3). Un ataque esta DETECTADO iff el pipeline RECHAZA el corpus mutado.
- K ataques por vector, en posiciones ESPARCIDAS de la ventana elegible (seq>=2221), deterministas.
- Metrica: TPR_vector = detectados / inyectados.  Umbral s.5: = 100% en TODOS los vectores.

Corre en el clon limpio del tag TFM-dataset-N500 (config pineado 2e35f26e), SIN secretos (camino publico).
"""
from __future__ import annotations
import base64, json, sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from runtime.eventlog import verify_actor_auth  # noqa: E402
from runtime.protocol_replay import validate_chain, verify_anchor_monotonicity  # noqa: E402

CFG = json.loads((ROOT / "protocol.config.json").read_text(encoding="utf-8-sig"))
START = 2221
LOG = ROOT / "runtime/state/events.jsonl"
ALL = [json.loads(l) for l in LOG.read_text(encoding="utf-8").splitlines() if l.strip()]
# indices (positions in ALL) of eligible events
ELIG = [i for i, e in enumerate(ALL) if e.get("seq", 0) >= START
        and (e.get("actor_auth") or {}).get("method") == "ed25519"]
assert len(ELIG) == 500, f"expected 500 eligible, got {len(ELIG)}"


def pipeline_rejects(events: list[dict]) -> tuple[bool, str]:
    """True iff the #4 verification pipeline REJECTS this (possibly mutated) corpus."""
    ch = validate_chain(events, CFG, root=ROOT)
    if ch.get("valid") is not True:
        return True, f"A1_chain:{ch.get('reason')}"
    for e in events:
        if (e.get("actor_auth") or {}).get("method") == "ed25519":
            r = verify_actor_auth(e, CFG, ROOT)
            if r.get("valid") is not True:
                return True, f"A2_actor_auth:seq{e.get('seq')}:{r.get('reason')}"
    an = verify_anchor_monotonicity(events, CFG)
    if an.get("valid") is not True:
        return True, f"A3_anchor:{(an.get('findings') or [{}])[0]}"
    return False, "accepted"


# sanity: unmutated corpus must be ACCEPTED (no false rejection)
_rej, _why = pipeline_rejects(ALL)
assert _rej is False, f"baseline corpus rejected: {_why}"


def targets(k: int) -> list[int]:
    """k evenly-spread positions within the eligible window (deterministic)."""
    if k >= len(ELIG):
        return list(ELIG)
    step = len(ELIG) / k
    return [ELIG[int(i * step)] for i in range(k)]


# ---- A1 vectors (chain integrity) ----
def a1_payload_alteration(pos: int):
    ev = deepcopy(ALL)
    p = ev[pos].get("payload")
    if isinstance(p, dict):
        p["__tamper__"] = "x"
    else:
        ev[pos]["payload"] = {"__tamper__": "x"}
    return ev

def a1_event_deletion(pos: int):
    ev = deepcopy(ALL)
    del ev[pos]
    return ev

def a1_event_insertion(pos: int):
    ev = deepcopy(ALL)
    forged = deepcopy(ev[pos])
    forged["idempotency_key"] = f"forged-insert:{pos}"
    ev.insert(pos + 1, forged)
    return ev

def a1_event_reordering(pos: int):
    ev = deepcopy(ALL)
    q = pos + 1 if pos + 1 < len(ev) else pos - 1
    ev[pos], ev[q] = ev[q], ev[pos]
    return ev


# ---- A2 vectors (actor_auth Ed25519) ----
_OTHER = {"Arquitecto": "Codex", "Codex": "Analista", "Analista": "Arquitecto"}

def a2_cross_attribution(pos: int):
    ev = deepcopy(ALL)
    e = ev[pos]
    e["actor"] = _OTHER.get(e.get("actor"), "Codex")  # claim a different author, keep original sig/keyid
    return ev

def a2_unregistered_keyid(pos: int):
    ev = deepcopy(ALL)
    ev[pos]["actor_auth"]["keyid"] = "ghost:v9"
    return ev

def a2_invalid_signature(pos: int):
    ev = deepcopy(ALL)
    sig = ev[pos]["actor_auth"]["sig"]
    raw = bytearray(base64.b64decode(sig))
    raw[0] ^= 0xFF  # flip a byte -> signature no longer verifies
    ev[pos]["actor_auth"]["sig"] = base64.b64encode(bytes(raw)).decode("ascii")
    return ev


VECTORS = {
    "A1-payload-alteration": a1_payload_alteration,
    "A1-event-deletion": a1_event_deletion,
    "A1-event-insertion": a1_event_insertion,
    "A1-event-reordering": a1_event_reordering,
    "A2-cross-attribution": a2_cross_attribution,
    "A2-unregistered-keyid": a2_unregistered_keyid,
    "A2-invalid-signature": a2_invalid_signature,
}

K = 25
results = {}
evasions = []
for name, fn in VECTORS.items():
    det = 0
    tgts = targets(K)
    per = []
    for pos in tgts:
        rej, why = pipeline_rejects(fn(pos))
        det += 1 if rej else 0
        per.append({"pos": pos, "seq": ALL[pos].get("seq"), "detected": rej, "why": why})
        if not rej:
            evasions.append({"vector": name, "pos": pos, "seq": ALL[pos].get("seq")})
    results[name] = {"injected": len(tgts), "detected": det, "tpr": det / len(tgts), "cases": per}

summary = {
    "schema": "fase1_attacks.v1",
    "corpus_tag": "TFM-dataset-N500",
    "K_per_vector": K,
    "vectors": {n: {"injected": r["injected"], "detected": r["detected"], "tpr": r["tpr"]}
                for n, r in results.items()},
    "all_vectors_100pct": all(r["tpr"] == 1.0 for r in results.values()),
    "evasions": evasions,
    "note_A3": "A3-anchor-rollback: corpus has 0 chain.anchor events (verify_anchor_monotonicity checked=0); "
               "anchor is declared-window/dormant in the sealed corpus -> A3 live-vector NOT exercisable on this "
               "corpus (reported honestly; tested separately on a synthetic anchored fixture).",
}
out = ROOT / "_measure" / "fase1_attacks_result.json"
out.write_text(json.dumps({"summary": summary, "detail": results}, indent=2, sort_keys=True) + "\n", encoding="ascii")
print(json.dumps(summary, indent=2, sort_keys=True))
