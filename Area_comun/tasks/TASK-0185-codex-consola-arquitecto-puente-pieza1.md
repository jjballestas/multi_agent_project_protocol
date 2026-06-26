---
task_id: TASK-0185
title: "Consola del Arquitecto pieza 1: proceso-puente gobernado (sesion viva + streaming, no-bypass, runtime-only, sesion unica, off-by-default) (SPEC-0098, DECISION-0062)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0098
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: TASK-0178 / DECISION-0062 (consola del Arquitecto; GO operador 2026-06-26)
reuses: []
linked_decisions: [DECISION-0062, DECISION-0057, DECISION-0022, DECISION-0040, DECISION-0050]
file: Area_comun/tasks/TASK-0185-codex-consola-arquitecto-puente-pieza1.md
---

# TASK-0185 - Consola del Arquitecto, pieza 1 (proceso-puente, slice minimo)

> maker=Codex / checker=Arquitecto. Repo = Zeus-protocol (producto, DECISION-0050). Vertical slice MINIMO
> end-to-end del puente; UI rica = pieza 2, auditoria endurecida = pieza 3. Off-by-default. NO toca #4/config.

## Alcance (SPEC-0098 AC1-AC6)
- **Proceso-puente** que lanza/mantiene UNA sesion viva del runtime del Arquitecto, recibe un mensaje del operador
  y **streamea** su salida/reporte de vuelta. Off-by-default.
- **Endpoints del front (server):** abrir/estado, enviar mensaje, **stream** (p.ej. SSE), detener. Read-only sobre
  el trabajo (no aplica estado por su cuenta).
- **Registro de activacion** FUERA del config pinned (`*.runtime.json` gitignored; versionado OFF).

## DoD (= SPEC-0098 AC1-AC6)
- AC1 off-by-default fail-closed (sin activacion runtime, todo inactivo; flag no commiteado).
- AC2 no-bypass (prueba negativa PERMANENTE): sin ruta de escritura al ledger/event-log; no importa escritores;
  toda mutacion del Arquitecto sigue por submit_intent.
- AC3 runtime-only (espejo DECISION-0057): solo lanza/relanza/detiene; nunca identidad/llaves/registro/config;
  **stop del operador honrado** (la sesion termina de verdad).
- AC4 sesion unica (anti-colision): a lo sumo una sesion viva; segundo intento reusa o se rechaza, nunca paralela.
- AC5 streaming + guarda PII: salida transmitida; lo persistido redactado y NUNCA al #4 (DECISION-0040).
- AC6 gates: gate rapido verde + caso en tier CI; protocolo validate exit 0 (con/sin secretos), drift 0,
  encoding/neutrality exit 0; protocol.config.json/genesis intactos; Co-Authored-By Codex.

## Fuera de alcance
- UI conversacional rica + transporte avanzado (pieza 2); auditoria endurecida (pieza 3).
- Consolas para Codex/Analista; NOVA; multi-tenant; alta/baja de agente (RF-9). Cualquier escritura directa al
  ledger desde el canal (prohibida).

## Notas
- El puente DIRIGE al Arquitecto, no actua por el (no-bypass + runtime-only + off-by-default = condicion de cierre).
- Clon del producto en Windows: `git -c core.longpaths=true`. Checker (Arquitecto) re-verifica desde clon limpio.
