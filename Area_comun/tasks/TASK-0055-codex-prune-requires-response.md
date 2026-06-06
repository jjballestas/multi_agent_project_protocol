---
id: TASK-0055
owner: Codex
status: in_progress
type: implementation
priority: normal
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: []
relates_to: [TASK-0035, TASK-0034]
phase: P2
spec_id: Area_comun/specs/SPEC-0041-prune-requires-response.md
linked_decisions: [DECISION-0014, DECISION-0012]
execution_pipeline: [diagnosticar en scripts/prune_state.py la causa exacta por la que un mensaje requires_response puede acabar en archived/ con un status que el validador marca como mismatch; (1) que el prune EXIMA del archivado a mensajes con requires_response:true cuya respuesta no esta resuelta (sin respuesta enlazada / sin status de cierre) -> los deja donde estan; (2) que todo mensaje que el prune mueva a archived/ quede con status:archived garantizado (robusto al formato/encoding del frontmatter) -> nunca un mismatch status<->carpeta; aplicar la misma logica en scripts/prune_state.ps1 (paridad); crear golden determinista de prune con los casos del test plan]
acceptance_criteria: [un mensaje requires_response:true sin resolver NO es archivado por el prune (se exime); un mensaje requires_response resuelto que el prune archiva queda con status:archived (0 mismatch status<->carpeta en el validador); una 2da corrida de prune no reintroduce mismatches (idempotente respecto del gate); el resto del comportamiento del prune -claims/tasks/umbrales DECISION-0014- queda intacto; paridad py/.ps1; aditivo; sin red; sin secretos; neutralidad de dominio limpia]
test_plan: [golden determinista de prune (sin red): (1) requires_response:true sin resolver -> prune NO lo archiva -> validador verde; (2) requires_response resuelto -> prune lo archiva con status:archived -> validador verde (0 mismatch); (3) 2da corrida de prune -> no reintroduce mismatches; (4) regresion: claims/tasks/umbrales del prune intactos; validador/encoding/neutralidad py + paridad ps1 verdes; suite runtime sin regresion]
closure_criteria: [scripts/prune_state.py corregido de raiz (exime requires_response sin resolver + reconcilia status:archived al mover); paridad en scripts/prune_state.ps1; golden de prune verde con los 4 casos; validador/encoding/neutralidad py verdes (+ paridad ps1 atestiguada); el prune ya no puede dejar un mismatch status<->carpeta ni archivar conversaciones abiertas; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0055 - Prune robusto ante mensajes que requieren respuesta

> `implementation` -> SDD. Fix de raiz de un FOLLOW-UP de higiene rastreado desde el cierre de Capa A.
> Aditivo, paridad py/.ps1, no cambia umbrales (DECISION-0014). Ver SPEC-0041. NO requiere DECISION nueva.

## Contexto (el FOLLOW-UP)

Al cerrar Capa A aparecio un mensaje en `Area_comun/mailbox/archived/` cuyo `status` el validador
(`validate_collaboration_state.py`, gate status<->carpeta de TASK-0035) marca como **ERROR** (mismatch),
y hubo que corregirlo a mano (MSG-capaA-completa). La raiz: el prune (`scripts/prune_state.py`,
`prune_mailbox`) no reconcilia correctamente el ciclo de vida de los mensajes que aun **requieren
respuesta**. Debe arreglarse de raiz para que el prune nunca deje un mismatch ni archive una conversacion
logicamente abierta.

## Alcance

1. **No archivar lo abierto:** el prune EXIME del archivado a mensajes `requires_response: true` cuya
   respuesta no esta resuelta (sin respuesta enlazada / sin status de cierre).
2. **Reconciliar al archivar:** todo mensaje que el prune mueva a `archived/` queda con `status: archived`
   garantizado (robusto al formato/encoding del frontmatter) -> nunca un mismatch status<->carpeta.
3. **Paridad** en `scripts/prune_state.ps1`.
4. **Golden determinista** de prune con los 4 casos del test plan.

## Restricciones

- **Aditivo**; no cambiar umbrales de poda ni el archivado de claims/tasks (DECISION-0014).
- **Paridad py/.ps1**; **sin red**; sin secretos; **neutralidad de dominio** limpia.
- Fuera de alcance: Fase 5 (TASK-0054), runtime de guardrails. Cambio incompatible => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico**: claim liberado al pasar a `in_review` (DECISION-0018).

## Nota

Tarea de higiene independiente de Fase 5. La siguiente rebanada de Fase 5 (5.2 tool-policy deny-by-default)
la especifico y encolo aparte el arquitecto; no arrancarla aqui.
