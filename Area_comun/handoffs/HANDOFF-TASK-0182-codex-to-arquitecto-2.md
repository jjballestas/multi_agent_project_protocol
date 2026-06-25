---
handoff_id: HANDOFF-TASK-0182-codex-to-arquitecto-2
task_id: TASK-0182
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-26T00:35:00Z
product_commit: a6b830c
---

# TASK-0182 cambio - CI full suite

## Resultado

Se corrigio el item de cambio acotado: GitHub Actions ya no ejecuta el gate rapido `npm test`.
Ahora ejecuta `npm run test:ci`, que delega a `npm run test:slow` y activa
`ZEUS_RUN_SLOW_TESTS=1`, por lo que la automatizacion corre los 93 tests completos, incluidos los
guards lentos de PII, no-bypass, no-egress, candidate-review y auto-commit-push.

`npm test` queda rapido para el revisor interactivo y desarrollo local. README documenta la
separacion.

## Producto

- Repo: `D:/Agentes/Zeus/Zeus-protocol`
- Commit: `a6b830c ci(test): run full suite in automation`
- Archivos tocados:
  - `.github/workflows/ci.yml`
  - `package.json`
  - `README.md`
- Produccion no tocada: `src/server.js` y `public/app.js` sin cambios.

## Evidencia

- `node --check src/server.js public/app.js tests/staticContract.test.js` OK.
- `git diff --check -- .github/workflows/ci.yml package.json README.md` OK.
- `npm test` PASS: 93 tests enumerados, 77 pass, 16 skip, 0 fail, duration ~1.3s.
- `npm run test:ci` PASS: 93 pass, 0 skip, 0 fail, duration ~962s.
- Intento previo de `npm run test:ci` con timeout local de 904s expiro por margen insuficiente; la
  repeticion con 1800s completo verde.

## Pendiente para checker

Revisar en clon limpio que `.github/workflows/ci.yml` invoca `npm run test:ci` y que el job ejecuta
el suite completo, no el default rapido.
