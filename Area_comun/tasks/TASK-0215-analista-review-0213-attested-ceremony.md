---
task_id: TASK-0215
title: "Revision ADVERSARIAL de la ceremonia de instanciacion atestada (TASK-0213): keygen/firma/secretos/guardrail (DECISION-0069)"
type: review
status: done
owner: Analista
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
author_under_review: Codex
checker: Arquitecto
linked_decisions: [DECISION-0069]
file: Area_comun/tasks/TASK-0215-analista-review-0213-attested-ceremony.md
---

# TASK-0215 -- Revision adversarial de TASK-0213 (ceremonia atestada)

## Contexto
Codex entrego TASK-0213 (commit `d2d19e2`): `scripts/keygen_agent.py` + `new_instance.py --tier attested --roster`
+ `scripts/test_attested_instancing.py`. Implementa DECISION-0069 (keygen por firmante, workers keyless con
provenance, verificacion portable por tercero, guardrail TFM). Checker (Arquitecto) ya verifico: pineados del hub
byte-identicos (guardrail OK) y golden PASS. Por ser SENSIBLE A SEGURIDAD se pide tu pasada adversarial.

## Eres el 3er firmante -- entrega via LEDGER
Reclama TASK-0215 con submit_intent (claim ACQUIRE firmado Ed25519). Entrega el veredicto como artefacto
`Area_comun/artifacts/ANALISTA-TASK-0215-veredicto.md` + MSG REVIEW al Arquitecto, commit como autor Analista, y
RELEASE del claim. NO toques task_status.

## Vectores (clon limpio, exit codes; intenta REFUTAR)
- **V1 (secretos):** intenta que un secreto (privada PEM / HMAC) se IMPRIMA a stdout, se COMMITEE (no gitignored),
  o se filtre fuera de `protocol-secrets/`. Confirma que la privada nunca sale y que solo la PUBLICA es portable.
- **V2 (forja / worker keyless):** intenta que un WORKER keyless ESCRIBA el ledger bajo enforce (forjar actor_auth,
  reusar la clave de otro, atribucion cruzada). Debe fallar fail-closed antes de escribir.
- **V3 (verificacion por tercero):** monta un clon SIN `protocol-secrets/` y confirma que verifica el ledger via
  publicas (validate exit 0) y que NO se puede firmar sin la privada (fail-closed). Busca un falso-verde.
- **V4 (GUARDRAIL TFM):** confirma INDEPENDIENTEMENTE que correr keygen+ceremonia deja los pineados del hub
  (eventlog.py, validador, protocol.config.json, override) byte-identicos; intenta encontrar un camino que los toque.
- **V5 (genesis/cadena):** la instancia nueva tiene genesis sano (drift 0, cadena valida); enforce nace OFF.
- **V6 (neutralidad):** sin terminos de dominio en lo generado/neutral.

## Veredicto
Por vector SOSTIENE/DEBIL/REFUTADO + cambio exigido, con reproduccion (exit codes). Conclusion: TASK-0213
CERRABLE vs CAMBIO-REQUERIDO. ASCII-only (corre scan_encoding antes de commitear). Minimal narration.
