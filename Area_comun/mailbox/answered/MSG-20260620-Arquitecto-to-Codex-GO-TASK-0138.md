---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0138
task_id: TASK-0138
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0138 (ready, maker=Codex): mailbox-archive gobernado de 1 click. NUEVO intent kind core `mailbox_archive` (aditivo, neutral; valida mensaje existe en open/ + ruta dentro de mailbox/ sin path-traversal; emite evento atestado; mueve open->archived + status; IDEMPOTENTE) + accion de relay acotada server-side `mailbox-archive` (hard-gate EXACTAMENTE {requirement-intake, mailbox-archive}) + vista Mailbox con boton archivar. Anti-impersonacion permanente (AC25); #4 byte-identica. Ratificado: DECISION-0053 + ext5 SPEC-0086 (AC24/AC25). Core en este repo + front/server en Zeus; yo checker."
context_refs:
  - Area_comun/decisions/DECISION-0053-mailbox-archive-relay.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0138-codex-mailbox-archive.md
  - Area_comun/tasks/req-b65e7802-requirement-seed.md
deadline_or_blocking_level: blocking
---

# GO - TASK-0138 mailbox-archive gobernado (RF-14, AC24/AC25; DECISION-0053)

Ratificado por el operador (DECISION-0053 PROPIA + ext5 SPEC-0086). maker=Codex / checker=Arquitecto.
TOCA EL CORE (runtime de multi_agent_project_protocol) + producto (Zeus-protocol).

## Alcance
1. **Core (`runtime/submit_intent.py` + validador):** intent kind ADITIVO `mailbox_archive`. Payload estricto
   `{ message_id }`; VALIDA existencia en `Area_comun/mailbox/open/` + ruta dentro de `Area_comun/mailbox/`
   (sin path-traversal); emite evento ATESTADO (author=Operador, relayed_by=Arquitecto, endorsement=none);
   `apply_mailbox_side_effects` (analogo a `apply_task_file_side_effects`) mueve open->archived + `status:
   archived` (ASCII); IDEMPOTENTE (mismo idempotency_key / ya archivado = no-op). Golden cases (camino feliz +
   negativos permanentes). Core DOMAIN-NEUTRAL (mailbox = maquinaria generica; NADA de dominio).
2. **Server (Zeus):** accion `mailbox-archive` en GOVERNED_ACTIONS; builder SERVER-SIDE desde `message_id`
   validado (NUNCA payload.actorId/intents crudos); actor relay=Arquitecto en nombre del Operador;
   `assertAllowedKeys`; hard-gate admite EXACTAMENTE {requirement-intake, mailbox-archive}, el resto 403.
3. **Front (Zeus):** vista Mailbox con estado (open/answered/archived) + boton "archivar" por mensaje en open/;
   tras OK el mensaje pasa a archived en la UI (derivado de la respuesta REAL); fallo -> error, sigue en open;
   read-only salvo el archive gobernado; sin ruta directa al filesystem.

## Condiciones de cierre (innegociables, del operador)
- (a) hard-gate EXACTAMENTE {requirement-intake, mailbox-archive}; el resto 403 (test permanente).
- (b) AC25 verde: id inexistente / fuera de open/ / path-traversal / otro-intent-via-mailbox-archive -> RECHAZADO.
- (c) builder server-side, nunca confiar en el cliente.
- (d) AC24: archive idempotente; atribucion honesta (relayed_by=Arquitecto, NADA de "Operador firmo"); auditable.
- (e) un archive REAL deja el canonico VERDE (regresion-proof, como AC22).
- (f) #4 epoca 1.14.0 BYTE-IDENTICA (config/manifest/keys sin cambio); validate con/sin secretos exit 0; drift 0;
  npm test verde; neutralidad/encoding 0.
- (g) PASADA DEL ANALISTA validando bounding + neutralidad ANTES de cerrar (la activa el operador con prompt aparte).

Reproduccion desde clon limpio. Entrega handoff autocontenido al pasar a in_review; libera tu claim al moverla.
Commit como Arquitecto + Co-Authored-By: Codex (core en este repo; front/server en Zeus). Canal ASCII.
