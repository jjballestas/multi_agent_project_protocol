---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01-retry
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-env-listas-relanza-codex-desbloquea-P4.1 (env vars listas)
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-remediation-1-in-review (bloqueo por credenciales)
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-2.md (product commit 00a3f47)
one_line_summary: "Cron de Codex ya relanzado (log confirma restart 2026-07-05T12:06:09, pid 99072, heartbeats limpios) y AMBAS env vars del harness ya estan en el entorno de usuario Windows (validadas por el DBA: conexion OK + dry_run reset en cero, sin mutar). Re-ejecuta F-NOVA-01 contra DbsFinanciero_SANDBOX ahora que tu proceso relanzado deberia verlas."
requested_action: "[ACTION] Las 2 variables (NOVA_BUDGET_PARITY_CONNECTION_STRING, NOVA_BUDGET_SANDBOX_RESET_SQL) estan configuradas SOLO en el entorno de usuario de Windows (secreto no viaja por repo/mailbox; tu y yo solo confirmamos presencia, nunca el valor). Tu proceso/cron ya fue relanzado por mi lado y deberia recogerlas. (1) CONFIRMA presencia de ambas env vars en tu sesion actual (solo presencia, no el valor). (2) Re-ejecuta F-NOVA-01 sobre el commit 00a3f47 (Nova-Budget): los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 contra DbsFinanciero_SANDBOX, cada THROW (50230-50243, 50212, 50065) re-verificado falsable contra OBJECT_DEFINITION del proc DESPLEGADO; sesion con ANSI_NULLS ON + QUOTED_IDENTIFIER ON + SESSION_CONTEXT('tenant_id'); llama Budget.Reset_Sandbox_Mutator_Baseline @task_id=... ENTRE corridas (repetibilidad, no solo al arranque). (3) Si los 8 criterios pasan: TASK-0253 vuelve a in_review con la evidencia sandbox citada (query/resultado, no el connection string); notifica handoff a Arquitecto. (4) Si P4.1 cierra con esto: CAPTURA la fila CLOSE con tokens_total_atribuibles (del err.log ANTES de rotar) via medicion_ledger.py --corpus EXPLICITO -- no repetir el hueco de F3.3. RESPONDE con: (a) env vars presentes si/no; (b) resultado de los 8 criterios + THROW; (c) si P4.1 cerro con fila CLOSE + tokens."
question: ""
---

# ACTION - Reintenta F-NOVA-01 con env vars ya configuradas

El DBA configuro ambas variables del harness en el entorno de usuario de Windows (secreto NUNCA en
repo/mailbox). Tu cron ya fue relanzado (log: restart 2026-07-05T12:06:09, pid 99072, heartbeats
limpios). Reintenta la verificacion sandbox de F-NOVA-01 sobre el commit 00a3f47.

## Que verificar
- Presencia (no valor) de `NOVA_BUDGET_PARITY_CONNECTION_STRING` y `NOVA_BUDGET_SANDBOX_RESET_SQL`.
- Los 8 criterios Given/When/Then (SPEC-NOVA-P4-001 s.7) contra `DbsFinanciero_SANDBOX`.
- Cada THROW (50230-50243, 50212, 50065) falsable contra `OBJECT_DEFINITION` del proc desplegado.
- Sesion: `ANSI_NULLS ON` + `QUOTED_IDENTIFIER ON` + `SESSION_CONTEXT('tenant_id')`.
- Reset (`Budget.Reset_Sandbox_Mutator_Baseline @task_id=...`) ENTRE corridas, no solo al arranque.

## Si pasa
TASK-0253 -> in_review con evidencia citada (query/resultado, nunca el secreto). Si P4.1 cierra:
captura la fila CLOSE con tokens (err.log antes de rotar) via `medicion_ledger.py --corpus` explicito.

## Responde
(a) env vars presentes si/no; (b) resultado 8 criterios + THROW; (c) P4.1 cerro con CLOSE + tokens?
