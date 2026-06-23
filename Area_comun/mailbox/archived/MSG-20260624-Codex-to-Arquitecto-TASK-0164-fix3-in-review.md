---
message_id: MSG-20260624-Codex-to-Arquitecto-TASK-0164-fix3-in-review
task_id: TASK-0164
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0164 CAMBIO2 entregado: mid-file torn JSONL con evento valido posterior ahora falla cerrado sin truncar ni aplicar; tail-torn sigue reparando. Handoff: Area_comun/handoffs/HANDOFF-TASK-0164-codex-to-arquitecto-3.md"
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0164-codex-to-arquitecto-3.md
  - runtime/eventlog.py
  - examples/intent_tx_cases/run_intent_tx_cases.py
  - 434b2e9
deadline_or_blocking_level: normal
---

# TASK-0164 fix3 in_review

Implementado y listo para review.

Resumen: `truncate_torn_jsonl_tail` conserva la reparacion de tail-torn, pero si encuentra una linea JSONL invalida/no-objeto con un evento valido posterior, rechaza con error de integridad y no trunca el log.

Evidencia principal:
- `python -m py_compile runtime/eventlog.py runtime/submit_intent.py examples/intent_tx_cases/run_intent_tx_cases.py` PASS.
- `python examples/intent_tx_cases/run_intent_tx_cases.py` PASS 10/10.
- `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` PASS 8/8.
- encoding, neutrality, validate OK.
- drift false antes de entrega: `up_to_seq=1478`.

Nota: `--with-secrets` no existe en el validador actual.
