---
id: TASK-0017
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0016]
relates_to: [TASK-0018]
phase: P2
spec_id: Area_comun/specs/SPEC-0017-ci-completo-scan-neutralidad.md
linked_decisions: [DECISION-0006, DECISION-0001]
execution_pipeline: [Extender validate.yml con validador .ps1 via pwsh, AÃ±adir harness SDD y compacto a CI, Implementar scan_domain_neutrality .py/.ps1 con denylist en protocol.config, Golden cases del scan, Verificar CI verde con ambos runtimes]
acceptance_criteria: [validate.yml ejecuta validate.ps1 (pwsh) + harness SDD + harness compacto + scan, scan falla ante tÃ©rmino de dominio en core/templates y pasa en repo actual, paridad scan .py/.ps1, denylist y rutas configurables en protocol.config, sin cambios de dominio en el core]
test_plan: [CI en ubuntu con setup-python + pwsh, golden cases del scan (positivo y negativo), dogfood + minimal_instance verdes en ambos validadores]
closure_criteria: [CI verde ejecutando todos los gates de AGENTS.md Â§5, scan integrado y con golden cases, handoff documenta gates aÃ±adidos, claim liberado]
---

# TASK-0017 â€” CI completo + scan de neutralidad de dominio

> `implementation` â†’ SDD obligatorio; implementar contra
> [SPEC-0017](../specs/SPEC-0017-ci-completo-scan-neutralidad.md) y DECISION-0006 Â§2â€“Â§3.
> `ready` (spec emitida por TASK-0016). Aditivo y neutral.

## Resumen
Cierra la grieta contratoâ†”CI: todo gate de `AGENTS.md` Â§5 corre en CI, incluido el scan de
neutralidad de dominio (hoy inexistente como script). Ver DECISION-0006 Â§2â€“Â§3.

## notas
- No tocar lÃ³gica de validaciÃ³n de estado; solo aÃ±adir cobertura de CI + el script de scan.


