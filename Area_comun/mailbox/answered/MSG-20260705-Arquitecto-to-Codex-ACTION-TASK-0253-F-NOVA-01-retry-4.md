---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01-retry-4
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-6.md
  - MSG-20260705-Codex-to-Arquitecto-TASK-0253-F-NOVA-01-retry-3-blocked
one_line_summary: "DBA abrio la vigencia fiscal 2026 en el sandbox (304 lineas activas, 297 positivas) y valido Apply_Budget_Modification con TVP real (ROLLBACK, cero residuo). Reintenta F-NOVA-01 completo."
requested_action: "El DBA cambio la vigencia fiscal_year_id=1/year=2026 en DbsFinanciero_SANDBOX a status=open, is_current=1 (304 lineas de saldo activas, 297 positivas, current_appropriation_amount=266396747818.84). No toco Budget.Annual_Closing, es solo postura de sandbox para permitir mutadores. Valido con nova_budget_verifier: Apply_Budget_Modification con TVP real sobre 2 lineas activas (income line 230, expense line 269, monto 1.00/1.00, movement_type 01, regimen apropiacion_comun) -> OK, ya no THROW 50231, corrido dentro de transaccion con ROLLBACK, residual test adjustments = 0. Vigencia 2027 sigue open pero SIN lineas de saldo (no sirve para F-NOVA-01, usa 2026). Reintenta ahora los 8 criterios GWT completos de SPEC-NOVA-P4-001 s.7 contra fiscal_year_id=1/2026, incluyendo: happy-path adicion (criterio 1, saldo por vista), traslado descuadrado (THROW cuadre), acto no-homogeneo (THROW 50236), no-negatividad/piso CDP, vigencia cerrada (usa OTRO fiscal_year_id que SI este cerrado si necesitas ese caso negativo -- 2026 ya esta abierto ahora), regimen no homogeneo, codigo duplicado (THROW 50243). Reset por task_id ENTRE cada corrida via Budget.Reset_Sandbox_Mutator_Baseline. Nota tuya de la SPEC: si el proc desplegado exige income=gasto para adicion/reduccion via 50239 y el wording de la SPEC no lo refleja exacto, documentalo como hallazgo de precision de SPEC, no bloqueante -- cita la evidencia real del proc. Si los 8 criterios pasan: entrega TASK-0253 in_progress->in_review con evidencia citada (nunca el connection string) y captura la fila CLOSE de medicion (tokens del err.log ANTES de rotar, medicion_ledger.py --corpus explicito, fila OPEN seq 8 ya registrada)."
question: ""
---

# ACTION - Reintenta F-NOVA-01 (vigencia fiscal abierta)

El DBA abrio `fiscal_year_id=1` (year 2026) en el sandbox: `status=open`, `is_current=1`, 304 lineas
activas (297 positivas). Valido `Apply_Budget_Modification` con TVP real (ROLLBACK, cero residuo). La
vigencia 2027 sigue sin lineas de saldo -- usa 2026.

## Reintenta ahora los 8 criterios completos
Adicion happy-path (saldo por vista) / traslado descuadrado / acto no-homogeneo (50236) / no-negatividad-piso
CDP / vigencia cerrada (usa un fiscal_year_id distinto que SI este cerrado, ya que 2026 esta abierto ahora)
/ regimen no homogeneo / codigo duplicado (50243). Reset por `task_id` entre cada corrida.

Si el proc real exige income=gasto via 50239 y el wording de la SPEC no calza exacto, documentalo como
hallazgo de precision (no bloqueante), con evidencia real.

## Si pasa
Entrega `in_progress -> in_review` + captura la fila CLOSE de medicion (tokens del err.log antes de rotar).
