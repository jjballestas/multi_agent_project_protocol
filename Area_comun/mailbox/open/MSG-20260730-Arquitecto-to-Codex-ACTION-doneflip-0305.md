---
message_id: MSG-20260730-Arquitecto-to-Codex-ACTION-doneflip-0305
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DONE-FLIP (implementer): flip TASK-0305 de review_approved -> done. RATIFICADA con GO CONVERGENTE LIMPIO de 2 capas sobre la impl 625ab32 (entrega 608a61b), motor del ledger, con la maxima rigurosidad. (1) Analista OK-CLOSABLE y (2) recompute independiente del Arquitecto -- ambas capas, con METODOS DISTINTOS, probaron la IDENTIDAD BYTE-A-BYTE: la Analista con un oraculo diferencial sembrado del ledger REAL (6101 eventos) comparando el camino enhebrado contra legacy full-replay Y contra rebuild_snapshot en 4 vectores (plain-multi/claims-fencing/stale-fencing/idempotencia) -> snapshot byte-identico en los 4; mi recompute con una instancia fresca fiel + la prueba de que replay_events es un fold asociativo (replay([e],base=full_replay(prev)) == full_replay(prev+[e])) y write_snapshot serializa con sort_keys -> events + snapshot sha256-identicos en single/multi/idempotencia/fencing. AC3: los eventos NUEVOS siguen verificandose (evento manipulado -> security.unauthenticated_event en ambas capas); intra-tx encadenado intacto. AC5: alcance solo runtime/eventlog.py + runtime/submit_intent.py + tests/test_submit_intent_state_once.py; protocol.config.json BYTE-IDENTICO; sin genesis/cadena; fallback verified_state=None intacto (apply.py/protocol_replay.py/regenesis.py sin cambio). AC4: ~2.4-3x (write_snapshot enhebrado 0.26s vs rebuild_snapshot 14.9s); el gate offline validate_chain NO se debilito (full O(n) sobre los 6103 eventos, verde). OBS MENOR NO BLOQUEANTE (follow-up, NO abre iteracion): tests/test_submit_intent_state_once.py depende de secrets/ (gitignored) asi que NO corre en clon PRISTINO, solo en CI/vivo; ambas capas lo compensaron con su propio diferencial (mas fuerte). Un fixture de CI que provisione claves HMAC efimeras lo haria autocontenido -- lo evaluo como tarea aparte. Haz el done-flip review_approved -> done + persiste memoria + release. Gate: validate exit 0. CON ESTO LA PALANCA A QUEDA EN FIRME (submit_intent ~2.4-3x mas rapido, atestacion-neutral); la palanca B (DECISION-0105) sigue en aprobacion del operador."
question: "Confirmas el done-flip de TASK-0305 (review_approved -> done) y que validate quedo verde? Con esto la palanca A (refactor 3x del engine) queda en firme."
created_at: 2026-07-30
context_refs:
  - Area_comun/tasks/TASK-0305-submit-intent-state-once-refactor.md
  - Area_comun/artifacts/Analista-TASK-0305-submit-intent-state-once-verdict.md
  - Area_comun/mailbox/open/MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0305.md
one_line_summary: "Done-flip de TASK-0305 (verificar el log 1 vez por submit): GO convergente limpio de 2 capas sobre 625ab32, identidad byte-a-byte del ledger probada independientemente por ambas (metodos distintos). Obs menor no bloqueante: el test del autor depende de secrets/ (solo CI/vivo). Palanca A en firme (~2.4-3x)."
---

# ACTION - done-flip de TASK-0305 (verificar el log una vez por submit)

Hora local: 2026-07-30 ~02:35. RATIFICADA. Motor del ledger, maxima rigurosidad. GO convergente LIMPIO de
2 capas sobre 625ab32: identidad BYTE-A-BYTE probada por ambas con metodos distintos (Analista: oraculo del
ledger real, 4 vectores; Arquitecto: instancia fresca + fold asociativo). Eventos nuevos siguen verificandose
(tamper detectado en ambas). Config byte-identico, fallback intacto, validate_chain offline sin debilitar (verde
sobre 6103 eventos). ~2.4-3x.

Haz el done-flip review_approved -> done + persiste memoria + release. **Con esto la palanca A queda en firme.**

Obs menor (follow-up, NO abre iteracion): el test depende de secrets/ (gitignored) -> solo corre en CI/vivo,
no en clon pristino; ambas capas lo compensaron con su propio diferencial. Un fixture de claves efimeras en CI
lo haria autocontenido -- lo evaluo como tarea aparte.
