---
message_id: MSG-20260622-Arquitecto-to-Operador-CHECKER-VERDE-TASK-0152
task_id: TASK-0152
type: FYI
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "CHECKER VERDE de la Fase C (TASK-0152, carga por archivo v2: agente extractor + AC45). DESDE CLON LIMPIO: npm 43/43; AC45 guard de salida de red a TODO src/** con control positivo real (src/evil.js con fetch -> violacion; git push gobernado allowlisted); AC45 purga/TTL del raw (huerfano viejo barrido); AC41 loop OFF-by-default (disabled->403), sin consent->409, con FILE_EXTRACTION_AGENT->completed-N networkEgress:false, candidatas CAND-* en store no-ledger. validate con/sin secretos exit 0; #4 byte-identica; drift 0. NO cerrado: DECISION-0056 exige PASADA DEL ANALISTA -> ya deje la INSTRUCCION para el Analista en open/ (MSG-...-REVISAR-TASK-0152-faseC con 6 vectores). ACTIVALO; con su OK cierro la Fase C. USO VIVO del extractor = GO APARTE tuyo."
context_refs:
  - Area_comun/tasks/TASK-0152-codex-file-intake-v2-faseC.md
  - Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0152-faseC.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
deadline_or_blocking_level: normal
---

# CHECKER VERDE - Fase C (TASK-0152) + instruccion del Analista lista

Reproduje la entrega de Codex (Zeus 63a80ee) DESDE CLON LIMPIO. Verde:
- **AC45 guard a TODO src/**:** `collectSourceFiles()` recorre todo `src/**`; control positivo real: un
  `src/evil.js` con `fetch("https://evil...")` -> violacion `{file:"src/evil.js",reason:"fetch"}`; el git push
  gobernado queda allowlisted. Falsable, no estatico-verde.
- **AC45 purga/TTL del raw:** un raw huerfano con timestamp viejo + `rawUploadTtlMs` -> barrido (assertMissing);
  purga al estado terminal de la candidata (approved/discarded).
- **AC41 loop:** OFF-by-default (server disabled -> 403); sin consentimiento -> 409; con `FILE_EXTRACTION_AGENT`
  -> 200 `completed-N`, **`networkEgress:false`**, frontera `agent_extractor_explicit_consent`, candidata
  `CAND-*` con `source_file_sha256` escrita al store no-ledger. Provider `deterministic-local` (no abre SDK/socket).
- Estados de extraccion (`running/completed-N/failed/timeout-released/...`) en `candidateReview.extractionStates`,
  FUERA de TASK_INDEX/PROJECT_STATE.
- Gates: validate con/sin secretos exit 0; #4 epoca 1.14.0 BYTE-IDENTICA; drift 0; npm 43/43 clon limpio sin flake.

**NO la cierro:** DECISION-0056 cond. (i) exige la **PASADA DEL ANALISTA** (esta es la VENTANA REAL DE MODELO).
Ya deje la **INSTRUCCION para el Analista** en `Area_comun/mailbox/open/MSG-...-REVISAR-TASK-0152-faseC.md` (6
vectores: guard-a-todo-src no solo fetch, purga/TTL, loop off+consent+cero-egress, fuera del ledger, carry
AC40/AC43/AC44, #4 byte-identica). **Activa al Analista**; con su OK cierro la Fase C.

**Uso vivo del extractor (encenderlo contra archivos reales) = GO APARTE tuyo** -- el loop entregado es provider
local determinista para CI; off-by-default (env-gated). Canal ASCII.
