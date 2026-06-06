---
id: TASK-0053
owner: Codex
status: done
type: documentation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0043]
relates_to: [TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0001, DECISION-0015]
objective: Cubrir el criterio 17 de SPEC-0038 (Decision de SemVer justificada segun consumidores reales del schema) declarando una version explicita del turn_schema y documentando su politica de versionado, ultimo item de la Capa A.
expected_output: (1) version explicita declarada para runtime/turn_schema.json (campo aditivo, p.ej. schema_version, sin romper la validacion existente); (2) doc de politica de versionado del schema en Area_comun/protocol/ (que cambio es PATCH/MINOR/MAJOR segun los consumidores reales turn_validate/apply/adaptadores); (3) justificacion de que los cambios aditivos de Fases 1-4 fueron MINOR (coherente con DECISION-0001).
question_to_resolve: Que version corresponde al turn_schema hoy y bajo que regla evoluciona (campos opcionales nuevos = MINOR aditivo; quitar/renombrar requerido o cambiar semantica = MAJOR; correccion no contractual = PATCH).
closure_criterion: turn_schema declara version explicita (aditivo, sin romper golden turn schema 5/5 + semantic 5/5 ni la suite); doc de politica SemVer del schema publicada en Area_comun/protocol/; justificacion Fases 1-4=MINOR registrada; gates py verdes; handoff autocontenido; release atomico al pasar a in_review (DECISION-0018).
---

# TASK-0053 - Capa A.7: SemVer del turn_schema (criterio 17)

> `documentation` (con cambio aditivo menor al schema). Cubre el **criterio 17** de SPEC-0038:
> "Decision de SemVer justificada segun consumidores reales del schema." **Ultimo item de la Capa A.**
> Aditivo; fallback intacto. Release ATOMICO al cerrar (DECISION-0018).

## Contexto

El `runtime/turn_schema.json` ha evolucionado de forma aditiva a lo largo de las Fases 1-4 (campos
opcionales nuevos: `attempt_id`, `idempotency_key`, `aggregate_version`, `fencing_token`,
`transitions.review_qa`, estados Review/QA). Falta cerrar el criterio 17: declarar una version explicita del
schema y documentar la politica de versionado segun sus consumidores reales (turn_validate, apply,
adaptadores), justificando que esos cambios fueron MINOR (aditivos), coherente con DECISION-0001.

## Alcance

1. **Version explicita del schema:** declarar la version del turn_schema de forma aditiva (p.ej. un campo
   `schema_version`/`version` en `runtime/turn_schema.json`, o un mecanismo equivalente) sin romper la
   validacion ni los golden de turno existentes (schema 5/5 + semantic 5/5).
2. **Politica de versionado del schema** (doc en `Area_comun/protocol/`): que cambio del schema es
   PATCH / MINOR / MAJOR en funcion de los consumidores reales:
   - campo opcional nuevo / relajacion compatible => **MINOR** (aditivo);
   - quitar/renombrar un campo requerido, endurecer una restriccion, cambiar semantica => **MAJOR**;
   - correccion que no cambia el contrato (typo, descripcion) => **PATCH**.
3. **Justificacion historica:** registrar que los cambios de Fases 1-4 al turn_schema fueron aditivos =>
   MINOR, consistente con como se versiono el protocolo (DECISION-0001).

## Restricciones

- **Aditivo**: si tocas `runtime/turn_schema.json`, debe seguir validando los golden de turno (schema 5/5,
  semantic 5/5) y toda la suite runtime; no romper contrato ni golden existentes.
- **Sin red**; sin secretos; **neutralidad de dominio** intacta.
- Handoff autocontenido; **release ATOMICO** al pasar a `in_review` (mensaje + liberar claim + flip status
  juntos; DECISION-0018).

## Nota de cierre de Capa A

Este es el ULTIMO item de la Capa A (consolidacion del nucleo N-agente). Con A.7 cerrada: A.5 (CI) + A.1
(writer-vivo Fase A) + A.6 (hardening I1/I2) + A.2 (golden N=3/N=5) + A.3 (property-based I1-I8) + A.4
(concurrency sim) + A.7 (SemVer schema) => Capa A COMPLETA. Tras aceptar A.7, Claude reportara al operador
que la Capa A esta lista y preguntara el siguiente paso (Fase 5 gateada / release v0.10.0 / detener). Fase
B (writer-vivo del estado de protocolo) y Fase 5 siguen GATEADAS: NO arrancar.
