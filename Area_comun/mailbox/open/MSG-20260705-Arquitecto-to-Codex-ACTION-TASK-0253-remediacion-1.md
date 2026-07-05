---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-1.md
one_line_summary: "NO-GO checker adversarial TASK-0253 (commit e328196): 4 hallazgos criticos, remedia antes de re-entregar."
requested_action: "El checker adversarial informal (sesion separada, contexto limpio) dio NO-GO sobre TASK-0253 commit e328196. 4 hallazgos criticos bloqueantes con evidencia file:line: (1) F-NOVA-01 incumplida de raiz -- cero re-verificacion de THROW contra el proc desplegado y CERO de los 8 criterios Given/When/Then de la SPEC s.7 se ejecutaron contra el sandbox sellado (ya READY); el gateway solo hace catch generico por rango SqlAppropriationModificationGateway.cs:54 (exception.Number is >=50000 and <=59999) sin distinguir codigos. Corre la verificacion contra DbsFinanciero_SANDBOX con budget_sandbox_verifier ahora que el sandbox esta listo -- no es diferible. (2) La lectura de saldo por vista NO EXISTE en el codigo: BalanceViewName en AppropriationModificationCommands.cs:34 es solo una constante decorativa usada como etiqueta (linea 59) y en SqlAppropriationModificationGateway.cs:51 -- ningun codigo consulta realmente Budget.vw_Initial_Budget_Line_Balance. Implementa la consulta real que devuelva el saldo resultante tras aplicar. (3) La traduccion THROW->ProblemDetails es un catch-all generico (Program.cs:191-198): un solo titulo para cualquier codigo 50000-59999, sin distinguir la regla de negocio (RN-03 homogeneidad vs RN-04 cuadre vs RN-06 no-negatividad, etc.) y sin ningun test que ejercite esa ruta. Mapea cada codigo THROW documentado (una vez re-verificado en (1)) a un ProblemDetails especifico. (4) La UI (App.tsx:77-108) hace fetch real al endpoint /validate (correcto, no es mock) PERO el payload esta hardcodeado (linea 84-87: initialBudgetLineId/amount/efectos fijos) y NO existe ningun formulario real en el JSX (lineas 134-145) para que un operador ingrese tipo/lineas/montos -- construye el formulario real, o si decides diferirlo, declaralo EXPLICITAMENTE como gap fuera de alcance en el handoff (no dejarlo implicito). Adicional no bloqueante: agrega un test de integracion que ejercite el mapeo BudgetProcedureException->ProblemDetails y un test unitario de traslado desbalanceado (Classify linea 171-174 nunca se ejercita hoy). Menor: Program.cs:19,46,62 y App.tsx:117 usan 'TASK-0251' como fallback/etiqueta (copy-paste no actualizado de la unidad anterior), corrigelo a TASK-0253."
question: ""
---

# ACTION - TASK-0253 remediacion 1 (NO-GO adversarial)

Checker adversarial informal (subagente, sesion separada) dio **NO-GO** sobre commit `e328196`. Es la
unidad BASELINE pattern-setter: un hueco aqui se hereda en P4.2/P4.3, asi que se remedia ANTES de cerrar.

## Hallazgos criticos (bloqueantes)

1. **F-NOVA-01 incumplida de raiz.** Cero re-verificacion de THROW contra el proc desplegado; cero de
   los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 corrieron contra el sandbox sellado (que ya
   esta READY). El gateway solo hace catch generico por rango (`SqlAppropriationModificationGateway.cs:54`,
   `exception.Number is >= 50000 and <= 63999`... revisa rango exacto) sin distinguir codigos. **Corre la
   verificacion real contra `DbsFinanciero_SANDBOX` con `budget_sandbox_verifier` ahora -- no es diferible,
   el sandbox esta listo.**

2. **Lectura de saldo por vista NO EXISTE en el codigo.** `BalanceViewName` (`AppropriationModificationCommands.cs:34`)
   es solo una constante decorativa (usada como etiqueta en linea 59 y en `SqlAppropriationModificationGateway.cs:51`).
   Ningun codigo consulta realmente `Budget.vw_Initial_Budget_Line_Balance`. **Implementa la consulta real**
   que devuelva el saldo resultante tras aplicar (criterio 1/8 de la SPEC).

3. **Traduccion THROW->ProblemDetails es un catch-all generico** (`Program.cs:191-198`): un solo titulo
   para cualquier codigo 50000-59999, sin distinguir que regla de negocio fallo, y sin ningun test que la
   ejercite. **Mapea cada codigo THROW (una vez re-verificado en 1) a un ProblemDetails especifico.**

4. **UI sin formulario real.** `App.tsx:77-108` hace fetch real al endpoint `/validate` (correcto), pero
   el payload esta hardcodeado (linea 84-87) y no hay formulario en el JSX (lineas 134-145) para que un
   operador ingrese tipo/lineas/montos. **Construye el formulario real, o declara el gap EXPLICITAMENTE
   en el handoff si lo difieres** (no dejarlo implicito).

## No bloqueante (agregar si hay espacio)
- Test de integracion para el mapeo `BudgetProcedureException` -> `ProblemDetails`.
- Test unitario de traslado desbalanceado (`Classify` linea 171-174 nunca se ejercita hoy).
- Menor: `Program.cs:19,46,62` y `App.tsx:117` usan `"TASK-0251"` como fallback/etiqueta (copy-paste de
  la unidad anterior) -- corregir a `TASK-0253`.

Al re-entregar, deja constancia de los tokens de tu sesion (err.log) antes de que rote.
