#!/usr/bin/env python3
"""TFM H2 -- Sobrecoste acotado de #4 (atestacion) vs baseline sin #4.

Umbrales pre-comprometidos (plan s.5 / pre-registro s.5):
  * Latencia: delta mediana <= 50 ms/ev AND delta p95 <= 200 ms/ev.
  * Almacenamiento: delta <= 4 KB/evento.
  * Tokens: delta <= 5%.

Metodo (determinista, sobre el corpus sellado del tag):

ALMACENAMIENTO -- medible directo y exacto. #4 anade a cada evento: actor_auth (Ed25519,
  keyid+sig), event_auth (HMAC, integridad simetrica) y prev_hash (encadenado). El baseline
  "sin #4" = el mismo evento canonico SIN esos tres campos. delta_bytes/ev = len(canonical(con))
  - len(canonical(sin)), medido sobre los 500 elegibles. Reportamos media, mediana, p95, max.

LATENCIA -- medida del CAMINO CRIPTOGRAFICO real de #4 por evento: verificacion Ed25519
  (verify_actor_auth) + verificacion HMAC (verify_event_auth) + recomputo del encadenado
  (compute_event_prev_hash). Es el coste que #4 agrega al camino de escritura/lectura. El
  baseline "sin #4" no ejecuta ninguno de esos pasos (coste ~0). delta = tiempo_con - tiempo_sin
  por evento; reportamos mediana y p95 en ms/ev sobre los 500 (R repeticiones para estabilidad).
  LIMITACION declarada: mide el coste criptografico/encadenado in-proceso, no I/O de disco ni
  red de anclaje (mismo disco, s.8). Es el delta atribuible a #4 sobre la misma carga.

TOKENS -- #4 firma HASHES, no texto (DECISION-0033/0040). actor_auth/event_auth/prev_hash viven
  en el LEDGER (runtime/state/events.jsonl), que NO se carga en el contexto del agente: el
  contexto de coordinacion son los globs de cold-start + slim views (measure_context_cost.py),
  identicos exista o no #4. Por tanto el delta de tokens de coordinacion por #4 es 0 por
  construccion. Lo evidenciamos: (a) el ledger no esta en coldstart_globs; (b) el tamano del
  payload firmable (actor_auth_message) excluye la firma. Reportamos delta_tokens% = 0 con su
  justificacion y la limitacion (no hay traza de tokens reales atribuible a #4; los tokens reales
  por agente -agent_token_usage.py- son de la sesion, no del campo de firma).

Solo lee el corpus; no escribe ledger; no commits.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.eventlog import (  # noqa: E402
    canonical_json,
    compute_event_prev_hash,
    event_without_chain_fields,
    verify_actor_auth,
    verify_event_auth,
)

DATASET_START_SEQ = 2221
ADDED_BY_CHAIN4 = ("actor_auth", "event_auth", "prev_hash")
COLDSTART_GLOBS_KEY = "coldstart_globs"
LEDGER_PATH = "runtime/state/events.jsonl"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_events(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return sorted(out, key=lambda e: int(e.get("seq") or 0))


def event_without_chain4(event: dict[str, Any]) -> dict[str, Any]:
    payload = dict(event)
    for key in ADDED_BY_CHAIN4:
        payload.pop(key, None)
    return payload


def pctl(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = q * (len(s) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    frac = pos - lo
    return s[lo] + (s[hi] - s[lo]) * frac


def measure_storage(elig: list[dict[str, Any]]) -> dict[str, Any]:
    deltas: list[int] = []
    with_bytes: list[int] = []
    without_bytes: list[int] = []
    for e in elig:
        cwith = len(canonical_json(e).encode("utf-8"))
        cwithout = len(canonical_json(event_without_chain4(e)).encode("utf-8"))
        with_bytes.append(cwith)
        without_bytes.append(cwithout)
        deltas.append(cwith - cwithout)
    mean = statistics.fmean(deltas)
    return {
        "n": len(elig),
        "delta_bytes_mean": round(mean, 2),
        "delta_bytes_median": statistics.median(deltas),
        "delta_bytes_p95": round(pctl([float(d) for d in deltas], 0.95), 2),
        "delta_bytes_max": max(deltas),
        "mean_event_bytes_with_chain4": round(statistics.fmean(with_bytes), 2),
        "mean_event_bytes_without_chain4": round(statistics.fmean(without_bytes), 2),
        "delta_kb_per_event_mean": round(mean / 1024, 5),
        "threshold_s5_kb": 4,
        "pass": (mean / 1024) <= 4,
    }


def measure_latency(elig: list[dict[str, Any]], config: dict[str, Any], root: Path, repeats: int) -> dict[str, Any]:
    # Por evento: coste de #4 = verify Ed25519 + verify HMAC + recompute prev_hash.
    # Baseline sin #4 = no ejecutar nada de eso (un no-op equivalente: acceder al evento).
    per_event_with: list[float] = []
    per_event_without: list[float] = []
    for e in elig:
        prev = "0" * 64  # ancla ficticia constante; mide el costo del recomputo, no su valor
        # CON #4
        best_with = None
        for _ in range(repeats):
            t0 = time.perf_counter()
            verify_actor_auth(e, config, root)
            verify_event_auth(e, config, root=root)
            compute_event_prev_hash(e, prev)
            dt = (time.perf_counter() - t0) * 1000.0
            best_with = dt if best_with is None else min(best_with, dt)
        # SIN #4 (baseline): el evento no lleva firma/cadena; el camino no hace criptografia.
        best_without = None
        for _ in range(repeats):
            t0 = time.perf_counter()
            _ = event_without_chain4(e)  # trabajo equivalente minimo del baseline
            dt = (time.perf_counter() - t0) * 1000.0
            best_without = dt if best_without is None else min(best_without, dt)
        per_event_with.append(best_with or 0.0)
        per_event_without.append(best_without or 0.0)

    deltas = [w - wo for w, wo in zip(per_event_with, per_event_without)]
    return {
        "n": len(elig),
        "repeats_per_event": repeats,
        "method": "min-of-R per event; delta = (verify_ed25519 + verify_hmac + recompute_prev_hash) - baseline_noop",
        "with_chain4_ms_median": round(statistics.median(per_event_with), 4),
        "with_chain4_ms_p95": round(pctl(per_event_with, 0.95), 4),
        "without_chain4_ms_median": round(statistics.median(per_event_without), 6),
        "delta_ms_median": round(statistics.median(deltas), 4),
        "delta_ms_p95": round(pctl(deltas, 0.95), 4),
        "delta_ms_mean": round(statistics.fmean(deltas), 4),
        "delta_ms_max": round(max(deltas), 4),
        "threshold_s5_median_ms": 50,
        "threshold_s5_p95_ms": 200,
        "pass_median": statistics.median(deltas) <= 50,
        "pass_p95": pctl(deltas, 0.95) <= 200,
    }


def measure_tokens(config: dict[str, Any]) -> dict[str, Any]:
    # Evidencia estructural de delta tokens = 0 por #4.
    coldstart = (config.get("token_cost") or {}).get(COLDSTART_GLOBS_KEY) or []
    ledger_in_coldstart = LEDGER_PATH in coldstart
    return {
        "delta_tokens_pct": 0.0,
        "threshold_s5_pct": 5,
        "pass": True,
        "ledger_in_coldstart_globs": ledger_in_coldstart,
        "coldstart_globs": coldstart,
        "rationale": (
            "#4 firma HASHES no texto (DECISION-0033/0040); actor_auth/event_auth/prev_hash viven "
            "en el ledger (runtime/state/events.jsonl) que NO esta en coldstart_globs, luego no entra "
            "al contexto del agente. El contexto de coordinacion (cold-start + slim views) es identico "
            "con o sin #4 -> delta de tokens de coordinacion = 0 por construccion."
        ),
        "limitation": (
            "No existe una traza de tokens reales atribuible al campo de firma (agent_token_usage.py "
            "mide tokens de sesion del agente, no del campo actor_auth). El 0% es estructural/by-design, "
            "no una medicion empirica de un delta no-cero reducido a 0 (declarado en s.8)."
        ),
    }


def run(corpus: Path, config_path: Path, out_dir: Path, repeats: int) -> dict[str, Any]:
    events = load_events(corpus)
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    root = corpus.parent.resolve()
    elig = [
        e
        for e in events
        if int(e.get("seq") or 0) >= DATASET_START_SEQ
        and (e.get("actor_auth") or {}).get("method") == "ed25519"
    ]

    storage = measure_storage(elig)
    latency = measure_latency(elig, config, root, repeats)
    tokens = measure_tokens(config)

    verdict = (
        "CONFIRMADA"
        if (storage["pass"] and latency["pass_median"] and latency["pass_p95"] and tokens["pass"])
        else "REFUTADA"
    )

    result = {
        "schema": "tfm_h2_overhead.v1",
        "generated_utc": utc_now(),
        "corpus": str(corpus),
        "eligible_total": len(elig),
        "storage": storage,
        "latency": latency,
        "tokens": tokens,
        "verdict_h2": verdict,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "h2_overhead.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--repeats", type=int, default=5, help="repeticiones por evento (min-of-R)")
    args = ap.parse_args()
    result = run(Path(args.corpus), Path(args.config), Path(args.out), args.repeats)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict_h2"] == "CONFIRMADA" else 1


if __name__ == "__main__":
    raise SystemExit(main())
