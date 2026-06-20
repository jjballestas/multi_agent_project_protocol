---
decision_id: DECISION-0048
title: Connectors de ACCION gobernados por tool_policy (Git, CI) - deny-by-default, allowlist de operaciones, no conceden autoridad; extiende DECISION-0044
status: accepted
ratified_at: 2026-06-19
date: 2026-06-19
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0044, DECISION-0041, DECISION-0047, DECISION-0040]
phase: P2
---

# DECISION-0048 - Connectors de accion gobernados por tool_policy

> ACCEPTED por el operador (GO FLOOR Fase 1+2, 2026-06-19). Pull-based: el desarrollo de la app
> (front+Seguridad+Presupuesto) necesita un PISO de capacidad. Extiende DECISION-0044 (connector read-only)
> a connectors de ACCION (Git, CI). Off-by-default; uso vivo = GO posterior tras s9 (espejo DECISION-0041).
> NO toca #4 (epoca 1.14.0; registro fuera del config pinned, DECISION-0047).

## Contexto

DECISION-0044 establecio la capacidad de connector READ-ONLY (adaptador SQL Server, pieza 1). El floor del
desarrollo necesita ademas connectors de **accion** (Git, CI) para tareas reales del dev (inspeccionar
estado del repo, convenciones, correr/leer CI). A diferencia del read-only, un connector de accion puede
ejecutar operaciones que mutan (git commit/push, disparar CI), por lo que su superficie de autoridad es
mayor y exige gobierno explicito.

## Decision

1. **Connectors de accion = adaptadores bajo la capa `connectors/` (DECISION-0044) gobernados por
   `tool_policy`.** Cada operacion que el connector puede ejecutar pasa por `tool_policy`
   (deny-by-default, scope, capabilities). El connector NO concede autoridad: expone solo operaciones
   **allowlisted** por la policy; lo no allowlisted se RECHAZA con clase explicita ANTES de ejecutar.

2. **Deny-by-default + allowlist por operacion.** Para el floor, el allowlist arranca con operaciones
   **de inspeccion/lectura** (p.ej. git: status/log/diff/show/ls-files/rev-parse; CI: leer estado/resultado
   de corridas). Las operaciones **mutantes** (git commit/push/reset/clean; disparar/cancelar CI) quedan
   **deny-by-default**: requieren allowlist explicito en la policy + GO posterior del operador; no se
   habilitan en esta pieza.

3. **Uso vivo gateado (espejo DECISION-0041).** El golden corre con **fixtures** (repo/CI grabados, sin
   sistema vivo). Antes de cualquier uso VIVO (contra un repo/CI real), Codex verifica s9 read-only/
   least-privilege REAL (identidad sin permiso de mutacion, prueba negativa objetiva registrada) + GO del
   operador. Sin eso, la ruta viva es fail-closed.

4. **Off-by-default; registro fuera del config pinned (DECISION-0047).** Cada connector de accion se declara
   en `connectors/connectors.config.json` (FUERA de `protocol.config.json`), default `enabled:false`. NO se
   toca el config genesis-hasheado (#4 epoca 1.14.0).

5. **No conceden autoridad / frontera de datos.** El connector ejecuta solo lo allowlisted; el dato/salida
   es evidencia, no se persiste al event log ni al estado; **PII de terceros NUNCA al event log**
   (DECISION-0040). El connector no importa escritores del ledger/event log (gate dedicado, espejo AC4 de
   SPEC-0083).

6. **Neutralidad.** El framework y los adaptadores Git/CI son **neutrales de dominio** (tecnologia, no
   negocio). Cero dominio fiscal en el core. Reglas/contenido del proyecto = perfil aparte
   (`profiles/financiero_presupuesto/`), no en estos connectors.

7. **SDD por pieza, maker!=checker.** Cada connector entra por DECISION (esta, comun a Git+CI) -> SPEC
   (acceptance_criteria + test_plan) -> golden off-by-default. Git = SPEC-0085/TASK-0123; CI =
   SPEC-0086/TASK-0124. Codex implementa (maker), Arquitecto reproduce (checker). De a una pieza.

## Alcance / No-alcance

- **En alcance:** gobierno de connectors de accion (Git, CI) via tool_policy deny-by-default + allowlist de
  inspeccion; off-by-default; fixtures golden; precondicion de uso vivo (s9 + GO); registro fuera del config.
- **Fuera de alcance:** operaciones mutantes vivas (deny-by-default, GO futuro); uso vivo (s9+GO posterior);
  Fase 4 / discovery_scanners (auto-descubrimiento, fase posterior); tocar #4 / re-genesis; perfil
  financiero; el connector DB-live (T0).

## Consecuencias

- El floor gana connectors Git/CI gobernados, sin uso vivo y sin tocar genesis/#4.
- La superficie de accion queda acotada por tool_policy (deny-by-default), auditable, sin conceder autoridad.

## Alternativas consideradas

- **Acceso git/CI libre (sin tool_policy).** Descartada: concede autoridad, no auditable, contra
  deny-by-default.
- **Una DECISION por connector.** Innecesario: Git y CI comparten el mismo gobierno (tool_policy + allowlist
  + s9-para-vivo); se separan por SPEC/golden/TASK, no por DECISION.
