---
message_id: MSG-20260624-Arquitecto-to-Codex-GO-TASK-0165
task_id: TASK-0165
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0165 (ready): panel Operar-Agentes Q2 = consola/compositor de prompts agente-a-agente en Zeus-protocol (SPEC-0088 AC1-AC6). AC1 vista con combo de agente (del agent_registry) + caja de prompt + Enviar. AC2 Enviar = accion gobernada SERVER-SIDE mailbox_send: el server compone un MSG mailbox (from:Operador, relayed_by:Arquitecto, to:<agente>, type:DIRECTIVE/QUESTION, operator_directive:true, cuerpo=prompt) y lo escribe+commit+push (auto-commit-push AC58); NO segundo escritor (AC17); el front NO escribe el archivo directo. AC3 PII+ASCII en el prompt (AC16). AC4 vista de HILO read-only: lee mailbox open+archived filtrado por el agente, muestra prompt+respuestas en orden. AC5 estado de envio + error amable AC72. AC6 off-by-default, #4 byte-id, despertar runtime=Q1 fuera de alcance. El claim del MSG usa grano fino (CLAIMS.json#<id>, ya en el nucleo). maker=Codex/checker=Arquitecto+Analista. NUNCA pilotar contra el log vivo (clon desechable)."
requested_action: "Reclama TASK-0165 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. AC1: vista/panel 'Operar Agentes' (o seccion) con combo de agente poblado del agent_registry real (Arquitecto/Codex/Analista + workers) + caja de prompt + boton Enviar (deshabilitado sin agente). AC2: implementa una ACCION GOBERNADA server-side mailbox_send (analoga a requirement-intake): el server recibe {agente, prompt}, compone el MSG mailbox bien formado (from:Operador, relayed_by:Arquitecto, to:<agente>, type:DIRECTIVE, status:open, operator_directive:true, one_line_summary + cuerpo=prompt redactado), lo escribe en Area_comun/mailbox/open/ del PROTOCOLO y hace commit+push (reusa commitAndPushSubmitIntentOutputs/auto-commit-push); el front llama esa accion, NO escribe el archivo directo; carry AC17 no-bypass (no toca submit_intent-state ni capabilities). AC3: cuerpo ASCII + redaccion PII en el plano publicable + aviso. AC4: vista de hilo read-only que lee el mailbox (open+archived) filtrado por to/from=<agente> (via el lector canonico read-only existente) y muestra el hilo en orden con PII redactada. AC5: indicador enviando + exito (refresca el hilo) o error amable AC72 (ledger-busy -> 'Canal ocupado, intente mas tarde'). AC6: off-by-default; #4 byte-id (protocol.config.json sin tocar). Behavior-tests deterministas por AC. Manten verde: node --test clon limpio (EXIT explicito), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. REPRO: seleccionar Codex + prompt + Enviar -> MSG mailbox to:Codex operator_directive; el hilo lo muestra. Entrega in_review."
context_refs:
  - Area_comun/specs/SPEC-0088-panel-operar-agentes-q2-consola-prompts.md
  - Area_comun/tasks/TASK-0165-codex-panel-operar-agentes-q2-consola-prompts.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: normal
---

# GO - TASK-0165: panel Operar-Agentes Q2 consola de prompts (SPEC-0088)

Primera pieza del panel. Consola de prompts agente-a-agente: combo de agente + caja de prompt -> accion gobernada
server-side mailbox_send (compone el MSG mailbox + commit+push, NO bypass) + vista de hilo read-only (lee el mailbox
filtrado por agente). PII/ASCII + error amable. Detalle en SPEC-0088 AC1-AC6. maker=Codex / checker=Arquitecto +
Analista. #4 byte-id; clon desechable.
