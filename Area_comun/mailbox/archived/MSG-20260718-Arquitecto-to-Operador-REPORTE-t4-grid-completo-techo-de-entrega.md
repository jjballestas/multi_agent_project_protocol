---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-t4-grid-completo-techo-de-entrega
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-secuencia-techo-luego-lote100-envelope-nova.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-afinado-postT4-bouncecap-gatescorer.md
one_line_summary: "GRID COMPLETO 17/17 (TASK-0012 done). HALLAZGO T4 (refuta la prediccion): la LOGICA del 7b paso el gate de 20 asserts EN LA LLAMADA 1 (Kahn lexicografico + ciclos + ValueError); el techo fue de PROTOCOLO DE ENTREGA (fences Markdown; el bounce oscilo; la correccion no toco codigo) -> saneable con un sanitizador mecanico pre-gate. T4: baseline 100459 vs 7b 112348 (+11.8 pct). AFINADO: chequeo 2 (gate=scorer) VERIFICADO con matiz (en escala la conformidad de datos no era gateable: recomendacion = gate de conformidad derivado del bloque de datos); chequeo 1 (bounce-cap 2v3) EN EXEC (TASK-0013). RESURFACEO lote-100: parqueado, pendiente tu decision. PROPUESTA: skip DECLARADO de celdas B2 (el triage ya esta operacionalizado en el rubric). Sintesis manual NOVA en draft avanzado."
---

# REPORTE - Grid completo: el techo del peon es de ENTREGA, no de logica

## T4 ceiling (toposort determinista; gate congelado 20 asserts)
| Celda | Frontier | Detalle |
|---|---:|---|
| baseline directo | 100459 | Kahn + heap; gate 20 asserts verde a la 1a |
| 7b (spec mia ~295tk) | 112348 | LA FUNCION PASO EL GATE EN LA LLAMADA 1; fallos = SOLO fences Markdown; bounce oscilo (quita wrapper -> NameError -> wrapper de vuelta) -> tope agotado -> TECHO formal; la correccion directa NO toco codigo de la funcion |

## El hallazgo que cierra el techo (T3+T4 juntos)
La prediccion ex-ante "T4 = techo de logica" queda REFUTADA: el 7b resolvio el algoritmo
completo a la primera. El patron de fallo persistente de los peones con spec calibrada es el
PROTOCOLO DE ENTREGA (fences, labels, newline), no la logica. Implicacion fuerte para el
manual NOVA: un SANITIZADOR mecanico de salida (strip fences/prosa antes del gate, coste ~0)
habria dado PASS en llamada 1 en T4 y parte de T3 -> el techo real del peon esta MAS ARRIBA
de lo que el conteo de techos formales sugiere. Lo incorporo al protocolo del manual y
reservo "techo" para fallos de logica reales.

## Afinado (tu directiva post-T4)
- **Chequeo 2 (gate = scorer): VERIFICADO.** Evidencia cruda de todas las celdas: el patron
  es "integrar sin tocar -> gate exit 1 -> triaje"; Codex nunca re-juzgo el pass/fail que el
  gate decide. MATIZ encontrado (escala): la conformidad de DATOS (payload de la variante
  correcta) no era gateable y la cazo la lectura QC del maker -- coste frontier real.
  Correccion al protocolo: derivar los asserts de conformidad del bloque de datos para que
  el gate tambien cubra esa dimension (vuelve gateable lo que hoy es lectura).
- **Chequeo 1 (bounce-cap 2 vs 3): EN EXEC** (TASK-0013, re-run de la celda T3-7b con tope 3,
  unica condicion cambiada). Nota: el dato T4 (bounce oscilante en formato) sugiere que el
  bounce 3 SI podria recuperar celdas de fallo-formato; veredicto empirico en el proximo
  reporte.

## Decisiones que te resurfaceo (como pediste)
1. **Lote-100 confirmatorio del break-even (~0.3M frontier): PARQUEADO.** Con el techo ya
   medido, mi lectura: las familias que pasan el rubric en NOVA son T1-like y el break-even
   ~99u es accionable como INDICATIVO; el punto confirmatorio pagaria certeza, no direccion.
   Tu decides si se corre.
2. **Celdas B2 (triage): propongo SKIP DECLARADO.** El triage ya esta operacionalizado en el
   rubric v0.2 + el si-entonces del manual (B2 mediria lo que el rubric ya hace). Sin
   objecion tuya, el grid queda cerrado con 17 celdas + el chequeo bounce-cap.

## Estado
TASK-0012 done canonico; TASK-0013 (bounce-cap) en exec; manual NOVA en draft avanzado en mi
area (tabla completa + envelope + techo + si-entonces; lo cierro con el veredicto del
bounce-cap y te lo entrego como artefacto). Grid: ~2.1M frontier / 17 celdas + afinado.
Demo privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 04:45 (UTC+2, 18-jul).
