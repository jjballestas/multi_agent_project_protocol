---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-techo-entrega-7b-medido
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-delegado-medir-techo-entrega-7b.md
one_line_summary: "TECHO DE ENTREGA DEL 7B MEDIDO (TASK-0020 ratificada; doneflip en cola; manual v1.3 con 5 reglas de dimensionamiento). RESULTADO NITIDO: la entrega estructural NO es el techo (10/10 bloques de 5fn completos, 50/50 funciones, 0 truncamientos, 0 omisiones); EL TECHO REAL ES DE REPARACION -- hallazgo del sello 0101 no declarado por el maker: 4 de 5 bounces devolvieron codigo BYTE-IDENTICO pese al feedback del gate en el prompt (el 7b no consume feedback correctivo). Causas raiz de las 4 familias escaladas: tipos float/round (3), off-by-one (1), forma del dato (1); NINGUNA por volumen. Calidad final 250/250 con peon 30/50 + maker 20/50. Coste como contexto: 195603 (~+43 pct vs directo; cruce sigue cerrado). Reglas nuevas al manual: bounce SOLO para deslices de formato (logica/tipos -> correccion directa sin quemar bounce), deteccion mecanica de bounce-noop por hash, spec con 'sin float' explicito."
---

# REPORTE - Techo de entrega del 7b: medido (rectificacion ejecutada)

## El resultado que pediste (medir, no opinar)
| dimension | medido |
|---|---|
| entrega estructural (bloques de 5 fn) | 10/10 completos; 50/50 funciones; 0 truncamientos (done_reason=stop 15/15); 0 omisiones |
| calidad primera pasada | 5/10 familias limpias (25/50 fn) |
| bounces | 5; SOLO 1 reparo (desliz de formato); 4 devolvieron codigo BYTE-IDENTICO |
| escalacion | 4/10 familias -> correccion minima del maker (reemplazo por su bloque del directo, byte-identico) |
| calidad final | gate 250/250 + regresion verdes; sello 0101 GO-CON-HALLAZGOS (2 MENORES) |
| coste (CONTEXTO) | 195603 vs directo 137042 (~+43 pct); el cruce sigue cerrado, no se reabre |

## El hallazgo central (del sello, invisible en el resumen del maker)
**El techo del 7b a esta escala NO es de volumen: es de REPARACION.** El peon entrega
bloques de 5 funciones estructuralmente perfectos, pero NO consume feedback correctivo:
en 4 de los 5 bounces devolvio la MISMA respuesta byte a byte aunque el prompt llevaba el
error exacto del gate ("1000.0 != 1000"). Solo el replay del sello lo revelo (el maker no
comparo la salida del bounce con la inicial; fix de proceso pedido en el doneflip:
registrar bounce-noop por hash).

## Causas raiz por familia escalada (la guia de dimensionamiento)
- Disciplina de TIPOS (3/5): round() devuelve float ("1000.0 != 1000"); el fallo dominante.
- Off-by-one de indexacion (1); malinterpretacion de la forma del dato (1).
- NINGUNA por volumen ni contexto del bloque. Y las familias del peon que pasaron van
  byte-verbatim al modulo final (30/50 funciones son 100 pct del peon).

## Reglas nuevas al manual (v1.3, s.10; estado RECOMENDACION hasta tu firma)
1. Unidades de peon hasta 5 fn/bloque: entrega estructural fiable (con sanitizador).
2. Bounce SOLO para deslices de FORMATO; fallos de logica/tipos van DIRECTO a correccion
   del maker sin quemar el bounce (el 7b re-emite lo mismo).
3. Deteccion mecanica de bounce-noop: hash de respuesta bounce vs inicial.
4. Specs para peones con aritmetica: "enteros, sin float, sin round()" EXPLICITO con
   ejemplo negativo.
5. Los contratos de division declaran modo de redondeo (el sello cazo una
   subdeterminacion de la spec por DIFF entre brazos: floor vs round-nearest, ambos
   pasan el gate; tecnica nueva de sello: comparar brazos fuera de los vectores).

## Estado
TASK-0020 ratificada (c63f5c1); doneflip mecanico en cola; con el, la instancia queda
TASK-0006..0020 (15 tareas) done y la serie cerrada DEL TODO: economia (estructural) +
dimensionamiento (medido). Manual v1.3 pusheado (fb269c7). 2 MENORES del sello y el gap
de spec quedan registrados en el veredicto. Fondo intacto: N=500, 2E35F26E, 1.14.0.
Demo privada, NO citable.

-- Arquitecto. Hora local 16:20 (UTC+2, 18-jul).
