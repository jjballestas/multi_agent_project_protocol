---
task_id: TASK-0298
title: "Aegis Front MVP L1 unidad 1: convertir el architect-bridge de control-spawn a observacion-tail (firehose de la sesion real del Arquitecto via run-logs del cron; observation-only, read-only, dual-session-safe)"
type: feature
status: in_progress
owner: Codex
maker: Codex
checker: Analista
reviewer: Analista
phase: P2
priority: normal
created_at: 2026-07-27
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin: TASK-0178 / DESIGN-0178 (Aegis Front; goal del operador 2026-07-27; stack vanilla + firehose de sesion real + fuente cron run-logs)
project: multi_agent_project_protocol
relates_to: [TASK-0178, TASK-0185, TASK-0186, TASK-0187, TASK-0188, DECISION-0050, DECISION-0095]
linked_decisions: [DECISION-0050, DECISION-0095, DECISION-0057]
file: Area_comun/tasks/TASK-0298-aegis-bridge-observacion-tail.md
intake:
  type: feature
  goal: Primera unidad del MVP L1 del Aegis Front (DESIGN-0178, s.0 manda). El architect-bridge de Zeus-protocol HOY es el modelo que DESIGN-0178 RECHAZO: spawnea un SEGUNDO Arquitecto dentro del repo gobernado (server.js createArchitectBridgeManager open() -> spawn) + reenvia stdin (send() / launcher) = CANAL DE CONTROL + la UI es una consola de MANDO (textarea "Mensaje al Arquitecto" + Enviar). Convertirlo a OBSERVACION PURA: transmite la sesion REAL del Arquitecto EN VIVO tailando los run-logs que el cron del Arquitecto YA escribe (PROTOCOL_REPO_PATH/.protocol-tmp/arquitecto_cron/runs/<stamp>-arquitecto.out.log via Start-Process -RedirectStandardOutput), read-only, SIN canal de control, con guarda anti-segundo-Arquitecto por construccion (cero ruta de spawn en el bridge). Honra I1 (el usuario OBSERVA, no dirige), I2/I3 (el front nunca firma/actua por el usuario). Reusa la plomeria SSE + redaccion PII + audit + coalescing que YA existen. Stack VANILLA existente (NO React). Fuente observable canonica = run-logs del cron (decision del operador); el modo interactivo queda como fast-follow (transcript-sink, fuera de alcance). Codigo en Zeus-protocol; gobernado desde el hub (patron 0180-0199); cross-atestado (DECISION-0095). NO toca el ledger/estado gobernado del hub ni el config pineado.
  acceptance:
    - AC1 STREAM EN VIVO - con un observeRunsDir + pid de cron "vivo" (via config/env, NO path hardcodeado), escribir incrementalmente a <stamp>-arquitecto.out.log emite esos bytes como eventos SSE 'output' redactados y coalescidos por el cliente; detecta rollover de run-log (nuevo ciclo del cron = archivo nuevo) con un evento 'status' de frontera.
    - AC2 READ-ONLY - el bridge solo LEE observeRunsDir y escribe unicamente su propio audit (.runtime/architect-bridge/); snapshot byte-a-byte de un estado gobernado de muestra (p.ej. TASK_INDEX.json + events.jsonl del observeRunsDir root) y del run-log ANTES/DESPUES de attach+stream = identicos. Cero ruta de escritura a estado gobernado (el patron DIRECT_WRITE_ROUTE_PATTERN se mantiene).
    - AC3 CONTROL DESHABILITADO (I1) - el endpoint /send responde 403 "observation-only: control disabled" sin escribir nada ni emitir evento 'input'; el launcher deja de reenviar stdin (se quita el forward de process.stdin); la UI no tiene compose (textarea/boton "Enviar" removidos; "Abrir/Finalizar" -> "Observar/Desadjuntar").
    - AC4 ANTI-SEGUNDO-ARQUITECTO (I3) - el codigo del manager NO contiene `spawn(`; con pid de cron NO vivo, /open degrada a estado 'dormant'/no-live-session (nunca spawnea). Direccion fail-safe: mal-detectar "vivo" solo tailea un log terminado (inocuo, read-only); mal-detectar "muerto" degrada.
    - AC5 PII - vector de PII (email/telefono/NIT/documento/cuenta/direccion) inyectado en el run-log -> aparece [*-REDACTED] en SSE y en el audit, y los literales estan AUSENTES (reusa el vector de TASK-0187).
    - AC6 CONTRATO + GATES - la lista contractual de 5 endpoints del bridge se mantiene (staticContract); node --test verde en Zeus-protocol; los tests de spawn/control (TASK-0185/0188 "streams one live session", "honors operator stop", forward de stdin) se REESCRIBEN a tail/observacion; nuevos tests de read-only, control-inerte (403) y dual-session (dormant sin spawn).
  verification_cmd:
    - cd D:/Agentes/Zeus/Zeus-protocol
    - node --test
    - (el checker corre en clon limpio de Zeus-protocol; observeRunsDir/cronPidPath por config/env, JAMAS path hardcodeado, o el clon limpio no lo encuentra)
  scope_routes:
    - D:/Agentes/Zeus/Zeus-protocol/src/server.js
    - D:/Agentes/Zeus/Zeus-protocol/scripts/architect-runtime-launcher.mjs
    - D:/Agentes/Zeus/Zeus-protocol/public/app.js
    - D:/Agentes/Zeus/Zeus-protocol/architect-bridge.config.json
    - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
  out_of_scope:
    - Opcion (b) transcript-sink para el modo INTERACTIVO del Arquitecto -- fast-follow, FUERA de esta unidad (riesgo E1 del Plan; la fuente canonica del MVP es el cron).
    - Reescritura a React+TS+Vite -- FUERA; se construye sobre el vanilla existente (decision del operador).
    - Cualquier escritura al ledger/estado gobernado del hub -- el bridge es READ-ONLY (no-bypass permanente).
    - protocol.config.json pineado del hub (2E35F26E, epoch 1.14.0), dataset N=500 -- fondo intocable.
    - Provision/onboarding (L2/L3), distribucion, licencia -- fases posteriores del roadmap.
  risk: medium
  estimate: M
---

# TASK-0298 - Aegis Front MVP L1 unidad 1: bridge control-spawn -> observacion-tail

> maker=Codex / checker=Analista. Repo = Zeus-protocol (producto, DECISION-0050). Codigo alla, gobernanza
> aqui (patron 0180-0199), cross-atestado (DECISION-0095). Fuente del diseno: DESIGN-0178 (s.0 manda).

## Encuadre
El architect-bridge de hoy ES el modelo que DESIGN-0178 rechazo (spawnea un 2do Arquitecto + reenvia
stdin = control + UI de mando). Esta unidad lo convierte en OBSERVACION PURA: sin spawn, sin canal de
control, tail redactado de los run-logs del cron del Arquitecto -> SSE. La sesion REAL ya se emite a
disco (arquitecto_cron.ps1 con Start-Process -RedirectStandardOutput). El bridge se vuelve un tail -f
redactado sobre un archivo que el Arquitecto real ya produce; el anti-segundo-Arquitecto pasa de riesgo
a mitigar a IMPOSIBLE (el bridge no tiene ruta de spawn).

## Decisiones del operador (2026-07-27)
- Stack: vanilla existente (Node/JS), NO React.
- Primera unidad: firehose de la sesion REAL del Arquitecto en vivo.
- Fuente observable canonica: run-logs del cron (.protocol-tmp/arquitecto_cron/runs/*-arquitecto.out.log).

## Riesgos declarados (para el checker)
- E1: la fuente (a) solo observa al Arquitecto en modo CRON; el modo interactivo queda sin sink
  (fast-follow, fuera de alcance). El panel muestra honestamente "sin sesion viva" si el cron no corre.
  DECLARADO, no es defecto -- el checker NO debe marcarlo como gap de esta unidad.
- Liveness "en vivo" = segun se vacia el buffer de Start-Process -RedirectStandardOutput (no keystroke-level).
- Rollover: carrera si un ciclo del cron arranca entre polls (posible perdida del borde inicial de un ciclo).
- PII best-effort (regex); mitigacion = operatorPresentRequired + localhost.
- Decision menor del maker: launcher NEUTRALIZAR (quitar stdin-forward) vs RETIRAR (rompe tests 0188/README);
  recomendado NEUTRALIZAR + reescribir los tests de spawn.

## Cierre / cross-atestacion (DECISION-0095)
Deliverable en Zeus-protocol; al cerrar, anclar la entrada de cross-atest al hub por blob de git (patron
0185/0188). Ciclo gobernado: maker Codex -> recomputo del Arquitecto -> review adversarial de la Analista
en clon limpio de Zeus-protocol -> ratifico -> done-flip por Codex. Tope 2 iteraciones.
