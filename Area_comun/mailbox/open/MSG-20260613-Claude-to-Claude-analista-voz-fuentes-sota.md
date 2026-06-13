---
message_id: MSG-20260613-Claude-to-Claude-analista-voz-fuentes-sota
type: REQUEST
task_id: TASK-0109
from: Claude
to: Claude-analista
status: open
requires_response: false
response_owner: none
one_line_summary: Voz 2 de 3 (FUENTES/SOTA) de la revision adversarial de los deltas SOTA. Sesion Claude SEPARADA (la corre el operador con prompt de analista); este MSG deja registro. Verifica que los papers citados existan y que los claims cuantitativos coincidan; marca refutados. No leas las otras voces.
requested_action: (Sesion analista, orquestada por el operador) Verifica fuentes y claims de PROPUESTA-deltas-sota-spec-0078.md + ESTUDIO; entrega VOZ-ANALISTA-fuentes-sota.md en Area_comun/artifacts/ con veredicto por fuente (existe / claim coincide / refutado, voto 3-0 o 0-3).
context_refs:
  - Area_comun/artifacts/PROPUESTA-deltas-sota-spec-0078.md
  - Area_comun/artifacts/ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md
  - Area_comun/specs/SPEC-0078-compaction-y-subagentes.md
  - Area_comun/tasks/TASK-0109-claude-revision-adversarial-sota.md
---

# Voz 2/3 - FUENTES / SOTA (Claude-analista) - registro

> NOTA: esta voz la ejecuta una SESION CLAUDE SEPARADA (no el consolidador), corrida por el operador
> con el prompt de analista. Este mensaje queda en mailbox solo para dejar REGISTRO de la solicitud y
> su lente. La entrega llega como artefacto via el operador. maker != checker: no leer las otras voces.

## Tu lente: VERIFICACION DE FUENTES Y CLAIMS

La PROPUESTA cita papers y numeros que el operador sospecha mal atribuidos. Verifica, fuente por fuente:

- Existen realmente estos arXiv? Coinciden titulo/venue/fecha?
  - 2602.16284 (Attention Matching, ICML 2026)
  - 2603.18718 (MemMA, Mar 2026)
  - 2601.07190 (Focus, Jan 2026)
  - 2606.00610 (MemGraphRAG, KDD 2026)
  - 2604.01707 (Memory in LLM Era, Apr 2026)
- Coinciden los claims cuantitativos con lo que dice la fuente (no con la parafrasis de la PROPUESTA)?
  - "50x-100x compaction en 5-8k tokens; F1 degradation <5% / <15%" (DELTA-1)
  - "22.7% reduccion con consolidacion cada 10-15 tool calls" atribuido a Focus (DELTA-2)
  - "+4.82 F1 con edicion atomica ADD/UPDATE/DELETE" (DELTA-3)
  - "450-1200 tokens summary SOTA" (DELTA-4)
- Aplicabilidad (clave): el mecanismo de DELTA-1 (compactacion de KV-cache / Attention Matching) aplica
  a TURNOS CLI ensamblados, o es de otra capa (inferencia/atencion) que no toca nuestro contexto?
- Metodologia: la PROPUESTA dice "109 claims extraidos, 25 verificados, 14 confirmados 3-0, 11 refutados
  0-3". Es reproducible esa verificacion? que claims sobreviven y cuales caen?

## Meta-criterio del operador (innegociable)

Ningun numero no verificado entra a SPEC/AC/golden. Umbrales y metas salen de NUESTRA medicion
(measure_context_cost, DECISION-0008), no de citas.

## Entrega

`Area_comun/artifacts/VOZ-ANALISTA-fuentes-sota.md`: veredicto por fuente y por claim (existe/coincide/
refutado), con foco explicito en si DELTA-1 (KV-cache) aplica y si DELTA-2 (Focus) esta bien atribuido.
