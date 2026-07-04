---
task_id: TASK-0252
title: "[VISION-NOVA] Cablea el harness de paridad exec-vs-endpoint al sandbox (rol budget_sandbox_verifier)"
type: feature
status: in_review
owner: Codex
phase: P2
priority: low
created_at: 2026-07-04
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0091, DECISION-0078]
linked_decisions: [DECISION-0091, DECISION-0078]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md
intake:
  type: feature
  goal: Cablear el harness de paridad (exec-vs-endpoint) a la cadena de conexion del sandbox DbsFinanciero_SANDBOX usando el rol budget_sandbox_verifier (GRANT EXECUTE definido y ejecutado por el Operador), reemplazando al conector readonly nova_sql_connector_readonly_s9 para las pruebas que requieren EXECUTE real (no solo verificacion de existencia, F-NOVA-01).
  acceptance:
    - Harness usa el rol budget_sandbox_verifier contra DbsFinanciero_SANDBOX (NUNCA produccion) para paridad exec-vs-endpoint.
    - Columna del schema paridad_exec_vs_endpoint (pass/fail/NA) se puebla correctamente segun el resultado real de ejecutar el proc vs invocar el endpoint.
    - El harness RESETEA el sandbox a la linea base sellada ENTRE corridas (evita contaminacion cruzada de brazos, procs de la superficie mutan el sandbox).
    - Relay al Operador/DBA del hardening recomendado (guard IF DB_NAME() NOT LIKE '%SANDBOX%' THROW en el script SQL fuente, fuera del hub) -- no es codigo de esta tarea, es una recomendacion a transmitir.
    - Annul_Availability_Certificate/Annul_Commitment NO se incluyen (brechas B-04, PAR-2 sigue diferido); si el script fuente los agrega antes de que existan, la tarea debe senalarlo como anomalia, no silenciarlo.
  verification_cmd:
    - dotnet test NOVA.sln
  scope_routes:
    - (repo producto Nova-Budget, harness de integracion, fuera del hub)
  out_of_scope:
    - NO ejecuta el GRANT EXECUTE (ya lo ejecuta el Operador de su parte, fuera del hub).
    - NO agrega Annul_* a la superficie (brechas B-04, enmienda fechada cuando existan).
    - NO toca el conector readonly_s9 (sigue sirviendo para verificacion de existencia, F-NOVA-01, en unidades no-mutadoras).
  risk: medium
  estimate: S
---

# TASK-0252 - Harness de paridad exec-vs-endpoint (rol budget_sandbox_verifier)

Owner: Codex (implementa) + Analista (gate formal) + Arquitecto (checker de alcance/neutralidad).

## Contexto (DIRECTIVA operador grant-sandbox-rol-paridad-harness)
El Operador definio y ejecuta de su parte el GRANT EXECUTE del estudio (rol `budget_sandbox_verifier`,
15 procs + 89 vistas + 1 dependencia cross-schema, superficie identica baseline/gobernado). Esta tarea
cablea el HARNESS de Codex para usar ese rol en las pruebas de paridad (exec-vs-endpoint) de las unidades
mutadoras (P4.x), reemplazando al conector readonly solo para ESE proposito.

## Prioridad
**Por debajo del fix-loop de F3.3** (TASK-0249, ya cerrado) y de la apertura del dev medido P2.1/P2.2
(TASK-0250/0251, read-only, NO requieren este harness). Es prep para cuando abra el dev medido de las
unidades mutadoras P4.x. NO se GO-ea todavia; queda `proposed` en cola.

## DoD (testable)
Ver bloque intake (acceptance). Gate FORMAL del Analista (infra gobernada) + gates del hub verdes.
