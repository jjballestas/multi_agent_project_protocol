---
message_id: MSG-20260622-Arquitecto-to-Operador-CHECKER-VERDE-TASK-0151
task_id: TASK-0151
type: FYI
from: Arquitecto
to: Operador
status: archived
requires_response: false
response_owner: Operador
one_line_summary: "CHECKER VERDE de la Fase B (TASK-0151, carga por archivo v2). DESDE CLON LIMPIO: candidatas en store NO-ledger (OS tmp); GATE HUMANO DURO de PII (aprobar sin declarar PII -> 409); re-screen candidate->intake; id del contenido editado (sha256, 1 archivo->N candidatas->N REQ); flake estabilizado. npm 43/43 clon limpio; validate con/sin secretos exit 0; #4 byte-identica; drift 0. NO cerrado: DECISION-0056 exige PASADA DEL ANALISTA -> ya deje la INSTRUCCION para el Analista en open/ (MSG-...-REVISAR-TASK-0151-faseB con 6 vectores a refutar). ACTIVALO; con su OK cierro Fase B y promuevo Fase C."
context_refs:
  - Area_comun/tasks/TASK-0151-codex-file-intake-v2-faseB.md
  - Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0151-faseB.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
deadline_or_blocking_level: normal
---

# CHECKER VERDE - Fase B (TASK-0151) + instruccion del Analista lista

Reproduje la entrega de Codex (Zeus 0a5e737) DESDE CLON LIMPIO (leccion CRLF). Verde:
- **AC41 candidatas NO-ledger:** store en OS tmp (`FILE_CANDIDATE_STORE_ROOT||tmpdir()/zeus-protocol-file-
  candidates`), fuera del dataset; panel `/api/protocol/intake-candidates` (GET) + `/discard` (POST); las
  candidatas no entran a TASK_INDEX/atestado; drift 0.
- **AC43 GATE HUMANO DURO de PII:** aprobar SIN declarar PII -> 409 "candidate approval requires human PII review
  acknowledgement"; RE-SCREEN candidate->intake (redactPublicText al aprobar); **id del CONTENIDO EDITADO**
  (sha256Hex del texto editado, no del archivo) -> 1 archivo -> N candidatas -> N REQ distintos.
- **AC45 c flake estabilizado:** npm test **43/43 en CLON LIMPIO** (sin parpadeo frio-vs-caliente).
- Gates: validate con/sin secretos exit 0; #4 epoca 1.14.0 BYTE-IDENTICA; drift 0.

**NO la cierro:** DECISION-0056 cond. (i) exige la **PASADA DEL ANALISTA** (toca el gate de PII). Ya deje la
**INSTRUCCION para el Analista** en `Area_comun/mailbox/open/MSG-...-REVISAR-TASK-0151-faseB.md` (paquete estatico
autocontenido, anclado en canonico, con los 6 vectores a refutar). **Activa al Analista**; con su OK cierro la
Fase B y promuevo la Fase C (agente extractor; uso vivo = GO aparte tuyo).

Cron de monitoreo activo (9954b818): no cierra Fase B sin el Analista. Canal ASCII.
