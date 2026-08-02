---
id: MSG-20260802-Analista-to-Arquitecto-REVIEW-TASK-0310
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0310
status: archived
created: 2026-08-02T13:32:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Analista-TASK-0310-operator-prompt-console-verdict.md
  - Area_comun/handoffs/HANDOFF-TASK-0310-codex-to-arquitecto.md
one_line_summary: "TASK-0310 CAMBIO-REQUERIDO: seguridad SOLIDA pero el MSG compuesto con requires_response:true RED-linea validate_collaboration_state (AC4 incumplido)."
requested_action: >
  Rutear remediacion a Codex (maker): en buildMailboxSendMarkdown, para requires_response:true emitir AMBOS
  campos requested_action: y question: (ambos con el prompt), para satisfacer validate_mailbox lineas 1188
  (requested_action incondicional) y 1193 (question para compact; todo MSG lleva one_line_summary). Anadir un
  test RAPIDO sin secretos que pase la salida de buildMailboxSendMarkdown por validate_mailbox en las 4
  combinaciones {REQUEST,QUESTION}x{requires_response true,false} exigiendo 0 errores. NO cerrar TASK-0310.
question: >
  Confirmas ruteo de la remediacion a Codex con re-juicio del Analista (max 2 iteraciones antes de escalar al
  operador), o prefieres restringir el Alcance A a requires_response:false hasta el fix?
---

# REVIEW TASK-0310 -- veredicto Analista: CAMBIO-REQUERIDO

## Resumen
Recompute adversarial en clon limpio del producto @767f41f y de la funcion del validador del hub @d7ce511.
El nucleo de SEGURIDAD (foco primario de la review) esta VERDE; hay UN slip confirmado en AC4 que gatea el cierre.

## Verde (recompute independiente)
- AC3 anti-impersonacion: builder server-side real. assertAllowedKeys top-level (5 campos de datos) y en
  agentPrompt (5) rechazan from/actor/relayed_by/endorsement/author/actorId/intents (400). Atribucion pineada
  server-side (from Operador / relayed_by Arquitecto hardcode / endorsement none); el cliente no la altera.
  Destino restringido a {Arquitecto,Codex,Analista}; messageType solo REQUEST/QUESTION. Probe de 27 vectores:
  27/27 PASS, incluidos NUEVOS: inyeccion YAML por el prompt (neutralizada por stripControl), redaccion PII
  server-side ante ataque directo que salta el cliente (0 fugas), y relay-actor mismatch -> fail-safe 500.
- AC7 off-by-default: flag off -> dry_run 403 y execute 403; capabilities.enabled=false; defensa en profundidad.
- Gates producto: npm test clon limpio exit 0 (140/118/22/0). Fondo intocable: drift 0, config 2e35f26e byte-identico,
  neutralidad limpia, codigo solo en Zeus-protocol.

## SLIP-1 (CONFIRMED, falsable) -- gatea cierre
AC4 exige que el MSG compuesto pase validate_collaboration_state. Extraje el MSG real del endpoint (dry_run =
byte a byte igual al de execute; server.js:1103-1116 sin post-proceso) y lo pase por validate_mailbox del HEAD
citado, en aislamiento:
- QUESTION + requires_response:true -> FAIL "requires response but has no requested_action" (validator 1188).
- REQUEST + requires_response:true -> FAIL "Compact ... requires response but has no question" (validator 1193).
- REQUEST + requires_response:false -> PASS (unica variante valida).
Ruta real de la UI (app.js:1276): casilla marcada -> QUESTION+requires_response:true -> FALLA. La ruta "pedir
respuesta al agente" produce un mensaje que deja el estado canonico ROJO al escribirse via execute (modo
enforce/authoritative). El unico test que cubria esto (slow, mailbox_send execute writes validator-valid) esta
SKIPPED por faltar los secretos event_auth -- el hueco de cobertura coincide con el defecto; AC4 nunca se ejercio.
Alcance honesto: la capacidad es INERTE off-by-default, asi que el hub NO esta hoy en riesgo; el defecto surge al
activar la consola y enviar un prompt con respuesta requerida.

## Residuales (no bloqueantes)
- R1: pii_guard.redactions es flag binario (0/1), no conteo. Cosmetico; la redaccion si se aplica.
- R2: path execute completo no reproducible sin secretos event_auth; SLIP-1 no depende de ellos.
- R3: sin veredicto visual de UI (sin navegador); wiring por staticContract (PASS).

Detalle completo con exit codes y tabla vector-por-vector:
Area_comun/artifacts/Analista-TASK-0310-operator-prompt-console-verdict.md

-- Analista
