---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01-retry-2
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-3.md
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-blocked
  - "D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md"
one_line_summary: "DBA otorgo VIEW DEFINITION sobre Apply_Budget_Modification y Budget_Adjustment (resuelve el trigger). Reintenta F-NOVA-01 completo."
requested_action: "El DBA aplico GRANT VIEW DEFINITION ON OBJECT::[Budget].[Apply_Budget_Modification] y GRANT VIEW DEFINITION ON OBJECT::[Budget].[Budget_Adjustment] (esta ultima resuelve OBJECT_DEFINITION del trigger Budget.trg_budget_adjustment__cascade_status via la tabla padre, ya que SQL Server no acepta el grant directo sobre un trigger DML). Validado por el DBA con el login nova_budget_verifier: OBJECT_DEFINITION visible en ambos objetos (definition_length 9412 y 2009 respectivamente), THROW 50230 y 50243 encontrados en el texto del proc. El grant esta en sandbox-grant-execute.sql linea 38 (re-ejecutado completo sin error) y el DBA ya actualizo docs/budget-parity-harness.md linea 40. Reintenta F-NOVA-01 completo: (1) confirma presencia de las 2 env vars (solo presencia); (2) OBJECT_DEFINITION/sys.objects contra Apply_Budget_Modification para re-verificar el set EXACTO de THROW (50230-50243, 50212, 50065 documentados -- confirma cuales aparecen realmente, el precedente F-0246-02 encontro divergencia en un proc hermano, no asumas que el set documentado es completo/exacto); (3) corre los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 contra el sandbox real (incluyendo que el saldo resultante se lea de vw_Initial_Budget_Line_Balance); (4) reset por task_id ENTRE cada corrida (ya tienes esto resuelto en tu fix de reset con @taskId='TASK-0253' del commit anterior). Si los 8 criterios + el set de THROW re-verificado pasan: entrega TASK-0253 in_progress->in_review con la evidencia (query/resultado, nunca el connection string) y captura la fila CLOSE de medicion (tokens_total_atribuibles del err.log ANTES de que rote, via medicion_ledger.py --corpus explicito, clave TASK-0253 ya tiene fila OPEN seq 8)."
question: ""
---

# ACTION - Reintenta F-NOVA-01 (permiso VIEW DEFINITION ya resuelto)

El DBA otorgo el permiso que faltaba:
- `GRANT VIEW DEFINITION ON OBJECT::[Budget].[Apply_Budget_Modification] TO [budget_sandbox_verifier];`
- `GRANT VIEW DEFINITION ON OBJECT::[Budget].[Budget_Adjustment] TO [budget_sandbox_verifier];` (resuelve
  el trigger `trg_budget_adjustment__cascade_status` via la tabla padre -- SQL Server no acepta el grant
  directo sobre un trigger DML).

Validado por el DBA con `nova_budget_verifier`: `OBJECT_DEFINITION` visible en ambos (9412 y 2009 chars),
THROW 50230 y 50243 encontrados en el texto real del proc. `sandbox-grant-execute.sql` re-ejecutado
completo sin error.

## Reintenta ahora
1. Confirma presencia (no valor) de las 2 env vars.
2. Re-verifica el set EXACTO de THROW (50230-50243, 50212, 50065) contra `OBJECT_DEFINITION` real -- no
   asumas que el documentado es completo (precedente F-0246-02: un proc hermano diverge).
3. Corre los 8 criterios GWT de `SPEC-NOVA-P4-001` s.7 contra el sandbox, saldo por vista incluido.
4. Reset por `task_id` entre corridas (ya resuelto en tu fix anterior).

## Si pasa
Entrega `in_progress -> in_review` con evidencia (nunca el secreto) y captura la fila CLOSE de medicion
(tokens del err.log antes de rotar, `--corpus` explicito, clave `TASK-0253`).
