---
spec_id: SPEC-0051-prune-next-actions
task_id: TASK-0065
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0014, DECISION-0012]
relates_to: [SPEC-0033, SPEC-0041]
---

> Mini-spec del FOLLOW-UP de higiene rastreado desde Capa A / D2.1: el prune poda claims/tasks/mailbox
> pero NO condensa `next_actions`. Fix de raiz, aditivo, paridad py/.ps1 (la .ps1 delega en la .py).
> No cambia umbrales de poda (DECISION-0014) ni el comportamiento existente del prune. NO requiere
> DECISION nueva.

# SPEC-0051 - Prune condensa next_actions de PROJECT_STATE

## 1. Problema

`scripts/prune_state.py:prune_project_state` solo podaba `active_tasks`. El arreglo
`PROJECT_STATE.json#next_actions` crecia sin limite (28 entradas; el historico previo se condenso A MANO
con una entrada centinela "[HISTORICO PODADO]"). Esto infla el cold-start (presupuesto de tokens,
DECISION-0014) y obliga a poda manual.

## 2. Solucion

1. **Umbral config-gated** `recent_next_actions` en `protocol.config.json#maintenance` (default 0 / ausente
   => comportamiento previo, no condensa). Vivo: 8; template: 8 (gateado por `maintenance.enabled:false`).
2. **Condensacion determinista** en `prune_project_state` via `condense_next_actions`: cuando el numero de
   entradas regulares (no centinela) supera el umbral, conserva las N mas recientes y reemplaza el resto por
   UNA entrada centinela "[HISTORICO PODADO] <total> next_actions historicas condensadas por el prune
   (DECISION-0014); trazabilidad en git history + memoria de Claude". Centinelas previos se preservan
   fusionando su conteo (parseo de "[HISTORICO PODADO] <n>").
3. **Idempotente:** una segunda corrida no re-condensa (las regulares ya son <= umbral) ni duplica centinela.
4. **Paridad** py/.ps1 automatica (la .ps1 delega en la .py). Reportado en el run-log como
   `next_actions_condensed`.

## 3. Tests (golden determinista, sin red; examples/runtime_prune_cases)

1. Sobre umbral -> condensa: 1 centinela + N recientes; conteo correcto; idempotente (segunda corrida igual).
2. Bajo umbral -> sin cambios.
3. Umbral ausente/0 -> comportamiento previo intacto.
4. Centinela previo -> fusiona conteo (37 + condensadas) y conserva N recientes.
5. Regresion: mailbox-safety y claims/tasks (DECISION-0014/SPEC-0041) intactos.

## 4. Fuera de alcance

- Umbrales y logica de claims/tasks/mailbox (DECISION-0014/SPEC-0041): sin cambios.
- Reescritura del texto de las next_actions (solo se condensa la lista).
- Cambio incompatible de contrato => blocked + DECISION.

## 5. SemVer

- MINOR (correccion de higiene aditiva; config-gated; no cambia contrato ni umbrales existentes).
