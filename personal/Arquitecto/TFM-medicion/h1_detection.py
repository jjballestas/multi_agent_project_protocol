#!/usr/bin/env python3
"""TFM H1 -- Deteccion (TPR A1/A2/A3) + FPR + salud AC2 sobre el corpus sellado N=500.

INTEGRIDAD (vinculante, plan s.Reglas):
  * Mide SOLO el corpus del tag TFM-dataset-N500 (commit e3646ae). Lee una COPIA extraida
    con `git show ...:runtime/state/events.jsonl`; nunca el working tree vivo ni el ledger vivo.
  * La inyeccion de ataques es PROGRAMATICA y DETERMINISTA, con conteos. No hay juicio de agente.
  * La deteccion se evalua con el MECANISMO REAL del protocolo:
      - A1 (integridad/encadenado): runtime.protocol_replay.validate_chain + replay rejections.
      - A2 (no-repudio asimetrico, actor_auth Ed25519): runtime.eventlog.verify_actor_auth.
      - A3 (rollback del ancla): runtime.protocol_replay.verify_anchor_monotonicity + chain genesis.
  * Solo lee; no escribe el ledger; no commits.

USO:
  python personal/Arquitecto/TFM-medicion/h1_detection.py \
      --corpus personal/Arquitecto/TFM-medicion/corpus/events.jsonl \
      --config personal/Arquitecto/TFM-medicion/corpus/protocol.config.json \
      --out personal/Arquitecto/TFM-medicion/data

Salida: imprime JSON y escribe data/h1_detection.json + data/h1_attacks_raw.csv.
Determinista: cada ataque usa indices fijos (no aleatorio); re-ejecutar da identico.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# El medidor importa el MECANISMO REAL del protocolo (no reimplementa la deteccion).
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.eventlog import (  # noqa: E402
    ACTOR_AUTH_TAMPER_REASONS,
    actor_keyid,
    canonical_hash,
    canonical_json,
    compute_event_prev_hash,
    compute_genesis_prev_hash,
    verify_actor_auth,
)
from runtime.protocol_replay import validate_chain, verify_anchor_monotonicity  # noqa: E402

DATASET_START_SEQ = 2221  # ventana elegible canonica (monitor_dataset_ed25519.py)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        events.append(json.loads(line))
    return sorted(events, key=lambda e: int(e.get("seq") or 0))


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def eligible(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        e
        for e in events
        if int(e.get("seq") or 0) >= DATASET_START_SEQ
        and (e.get("actor_auth") or {}).get("method") == "ed25519"
    ]


# ---------------------------------------------------------------------------
# Deteccion = mecanismo real. Cada funcion devuelve (detectado: bool, motivo: str).
# ---------------------------------------------------------------------------

def detect_chain_break(events: list[dict[str, Any]], config: dict[str, Any], root: Path) -> tuple[bool, str]:
    """A1: integridad de la cadena. validate_chain del protocolo (hashes, secret-independiente)."""
    result = validate_chain(events, config, root=root)
    if result.get("valid") is not True:
        return True, f"chain:{result.get('reason')}@seq={result.get('seq')}"
    return False, "chain_valid"


def detect_actor_auth_tamper(events: list[dict[str, Any]], config: dict[str, Any], root: Path) -> tuple[bool, str]:
    """A2: no-repudio. verify_actor_auth del protocolo sobre cada evento elegible alterado."""
    for e in events:
        if int(e.get("seq") or 0) < DATASET_START_SEQ:
            continue
        res = verify_actor_auth(e, config, root)
        if res.get("valid") is not True and str(res.get("reason")) in ACTOR_AUTH_TAMPER_REASONS:
            return True, f"actor_auth:{res.get('reason')}@seq={e.get('seq')}"
    return False, "actor_auth_all_valid"


def detect_anchor_rollback(events: list[dict[str, Any]], config: dict[str, Any], root: Path) -> tuple[bool, str]:
    """A3: rollback/anclaje. Doble check: monotonia de chain.anchor + integridad del genesis de cadena.

    El corpus ancla via la cadena hash con genesis ligado a protocol.config.json. Un rollback del
    ancla = mover/retroceder el digest de cabeza anclado. Lo evaluamos con verify_anchor_monotonicity
    (si hay eventos chain.anchor) y, como el ancla efectiva del corpus es el genesis de cadena
    ligado al config, tambien con validate_chain (un rollback rompe el encadenado verificable).
    """
    anchors = verify_anchor_monotonicity(events, config)
    if anchors.get("valid") is not True:
        return True, f"anchor:{(anchors.get('findings') or [{}])[0].get('error')}"
    # Ancla efectiva del corpus: genesis de cadena ligado al config (DECISION #4).
    chain = validate_chain(events, config, root=root)
    if chain.get("valid") is not True:
        return True, f"anchor_via_chain:{chain.get('reason')}@seq={chain.get('seq')}"
    return False, "anchor_intact"


# ---------------------------------------------------------------------------
# Inyectores de ataque (deterministas). Operan sobre COPIAS profundas.
# Cada inyector recibe la lista completa de eventos del corpus (para mantener cadena)
# y el conjunto de seqs elegibles; muta de forma puntual y reproducible.
# ---------------------------------------------------------------------------

def _target_seqs(elig_seqs: list[int], k: int) -> list[int]:
    """k seqs elegibles distribuidos de forma DETERMINISTA (inicio, paso fijo)."""
    if k <= 0 or not elig_seqs:
        return []
    if k >= len(elig_seqs):
        return list(elig_seqs)
    step = len(elig_seqs) / k
    return [elig_seqs[int(i * step)] for i in range(k)]


def by_seq(events: list[dict[str, Any]], seq: int) -> dict[str, Any]:
    for e in events:
        if int(e.get("seq") or 0) == seq:
            return e
    raise KeyError(seq)


# --- A1: integridad del ledger (rompe prev_hash / orden) ---

def a1_payload_alteration(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    ev = by_seq(m, seq)
    # Alteracion puntual del payload: cambia un valor estructural -> prev_hash deja de cuadrar.
    ev.setdefault("payload", {})["__tamper__"] = "altered"
    return m


def a1_event_deletion(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    # Borra un evento elegible -> gap en seq y prev_hash del siguiente no cuadra.
    return [deepcopy(e) for e in events if int(e.get("seq") or 0) != seq]


def a1_event_insertion(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    template = deepcopy(by_seq(m, seq))
    forged = deepcopy(template)
    forged["seq"] = seq  # colision/duplicado de seq -> rompe contiguidad y prev_hash
    forged["idempotency_key"] = f"forged:insert:{seq}"
    forged.setdefault("payload", {})["__forged__"] = True
    # Insertar justo despues del objetivo (conserva orden por seq al re-ordenar el validador).
    out: list[dict[str, Any]] = []
    for e in m:
        out.append(e)
        if int(e.get("seq") or 0) == seq:
            out.append(forged)
    return out


def a1_event_reordering(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    # Intercambia prev_hash de dos eventos elegibles consecutivos (reordenamiento que
    # validate_chain detecta como hash mismatch aunque el orden por seq se mantenga).
    idx = next(i for i, e in enumerate(m) if int(e.get("seq") or 0) == seq)
    nxt = idx + 1
    while nxt < len(m) and int(m[nxt].get("seq") or 0) < DATASET_START_SEQ:
        nxt += 1
    if nxt >= len(m):
        # objetivo es el ultimo elegible: intercambia con el anterior elegible
        prev = idx - 1
        while prev >= 0 and int(m[prev].get("seq") or 0) < DATASET_START_SEQ:
            prev -= 1
        nxt = prev
    m[idx]["prev_hash"], m[nxt]["prev_hash"] = m[nxt].get("prev_hash"), m[idx].get("prev_hash")
    return m


# --- A2: atribucion/firma (rompe actor_auth Ed25519) ---

def _other_actor(cur: str) -> str:
    return "Codex" if cur != "Codex" else "Arquitecto"


def a2_cross_attribution(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    ev = by_seq(m, seq)
    # Firmar como otro agente: cambiar el actor manteniendo keyid/sig del original
    # -> keyid_mismatch (la firma valida del actor original ya no corresponde al actor declarado).
    ev["actor"] = _other_actor(str(ev.get("actor") or ""))
    return m


def a2_cross_attribution_forged_keyid(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    """Variante ADVERSARIAL fuerte: reescribe actor Y keyid de forma coherente (intenta
    re-atribuir la autoria a otro agente con su propio keyid). La firma Ed25519 liga el
    evento canonico incl. `actor`, asi que NO valida -> invalid_signature. Demuestra el
    no-repudio real: ni con keyid coherente se puede falsear la autoria."""
    m = deepcopy(events)
    ev = by_seq(m, seq)
    other = _other_actor(str(ev.get("actor") or ""))
    ev["actor"] = other
    ev.setdefault("actor_auth", {})["keyid"] = actor_keyid(other, None, None)
    return m


def a2_foreign_keyid(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    ev = by_seq(m, seq)
    # keyid no registrado / ajeno -> keyid_mismatch o unknown_keyid.
    ev.setdefault("actor_auth", {})["keyid"] = "intruso:v9"
    return m


def a2_invalid_signature(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    m = deepcopy(events)
    ev = by_seq(m, seq)
    # Firma Ed25519 invalida: corromper la firma base64 (mismo largo, bits cambiados) -> invalid_signature.
    sig = str(ev.get("actor_auth", {}).get("sig") or "")
    if sig:
        # Invierte el primer caracter base64 a otro distinto de forma determinista.
        flipped = ("B" if sig[0] != "B" else "C") + sig[1:]
        ev["actor_auth"]["sig"] = flipped
    return m


# --- A3: rollback del ancla / digest de cabeza no anclado ---

def a3_anchor_rollback(events: list[dict[str, Any]], seq: int) -> list[dict[str, Any]]:
    """Rollback del ancla declarada: el ancla del corpus es el genesis de cadena ligado al
    config (#4). Un rollback = el digest de cabeza anclado deja de ligar la cadena. Lo
    materializamos retrocediendo el prev_hash del evento elegible (la cabeza encadenada del
    segmento elegible deja de anclar a su predecesor) -> validate_chain reporta corrupcion.
    Es el caso 'digest de cabeza no anclado / ventana declarada' del plan s.1 A3.
    """
    m = deepcopy(events)
    ev = by_seq(m, seq)
    # Retrocede el ancla: usa un prev_hash invalido (cero) simulando un ancla rebobinada.
    ev["prev_hash"] = "0" * 64
    return m


AttackInjector = Callable[[list[dict[str, Any]], int], list[dict[str, Any]]]

# (vector, nombre, inyector, detector)
VECTORS: dict[str, list[tuple[str, AttackInjector, str]]] = {
    "A1": [
        ("payload_alteration", a1_payload_alteration, "chain"),
        ("event_deletion", a1_event_deletion, "chain"),
        ("event_insertion", a1_event_insertion, "chain"),
        ("event_reordering", a1_event_reordering, "chain"),
    ],
    "A2": [
        ("cross_attribution", a2_cross_attribution, "actor_auth"),
        ("cross_attribution_forged_keyid", a2_cross_attribution_forged_keyid, "actor_auth"),
        ("foreign_keyid", a2_foreign_keyid, "actor_auth"),
        ("invalid_signature", a2_invalid_signature, "actor_auth"),
    ],
    "A3": [
        ("anchor_rollback", a3_anchor_rollback, "anchor"),
    ],
}

DETECTORS = {
    "chain": detect_chain_break,
    "actor_auth": detect_actor_auth_tamper,
    "anchor": detect_anchor_rollback,
}


def run(corpus: Path, config_path: Path, out_dir: Path, k_per_subtype: int) -> dict[str, Any]:
    events = load_events(corpus)
    config = load_config(config_path)
    # root del clon = carpeta del corpus (contiene protocol.config.json para genesis del chain).
    root = corpus.parent.resolve()

    elig = eligible(events)
    elig_seqs = sorted(int(e.get("seq") or 0) for e in elig)
    breakdown: dict[str, int] = {}
    for e in elig:
        a = str(e.get("actor") or "?")
        breakdown[a] = breakdown.get(a, 0) + 1

    # Sanity: el corpus limpio debe ser detectado como LIMPIO por los tres detectores
    # (esto es tambien el control de FPR de la cadena/firma/ancla; ver h1_fpr_ac2.py para los 500).
    baseline = {
        "chain": detect_chain_break(events, config, root),
        "actor_auth": detect_actor_auth_tamper(events, config, root),
        "anchor": detect_anchor_rollback(events, config, root),
    }
    baseline_clean = all(det[0] is False for det in baseline.values())

    raw_rows: list[dict[str, Any]] = []
    per_vector: dict[str, dict[str, Any]] = {}

    for vector, subtypes in VECTORS.items():
        injected = 0
        detected = 0
        evasions: list[dict[str, Any]] = []
        per_subtype: dict[str, dict[str, int]] = {}
        for sub_name, injector, det_key in subtypes:
            seqs = _target_seqs(elig_seqs, k_per_subtype)
            sub_injected = 0
            sub_detected = 0
            detector = DETECTORS[det_key]
            for seq in seqs:
                mutated = injector(events, seq)
                is_detected, reason = detector(mutated, config, root)
                injected += 1
                sub_injected += 1
                if is_detected:
                    detected += 1
                    sub_detected += 1
                else:
                    evasions.append({"subtype": sub_name, "seq": seq})
                raw_rows.append(
                    {
                        "vector": vector,
                        "subtype": sub_name,
                        "target_seq": seq,
                        "detector": det_key,
                        "detected": int(is_detected),
                        "reason": reason,
                    }
                )
            per_subtype[sub_name] = {"injected": sub_injected, "detected": sub_detected}
        per_vector[vector] = {
            "injected": injected,
            "detected": detected,
            "tpr": (detected / injected) if injected else None,
            "evasions": evasions,
            "per_subtype": per_subtype,
        }

    all_tpr_100 = all(v["tpr"] == 1.0 for v in per_vector.values())
    total_injected = sum(v["injected"] for v in per_vector.values())
    total_detected = sum(v["detected"] for v in per_vector.values())

    result = {
        "schema": "tfm_h1_detection.v1",
        "generated_utc": utc_now(),
        "corpus": str(corpus),
        "config": str(config_path),
        "dataset_start_seq": DATASET_START_SEQ,
        "k_per_subtype": k_per_subtype,
        "eligible_total": len(elig),
        "eligible_breakdown": dict(sorted(breakdown.items())),
        "baseline_corpus_clean": baseline_clean,
        "baseline_detail": {k: {"detected": v[0], "reason": v[1]} for k, v in baseline.items()},
        "per_vector": per_vector,
        "totals": {"injected": total_injected, "detected": total_detected},
        "threshold_s5": "detection == 100% en TODOS los vectores (binario, AC3)",
        "all_vectors_tpr_100": all_tpr_100,
        "verdict_detection": "CONFIRMADA" if (all_tpr_100 and baseline_clean) else "REFUTADA",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "h1_detection.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (out_dir / "h1_attacks_raw.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh, fieldnames=["vector", "subtype", "target_seq", "detector", "detected", "reason"]
        )
        writer.writeheader()
        writer.writerows(raw_rows)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=50, help="ataques por subtipo (determinista)")
    args = ap.parse_args()
    result = run(Path(args.corpus), Path(args.config), Path(args.out), args.k)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict_detection"] == "CONFIRMADA" else 1


if __name__ == "__main__":
    raise SystemExit(main())
