---
message_id: MSG-20260613-ClaudeAnalista-to-Claude-voz-fuentes-sota
type: REVIEW
task_id: TASK-0109
from: Claude-analista
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: Voz analista (FUENTES/SOTA) entregada. DELTA-1 y DELTA-2 MAL-ATRIBUIDOS confirmado; DELTA-3/5 MANTENER; veredicto por fuente y por delta en el artefacto. GO condicional a medicion propia.
requested_action: "Voz fuentes/SOTA entregada en artifacts/ANALISTA-deltas-sota-spec-0078.md"
context_refs:
  - Area_comun/artifacts/ANALISTA-deltas-sota-spec-0078.md
  - Area_comun/artifacts/PROPUESTA-deltas-sota-spec-0078.md
  - Area_comun/artifacts/ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md
  - Area_comun/specs/SPEC-0078-compaction-y-subagentes.md
  - Area_comun/tasks/TASK-0109-claude-revision-adversarial-sota.md
---

# Voz 2/3 - FUENTES / SOTA (Claude-analista) - ENTREGA

> maker != checker: trabaje por mi cuenta, sin leer las otras voces (Codex, Operador).
> No consolido ni decido. Este mensaje avisa que el artefacto esta listo para que el arquitecto
> lo recoja via TASK-0109.

## Entregable

`Area_comun/artifacts/ANALISTA-deltas-sota-spec-0078.md`

Contiene: veredicto en 5 lineas, tabla de fuentes (claim -> estado -> enlace), aplicabilidad por
arquitectura, evaluacion del PDF, y juicio por delta (1..5). Markdown acotado, UTF-8.

## Hallazgos clave (resumen para el arquitecto)

1. **DELTA-1 MAL-ATRIBUIDO (confirmado).** arXiv:2602.16284 es compactacion de **KV-cache en espacio
   latente** (capa de inferencia/atencion), NO aplica a TURNOS CLI ensamblados. Los umbrales ">100k" y
   "F1 <5%/<15%" **no estan en el paper**; son interpolacion del ESTUDIO. -> REFORMULAR: el mecanismo
   (warning + fallback) se mantiene; los numeros salen de measure_context_cost (DECISION-0008).

2. **DELTA-2 MAL-ATRIBUIDO (confirmado).** arXiv:2601.07190 (Focus) es un mecanismo **AGENTE-AUTONOMO**;
   no especifica "cada 10-15 tool calls". Esa cadencia es **adicion del ESTUDIO**, no del paper, y el
   22.7% no se deriva de ella. -> REFORMULAR: patron periodico determinista es correcto para
   single-writer, pero "10" es provisional/tuneable, no baseline SOTA.

3. **DELTA-3 CONFIRMADO (patron).** arXiv:2603.18718 (MemMA) valida edicion atomica ADD/UPDATE/DELETE.
   Caveat: asume 4 agentes (Meta-Thinker + Memory Manager); adoptar el patron, no la coordinacion
   multi-agente. -> MANTENER como Future Work (TASK-0107), off-by-default.

4. **DELTA-4 NO-VERIFICABLE.** arXiv:2604.01707 verificado solo 2-1 en el propio ESTUDIO; rango 450-1200
   como guia, no ley. -> DECIDIR 2000 vs 1200 por medicion propia + justificar en spec.

5. **DELTA-5 MANTENER.** GC-8/GC-9 coverage correcta. Sugerencia: GC-9 asierte sobre umbral medido, no
   heredado.

## Reclasificacion de votos del ESTUDIO

- Mantener "Verified 3-0" solo para: 2603.18718, 2502.12110, 2603.09619.
- Bajar a "patron confirmado / cifra no atribuible": 2602.16284, 2601.07190.
- No-verificables (claim generico o sin acceso): 2604.01707, 2603.10062, 2606.00610.

## Meta-criterio del operador (respetado)

Ningun numero no verificado debe entrar a SPEC/AC/golden. Detectada **contradiccion interna** en el
ESTUDIO: 6.3 pide baseline propio ANTES de TASK-0106, pero DELTA-1/DELTA-2 fijan umbrales/cadencias como
si vinieran de SOTA. La reformulacion propuesta la resuelve: deltas describen el MECANISMO; los VALORES
salen de la medicion.

## Veredicto neto (no vinculante - soy una voz)

GO condicional para TASK-0106: DELTA-3 y DELTA-5 directos; DELTA-1, 2, 4 condicionados a medicion propia
+ correccion de procedencia de fuentes. Rechazar cualquier deriva a Neo4j/LlamaIndex/servicio de memoria
persistente (rompen neutralidad y single-writer).
