---
id: TASK-0113
owner: Codex
status: ready
type: implementation
priority: high
created_at: 2026-06-14
updated_at: 2026-06-14
depends_on: []
relates_to: [TASK-0111, DECISION-0029]
phase: P2
spec_id: SPEC-0080
linked_decisions: [DECISION-0029]
deliverables:
  - runtime/eventlog.py (event_without_chain_fields excluye event_auth)
  - examples (golden NUEVO chain+auth+cost juntos)
relevant_files:
  - runtime/eventlog.py
  - runtime/protocol_replay.py
  - examples/runtime_event_auth_cases
  - examples/chain_cases
blocked_by_questions: []
objective: Corregir el bug PRE-EXISTENTE de la maquinaria #4 (DECISION-0029) hallado por la review de seguridad de Codex sobre TASK-0111 y reproducido por el architect: con event_state.chain_enabled=true Y event_auth.enabled=true a la vez, append_event calcula prev_hash ANTES de sign_event (hashea sin event_auth) mientras validate_chain recalcula sobre el evento firmado (event_without_chain_fields no excluye event_auth) => cadena invalidada falsamente.
expected_output: (1) event_without_chain_fields excluye tambien event_auth (ademas de prev_hash y deduped) -> append y validate hashean el MISMO payload; la firma sigue cubriendo prev_hash; chain-solo y auth-solo byte-equivalentes. (2) Golden NUEVO que active event_auth.enabled=true + event_state.chain_enabled=true + metrics.cost_attribution_enabled=true JUNTOS, emita un cost.attributed y eventos normales, y verifique verify_event_auth + validate_chain(valid:true) + protocol_state_drift(has_drift=false); caso negativo: tampering detectado. (3) Sin regresion: chain 10/10, event_auth 5/5, cost-attribution, eventlog, intent_flow, enforce.
question_to_resolve: Ninguna abierta. SPEC-0080 fija el contrato. Fix verificado por el architect (parche -> MATCH=True). maker=Codex, checker=Claude.
maker_checker: Codex implementa (lo hallo en su review; runtime impl es su carril); Claude revisa (maker != checker). Decision del operador 2026-06-14.
closure_criterion: parche + golden chain+auth+cost juntos verde (positivo + tampering negativo) + sin regresion + gates verdes (drift 0); revision del architect; TASK-0113 en done. NO bloquea la activacion de cost-attribution (que mantiene chain/auth OFF); cierra antes de activar chain+auth juntos.
sdd_required: true
---

# TASK-0113 - Fix chain+auth: prev_hash/sign ordering (DECISION-0029 / SPEC-0080)

> Bug pre-existente de #4, hallado por Codex (review TASK-0111) y reproducido por el architect. Codex
> implementa, Claude revisa (decision del operador). Fix verificado: opcion (b) en SPEC-0080. NO bloquea
> el piloto de cost-attribution (chain/auth siguen OFF); cierra antes de cualquier activacion de
> chain+auth juntos.
