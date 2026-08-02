---
task_id: TASK-0310
file: Area_comun/tasks/TASK-0310-consola-prompt-operador-front.md
title: "Front Zeus-protocol: consola de prompt operador->agente (compose de MSG gobernado + vista de hilo), off-by-default (SPEC-0112 / DECISION-0106)"
status: ready
type: product
owner: Codex
reviewer: Analista
priority: normal
project: Zeus-protocol
spec_id: SPEC-0112
relates_to:
  - DECISION-0106
  - SPEC-0112
  - TASK-0178
  - REQ-ZEUS-001
created_at: 2026-08-02
intake:
  type: feature
  goal: >
    Implementar el Alcance A (P1) de TASK-0178 en el front Zeus-protocol: una consola de prompt que expone el
    mailbox gobernado como canal de conversacion operador->agente (compose de un MSG-*.md gobernado + vista de
    hilo con respuestas), para hablar con Arquitecto/Codex/Analista sin VS Code. Superficie de escritura ACOTADA
    con builder server-side y anti-impersonacion (DECISION-0106, hereda 0051/0052/0054). OFF-BY-DEFAULT. Codigo
    solo en Zeus-protocol; el hub/#4 no se toca.
  acceptance:
    - "AC1 (UI + confirm): consola con selector de agente (Arquitecto/Codex/Analista) + textarea de prompt + preview dry_run del MSG canonico + envio con confirmacion explicita (confirm:*; sin confirm -> 409, prueba negativa). Todo detras de un flag OFF-BY-DEFAULT en un registro FUERA del config pinned."
    - "AC2 (compose server-side): al confirmar, el SERVIDOR construye el MSG-*.md canonico en Area_comun/mailbox/open/ (from: Operador, to: <agente>, type reconocido por el cron del destino, status: open, created hora real, operator_directive: true, requires_response + response_owner + requested_action/question si aplica; cuerpo = prompt). El cliente NO inyecta el MSG ni el actor."
    - "AC3 (anti-impersonacion, prueba negativa PERMANENTE): fijar from/actor/relayed_by desde el cliente, o enviar forma distinta al operator-agent-message (otro kind, MSG a un no-agente, campos crudos) -> RECHAZADO. El servidor nunca confia en el cliente para autoria ni forma (patron 0052)."
    - "AC4 (atribucion + persistencia): from: Operador; al auto-commit-push (patron 0054) relayed_by: <firmante front> + endorsement: none. El MSG compuesto pasa validate_collaboration_state.py + scan_encoding.py exit 0 (mailbox valido, ASCII)."
    - "AC5 (PII/ASCII, hereda 0051/0040): separa intencion-llano del payload sensible, redacta/marca texto libre en plano publicable, ASCII a lo que se escribe, ADVIERTE al operador en compose y confirm. No levanta DEF-PII."
    - "AC6 (vista de hilo read-only): lee el mailbox (open + archived) filtrado por agente y muestra prompts del operador + respuestas del agente en orden. Solo lectura."
    - "AC7 (fondo intocable + gates): #4 del hub byte-identico (drift 0); sin cambios en core/protocolo; npm test Zeus-protocol exit 0 en clon limpio; con flag off la capacidad es inerte (prueba)."
  verification_cmd:
    - "cd D:/Agentes/Zeus/Zeus-protocol && npm test"
  scope_routes:
    - src/server.js
    - public/app.js
    - public/index.html
    - public/styles.css
    - tests/staticContract.test.js
  out_of_scope: >
    Lanzar/detener runtimes desde el front (Alcance B); supervisor front-server (Alcance C); alta de agentes /
    enlace a LLM (P4/RF-9); cambios en el hub/protocolo/#4/genesis; nuevo INTENT_TYPES del runtime.
  risk: medium
  estimate: L
notes: >
  Alcance A (P1) de TASK-0178, gobernado por DECISION-0106 (ratificada por el operador 2026-08-02) + SPEC-0112.
  Repo de producto Zeus-protocol; gobernanza en el hub. Riesgo medio: NUEVA superficie de escritura -> el corazon
  de la seguridad es el builder server-side + la prueba negativa PERMANENTE de anti-impersonacion (patron 0052).
  Off-by-default. Gate maker != checker: Analista + Arquitecto verifican el builder server-side, la negativa de
  impersonacion, la persistencia gobernada honesta y (si hay browser) el render; sin browser, por contrato + fixtures.
---

# TASK-0310 - Consola de prompt operador->agente (front Zeus-protocol)

## Contexto
Alcance A de TASK-0178. DECISION-0106 (ratificada) habilita exponer el mailbox gobernado como consola de prompt.
Ver SPEC-0112 para arquitectura (builder server-side, anti-impersonacion) y AC completos.

## Entregable
- Front Zeus-protocol: UI consola (compose + confirm) + vista de hilo read-only + endpoint/builder server-side +
  persistencia gobernada (auto-commit-push del MSG) + flag off-by-default (fuera del config pinned) + tests
  (contrato + negativa de impersonacion + off-by-default).

## Seguridad (no negociable)
El builder es server-side con forma estricta; el cliente jamas inyecta el MSG crudo ni el actor. Prueba negativa
PERMANENTE: forma-ajena o actor forjado -> RECHAZADO (patron DECISION-0052). #4 del hub byte-identico.
