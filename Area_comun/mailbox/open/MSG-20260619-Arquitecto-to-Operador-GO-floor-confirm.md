---
message_id: MSG-20260619-Arquitecto-to-Operador-GO-floor-confirm
type: RESPONSE
task_id: none
from: Arquitecto
to: Operador
requires_response: false
response_owner: Operador
status: open
one_line_summary: Confirmo el alcance del FLOOR (Fase2 Git+CI via tool_policy deny-by-default; Fase1 registro+digestion skills + 3 skills neutrales; off-by-default; sin Fase4; sin DB-live hasta T0; sin tocar #4) y arranco de a una pieza por SDD. Pieza 1 Git connector promovida + GO a Codex. Monitoreo reactivado.
context_refs:
  - Area_comun/decisions/DECISION-0048-connectors-accion-tool-policy.md
  - Area_comun/specs/SPEC-0085-connector-git-readonly.md
  - MSG-20260619-Operador-to-Arquitecto-GO-floor-fase1-2
deadline_or_blocking_level: normal
---

# Confirmado: FLOOR pull-based, de a una pieza por SDD

Alcance confirmado tal cual: **Fase 2** connectors Git+CI sobre tool_policy deny-by-default (fixtures, sin
uso vivo sin s9+GO, registro fuera del config pinned); **Fase 1** mecanismo de skills (registro+digestion
fuera del config) + 3 skills neutrales (convenciones DDL, regla-de-negocio-vs-legacy, verificacion de
migracion) como artefactos de instancia (contenido del proyecto al perfil, no al core). **NO Fase 4**, **NO
uso vivo** de connectors (s9+GO), **NO tocar #4** (epoca 1.14.0, DECISION-0047), **una pieza a la vez**.

## Orden y roles
Git -> CI -> registro+digestion skills -> 3 skills. SDD por pieza (DECISION->SPEC con AC+test_plan->golden),
**maker=Codex / checker=Arquitecto** (yo diseno + reproduzco; Codex implementa), off-by-default, cada una
verde en clon limpio (validate exit 0 con y SIN secretos, DECISION-0046) antes de la siguiente. Reporto al
cerrar cada pieza.

## Pieza 1 - EN MARCHA
- **DECISION-0048** (connectors de accion gobernados por tool_policy, deny-by-default, allowlist de
  inspeccion, no conceden autoridad; extiende DECISION-0044) + **SPEC-0085** (Git inspeccion) + **TASK-0123**
  (ready/Codex) promovidos al canonico (drift 0, sin tocar config/genesis).
- **GO a Codex** para TASK-0123 (Git connector inspeccion deny-by-default + golden fixtures). Maker Codex,
  checker yo.
- Para que el maker!=checker corra, necesito a **Codex activo** para el floor; si no lo esta, avisame y lo
  encolo igual (el GO ya esta en el buzon).

## Recordatorios en pie
Connector DB-live + perfil financiero = T0/post-T0 (s9+GO). PII de terceros nunca al event log
(DECISION-0040); DEF-PII (TASK-0118) diferida. Una sola ventana de riesgo. Monitoreo reactivado.
