---
task_id: TASK-0250
title: "[VISION-NOVA][P2.1] Read model de parametros (rubros/fuentes/rubro-fuente/BPIN/series) - dev BASELINE"
type: feature
status: ready
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
file: Area_comun/tasks/TASK-0250-p21-read-model-parametros.md
intake:
  type: feature
  goal: Implementar el read model de parametros (rubros, fuentes, rubro-fuente, BPIN, series documentales) sobre las vistas vw_* existentes, per SPEC-NOVA-P2-002, en Nova-Budget. Unidad BASELINE, fuera del contraste (mandada por el GOAL).
  acceptance:
    - Cumple los criterios de aceptacion 1-N de SPEC-NOVA-P2-002 s.7 (falsables, paridad de conteo contra las vistas).
    - F-NOVA-01: cada objeto/vista RE-VERIFICADO contra la BD desplegada antes de fijar el criterio.
    - Deuda GOAL-P1 (harness front apps/nova-web) verde en clon limpio ANTES de la UI de esta unidad.
    - checker_formal=0 (baseline); adversarial informal de 12 puntos en SESION SEPARADA (dev != adversarial).
    - cache-confound declarado o mismo runtime que su comparador (measurement, SPEC s.DoR).
  verification_cmd:
    - dotnet test NOVA.sln
    - npm test --prefix apps/nova-web
  scope_routes:
    - (repo producto Nova-Budget, fuera del hub)
  out_of_scope:
    - NO mutaciones (es read-only); NO toca CRUD ni reimplementa logica de las vistas.
    - NO abre hasta que F3.3 (TASK-0249, instrumentacion) este lista, o el Operador autorice captura manual de fallback.
  risk: low
  estimate: M
---

# TASK-0250 - [VISION-NOVA][P2.1] Read model de parametros (dev BASELINE)

Owner: Codex (implementa, Nova-Budget) + adversarial informal en sesion separada (checker vivo del
baseline) + Arquitecto (checker de gates del hub / neutralidad).

## Contexto
Unidad P2.1, BASELINE, fuera del contraste A/B (mandada por el GOAL). SPEC completa:
`Area_comun/specs/nova/SPEC-NOVA-P2-002-parameters-read-model.md`. Preparada aqui (DIRECTIVA operador
cola-F3.3-lista-no-idle, item Q2 "coordina/prepara en paralelo"); **NO se GO-ea todavia**: abre cuando
F3.3 (TASK-0249) este lista para instrumentar el brazo, o con captura manual (`medicion_ledger.py`) si
el Operador decide no esperar.

## DoD (testable)
Ver bloque intake (acceptance) + SPEC s.7/s.8. Gate: adversarial informal de 12 puntos en sesion separada
(checker_formal=0, baseline) + gates del hub verdes + atestacion sha256 de la SPEC.
