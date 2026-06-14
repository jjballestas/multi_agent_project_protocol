---
spec_id: SPEC-0080-fix-chain-auth-prev-hash
task_id: TASK-0113
type: implementation
status: ready
linked_decisions:
  - DECISION-0029
created_at: 2026-06-14
updated_at: 2026-06-14
author: Claude (architect)
---

# SPEC-0080 - Fix chain+auth: prev_hash/sign ordering en el event log

## Context

Bug PRE-EXISTENTE y LATENTE de la maquinaria #4 (encadenado + firma de eventos, DECISION-0029),
hallado por la revision de seguridad de Codex sobre TASK-0111 (cost-attribution) y reproducido
independientemente por el architect. Con `event_state.chain_enabled=true` Y `event_auth.enabled=true`
a la vez, la cadena se invalida falsamente:

- `EventWriter.append_event` calcula `prev_hash` ANTES de `sign_event`, asi que hashea el evento SIN
  `event_auth` (la firma se anade despues).
- `validate_chain` (protocol_replay.py) recalcula con `compute_event_prev_hash` sobre el evento
  ALMACENADO (ya firmado), y `event_without_chain_fields` NO excluye `event_auth`, asi que hashea CON
  `event_auth`.
- Resultado: `prev_hash` de append != `prev_hash` de validate => "corruption at seq" falso.

Reproduccion (architect): append_prev_hash=3f6abedb..., validate_prev_hash=c1fc6998... (MATCH=False).
Afecta a TODOS los eventos bajo ambos flags; `cost.attributed` solo lo expuso. CERO exposicion viva:
chain y auth estan off-by-default. La raiz: ningun golden ejercita ambos flags JUNTOS (chain 10/10 y
event_auth 5/5 corren por separado).

## Scope

- `runtime/eventlog.py::event_without_chain_fields`: excluir tambien `event_auth` (ademas de
  `prev_hash` y `deduped`), para que append y validate hasheen el MISMO payload canonico.
- Golden NUEVO que ejercita `chain_enabled=true` + `event_auth.enabled=true` JUNTOS y verifica que
  `validate_chain` reporta `valid:true` (la cobertura que faltaba). Caso negativo: tampering de un
  evento firmado sigue detectandose.

## Out Of Scope

cost-attribution (TASK-0111, que esta bloqueada por esta), activacion de flags, cualquier otro cambio
de maquinaria. No tocar `enforce`/`authoritative`.

## execution_pipeline

1. En `event_without_chain_fields` anadir `payload.pop("event_auth", None)`.
2. Anadir golden (p.ej. en `examples/chain_cases/` o `examples/runtime_event_auth_cases/`, o un nuevo
   `examples/chain_auth_combined_cases/`) que: active `event_auth.enabled=true` +
   `event_state.chain_enabled=true` + `metrics.cost_attribution_enabled=true` JUNTOS, escriba >=2
   eventos via `append_event` INCLUYENDO un `cost.attributed`, y afirme `validate_chain(...).valid is
   True` + `verify_event_auth` OK + `protocol_state_drift(has_drift=false)` (regresion pedida
   explicitamente por Codex en su blocker). Caso negativo: mutar un evento => `validate_chain` detecta
   corrupcion.
3. Correr regresion: chain 10/10, event_auth 5/5, cost-attribution 6/6, eventlog, intent_flow, enforce.

## acceptance_criteria

- Con chain+auth ambos on, `append_event` y `validate_chain` computan el MISMO `prev_hash`
  (verificado: el parche hace MATCH=True).
- La firma sigue cubriendo `prev_hash` (la firma atesta la posicion en la cadena): `sign_event` firma
  `signable_event`, que conserva `prev_hash`; el orden de append no cambia, solo el conjunto de campos
  hasheados por la cadena.
- chain-solo y auth-solo quedan byte-equivalentes (sin event_auth presente, el pop es no-op).
- Golden chain+auth-juntos verde (positivo + negativo de tampering).
- Sin regresion: chain 10/10, event_auth 5/5, cost-attribution 6/6, eventlog, intent_flow, enforce.

## linked_decisions

- `DECISION-0029`: la maquinaria de procedencia (prev_hash + firma) cuyo invariante este fix restaura.

## test_plan

- Nuevo golden chain+auth-juntos (positivo + tampering negativo).
- Reruns: `examples/chain_cases`, `examples/runtime_event_auth_cases`,
  `examples/runtime_cost_attribution_cases`, `examples/runtime_eventlog_cases`,
  `examples/intent_flow_cases`, `examples/runtime_protocol_enforce_cases`.
- Gates: validador/encoding/neutralidad. Drift 0.

## closure_criteria

- Parche aplicado + golden chain+auth-juntos verde + sin regresion + gates verdes; revision del
  architect (Claude); TASK-0113 en done. Al cerrar, desbloquea TASK-0111.

## Risks

- **Riesgo:** la firma deja de cubrir la cadena. **Mitigacion:** la firma cubre `prev_hash` (no al
  reves); el fix solo saca `event_auth` del conjunto hasheado por la cadena, no cambia que la firma
  incluya `prev_hash`. Verificar en el golden que tampering del evento sigue detectado.
- **Riesgo:** version. Bug fix en maquinaria dormida => PATCH; sin bump hasta que se decida (puede
  plegarse al 1.6.0 de la activacion de #3, o 1.5.1). Decision al cierre.

## Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| append==validate prev_hash con chain+auth | TASK-0113 | golden chain+auth-juntos (positivo) | validate_chain valid:true |
| firma cubre prev_hash; tampering detectado | TASK-0113 | golden (negativo) | corrupcion detectada |
| sin regresion chain/auth/cost/eventlog | TASK-0113 | reruns | suites verdes |
