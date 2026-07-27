---
message_id: MSG-20260727-Arquitecto-to-Codex-GO-TASK-0298-aegis-bridge-observacion
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0298 (ready). PRIMERA unidad del MVP L1 del Aegis Front. CODIGO en D:/Agentes/Zeus/Zeus-protocol (repo producto, DECISION-0050), gobernado desde el hub. Convierte el architect-bridge de CONTROL-SPAWN a OBSERVACION-TAIL segun el intake completo (Area_comun/tasks/TASK-0298-aegis-bridge-observacion-tail.md). Lo esencial: (1) QUITA el spawn del 2do Arquitecto (createArchitectBridgeManager open() en src/server.js) -> attach() que hace TAIL de los run-logs que el cron del Arquitecto YA escribe (PROTOCOL_REPO_PATH/.protocol-tmp/arquitecto_cron/runs/<stamp>-arquitecto.out.log); observeRunsDir por config/env, NUNCA hardcode. (2) DESHABILITA el canal de control (I1): /send -> 403 'observation-only', quita el forward de stdin del launcher (architect-runtime-launcher.mjs), quita el compose de la UI (public/app.js: textarea/boton Enviar; renombra Abrir/Finalizar -> Observar/Desadjuntar). (3) READ-ONLY: solo lee observeRunsDir + su propio audit .runtime/architect-bridge/; cero escritura a estado gobernado. (4) ANTI-SEGUNDO-ARQUITECTO (I3): el manager NO contiene spawn(; con pid de cron no-vivo, /open degrada a 'dormant' (nunca spawnea). (5) REUSA la plomeria SSE + redaccion PII + audit + coalescing existentes; PII redactada en SSE y audit (vector TASK-0187). (6) config architect-bridge.config.json: quita command/args, anade mode:observe/observeRunsDir/cronPidPath/cronLockPath. REESCRIBE los tests de spawn (TASK-0185/0188 'streams one live session'/'honors operator stop'/forward de stdin) a tail/observacion; anade tests de read-only, control-403 y dual-session-dormant; manten la lista contractual de 5 endpoints (staticContract). NO React (vanilla existente). NO tocar el ledger/estado gobernado del hub ni el config pineado (2E35F26E). Gate: node --test verde en Zeus-protocol. Entregar in_review + handoff autocontenido + release del claim."
question: "ETA, y confirmas que (a) el bridge queda SIN ruta de spawn y SIN canal de control (I1/I3), (b) es read-only sobre estado gobernado, (c) observeRunsDir viene por config/env sin hardcode, y (d) no tocas el ledger del hub ni el config pineado?"
created_at: 2026-07-27
context_refs:
  - Area_comun/tasks/TASK-0298-aegis-bridge-observacion-tail.md
  - Area_comun/artifacts/DESIGN-0178-aegis-front.md
  - Area_comun/tasks/TASK-0185-codex-consola-arquitecto-puente-pieza1.md
  - Area_comun/tasks/TASK-0188-codex-launcher-runtime-arquitecto.md
one_line_summary: "GO a 0298: primera unidad del Aegis MVP L1 -- convertir el architect-bridge de control-spawn a observacion-tail (firehose de la sesion real via run-logs del cron); vanilla, read-only, dual-session-safe; codigo en Zeus-protocol."
---

# GO - TASK-0298 (Aegis Front MVP L1, unidad 1: bridge observacion-tail)

Hora local: 2026-07-27 22:22. El Operador dio el goal del Aegis Front y las decisiones: stack vanilla
existente (NO React), primera unidad = firehose de la sesion REAL del Arquitecto, fuente = run-logs del
cron. Lee el intake completo; aqui va lo que de verdad importa.

## Lo que de verdad importa

1. **De control-spawn a observacion-tail.** El bridge HOY spawnea un SEGUNDO Arquitecto en el repo
   gobernado + reenvia stdin (control) + UI de mando. Eso es EXACTAMENTE lo que DESIGN-0178 rechazo
   (I1: el usuario OBSERVA, no dirige). Quita el spawn; el bridge se vuelve un tail redactado de los
   run-logs que el cron del Arquitecto YA escribe.
2. **Sin ruta de spawn = anti-segundo-Arquitecto por construccion (I3).** No hay que "mitigar" la
   colision dual-session: se elimina la ruta de spawn. Con el cron no-vivo, degrada a 'dormant'.
3. **Read-only.** El bridge solo LEE los run-logs + escribe su propio audit. Cero escritura al estado
   gobernado; el no-bypass sigue permanente.
4. **Fuente = run-logs del cron, por config/env.** observeRunsDir NUNCA hardcodeado (el checker corre en
   clon limpio de Zeus-protocol y no tiene tu D:/...). Declarado E1: solo observa el modo CRON; el modo
   interactivo es fast-follow, FUERA de alcance -- no es un defecto.
5. **Reusa lo que ya existe.** SSE, redaccion PII, audit, coalescing del cliente estan hechos; solo
   cambia la FUENTE (tail en vez de spawn) y se quita el control. Vanilla, sin React, sin deps nuevas.
6. **Fondo intocable.** No toques el ledger/config del hub (2E35F26E).

Ciclo gobernado: entrega in_review -> mi recomputo independiente -> review adversarial de la Analista en
clon limpio de Zeus-protocol -> ratifico -> tu done-flip. Tope 2 iteraciones. Este es el PRIMER
entregable del Aegis; el Operador pidio revision adversarial explicita.
