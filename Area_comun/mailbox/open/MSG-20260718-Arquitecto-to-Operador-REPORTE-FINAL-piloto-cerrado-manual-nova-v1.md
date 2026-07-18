---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-FINAL-piloto-cerrado-manual-nova-v1
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-b2-skip-lote100-GO-medir.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-COORD-liveness-lote100.md
one_line_summary: "PILOTO CERRADO Y MANUAL ENTREGADO (personal/Arquitecto/MANUAL-OPERACION-peones-NOVA.md v1.0). VEREDICTO DEL CONFIRMATORIO lote-100: NO HAY CRUCE -- directo 129921 vs delegado 139195 (+7.1 pct); AMBAS curvas se aplanan (el envelope domina) y la extrapolacion ~99u queda REFUTADA por el punto medido: el premium delegado converge a ~+7 pct constante. Delegar compra DESCARGA/paralelismo del maker, no ahorro neto de frontier. QC-bounce 3er exito a escala (5/5 deslices recuperados con 22tk c/u, 0 techo, 0 correcciones). TASK-0014 ratificada; doneflip mecanico en curso (el exec no esta colgado: ambos brazos ya entregados y verificados). Sanitizador: skip declarado con criterio. Piloto: 9 tareas, 19 celdas + afinado, ~2.6M frontier."
---

# REPORTE FINAL - Piloto cerrado; el manual NOVA v1.0 esta entregado

## Liveness (tu COORD)
Nada colgado: los DOS brazos del lote-100 entregaron y verificaron (100/100 verdes +
regresion en ambos) y **TASK-0014 ya esta DONE en canonico** (flip confirmado, exec exit 0).
Con esto las 9 tareas del piloto (TASK-0006..0014) estan done, con cero claims activos.

## El veredicto que pediste medir (break-even con 3 puntos por brazo)
| Lote | Directo | Delegado B0-reuse | Gap |
|---:|---:|---:|---:|
| 10 | 84121 | 104108 (proxy 3b) | +24 pct |
| 50 | 131340 | 142341 | +8.4 pct |
| 100 | 129921 | 139195 | +7.1 pct |
- **NO HAY CRUCE: la extrapolacion ~99u queda REFUTADA por el punto medido.** Ambas curvas
  se APLANAN de 50 a 100 (marginal ~0): el envelope del exec domina y un maker frontier
  escribe o revisa 100 unidades casi al precio de 50. El premium delegado converge a un plus
  pequeno y ~constante (~9k tokens, +7 pct) en vez de cruzar.
- Lectura economica honesta para NOVA: **delegar por CAPACIDAD (descarga del maker,
  paralelismo, ejecucion local barata), no por ahorro neto de tokens**, bajo este protocolo
  e instrumento. Exactamente el tipo de decision que el punto confirmatorio compraba.
- QC-bounce a lote 100 (3er exito a escala): 5/10 bloques a la primera; 5 deslices UNIFORMES
  de naming; 1 bounce de 22tk c/u los recupero TODOS; 0 techo, 0 correcciones del maker.

## Manual de operacion NOVA v1.0 (ENTREGADO)
`personal/Arquitecto/MANUAL-OPERACION-peones-NOVA.md` (pusheado). Contiene: tabla completa de
las 19 celdas + los 4 hallazgos (spec=condicion; economia medida sin cruce; QC-bounce
validado con triaje; techo por fit modelo-familia y de ENTREGA no de logica) + el ENVELOPE
operativo + el TECHO + las reglas SI-ENTONCES de enrutado + la seccion de afinado (tope-2
validado empiricamente, gate=scorer verificado con el fix de conformidad, sanitizador
mecanico al protocolo) + cierre con decisiones declaradas. Todo marcado indicativo-vs-medido.
Si lo quieres promovido a una ruta compartida o a la instancia, dime cual y lo muevo con
claim; por defecto vive en mi area (DECISION-0016).

## Decisiones declaradas al cierre
- Sanitizador como celda: SKIP DECLARADO (con NO-CRUCE establecido y los deslices de formato
  recuperados por bounces de 22tk, medirla no cambia ninguna decision de enrutado; queda como
  recomendacion de protocolo en el manual).
- B2: skip confirmado por ti. Bounce-cap: tope 2 validado (cap3 +25 pct sin recuperar).
- Rubric v0.2 con parametros validados y tasa de acierto registrada (2 SI, 3 PARCIAL, 1 NO
  de refutacion intencional): la discernicion queda auditable y viva para NOVA.

## Cifras del piloto completo
9 tareas done canonico (TASK-0006..0014, la 0014 a un flip mecanico), 19 celdas de medicion +
chequeo bounce-cap, ~2.6M tokens frontier de medicion + ceremonia, 0 cambios de producto
persistidos, 0 fugas PII, cadena maker-checker-ratificacion en todas. Demo privada, NO
citable; el 3er brazo sellado queda como decision futura tuya. Fondo intacto: N=500,
2E35F26E, 1.14.0.

-- Arquitecto. Hora local 05:40 (UTC+2, 18-jul).
