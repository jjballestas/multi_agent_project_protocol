# ANALISIS - Medicion A/B de la narracion intra-ejecucion (TASK-0110)

**Estado:** EN CURSO (esqueleto). Deliverable de TASK-0110. Coordina Claude; las corridas las ejecuta quien
corre los agentes y el operador/arquitecto captura los numeros. **Gate: cero codigo, cero cambio de
metodologia hasta que la medicion confirme y haya GO para una DECISION (addendum a DECISION-0005).**

## Hipotesis

Minimizar la narracion intra-ejecucion (variante B = reporte final, sin narrar cada paso) **reduce los
tokens de output por tarea** y **mantiene** la auditabilidad (handoff autocontenido, validador verde,
drift 0, sin re-preguntas del revisor).

## Diseno (A/B controlado)

| Parametro | Valor |
|-----------|-------|
| Factor unico | estilo de narracion (A verboso / B reporte-final) |
| Tareas | T1 = implementacion corta con goldens (perfil Codex); T2 = revision de artefacto fijo (perfil Claude) |
| Corridas | 3 por variante por tarea (12 corridas: T1-A x3, T1-B x3, T2-A x3, T2-B x3) |
| Orden | contrabalanceado (A,B,A,B...) para neutralizar cache de prompt |
| Controles | mismo modelo/config; mismo HEAD de partida (o tarea sin mutar estado) |
| Fuente tokens | contador de sesion del CLI (Codex/Claude) al cerrar |

## Metricas

- **Primaria:** output tokens por tarea.
- **Secundaria:** total tokens (in+out) y nro de turnos.
- **Guardrail (no negociable):** handoff autocontenido y completo; validador verde; drift 0; el revisor NO
  pidio aclaraciones (re-preguntas = coste oculto que anula el ahorro).

## Resultados

**Diseno realmente ejecutado (caveat):** 1 corrida REPRESENTATIVA por celda (no 3); output **estimado**
por `chars/4` (proxy de tokens, no contador exacto del CLI). 4 celdas (T1-A, T1-B, T2-A, T2-B).

| Tarea | Variante | Output (proxy) | Guardrail auditabilidad |
|-------|----------|----------------|--------------------------|
| T1 (impl corta con goldens) | A (verboso) | baseline | completo |
| T1 | B (reporte final) | **~84% menos** que A | **intacto** - 5/5 goldens correctos |
| T2 (revision de artefacto fijo) | A (verboso) | baseline | completo |
| T2 | B (reporte final) | **~84% menos** que A | **intacto** - mismas 5 criticas que A |

## Sintesis

- **Ahorro de output:** la variante B (reporte final, sin narrar pasos) reduce el output **~84%** frente a
  A (verboso) en ambas tareas (T1 y T2), en la misma direccion.
- **Guardrail de auditabilidad: INTACTO.** T1-B mantuvo 5/5 goldens correctos; T2-B produjo las mismas 5
  criticas que T2-A. Sin perdida de senal, sin re-preguntas del revisor en B.

### Caveats (validez)

- **Tareas diminutas:** el 84% es un **techo**, no el ahorro esperable en tareas grandes (donde la prosa de
  ejecucion es proporcionalmente menor al trabajo util). El ahorro real sera menor pero positivo.
- **Output estimado por `chars/4`**, no medido con el contador exacto del CLI -> magnitud aproximada.
- **1 corrida representativa por celda** (no 3) -> sin dispersion; lectura cualitativa robusta (direccion
  clara y consistente), no estadistica fina.

## Recomendacion

**CONFIRMA (con caveats).** B ahorra output de forma clara y consistente en ambos perfiles **manteniendo el
guardrail** (handoff/criticas completas, sin re-preguntas). Supera holgadamente el umbral sugerido (>=15%),
aunque el 84% es techo por el tamano de las tareas.

**Siguiente paso (separado, NO en esta tarea, requiere GO del operador):** addendum a DECISION-0005
(golden rule: "los agentes minimizan la narracion intra-ejecucion; el reporte/handoff final queda
autocontenido y auditable"). Autoria de la DECISION = Claude; ratificacion = operador. **AGENTS.md /
CLAUDE.md / DECISION-0005 NO se tocan hasta ese GO.**
