---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0217
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0217
status: open
requires_response: false
---

# GO - TASK-0217 (Zeus-Aegis: Backlog 0 vs Dashboard Tasks>0)

Codex: arranca **TASK-0217** (maker). Spec autocontenido en
`Area_comun/tasks/TASK-0217-codex-zeus-aegis-backlog-consistency.md`.

Bug reportado por el operador: Dashboard `Tasks 11` pero **Backlog 0** ("0 visible tasks"). Causa (diagnostico
checker) en `vendor/hermes-2.3.0/src/server/governance-readonly.ts`: `getGovernanceBacklog()` lee
`TASK_INDEX.slim.json` y `getGovernanceMetrics()` lee `TASK_INDEX.json` -> **fuentes distintas**, conteos no
cuadran y el Backlog puede salir 0. Fix: **unificar la fuente** canonica de tareas (backlog y dashboard del mismo
universo, o etiquetar la diferencia "backlog activo" vs "total") + asegurar que el view pinta lo recibido (revisar
el path resiliente de carga de TASK-0212). Conservar acordeones/filtros de TASK-0210. READ-ONLY.

Repo `D:/Agentes/Zeus/Zeus-Aegis`. AC1-AC3 en el spec. **Gate checker: RENDER HEADLESS + SCREENSHOT** que el
Backlog ya NO sale 0 con ready/proposed. `pnpm governance:smoke` PASS + f0-test verde. Commit como Arquitecto +
`Co-Authored-By: Codex`, entrega `in_review`. ETA corta-media.
