---
spec_id: SPEC-0101
task_id: TASK-0188
type: security
status: accepted
linked_decisions:
  - DECISION-0063
  - DECISION-0062
  - DECISION-0057
  - DECISION-0022
  - DECISION-0050
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0101 - Launcher del runtime del Arquitecto (lo que el puente hace spawn)

## Context

DECISION-0063 (accepted): construir el launcher que el puente de la consola (DECISION-0062, TASK-0185) hace
`spawn` para correr un Arquitecto interactivo. Contrato stdin(mensaje operador)->turno->stdout(streaming),
identidad existente, no-bypass, off-by-default, sesion unica, cese honrado. maker=Codex / checker=Arquitecto.
Repo = Zeus-protocol. El runtime de Arquitecto concreto (CLI) es **dependencia de entorno**; en tests se usa un
**inner-runtime STUB** (no se invoca un Arquitecto real).

## Scope

- **Wrapper launcher** (Zeus, p.ej. `scripts/architect-runtime-launcher.mjs`) apto como `command` del puente:
  lee mensajes del operador por **stdin** (uno por turno), invoca el **inner-runtime configurado** (el CLI del
  Arquitecto, via env/config), emite su salida por **stdout** linea a linea (para el streaming del puente), y
  mantiene contexto entre turnos (proceso de larga vida).
- **Inner-runtime configurable:** el binario/args del Arquitecto se toma de config/env (no hardcode); en tests =
  stub determinista. Esto permite probar el CONTRATO sin un Arquitecto real.
- **Guarda de instancia unica** del launcher (lockfile/PID) + **cese** limpio (SIGTERM/cierre de stdin termina el
  inner y el launcher).
- El launcher NO escribe el ledger/estado; cualquier mutacion la hace el Arquitecto via `submit_intent`.

## Acceptance Criteria

- **AC1 (contrato stdin->turno->stdout):** con un inner-runtime stub, enviar N mensajes por stdin produce N
  respuestas en stdout en orden, line-buffered (apto para streaming); el proceso es de larga vida (no termina
  tras un turno). Behavior-test.
- **AC2 (inner-runtime configurable, no hardcode):** el binario/args del Arquitecto viene de config/env; test con
  un stub demuestra que NO hay un CLI hardcodeado y que un inner ausente falla closed (error claro, no cuelga).
- **AC3 (identidad existente / runtime-only, espejo DECISION-0057):** el launcher NO crea ni reconfigura
  identidad/llaves/`agent_registry`/config; pasa el entorno del Arquitecto existente al inner. Test de
  imports/rutas: no toca registro ni genera llaves.
- **AC4 (no-bypass):** el launcher NO importa escritores del ledger/event-log y NO escribe `Area_comun/state` ni
  `runtime/state/events.jsonl`; el ledger queda byte-identico durante una sesion del launcher con el stub. Prueba
  negativa.
- **AC5 (instancia unica + cese):** un segundo launcher no arranca en paralelo (lock/PID); SIGTERM o cierre de
  stdin termina inner+launcher de forma limpia (sin huerfanos). Behavior-test.
- **AC6 (off-by-default / integracion con el puente):** documentado como `command` del puente; sin runtime config
  (enabled:true + command), el puente no lo lanza (heredado DECISION-0062). README: como configurarlo para uso vivo
  (paso del operador presente).
- **AC7 (gates):** `npm test` (rapido) verde + casos en el tier CI (`npm run test:ci` en VENTANA QUIETA, 100%
  pass); protocolo validate exit 0 (con/sin secretos), drift 0, encoding/neutrality exit 0; `protocol.config.json`/
  genesis intactos; Co-Authored-By Codex.

## Out of scope

- Invocar un Arquitecto real en los tests (se usa stub); la activacion viva real = paso del operador presente
  (poner el inner-runtime real en el runtime config + arrancar el front).
- Launchers para Codex/Analista/otros; NOVA; multi-tenant; alta/baja de agente (re-genesis); cambiar identidad.

## Notes

- El launcher es el `command` que faltaba para que el puente corra un Arquitecto. Su poder es DIRIGIR al
  Arquitecto interactivo, no actuar por el (no-bypass + identidad existente + sesion unica + off-by-default).
- Repo producto Zeus-protocol; clon en Windows: `git -c core.longpaths=true`. Checker corre test:ci en ventana
  quieta (sin peers mid-exec).
