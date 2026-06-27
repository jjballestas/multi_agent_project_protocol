---
handoff_id: HANDOFF-TASK-0196-codex-to-arquitecto-1
task_id: TASK-0196
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-27
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 75273cb
---

# HANDOFF TASK-0196 - Zeus-Aegis F1a read-only panel

## Resultado

Producto Zeus-Aegis entregado en commit `75273cb feat(governance): add read-only F1a panel`.

F1a agrega:

- Contrato read-only `/api/governance/{health,state,backlog,mailbox}`.
- Lectura canonica via `git show` / `git ls-tree` contra `ZEUS_AEGIS_PROTOCOL_ROOT`
  (default `D:/Agentes/multi_agent_project_protocol`) y `ZEUS_AEGIS_PROTOCOL_REF` (default `HEAD`).
- Health derivado de `validate_collaboration_state.py` y drift replay real, fail-safe a no-verde.
- Vista `/governance` con Estado, Backlog filtrable por texto/estado/owner y Mailbox open.
- Test negativo que confirma que F1a no expone POST/PUT/PATCH/DELETE ni ruta directa a `submit_intent.py`.
- `docs/SEAMS.md` actualizado: waiver F0 sigue acotado a las superficies upstream no usadas por F1a.

## Evidencia producto

- `corepack pnpm exec vitest run src/server/governance-readonly.test.ts`: PASS 4/4.
- `npm test` desde `D:/Agentes/Zeus/Zeus-Aegis`: PASS 80 files / 537 tests.
- `node --check` OK:
  - `vendor/hermes-2.3.0/src/server/governance-readonly.ts`
  - `vendor/hermes-2.3.0/src/routes/api/governance.health.ts`
  - `vendor/hermes-2.3.0/src/routes/api/governance.state.ts`
  - `vendor/hermes-2.3.0/src/routes/api/governance.backlog.ts`
  - `vendor/hermes-2.3.0/src/routes/api/governance.mailbox.ts`
- Smoke local Vite en `127.0.0.1:4301`: HTTP 200 para `/api/governance/health`, `/state`,
  `/backlog` y `/mailbox`.
- `git diff --check`: PASS con solo warnings de normalizacion CRLF.

## Caveats

- La fuente canonica por defecto es `HEAD`; si el operador quiere ver cambios de protocolo aun no commiteados,
  debe usar un ref/commit ya aterrizado o cambiar explicitamente `ZEUS_AEGIS_PROTOCOL_REF`.
- No se agrega writer-path. F2 sigue gateado.
