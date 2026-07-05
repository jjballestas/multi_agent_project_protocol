---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01-retry-3
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-5.md
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-2-blocked
one_line_summary: "DBA otorgo GRANT EXECUTE ON TYPE Budget_Modification_Line_List (y Chain_Adjustment_Line_List para PAR-1). Reintenta F-NOVA-01 completo."
requested_action: "El DBA aplico GRANT EXECUTE ON TYPE::[Budget].[Budget_Modification_Line_List] TO [budget_sandbox_verifier] y valido con nova_budget_verifier: DECLARE @lines Budget.Budget_Modification_Line_List funciona (TYPE_ID 260). Tambien concedio EXECUTE ON TYPE::[Budget].[Chain_Adjustment_Line_List] (anticipando PAR-1, no bloqueante para ti ahora). Reintenta F-NOVA-01 completo: (1) confirma que la TVP ya se puede declarar; (2) corre los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 contra el sandbox real via Apply_Budget_Modification, saldo leido de vw_Initial_Budget_Line_Balance; (3) el set EXACTO de THROW ya lo confirmaste (50230-50243 presentes en el proc, 50212 en el trigger trg_budget_adjustment__validate_open_year) -- si 50065 sigue sin encontrarse en ningun objeto visible, documentalo como residual/gap (no lo cites como criterio falsable sin evidencia); (4) reset por task_id ENTRE corridas. Si los 8 criterios pasan con el set de THROW re-verificado: entrega TASK-0253 in_progress->in_review con evidencia citada (nunca el connection string) y captura la fila CLOSE de medicion (tokens del err.log ANTES de rotar, medicion_ledger.py --corpus explicito, clave TASK-0253 fila OPEN seq 8 ya registrada)."
question: ""
---

# ACTION - Reintenta F-NOVA-01 (permiso de TVP ya resuelto)

El DBA otorgo `GRANT EXECUTE ON TYPE::[Budget].[Budget_Modification_Line_List] TO [budget_sandbox_verifier]`,
validado con `nova_budget_verifier` (`DECLARE @lines Budget.Budget_Modification_Line_List` OK, TYPE_ID 260).

## Reintenta ahora
1. Confirma que la TVP ya se declara sin error.
2. Corre los 8 criterios GWT de `SPEC-NOVA-P4-001` s.7 contra el sandbox real, saldo por vista incluido.
3. El set de THROW ya esta confirmado (50230-50243 en el proc, 50212 en el trigger de vigencia). Si
   `50065` sigue sin aparecer en ningun objeto visible, documentalo como residual (no lo cites como
   falsable sin evidencia -- puede ser un gap real de la SPEC vs lo desplegado).
4. Reset por `task_id` entre corridas.

## Si pasa
Entrega `in_progress -> in_review` con evidencia citada (nunca el secreto) y captura la fila CLOSE de
medicion (tokens del err.log antes de rotar, `--corpus` explicito).
