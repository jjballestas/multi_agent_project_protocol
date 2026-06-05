---
decision_id: DECISION-0004
title: SDD (Spec-Driven Development) como gate previo a implementación, pipeline de ejecución y criterios de cierre
status: accepted
date: 2026-06-05
ratified_at: 2026-06-05
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0001, DECISION-0002, DECISION-0003, TASK-0008, TASK-0009, TASK-0010, TASK-0011, TASK-0012, TASK-0013]
phase: P2
---

# DECISION-0004 — SDD como gate previo a implementación + pipeline + criterios de cierre

## Contexto

Hoy la única salvaguarda contra ambigüedad es la regla genérica *"ambigüedad → `blocked` + una
pregunta concreta"*. No existe una capa formal que **obligue a tener claridad suficiente del
requerimiento, un pipeline de ejecución acordado y criterios de cierre verificables ANTES de
implementar**. Esto permite que un agente avance sobre supuestos o invente pasos.

Se adopta **Spec-Driven Development (SDD)** como disciplina del protocolo: la especificación y el
plan preceden a la ejecución, de forma **neutral de dominio** (SDD es proceso, no negocio).

## Decisión

### 1. SDD es un gate previo a la implementación

Ninguna **tarea implementable** puede pasar a `ready`, `claimed` o `in_progress` si antes no
declara, de forma completa y verificable, los **seis campos SDD**:

| Campo | Significado |
|-------|-------------|
| `spec_id` | Identificador de la especificación que gobierna la tarea (en `Area_comun/specs/`). |
| `execution_pipeline` | Pasos acordados de ejecución (qué se hará y en qué orden); el agente NO inventa pasos fuera de esto. |
| `acceptance_criteria` | Criterios de aceptación verificables del resultado. |
| `linked_decisions` | Decisiones que aplican/condicionan la tarea (p.ej. DECISION-0001..0004). |
| `test_plan` | Cómo se probará (comandos, fixtures, golden cases, validador). |
| `closure_criteria` | Condiciones objetivas que definen "done" (qué debe ser cierto para cerrar). |

Si falta cualquiera de los seis, la tarea **no es elegible** para `ready`/`claimed`/`in_progress`.

### 2. Ante ambigüedad, preguntar — nunca inventar

- Si el **requerimiento del usuario no está bien especificado**, o si el agente **tiene dudas**, el
  agente **pregunta antes de implementar o de crear la tarea**. No rellena huecos con supuestos ni
  inventa pasos.
- Si todavía **no hay suficiente claridad** para escribir una spec, se crea una tarea de tipo
  **`discovery` o `analysis`** (no `implementation`) cuyo propósito es producir esa claridad.
- Refuerza, no reemplaza, la regla existente *ambigüedad → `blocked` + pregunta concreta*.

### 3. Tipos de tarea

Toda tarea declara un `type`:

`implementation` · `refactor` · `integration` · `migration` · `security` · `release` ·
`discovery` · `analysis` · `review` · `documentation` · `triage`

### 4. Qué tipos exigen SDD completo (los 6 campos)

**SDD obligatorio:** `implementation`, `refactor`, `integration`, `migration`, `security`, `release`.

### 5. Qué tipos pueden no tener spec completa

**SDD ligero:** `discovery`, `analysis`, `review`, `documentation` (draft), `triage`.

Aun así, **incluso estas** deben declarar los **cuatro campos mínimos**:

| Campo mínimo | Significado |
|--------------|-------------|
| `objective` | Qué se busca. |
| `expected_output` | Qué entrega concreta produce. |
| `question_to_resolve` | La pregunta que la tarea debe responder. |
| `closure_criterion` | Cuándo se considera cerrada. |

Una tarea `documentation` que ya no es draft sino entrega formal se trata como implementable a
efectos de rigor si toca contrato/templates publicados (criterio del arquitecto).

### 6. Revisión cruzada y handoff

- La **revisión cruzada** valida el resultado **contra la spec (`spec_id`) y los
  `closure_criteria`/`acceptance_criteria`**, no contra la intuición del revisor.
- El **handoff** debe declarar explícitamente **qué criterios de aceptación/cierre se cumplieron y
  qué pruebas (`test_plan`) se ejecutaron**, con su resultado.

### 7. Estructura propuesta (la implementa TASK-0010)

```
Area_comun/specs/
├── SPEC_TEMPLATE.md                 # plantilla de especificación (los 6 campos + contexto + alcance)
├── PROJECT_BRIEF_TEMPLATE.md        # brief inicial de un proyecto/iniciativa
├── TEST_PLAN_TEMPLATE.md            # plan de pruebas reutilizable
└── TRACEABILITY_MATRIX_TEMPLATE.md  # matriz requisito → spec → tarea → prueba → criterio de cierre
```

Las specs viven en la instancia; el `spec_id` de cada tarea referencia un archivo en `specs/`.

### 8. Actualizaciones propuestas (las implementan TASK-0009/0011/0013)

- `Area_comun/protocol/TASK_PROTOCOL.md`: añade el gate SDD al ciclo de vida y la regla
  discovery-antes-de-implementar.
- `Area_comun/protocol/TASK_TEMPLATE.md`: añade `type` y los campos SDD (o los mínimos).
- `Area_comun/protocol/HANDOFF_TEMPLATE.md`: añade "criterios cumplidos" y "pruebas ejecutadas".
- `Area_comun/reports/HUMAN_REPORT_TEMPLATE.md`: refleja spec/criterios/pruebas.
- `README_INSTANCIACION.md`: cómo iniciar un proyecto con SDD.
- `protocol.config.template.json`: bloque `sdd` (ver §10).

### 9. Comportamiento del validador (lo implementa TASK-0011, aditivo)

- **No rompe tareas históricas `done`** ni instancias sin SDD: si `sdd.enabled` es falso/ausente,
  comportamiento idéntico al actual.
- Cuando `sdd.enabled` es verdadero y `enforcement` es `new_implementable_tasks`:
  - **ERROR** si una tarea de tipo SDD-obligatorio en `ready`/`claimed`/`in_progress` (o
    `in_review`/`done` creada bajo SDD) **carece de** `spec_id`, `execution_pipeline`,
    `acceptance_criteria`, `linked_decisions`, `test_plan` o `closure_criteria`, o si el archivo
    `spec_id` referenciado no existe.
  - **WARNING** si una tarea `discovery`/`analysis`/`review`/`documentation`/`triage` no declara
    `objective`, `expected_output`, `question_to_resolve` o `closure_criterion`.
  - Las tareas marcadas como **históricas/pre-SDD** (campo de exención o `created_at` previo a la
    adopción) quedan **fuera** del chequeo (sin migración retroactiva).
- La paridad `.py` ↔ `.ps1` se mantiene con golden cases (positivos y negativos), como en TASK-0007.

### 10. Activación por configuración

`protocol.config.json` (y su template) incorpora un bloque opcional:

```json
{
  "sdd": {
    "enabled": true,
    "enforcement": "new_implementable_tasks"
  }
}
```

- `enabled: false`/ausente → SDD documentado pero no forzado (default; cero impacto).
- `enforcement: "new_implementable_tasks"` → solo tareas implementables **nuevas**. (Valor futuro
  posible `all` exigiría retroactividad → MAJOR, ver §11.)

### 11. Versionado y compatibilidad (coherente con DECISION-0001)

- La capa SDD entra como **MINOR `v0.4.0`** si se implementa **aditivamente** (config-gated por
  defecto desactivada; sin migración retroactiva). No requiere aprobación humana adicional más allá
  de esta decisión, que el operador humano ya solicita.
- **Exigir SDD retroactivamente a TODAS las tareas (incluidas las `done`)** sería **incompatible →
  MAJOR**, y requeriría decisión + **aprobación humana** explícita (DECISION-0001 §4). **Fuera de
  alcance** de esta decisión.
- **Sin migración retroactiva:** las tareas históricas ya `done` (TASK-0001..0007) **no** se migran.

### 12. Alcance de aplicación

La regla aplica a **tareas nuevas** de tipo `implementation`, `refactor`, `integration`,
`migration`, `security`, `release`. El backlog de formalización (TASK-0008..0013) es el
**bootstrap**: TASK-0008 (design) produce las specs contra las que se implementan TASK-0009..0012.

## Consecuencias

- **Positivas:** claridad obligatoria antes de ejecutar; el agente no inventa pasos ni avanza sobre
  ambigüedad; trazabilidad requisito→spec→tarea→prueba→cierre; revisión objetiva contra criterios.
- **Costo:** más ceremonia por tarea implementable; se mitiga con plantillas (specs/) y con el modo
  config-gated.
- **Neutralidad:** SDD es proceso, **domain-neutral**; nada de stack/negocio entra al core.
- **Seguimiento:** backlog TASK-0008..0013; la capa se publica como `v0.4.0` al cerrarlos.

## Alternativas consideradas

- **Mantener solo "ambigüedad → blocked":** insuficiente; no obliga a spec/pipeline/cierre antes de
  ejecutar.
- **SDD obligatorio y retroactivo desde ya:** rompe compatibilidad (MAJOR) y no aporta valor sobre
  tareas ya cerradas; descartado.
- **SDD siempre-on (sin config):** menos flexible para instancias ligeras; el flag `sdd.enabled`
  permite adopción gradual.
