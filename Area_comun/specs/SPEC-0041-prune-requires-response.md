---
spec_id: SPEC-0041-prune-requires-response
task_id: TASK-0055
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0014, DECISION-0012]
relates_to: [SPEC-0033, SPEC-0034]
---

> Mini-spec de un FOLLOW-UP de higiene rastreado desde el cierre de Capa A. Fix de raiz, aditivo, con
> paridad py/.ps1. No cambia umbrales de poda (DECISION-0014) ni el comportamiento de claims/tasks del
> prune. NO requiere DECISION nueva. Si la implementacion obliga a un cambio incompatible => blocked.

# SPEC-0041 - Prune robusto ante mensajes que requieren respuesta

## 1. Problema

`scripts/prune_state.py` (`prune_mailbox`, ~127) mueve mensajes de `answered/` a `archived/` y fija
`status: archived` (`set_mailbox_status`, ~142). Durante el cierre de Capa A aparecio un mensaje en
`archived/` cuyo estado el validador (`validate_collaboration_state.py`, gate status<->carpeta de
TASK-0035, ~617-623) marca como **ERROR** (mismatch), y hubo que corregirlo a mano (MSG-capaA-completa).
El prune no debe dejar nunca un mismatch status<->carpeta, ni archivar un mensaje cuya conversacion sigue
**logicamente abierta** (`requires_response: true` sin resolver).

## 2. Diagnostico (a confirmar en codigo por Codex)

- Hipotesis: (a) algun camino deja un mensaje en `archived/` sin que su `status` quede en `archived`
  (mismatch); y/o (b) se archiva un mensaje cuya respuesta sigue pendiente (no deberia archivarse aun).
- `prune_mailbox` solo procesa `answered/`. El mismatch observado sugiere un mensaje `requires_response`
  que llego a `archived/` sin reconciliar. Codex (owner de scripts) ubica la causa exacta.

## 3. Alcance (fix de raiz, aditivo, paridad py/.ps1)

1. **No archivar lo que sigue abierto:** el prune **exime** del archivado a un mensaje con
   `requires_response: true` cuya respuesta no esta resuelta (sin respuesta enlazada / sin status de
   cierre). Lo deja donde corresponde en vez de moverlo a `archived/`.
2. **Reconciliar status al archivar:** todo mensaje que el prune mueva a `archived/` queda con
   `status: archived` garantizado (independiente del formato/encoding del frontmatter) -> nunca deja un
   mismatch status<->carpeta.
3. **Paridad** en `scripts/prune_state.ps1` (mismo comportamiento; atestiguada por Codex/CI).

## 4. Tests (golden determinista, sin red)

1. Plantar un mensaje `requires_response: true` sin resolver -> correr prune -> **NO** se archiva (sigue
   donde estaba); validador verde.
2. Mensaje `requires_response` resuelto (respuesta enlazada / status de cierre) -> prune lo archiva con
   `status: archived`; validador verde (0 mismatch status<->carpeta).
3. Segunda corrida de prune -> **no reintroduce** mismatches (idempotente respecto del gate).
4. Regresion: el resto del comportamiento del prune (claims/tasks/umbrales DECISION-0014) intacto.

## 5. Fuera de alcance

- Umbrales de poda y archivado de claims/tasks (DECISION-0014): sin cambios.
- Fase 5 (TASK-0054) y rutas de runtime de guardrails.
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer

- MINOR (correccion de higiene aditiva; no cambia contrato ni umbrales).
