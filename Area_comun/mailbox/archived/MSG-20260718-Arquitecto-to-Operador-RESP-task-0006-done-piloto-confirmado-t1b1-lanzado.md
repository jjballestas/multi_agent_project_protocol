---
message_id: MSG-20260718-Arquitecto-to-Operador-RESP-task-0006-done-piloto-confirmado-t1b1-lanzado
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-benchmark-peones-privado.md
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-piloto-eje-modo-delegacion-B0B1B2.md
one_line_summary: "TASK-0006 CERRADA (done seq 185; GO del checker claude-per-0101; tabla final A=84121 vs B0=169881, +102 por ciento, umbral 25 NO cumplido; peon 10/10 -- el coste es la ceremonia). CONFIRMO el protocolo del piloto y el eje B0/B1/B2. Re-run T1-B1 YA LANZADO (TASK-0007 ready + ACTION en la cola del CLI, commit instancia 7ba8c4b). Estimacion frontier del grid: ~22-26 execs Codex CLI."
---

# RESP - Cierre TASK-0006 + piloto confirmado + re-run T1-B1 en vuelo

## 1. TASK-0006 cerrada (canonico)
Done en seq 185, claim liberado en 186, validate 0, cero claims activos. Veredicto del checker
(claude per DECISION-0101, harness pendiente de cableado): GO -- mutacion 4/4 tests no-vacuos,
cobertura 20/20 contra las mitades pre-registradas, cero fugas de payload en 914 filas
publicables, spec-contrato cumple DECISION-0099; 1 MINOR de redaccion no bloqueante. Tabla
final: brazo A (directo) = 84121 tokens frontier; brazo B (delegado, modo B0 spec fresca) =
169881; delta +85760 (~+102 por ciento); umbral pre-declarado del 25 por ciento NO cumplido.
El peon rindio 10/10 (1 llamada, 20.2s, salida integrada identica modulo indentacion, 0
correcciones): el sobrecoste ES la ceremonia de delegar, no el peon. Demo NO citable.

## 2. Re-run T1 en B1-extractivo: LANZADO (prioridad 1 de tu directiva)
TASK-0007 registrada y promovida a ready + ACTION en la cola del Codex CLI (commit instancia
7ba8c4b; cron vivo; waiter armado). Reglas duras aplicadas en la intake:
- Extraer-no-generar: fuentes permitidas = intake de TASK-0006 + ACTION brazo-B original + como
  maximo 1 test de la mitad A copiado VERBATIM como ejemplo de patron. PROHIBIDAS: la spec B0
  (SPEC-PEON-lote-pii-mitadB.md), la salida previa del peon, y el codigo mitad-B de HEAD (que
  filtraria la respuesta).
- added-spec-tokens declarado con mapa de procedencia bloque a bloque en el artefacto del
  prompt (todo texto AUTORADO nuevo se aisla verbatim y se cuenta; ~0 = intake peon-ready).
- Base real pre-brazo-B (commit b330aee, solo mitad A integrada); suite completa verde con los
  10 tests del peon integrados; al final el archivo se RESTAURA a HEAD (cero cambio de producto
  sobre la tarea ya done).
- Asimetrias declaradas que juegan CONTRA B1 (claim acquire propio + restauracion): si aun asi
  colapsa hacia/por debajo de 84121, la conclusion "el 2x era artefacto de B0" es robusta.
Reporto B1 vs B0 (169881) vs A (84121) + added-spec-tokens en cuanto el exec cierre.

## 3. Confirmaciones que pediste
- Piloto (tiers/grid/metricas): CONFIRMADO sin ajustes de fondo. Escalera T1-T4 con gate duro
  pass/fail, eje escala, grid lean, wall-clock warm + iteraciones-hasta-verde + delta frontier
  con Codex CLI + modo de fallo, baseline de maquina anotado por celda.
- Eje B0/B1/B2 + regla dura de B1 (extraer, no generar): CONFIRMADO. Ajuste menor propuesto
  para no explotar el grid: las celdas delegadas corren por DEFECTO en B1 (el modo realista);
  B0 ya esta medido (T1 pequeno); B1-literal y B2 solo como celdas de control en T1 (lote
  pequeno y lote grande).
- added-spec-tokens instrumentable limpio: SI. El prompt reenviado es artefacto con mapa de
  procedencia; lo autorado-nuevo se aisla textual y se cuenta (aprox chars/4), verificable por
  diff contra las fuentes. Coste SUNK Arquitecto->Codex: lo registro por celda desde mis
  intakes/artefactos (declarado como aproximacion, no exacto a token).
- Estimacion de execs frontier del grid: escalera base 12 (3 tiers x 3 peones + 3 baselines) +
  eje escala 4 (T1/T2 grande x 7b + baseline) + T4 2 = 18 celdas; + ~4 celdas de control de
  modo (B1-literal/B2) + margen de re-runs por fallo => ~22-26 execs Codex CLI. La celda
  T1-pequeno-7b-B1 ya esta corriendo (TASK-0007) y se reusa en el grid.

Siguiente: al EXEC_EXIT de TASK-0007 reporto el resultado B1; en paralelo materializo el diseno
de T2/T3/T4 con sus gates duros (draft en mi area antes de registrar tareas). Fondo intacto:
N=500, config 2E35F26E, epoch 1.14.0.

-- Arquitecto. Hora local 00:30 (UTC+2, 18-jul).
