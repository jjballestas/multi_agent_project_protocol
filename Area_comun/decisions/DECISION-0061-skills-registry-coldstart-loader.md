---
decision_id: DECISION-0061
title: Skills gobernadas - registro fuera del config pinned + loader cold-start READ-ONLY, neutrales, off-by-default, no conceden autoridad (FLOOR skills Fase 1)
status: accepted
ratified_at: 2026-06-26
date: 2026-06-26
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0048, DECISION-0044, DECISION-0047, DECISION-0040, DECISION-0050]
phase: P2
---

# DECISION-0061 - Skills gobernadas (registro + loader cold-start read-only)

> ACCEPTED por el operador (GO FLOOR skills Fase 1, 2026-06-26). Pull-based: el desarrollo necesita
> capturar PROCEDIMIENTOS reutilizables (convenciones, verificaciones) que los agentes adquieren en frio.
> Espeja el gobierno de connectors (DECISION-0044/0048): capa separada, registro FUERA del config pinned,
> off-by-default, no concede autoridad. NO toca #4 (epoca 1.14.0, DECISION-0047).

## Contexto

DECISION-0048 dio el floor de connectors (Git/CI). La otra pieza del floor es **skills**: paquetes de
conocimiento/procedimiento reutilizables que un agente "digiere" para ejecutar mejor una tarea (p.ej.
convenciones de DDL, distinguir regla de negocio de legacy, verificar una migracion). Hoy ese conocimiento
vive disperso en runbooks personales; falta un mecanismo gobernado, neutral y trazable de **registro** y
**digestion**.

El operador eligio el modelo de digestion = **loader cold-start READ-ONLY**: una skill es un documento
gobernado que un agente lee en arranque en frio para adquirir el procedimiento, sin que el mecanismo conceda
autoridad ni escriba estado.

## Decision

1. **Capa `skills/` separada, mecanismo NEUTRAL.** Igual que `connectors/`, las skills viven en su propia
   capa bajo el protocolo. El **mecanismo** (framework + registro + loader) es **domain-neutral** y vive en
   el core. El **contenido** de skills con terminos de dominio vive SOLO bajo `profiles/<perfil>/skills/`
   (p.ej. `profiles/financiero_presupuesto/skills/`), NUNCA en el core (regla CLAUDE.md 1 / s.4).

2. **Registro FUERA del config pinned (DECISION-0047).** Las skills se declaran en
   `skills/skills.config.json` (FUERA de `protocol.config.json`), `schema_version: "skills.config.v1"`,
   default `enabled:false` por skill. Activar el config NO altera `chain.genesis`; el registro NO es parte
   del genesis del event-log.

3. **Digestion = loader cold-start READ-ONLY.** El loader es DETERMINISTA y de solo lectura: resuelve las
   skills habilitadas del registro y produce un indice/contenido que el agente lee en cold-start. El loader
   NO escribe estado, NO toca el ledger ni el event-log, NO ejecuta acciones, NO concede autoridad. Una
   skill aporta PROCEDIMIENTO (texto), no capacidad ejecutable.

4. **Trust boundary por skill (espejo connectors).** Cada entrada declara `read_only:true`,
   `grants_no_authority:true`, `persists_outputs:false`, su `profile`/scope y `neutral_core:false` cuando su
   contenido es de dominio (=> obliga ubicacion en `profiles/`). El loader rechaza (fail-closed) una skill
   mal declarada o cuyo contenido de dominio pretenda vivir en el core.

5. **Off-by-default; uso = lectura, no accion.** Por defecto deshabilitado. Habilitar una skill solo la hace
   legible por el loader; no ejecuta nada. No hay "uso vivo" riesgoso (a diferencia de connectors): una
   skill es texto inerte. Aun asi entra por SDD pieza a pieza, maker!=checker, golden fixtures.

6. **Frontera de datos / PII (DECISION-0040).** El contenido de skills es generico/de-perfil, sin PII de
   terceros ni secretos. El loader no importa escritores del ledger/event-log (gate dedicado, espejo AC4 de
   connectors). `scan_domain_neutrality` cubre la capa `skills/` del core (el mecanismo no contiene terminos
   de dominio).

7. **SDD por pieza, maker!=checker.** Fase 1: **pieza 1 = mecanismo** (framework + registro + loader cold-start
   + golden + cobertura de neutralidad), SPEC-0096 / TASK-0183, maker=Codex / checker=Arquitecto. **Pieza 2 =
   3 skills neutrales** (convenciones DDL / regla-negocio-vs-legacy / verificacion-migracion), contenido en
   `profiles/financiero_presupuesto/skills/`, GO posterior tras cerrar la pieza 1.

## Alcance

- **En alcance:** mecanismo neutral de skills (registro fuera del config pinned + loader cold-start read-only
  + trust boundary por skill + golden fixtures + cobertura de neutralidad); off-by-default; SDD por pieza.
- **Fuera de alcance:** las 3 skills neutrales en si (pieza 2, GO posterior); cualquier skill con contenido
  de dominio en el core; capacidad ejecutable/accion via skills; tocar genesis/#4/config pinned.

## Consecuencias

- El floor gana un mecanismo gobernado, neutral y trazable para capturar y digerir procedimiento reutilizable,
  sin conceder autoridad y sin tocar #4.
- Coste: una capa nueva (`skills/`) y un registro nuevo fuera del config; mantener la neutralidad del core
  (contenido de dominio solo en perfiles).

## Alternativas consideradas

- **Skills como citas en tareas/handoffs (sin loader):** mas liviano pero no da un mecanismo de carga
  reutilizable; el conocimiento queda atado al ciclo de tareas. Rechazado por el operador.
- **Skills en el front (Zeus):** empuja al repo producto; util para el operador pero no le da a los runtimes
  un mecanismo de carga en frio. Rechazado.
- **Meter el registro en `protocol.config.json`:** romperia el chain del #4 (DECISION-0047); por eso va fuera.
