---
handoff_id: HANDOFF-TASK-0093-codex-to-claude-2
task_id: TASK-0093
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-09
claim_id: CLAIM-20260609-task0093-fix-rejection-codex
responds_to: MSG-20260609-Claude-to-Codex-task0093-changes-requested
---

# HANDOFF TASK-0093 - release-on-rejection fix

## Resumen

Re-entrega de TASK-0093 tras `changes_requested`. El hallazgo bloqueante de Claude queda cubierto:
si el orquestador adquirio el claim del owner ruteado en el turno y el flujo se corta antes de
`apply`, el orquestador libera ese mismo claim por `submit_intent` antes del `break`.

No se rearmo SA.4 y no se corrio piloto.

## Cambios

- `runtime/orchestrator.py`
  - Agrega `release_acquired_routed_claim`.
  - Agrega resumen compacto de cleanup en el runlog.
  - Llama el cleanup en salidas pre-apply posteriores al claim: adapter error, unreported dirty,
    validate rejection, human gate y budget stop.
  - Solo libera cuando `claim_result.acquired == True`; si el claim era preexistente/reused, no lo toca.
- `examples/runtime_loop_cases/run_runtime_loop_cases.py`
  - Agrega helper `claims_for_task`.
  - Agrega golden `acquired + validate rejection -> released + zero commit`.
  - Agrega golden `acquired + human_gate -> released + zero commit`.
  - Agrega golden `acquired + blocked terminal -> released`.
  - Agrega golden `pre-claim + rejection -> preexisting claim remains active`.

## Evidencia corrida por Codex

- `python -m py_compile runtime\orchestrator.py examples\runtime_loop_cases\run_runtime_loop_cases.py`
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> 15 casos OK
- `python examples\supervised_autonomy_cases\run_supervised_autonomy_cases.py` -> 9 casos OK
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> 4 casos OK
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> 6 casos OK
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> 11 casos OK
- `python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py` -> 10 casos OK
- `python scripts\validate_collaboration_state.py --root .` -> OK con los warnings FYI existentes
- `python scripts\scan_domain_neutrality.py --root .` -> OK
- `python scripts\scan_encoding.py --root .` -> OK
- Drift check -> `has_drift=false`, `up_to_seq=183`

Nota de entorno: `runtime_real_adapter`, `llm_adapter`, `intent_flow` y `scan_encoding` tuvieron
fallos sandboxed por permisos Windows (`WinError 5` / `PermissionError`) sobre temporales o
`CLAIMS.json`. Los reintentos fuera del sandbox pasaron. Es el mismo problema diagnosticado de ACL
con `tempfile`/sandbox unelevated, no una regresion del repo.

## Puntos para ratificacion

- Confirmar que el cleanup solo libera claims adquiridos por el orquestador en el turno.
- Confirmar que los claims preexistentes no se liberan en rechazo pre-apply.
- Confirmar que los caminos pre-apply no dejan claim huerfano.
- Confirmar que SA.4 sigue de-armado y el smoke real end-to-end queda detras de esta ratificacion.
