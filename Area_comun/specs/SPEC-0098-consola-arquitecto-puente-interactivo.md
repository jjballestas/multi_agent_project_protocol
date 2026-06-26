---
spec_id: SPEC-0098
task_id: TASK-0185
type: security
status: accepted
linked_decisions:
  - DECISION-0062
  - DECISION-0057
  - DECISION-0022
  - DECISION-0040
  - DECISION-0050
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0098 - Consola del Arquitecto (puente interactivo persistente)

## Context

DECISION-0062 (accepted): canal vivo Operador<->Arquitecto via un puente de runtime PERSISTENTE + streaming a la
UI; invariantes no-bypass / runtime-only / sesion unica / off-by-default / auditoria+guarda PII. Codigo en
Zeus-protocol (producto, DECISION-0050); gobernanza aqui. Se construye **por pieza** (maker=Codex /
checker=Arquitecto):
- **Pieza 1 (TASK-0185, esta SPEC AC1-AC6):** el **proceso-puente** gobernado (vertical slice minimo end-to-end).
- Pieza 2 (tarea posterior): consola UI conversacional + transporte de streaming en el front.
- Pieza 3 (tarea posterior): auditoria (store controlado + guarda PII) endurecida.

## Scope (pieza 1 = proceso-puente, slice minimo)

- **Proceso-puente** en Zeus-protocol: lanza y mantiene **una** sesion VIVA del runtime del Arquitecto, recibe un
  mensaje del operador y **transmite (streaming)** la salida/reporte del Arquitecto de vuelta. Off-by-default.
- **Endpoints del front (server):** abrir/estado de la sesion, enviar mensaje, **stream** de salida (p.ej. SSE),
  detener la sesion. READ-ONLY sobre el trabajo (no aplica estado por su cuenta).
- **Registro de activacion** FUERA del config pinned (`*.runtime.json` gitignored; el versionado queda OFF).
- Vertical slice minimo: enviar 1 mensaje -> el puente despierta/alimenta la sesion del Arquitecto -> el operador
  ve el streaming -> stop honrado. UI rica = pieza 2.

## Acceptance Criteria (pieza 1)

- **AC1 (off-by-default fail-closed):** sin activacion por runtime config, el puente y sus endpoints estan
  INACTIVOS (no lanzan nada). El config versionado queda `enabled:false`; el flag no se commitea.
- **AC2 (no-bypass, prueba negativa PERMANENTE):** el puente/endpoints NO tienen ruta de escritura al ledger/
  event-log; toda mutacion de estado del Arquitecto sigue por `submit_intent`. Test negativo: el canal NO puede
  aplicar una transicion ni editar `Area_comun/state/*`; no importa escritores del ledger.
- **AC3 (runtime-only, espejo DECISION-0057):** el puente solo lanza/relanza/detiene la sesion del Arquitecto;
  NUNCA toca identidad/llaves/`agent_registry`/config. Test: no hay ruta a re-genesis/registro; **stop del
  operador honrado** (la sesion termina de verdad).
- **AC4 (sesion unica, anti-colision):** a lo sumo UNA sesion viva del Arquitecto; un segundo intento de abrir
  reusa o es rechazado, nunca arranca una paralela. Test de comportamiento.
- **AC5 (streaming + guarda PII):** la salida se transmite al operador; lo que se persista (audit minimo) va
  redactado best-effort y **NUNCA** al event-log #4 (DECISION-0040). El chat no contamina el dataset atestado.
- **AC6 (gates):** clon limpio del producto `npm test`/`node --test` verde (gate rapido) + el caso en el tier CI;
  protocolo `validate_collaboration_state.py` exit 0 (con/sin secretos), drift 0, scan_encoding/neutrality exit 0;
  `protocol.config.json`/genesis intactos; Co-Authored-By Codex.

## Out of scope (pieza 1)

- UI conversacional rica + transporte avanzado (pieza 2); auditoria endurecida (pieza 3).
- Consolas vivas para Codex/Analista; fabrica NOVA; multi-tenant; alta/baja de agente (RF-9 re-genesis).
- Cualquier ruta de escritura directa al ledger desde el canal (prohibida por invariante).

## Notes

- El puente es un wrapper de runtime (analogo a los crons pero interactivo + streaming + sesion unica); su poder
  es DIRIGIR al Arquitecto, no actuar por el. Por eso no-bypass + runtime-only + off-by-default + auditoria son
  condicion de cierre, no opcionales.
- Repo producto Zeus-protocol; clon en Windows: `git -c core.longpaths=true`.
