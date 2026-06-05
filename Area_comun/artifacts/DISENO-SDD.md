# DISEÑO SDD — diseño técnico de la capa Spec-Driven Development

> Entregable de **TASK-0008** (Claude, `analysis`). Implementa el diseño que fija
> [DECISION-0004](../decisions/DECISION-0004-sdd-pipeline-y-cierre.md). Es la **fuente de verdad**
> contra la que se implementan TASK-0009..0013. Neutral de dominio. La capa se publica como
> **v0.4.0** (MINOR, aditivo, config-gated).

## 0. Resumen

SDD = la **spec y el plan preceden a la ejecución**. Este documento fija: (1) el contrato exacto de
los campos por tarea, (2) los cambios a las plantillas del protocolo, (3) la estructura de
`Area_comun/specs/`, (4) el comportamiento del validador y el esquema de config, y (5) el índice de
specs del rollout (`spec_id` por tarea) que desbloquea a Codex.

## 1. Contrato de campos por tarea

### 1.1 Campos SDD completos (tipos implementables)

Obligatorios para `implementation`, `refactor`, `integration`, `migration`, `security`, `release`
**antes** de `ready`/`claimed`/`in_progress`:

| Campo | Forma | Regla de "completo" |
|-------|-------|---------------------|
| `spec_id` | string | Referencia a un archivo existente en `Area_comun/specs/` (p.ej. `Area_comun/specs/SPEC-0011-validator-sdd.md`). |
| `execution_pipeline` | lista ordenada de pasos | ≥1 paso; pasos concretos; el agente no ejecuta nada fuera de la lista sin actualizar la spec. |
| `acceptance_criteria` | lista verificable | ≥1; cada criterio comprobable objetivamente. |
| `linked_decisions` | lista | ≥1 (al menos la decisión que habilita la tarea); puede ser `[]` solo si la spec justifica que no aplica ninguna. |
| `test_plan` | texto/lista | comandos/fixtures/validador concretos; cómo se demuestra cada acceptance_criteria. |
| `closure_criteria` | lista | condiciones objetivas de "done"; superconjunto verificable de acceptance + handoff + validador verde. |

### 1.2 Campos mínimos (tipos no implementables)

Para `discovery`, `analysis`, `review`, `documentation` (draft), `triage`:

| Campo | Regla |
|-------|-------|
| `objective` | qué se busca (1 frase). |
| `expected_output` | entrega concreta (artefacto/decisión/respuesta). |
| `question_to_resolve` | la pregunta que la tarea responde. |
| `closure_criterion` | cuándo se cierra. |

`documentation` que toca contrato/templates publicados se trata con rigor de implementable
(criterio del arquitecto en revisión). Ver TASK-0013.

### 1.3 Ubicación de los campos

En el **frontmatter** de `Area_comun/tasks/TASK-XXXX-*.md` (machine-readable para el validador) y/o
en una sección del cuerpo. El validador (TASK-0011) lee el frontmatter; si un campo es lista, acepta
lista YAML o sección markdown con viñetas bajo el encabezado homónimo. Decisión: **frontmatter como
fuente canónica**; el cuerpo amplía.

## 2. Cambios a plantillas del protocolo (los implementa TASK-0009)

### 2.1 `Area_comun/protocol/TASK_PROTOCOL.md`
- Añadir al ciclo de vida el **gate SDD**: `proposed → (spec lista) → ready → claimed → in_progress
  → in_review → done`. Sin los campos del tipo, la tarea **no puede** dejar `proposed`.
- Añadir regla: *ambigüedad o requerimiento incompleto → preguntar; si no hay claridad para una
  spec, crear `discovery`/`analysis`, nunca `implementation`. No inventar pasos.*
- Añadir: la **revisión cruzada** valida contra `spec_id` + `acceptance_criteria`/`closure_criteria`.

### 2.2 `Area_comun/protocol/TASK_TEMPLATE.md`
- Añadir `type` al frontmatter y los **6 campos SDD** (implementables) o los **4 mínimos**.
- Incluir comentario guía de qué campos aplican según `type`.

### 2.3 `Area_comun/protocol/HANDOFF_TEMPLATE.md`
- Añadir secciones obligatorias: **"Criterios cumplidos"** (mapear cada acceptance/closure a
  evidencia) y **"Pruebas ejecutadas"** (comandos + resultado).

### 2.4 `Area_comun/reports/HUMAN_REPORT_TEMPLATE.md`
- Añadir referencia a `spec_id`, criterios y pruebas en el reporte humano.

## 3. Estructura de `Area_comun/specs/` (la materializa TASK-0010)

- **Plantillas reutilizables (deliverables de TASK-0010):**
  `SPEC_TEMPLATE.md`, `PROJECT_BRIEF_TEMPLATE.md`, `TEST_PLAN_TEMPLATE.md`,
  `TRACEABILITY_MATRIX_TEMPLATE.md`.
- **Specs concretas (creadas por TASK-0008, este entregable):** `SPEC-0009..SPEC-0013`.
- `SPEC_TEMPLATE.md` debe contener exactamente los 6 campos SDD + Contexto + Alcance + No-alcance +
  Riesgos. `TRACEABILITY_MATRIX_TEMPLATE.md`: columnas `requisito | spec_id | task_id | prueba |
  closure_criterion | estado`.

## 4. Validador — comportamiento (lo implementa TASK-0011, aditivo y con paridad)

### 4.1 Activación
`protocol.config.json`:
```json
{ "sdd": { "enabled": true, "enforcement": "new_implementable_tasks" } }
```
- `sdd` ausente o `enabled:false` → **sin chequeos SDD** (comportamiento idéntico al actual). Default.
- `enforcement`: `"new_implementable_tasks"` (único valor soportado en v0.4.0). Reservar `"all"`
  para un futuro MAJOR (retroactivo).

### 4.2 Exención de tareas pre-SDD (sin migración retroactiva)
Una tarea queda **exenta** si cumple cualquiera:
- declara `sdd_exempt: true`, **o**
- su `created_at` es anterior a `sdd.adopted_at` (si se declara en config; por defecto 2026-06-05), **o**
- no declara `type` (las históricas TASK-0001..0007 no lo tienen) → se asume pre-SDD.

### 4.3 Reglas (solo si `sdd.enabled` y la tarea NO está exenta)
- Si `type` ∈ {implementation, refactor, integration, migration, security, release} **y**
  `status` ∈ {ready, claimed, in_progress, in_review, done}:
  - **ERROR** por cada campo faltante/vacío de los 6 SDD.
  - **ERROR** si `spec_id` no resuelve a un archivo existente (relativo a la raíz de la instancia).
- Si `type` ∈ {discovery, analysis, review, documentation, triage} (cualquier status no-`proposed`):
  - **WARNING** por cada uno de los 4 mínimos ausente.
- `type` desconocido → **WARNING** "tipo de tarea no reconocido".
- Tareas en `proposed` no se chequean por campos SDD (aún se están especificando), salvo el
  `type` si está presente.

### 4.4 Paridad y pruebas
Igual que TASK-0007: lógica idéntica `.py`↔`.ps1`, mismos mensajes, golden cases positivos y
negativos en `examples/sdd_validation_cases/` (o reutilizar el patrón de `profile_validation_cases`).
Instancias actuales (`minimal_instance`, `generated_minimal_instance`, `dotnet_enterprise_instance`)
deben seguir **verdes** (no declaran `sdd` → sin chequeos).

## 5. Índice de specs del rollout (spec_id por tarea)

Specs concretas creadas por TASK-0008 (este entregable), en `Area_comun/specs/`:

| Tarea | spec_id | Tipo | Campos |
|-------|---------|------|--------|
| TASK-0009 | `Area_comun/specs/SPEC-0009-sdd-templates.md` | implementation | 6 SDD |
| TASK-0010 | `Area_comun/specs/SPEC-0010-specs-folder.md` | implementation | 6 SDD |
| TASK-0011 | `Area_comun/specs/SPEC-0011-validator-sdd.md` | implementation | 6 SDD |
| TASK-0012 | `Area_comun/specs/SPEC-0012-example-minimal-sdd.md` | implementation | 6 SDD |
| TASK-0013 | `Area_comun/specs/SPEC-0013-doc-sdd-onboarding.md` | documentation | 4 mínimos |

Con estas specs, Codex puede completar el frontmatter de cada tarea y pasarla a `ready`/`claimed`.

## 6. Orden de implementación recomendado

1. **TASK-0010** (specs/ + plantillas) y **TASK-0009** (templates de protocolo) en paralelo.
2. **TASK-0011** (validador SDD + config) — depende del contrato (§1, §4) y de specs/ (§3).
3. **TASK-0012** (ejemplo `minimal_sdd_instance`) — demuestra el validador con `sdd.enabled`.
4. **TASK-0013** (doc onboarding) — tras 0009/0010.
5. Cerrar y publicar **v0.4.0** (mover Unreleased en CHANGELOG + tag), revisión cruzada del arquitecto.

## 7. Decisión de diseño resuelta (pregunta abierta del handoff)
**Una spec por tarea** (no una global), enlazadas por la **matriz de trazabilidad**
(`TRACEABILITY_MATRIX_TEMPLATE.md`). Más granular, revisable y trazable requisito→spec→tarea→prueba.

## 8. Neutralidad
Todo lo anterior es **proceso** (domain-neutral). Ni el diseño, ni las plantillas, ni las specs del
rollout introducen términos de stack/negocio en el core ni en los `*.template.*`.
