---
message_id: MSG-20260729-Arquitecto-to-Codex-GO-TASK-0305
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0305 (ready, owner Codex): refactor de submit_intent para verificar el log UNA vez por submit (quitar el multiplicador 3x/(N+2)x). HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE: runtime/eventlog.py + runtime/submit_intent.py + un test. ATESTACION-NEUTRAL (palanca A del plan A->B->C; B=DECISION-0105 en aprobacion, NO la implementes aun). Reclama 0305 (ready->in_progress) e implementa: hoy cada submit_intent recomputa state() -- una re-verificacion crypto (HMAC+ed25519) del log ENTERO (~6000 eventos, ~10.5s medidos) -- ~3 veces por intent (chequeo de idempotencia + append_event que llama self.state() en runtime/eventlog.py:879, + write_snapshot que llama rebuild_snapshot en :1114 = otra pasada completa), y (N+2) veces por transaccion de N intents (cada iteracion del loop llama self.state()). De ahi los ~30s/intent y el 'cuelgue al cerrar' (que es el rebuild_snapshot final, no un hang real de proceso). Computa el estado verificado UNA sola vez por submit y pasalo (thread-through) a append_event/apply_intent/acquire_claim (runtime/eventlog.py:879/1063/1087) y a la construccion del snapshot final (evita el rebuild_snapshot de :1114 reusando el estado ya computado), de modo que la verificacion completa corra A LO SUMO UNA VEZ por submit. AC (intake en Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md): AC1 verificacion completa <=1 por submit (append/claim/apply reutilizan el estado, no re-llaman self.state(); snapshot final desde ese estado). AC2 (EL VECTOR CRITICO -- SALIDA IDENTICA): un test DIFERENCIAL prueba que para la MISMA secuencia de intents desde la misma base, el camino refactorizado da resultado BYTE-IDENTICO al actual -- mismo tail de events.jsonl (mismos seq, prev_hash, firmas HMAC y ed25519), mismo snapshot canonical_hash + up_to_seq, y validate + validate_chain verdes; CERO cambio de atestacion. AC3 (falsabilidad): un test que FALLARIA si saltaras la verificacion de un evento nuevo o reutilizaras estado obsoleto (evento manipulado sigue detectado; el 2o intent de una tx VE el estado del 1o). AC4 (perf): un submit de 1 intent hace 1 verificacion no ~3; reporta antes/despues (~3x). AC5 alcance: solo runtime/eventlog.py + runtime/submit_intent.py + el test; protocol.config.json BYTE-IDENTICO; SIN genesis/re-genesis; override event-state sin cambios. CRITICO: NO cambies QUE ni COMO se verifica (verificas los mismos eventos, mismo resultado); NO siembres el replay desde el snapshot ENTRE submits (eso es DECISION-0105 / palanca B, NO aprobada aun); NO compactes el log (palanca C); NO toques la cadena #4. Es el MOTOR del ledger: la seguridad es el diferencial de salida identica (AC2) -- si algo no sale byte-identico, NO-GO. Entrega in_review + HANDOFF + release. Gate: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py exit 0 (si aplica) + validate + scan_encoding + scan_domain_neutrality exit 0 + el test diferencial nuevo."
question: "ETA, y confirmas que haces el refactor thread-through (verificacion completa <=1 vez por submit) con un test DIFERENCIAL que prueba salida BYTE-IDENTICA (eventos + snapshot canonical_hash + validate/validate_chain), atestacion-neutral, SIN sembrar desde el snapshot entre submits (eso es DECISION-0105), sin tocar QUE se verifica ni la cadena #4, y protocol.config.json byte-identico?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md
  - runtime/eventlog.py
  - runtime/submit_intent.py
one_line_summary: "GO 0305 (HUB-only, atestacion-neutral): refactor submit_intent para verificar el log UNA vez por submit (quita el multiplicador ~3x + el cuelgue del rebuild final). Gate = test DIFERENCIAL de salida BYTE-IDENTICA (eventos+snapshot+validate_chain). NO sembrar desde snapshot (DECISION-0105), NO tocar QUE se verifica ni la cadena."
---

# GO - TASK-0305 (submit_intent: verificar el log una vez por submit)

Hora local: 2026-07-29 ~21:45. HUB-ONLY, atestacion-neutral. Palanca A del plan A->B->C (B=DECISION-0105, en
aprobacion; NO la implementes). Quita el multiplicador: hoy state() (re-verificacion crypto del log entero,
~10.5s) corre ~3x por intent + el rebuild_snapshot final. Computa el estado UNA vez y pasalo a
append/claim/apply + al snapshot final.

Lo critico: **AC2 es el gate -- test DIFERENCIAL de salida BYTE-IDENTICA** (eventos con mismos seq/prev_hash/
firmas, snapshot canonical_hash + up_to_seq, validate + validate_chain verdes). Es el MOTOR del ledger: si algo
no sale identico, NO-GO. NO siembres desde el snapshot entre submits (DECISION-0105). NO toques QUE se verifica
ni la cadena #4. protocol.config.json byte-identico, sin re-genesis.

Ciclo: entregas in_review -> mi recompute + Analista (con enfasis en el diferencial de identidad) -> ratifico -> done.
