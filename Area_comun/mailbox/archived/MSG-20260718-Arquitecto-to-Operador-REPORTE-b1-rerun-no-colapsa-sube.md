---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-b1-rerun-no-colapsa-sube
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-eje-modo-delegacion-B0B1B2.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-RESP-task-0006-done-piloto-confirmado-t1b1-lanzado.md
one_line_summary: "RESULTADO re-run T1-B1: el 2x NO colapsa -- SUBE. B1 = 279172 tokens frontier (vs B0 = 169881, A = 84121) CON added-spec-tokens = 0 verificado (extraccion pura, mapa de procedencia limpio). El peon SIN spec calibrada FALLO (3 llamadas: siguio el wrapper de gobernanza, invento un helper incompatible, se nego por falta de detalle); el maker corrigio los 10 tests el mismo. Lectura: la spec fresca de B0 NO era ceremonia desperdiciada -- es la condicion de rendimiento del peon (con ella: 10/10 en 1 llamada). Tesis 'el 2x era artefacto de B0': REFUTADA en T1. Demo NO citable."
---

# REPORTE - Re-run T1 en B1-extractivo: resultado y lectura

## Numeros (tokens frontier del exec, mismo instrumento Codex CLI)
| Condicion | Tokens frontier | Notas |
|---|---:|---|
| A directo | 84121 | maker escribe los 10 tests |
| B0 delegado, spec fresca | 169881 | peon 10/10 en 1 llamada, 20.2s, 0 correcciones |
| B1 delegado, extractivo | 279172 | added-spec-tokens = 0; peon fallo; maker corrigio 10/10 |

## Que paso en B1 (el hallazgo esta en el POR QUE)
- La extraccion fue LIMPIA: regla dura cumplida, 0 caracteres autorados nuevos, mapa de
  procedencia bloque a bloque verificable (intake TASK-0006 + ACTION brazo-B + 1 test mitad-A
  verbatim como patron). La metrica added-spec-tokens se instrumento sin friccion.
- El peon (3 llamadas, 259.8s total, arranque cold declarado) NO produjo codigo integrable:
  llamada 1 siguio el wrapper de gobernanza y devolvio una spec en vez de tests; llamada 2 (sin
  wrapper) dio estructura + 2 ejemplos pero invento un helper incompatible y metio una clave
  fuera de la mitad; llamada 3 se nego pidiendo mas detalle. 0 de 10 tests aceptados tal cual;
  el maker corrigio/escribio los 10 (suite 42 verde al primer intento; archivo restaurado a
  HEAD, cero cambio de producto).
- CONCLUSION: la intake anti-vibecoding es peon-ready para un maker FRONTIER, no para un 7b.
  La spec fresca de B0 es precisamente el trabajo de calibracion que hace util al peon. En la
  practica B1 degenero a brazo-A + ceremonia de peon fallido encima.

## Caveats declarados (honestidad del numero)
- El 279172 esta CONTAMINADO AL ALZA por un blocker de cierre ajeno al modo: el flip a
  in_review fallo por matriz de capabilities (mi error de registro: type analysis con owner
  implementer no tiene flip posible; el gate del runtime actuo bien, cero mutacion parcial) y
  el exec gasto tokens en diagnostico + handoff + MSG blocked. Fraccion no separable del log.
- Aun descontando ese overhead con generosidad, B1 NO baja de la zona de B0 y queda lejos de
  colapsar hacia 84121. Y el hallazgo cualitativo (peon 0/10 sin spec calibrada) es
  independiente del numero.
- Cierre canonico de TASK-0007 en curso (release -> type-fix a feature con rastro -> flip ->
  ratificacion -> done); reporto al cerrar.

## Implicacion para el grid (propuesta)
- B1 puro muere en T1: mantenerlo solo como control barato donde ya este pagado.
- El modo interesante pasa a ser B2 (triage: extraer solo si el peon puede, spec si no) y una
  celda nueva propuesta: **B0-reuse** -- reutilizar la spec B0 YA ESCRITA de una familia de
  tareas repetida (coste marginal de spec ~0 Y peon rindiendo). La amortizacion real parece
  estar en la REPETICION de la familia, no en la extraccion. Si confirmas, la incorporo al
  grid (reemplaza las celdas B1-literal, que tras este resultado ya no aportan: si el extracto
  limpio confundio al peon, la intake cruda con ruido solo puede ser peor -- lo dejo a tu
  criterio).

Fondo intacto: N=500, config 2E35F26E, epoch 1.14.0. Demo privada, NO citable.

-- Arquitecto. Hora local 00:55 (UTC+2, 18-jul).
