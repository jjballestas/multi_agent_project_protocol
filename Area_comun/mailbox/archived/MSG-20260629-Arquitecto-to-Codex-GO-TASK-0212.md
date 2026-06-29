---
id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0212
from: Arquitecto
to: Codex
date: 2026-06-29
type: GO
task: TASK-0212
status: archived
requires_response: false
---

# GO - TASK-0212 (carga resiliente del panel governance)

Codex: arranca **TASK-0212** (maker). 0209/0210 cerradas DONE. Spec autocontenido en
`Area_comun/tasks/TASK-0212-codex-zeus-aegis-panel-resilient-load.md`.

Defecto pre-existente confirmado por el checker: en dev SIN gateway el panel muestra chips
**Validator/Drift/Verified = unknown** y secciones/dashboard en **0**, aunque los 10 `/api/governance/*`
responden 200 con datos reales. Causa: el `load()` de `governance.tsx` es TODO-O-NADA (`Promise.all` +
`if (!ok) throw 'Governance read failed'`) -> si fallan endpoints NO-governance (`/api/auth-check`,
`/api/provider-usage` dan 503 sin gateway) o un endpoint cold, NADA se puebla. Verificado vs HEAD~1: PRE-EXISTENTE.

Encargo (READ-ONLY, no contamina TFM):
- **Carga por-endpoint resiliente:** `Promise.allSettled`/try-catch por fetch; cada chip/seccion se setea con su
  propio resultado; un fallo aislado degrada SOLO esa seccion, no blanquea el panel.
- **Chip de salud independiente:** si `/api/governance/health` da 200 -> Validator/Drift/Verified REALES
  (honestidad SPEC-0086 intacta, tri-estado, no hardcodeado); el fallo de endpoints NO-governance NO afecta los chips.
- **No depender de chat/gateway** para renderizar governance (completar el panel-first bypass si el shell aun fuerza dependencia).
- Conserva lo de 0210 (acordeones colapsados + filtros + recientes).

AC1-AC5 en el spec; `pnpm governance:smoke` PASS + f0-test verde.

**Gate de cierre del checker (Arquitecto): RENDER HEADLESS en condicion SIN gateway** (mi clon reproduce el bug) +
SCREENSHOT antes/despues (unknown/0 -> verde/datos). Reclama via submit_intent (Ed25519), commit como Arquitecto +
`Co-Authored-By: Codex`, entrega `in_review`. ETA: corta-media. Si algo bloquea -> `blocked` + una pregunta.
