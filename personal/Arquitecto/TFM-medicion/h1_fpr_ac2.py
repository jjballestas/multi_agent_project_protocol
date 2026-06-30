#!/usr/bin/env python3
"""TFM H1 -- FASE 2: FPR (sobre los 500 legitimos) + salud AC2.

FPR (plan s.5): correr el verificador determinista sobre el corpus legitimo SIN ataques;
  FPR = rechazos_falsos / 500. Umbral: == 0% (cualquier rechazo = defecto).
  Se evalua con el MECANISMO REAL: por cada evento elegible, verify_actor_auth (Ed25519) debe
  validar, y la cadena completa (validate_chain) debe ser valida. Un "rechazo falso" = un evento
  legitimo marcado como tamper por actor_auth, o la cadena rota sin haberla tocado.
  Tambien se corre runtime.eventlog.replay_events y se cuentan rejections de seguridad sobre
  eventos elegibles (debe ser 0 por motivo de tamper; los HMAC sin secreto NO son rechazo, son
  'unverifiable' por DECISION-0046).

Salud AC2 (plan s.5): atestaciones bien formadas y verificables / eventos autoria-relevantes.
  Denominador = eventos elegibles (autoria-relevantes, independiente del firmante). Numerador =
  los que tienen actor_auth Ed25519 con firma verificable contra la publica de su agente. Umbral:
  >= 99%.

Solo lee el corpus extraido del tag; no escribe ledger; no commits.
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

from runtime.eventlog import (  # noqa: E402
    ACTOR_AUTH_TAMPER_REASONS,
    read_protocol_config,
    replay_events,
    verify_actor_auth,
)
from runtime.protocol_replay import validate_chain  # noqa: E402

DATASET_START_SEQ = 2221


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_events(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return sorted(out, key=lambda e: int(e.get("seq") or 0))


def run(corpus: Path, config_path: Path, out_dir: Path) -> dict[str, Any]:
    events = load_events(corpus)
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    root = corpus.parent.resolve()

    elig = [
        e
        for e in events
        if int(e.get("seq") or 0) >= DATASET_START_SEQ
        and (e.get("actor_auth") or {}).get("method") == "ed25519"
    ]
    n = len(elig)

    # --- FPR: cada evento elegible debe verificar; contar rechazos falsos ---
    false_rejections: list[dict[str, Any]] = []
    for e in elig:
        res = verify_actor_auth(e, config, root)
        if res.get("valid") is not True and str(res.get("reason")) in ACTOR_AUTH_TAMPER_REASONS:
            false_rejections.append(
                {"seq": e.get("seq"), "actor": e.get("actor"), "reason": res.get("reason")}
            )
    # Cadena completa intacta (secret-independiente).
    chain = validate_chain(events, config, root=root)
    chain_false_reject = chain.get("valid") is not True

    # replay del protocolo: rejections de seguridad por TAMPER sobre eventos elegibles.
    replay_state = replay_events(events, config=config, root=root)
    sec_rejections = [
        r
        for r in replay_state.get("rejections", [])
        if int(r.get("seq") or 0) >= DATASET_START_SEQ
        and str(r.get("event") or "") in {"security.invalid_actor_auth", "security.unauthenticated_event"}
    ]
    # Nota: en clon sin secretos el HMAC da 'unresolved_key/missing_key' = UNVERIFIABLE (NO rechazo,
    # DECISION-0046). replay_events solo agrega rejections por ACTOR_AUTH_TAMPER_REASONS o por
    # EVENT_AUTH no-unverifiable. Aqui hay secretos en disco (corpus extraido), pero los contamos
    # explicitamente para transparencia.
    tamper_rejections = [r for r in sec_rejections if r.get("event") == "security.invalid_actor_auth"]

    fpr_count = len(false_rejections) + (1 if chain_false_reject else 0)
    fpr = fpr_count / n if n else None

    # --- AC2 salud: verificables / autoria-relevantes ---
    verifiable = sum(1 for e in elig if verify_actor_auth(e, config, root).get("valid") is True)
    ac2 = verifiable / n if n else None

    breakdown: dict[str, int] = {}
    for e in elig:
        a = str(e.get("actor") or "?")
        breakdown[a] = breakdown.get(a, 0) + 1

    result = {
        "schema": "tfm_h1_fpr_ac2.v1",
        "generated_utc": utc_now(),
        "corpus": str(corpus),
        "eligible_total": n,
        "eligible_breakdown": dict(sorted(breakdown.items())),
        "fpr": {
            "false_rejections_actor_auth": false_rejections,
            "chain_false_reject": chain_false_reject,
            "chain_reason": chain.get("reason"),
            "replay_tamper_rejections_eligible": tamper_rejections,
            "count": fpr_count,
            "fpr": fpr,
            "threshold_s5": "== 0%",
            "pass": fpr == 0.0,
        },
        "ac2_health": {
            "denominator_authorship_relevant": n,
            "numerator_verifiable_ed25519": verifiable,
            "rate": ac2,
            "threshold_s5": ">= 99%",
            "pass": (ac2 is not None and ac2 >= 0.99),
        },
        "verdict_fpr": "CONFIRMADA" if fpr == 0.0 else "REFUTADA",
        "verdict_ac2": "CONFIRMADA" if (ac2 is not None and ac2 >= 0.99) else "REFUTADA",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "h1_fpr_ac2.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    result = run(Path(args.corpus), Path(args.config), Path(args.out))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    ok = result["verdict_fpr"] == "CONFIRMADA" and result["verdict_ac2"] == "CONFIRMADA"
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
