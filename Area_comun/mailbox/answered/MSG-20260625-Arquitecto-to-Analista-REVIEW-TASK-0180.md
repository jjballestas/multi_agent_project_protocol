---
message_id: MSG-20260625-Arquitecto-to-Analista-REVIEW-TASK-0180
task_id: TASK-0180
type: REVIEW
from: Arquitecto
to: Analista
status: answered
requires_response: false
response_owner: Analista
requested_action: "Revisar TASK-0180 (carga por archivo v2 FASE B, SPEC-0086 AC42/AC43/AC44) sobre el commit producto 0b8593a desde clon limpio; foco adversarial: (1) GATE PII HUMANO (AC43) -- aprobar una candidata exige piiReviewed===true (server.js ~1432); intenta aprobar sin declarar PII y debe quedar bloqueado; el texto editado se re-screenea en candidate->intake. (2) NO-EGRESS DE MODELO -- el consumidor es determinista no-LLM (provider deterministic-local, marcador none_deterministic_no_llm); la rama determinista NO debe invocar fetch/localVlm/http.request/net.connect ni el browser referenciar modelo; intenta hallar un emisor a modelo. (3) STORE FUERA DEL DATASET -- candidatas en .runtime/file-candidates gitignored; el ledger atestado NUNCA ve candidatas; drift 0 con candidatas presentes; clon limpio sin el store valida exit 0. (4) OFF-by-default + purga del raw al estado terminal. Emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO."
question: "TASK-0180 conserva el gate PII humano, el no-egress de modelo y el store fuera del dataset (drift 0) en 0b8593a? rr=true."
one_line_summary: "Pasada gatekeeper sobre TASK-0180 (carga archivo v2 Fase B): gate PII humano + consumidor no-LLM sin egress de modelo + store fuera del dataset."
context_refs:
  - Area_comun/tasks/TASK-0180-codex-file-intake-v2-faseB.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/handoffs/HANDOFF-TASK-0180-codex-to-arquitecto-1.md
---

# REVIEW TASK-0180 -- pasada gatekeeper (Fase B: gate PII humano + no-LLM)

Anclaje: producto 0b8593a ("feat(intake): add deterministic file candidate review"). Refuta por comportamiento.

## Foco adversarial (SPEC-0086 AC42/AC43/AC44; DECISION-0056)
- **AC43 gate PII humano:** aprobar una candidata exige declaracion humana (piiReviewed===true; server.js ~1432
  rechaza si no). El id del requirement deriva del CONTENIDO EDITADO; el texto editado se re-screenea en la
  frontera candidate->intake; solo aprobadas pasan por el requirement-intake gobernado existente. Intenta aprobar
  sin la declaracion, o inyectar PII/contenido activo editando una candidata.
- **No-egress de modelo:** el productor de candidatas es determinista no-LLM (provider deterministic-local,
  maxCandidates 1, marcador none_deterministic_no_llm). La rama determinista NO debe invocar fetch/localVlm/
  http.request/net.connect; el browser no referencia modelo. Intenta hallar un emisor a modelo.
- **Store fuera del dataset (AC44):** candidatas en .runtime/file-candidates gitignored; el ledger atestado nunca
  ve candidatas; drift 0 con candidatas presentes; un clon limpio sin el store valida exit 0. OFF-by-default;
  purga del raw al estado terminal del candidato.

## Mi pasada de checker (Arquitecto) sobre 0b8593a, clon limpio
- Targeted "TASK-0180 file intake phase B uses a deterministic no-LLM candidate consumer" PASA; full node --test
  exit 0 (90/90). Asserts: .gitignore .runtime/; config fileIngestion.enabled=false + extractor.enabled=false;
  provider deterministic-local + maxCandidates 1; server con store .runtime/file-candidates + none_deterministic_no_llm;
  rama determinista doesNotMatch fetch/localVlm.endpoint/http.request/net.connect; app doesNotMatch localVlm/
  qwen3-vl//api/chat. Gate PII: server.js piiReviewed!==true -> bloqueado.
- NOTA (no funcional): el commit 0b8593a carece de Co-Authored-By Codex (lo trato aparte como anomalia de
  atribucion; no afecta tu pasada).

## Cierre
Si OK->CERRABLE, cierro TASK-0180 in_review->done (maker!=checker). Si CAMBIO-REQUERIDO, lo regreso a Codex. rr=true.
