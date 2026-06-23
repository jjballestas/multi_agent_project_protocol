---
handoff_id: HANDOFF-TASK-0164-codex-to-arquitecto-2
task_id: TASK-0164
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-23T22:25:00Z
---

# Handoff TASK-0164 - torn JSONL tail hardening

## Resultado
- Commit implementacion protocolo: `92ece27 fix(runtime): repair torn event log tail before append`.
- Commit memoria Codex: `55d4b67 chore(memory): record TASK-0164 torn-tail fix`.
- `submit_intent` y `submit_intents` inspeccionan `runtime/state/events.jsonl` dentro del lock fisico antes de idempotencia, validacion, append y materializacion.
- Si la cola JSONL contiene una ultima linea invalida/parcial, se trunca a la ultima linea valida antes de aceptar el nuevo intent. El resultado expone `log_repair`.
- El evento nuevo queda visible para `read_jsonl_torn_safe`; no puede aterrizar detras de una linea torn invisible con `applied:true`.

## Archivos cambiados
- `runtime/eventlog.py`
- `runtime/submit_intent.py`
- `examples/intent_tx_cases/run_intent_tx_cases.py`
- `personal/Codex/Memory.md`

## Evidencia
- `python -m py_compile runtime/eventlog.py runtime/submit_intent.py examples/intent_tx_cases/run_intent_tx_cases.py` OK.
- `python examples/intent_tx_cases/run_intent_tx_cases.py` OK, 9/9.
- `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` OK, 8/8 con paridad PowerShell.
- `python scripts/scan_encoding.py --root .` OK.
- `python scripts/scan_domain_neutrality.py --root .` OK.
- `python scripts/validate_collaboration_state.py --root .` OK.
- Drift: `has_drift=false`, `up_to_seq=1446` antes de la entrega.
- `git diff -- protocol.config.json runtime/state/genesis.json runtime/state/agent_registry.json runtime/state/keys.json` sin salida.
- `git diff --check` sin errores; solo aviso CRLF esperado sobre `runtime/state/snapshot.json`.

## Nota de revision
El test nuevo fuerza `events.jsonl` con una linea final parcial y luego ejecuta un `claim release`.
La aceptacion requiere que `log_repair` exista, que el evento de release sea el ultimo evento visible, que
`validate_chain` sea valido, que `prev_hash` encadene contra el evento previo visible y que drift sea 0.
