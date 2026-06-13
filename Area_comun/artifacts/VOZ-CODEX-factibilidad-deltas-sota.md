# VOZ CODEX - factibilidad

## Veredicto en 5 lineas

DELTA-1 no es implementable tal cual: KV-cache no es controlable desde un wrapper CLI; reformular a limite medido del contexto ensamblado por runtime.
DELTA-2 es factible como trigger determinista, pero "10 tool calls" debe quedar provisional y tuneable, no como baseline citado.
DELTA-3 debe diferirse: edicion atomica de estado choca con escritor unico si no pasa por `submit_intent`. Fuera de 0106.
DELTA-4 y DELTA-5 son testables si los limites y goldens se atan a medicion propia, no a numeros heredados.
Para TASK-0106 recomiendo minimo seguro: medicion, limites, clearing de tool-results, triggers provisionales y goldens estructurales.

## Juicio por delta

| Delta | Juicio | Coste | Razon tecnica |
| --- | --- | --- | --- |
| DELTA-1 umbrales | REFORMULAR | BAJA-MEDIA | El runtime solo arma contexto y llama CLI single-shot. No toca KV-cache ni atencion del backend. El equivalente real es medir `assembled_context_tokens` o proxy en `build_turn_context` y activar warning/fallback por umbral propio. |
| DELTA-2 trigger | REFORMULAR | MEDIA | Un trigger determinista por N tool calls, T minutos o tokens acumulados encaja con `orchestrator`/`runlog`. Pero N=10 debe ser cadencia inicial provisional. El overhead se mide en tiempo de construccion/consolidacion frente al wall time del turno y en delta de tokens enviados. |
| DELTA-3 edicion atomica | DIFERIR | ALTA | Editar estado directo rompe DECISION-0022. Si algun dia entra, solo via transaccion `submit_intent`, con rollback/idempotencia/drift gate. No pertenece al minimo seguro de 0106. |
| DELTA-4 limites summary | REFORMULAR | BAJA | Limite maximo de resumen es facil de probar, pero el valor debe salir de `measure_context_cost`/baseline local. No bajar a 1200 por cita externa. |
| DELTA-5 GC-8/GC-9 | IMPLEMENTABLE tras reformular | BAJA-MEDIA | Los goldens son deterministas si verifican comportamiento: clearing, referencias en runlog, warning/fallback por umbral medido. No deben afirmar F1, KV-cache ni cifras no medidas. |

## Factibilidad tecnica

DELTA-1: confirmo que el KV-cache no es tocable desde este runtime. `llm_turn_wrapper` invoca un backend por CLI; el control disponible esta antes de la llamada: que referencias, resumenes y resultados se incluyen en el prompt. El mecanismo correcto es medir el tamano del contexto ensamblado y aplicar limites configurables con warning + fallback.

DELTA-2: el trigger es viable en la capa de ensamblado/runlog. Se puede contar tool-results desde la ultima consolidacion, tiempo desde ultimo resumen y tamano estimado del contexto. `<5%` es un AC razonable como objetivo, pero solo si se valida en baseline propio; si el resumen llama otro LLM en caliente, el coste puede superar ese margen.

DELTA-3: riesgo alto porque introduce una via alternativa de escritura sobre memoria/protocolo. En modo escritor unico, cualquier mutacion auditable debe entrar por `submit_intent`. Mantenerlo como Future Work/TASK-0107 evita mezclar una mejora de contexto con un cambio de semantica del ledger.

DELTA-4/5: los tests pueden ser estables si usan fixtures: "cuando hay mas de N tool-results, el siguiente contexto no incluye cuerpos antiguos", "el runlog conserva referencia recuperable", "si tokens estimados > umbral medido, aparece warning/fallback". Lo que no debe testearse son numeros inventados o atribuidos a papers que no aplican.

## Orden recomendado para 0106

1. Anadir baseline de medicion del contexto ensamblado y overhead del turno.
2. Definir limites configurables off-by-default o conservadores.
3. Implementar clearing de tool-results antiguos preservando referencias en `runlog`.
4. Anadir trigger determinista provisional por N/T/tokens.
5. Anadir GC-8/GC-9 con asertos estructurales y umbrales derivados de medicion propia.

## Riesgos

- Perdida de contexto util por clearing agresivo; mitigar con referencias auditables en `runlog` y fallback explicito.
- Coste oculto si una consolidacion llama LLM en caliente; mitigar midiendo overhead y manteniendo el objetivo `<5%` como gate, no como supuesto.
- Drift o doble-escritura si DELTA-3 se implementa fuera del runtime; mitigar exigiendo `submit_intent`.
- Specs/goldens fragiles si congelan numeros no medidos; mitigar con `measure_context_cost` baseline antes del freeze.
