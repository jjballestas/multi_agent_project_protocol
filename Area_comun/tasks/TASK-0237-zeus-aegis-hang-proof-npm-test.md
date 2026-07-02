---
task_id: TASK-0237
title: "[REQ-ZEUS-001] Hang-proof del npm test en Zeus-Aegis: vitest run sin watch + testTimeout duro + teardown que mata esbuild/node + CI=1"
type: build
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-07-02
reviewer: Analista
checker: Arquitecto
project: multi_agent_project_protocol
relates_to: [REQ-ZEUS-001, TASK-0236]
linked_decisions: [DECISION-0077]
linked_reqs: [REQ-ZEUS-001]
file: Area_comun/tasks/TASK-0237-zeus-aegis-hang-proof-npm-test.md
---

# TASK-0237 - [REQ-ZEUS-001] Hang-proof del npm test en Zeus-Aegis

- **Owner build:** Codex - **Review:** Analista - **Checker:** Arquitecto. maker != checker.
- **Repo producto:** `D:/Agentes/Zeus/Zeus-Aegis`.
- **Origen (evidencia 2026-07-02):** la CAUSA PRIMARIA de los jams recurrentes es que la suite `npm test` del
  producto **se cuelga** en un clon limpio (err.log del run `20260701T222832Z` = npm test colgado en el clon Temp,
  sin avanzar, sin workers). Como CADA tarea de workstream (0222/0227/0229/...) corre `npm test` en clon limpio como
  gate obligatorio, un test que cuelga traba al exec del agente una y otra vez. Hay que hacer la suite a prueba de
  cuelgues en su origen (no solo mitigar en el harness, que es TASK-0236).

## Alcance (hang-proof de la suite)
1. **`vitest run` sin watch** (nunca modo watch en CI/gates): el comando de `npm test` debe terminar siempre, sin
   quedar a la escucha. Verificar el script `test` de `package.json` del producto (y del vendor hermes si aplica).
2. **`testTimeout` (y `hookTimeout`) DUROS** en la config de vitest: ningun test/hook puede colgarse indefinido; al
   exceder el timeout el runner FALLA (exit != 0), no cuelga.
3. **Teardown que mata procesos hijos al salir** (esbuild/node/servidores levantados por los tests): un
   `globalTeardown`/afterAll que cierre servidores y termine subprocesos, de modo que el runner no quede vivo
   esperando handles abiertos. Considerar `pool`/`poolOptions` de vitest y `--no-file-parallelism` si algun worker
   IPC se cuelga (el `ERR_IPC_CHANNEL_CLOSED` visto en 0222 apunta a teardown de workers).
4. **`CI=1`** (y flags equivalentes) en el entorno de test: fuerza el modo no-interactivo/no-watch y desactiva
   prompts/colores que puedan bloquear en un entorno headless/clon limpio.

## DoD
- `npm test` en clon limpio del producto **termina siempre** (verde o rojo por assertion/timeout), NUNCA cuelga;
  evidencia: correrlo N veces en clon limpio con tabla de procesos limpia, todas terminan con exit code en tiempo acotado.
- Reproducir el escenario de hoy (el run que colgaba) y demostrar que ahora falla-rapido o pasa, sin colgarse.
- No degradar la cobertura ni enmascarar fallos reales (un timeout que oculta un bug no vale; el timeout es un
  backstop, no una excusa).
- Gate Analista: **GO** con repro del cuelgue de hoy y prueba de terminacion acotada. maker != checker.
- Neutralidad: `scope` producto (Zeus-Aegis), no toca el core del protocolo. Sin secretos. Conservar NOTICE MIT.

## Handoff
Autocontenida. maker (Codex) != checker (Arquitecto), review Analista con repro. Ambiguedad -> blocked + 1 pregunta concreta.
NOTA: se relaciona con TASK-0236 (harness) -- 0237 arregla la CAUSA (la suite cuelga), 0236 endurece el harness que la corre.
