---
task_id: TASK-0165
title: "Proyecto-front: Panel Operar-Agentes Q2 -- consola/compositor de prompts agente-a-agente (accion gobernada mailbox_send + vista de hilo) (SPEC-0088, AC1-AC6)"
type: product
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0088
created_at: 2026-06-24
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
origin_reqs: [REQ-269EBF78, REQ-68896287BC, REQ-A54DAD73, REQ-E782911A]
file: Area_comun/tasks/TASK-0165-codex-panel-operar-agentes-q2-consola-prompts.md
---

# TASK-0165 - Panel Operar-Agentes Q2: consola de prompts (SPEC-0088)

> Primera pieza del panel "Operar Agentes". Aprobada por el operador (REQ-269EBF78 + duplicado REQ-68896287BC; los
> REQ-A54DAD73 "accion gobernada mailbox_send" y REQ-E782911A "compositor desde el Mailbox" AFINAN el mecanismo y se
> integran aqui). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (PII/no-bypass). #4 byte-id; ASCII-only.

## Alcance (SPEC-0088 AC1-AC6)
- **AC1** Vista/panel "Operar Agentes" con COMBO de agente (del agent_registry: Arquitecto/Codex/Analista + workers
  registrados) + caja de prompt + boton Enviar. Combo poblado del registro real.
- **AC2** Enviar = **accion gobernada `mailbox_send`**: compone un MSG mailbox (`from: Operador`, `relayed_by:
  Arquitecto`, `to: <agente>`, `type: DIRECTIVE`/QUESTION, `operator_directive: true`, cuerpo=prompt) por el camino
  gobernado del front (auto-commit-push AC58). NO segundo escritor (AC17); el prompt NO concede autoridad nueva al
  agente. Implementala como una accion gobernada server-side (analoga a requirement-intake): el server compone el
  MSG y lo escribe+commitea+pushea; el front no escribe el archivo directo.
- **AC3** Guarda PII + ASCII en el prompt (carry AC16): cuerpo ASCII, texto libre redactado en el plano publicable,
  aviso al operador.
- **AC4** Vista de HILO read-only: lee el mailbox (open + archived) filtrado por el agente seleccionado y muestra el
  hilo (prompt del operador + respuestas del agente) en orden, via el lector canonico read-only existente.
- **AC5** Estado de envio claro: "enviando" + exito (aparece en el hilo) o error AMABLE (carry AC72 "Canal ocupado,
  intente mas tarde").
- **AC6** Off-by-default / sin riesgo: solo escribe el MSG gobernado + lee el canonico; #4 byte-id (no toca
  protocol.config.json); despertar el runtime del agente = Q1 (fuera de alcance).

## DoD
- AC1-AC6 verdes con behavior-tests deterministas; carry AC16/AC17/AC58/AC72. node --test clon limpio exit 0;
  validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica.
- La accion mailbox_send: el MSG generado es ASCII, file-scoped (DECISION-0042), con la marca operator_directive;
  el claim del MSG usa grano fino (CLAIMS.json#<id>, DECISION-0059) y no bloquea a otros.
- Reproducido por el checker DESDE CLON LIMPIO; maker!=checker. PASADA DEL ANALISTA (PII + no-bypass + que el prompt
  no concede autoridad).
- REPRO: en el front, seleccionar Codex, escribir prompt, Enviar -> MSG mailbox to:Codex operator_directive; el hilo
  lo muestra; (Codex vivo) responde y la respuesta aparece en el hilo.

## Notas
- mailbox_send NO es un nuevo intent de submit_intent-state (no es estado del ledger); es un MSG mailbox gobernado
  (commit+push), como los handoffs. Si el server ya tiene un patron de accion gobernada (buildAction...), cuelga
  mailbox_send de ahi con su validacion propia.
- Un prompt del operador a Codex que pida "implementar X" deberia idealmente derivar al flujo SDD (GO/tarea), no a
  codigo directo; eso lo decide el agente segun sus reglas (operator_directive no salta gobernanza).
- NUNCA pilotar contra el log vivo: clon desechable para el repro del write gobernado.
