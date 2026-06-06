---
message_id: MSG-20260606-Claude-to-Codex-task0047-ci
type: TASK_ASSIGNMENT
task_id: TASK-0047
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: Encolada TASK-0047 (Capa A.5, criterio 14 SPEC-0038): correr las suites de runtime en CI. Aditivo, solo .github/workflows, sin tocar runtime ni contrato. Arranque de la consolidacion del nucleo elegida por el operador.
requested_action: Implementar TASK-0047 cuando la tomes; claim antes de tocar .github/workflows/validate.yml.
question: none
context_refs:
  - Area_comun/tasks/TASK-0047-codex-runtime-suites-en-ci.md
  - Area_comun/artifacts/INVENTARIO-n-agente-cierre-nucleo-20260606.md
  - .github/workflows/validate.yml
---

# TASK-0047 (Capa A.5) encolada

Codex, el operador decidio consolidar el NUCLEO (Capa A) antes de la Fase 5. Arrancamos por el item de
bajo riesgo y alto valor de proteccion: **llevar las suites de runtime a CI**.

Hoy CI corre validador/encoding/neutralidad + golden de protocolo, pero NO los runners de runtime (router,
eventlog, review_qa, registry, turn schema/semantic, apply, loop, observability, llm-adapter). Esta tarea
los agrega al workflow.

Reglas: aditivo, **solo `.github/workflows/validate.yml`**; no toques `runtime/` ni el contrato ni los
fixtures; determinismo (sin red, sin reloj real); `llm_adapter_cases` en modo recorded (SIN
--allow-real-invoker). Declara dependencias del job si hacen falta (p.ej. jsonschema). Detalle SDD en el
task-file.

Cierre: CI verde con las suites incluidas + resto de gates intactos; handoff autocontenido con los steps
exactos; claim liberado al pasar a in_review.

NOTA: el item delicado de la Capa A (event log como writer vivo, A.1) lo especifico yo aparte (spec/posible
DECISION). NO lo arranques; tampoco la Fase 5. Tu cola es TASK-0047.
