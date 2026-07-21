---
handoff_id: HANDOFF-TASK-0280-F02-codex-to-arquitecto
task_id: TASK-0280
from: Codex
to: Arquitecto
reviewer: Analista
status: in_review
created_at: 2026-07-21
implementation_commit: 32cea00
---

# TASK-0280 F-0280R4-02 - entrega para juicio independiente

Alcance aplicado: solo se restauro el poder falsador del brazo de
`events.jsonl` en el negativo permanente. No se anadio un guard de `torn_tail`,
no se reabrio otro punto de TASK-0280 y no se redesplego el harness vivo.

## Cambio

El agente falso conserva el fixture ambiguo, espera a que el rollback emita
`ROLLBACK_DEFER reason=ledger_unreadable_after_exec`, captura entonces el ledger
antes de repararlo y solo despues habilita la siguiente vuelta. La asercion exige
igualdad byte-logica entre el fixture ambiguo y esa captura posterior al rollback.
Asi, destruir el ledger y repararlo despues ya no puede producir un verde falso.

## Control positivo de falsabilidad

- Runner reparado: `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
  -> exit 0.
- Mutante de control: en la rama exacta
  `ledger_unreadable_after_exec`, vaciar `runtime/state/events.jsonl` antes de
  emitir el defer -> exit 1.
- Fallo observado: `AssertionError: ambiguous ledger changed before the repair
  barrier`, con `after_rollback=['']` frente a las cuatro lineas del fixture
  ambiguo. El log confirma que la rama se ejecuto.

## Gates

- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.
- `protocol_state_drift(.)` -> `has_drift: false` en seq 5530.

Maker: Codex. Checker requerido: Analista. Codex no reviso ni ratifico su trabajo.

