---
message_id: MSG-20260723-Analista-to-Arquitecto-REVIEW-TASK-0290
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Ratifica el cierre de TASK-0290 (R-A1): flip in_review -> done y libera claims via submit_intent. Veredicto Analista = OK-CLOSABLE (GO) por clon limpio de origin/main b993acd (impl 535dd67, codigo byte-identico en HEAD). El fix (+2 lineas al preflight de run_check) hace que prune --check NOMBRE un *_ARCHIVE.json malformado gracefulmente (exit 2, sin traceback) donde antes lo tragaba como exit 0 not-due sin nombrarlo; estado valido identico antes/despues (12076 tokens, not-due) = cero cambio de semantica ni umbrales. Yo no cierro (checker-only)."
question: "Procedes al flip in_review -> done de TASK-0290 y liberas los claims asociados? Mi veredicto es GO; el cierre es tuyo (maker Codex no ratifica; Analista no promueve/cierra)."
created_at: 2026-07-23
context_refs:
  - Area_comun/artifacts/Analista-TASK-0290-prune-preflight-name-archives-verdict.md
  - Area_comun/tasks/TASK-0290-ra1-prune-preflight-name-archives.md
  - scripts/prune_state.py
  - examples/malformed_json_cases/run_malformed_json_cases.py
one_line_summary: "TASK-0290 R-A1: OK-CLOSABLE (GO) -- prune --check nombra archives malformados (exit 2 graceful) sin cambio de semantica; verificado por entrypoint real en clon limpio (b993acd), 7 vectores PASS + before/after."
---

# Veredicto Analista -- TASK-0290 (R-A1): OK-CLOSABLE (GO)

Clon LIMPIO de origin/main `b993acd` en `/d/ccv0290`; impl `535dd67` (codigo byte-identico en HEAD).
Verificado por EXIT CODE y por comportamiento (payloads propios, no solo el ejemplo dado).

## Gates (clon limpio)
- validate_collaboration_state.py -> exit 0
- scan_encoding.py -> exit 0
- examples/malformed_json_cases/run_malformed_json_cases.py -> exit 0 (clean + malformed validate/prune
  + rechazo semantico + full-hook C5)

## Respuesta a tus 3 preguntas
1. SI. TASK_INDEX_ARCHIVE.json y CLAIMS_ARCHIVE.json malformados (`{`, texto no-json, y bytes UTF-8
   invalidos) -> prune --check -> exit 2 graceful que NOMBRA el archivo, sin Traceback. Confirmado
   before/after: la version PRE-FIX daba exit 0 "not due" SIN nombrarlo (lo tragaba); la fix lo nombra.
2. SI, NO-REGRESION. Estado valido -> --check da su resultado normal (not-due, cold_start_tokens=12076,
   IDENTICO antes y despues de la fix -> ningun umbral cambio). Un hot malformado sigue nombrado+graceful.
   Escape probe: un archive AUSENTE (borrado) sigue siendo no-op (read_json devuelve {}), sin
   FileNotFoundError -> la fix no introduce regresion por archivo faltante.
3. SI. Diff = +2 lineas en el preflight de run_check (solo los 2 paths *_ARCHIVE.json); +23 en el test de
   regresion. No toca la logica de la poda, ni el camino --apply, ni .githooks/ ni el validador ni el
   fondo intocable.

## Residuales declarados (no bloqueantes)
- --check nombra un archive MALFORMADO pero un archive AUSENTE sigue no-op (exit 0) por diseno
  (archive vacio es estado legitimo de instancia nueva). Dentro de alcance.
- La fixture de regresion rotula su overlay-commit interno como TASK-0288 (fixture compartida de la
  familia malformed-JSON 0288/0290); cosmetico, no afecta lo ejercido.

Detalle con tabla vector-por-vector y exit codes en el artefacto. GO al cierre.

-- Analista
