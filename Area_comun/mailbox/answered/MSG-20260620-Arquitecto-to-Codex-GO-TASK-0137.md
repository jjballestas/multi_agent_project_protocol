---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0137
task_id: TASK-0137
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0137 (ready, maker=Codex): vista Help (RF-14/UX). Nav item Help + routing 1:1 (AC12); guia navegable de metodologia+consola con fuente UNICA docs/MANUAL-operador.md (reusar, no duplicar); honesta (no documenta lo inexistente, AC11); READ-ONLY (sin superficie de escritura, AC17); conforme design-system (AC13). Ratificado por el Operador: ext4 SPEC-0086 (AC23 PERMANENTE). Codigo en Zeus-protocol; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0137-codex-front-help-view.md
  - Area_comun/tasks/req-fb27af72-requirement-seed.md
  - D:/Agentes/Zeus/Zeus-protocol/docs/MANUAL-operador.md
deadline_or_blocking_level: normal
---

# GO - TASK-0137 vista Help (RF-14, AC23)

Ratificado por el Operador (REQ-FB27AF72 -> ext4 SPEC-0086, AC23 PERMANENTE). maker=Codex / checker=Arquitecto.
Codigo en Zeus-protocol. UX READ-ONLY: NO nueva superficie de escritura.

OJO: el TITULO de la semilla viene mangleado ("arrancamos con nova.budget:") por el bug de campos-stale que ya
arreglo TASK-0135; el intent REAL esta en la NARRATIVA del seed (Help navegable de metodologia + consola).

## Alcance
1. Nav item Help + panel; "help" en NAV_VIEWS (routing 1:1, AC12). Activar Help -> SOLO su panel; vista
   desconocida -> fallback.
2. Guia DETALLADA y NAVEGABLE (secciones + indice/glosario): consola; observar vs operar; submit_intent
   escritor-unico; dry_run vs execute/confirmacion; atestacion #4; las vistas; intake RF-14; pipeline SDD;
   glosario.
3. Fuente UNICA = docs/MANUAL-operador.md (reusar, NO duplicar; implementacion a tu eleccion: servir el manual
   read-only y renderizarlo, o incluirlo en build desde ese unico archivo).
4. Honestidad (AC11): refleja lo que la app HACE hoy incl. limitaciones; lo no implementado se marca
   pendiente/fuera-de-alcance, no se afirma activo.
5. Read-only: sin botones de accion, sin llamadas a /actions/submit; conforme al design-system (AC13).

## Condicion de cierre
- AC23 verde como tests de COMPORTAMIENTO permanentes (routing "help" solo-su-panel + fallback; contenido
  derivado del manual = no placeholder, cubre secciones clave/glosario; no-bypass = sin superficie de escritura).
- Carry AC11/AC12/AC13/AC17 verdes.
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad limpia.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

Entrega handoff autocontenido al pasar a in_review; libera tu claim al moverla. Canal ASCII.
