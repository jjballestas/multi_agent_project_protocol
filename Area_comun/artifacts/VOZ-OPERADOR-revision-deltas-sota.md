> Voz HUMANA del analisis multi-voz de TASK-0109. Entregada por el operador, colocada por Claude
> (consolidador) sin alterar el contenido (solo normalizacion de codificacion UTF-8). Una de las 3
> voces independientes; no leyo a las otras (maker != checker).

# Voz del Operador — Análisis de los deltas SOTA (revisión multi-agente)

**Autor:** Operador (Jball), con asistencia de Cowork
**Fecha:** 2026-06-13
**Insumo analizado:** ESTUDIO Haiku (Análisis A) + propuesta DECISION-0031 (borrador) + SPEC-0078
**Tipo:** análisis (sin código). Independiente; no leí las otras voces (maker≠checker).

## Veredicto (5 líneas)

El estudio aporta dirección útil, pero **no está listo para grabar**: dos de sus deltas malinterpretan
sus fuentes y varios números no están verificados. Mi postura es **cauta**: **TASK-0106 espera** a que
la revisión de 3 voces verifique las fuentes y derive los umbrales de **nuestra propia medición**, no de
papers. Cuando se implemente, será **off-by-default + medir antes/después** (patrón slim-views). Y una
regla innegociable: **ningún cambio de estado fuera de `submit_intent`** (escritor único).

## Prioridad por el dolor real (no por elegancia SOTA)

El dolor concreto es que **el contexto del arquitecto se llena dentro de una sesión larga** (acumulación
de turnos/handoffs/salida de herramientas). Lo que mueve la aguja ahí, en orden:

1. **Tool-result clearing** (no reinyectar stdout/tool-output crudo de turnos previos) — alto valor, bajo
   riesgo. Es lo más directo contra el dolor.
2. **Límites de summary más bajos** (DELTA-4, ~1200) — barato y sensato.
3. **Trigger de consolidación explícito** (idea de DELTA-2) — valioso, pero su cadencia debe salir de
   nuestra medición, no del "cada 10 tool calls" mal atribuido a Focus.
4. Lo demás (umbrales tipo DELTA-1, edición atómica DELTA-3) — no ataca el dolor inmediato o es riesgoso.

## Tolerancia a riesgo

- **No implementar todavía.** Primero la revisión multi-agente verifica fuentes y cierra dudas
  (respuesta "más evidencia primero").
- Cuando se implemente: **off-by-default**, y solo se promueve si la **medición propia** confirma el
  ahorro (como hicimos con slim-views: 17.392 → 8.819 real).
- **Nada de encender en caliente** sin medición previa.

## Meta-criterio (innegociable)

No se graban en SPEC/AC/golden cases números que no estén verificados. Los umbrales y metas salen de
`measure_context_cost` (DECISION-0008), no de citas. Esto es directo: hoy ya encontramos que DELTA-1 y
DELTA-2 citan mal sus papers.

## Juicio por delta (lente de valor/riesgo)

- **DELTA-1 (umbrales de degradación, "KV-cache"):** **DESCARTAR como está** — la técnica citada
  (compactación de KV-cache) no aplica a turnos CLI. Si queremos un umbral de seguridad, que sea un
  **límite de tokens de contexto ensamblado medido por nosotros**, no esto.
- **DELTA-2 (trigger de consolidación):** **REFORMULAR.** La idea sí sirve; la cadencia se define con
  nuestra medición, sin atribuirla a Focus.
- **DELTA-3 (edición atómica de CLAIMS/TASK_INDEX/DECISIONS):** **FUERA de 0106.** Solo documentar como
  futuro; si algún día entra, **exclusivamente vía `submit_intent`**. Editar estado fuera del flujo es
  justo lo que causó el drift que el arquitecto tuvo que reparar con re-genesis esta misma sesión.
- **DELTA-4 (bajar límites de summary ~1200):** **MANTENER.** Barato y alineado.
- **DELTA-5 (golden cases GC-8/GC-9):** **MANTENER la idea** de añadir cobertura, pero los asertos NO se
  construyen sobre números inventados; las metas vienen de la medición.

## Alcance para TASK-0106 (cuando llegue)

**Mínimo y seguro:** tool-result clearing + límites de summary. El trigger explícito y cualquier otra
pieza esperan a que la revisión los respalde con evidencia y medición propia.

## GO condicionado

Doy GO a Codex para implementar TASK-0106 **solo después** de que: (a) la revisión de 3 voces converja;
(b) las fuentes SOTA estén verificadas; (c) los umbrales/metas se deriven de nuestra medición; (d) DELTA-3
quede explícitamente fuera de 0106. Hasta entonces, **0106 espera**.
