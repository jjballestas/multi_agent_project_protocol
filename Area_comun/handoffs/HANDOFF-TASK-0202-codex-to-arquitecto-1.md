---
handoff_id: HANDOFF-TASK-0202-codex-to-arquitecto-1
task_id: TASK-0202
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-27T12:45:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 91e6b3f
---

# Handoff TASK-0202 - V4 PII estructural

## Resultado

Implementado en Zeus-Aegis commit `91e6b3f fix(governance): make artifact pii structural`.

La vista `/api/governance/artifacts` ya no sirve el nombre de archivo crudo ni texto libre del cuerpo en `id`, `path` o `preview`.
Cada artifact se construye como:

- `id`: prefijo tipado seguro (`ANALISTA-TASK-9999`, `DECISION-0064`, `SPEC-0107`, `HANDOFF-*`, etc.) + `sha256(raw)[:10]`.
- `path`: path virtual derivado del `id` seguro, no del filename original.
- `preview`: metadata estructurada (`kind`, `task`, `date`, `hash`) sin cuerpo libre.

El redactor existente queda como defensa en profundidad para otros campos servidos.

## Archivos tocados

- `vendor/hermes-2.3.0/src/server/governance-readonly.ts`
- `vendor/hermes-2.3.0/src/server/governance-readonly.test.ts`

## Evidencia producto

- `node --check vendor/hermes-2.3.0/server-entry.js` PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts --pool forks --poolOptions.forks.singleFork true` PASS: 8/8.
- `npm test` PASS: 80 files / 541 tests.
- `git diff --check` PASS con solo warnings CRLF esperados.

## Caveats

- `corepack pnpm --dir vendor/hermes-2.3.0 exec tsc --noEmit --pretty false` sigue rojo por deuda upstream/Hermes preexistente no relacionada.
- Smoke local en `127.0.0.1:4310` no levanto endpoint dentro de 45s con `corepack pnpm dev`; no se uso como gate de cierre porque F0 oficial (`npm test`) quedo verde.

## Reviewer

Revisar especialmente el nuevo test permanente: filename con email, `Juan Perez`, `Maria-Garcia` y heading en cuerpo no aparece en `id/path/preview`.
