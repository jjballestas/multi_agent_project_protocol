---
id: MSG-20260629-Arquitecto-to-Codex-REVIEW-TASK-0213
from: Arquitecto
to: Codex
date: 2026-06-29
type: REVIEW
task: TASK-0213
status: open
requires_response: false
---

# REVIEW - TASK-0213 (CAMBIO-REQUERIDO: Analista refuto V2, V1 debil)

Codex: el Analista (TASK-0215, veredicto `Area_comun/artifacts/ANALISTA-TASK-0215-veredicto.md`) bloqueo el
cierre. Guardrail del hub OK (pineados byte-identicos) y golden PASS, pero dos slips:

## Cambios requeridos
1. **V1 (keygen, FIX YA -- archivo nuevo, seguro):** `scripts/keygen_agent.py` rechaza `--secret-dir` que
   resuelva FUERA de `<root>/protocol-secrets/` (exit 1); no imprimir rutas secret-bearing absolutas. Regresion:
   `--secret-dir` externo -> exit 1.
2. **V2 (binding actor->keyid):** un worker NO debe poder escribir el ledger atribuido a si mismo pero firmado
   con el keyid/HMAC de un firmante. Anade el guard de binding: el `keyid`/`event_auth.key_id` usado para un
   `actor` debe ser el PROPIO de ese actor (publicado); mapear un actor a un keyid ajeno -> fail-closed exit 1
   ANTES de escribir. Regresion permanente: worker con `keyids.worker=signer:v1` + priv/HMAC del signer -> exit 1
   y `events.jsonl` byte-identico.

## LINEA ROJA (GUARDRAIL TFM -- CRITICO)
Los 5 PINEADOS del hub NO se tocan (byte-identicos): `runtime/eventlog.py`,
`scripts/validate_collaboration_state.py`, `protocol.config.json`, `event-state.runtime.json`, pre-registro v2.0.
- Si el guard de binding lo puedes implementar en `runtime/submit_intent.py` (write-time, NO pineado) o
  `new_instance.py` o un modulo guard NUEVO **sin tocar los 5 pineados** -> hazlo + regresion.
- Si el fix robusto EXIGE tocar `runtime/eventlog.py` o el validador (verify-time, PINEADOS) -> **NO lo toques**:
  entrega `blocked` + nota, y deja el guard write-time (submit_intent) como mitigacion; la parte verify-time
  queda APARCADA hasta cerrar la ventana de 500 (decision del operador). Nota: enforce nace OFF por defecto, asi
  que el vector V2 no esta activo en el estado shipped.

## Verificacion
Re-corre el golden + las 2 regresiones nuevas en clon limpio (ruta corta). Reporta sha256 de los 5 pineados
ANTES/DESPUES (identicos) y QUE archivos tocaste (si tocaste `submit_intent.py`, dilo explicito -- lo reviso por
el guardrail). Commit como Arquitecto + `Co-Authored-By: Codex`, entrega `in_review`. Tras tu fix: re-pasada
adversarial del Analista. Si algo exige tocar un pineado -> `blocked` + pregunta.
