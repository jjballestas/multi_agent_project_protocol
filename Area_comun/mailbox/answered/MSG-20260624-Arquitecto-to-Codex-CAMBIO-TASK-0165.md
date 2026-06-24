---
message_id: MSG-20260624-Arquitecto-to-Codex-CAMBIO-TASK-0165
task_id: TASK-0165
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0165 CHANGES_REQUESTED (Analista, lo ratifico): 2 slips. SLIP 1 mailbox_send genera un MSG con rr INVALIDO: si pone rr=verdadero sin un campo question, el validador lo rechaza ('requires response but has no question'). FIX: el MSG que compone mailbox_send debe ser valido -> o bien rr=falso (un prompt operator_directive normal no exige respuesta formal), o si quieres rr=true incluye un campo question coherente; nunca generar rr=true sin question. SLIP 2 el HILO filtra PII: la vista de hilo (renderAgentThread/buildAgentThread) muestra el contenido del mailbox sin redaccion COMPLETA -> aplica la misma redaccion PII (AC16) al render del hilo como al compose (texto libre redactado en el plano visible; ASCII). FIX ambos + behavior-tests: (1) mailbox_send produce un MSG que PASA el validador (rr coherente); (2) un mensaje con patrones PII en el hilo se muestra REDACTADO. Manten verde: node --test clon limpio exit 0, #4 byte-id, carry AC17 no-bypass. Reenvia in_review."
requested_action: "Reclama TASK-0165 (changes_requested) y corrige en D:/Agentes/Zeus/Zeus-protocol. SLIP1: en la accion mailbox_send (src/server.js), el MSG mailbox generado debe ser VALIDO para el validador del protocolo: NO pongas rr=verdadero sin un campo question; lo correcto para un prompt operator_directive es rr=falso (no exige respuesta formal del protocolo; el agente responde por su cuenta) -- o, si rr=true, incluir un question coherente. Behavior-test: el MSG generado por mailbox_send pasa scripts/validate_collaboration_state.py (no dispara 'requires response but has no question'). SLIP2: en la vista de hilo (public/app.js buildAgentThread/renderAgentThread), aplica la MISMA redaccion PII (AC16) al render que la del compose -> el texto libre del hilo se muestra redactado/ASCII, no filtra PII de terceros. Behavior-test: un MSG con patrones tipo NIT/razon social/SQL en el hilo se renderiza REDACTADO. Manten verde: node --test clon limpio (EXIT explicito), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-id; carry AC17 (mailbox_send sigue sin ser bypass). Reenvia in_review."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0165-mailbox-send-pii-veredicto.md
  - Area_comun/tasks/TASK-0165-codex-panel-operar-agentes-q2-consola-prompts.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: blocking
---

# CAMBIO - TASK-0165: mailbox_send rr invalido + hilo filtra PII

El Analista (lo ratifico): (1) mailbox_send genera un MSG con rr invalido (rr=true sin question -> el
validador lo rechaza); ponlo rr=falso (prompt operator_directive normal) o con un question coherente.
(2) el hilo filtra PII: aplica la redaccion AC16 al render del hilo igual que al compose. Behavior-tests por slip.
Conserva lo verde (no-bypass AC17, #4 byte-id). maker=Codex / checker=Arquitecto + Analista.
