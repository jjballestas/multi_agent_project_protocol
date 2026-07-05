---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-remediacion-2-evidencia
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-7.md
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
one_line_summary: "NO-GO condicional del checker adversarial final: la evidencia F-NOVA-01 (8 GWT) no esta versionada en el repo, solo narrada en el handoff. Falta commitear evidencia trazable + la fila CLOSE de medicion."
requested_action: "El checker adversarial final (sesion separada) reviso el commit 33adb5b y dio NO-GO CONDICIONAL, no por el codigo (que confirmo solido, sin regresion de items 2/3/4, 39/39 tests verdes) sino porque la evidencia de F-NOVA-01 (los 8 GWT en vivo: adjustment_id 111, codigos TASK-0253-GWT1..7, DUP0253A, delta +1.0000) NO existe en ningun artefacto del repo (ni script SQL, ni test de integracion, ni log capturado) -- solo esta narrada en el handoff/mailbox. Ademas encontro que docs/budget-parity-harness.md tiene cambios SIN COMMITEAR en el working tree (la narrativa de los GRANTs escalonados). Para una unidad pattern-setter que P4.2/P4.3 heredan, la SPEC exige explicitamente 'cada THROW RE-VERIFICADO... antes de fijarse en un criterio' con evidencia trazable, no solo narrada (TASK-0253 acceptance item 2). ACCIONES antes de re-entregar: (1) COMMITEA docs/budget-parity-harness.md con la narrativa real de los permisos (VIEW DEFINITION del proc+trigger via tabla padre, EXECUTE ON TYPE del TVP, apertura de fiscal_year_id) -- reemplaza el texto viejo que aun dice 'Annul_Availability_Certificate y Annul_Commitment quedan fuera de este harness' si ya no aplica. (2) COMMITEA un artefacto REPRODUCIBLE de los 8 GWT: idealmente un test de integracion real (similar a BudgetParityHarnessTests.cs pero para Apply_Budget_Modification, gateado por las mismas env vars NOVA_BUDGET_PARITY_CONNECTION_STRING/NOVA_BUDGET_SANDBOX_RESET_SQL, que devuelva NA si faltan) que ejercite los 8 casos y capture el resultado -- no un script suelto sin versionar. Si un test de integracion real no es viable ahora mismo, como minimo commitea el script .sql de los 8 GWT (en tests/ o docs/) MAS un log de la corrida capturado como artefacto versionado (sin secretos). (3) ESCRIBE la fila CLOSE de medicion tu mismo esta vez: el path correcto es personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_ledger.py --corpus personal/Arquitecto/TFM-medicion/corpus/medicion (el path que buscaste, instrumentacion_estudio/, no existe -- gotcha ya documentado). Si prefieres NO tocar mi area personal, DEJALO EXPLICITO en el handoff (no lo escribas tu, yo la capturo) -- correctamente lo declaraste como riesgo la vez pasada, manten esa disciplina, yo la cierro. (4) Re-entrega in_review citando el commit con la evidencia versionada."
question: ""
---

# ACTION - Remediacion 2: evidencia F-NOVA-01 debe quedar versionada

Checker adversarial final: **NO-GO CONDICIONAL**. El codigo esta bien (sin regresion, 39/39 tests). El
problema es que la evidencia de los 8 GWT vive SOLO en el handoff/mailbox -- ningun artefacto del repo la
respalda. Para el pattern-setter que P4.2/P4.3 heredan, eso no es trazable.

## Antes de re-entregar

1. **Commitea `docs/budget-parity-harness.md`** con la narrativa real de los permisos (VIEW DEFINITION,
   TVP, vigencia fiscal) -- tiene cambios sin commitear ahora mismo.
2. **Commitea un artefacto reproducible de los 8 GWT** (test de integracion real, gateado por las mismas
   env vars, NA si faltan -- o al menos el script `.sql` + log capturado, versionado, sin secretos).
3. **Fila CLOSE de medicion:** escribela tu (path correcto:
   `personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_ledger.py --corpus
   personal/Arquitecto/TFM-medicion/corpus/medicion`) o declaralo explicito para que yo la cierre --
   manten la disciplina de no tocar mi area sin claim si prefieres lo segundo.
4. Re-entrega `in_review` citando el commit con la evidencia ya versionada.
