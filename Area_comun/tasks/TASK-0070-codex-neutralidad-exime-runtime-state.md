---
id: TASK-0070
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0069]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0056-neutralidad-exime-runtime-state.md
linked_decisions: [DECISION-0022, DECISION-0017]
execution_pipeline: [anadir runtime/state/** a domain_neutrality.exempt_globs en protocol.config.json (vivo) y protocol.config.template.json (master); confirmar paridad py/.ps1 (ambos leen exempt_globs del config); golden en examples/neutrality_scan_cases (o nuevo) que demuestre: termino del denylist bajo runtime/state => PASA (exento) y termino en una fuente runtime/*.py escaneada => sigue FALLANDO; documentar que runtime/state NO se gitignora (en autoritativo el log/snapshots son fuente de verdad y deben commitearse); CI]
acceptance_criteria: [runtime/state/** exento del scan de neutralidad en protocol.config.json y protocol.config.template.json; un termino del denylist bajo runtime/state pasa el scan; un termino del denylist en una fuente runtime escaneada (p.ej. runtime/*.py) sigue fallando (la exencion no abre agujero en el core); golden + paridad py/.ps1; validador/encoding/neutralidad/prune py/ps verdes; sin debilitar el boundary del core; sin cambiar el denylist ni el turn schema]
expected_output: runtime/state/** exento de neutralidad (vivo+template), demostrado por golden (exento pasa / fuente escaneada falla); gates verdes; nota de gitignore.
test_plan: [golden neutralidad: termino denylist bajo runtime/state => pasa; termino en runtime/*.py escaneado => falla; regresion del resto del scan; paridad py/ps; suite de gates verde]
question_to_resolve: ninguna (alcance claro en SPEC-0056). Si exime mas de lo debido o requiere gitignorar el log autoritativo => blocked + pregunta.
closure_criterion: runtime/state/** exento de neutralidad (vivo+template) + golden (exento pasa / fuente falla) + paridad py/.ps1 + gates verdes + nota gitignore; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [runtime/state/** en exempt_globs (protocol.config.json + protocol.config.template.json); golden demuestra exento-pasa y fuente-escaneada-falla; paridad py/.ps1; runtime/state NO gitignorado (documentado); sin debilitar core; sin tocar denylist/turn schema; validador/encoding/neutralidad/prune py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0070 - Neutralidad exime runtime/state (dato generado por el runtime)

## Contexto

Al intentar la activacion sombra del writer-vivo (Fase B, 3.b), el genesis por referencia escribe el snapshot
content-addressed en `runtime/state/snapshots/<hash>.json`, que embebe el estado de protocolo vivo (puede
referenciar el dominio del piloto). El scan de neutralidad cubre `runtime/**` => falla. Es un defecto de gate:
`runtime/state/` es dato GENERADO por el runtime (analogo al ledger vivo `Area_comun/state/*.json` ya exento,
y a `runtime/runs/` ya gitignorado). Ver SPEC-0056. Desbloquea la activacion sombra.

## Alcance (ver SPEC-0056 sec.2)

1. Anadir `runtime/state/**` a `domain_neutrality.exempt_globs` en `protocol.config.json` (vivo) y
   `protocol.config.template.json` (master).
2. Golden: termino del denylist bajo `runtime/state` => PASA; termino en una fuente `runtime/*.py` escaneada
   => sigue FALLANDO.
3. NO gitignorar `runtime/state/` (en autoritativo el log/snapshots son fuente de verdad); documentar.

## Restricciones

- **Aditivo, NO debilita el boundary del core**: la fuente del runtime (`runtime/*.py`, `runtime/adapters/**`,
  `runtime/*.md`) sigue escaneada; solo se exime el estado generado. Paridad py/.ps1.
- No cambiar el `denylist` ni el contrato del turn schema. Neutralidad/sin secretos/ASCII (DECISION-0012).
- Cambio incompatible o exencion demasiado amplia => `blocked` + pregunta.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020).

## Nota

Prerequisito para re-intentar la activacion sombra del writer-vivo (que el operador aprobo). Tras esta tarea,
Claude re-aplica la activacion sombra (enabled+materialize, enforce/authoritative siguen off). Promovida de a
una (DECISION-0020). Codex autonomo: tomala cuando `ready`; GO enviado por mailbox.

## Progreso

- 2026-06-07 Codex reclamo la tarea tras GO de Claude. Anomalia previa sobre ledger queda resuelta por la
  regularizacion posterior (TASK_INDEX + GO presentes).
- 2026-06-07 Codex entrega a `in_review`: `runtime/state/**` exento en config viva/template, golden
  exento-pasa/fuente-falla con paridad py/ps, nota de no gitignore y gates verdes.
