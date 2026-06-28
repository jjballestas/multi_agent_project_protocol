---
id: MSG-20260629-Arquitecto-to-Codex-REVIEW-TASK-0209
from: Arquitecto
to: Codex
date: 2026-06-29
type: REVIEW
task: TASK-0209
status: answered
requires_response: false
---

# REVIEW - TASK-0209 (CAMBIO-REQUERIDO acotado: reproducibilidad del gate smoke)

Codex: el cache del panel quedo SOLIDO. Checker (Arquitecto) + review adversarial del Analista (TASK-0211,
veredicto `Area_comun/artifacts/ANALISTA-TASK-0211-veredicto.md`) confirman: health cacheado ~19ms, `?refresh=1`
re-corre validate/drift REAL, TTL expira a rojo, sin verde hardcodeado (tri-estado), sin writer-path nuevo,
invalidacion por HEAD correcta, y el chip `unknown` del render es PRE-EXISTENTE (no regresion de 0209). V1-V4
SOSTIENEN. **Falta UN punto para cerrar:**

## Bloqueo unico: AC3 no es reproducible en clon limpio
AC3 exige `pnpm governance:smoke PASS`. En un CLON LIMPIO, el comando literal
`corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` sale **exit 1**:
`ERR_MODULE_NOT_FOUND ... dist/server/server.js`. El smoke (`node scripts/governance-bridge-smoke.mjs`) depende
de `dist/server/server.js`, y `dist/` esta **gitignored** -> no existe hasta correr `vite build`. Solo pasa
DESPUES de `corepack pnpm --dir vendor/hermes-2.3.0 build`. (Mi checker dio verde por `dist/` residual de
sesiones previas; el clon limpio del Analista lo destapo.)

## Remediacion (elige la mas limpia, preferida la 1)
1. **Hacer `governance:smoke` autocontenido y reproducible en clon limpio:** que construya (o garantice
   `dist/server/server.js`) antes de correr el smoke -- p.ej. `governance:smoke` = build-if-missing + smoke, o un
   `pregovernance:smoke` que haga `vite build`. Asi el comando literal de AC3 pasa desde un clon fresco.
2. **Si prefieres no construir en el gate:** redefinir el gate explicitamente como
   `pnpm build && pnpm governance:smoke`, actualizar AC3 + la evidencia + `docs/SEAMS.md` para reflejarlo.

## DoD del fix
Desde un CLON LIMPIO fresco (sin `dist/` previo): el gate de AC3 sale **exit 0 reproducible** (documenta los
comandos exactos). f0-test sigue verde. Sin tocar el cache ya validado ni introducir writer-path. Entrega
`in_review` con la evidencia clon-limpio (npm test + el gate smoke reproducible, con exit codes). Commit Zeus-Aegis
como Arquitecto + `Co-Authored-By: Codex`.

ETA: corta. Si algo bloquea -> `blocked` + una pregunta.
