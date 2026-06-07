---
spec_id: SPEC-0051-prune-next-actions
task_id: TASK-0065
type: implementation
status: draft
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0014, DECISION-0012]
relates_to: [SPEC-0033, SPEC-0041]
---

> Mini-spec del FOLLOW-UP de higiene rastreado desde Capa A / D2.1: el prune poda claims/tasks/mailbox
> pero NO condensa `next_actions`. Fix de raiz, aditivo, paridad py/.ps1. No cambia umbrales de poda
> (DECISION-0014) ni el comportamiento existente del prune. NO requiere DECISION nueva. Cambio
> incompatible => blocked + pregunta.

# SPEC-0051 - Prune condensa next_actions de PROJECT_STATE

## 1. Problema

`scripts/prune_state.py:prune_project_state` (~110) solo poda `active_tasks` (conserva los `done` mas
recientes). El arreglo `PROJECT_STATE.json#next_actions` crece sin limite (hoy 27 entradas; el snapshot
historico previo se condenso A MANO en una entrada "[HISTORICO PODADO]"). Esto infla el cold-start
(presupuesto de tokens, DECISION-0014) y obliga a poda manual. El prune debe condensar `next_actions`
automaticamente, igual que ya hace con tasks/mailbox.

## 2. Diagnostico (a confirmar en codigo por Codex, owner de scripts)

- `prune_project_state` no toca `next_actions`. No hay umbral de retencion para esa lista.
- La condensacion manual existente usa una entrada centinela "[HISTORICO PODADO] N entradas ... removidas
  ... trazabilidad en git history + memoria". El fix debe reproducir ese patron de forma determinista.

## 3. Alcance (fix de raiz, aditivo, paridad py/.ps1)

1. **Umbral de retencion configurable** para `next_actions` en `protocol.config.json#maintenance`
   (p.ej. `recent_next_actions`, default conservador), analogo a `recent_done_tasks` /
   `mailbox_keep_recent`. Ausente/0 => comportamiento actual (no condensa) para no romper instancias.
2. **Condensar al podar:** cuando `len(next_actions) > umbral`, conservar las N mas recientes y reemplazar
   el resto por UNA entrada centinela determinista que registre cuantas se removieron y donde queda la
   traza (git history + memoria). Idempotente: una segunda corrida no re-condensa lo ya condensado ni
   duplica el centinela.
3. **Preservar entradas centinela** previas (no las cuenta como podables ni las borra).
4. **Paridad** en `scripts/prune_state.ps1` (mismo comportamiento; atestiguada por Codex/CI).

## 4. Tests (golden determinista, sin red)

1. `next_actions` por encima del umbral -> prune condensa: quedan N recientes + 1 centinela con el conteo
   correcto; validador verde.
2. `next_actions` por debajo del umbral -> sin cambios.
3. Segunda corrida -> idempotente (no re-condensa, no duplica centinela).
4. Umbral ausente/0 -> comportamiento actual intacto (regresion).
5. Resto del prune (claims/tasks/mailbox, umbrales DECISION-0014) intacto.

## 5. Fuera de alcance

- Umbrales y logica de claims/tasks/mailbox (DECISION-0014/SPEC-0041): sin cambios.
- Semantica del contenido de las next_actions (no se reescribe el texto, solo se condensa la lista).
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer

- MINOR (correccion de higiene aditiva; config-gated; no cambia contrato ni umbrales existentes).
