---
task_id: TASK-0251
title: "[VISION-NOVA][P2.2] Reporte de ejecucion presupuestal (Get_Budget_Execution_Report) - dev BASELINE, miembro PAR-D anclado"
type: feature
status: proposed
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-04
reviewer: adversarial-informal-sesion-separada
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, DECISION-0091]
linked_decisions: [DECISION-0091]
linked_reqs: [GOAL-VISION-NOVA-001]
file: Area_comun/tasks/TASK-0251-p22-reporte-ejecucion-presupuestal.md
intake:
  type: feature
  goal: Implementar el reporte de ejecucion presupuestal (Get_Budget_Execution_Report) per SPEC-NOVA-P2-001, en Nova-Budget. Unidad BASELINE, miembro ANCLADO de PAR-D (spec_prepagado=true, fase SPEC excluida del delta).
  acceptance:
    - Cumple los criterios de aceptacion de SPEC-NOVA-P2-001 s.7 (falsables).
    - F-NOVA-01: objetos/proc RE-VERIFICADOS contra la BD desplegada antes de fijar el criterio.
    - Deuda GOAL-P1 (harness front apps/nova-web) verde en clon limpio ANTES de la UI de esta unidad.
    - checker_formal=0 (baseline); adversarial informal de 12 puntos en SESION SEPARADA.
    - cache-confound declarado o mismo runtime que su comparador (measurement, SPEC s.DoR).
  verification_cmd:
    - dotnet test NOVA.sln
    - npm test --prefix apps/nova-web
  scope_routes:
    - (repo producto Nova-Budget, fuera del hub)
  out_of_scope:
    - NO reimplementa el calculo del reporte en C# (usa el proc/gateway tipado, SPEC s.6).
    - NO abre hasta que F3.3 (TASK-0249, instrumentacion) este lista, o el Operador autorice captura manual de fallback.
  risk: low
  estimate: M
---

# TASK-0251 - [VISION-NOVA][P2.2] Reporte de ejecucion presupuestal (dev BASELINE, PAR-D anclado)

Owner: Codex (implementa, Nova-Budget) + adversarial informal en sesion separada (checker vivo del
baseline) + Arquitecto (checker de gates del hub / neutralidad).

## Contexto
Unidad P2.2, BASELINE, miembro ANCLADO de PAR-D (`spec_prepagado=true`; su fase SPEC ya se excluyo del
delta del estudio, `NOVA_ESTUDIO_Particion` s.2.1). SPEC completa:
`Area_comun/specs/nova/SPEC-NOVA-P2-001-budget-execution-report.md`. Preparada aqui (DIRECTIVA operador
cola-F3.3-lista-no-idle, item Q2); **NO se GO-ea todavia**: abre cuando F3.3 (TASK-0249) este lista, o
con captura manual (`medicion_ledger.py`) si el Operador decide no esperar.

## DoD (testable)
Ver bloque intake (acceptance) + SPEC s.7/s.8. Gate: adversarial informal de 12 puntos en sesion separada
(checker_formal=0, baseline) + gates del hub verdes + atestacion sha256 de la SPEC.
