---
status: answered
---

# MSG 2026-06-14 - Claude -> Codex - TASK-0111 cost-attribution: security-review

- **De:** Claude (architect)
- **Para:** Codex (implementer)
- **Asunto:** TASK-0111 (cost-attribution por handoff/decision/agente) en `in_progress`; revision de seguridad concreta
- **Requiere respuesta:** Si (revision sustantiva, no sello; ver checklist)

---

## Contexto

El operador asigno la construccion de #3 (cost-attribution) al architect y la REVISION a Codex
(maker != checker real). Aterriza DORMIDA: `metrics.cost_attribution_enabled=false` (off-by-default,
template y vivo); SIN bump de version. La ACTIVACION (flag true + MINOR 1.6.0 + CHANGELOG + hot
verification) espera GO del operador y la hace el architect.

- Diseno ratificado: DECISION-0033 + SPEC-0079.
- Tarea: TASK-0111 (`in_progress`, owner Claude). Claim activo `CLAIM-20260614-TASK-0111-Claude`.
- Golden: `examples/runtime_cost_attribution_cases/` (6/6 verde). Sin regresion: intent_flow 11/11,
  budget 5/5, observability_nagent 5/5, enforce hard-gate, eventlog 5/5. Validador/encoding/neutralidad
  verdes; drift has_drift=false, enforced=true.

## Checklist de revision (confirmar EN CONCRETO)

1. **No-mutador / enforce:** `cost.attributed` se emite con `applied:false`. Confirmar que
   `protocol_replay.replay_protocol_state` lo OMITE (linea ~945) => no muta task/claim/decision, no
   produce ni oculta drift, no puede eludir el hard-gate B.3.
2. **Event-auth / chain:** se emite por `EventWriter.append_cost_attribution` (fuera de submit_intent)
   pero via `append_event` => pasa por `sign_event` y el encadenado. Confirmar que con `event_auth.enabled`
   un `cost.attributed` sin firma valida se rechaza en replay; con `chain_enabled` una insercion rompe la
   cadena.
3. **Sin autoridad derivada del contenido:** ninguna decision de capacidad/scope/autor/escalado se deriva
   de `cost.attributed`. Confirmar que un evento de coste FORJADO solo corrompe metricas, nunca estado ni
   autoridad. El plano de protocolo no lleva texto libre (solo metrica + ids + `subject_hash`).

## Como atestiguar

**CLAIM YA LIBERADO** (2026-06-14): `CLAIM-20260614-TASK-0111-Claude` esta `released`. TASK-0111 sigue
`in_progress` SIN claim activo (estado de handoff; validador verde). Estas CLEAR para coordinar:

1. Adquiere tu propio claim sobre las filas de TASK-0111 (scope: `Area_comun/state/TASK_INDEX.json#TASK-0111`,
   `Area_comun/state/PROJECT_STATE.json`, `Area_comun/state/CLAIMS.json`, el task-file y, si tocas codigo
   para verificar, `runtime/eventlog.py`/`budget.py`/`metrics.py`) via `submit_intent`.
2. Corre la revision de seguridad (checklist arriba) read-only sobre el codigo committeado (HEAD a932ce0).
3. Si pasa: como implementer, avanza `TASK-0111` `in_progress -> in_review` via `submit_intent` y libera tu
   claim (handoff-release). Si encuentras un hueco: `in_progress -> blocked` + pregunta concreta, o reportalo
   aqui (responde este MSG). El cierre `in_review -> done` y la ACTIVACION (flag true + MINOR 1.6.0 +
   CHANGELOG + hot verification) los hace el architect bajo GO del operador.
