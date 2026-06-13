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

## Resultados (a completar con las corridas)

| Tarea | Variante | Corrida | Output tok | Total tok | Turnos | Handoff completo | Validador | Drift 0 | Re-preguntas |
|-------|----------|---------|-----------|-----------|--------|------------------|-----------|---------|--------------|
| T1 | A | 1 | | | | | | | |
| T1 | A | 2 | | | | | | | |
| T1 | A | 3 | | | | | | | |
| T1 | B | 1 | | | | | | | |
| T1 | B | 2 | | | | | | | |
| T1 | B | 3 | | | | | | | |
| T2 | A | 1 | | | | | | | |
| T2 | A | 2 | | | | | | | |
| T2 | A | 3 | | | | | | | |
| T2 | B | 1 | | | | | | | |
| T2 | B | 2 | | | | | | | |
| T2 | B | 3 | | | | | | | |

## Sintesis (a completar)

- Media y dispersion de output tokens por variante (A vs B), por tarea.
- Porcentaje de ahorro medio de B vs A (apuntan las 3 corridas en la misma direccion?).
- Estado del guardrail de auditabilidad en B (se mantuvo en todas las corridas?).

## Recomendacion (a completar)

- CONFIRMA / NO CONFIRMA segun el criterio del operador (sugerencia: ahorro medio >=15% consistente +
  guardrail intacto). Si CONFIRMA: siguiente paso separado, con GO del operador = addendum a DECISION-0005
  (golden rule "los agentes minimizan la narracion intra-ejecucion; el reporte/handoff final queda
  autocontenido y auditable"). Autoria de la DECISION = Claude; ratificacion = operador.
