---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-escala-breakeven-99u
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-b0reuse-quita-b1literal-sigue-grid.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-rubric-enrutado-peon-vs-codex.md
one_line_summary: "CELDA ESCALA CERRADA (TASK-0010 ratificada; doneflip mecanico en cola): EL CRUCE EXISTE. Lote 50: directo 131340 vs delegado-B0reuse-7b 142341 (gap +8.4 pct, venia de +24 a lote 10 y +102 con spec fresca). Marginales: delegado ~956 tokens/unidad BAJO el directo ~1180 -> BREAK-EVEN EXTRAPOLADO ~99 UNIDADES POR EXEC. QC-BOUNCE VALIDADO: 5 bounces desliz (mismo feedback de 22 tokens corrigio los 5), 0 techos, 0 correcciones de codigo del maker, 50/50 aceptados. RUBRIC calibrado (acierto parcial: bounce-apta SI, per-unit-cae fue solo marginal). Caveats: 2 puntos por brazo, proxy 3b en el intercepto delegado, 1 corrida por celda. Siguiente: T3 con spec MIA (topologia aplanada completa)."
---

# REPORTE - Celda ESCALA: el cruce existe (~99 unidades/exec)

## Numeros (tokens frontier, mismo instrumento)
| Brazo (lote 50) | Frontier | Per-unit | Detalle |
|---|---:|---:|---|
| Directo | 131340 | 2627 | 50 tests + regresion verdes, 1 iteracion |
| Delegado 7b B0-reuse + QC-bounce | 142341 | 2847 | 10 llamadas (2 por bloque con bounce), 5 bounces DESLIZ, 0 techo, 0 correcciones de codigo, 50/50 aceptados post-bounce |

## La curva del gap (todo el grid T1-escala)
spec fresca lote 10: +102 pct -> spec sunk lote 10: +24 pct -> spec sunk lote 50: +8.4 pct.

## Break-even (tu pregunta del GO)
- Marginal por unidad (ajuste 2 puntos por brazo): directo ~1180, delegado ~956. **El marginal
  delegado esta POR DEBAJO: el cruce existe.**
- **Break-even extrapolado: ~99 unidades por exec.** A lotes de ~100+ unidades de una familia
  con spec sunk, delegar al peon cuesta MENOS frontier que hacerlo directo -- ademas de
  descargar el trabajo mecanico del maker.
- Caveats de honestidad: ajuste lineal con 2 puntos; intercepto delegado usa el punto reuse-3b
  de T1 como proxy (mezcla peones); 1 corrida por celda (indicativo, no estadistico); demo NO
  citable. Si quieres el punto confirmatorio, una corrida a lote 100 en ambos brazos lo
  decide empiricamente (~0.3M frontier extra); la dejo como celda OPCIONAL a tu criterio.

## QC-bounce (primera celda con topologia aplanada completa): VALIDADO
El patron de fallo fue uniforme (el peon preferia el ejemplo de la spec sobre las filas de
parametros de su bloque) y UN feedback identico de 22 tokens lo corrigio las 5 veces. El
bounce barato sustituyo por completo a la correccion cara del maker. Leccion para la spec
peon-ready: mover los parametros del bloque ANTES del ejemplo (lo aplico en mis specs T3/T4).

## Rubric calibrado (tasa de acierto, honesta)
Prediccion ex-ante de escala: "bounce-apta, <=1 correccion por bloque; per-unit delegado CAE
bajo el directo". Resultado: bounce-apta SI (mejor de lo previsto: 0 correcciones); pero el
per-unit TOTAL no cayo bajo el directo a lote 50 -- solo el MARGINAL. Acierto PARCIAL,
registrado en el rubric v0.2 (hub, personal/Arquitecto/RUBRIC-enrutado-peon-vs-codex.md).

## Estado y siguiente
TASK-0010 ratificada review_approved; doneflip mecanico en cola (lo confirmo en el proximo
reporte). Grid: 11 celdas medidas, ~1.45M frontier acumulado. Siguiente: T3 (formatter sobre
el contrato real de query_memory_db; PRIMERA celda con spec peon-ready autorada POR MI --
added-spec lado Arquitecto medido; prediccion ex-ante: zona Codex, el peon no pasa ni con
bounce x2); luego T4 ceiling y B2. Demo privada, NO citable. Fondo intacto: N=500, 2E35F26E,
1.14.0.

-- Arquitecto. Hora local 03:15 (UTC+2, 18-jul).
