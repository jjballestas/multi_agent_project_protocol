---
id: MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0337-r2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0337
status: archived
created: 2026-08-16T12:25:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0337 r2 esta lista para review independiente; AC6 y AC10 quedan acreditados por conducta en layouts plano y anidado.
requested_action: Enruta review independiente de TASK-0337 sobre d4c2e8c3 y este cierre gobernado.
question: Confirma si el checker ratifica que la memoria propia arranca y que un residuo ajeno intersectante conserva el veto en ambos layouts.
context_refs:
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# Handoff TASK-0337 r2

## Resultado

- `Get-StagedResidueState` deriva con `git rev-parse --show-prefix` el prefijo de la instancia.
- Layout plano: prefijo vacio y conducta preservada.
- Layout anidado: `Aegis/personal/TestPeer/MEMORY.md` se reconoce como memoria propia y no difiere.
- En ambos layouts, `work/target.txt` ajeno e intersectante sigue difiriendo.
- El log conserva el par exacto `dirty_path` / `message_route`; en el layout anidado el primero
  mantiene la ruta observada por Git y el segundo mantiene el scope relativo a la instancia.

## Evidencia

- Commit de implementacion: `d4c2e8c3`.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: PASS.
- Negativos: el global-veto mutant y el prefix-elision mutant mueren.
- `python scripts/check_falsification_contracts.py --root .`: PASS, 76/76.
- `python scripts/validate_collaboration_state.py --root .`: PASS.
- `python scripts/scan_encoding.py --root .`: PASS.
- `python scripts/scan_domain_neutrality.py --root .`: PASS.
- Drift: false en seq 9494 antes del commit de implementacion.

## Rojo preexistente delimitado

`python scripts/test_exec_lease_harness.py` sigue rojo en tres controles de liveness de procesos:
CPU silenciosa, lease ilegible vivo y admission liveness. El mismo conjunto falla en un clon limpio
de HEAD previo `2636eb9a`; TASK-0337 no toca esas rutas de produccion. El contrato extraido que cubre
`Get-StagedResidueState` pasa, y la suite E2E de retry completa pasa. No se absorbio ese defecto ajeno.

Codex es maker; no reviso ni ratifico esta entrega.
