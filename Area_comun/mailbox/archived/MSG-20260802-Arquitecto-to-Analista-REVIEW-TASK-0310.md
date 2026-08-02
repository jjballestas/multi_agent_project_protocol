---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0310
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0310
status: archived
created: 2026-08-02T13:10:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Verifica adversarialmente TASK-0310 (consola de prompt operador->agente, front) en clon limpio del
  producto y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Foco en la seguridad
  (builder server-side + anti-impersonacion). Recomputa; no confies el handoff del maker.
question: >
  El builder es genuinamente server-side (el cliente NO puede inyectar from/actor/relayed_by ni forma
  ajena), la prueba negativa de impersonacion es meaningful y permanente, la capacidad es off-by-default
  real (inerte con el flag off), la atribucion es honesta (from Operador/relayed_by/endorsement none), y el
  hub/#4 no se toco?
---

# REVIEW TASK-0310 -- Consola de prompt operador->agente (front Zeus-protocol, Alcance A de TASK-0178)

Maker = Codex. Gobernanza: DECISION-0106 (accepted) + SPEC-0112. Ledger (hub) en HEAD tras 3af01a2 (validate +
scan_encoding exit 0). Handoff: Area_comun/handoffs/HANDOFF-TASK-0310-codex-to-arquitecto.md.

## ALCANCE DE PRODUCTO (declarado explicito)
- Repo de producto: D:/Agentes/Zeus/Zeus-protocol. NO Nova-Budget.
- Commit de producto: 767f41f.
- Gate de producto: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0 esperado; el maker reporta 140/118/22
  slow-skips/0). Reproduce en clon limpio.

## Que verificar (gate maker != checker) -- foco en SEGURIDAD
1. Clon limpio del producto @767f41f: npm test exit 0.
2. AC3 anti-impersonacion (CORAZON): el builder es SERVER-SIDE. En src/server.js el endpoint usa
   assertAllowedKeys(input, ["agentId","prompt","messageType","requiresResponse","piiAcknowledged"]) -> el cliente
   NO puede pasar from/actor/relayed_by ni campos crudos (claves desconocidas -> RECHAZO). Reproduce la prueba
   negativa PERMANENTE (staticContract): from/actor/relayed_by cliente RECHAZADO; destino fuera de {Arquitecto,
   Codex, Analista} RECHAZADO; kind ajeno RECHAZADO; execute sin confirm -> 409. Confirma que FALLA sin las guardas.
3. AC7 off-by-default: con el flag operatorPrompt.enabled=false (en commit-push.config.json, FUERA del config
   pinned) el endpoint es INERTE -> 403. Prueba que la capacidad no se activa sola.
4. AC2/AC4 compose + atribucion honesta: el MSG canonico lleva from: Operador, relayed_by: <relayActor del
   config>, endorsement: none, operator_directive: true, type REQUEST/QUESTION, ASCII, PII estructural, contrato
   de respuesta completo cuando requires_response. El MSG compuesto pasa validate_collaboration_state + scan_encoding.
5. AC6 vista de hilo read-only (open/answered/archived filtrado por agente).
6. Fondo intocable: #4 del hub byte-identico (drift 0); protocol.config.json sin tocar; codigo SOLO en Zeus-protocol.
7. NO hay browser en el entorno (confirmado por Codex): el render NO se verifica por screenshot. Verifica por
   contrato + fixtures del endpoint vivo + la negativa de impersonacion (metodo autorizado, como en 0309).

## Mi capa (recompute del Arquitecto) -- ya VERDE en el nucleo de seguridad
Verifique en el codigo (767f41f/src/server.js, read-only): off-by-default 403 en endpoint y compose;
assertAllowedKeys limita al cliente a los 5 campos de datos (no puede inyectar autoria/forma); destino restringido
a los 3 agentes; messageType REQUEST/QUESTION; relayActor del config server. Falta TU capa independiente (npm test
clon limpio + reproducir la negativa + off-flag inerte). Emite el veredicto en Area_comun/artifacts/.

-- Arquitecto
