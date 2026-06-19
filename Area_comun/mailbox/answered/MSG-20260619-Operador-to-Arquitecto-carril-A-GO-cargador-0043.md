---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-cargador-0043
type: DECISION
task_id: TASK-0117
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
answered_by: MSG-20260619-Arquitecto-to-Operador-carril-A-integridad-y-secuencia
one_line_summary: GO al diseno del cargador (DECISION-0043 + SPEC-0082, ratificado). Pasada de Codex sobre el DRAFT ANTES de promover; anchor = repo nuevo dedicado e independiente; PRECONDICION DURA = recuperar integridad del working tree (3 archivos truncados) antes de re-genesis/provisioning/piloto. #4 sigue OFF.
requested_action: (a) Ratificar y promover DECISION-0043 + SPEC-0082 + TASK-0120 por submit_intent (MINOR + CHANGELOG, #4 OFF) SOLO despues de (b). (b) Correr la pasada de factibilidad de Codex sobre el DRAFT antes de promover; Analista honestidad: omitir salvo que Codex levante algo. (c) Cerrar la recuperacion de integridad del working tree ANTES del re-genesis/provisioning/piloto.
question: Confirmas la secuencia integridad -> pasada Codex -> promover -> implementar -> provisioning (anchor nuevo dedicado) -> piloto, con #4 OFF hasta el piloto?
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0043-event-auth-secret-resolution.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0082-event-auth-secret-resolution.md
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
validation_refs:
  - "git show HEAD vs working tree: scripts/validate_collaboration_state.py 983->960 (no compila); runtime/submit_intent.py 1053->1031 (no compila); runtime/state/events.jsonl 587->538 (-49 eventos)"
deadline_or_blocking_level: blocking
---

# GO al cargador (DECISION-0043 / SPEC-0082) con precondicion de integridad

Diseno revisado y verificado contra codigo. Va. Detalle por punto:

## (a) Diseno: ratificado
DECISION-0043 + SPEC-0082 son el alcance minimo correcto. Verificado: Ed25519 ya es wrapper-side
(`llm_turn_wrapper.py:sign_turn_report` lee el PEM externo), el unico secreto runtime es el HMAC de
`event_auth`, `read_protocol_config` lee directo sin overlay/env, y AC5 fija la propiedad clave
(dos secretos distintos -> firmas distintas, `signable_event`/`prev_hash` identicos). Fail-closed (AC3),
gate de no-literal-commiteado (AC4) y path-safety (AC6) cubren la frontera no-secretos. Promueve por
submit_intent: MINOR + CHANGELOG, **#4 sigue OFF**.

## (b) Pasada de Codex ANTES de promover
Toca la ruta de firma: corre la pasada de factibilidad de Codex sobre el DRAFT antes de meterlo al
ledger (seguro barato, mantiene maker!=checker: tu eres autor del diseno, Codex revisor del draft; se
invierten para implementar/revisar TASK-0120). Analista honestidad: omitir salvo que Codex levante algo.

## (c) Anchor remote
Creo uno **nuevo dedicado**, append-only, dominio de confianza independiente del repo principal, rama
`audits/default`. Reusar solo valdria si fuera remote/cuenta realmente separado; un repo nuevo es mas
limpio. Te paso el `anchor_config.remote_url` cuando lo tenga (no bloquea (a)/(b)).

## PRECONDICION DURA (no estaba en tu reporte)
El working tree vivo tiene 3 archivos **truncados** vs HEAD (ver validation_refs), incluido el event log
autoritativo (-49 eventos) y el propio gate AC6 (`validate_collaboration_state.py`, no compila). El
**re-genesis del paso 5 NO puede correr sobre el arbol truncado**: se anclaria estado corrupto. Antes de
re-genesis/provisioning/piloto: restaurar los 3 desde HEAD (son truncamientos puros; HEAD compila y esta
completo), verificar `py_compile` + `validate_collaboration_state --root .` verde + replay==hot + drift 0.
La implementacion de TASK-0120 puede arrancar en paralelo (HEAD esta limpio).

## Limites
#4 OFF hasta el piloto (chain/agent_signatures/anchor/event_auth). Sin SA.4 / Capa C / subagents.
TASK-0118 (DEF-PII) sigue diferida. Codex y los crons activos. Canal ASCII.
