---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0252-harness-paridad
from: Arquitecto
to: Codex
type: GO
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md
  - MSG del Operador: GRANT EXECUTE ejecutado+validado (rol budget_sandbox_verifier, login nova_budget_verifier, 105 permisos, DbsFinanciero_SANDBOX)
one_line_summary: "GO para TASK-0252 (ready ya volteado): cablea el harness de paridad exec-vs-endpoint al sandbox de mutadores. Baja prioridad, relleno legitimo mientras P3.1 espera Sprint 1 (30-jul)."
requested_action: "Implementa TASK-0252 segun su intake (acceptance). Datos definitivos de conexion: LOGIN/USUARIO = nova_budget_verifier (SQL login + usuario en BD), ROL = budget_sandbox_verifier, BD = DbsFinanciero_SANDBOX. La clave sale de la config de entorno / secret store FUERA del repo (NUNCA hardcodear ni commitear). El GRANT ya esta EJECUTADO Y VALIDADO por el Operador: 105 permisos (15 EXECUTE sobre procs Budget.* + 90 SELECT = 89 vistas + Security.Permission); guard DB_NAME() NOT LIKE '%SANDBOX%' probado (aborta 51011 contra prod); smoke OK (SELECT vw_Commitment_Balance + EXEC Get_Budget_Execution_Report). Este login REEMPLAZA a nova_sql_connector_readonly_s9 SOLO para pruebas de PARIDAD (readonly_s9 se mantiene para verificacion de EXISTENCIA, F-NOVA-01). El harness debe RESETEAR el sandbox a la linea base sellada ENTRE corridas (los procs mutan; sin reset, un brazo contamina al otro). Columna del schema: paridad_exec_vs_endpoint (pass/fail/NA). Gate FORMAL del Analista al entregar (infra gobernada, no unidad de contraste)."
question: ""
---

# GO - TASK-0252 (harness de paridad exec-vs-endpoint)

Relleno legitimo de baja prioridad mientras P3.1 (pattern-setter) espera su ventana de Sprint 1
(post-30-jul, per sello s.3.3 -- confirmado por el Operador, no se adelanta). Ver el `.md` de la tarea
para el DoD completo. Datos de conexion definitivos en `requested_action`.
