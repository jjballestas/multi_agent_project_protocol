---
artifact_id: ANALISTA-TASK-0237-hang-proof-veredicto
task_id: TASK-0237
author: Analista
type: review_verdict
created_at: 2026-07-02
verdict: CAMBIO-REQUERIDO
---

# ANALISTA TASK-0237 hang-proof verdict

Firma: Analista.

## Veredicto

CAMBIO-REQUERIDO / NO-GO de cierre. El `npm test` de la raiz del producto paso 3/3 en clon limpio y el
watchdog de la raiz devuelve exit 124 acotado, pero el watchdog interno del paquete vendor no cumple la
evidencia declarada: con `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` imprime el
mensaje de hard timeout y no termina dentro de 120 s. Eso refuta el claim "exit 124 en 6.1s" y deja un backstop
interno que no mata realmente el runner en Windows.

## Ancla canonica

| Item | Valor |
| --- | --- |
| Protocolo HEAD vivo | `cf84aa06f98dcf371e47c035b0c7ebe4e60a9ba2` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260702-Arquitecto-to-Analista-REVIEW-TASK-0237-hang-proof.md` |
| Handoff | `Area_comun/handoffs/HANDOFF-TASK-0237-codex-to-arquitecto-1.md` |
| Producto canonico | `D:/Agentes/Zeus/Zeus-Aegis` |
| Producto commit | `b3d863a9889c67274590232959eeb07ac324a548` |
| Nota de ancla | La orden generica nombraba `Zeus-protocol`, pero `b3d863a` no existe alli (cat-file exit 128) y si existe en `Zeus-Aegis` (exit 0), que es el `product_repo` canonico de TASK-0237. |
| Clon limpio producto | `C:/Users/johnb/AppData/Local/Temp/analista-0237-aegis-c38fe58fa1f14ee6b89c1cfe45d3dd3a/zeus-aegis` |

## Reproduccion y gates

| Gate | Resultado |
| --- | --- |
| `npm test` clon limpio run 1 | exit 0; wall 258.6 s; Vitest 83 files / 562 tests; duration 144.26 s |
| `npm test` clon limpio run 2 | exit 0; wall 129.4 s; Vitest 83 files / 562 tests; duration 122.58 s |
| `npm test` clon limpio run 3 | exit 0; wall 216.8 s; Vitest 83 files / 562 tests; duration 210.01 s |
| Root watchdog `ZEUS_AEGIS_ROOT_TEST_HARD_TIMEOUT_MS=1 npm test` | exit 124; wall 1.2 s; log contiene `run-product-test: hard timeout after 1ms` |
| Vendor watchdog `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` | SLIPS: herramienta externa mato la prueba por timeout a 124 s; log contiene `zeus-aegis-f0-test: hard timeout after 1ms` pero el proceso siguio ejecutando tests despues del timeout |
| Bug real no enmascarado | PASS: test inyectado con `expect(1).toBe(2)` via `vitest run` sale exit 1 en 7.0 s |
| Procesos remanentes tras pruebas | PASS acotado: no quedaron procesos `node`/`npm`; solo `cmd` preexistentes ajenos |
| Protocolo live validate | exit 0 |
| Protocolo secretless validate en clon limpio | exit 0 |
| Drift live | `has_drift=false`, `up_to_seq=3041` |
| Drift secretless | `has_drift=false`, `up_to_seq=3032` |
| Domain neutrality scan | exit 0 live y secretless |
| Encoding scan | exit 0 live y secretless |
| `protocol.config.json` sha256 | `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354` |

## Vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| `npm test` raiz usa ruta no-watch | PASA | `package.json` raiz ejecuta `node scripts/run-product-test.mjs`; vendor ejecuta `node scripts/zeus-aegis-f0-test.mjs`; el script vendor invoca `vitest run`. |
| `CI=1` en entorno de test | PASA | Ambos wrappers inyectan `CI: '1'`; vendor tambien inyecta `VITEST: '1'`. |
| Serializacion / no file parallelism | PASA | Vendor pasa `--pool=threads`, `--maxWorkers=1`, `--no-file-parallelism`; `vite.config.ts` fija `pool: 'threads'` y `fileParallelism: false`. |
| Timeout de tests/hooks | PASA | Vendor CLI pasa `--testTimeout=30000 --hookTimeout=30000`; `vite.config.ts` fija `testTimeout`, `hookTimeout` y `teardownTimeout`. |
| Suite full termina en clon limpio | PASA | 3 corridas consecutivas de `npm test` terminaron exit 0 (258.6 s, 129.4 s, 216.8 s). |
| Root hard timeout del comando canonico | PASA | `ZEUS_AEGIS_ROOT_TEST_HARD_TIMEOUT_MS=1 npm test` termino exit 124 en 1.2 s. |
| Vendor hard timeout declarado por Codex | SLIPS | `ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS=1 npm --prefix vendor/hermes-2.3.0 test` no termino dentro de 120 s. El log muestra que el timeout se disparo, pero Vitest siguio corriendo. |
| No enmascarar bugs reales | PASA | Un test inyectado con assertion falsa produjo exit 1 en 7.0 s. |
| Teardown mata procesos hijos | RIESGO DECLARADO | Root watchdog no dejo `node`/`npm`, pero el watchdog vendor no mato el runner cuando se disparo. Esto apunta a kill de arbol incompleto bajo `shell: true`/Windows en la capa vendor. |

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0237 hasta que el watchdog vendor cumpla lo declarado: un timeout de
`ZEUS_AEGIS_TEST_HARD_TIMEOUT_MS` debe terminar con exit 124 en tiempo acotado y no seguir ejecutando Vitest
despues del mensaje de timeout. Caso permanente recomendado: ejecutar el paquete vendor con timeout minimo y
asertar exit 124 + ausencia de procesos `node` descendientes.

Residual no bloqueante si se corrige lo anterior: el root wrapper si da un backstop de 15 minutos para `npm test`,
pero eso no sustituye el fail-fast interno prometido por el handoff.
