# DRAFT TASK-0298 -- Aegis Front MVP L1, unidad 1: bridge control-spawn -> observacion-tail

> Draft privado. Se convierte en Area_comun/tasks/TASK-0298-*.md al registrar (tras rutear la review de 0297).
> Codigo en D:/Agentes/Zeus/Zeus-protocol (repo producto); gobernado desde el hub (rango 02xx, como 0180-0199);
> cross-atestado (DECISION-0095). Fuente del diseno: DESIGN-0178 (s.0 manda) + Plan agent 2026-07-27.

## Decisiones del Operador (2026-07-27)
- Stack: construir sobre el VANILLA existente (Node/JS), NO reescribir a React.
- Primera unidad: FIREHOSE de la sesion REAL del Arquitecto en vivo.
- Fuente observable canonica: RUN-LOGS DEL CRON (.protocol-tmp/arquitecto_cron/runs/*-arquitecto.out.log).

## Encuadre
El architect-bridge de hoy ES el modelo que DESIGN-0178 rechazo: spawnea un SEGUNDO Arquitecto dentro del repo
gobernado + `send()`/stdin-forward = canal de control + UI de mando. Esta unidad lo convierte en OBSERVACION PURA:
sin spawn, sin canal de control, tail redactado de los run-logs del cron -> SSE. Reusa toda la plomeria SSE +
redaccion PII + audit + coalescing que YA existen.

## intake (borrador)
- type: feature
- goal: Convertir el architect-bridge de Zeus-protocol de "control-spawn" (spawnea un 2do Arquitecto + forward de
  stdin + UI de mando) a "observacion-tail": transmite la sesion REAL del Arquitecto en vivo tailando los run-logs
  del cron (.protocol-tmp/arquitecto_cron/runs/*-arquitecto.out.log del hub), read-only, sin canal de control, con
  guarda anti-segundo-Arquitecto por construccion (cero ruta de spawn). Honra I1 (el usuario OBSERVA, no dirige),
  I2/I3 (no firma/actua por el usuario). Reusa la plomeria SSE + redaccion PII + audit existentes.
- acceptance:
  - AC1 STREAM EN VIVO: con un observeRunsDir + pid de cron "vivo" (fixture, por config/env NO hardcode), escribir
    incrementalmente a <stamp>-arquitecto.out.log emite esos bytes como eventos SSE `output` redactados y
    coalescidos por el cliente. Detecta rollover de run-log (nuevo ciclo del cron) con un evento `status` de frontera.
  - AC2 READ-ONLY: el bridge solo lee observeRunsDir + escribe su propio audit .runtime/architect-bridge/; snapshot
    byte-a-byte de Area_comun/state/TASK_INDEX.json, runtime/state/events.jsonl y del run-log ANTES/DESPUES de
    attach+stream = identicos. Cero ruta de escritura a estado gobernado.
  - AC3 CONTROL DESHABILITADO (I1): endpoint /send responde 403 "observation-only"; cero eventos `input`; la UI no
    tiene compose (textarea/boton Enviar removidos). El launcher deja de forwardear stdin.
  - AC4 ANTI-SEGUNDO-ARQUITECTO (I3): el manager NO contiene `spawn(`; con pid de cron no-vivo, /open degrada a
    `dormant`/no-live-session (nunca spawnea). Direccion fail-safe: mal-"vivo" solo tailea un log viejo (inocuo).
  - AC5 PII: vector de PII (email/telefono/NIT/doc/cuenta/direccion) inyectado en el run-log -> [*-REDACTED] en SSE
    y audit; ausencia de los literales (reusa el vector de TASK-0187).
  - AC6 CONTRATO + gates: la lista de 5 endpoints del bridge se mantiene (staticContract); node --test verde;
    tests de spawn (TASK-0185/0188) reescritos a tail.
- verification_cmd:
  - cd D:/Agentes/Zeus/Zeus-protocol && node --test
  - (checker en clon limpio de Zeus-protocol; fuente observeRunsDir por env, sin path hardcode)
- scope_routes (en Zeus-protocol):
  - src/server.js (createArchitectBridgeManager: quitar spawn/open->attach/send->403/stop->detach + tailRunLog + dualSessionGuard)
  - scripts/architect-runtime-launcher.mjs (quitar forward de stdin; sacarlo del path del bridge)
  - public/app.js (createArchitectConsoleController/renderArchitectConsoleView: quitar compose; renombrar a Observar)
  - architect-bridge.config.json (quitar command/args; anadir mode:observe/observeRunsDir/cronPidPath/cronLockPath)
  - tests/staticContract.test.js (reescribir 0185/0188 spawn->tail; nuevos tests read-only/control-inerte/dual-session)
- out_of_scope:
  - Opcion (b) transcript-sink para el modo INTERACTIVO -- fast-follow, FUERA de esta unidad (E1 del Plan).
  - Reescritura a React+TS+Vite -- FUERA (se construye sobre el vanilla existente).
  - Tocar el ledger/estado gobernado del hub -- el bridge es READ-ONLY.
  - protocol.config.json pineado del hub (2E35F26E) -- fondo intocable.
- risk: medium (toca el bridge existente + tests; pero read-only y sin spawn reduce el riesgo de invariante).
- estimate: M

## Riesgos declarados (del Plan, para el checker)
- E1: la fuente (a) solo observa al Arquitecto en modo CRON; el modo interactivo queda sin sink (fast-follow b).
  El panel muestra honestamente "sin sesion viva" si el cron no corre. DECLARADO, no es un defecto.
- Liveness "en vivo" = segun se vacia el buffer de Start-Process -RedirectStandardOutput (no keystroke-level).
- Rollover: carrera si un ciclo del cron arranca entre polls (se puede perder el borde inicial de un ciclo).
- PII best-effort (regex); mitigacion = operatorPresentRequired + localhost.
- Decision menor: launcher NEUTRALIZAR (quitar stdin-forward) vs RETIRAR (rompe tests 0188/README). Recomiendo
  NEUTRALIZAR (delta menor) + reescribir los tests de spawn.

## Cross-atestacion (cierre, DECISION-0095)
Deliverable en Zeus-protocol; al cerrar, anclar la entrada de cross-atest al hub por blob de git (como 0185/0188).
Confirmar con el Operador/patron previo el mecanismo exacto de cross-atest al ratificar.
