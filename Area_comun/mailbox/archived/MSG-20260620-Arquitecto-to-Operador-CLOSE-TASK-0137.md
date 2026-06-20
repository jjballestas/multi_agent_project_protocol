---
message_id: MSG-20260620-Arquitecto-to-Operador-CLOSE-TASK-0137
task_id: TASK-0137
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "CERRADA TASK-0137 (REQ-FB27AF72 vista Help) -> done. AC23 verde (routing 1:1 + fallback; manual fuente unica read-only; secciones/glosario cubiertos; sin superficie de escritura). maker=Codex/checker=Arquitecto. Sigue el #3 (REQ-B65E7802 mailbox-archive, toca el relay)."
context_refs:
  - Area_comun/tasks/TASK-0137-codex-front-help-view.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
deadline_or_blocking_level: normal
---

# CIERRE TASK-0137 - vista Help (RF-14, AC23)

Cerrada a `done` (checker=Arquitecto, maker=Codex, maker!=checker). Reproducida desde el codigo entregado.

## Verificacion (AC23 verde, test de comportamiento permanente)
- **Routing:** "help" en NAV_VIEWS; activar Help -> SOLO su panel visible (1 de N), resto hidden; vista
  desconocida -> fallback dashboard (hereda AC12).
- **Fuente unica:** el panel consume `GET /api/help/manual` (GET-only, `readFile` de path fijo
  `docs/MANUAL-operador.md`, read-only, sin path-traversal); NO duplica el texto. `helpCoverage(manual)` cubre
  consola, observar/operar, submit_intent, dry_run/execute, #4, vistas, intake RF-14, SDD y glosario.
- **No-bypass (AC17):** el panel Help no expone botones ni llamadas a `/actions/submit` (asertado por test).
- **Honestidad (AC11):** el contenido es el manual real (fuente de verdad), no afirma features inexistentes.
- **Diseno (AC13):** dark-first, tokens; la vista existe y navega.

## Gates
- Zeus `npm test` 24/24.
- Protocolo `validate` exit 0 CON y SIN secretos (clon limpio, DECISION-0046); drift 0.
- #4 epoca 1.14.0 BYTE-IDENTICA (config/manifest/keys sin cambio); UX read-only (sin nueva superficie de escritura).

Codigo en Zeus-protocol (commit como Arquitecto + Co-Authored-By: Codex; push de Zeus al remote sigue GATEADO
a tu accion). Canal ASCII.

## Siguiente
Sigo con el **#3 REQ-B65E7802** (higiene de mailbox con 1 click desde el front). OJO: **toca el RELAY** ->
extiende DECISION-0052 con una accion acotada "mailbox-archive" (builder server-side que emite open->archived
via submit_intent, NUNCA edita el mailbox directo, prueba negativa de impersonacion permanente). Evaluare si
basta extender 0052 o amerita DECISION propia, y te presento el draft para ratificacion.
