---
id: TASK-0110
owner: Claude
status: in_progress
type: analysis
priority: normal
created_at: 2026-06-13
updated_at: 2026-06-13
depends_on: []
relates_to: [DECISION-0005, DECISION-0008]
phase: P2
spec_id: none
linked_decisions: [DECISION-0005, DECISION-0008]
deliverables:
  - Area_comun/artifacts/ANALISIS-medicion-narracion-tokens-20260613.md
blocked_by_questions: []
sdd_required: false
objective: Medir (A/B controlado) si la directiva "narracion minima / reporte final" reduce tokens por tarea SIN perder auditabilidad, antes de codificar cualquier regla. Aplica el meta-criterio "medir, no asumir" (DECISION-0008). NO se cambia metodologia en esta fase.
expected_output: Artefacto Area_comun/artifacts/ANALISIS-medicion-narracion-tokens-20260613.md con - diseno A/B (unico factor = estilo: A verboso / B reporte-final), 2 tareas representativas (impl corta con goldens + revision de artefacto fijo), 3 corridas por variante, orden contrabalanceado; metricas - output tokens (primaria), total tokens + nro turnos (secundaria); guardrail de auditabilidad (handoff autocontenido, validador verde, drift 0, sin re-preguntas del revisor); tabla por corrida + media/dispersion + porcentaje de ahorro + conclusion/recomendacion (codificar o no).
question_to_resolve: La variante B (reporte final, sin narrar pasos) reduce output tokens de forma consistente (sugerencia operador - ahorro medio >=15%, 3 corridas coincidentes) manteniendo el guardrail de auditabilidad? Fuente de tokens - contador de sesion del CLI (Codex/Claude); measure_context_cost mide contexto de entrada por turno (loop OFF), no es la fuente primaria aqui.
closure_criterion: Artefacto con las 6 corridas (2 tareas x A/B... realmente 2 tareas x 2 variantes x 3 = 12 corridas) volcadas, media/dispersion, porcentaje de ahorro y estado del guardrail; recomendacion (confirma/no confirma) al operador. NO se tocan AGENTS.md/CLAUDE.md/DECISION-0005 en esta fase. Si confirma, el siguiente paso (separado, con GO del operador) es una DECISION = addendum a DECISION-0005, cuya autoria es de Claude y ratificacion del operador.
---

# TASK-0110 - Medicion A/B de la narracion intra-ejecucion (ahorro de tokens vs auditabilidad)

> IN_PROGRESS (Claude 2026-06-13, por orden del operador en PLAN-medicion-narracion-tokens). Tipo analysis;
> Claude coordina + consolida. Las corridas las ejecuta quien corre los agentes; el operador/arquitecto
> captura los numeros del contador de sesion. **Gate: cero codigo, cero cambio de metodologia.**

## Contexto

El operador dio la directiva "no narres cada accion durante la ejecucion; haz un reporte final y ya"
(guardada como feedback). Antes de codificarla como golden rule (addendum a DECISION-0005), se MIDE si
realmente ahorra tokens sin perder auditabilidad (meta-criterio "medir, no asumir", como con slim-views).

## Diseno (del plan del operador)

- **Variantes (unico factor):** A = verboso (narra cada accion); B = reporte final (sin narrar pasos,
  handoff autocontenido).
- **2 tareas representativas:** (i) implementacion corta con golden cases (perfil Codex); (ii) revision/
  analisis de un artefacto fijo (perfil Claude/analista).
- **3 corridas por variante por tarea**, orden contrabalanceado (A,B,A,B...), mismo modelo/config, mismo
  HEAD de partida (o tarea que no mute estado).
- **Metricas:** output tokens (primaria); total tokens + nro de turnos (secundaria); guardrail de
  auditabilidad (handoff completo, validador verde, drift 0, sin re-preguntas del revisor).
- **Fuente de tokens:** contador de sesion del CLI (Codex/Claude) al cerrar.

## Criterio de decision (lo fija el operador; sugerencia)

CONFIRMA si B reduce output de forma consistente (ahorro medio >=15%, 3 corridas coincidentes) Y el
guardrail se mantiene -> se codifica la golden rule (paso separado, con GO). NO confirma si el ahorro es
marginal o la auditabilidad cae -> queda como sugerencia.

## Entrega

`Area_comun/artifacts/ANALISIS-medicion-narracion-tokens-20260613.md` con la tabla de corridas + media/
dispersion + porcentaje de ahorro + conclusion. NO tocar AGENTS.md/CLAUDE.md/DECISION-0005 en esta fase.
