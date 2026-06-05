---
spec_id: SPEC-0026-contrato-de-turno
task_id: TASK-0027
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0026 — Contrato de turno (turn report)

## Contexto
DECISION-0009 §4: la pieza clave del runtime es el **contrato de turno**: lo que un agente devuelve
tras UN turno para que el orquestador aplique transiciones de forma **determinista y segura**. El
esquema vive en `runtime/turn_schema.json` (entregado por TASK-0026/M0). Ver
[DISENO-runtime-orquestacion-automatizada.md](../artifacts/DISENO-runtime-orquestacion-automatizada.md) §4.

## Alcance
- Validación del *turn report* contra `runtime/turn_schema.json`.
- Aplicación de transiciones por el orquestador (task_status, claims, mailbox, handoff).
- Invariante de seguridad **write-allowlist**: `changed_paths ⊆ scope del claim activo del agente`.
- Golden cases en `examples/runtime_turn_cases/` (válidos + inválidos).

## No-alcance
- No implementa el router (SPEC-0027) ni los adapters. No invoca agentes reales (eso es M1+).

## execution_pipeline
1. Cargar y validar el report contra `turn_schema.json` (draft-07, estricto). Report inválido ⇒
   turno rechazado, sin aplicar nada.
2. Verificar `agent` == owner del claim activo; y **cada** `changed_paths[i]` cubierto por el scope
   del claim (si no ⇒ rechazo: escritura fuera de allowlist).
3. Verificar `transitions.task_status.from` == estado actual de la tarea (detección de carrera);
   `claims`/`mailbox` aplicables (acquire de ruta no reclamada por otro; release del propio).
4. Aplicar transiciones de forma atómica; correr **gate** (`validate_collaboration_state` + scan de
   neutralidad). Verde ⇒ commit (1 turno = 1 commit, mensaje = `commit_message`). Rojo ⇒ `git revert`
   + tarea a `blocked` + escalar.
5. Si `outcome ∈ {decision_required, human_required}` o `gate.human_required` ⇒ **parar el loop** y
   escalar al humano (no autocontinuar).
6. Golden cases: report válido aplicado; report con `changed_paths` fuera de claim ⇒ rechazo; report
   con `from` desfasado ⇒ rechazo; report `human_required` ⇒ parada.

## acceptance_criteria
- Report válido pasa el esquema y se aplica; inválido se rechaza sin tocar estado.
- `changed_paths` fuera del scope del claim ⇒ turno rechazado (write-allowlist).
- `task_status.from` que no casa con el estado actual ⇒ rechazo (anti-carrera).
- `decision_required`/`human_required` ⇒ el orquestador para y escala.
- Tras aplicar, el gate corre y decide commit vs revert.

## linked_decisions
- `DECISION-0009` (runtime, §4 contrato); `DECISION-0007` (claim como lock / write-allowlist);
  `DECISION-0001` (aditivo, off-by-default ⇒ MINOR).

## test_plan
- Validar `turn_schema.json` con un validador JSON Schema (draft-07) sobre los golden reports.
- Golden cases en `examples/runtime_turn_cases/`: `valid_in_review`, `out_of_allowlist`,
  `stale_from`, `human_required`.

## closure_criteria
- Esquema validado + golden (válidos/inválidos) pasan; write-allowlist y anti-carrera demostrados;
  gate+commit/revert documentado; revisión del arquitecto OK; claim liberado.

## Risks
- Un contrato laxo permitiría transiciones inseguras. Mitigación: esquema estricto
  (`additionalProperties:false`, enums) + write-allowlist + gate por turno detrás.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Report validado por esquema | TASK-0027 | golden válido/inválido | esquema estricto verde |
| Write-allowlist (changed_paths ⊆ claim) | TASK-0027 | golden out_of_allowlist | turno rechazado |
| Anti-carrera (from casa) | TASK-0027 | golden stale_from | turno rechazado |
| Parada humana | TASK-0027 | golden human_required | loop se detiene |
