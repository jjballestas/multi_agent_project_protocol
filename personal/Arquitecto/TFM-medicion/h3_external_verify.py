#!/usr/bin/env python3
"""TFM H3 -- Verificabilidad independiente (clon limpio, solo claves PUBLICAS).

Umbrales pre-comprometidos (plan s.5 / pre-registro s.5):
  * Acuerdo de veredicto externo == 100% sobre los 500 (verdicto identico al interno).
  * Match clon-limpio: hash canonico (con secretos) == (sin secretos) -> SI.
  * Firmas Ed25519 verificables con la publica de cada agente.

Camino REAL secret-independiente (DECISION-0046):
  - El verificador externo corre runtime.protocol_replay sobre un CLON LIMPIO del tag SIN secretos
    (solo signature_config.public_keys en protocol.config.json). El hash canonico del estado de
    protocolo (replay_protocol_state -> protocol_snapshot.canonical_hash) NO depende de secretos:
    los HMAC sin secreto se clasifican 'unresolved_key/missing_key' = UNVERIFIABLE y NO mutan el
    estado materializado. Por tanto el hash con y sin secretos debe coincidir.
  - "Veredicto" por evento elegible = la pareja (chain_ok_global, actor_auth_valid_evento). El
    externo (clon limpio) debe coincidir 1:1 con el interno (corpus con acceso a secretos).
  - Firmas Ed25519: verify_actor_auth con SOLO las publicas del config -> todas validas.

ENTRADAS:
  --internal-root : raiz CON acceso a secretos (la del repo vivo) para el lado 'interno'.
  --external-root : raiz del CLON LIMPIO sin secretos (materializado de git archive del tag).
Ambas raices contienen el MISMO events.jsonl + protocol.config.json del tag.

Solo lee; no escribe ledger; no commits.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.eventlog import verify_actor_auth, verify_event_auth  # noqa: E402
from runtime.protocol_replay import (  # noqa: E402
    replay_protocol_state,
    validate_chain,
)

DATASET_START_SEQ = 2221


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_events(root: Path) -> list[dict[str, Any]]:
    path = root / "runtime" / "state" / "events.jsonl"
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return sorted(out, key=lambda e: int(e.get("seq") or 0))


def load_config(root: Path) -> dict[str, Any]:
    return json.loads((root / "protocol.config.json").read_text(encoding="utf-8-sig"))


def per_event_verdict(events: list[dict[str, Any]], config: dict[str, Any], root: Path) -> dict[int, dict[str, Any]]:
    """Veredicto por evento elegible: actor_auth Ed25519 valido (secret-independiente) +
    event_auth resultado (depende de secretos: aqui lo registramos pero NO afecta el veredicto
    de autoria, que es el medido en H1/H3)."""
    chain = validate_chain(events, config, root=root)
    verdict: dict[int, dict[str, Any]] = {}
    for e in events:
        seq = int(e.get("seq") or 0)
        if seq < DATASET_START_SEQ or (e.get("actor_auth") or {}).get("method") != "ed25519":
            continue
        aa = verify_actor_auth(e, config, root)
        ea = verify_event_auth(e, config, root=root)
        verdict[seq] = {
            "actor_auth_valid": bool(aa.get("valid") is True),
            "actor_auth_reason": aa.get("reason"),
            "event_auth_valid": bool(ea.get("valid") is True),
            "event_auth_reason": ea.get("reason"),
            "chain_valid": bool(chain.get("valid") is True),
        }
    return verdict


def secret_independent_state_hash(root: Path) -> str:
    events = load_events(root)
    config = load_config(root)
    snap = replay_protocol_state(events, root=root)
    return str(snap.get("canonical_hash") or "")


def run(internal_root: Path, external_root: Path, out_dir: Path) -> dict[str, Any]:
    int_events = load_events(internal_root)
    int_config = load_config(internal_root)
    ext_events = load_events(external_root)
    ext_config = load_config(external_root)

    # --- Veredicto de AUTORIA por evento (la metrica de acuerdo de H3) ---
    internal_v = per_event_verdict(int_events, int_config, internal_root.resolve())
    external_v = per_event_verdict(ext_events, ext_config, external_root.resolve())

    seqs = sorted(set(internal_v) | set(external_v))
    agree = 0
    disagreements: list[dict[str, Any]] = []
    ext_all_actor_auth_valid = True
    for s in seqs:
        iv = internal_v.get(s)
        ev = external_v.get(s)
        # Acuerdo sobre la validez de autoria (actor_auth Ed25519, secret-independiente).
        i_ok = iv["actor_auth_valid"] if iv else None
        e_ok = ev["actor_auth_valid"] if ev else None
        if ev and not ev["actor_auth_valid"]:
            ext_all_actor_auth_valid = False
        if i_ok == e_ok and i_ok is not None:
            agree += 1
        else:
            disagreements.append({"seq": s, "internal": i_ok, "external": e_ok})
    n = len(seqs)
    agreement_rate = (agree / n) if n else None

    # --- Match clon-limpio del hash canonico (con secretos vs sin secretos) ---
    internal_hash = secret_independent_state_hash(internal_root)
    external_hash = secret_independent_state_hash(external_root)
    hashes_match = internal_hash == external_hash and bool(internal_hash)

    # --- Conteo de firmas Ed25519 verificables con SOLO publicas en el clon limpio ---
    ext_verifiable = sum(1 for v in external_v.values() if v["actor_auth_valid"])
    # HMAC en clon limpio: sin secretos -> debe ser 'unverifiable' (NO tamper). Lo evidenciamos.
    ext_event_auth_reasons: dict[str, int] = {}
    for v in external_v.values():
        r = str(v.get("event_auth_reason"))
        ext_event_auth_reasons[r] = ext_event_auth_reasons.get(r, 0) + 1

    verdict_h3 = (
        "CONFIRMADA"
        if (agreement_rate == 1.0 and hashes_match and ext_all_actor_auth_valid)
        else "REFUTADA"
    )

    breakdown: dict[str, int] = {}
    for e in ext_events:
        seq = int(e.get("seq") or 0)
        if seq >= DATASET_START_SEQ and (e.get("actor_auth") or {}).get("method") == "ed25519":
            a = str(e.get("actor") or "?")
            breakdown[a] = breakdown.get(a, 0) + 1

    result = {
        "schema": "tfm_h3_external_verify.v1",
        "generated_utc": utc_now(),
        "internal_root": str(internal_root),
        "external_root_clean_clone": str(external_root),
        "eligible_total": n,
        "eligible_breakdown_clean_clone": dict(sorted(breakdown.items())),
        "agreement": {
            "eligible_compared": n,
            "agree": agree,
            "rate": agreement_rate,
            "disagreements": disagreements,
            "threshold_s5": "== 100%",
            "pass": agreement_rate == 1.0,
        },
        "clean_clone_hash_match": {
            "internal_state_canonical_hash": internal_hash,
            "external_state_canonical_hash": external_hash,
            "match": hashes_match,
            "threshold_s5": "match == si",
            "pass": hashes_match,
        },
        "ed25519_public_only_verification": {
            "verifiable_signatures_clean_clone": ext_verifiable,
            "of_total": n,
            "all_valid": ext_all_actor_auth_valid,
            "event_auth_reasons_clean_clone": ext_event_auth_reasons,
            "note": (
                "En el clon limpio las firmas Ed25519 (actor_auth) verifican con SOLO las publicas "
                "del config. El HMAC (event_auth) sin secreto se clasifica unverifiable "
                "(unresolved_key/missing_key) por DECISION-0046, NO como tamper: por eso el hash de "
                "estado es identico con y sin secretos."
            ),
        },
        "verdict_h3": verdict_h3,
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "h3_external_verify.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--internal-root", required=True, help="raiz CON acceso a secretos")
    ap.add_argument("--external-root", required=True, help="raiz del clon limpio SIN secretos")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    result = run(Path(args.internal_root), Path(args.external_root), Path(args.out))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["verdict_h3"] == "CONFIRMADA" else 1


if __name__ == "__main__":
    raise SystemExit(main())
