---
id: TASK-0064
owner: Codex
status: ready
type: documentation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0058, TASK-0061, TASK-0063]
relates_to: [TASK-0053]
phase: P2
spec_id: Area_comun/specs/SPEC-0050-d2.4-versionado-paquete.md
linked_decisions: [DECISION-0001, DECISION-0019, DECISION-0021]
execution_pipeline: [crear documento de versionado del paquete (p.ej. Area_comun/protocol/PACKAGE_VERSIONING.md) que consolide para el adoptante los 4 ejes de version -protocol_version (DECISION-0001), runtime_version (D2.2), schema_version del turn_schema (SCHEMA_VERSIONING.md), profile_version (DECISION-0003)- y que es MAJOR/MINOR/PATCH desde la perspectiva del adoptante + compatibilidad por tier (coordination/runtime); notas de migracion para adoptantes (subir de tier lite->runtime via new_instance/upgrade, adoptar deltas con upgrade_instance inform-only, politica de cambios incompatibles = decision+aprobacion del adoptante, referencia al CHANGELOG); enlazar sin duplicar con DECISION-0001/SCHEMA_VERSIONING/README_INSTANCIACION/N_AGENT_RUNTIME; neutralidad, sin secretos]
acceptance_criteria: [documento de versionado del paquete + notas de migracion presentes, coherentes y enlazados (sin duplicar); explica los 4 ejes de version y su SemVer para el adoptante, compatibilidad por tier, migracion lite->runtime; neutralidad limpia; sin secretos; validador/encoding/neutralidad py verdes; solo documentacion (no cambia runtime)]
expected_output: documento de versionado del paquete-metodologia + notas de migracion para adoptantes, neutral, coherente y enlazado; gates verdes.
test_plan: [validador/encoding/neutralidad py verdes; coherencia con DECISION-0001/SCHEMA_VERSIONING/runtime_version/tiers; enlaces validos; sin duplicacion; suite runtime sin tocar (documentacion)]
question_to_resolve: ninguna (alcance claro en SPEC-0050); ambiguedad de contrato => blocked + pregunta.
closure_criterion: documento de versionado + migracion completos, coherentes, neutrales, sin secretos, sin duplicacion; gates py verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [documento de versionado del paquete + notas de migracion (4 ejes + SemVer adoptante + compatibilidad por tier + migracion lite->runtime) publicables y coherentes; enlazado sin duplicar; neutralidad limpia; sin secretos; gates py verdes; handoff autocontenido; release atomico - claim liberado al pasar a in_review (DECISION-0018)]
---

# TASK-0064 - D2.4: SemVer del paquete-metodologia + notas de migracion

> `documentation` -> SDD ligero. Rebanada D2.4 (ultima de D2) del track de distribucion = v1.0. Documenta el
> versionado y la migracion para adoptantes. Solo documentacion, neutral, sin secretos. Ver SPEC-0050.

## Contexto

Un adoptante necesita reglas claras de versionado/migracion. Hoy estan dispersas (DECISION-0001 protocolo;
SCHEMA_VERSIONING turn_schema; runtime_version en D2.2; profile_version DECISION-0003). D2.4 las consolida.

## Alcance (ver SPEC-0050 sec.2)

1. Documento de versionado del paquete (p.ej. Area_comun/protocol/PACKAGE_VERSIONING.md): 4 ejes de version
   + MAJOR/MINOR/PATCH para el adoptante + compatibilidad por tier.
2. Notas de migracion: subir tier lite->runtime, adoptar deltas (upgrade_instance inform-only), politica de
   cambios incompatibles, referencia al CHANGELOG.
3. Enlazar sin duplicar (DECISION-0001/SCHEMA_VERSIONING/README_INSTANCIACION/N_AGENT_RUNTIME).

## Restricciones

- Solo documentacion (no cambia runtime); **neutralidad**; **sin secretos**; coherente; sin duplicacion.
- Fuera de alcance: el RELEASE v1.0 en si (bump protocol_version 1.0.0 + CHANGELOG + tag) = paso aparte con
  APROBACION HUMANA, tras D2.4 + DECISION-0020 + fix prune. Fase B/7. Cambio incompatible => `blocked`.
- **Handoff autocontenido** (handoff + in-review en el mismo paso del flip); **release atomico** (DECISION-0018).

## Nota

v1.0: D0 + D2.1 + D2.2 + wrapper + D2.3 done -> **D2.4 (esta, ultima de D2)** -> DECISION-0020 (regla
anti-colision) + fix prune -> RELEASE v1.0 (aprobacion humana). Codex autonomo (~100s): tomala cuando ready.
