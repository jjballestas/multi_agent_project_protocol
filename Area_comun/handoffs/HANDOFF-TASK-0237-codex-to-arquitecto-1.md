---
handoff_id: HANDOFF-TASK-0237-codex-to-arquitecto-1
task_id: TASK-0237
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-02
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: b3d863a
---

# TASK-0237 - Hang-proof de npm test en Zeus-Aegis

## Resultado
- Commit producto: `b3d863a test(governance): bound zeus aegis npm test`.
- `npm test` del repo raiz ahora entra por `scripts/run-product-test.mjs`, que instala con `CI=1`, ejecuta el test vendor y mata el arbol del proceso si supera el timeout duro.
- `vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` mantiene `vitest run`, fuerza `CI=1`, `--pool=threads`, `--maxWorkers=1`, `--no-file-parallelism`, `--testTimeout=30000`, `--hookTimeout=30000`, y hard timeout de runner.
- `vite.config.ts` fija `pool: 'threads'`, `fileParallelism: false`, `testTimeout`, `hookTimeout` y `teardownTimeout`.

## Repro del fallo observado
- Con la variante inicial basada en proceso fork se reprodujo el fallo de IPC observado en TASK-0222/0237: `ERR_IPC_CHANNEL_CLOSED`; el proceso termino con exit `1` en 114.9s, sin colgar.
- Tras cambiar a pool de threads + no-file-parallelism, la suite paso y termino acotada.

## Evidencia
- `node --check scripts/run-product-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `git diff --check`: PASS con solo warnings CRLF de Git.
- Watchdog negativo: `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test`: exit `124` en 6.1s, mata el arbol y no cuelga.
- Local `npm test`: PASS, 83 files / 562 tests, 185.9s.
- Clean clone `C:/Users/johnb/AppData/Local/Temp/codex-0237-zeus-aegis-clean-b3d863a-1`: `npm test` PASS, 83 files / 562 tests, 112s.
- Clean clone `C:/Users/johnb/AppData/Local/Temp/codex-0237-zeus-aegis-clean-b3d863a-2`: `npm test` PASS, 83 files / 562 tests, 263.7s including fresh install.

## Notas de review
- No se cambio NOTICE/Licencia.
- No se redujo la lista de suites F0; el conteo sube a 83 files / 562 tests por incluir la suite `zeus-env-aliases` de TASK-0229.
- TASK-0229 quedo bloqueada temporalmente antes de tomar TASK-0237 porque su gate obligatorio dependia de este arreglo; puede reanudarse tras esta review.
