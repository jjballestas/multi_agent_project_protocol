---
id: TASK-0111
owner: Claude
status: in_progress
type: implementation
priority: high
created_at: 2026-06-14
updated_at: 2026-06-14
depends_on: []
relates_to: [TASK-0113, DECISION-0033, DECISION-0022, DECISION-0028, DECISION-0030, DECISION-0009, DECISION-0024]
phase: P2
spec_id: SPEC-0079
linked_decisions: [DECISION-0033]
deliverables:
  - runtime/eventlog.py (cost_attribution_enabled + EventWriter.append_cost_attribution, applied:false)
  - runtime/budget.py (cost_attribution_record + cost_attribution_idempotency_key + attribute_cost)
  - runtime/metrics.py (summarize_cost_attribution: by_handoff/by_decision/by_agent)
  - protocol.config.json + protocol.config.template.json (metrics.cost_attribution_enabled, off-by-default)
  - examples/runtime_cost_attribution_cases/ (golden GC-1..GC-6)
  - .github/workflows/validate.yml (linea CI del golden)
relevant_files:
  - runtime/eventlog.py
  - runtime/budget.py
  - runtime/metrics.py
  - runtime/protocol_replay.py
  - protocol.config.json
  - protocol.config.template.json
blocked_by_questions: []
objective: Imputacion de coste de tokens POR handoff/decision/agente (las tres dimensiones), construida sobre el event log, off-by-default, esquema de DOS PLANOS (plano de protocolo sin texto libre; carga util por hash). Instrumentacion de medicion VIVA antes del piloto del loop, para capturar en caliente y no retrofitar.
expected_output: (1) Evento cost.attributed con applied:false (anotacion no-mutadora; replay de estado lo omite => sin drift; no pasa por submit_intent). (2) Flag metrics.cost_attribution_enabled (ausente=>false); template false, vivo se activa SOLO en el paso de activacion (GO del operador). (3) Constructor sin texto libre (subject por canonical_hash). (4) summarize_cost_attribution: by_handoff (cada handoff separado, sin agregacion cruzada), by_decision (por decision_id), by_agent (suma por actor). (5) Golden: handoff simple / varios handoffs sin agregacion cruzada / por decision / off-by-default byte-equivalente / drift no-afectado. (6) Sin regresion en intent_flow ni en el hard-gate (enforce: enforced=True, has_drift=False).
question_to_resolve: Ninguna abierta. SPEC-0079 fija contrato y barra; DECISION-0033 ratificada por el operador.
maker_checker: |
  El architect (Claude) construyo la implementacion (de-risking aceptado por el operador). La REVISION la
  hace CODEX (maker != checker real, no sello): Codex revisa el codigo y confirma EN CONCRETO que
  cost.attributed (applied:false, emitido fuera de submit_intent) NO permite (a) eludir enforce / el
  hard-gate B.3 de drift, (b) eludir event-auth cuando este on, ni (c) inyectar eventos de coste
  forjados que deriven autoridad. Codex, como implementer, atestigua avanzando el hop
  in_progress->in_review (su capability). El cierre in_review->done (reviewer=Claude) ocurre en la
  ACTIVACION post-GO, junto con: hot verification (imputacion en evento real + drift 0 + replay==hot),
  flip del flag a true, SemVer MINOR 1.6.0 + CHANGELOG.
closure_criterion: golden verde + sin regresion (intent_flow + hard-gate) + revision de Codex pasada + verificacion EN CALIENTE (drift 0, replay==hot) + activacion (flag true + MINOR 1.6.0 + CHANGELOG) bajo GO del operador; handoff autocontenido; TASK-0111 en done.
sdd_required: true
---

# TASK-0111 - Cost-attribution por handoff/decision/agente (DECISION-0033 / SPEC-0079)

> Diseño RATIFICADO por el operador (2026-06-14). Implementacion del architect aceptada como de-risking.
> Aterriza DORMIDA (flag off-by-default; sin bump de version). La ACTIVACION (flag true + MINOR 1.6.0 +
> CHANGELOG + hot verification + cierre) espera GO explicito del operador. Escritor unico: toda mutacion
> de estado por submit_intent. enforce/authoritative intactos; subagents_enabled false; SA.4 sin disparar.

## Endurecimiento aplicado (analista pasada-3, 2026-06-14)

Esquema fijado ANTES de cualquier emision en caliente (log inmutable): subject canonico por dimension
(`{handoff_id}`/`{decision_id}`/`{agent_id}`); `cost_tokens` = total del productor (input+output); tags
`cost_unit`/`cost_schema` (summarizer rechaza filas sin ellos); `subject_hash` reetiquetado SEUDONIMO;
`actor` restringido a vocabulario de agentes. Golden 10/10. Review del analista cerrada.

## Relacion con TASK-0113 (chain+auth)

La review de Codex hallo un bug LATENTE de #4 (chain+auth: `event_without_chain_fields` no excluye
`event_auth`) => TASK-0113 (Codex implementa, Claude revisa). NO bloquea la activacion de cost-attribution:
la activacion mantiene `chain_enabled`/`event_auth.enabled` OFF, asi que el bug no se dispara; TASK-0113
cierra antes de activar chain+auth juntos. Codex re-revisa el codigo endurecido para su hop in_review.

## Pendiente para Codex (revision de seguridad concreta)
1. cost.attributed es applied:false => `protocol_replay.replay_protocol_state` lo omite (no muta
   task/claim/decision, no produce ni oculta drift). Confirmar que no hay ruta de mutacion de estado.
2. Emitido por `EventWriter.append_cost_attribution` (fuera de submit_intent), pero via `append_event`
   => respeta `sign_event` (event-auth) y el encadenado (`chain_enabled`). Confirmar que con event-auth
   on, un cost.attributed sin firma valida se rechaza en replay; con chain on, una insercion se detecta.
3. Ninguna decision de autoridad (capacidad/scope/autor/escalado) se deriva del contenido de
   cost.attributed: la metrica es informativa. Confirmar que un evento de coste forjado solo corrompe
   metricas, nunca estado ni autoridad.
