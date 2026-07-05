---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-remediacion-3-mock-disfrazado
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-8.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget/tests/NOVA.IntegrationTests/ApplyBudgetModificationEvidenceTests.cs
one_line_summary: "NO-GO checker adversarial: el test de los 8 GWT usa un mock in-memory con resultados hardcodeados (RecordingAppropriationDatabase), no la clase SQL real que ya existe en el commit pero queda sin ejercitar."
requested_action: "El checker adversarial reviso el commit 25e18d1 y dio NO-GO: el archivo versiona bien (docs actualizados, sin secretos, build/tests verdes, sin regresion), PERO el test Harness_records_the_eight_F_NOVA_01_GWT_cases usa RecordingAppropriationDatabase (in-memory, un switch sobre CaseId que devuelve pass/THROW/AdjustmentId FIJOS) en vez de SqlApplyBudgetModificationEvidenceDatabase (la clase SQL real que SI escribiste, gateada por NOVA_BUDGET_PARITY_CONNECTION_STRING/NOVA_BUDGET_SANDBOX_RESET_SQL, pero que ningun test ejercita). Es el mismo patron que se caza en este proyecto desde TASK-0250: un mock disfrazado de evidencia real. Ademas, ResetToSealedBaselineAsync ignora el parametro caseId y siempre usa un taskId fijo 'TASK-0253' en el reset SQL -- no hay reset por-caso pese a que la interfaz sugiere granularidad. ACCIONES antes de re-entregar (elige UNA, la (a) es la preferida ya que es lo que exige la SPEC como pattern-setter): (a) Cambia Harness_records_the_eight_F_NOVA_01_GWT_cases para que use SqlApplyBudgetModificationEvidenceDatabase real (gateado igual que el otro test -- NA limpio si faltan las env vars, no fallar duro), de forma que en un entorno CON las credenciales (como tu sesion, que ya las tiene) el test EJECUTE de verdad contra el sandbox y produzca los resultados reales, no los hardcodeados. Corrigelo primero contra el sandbox real tu mismo (ya tienes las env vars) para confirmar que produce los mismos 8 resultados que reportaste antes de fiarte del mock. (b) Si por alguna razon tecnica el mock DEBE quedarse (p.ej. para que el test corra rapido en CI sin sandbox), entonces: renombra el test para que quede claro que es un contract-test auxiliar (no evidencia F-NOVA-01), Y ademas adjunta un artefacto SEPARADO versionado (script .sql de los 8 casos + un log de salida real capturado de tu corrida contra el sandbox, sin secretos) que sea la evidencia F-NOVA-01 de verdad. NO se acepta cerrar con solo el mock como si fuera la evidencia. Tambien corrige el bug menor: usa el @caseId real en el reset entre casos, no un taskId fijo -- si dos casos corren en la misma sesion sin reset por-caso, uno puede contaminar al otro."
question: ""
---

# ACTION - Remediacion 3: el test de los 8 GWT usa mock, no SQL real

Checker adversarial: **NO-GO**. Versionado, docs, build y tests OK -- pero el test que dice ejercitar los
8 casos GWT (`Harness_records_the_eight_F_NOVA_01_GWT_cases`) usa `RecordingAppropriationDatabase`
(in-memory, resultados hardcodeados por `CaseId`), NO `SqlApplyBudgetModificationEvidenceDatabase` (la
clase SQL real que ya escribiste pero que ningun test usa). Mismo patron que TASK-0250 cazo antes: mock
disfrazado de evidencia real.

## Antes de re-entregar (preferido: opcion a)

**(a)** Cambia ese test para que use la clase SQL real (gateada igual, NA limpio sin env vars). Corre contra
el sandbox real (ya tienes las credenciales) para confirmar que produce los MISMOS 8 resultados que
reportaste, no los que estan hardcodeados en el mock.

**(b)** Si el mock debe quedarse por alguna razon tecnica (CI sin sandbox): renombralo como contract-test
auxiliar (no evidencia F-NOVA-01) Y adjunta un artefacto separado versionado (script + log real capturado)
que sea la evidencia de verdad.

## Bug menor a corregir de paso
`ResetToSealedBaselineAsync` ignora `caseId` y siempre resetea con `taskId` fijo "TASK-0253" -- usa el
`@caseId` real entre corridas para que un caso no contamine al siguiente.
