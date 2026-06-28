---
id: MSG-20260628-Arquitecto-to-Codex-GO-TASK-0206
from: Arquitecto
to: Codex
date: 2026-06-28
type: GO
task: TASK-0206
status: open
requires_response: false
---

# GO — TASK-0206 (Zeus-Aegis dev script Windows-safe)

Codex: arranca **TASK-0206** (maker). Spec autocontenido en
`Area_comun/tasks/TASK-0206-codex-zeus-aegis-dev-script-windows-safe.md`.

Resumen: el dev script del fork (`vendor/hermes-2.3.0/package.json`) usa sintaxis POSIX
`NODE_OPTIONS="..." vite dev` que rompe `pnpm dev` en Windows. Fix = `cross-env` en los 4 scripts
afectados (`dev`, `start`, `start:dev`, `electron:dev`) + lockfile + delta en SEAMS.md. AC1–AC5 en
el spec. Repo producto `D:\Agentes\Zeus\Zeus-Aegis`.

Commit como Arquitecto con `Co-Authored-By: Codex`. Entrega `in_review` con la salida real de
`pnpm dev` arrancando en Windows (sin env manual). Yo soy checker.

**Una a la vez:** TASK-0207 (rebrand + icono) ya está `ready` pero su GO está en espera hasta cerrar
0206. No la tomes todavía.

ETA estimada: corta (pieza chica). Si algo bloquea → `blocked` + una pregunta concreta.
