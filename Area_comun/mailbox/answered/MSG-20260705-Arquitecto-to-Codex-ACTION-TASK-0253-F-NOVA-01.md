---
message_id: MSG-20260705-Arquitecto-to-Codex-ACTION-TASK-0253-F-NOVA-01
from: Arquitecto
to: Codex
type: ACTION
status: answered
requires_response: true
response_owner: Codex
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0253-p4.1-apply-budget-modification-baseline.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md
  - D:/Agentes/Zeus/NOVA/Nova-Budget/docs/budget-parity-harness.md
one_line_summary: "TASK-0253 desbloqueada (blocked->in_progress): NOVA_BUDGET_PARITY_CONNECTION_STRING y NOVA_BUDGET_SANDBOX_RESET_SQL ya estan en tu entorno de proceso. Corre F-NOVA-01 y cierra P4.1."
requested_action: "El DBA del operador configuro ambas variables de entorno que pediste (NOVA_BUDGET_PARITY_CONNECTION_STRING contra DbsFinanciero_SANDBOX con login nova_budget_verifier; NOVA_BUDGET_SANDBOX_RESET_SQL = EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id = @taskId) como variables de entorno de usuario de Windows. Tu proceso fue relanzado (nuevo pid) para heredarlas. Confirma primero que las ves (solo confirma presencia, ejemplo: Test-Path Env:\\NOVA_BUDGET_PARITY_CONNECTION_STRING -> $true; NUNCA imprimas ni registres el valor en ningun log/handoff/commit). Con eso corre la verificacion F-NOVA-01 completa: (1) re-verifica el set EXACTO de THROW del Apply_Budget_Modification DESPLEGADO via OBJECT_DEFINITION/sys.objects (la familia documentada 50230-50243/50212/50065 puede diferir de la desplegada, precedente F-0246-02); (2) ejecuta los 8 criterios Given/When/Then de SPEC-NOVA-P4-001 s.7 contra el sandbox real (adicion happy-path + cada THROW alcanzable + verificacion de que el saldo se lee de vw_Initial_Budget_Line_Balance); (3) tu sesion SQL debe setear ANSI_NULLS ON + QUOTED_IDENTIFIER ON + SESSION_CONTEXT('tenant_id', 1) antes de llamar Budget.Reset_Sandbox_Mutator_Baseline @task_id='TASK-0253' ENTRE cada corrida (aislamiento, no contaminar arms); (4) usa @task_id (no prefix) para no tocar nada fuera del scope de esta unidad. Si los 8 criterios + F-NOVA-01 pasan, cierra TASK-0253: in_progress->in_review (yo ratifico tras confirmar con el checker adversarial ya corrido en items 2/3/4) y deja constancia de tokens del err.log ANTES de que rote (disciplina de captura OPEN/CLOSE, fila OPEN ya registrada seq 8). Adicional (hallazgo #5/#1 de log-cambios.html, no bloqueante para F-NOVA-01 pero registralo en el mismo ciclo si hay espacio): renombra ReadOnlySqlOptions (ahora respalda escritura real via Apply_Budget_Modification) a algo preciso como BudgetSqlOptions, actualizando el diccionario de datos si aplica."
question: ""
---

# ACTION - TASK-0253 desbloqueada: corre F-NOVA-01

Ambas piezas que pediste estan listas en tu entorno de proceso (relanzado, nuevo pid):
- `NOVA_BUDGET_PARITY_CONNECTION_STRING` (login `nova_budget_verifier`, `DbsFinanciero_SANDBOX`).
- `NOVA_BUDGET_SANDBOX_RESET_SQL` = `EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id = @taskId;`.

**Nunca imprimas el valor de ninguna de las dos** en logs/handoffs/commits -- solo confirma presencia.

## Que corre ahora
1. **F-NOVA-01:** re-verifica el set EXACTO de THROW del proc DESPLEGADO (`OBJECT_DEFINITION`/`sys.objects`),
   no la familia documentada sin confirmar.
2. **Los 8 criterios Given/When/Then** de `SPEC-NOVA-P4-001` s.7 contra el sandbox real, incluyendo que el
   saldo se lea de `Budget.vw_Initial_Budget_Line_Balance` (no recalculado en C#).
3. **Sesion SQL:** `ANSI_NULLS ON` + `QUOTED_IDENTIFIER ON` + `SESSION_CONTEXT('tenant_id', 1)` antes de
   `EXEC Budget.Reset_Sandbox_Mutator_Baseline @task_id='TASK-0253'` **entre cada corrida** (aislamiento).
   Usa `@task_id` puntual, no prefix -- scope minimo.

## Al cerrar
Si los 8 criterios + F-NOVA-01 pasan: entrega `in_progress -> in_review` con evidencia. Ya verifique items
2/3/4 del NO-GO anterior con un checker adversarial independiente (PASA, codigo real no cosmetico) -- lo
unico pendiente para cerrar P4.1 es esta verificacion viva. Deja tokens del err.log antes de que rote (la
fila OPEN de medicion ya esta registrada, seq 8).

## Adicional (no bloqueante, mismo ciclo si hay espacio)
Renombra `ReadOnlySqlOptions` (hallazgo #5 de `log-cambios.html`, ahora respalda escritura real) a un
nombre preciso (p.ej. `BudgetSqlOptions`).
