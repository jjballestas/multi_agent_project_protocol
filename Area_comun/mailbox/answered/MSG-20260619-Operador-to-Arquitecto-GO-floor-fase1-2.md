---
message_id: MSG-20260619-Operador-to-Arquitecto-GO-floor-fase1-2
type: DECISION
task_id: none
from: Operador
to: Arquitecto
requires_response: true
response_owner: Arquitecto
status: answered
one_line_summary: GO a construir el FLOOR de Fase 1 (Skills: registro+digestion) + Fase 2 (Connectors: Git + CI) en paralelo a que termino la DB. Jalado por necesidad real fechada = desarrollo de la app (front+Seguridad+Presupuesto, lanzamiento 2026-06-20). De a una pieza, DECISION->SPEC->golden, off-by-default, neutral. NO Fase 4 (auto-descubrimiento). DB-live connector queda para T0.
requested_action: "Construir el FLOOR minimo, una pieza a la vez (SDD: DECISION->SPEC->golden, maker!=checker, off-by-default): FASE 2 connectors que NO dependen de la DB -> Git + CI (gobernados por tool_policy deny-by-default, golden con fixtures, sin uso vivo sin s9+GO). FASE 1 mecanismo de skills (registro+digestion, E1) con el registro FUERA del config pinned (epoca, DECISION-0047) + 3 skills neutrales (convenciones DDL, verificar regla-de-negocio-vs-legacy, verificacion de migracion) como artefactos de instancia (no dominio en el core). NO construir Fase 4 / discovery_scanners. NO uso vivo de connectors (s9+GO posterior). NO tocar #4 (epoca 1.14.0, sin re-genesis)."
question: "Confirmas el alcance del FLOOR (Fase 2: Git+CI; Fase 1: registro+digestion + 3 skills neutrales; off-by-default; sin Fase 4; sin DB-live hasta T0) y arrancas de a una pieza por SDD?"
context_refs:
  - personal/operador/sintesis_hoja_de_ruta.html
  - Area_comun/decisions/DECISION-0047-versionado-epoca-bajo-4.md
  - Area_comun/decisions/DECISION-0044-connector-readonly-deny-by-default.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
deadline_or_blocking_level: normal
---

# GO - FLOOR de Fase 1 (Skills) + Fase 2 (Connectors), pull-based, sin Fase 4

Necesidad real con fecha (regla 3.4): el desarrollo de la app web (front + Seguridad + Presupuesto) sobre
la DB modelada en `D:\Agentes\Ingenas\Budget`, lanzamiento 2026-06-20 10:00 (o antes). Para que el dataset
sea desarrollo real (no coordinacion de texto), el dev necesita un PISO de capacidad. Construyelo **de a
una pieza**, SDD completo (DECISION -> SPEC con AC+test_plan -> golden), maker!=checker, **off-by-default**.

## FASE 2 - connectors del floor (arrancar YA, NO dependen de la DB)
- **Git** y **CI**: capa de conector sobre `tool_policy` (deny-by-default, scope, capabilities; "MCP no
  concede autoridad"). Golden con **fixtures** (sin sistema vivo). **Sin uso vivo** sin verificacion s9 +
  mi GO (espejo DECISION-0041). Registro en `connectors.config.json` (fuera del config pinned).
- El connector **DB read-only** ya esta (pieza 1); su **uso vivo** queda para T0 (s9 + GO).

## FASE 1 - mecanismo de skills (floor)
- **E1: registro + digestion** (contrato SKILL en `Area_comun/protocol/` + bloque de registro **FUERA de
  `protocol.config.json`** -- el config es inmutable-por-epoca bajo #4, DECISION-0047; usa un
  `skills.config.json` u equivalente, como connectors). Mecanismo **neutral**, cabe en el core.
- **3 skills neutrales** que el dev repite: convenciones DDL, verificar regla-de-negocio-vs-legacy,
  verificacion de migracion. Declaradas como **artefactos de instancia/perfil** (referencia por ID); el
  **contenido especifico del proyecto NO va al core neutral** (las reglas fiscales son del perfil, aparte).

## Limites duros (compliance)
- **NO Fase 4 / discovery_scanners** (auto-descubrimiento): es fase posterior, jalada por su propia
  necesidad; aqui solo declaramos lo que el dev necesita, no auto-deteccion.
- **NO uso vivo** de ningun connector sin s9 read-only verificada por Codex + mi GO.
- **NO tocar #4** (epoca 1.14.0, sin re-genesis; capacidades nuevas fuera del config pinned).
- **Neutralidad:** cero dominio fiscal/negocio en el core ni en `*.template.*`; el perfil
  `profiles/financiero_presupuesto/` es pieza aparte (no en este floor).
- **Una pieza a la vez** (no combinar ventanas); cada una verde en clon limpio (validate exit 0) antes de
  la siguiente. PII de terceros nunca al event log. DEF-PII (TASK-0118) diferida.

## Orden sugerido y reporte
Git -> CI -> registro+digestion de skills -> 3 skills. Reporta al cerrar cada pieza (canonico, gates
verdes, drift 0). El connector DB-live y el perfil financiero se jalan en T0 / post-T0. Canal ASCII.
