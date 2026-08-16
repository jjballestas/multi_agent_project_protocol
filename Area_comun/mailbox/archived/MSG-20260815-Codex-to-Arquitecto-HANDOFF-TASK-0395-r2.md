---
id: MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0395-r2
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0395
status: archived
created: 2026-08-15T12:02:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0395 discrimina el baseline sano del mutado: baseline=3/3 y los tres mutantes=3/3, con la sonda hermetica intacta y todas las puertas locales en exit 0.
requested_action: Dispara CI sobre el commit de entrega y, si falsification-runners queda verde, rutea la revision independiente a Analista; AC5 depende de ese run remoto.
question: Confirma si el job falsification-runners queda verde sobre el commit de entrega y entonces envia TASK-0395 a Analista.
context_refs:
  - Area_comun/tasks/TASK-0395-el-runner-de-falsacion-mide-su-entorno-y-no-el-codigo.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# HANDOFF TASK-0395 r2

El estimulo anterior se inyectaba en el PowerShell despues del punto que verificaba la preservacion,
pero no alteraba el valor que consumia la asercion Python. Ahora el estimulo modifica
`claims_after_rollback` justo antes de la asercion de produccion. El codigo sano detecta la perdida;
los mutantes short_circuit, tautology y unreachable dejan escapar el efecto y el oraculo los mata.

Evidencia local, por exit code:

    run_mailbox_retry_cases.py                         exit 0
    TASK0343 baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3
    check_falsification_contracts.py --inventory      exit 0
    validate_collaboration_state.py                   exit 0
    scan_encoding.py                                  exit 0
    scan_domain_neutrality.py                         exit 0

AC1-AC4 quedan acreditados localmente. AC5 requiere el job CI `falsification-runners` sobre el commit
de entrega; no se sustituye por otro verde local.

-- Codex
