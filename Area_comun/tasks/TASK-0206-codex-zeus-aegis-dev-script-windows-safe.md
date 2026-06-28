---
task_id: TASK-0206
title: "Zeus-Aegis: dev script Windows-safe (cross-env) - fix pnpm dev en Windows (DECISION-0064)"
type: product
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-06-28
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064]
file: Area_comun/tasks/TASK-0206-codex-zeus-aegis-dev-script-windows-safe.md
---

# TASK-0206 — Zeus-Aegis: dev script Windows-safe (cross-env)

## Contexto
El fork vendido `vendor/hermes-2.3.0` define sus scripts npm con sintaxis **POSIX sh**
(`NODE_OPTIONS="..." vite dev`). En Windows pnpm los corre vía `cmd.exe`, que NO entiende el
prefijo `VAR="valor" comando` y falla antes de invocar `vite`. Hoy el panel solo arranca con el
workaround manual `$env:NODE_OPTIONS=...; pnpm exec vite dev`.

Scripts afectados en `vendor/hermes-2.3.0/package.json` (verificados):
- `dev`        → `NODE_OPTIONS="--max-old-space-size=2048" vite dev`
- `start`      → `NODE_OPTIONS="--max-old-space-size=2048" node .output/server/index.mjs`
- `start:dev`  → `NODE_OPTIONS="--max-old-space-size=2048" vite dev`
- `electron:dev` → `NODE_ENV=development electron .`

`cross-env` NO está instalado.

## Objetivo
`pnpm dev` (y los demás) arrancan en Windows **sin** env manual, sin romper macOS/Linux.

## Alcance (solo esto)
1. Añadir `cross-env` a `devDependencies` de `vendor/hermes-2.3.0/package.json` y actualizar el lockfile (`pnpm install`).
2. Reescribir los 4 scripts con `cross-env`, p.ej.:
   - `"dev": "cross-env NODE_OPTIONS=--max-old-space-size=2048 vite dev"`
   - análogos para `start`, `start:dev`, `electron:dev` (`cross-env NODE_ENV=development electron .`).
3. Registrar el cambio como **delta de fork intencional** en `SEAMS.md` (o el log de parches del fork): qué se tocó y por qué, para no perderlo en un futuro sync con upstream.

## Fuera de alcance
No tocar otros scripts ni lógica; no actualizar versiones de otras deps; no rebrand (eso es TASK-0207).

## Criterios de aceptación
- **AC1:** en Windows, `pnpm dev` arranca Vite y sirve `http://127.0.0.1:3000/governance` sin necesidad de setear `NODE_OPTIONS` a mano.
- **AC2:** `pnpm start:dev` y `pnpm electron:dev` arrancan igual (o fallan solo por causas no relacionadas con la sintaxis de env).
- **AC3:** `cross-env` aparece en `package.json` devDependencies y en el lockfile; `pnpm install` reproducible.
- **AC4:** el delta queda documentado en SEAMS.md/log de parches del fork.
- **AC5:** la suite del fork sigue igual que antes del cambio (no introducir regresión: `pnpm test` sin nuevos fallos respecto al baseline waivado).

## Definition of Done
AC1–AC5 verdes; handoff autocontenido `in_review` a Arquitecto (checker) con: salida real de `pnpm dev` arrancando en Windows, diff de package.md/lockfile, y nota SEAMS. Commit en Zeus-Aegis como Arquitecto con `Co-Authored-By: Codex`. Sin tocar el core del protocolo ni el baseline TFM.
