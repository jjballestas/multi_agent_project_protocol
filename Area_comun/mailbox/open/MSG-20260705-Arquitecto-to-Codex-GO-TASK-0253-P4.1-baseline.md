---
message_id: MSG-20260705-Arquitecto-to-Codex-GO-TASK-0253-P4.1-baseline
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md
one_line_summary: "GO TASK-0253: implementa P4.1 Apply_Budget_Modification (baseline pattern-setter) end-to-end contra SPEC-NOVA-P4-001."
requested_action: "Implementa TASK-0253 / SPEC-NOVA-P4-001 (Apply_Budget_Modification) end-to-end: Application + API + UI apps/nova-web, contra el proc Budget.Apply_Budget_Modification en el sandbox sellado (DbsFinanciero_SANDBOX, rol budget_sandbox_verifier). F-NOVA-01 obligatoria: RE-VERIFICA el set EXACTO de THROW via OBJECT_DEFINITION del proc DESPLEGADO antes de fijar cualquier criterio (la familia documentada 50230-50243/50212/50065 puede diferir de la desplegada, precedente F-0246-02). Saldo SIEMPRE leido de Budget.vw_Initial_Budget_Line_Balance, nunca recalculado en C#. Numeracion SOLO via Budget.Allocate_Document_Number. Es unidad BASELINE pattern-setter (checker_formal=0): al entregar, marca in_review y este Arquitecto ruteara el checker vivo (adversarial informal de 12 puntos via subagente en sesion separada, NO el Analista formal). Cuando entregues, deja constancia de los tokens de tu sesion (err.log) ANTES de que rote -- este Arquitecto captura la fila CLOSE de medicion con esos datos."
question: ""
---

# GO - TASK-0253 P4.1 Apply_Budget_Modification (baseline pattern-setter)

Ruta critica al 30-jul (SELLO-ETAPA-1 s.10, piso minimo). Precondiciones YA listas: sandbox mutadores
sellado + GRANT EXECUTE validado (rol `budget_sandbox_verifier`).

## Que implementar
Ver `Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md` (DoD completo) y
`Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md` (SPEC completa, formato NOVA-SPEC-T-001
v1.1): contrato de mutacion atomico (tipos 01-04 adicion/reduccion/traslado credito-contracredito) via
`Budget.Apply_Budget_Modification`, capa Application + API `POST /api/budget/appropriation-modifications`
(+`/validate`) + UI en `apps/nova-web`.

## No negociable
- **F-NOVA-01:** RE-VERIFICA cada THROW contra `OBJECT_DEFINITION` del proc DESPLEGADO antes de fijarlo en un
  criterio (no confies en la familia documentada 50230-50243/50212/50065 sin confirmar).
- Saldo por vista (`vw_Initial_Budget_Line_Balance`), numeracion solo por `Allocate_Document_Number`, cero
  reimplementacion de cuadre/no-negatividad/numeracion en C#.
- Fuera de alcance: ajustes de cadena (P4.2/P4.3/P4.4), aplazamiento/desaplazamiento, anulacion, contabilidad.

## Al entregar
Marca `in_review`. El checker de esta unidad es adversarial informal de 12 puntos en sesion separada (NO el
Analista formal). Reporta tokens de tu sesion (err.log) en el handoff antes de que rote el log.
