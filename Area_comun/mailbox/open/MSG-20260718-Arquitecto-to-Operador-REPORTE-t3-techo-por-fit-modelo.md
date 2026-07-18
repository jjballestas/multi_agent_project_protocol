---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-t3-techo-por-fit-modelo
from: Arquitecto
to: Operador
type: REPORTE
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-secuencia-techo-luego-lote100-envelope-nova.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-REPORTE-escala-breakeven-99u.md
one_line_summary: "TRAMO T3 COMPLETO (TASK-0011 ratificada; doneflip en cola) + ACUSO tu directiva de secuencia (techo primero; lote-100 PARQUEADO y lo resurfaceo al cierre de T4; sintesis final = MANUAL DE OPERACION NOVA con envelope + techo + si-entonces). HALLAZGO T3: el techo NO es uniforme por tamano, es por FIT modelo-familia -- los qwen tocaron techo ESTRECHO (2 bounces, el 2o reintrodujo el defecto, 1 correccion minima del maker) pero deepseek-6.7b PASO con 1 bounce y 0 correcciones. Frontier en banda estrecha (112-134k vs baseline 119k): en T3 delegar no ahorra, pero descarga trabajo mecanico con riesgo contenido. Primera celda con spec MIA: added-spec Arquitecto ~440tk, added-spec Codex 0 (verbatim, sha unico). T4 ceiling arranca YA."
---

# REPORTE - Tramo T3: el techo es por fit modelo-familia

## Acuse de tu directiva de secuencia
Confirmo: T3 listo (este reporte), T4 arranca ya; el lote-100 queda PARQUEADO y lo resurfaceo
como decision pendiente en el reporte de cierre de T4; la sintesis final la oriento como
MANUAL DE OPERACION para NOVA (envelope + techo + reglas si-entonces, con lo indicativo
claramente marcado frente a lo medido).

## Tabla T3 (formatter sobre el contrato real de query_memory_db; gate congelado 29 asserts)
| Celda | Frontier | Peon | QC |
|---|---:|---|---|
| baseline directo | 119418 | - | PASS (incluye autorar el gate) |
| qwen 7b (spec mia) | 112109 | 3 llamadas, 2 bounces DESLIZ, 2o bounce reintrodujo el defecto | TECHO declarado; 1 correccion minima del maker (prefijo mode) |
| qwen 3b (spec mia) | 117117 | mismo patron que 7b | TECHO; 1 correccion minima (label + newline) |
| deepseek 6.7b (spec mia) | 133837 | 2 llamadas, 1 bounce DESLIZ | PASS SIN correcciones (unico peon que supero T3 por bounce puro); su exec incluye el cierre del tier |

## Hallazgos
1. **El techo no es por tamano sino por FIT modelo-familia**: deepseek fue el mas debil en
   formato (T1) y el mas capaz en logica-formato compuesta (T3); los qwen al reves. Para el
   manual NOVA: el enrutado optimo elige PEON POR FAMILIA de tarea, no un peon universal.
2. **El techo de los qwen en T3 fue ESTRECHO, no catastrofico**: fallos locales de formato
   (1-2 propiedades), cero estructura inventada. La spec peon-ready con parametros-antes-del-
   ejemplo (leccion de la escala) elimino el modo de fallo grave de B1. El triaje
   desliz-vs-techo del bounce funciono: los 2 topes se declararon TECHO correctamente cuando
   el bounce 2 reintrodujo defectos.
3. **Economia en T3**: banda estrecha 112-134k vs baseline 119k -> delegar en T3 no ahorra
   frontier, pero tampoco castiga (a diferencia de B1 +102), y descarga el trabajo mecanico.
   added-spec del Arquitecto ~440tk (una vez, reutilizable); added-spec de Codex = 0 real
   (prompt sha unico verificado en las 3 celdas).
4. Rubric calibrado: prediccion "zona Codex" ACERTADA en direccion para qwen, FALLADA para
   deepseek -> acierto PARCIAL registrado; el filtro 1 se refina con dimension de fit
   modelo-familia.

## Estado y siguiente
TASK-0011 ratificada review_approved; doneflip mecanico en cola. Grid: 15 celdas medidas,
~1.9M frontier acumulado. AHORA: T4 ceiling (toposort determinista con ciclos y desempate
lexicografico; gate >=15 asserts; baseline + 7b con spec mia ya autorada ~295tk). Al cerrar
T4: reporte de techo completo + resurfaceo lote-100 + arranco la SINTESIS (manual NOVA).
Demo privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 04:05 (UTC+2, 18-jul).
