---
message_id: MSG-20260625-Arquitecto-to-Codex-GO-TASK-0181
task_id: TASK-0181
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
requested_action: "Implementar TASK-0181 (Intake modo 'necesidad', SPEC-0095, REQ-7095D30A) en Zeus-protocol como maker, OFF-by-default. Es una nueva SUPERFICIE DE ENTRADA (textarea + voz) al pipeline de extraccion YA entregado de la carga por archivo (TASK-0180); NO enciende el extractor LLM (Fase C). Entregar: (1) AC1 modo 'Necesidad' en el selector del Intake junto a Manual y Por archivo (carry AC42; obligatorios validados; design-system AC13); (2) AC2 formulario aparte con textarea grande + el control de dictado por voz REUTILIZADO de TASK-0179/SPEC-0094 (locale es-CO, captura sostenida con su control de finalizacion manual + timer + indicador, egress opt-in/off-by-default + aviso); texto escrito o dictado llena el textarea; (3) AC3 botonera estilo modo-archivo 'Extraer': el texto del textarea va como FUENTE inerte (screened best-effort PII) al MISMO consumidor determinista no-LLM (provider deterministic-local, none_deterministic_no_llm, sin fetch/localVlm/http/net) -> candidatas en el store NO-LEDGER .runtime/file-candidates gitignored (drift 0; clon limpio sin store valida exit 0); (4) AC4 revision + gate PII humano (piiReviewed===true) + aprobar -> requirement-intake gobernado (AC39), REUSANDO el panel/flujo de TASK-0180; id del requirement deriva del contenido editado; descartar purga el raw. Carries verdes: egress de voz off-by-default + aviso, no-egress de modelo, store fuera del dataset + drift 0, #4 byte-identica, AC11/AC12/AC13. behavior-tests por AC; node --test clon limpio exit 0. Mover a in_review via submit_intent (claim file-scoped) con gates verdes. Commit como Arquitecto + Co-Authored-By Codex."
question: "Tomas TASK-0181 (Intake modo necesidad dictar/escribir -> pipeline determinista -> candidatas) y entregas a in_review con gates verdes? rr=true."
one_line_summary: "GO a Codex: TASK-0181 Intake modo necesidad (textarea + voz reusada de TASK-0179) -> mismo pipeline determinista de TASK-0180 -> candidatas; REQ-7095D30A; maker=Codex / checker=Arquitecto + Analista."
context_refs:
  - Area_comun/tasks/TASK-0181-codex-front-intake-modo-necesidad.md
  - Area_comun/specs/SPEC-0095-front-intake-modo-necesidad-dictado.md
  - Area_comun/tasks/req-7095d30a-requirement-seed.md
  - Area_comun/tasks/TASK-0180-codex-file-intake-v2-faseB.md
  - Area_comun/tasks/TASK-0179-codex-front-dictado-voz-idioma-captura.md
---

# GO TASK-0181 -- Intake modo "necesidad" (dictar/escribir) -> pipeline determinista

Origen: REQ-7095D30A (operador). Quiere un tercer modo de Intake junto a Manual y Por archivo: dictar o escribir
una **necesidad** en un textarea grande con microfono (el mismo de la opcion manual) y la botonera del modo archivo;
la necesidad va al MISMO extractor que la carga por archivo y se vuelve candidatas que acepta/rechaza/envia igual.

## Decision del operador: motor DETERMINISTA no-LLM (ya)
Se construye sobre el consumidor determinista no-LLM de TASK-0180 (1 candidata, sin egress de modelo). El extractor
LLM real (1..N, Fase C) queda gateado y FUERA de alcance; este modo hereda 1..N cuando se encienda Fase C por usar
el mismo pipeline.

## Alcance (SPEC-0095 AC1-AC4)
- AC1 modo 'Necesidad' en el selector (carry AC42, design-system AC13).
- AC2 formulario textarea grande + control de dictado de voz REUSADO de TASK-0179 (es-CO, captura manual con
  finalizacion + timer + indicador; egress opt-in/off-by-default + aviso).
- AC3 'Extraer' -> texto como fuente inerte screened -> consumidor determinista no-LLM -> candidatas en store
  NO-LEDGER .runtime gitignored (drift 0; clon limpio sin store valida exit 0); sin fetch/modelo.
- AC4 revision + gate PII humano + aprobar -> requirement-intake gobernado, REUSANDO el panel de TASK-0180.

## Cierre
maker=Codex / checker=Arquitecto clon limpio (maker!=checker) + PASADA DEL ANALISTA (PII del texto libre + egress
de voz opt-in + no-egress de modelo + store fuera del dataset). Mueve a in_review con gates verdes via
submit_intent (claim file-scoped); yo verifico, luego el Analista; cierro in_review->done. rr=true.
