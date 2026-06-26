---
task_id: TASK-0188
title: "Launcher del runtime del Arquitecto (command del puente): contrato stdin->turno->stdout, inner configurable, identidad existente, no-bypass, instancia unica, off-by-default (SPEC-0101, DECISION-0063)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0101
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: DECISION-0063 (activar consola; construir launcher; GO operador 2026-06-26)
reuses: [TASK-0185]
linked_decisions: [DECISION-0063, DECISION-0062, DECISION-0057, DECISION-0022, DECISION-0050]
file: Area_comun/tasks/TASK-0188-codex-launcher-runtime-arquitecto.md
---

# TASK-0188 - Launcher del runtime del Arquitecto

> maker=Codex / checker=Arquitecto. Repo = Zeus-protocol. Es el `command` que el puente (TASK-0185) hace spawn.
> Tests con inner-runtime STUB (no Arquitecto real). Off-by-default. NO toca #4/config. La activacion viva real =
> paso del operador presente (poner el inner real en el runtime config).

## Alcance (SPEC-0101 AC1-AC7)
- **Wrapper launcher** (p.ej. `scripts/architect-runtime-launcher.mjs`): lee mensajes por stdin (uno por turno),
  invoca el **inner-runtime configurable** (CLI del Arquitecto via env/config), emite su salida por stdout
  line-buffered (streaming), proceso de larga vida con contexto entre turnos.
- **Instancia unica** (lock/PID) + **cese** limpio (SIGTERM/cierre stdin -> termina inner+launcher sin huerfanos).
- NO escribe ledger/estado; mutaciones = Arquitecto via submit_intent.

## DoD (= SPEC-0101 AC1-AC7)
- AC1 contrato stdin->turno->stdout (N msgs -> N respuestas en orden, line-buffered, proceso de larga vida) con stub.
- AC2 inner-runtime configurable (no hardcode); inner ausente falla-closed con error claro.
- AC3 identidad existente / runtime-only (no crea/reconfigura identidad/llaves/registro; pasa env existente).
- AC4 no-bypass (no importa escritores; no escribe Area_comun/state ni events.jsonl; ledger byte-identico con stub).
- AC5 instancia unica (2o no arranca) + cese limpio (sin huerfanos).
- AC6 off-by-default / integra como command del puente; README: como configurarlo para uso vivo (paso operador).
- AC7 gates: npm test rapido verde + test:ci VENTANA QUIETA 100% pass; protocolo validate exit 0 (con/sin secretos),
  drift 0, encoding/neutralidad exit 0; config/genesis intactos; Co-Authored-By Codex.

## Fuera de alcance
- Invocar un Arquitecto real en tests (stub); la activacion viva = paso del operador presente.
- Launchers para otros agentes; NOVA; multi-tenant; alta/baja de agente; cambiar identidad.

## Notas
- El launcher DIRIGE al Arquitecto interactivo, no actua por el. Reusa/encaja con el puente de TASK-0185 (su
  config.command). Checker corre test:ci en ventana quieta (`git -c core.longpaths=true` al clonar en Windows).
