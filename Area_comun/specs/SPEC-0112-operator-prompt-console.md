---
spec_id: SPEC-0112
title: Consola de prompt operador->agente en el front (Alcance A / P1 de TASK-0178) -- compose de MSG gobernado + vista de hilo, off-by-default
status: ready
owner: Codex
decision: DECISION-0106
relates_to: [DECISION-0106, DECISION-0051, DECISION-0052, DECISION-0054, TASK-0178, REQ-ZEUS-001]
project: Zeus-protocol
date: 2026-08-02
file: Area_comun/specs/SPEC-0112-operator-prompt-console.md
---

# SPEC-0112 -- Consola de prompt operador->agente (front Zeus-protocol)

Operacionaliza DECISION-0106 (ratificada 2026-08-02): expone el mailbox gobernado como una consola de prompt en
el panel, para que el operador hable con los agentes (Arquitecto/Codex/Analista) y vea sus respuestas SIN VS Code.
Repo de producto: `D:\Agentes\Zeus\Zeus-protocol`. Gobernanza en el hub. **Off-by-default.** Core neutral (sin
cambios en el hub/#4).

## Alcance (P1 de TASK-0178)
DOS piezas: (a) COMPOSE (escritura acotada) de un MSG gobernado operador->agente; (b) VISTA DE HILO (lectura) del
mailbox por agente. NO incluye lanzar/detener runtimes (Alcance B), supervisor (C), ni alta de agentes (P4).

## Arquitectura (heredada de DECISION-0051/0052/0054)
- **Builder SERVER-SIDE, forma estricta:** el endpoint recibe SOLO campos de datos validados (destinatario,
  cuerpo, y opcionalmente requires_response). El SERVIDOR construye el MSG-*.md canonico. El cliente NUNCA envia
  el MSG crudo ni el `actor`/`from`/`relayed_by`. Reusa el patron `governed-action` (dry_run preview + execute
  confirmado), NO un segundo escritor.
- **Persistencia gobernada:** el MSG se escribe a `Area_comun/mailbox/open/` y se commitea+pushea al canal
  gobernado (patron auto-commit-push de DECISION-0054) para que el cron del agente destino lo procese. Off-by-default.

## Criterios de aceptacion
- **AC1 (UI consola):** en el front hay una consola con (i) selector de agente destino (Arquitecto/Codex/Analista),
  (ii) area de texto para el prompt, (iii) preview (dry_run) del MSG canonico que se compondria, (iv) boton de envio
  con confirmacion explicita (`confirm:*`, patron 0051; sin confirm -> 409, no escribe: prueba negativa). Toda la
  capacidad esta detras de un flag OFF-BY-DEFAULT en un registro FUERA del config pinned.
- **AC2 (compose server-side):** al confirmar, el SERVIDOR construye un MSG-*.md canonico en
  `Area_comun/mailbox/open/` con frontmatter valido: `id`, `from: Operador`, `to: <agente>`, `type` reconocido por
  el cron del destino (p.ej. REQUEST/QUESTION), `status: open`, `created` (hora real), `operator_directive: true`,
  y (si el operador lo pide) `requires_response: true` + `response_owner: <agente>` + `requested_action`/`question`.
  El cuerpo es el prompt del operador. El cliente NO inyecta el MSG ni el actor.
- **AC3 (anti-impersonacion -- prueba negativa PERMANENTE):** cualquier intento por esta via de (a) fijar
  `from`/`actor`/`relayed_by` desde el cliente, o (b) enviar una forma distinta al operator-agent-message (otro
  kind/intent, un MSG a un no-agente, campos crudos) -> RECHAZADO (test negativo permanente, patron 0052). El
  servidor jamas confia en el cliente para autoria ni forma.
- **AC4 (atribucion + persistencia honesta):** el MSG lleva `from: Operador`; al commitear/pushear (auto), el
  commit/registro refleja `relayed_by: <firmante del front>` + `endorsement: none` (origen+transporte, NO aval).
  El MSG compuesto pasa `validate_collaboration_state.py` (forma de mailbox valida: requires_response => response_owner)
  y `scan_encoding.py` (ASCII) -> exit 0.
- **AC5 (guarda PII/ASCII, hereda 0051/0040):** el compose separa intencion-llano del payload sensible, redacta/
  marca el texto libre en el plano publicable, fuerza ASCII a lo que se escribe al protocolo, y ADVIERTE al operador
  en compose y confirm. No levanta DEF-PII.
- **AC6 (vista de hilo, read-only):** la consola LEE el mailbox (open + archived) filtrado por el agente
  seleccionado y muestra, en orden, los prompts del operador + las respuestas del agente. Solo lectura; sin nueva
  superficie de escritura. Refresco/estado de frescura coherente con el resto del panel.
- **AC7 (fondo intocable + gates):** #4 del hub byte-identico (drift 0 necesario, no suficiente); sin cambios en
  el core/protocolo (codigo solo en Zeus-protocol); `npm test` del repo Zeus-protocol exit 0 en clon limpio; la
  capacidad OFF-by-default no se activa sola (prueba: con el flag off, no hay compose ni endpoint activo).

## Alcance de archivos (Zeus-protocol)
- IN: server (endpoint + builder server-side + auto-commit-push del MSG), public (UI consola + vista de hilo),
  registro del flag off-by-default (fuera del config pinned), tests (contrato estatico + prueba negativa de
  anti-impersonacion + off-by-default).
- OUT: lanzar/detener runtimes; supervisor; alta de agentes; cambios en el hub/protocolo/#4; nuevo INTENT_TYPES.

## Test plan
- Prueba negativa AC1: sin `confirm` -> 409, no escribe. AC3: forma-ajena / actor forjado / no-agente -> RECHAZADO.
  Off-by-default: flag off -> capacidad inerte.
- Prueba positiva: compose valido -> MSG canonico en open/ que pasa validate + scan_encoding; vista de hilo
  muestra prompt + respuesta (fixture de mailbox).
- #4 byte-identico antes/despues (hub intacto). npm test exit 0 en clon limpio.

## DoD
Cumple AC1-AC7; off-by-default; anti-impersonacion probada (negativa permanente); #4 intacto; core neutral; gate
maker != checker (Analista + Arquitecto): verificar el builder server-side, la prueba negativa de impersonacion, la
persistencia gobernada y (si hay browser) el render de la consola; sin browser, verificar por contrato + fixtures.
Cierre gobernado.
