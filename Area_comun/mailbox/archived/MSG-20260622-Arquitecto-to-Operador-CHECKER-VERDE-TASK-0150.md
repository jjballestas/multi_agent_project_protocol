---
message_id: MSG-20260622-Arquitecto-to-Operador-CHECKER-VERDE-TASK-0150
task_id: TASK-0150
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "CHECKER VERDE de TASK-0150 (carga por archivo v2 FASE A, plumbing determinista). DESDE CLON LIMPIO: AC40 no-MODELO-egress (guard estatico falsable + control positivo que atrapa imports de openai/anthropic/google + endpoints + WebSocket/node:net) + store en OS tmpdir FUERA del dataset (git ls-files vacio) + SHA-256 + emit extraction-task con contrato (incluye human-PII-review + candidate-store-outside-ledger) + off-by-default; AC42 selector de modo. npm 42/42 clon limpio; validate con/sin secretos exit 0; #4 byte-identica; drift 0. NO cerrado: DECISION-0056 exige PASADA DEL ANALISTA (ingest/egress/PII) -> ACTIVALA. Codex 5121335."
context_refs:
  - Area_comun/tasks/TASK-0150-codex-file-intake-v2-faseA.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/artifacts/REDTEAM-ingestion-v2-OPCION4-veredicto.md
deadline_or_blocking_level: normal
---

# CHECKER VERDE - TASK-0150 carga por archivo v2 FASE A (no cerrado; falta Analista)

Reproduje la entrega de Codex (Zeus 5121335) DESDE CLON LIMPIO (leccion CRLF). Verde:
- **AC40 Upload no-MODELO-egress:** test estatico falsable + **control positivo** -- el patron rechaza imports de
  `openai`/`@anthropic-ai/sdk`/`@google/generative-ai`/`ai`, `api.openai.com`/`api.anthropic.com`/
  `generativelanguage.googleapis.com`, `new WebSocket(`, `node:net|tls|dgram`; y CONFIRMA que atrapa un import
  falso (control positivo). Es el fix M3 del red-team.
- **Store FUERA del dataset (B1 resuelto):** `FILE_UPLOAD_STORE_ROOT || tmpdir()/zeus-protocol-file-intake` (OS
  temp); `git ls-files` del store = vacio (no entra al repo/atestado). SHA-256 sobre bytes (createHash). Emit
  extraction-task con CONTRATO autocontenido (source_file_sha256 + candidate_hash + "candidate store outside
  ledger" + "each candidate still requires human PII review before governed intake"). Off-by-default.
- **AC42 selector de modo** (digitado vs archivo) en el front.
- Gates: npm test **42/42 en CLON LIMPIO**; validate con/sin secretos exit 0; #4 epoca 1.14.0 BYTE-IDENTICA;
  drift 0.

**NO la cierro:** DECISION-0056 cond. (i) exige **PASADA DEL ANALISTA** (ingest/egress/PII, incl. el salto
LLM->intake) antes de cerrar. **Activa al Analista** anclando en el commit pusheado. Con su OK cierro Fase A; sin
encender vivo (OFF; activacion por env; Fases B panel+gate-PII / C agente extractor pendientes).

Codex sigue activo. Push de Zeus al remote sigue gateado a tu accion. Canal ASCII.
