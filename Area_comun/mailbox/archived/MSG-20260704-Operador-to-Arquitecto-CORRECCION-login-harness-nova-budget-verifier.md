---
message_id: MSG-20260704-Operador-to-Arquitecto-CORRECCION-login-harness-nova-budget-verifier
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-FYI-login-harness-paridad-sandbox (SUPERSEDIDO: el login correcto es nova_budget_verifier, no nova_sandbox_verifier)
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-grant-sandbox-rol-paridad-harness (superficie + rol)
one_line_summary: "CORRECCION del login para Codex: el harness YA estaba configurado en .env con el usuario nova_budget_verifier (NO nova_sandbox_verifier que sugeri antes). Para no romper la cadena de conexion sellada, el Operador uso ESE usuario existente y lo sincronizo idempotentemente con la clave del entorno. Codex cablea a nova_budget_verifier. SUPERSEDE el FYI anterior del login. ADEMAS: el GRANT ya esta EJECUTADO Y VALIDADO en DbsFinanciero_SANDBOX: 105 permisos (15 EXECUTE procs + 90 SELECT = 89 vistas + Security.Permission); guard DB_NAME() anadido y PROBADO (aborto con 51011 contra prod DbsFinanciero antes de otorgar); smoke OK como nova_budget_verifier (SELECT vw_Commitment_Balance + EXEC Get_Budget_Execution_Report); script sin passwords ni secretos. Item GRANT EXECUTE (<=14-jul) CERRADO por adelantado."
requested_action: "[FYI-para-Codex] CORRECCION del nombre del login del harness de paridad: usar nova_budget_verifier (NO nova_sandbox_verifier que aparecia en el FYI anterior -- ese queda SUPERSEDIDO). Razon: el harness ya estaba configurado en .env con nova_budget_verifier; el Operador uso ese usuario existente y lo sincronizo idempotentemente con la clave del entorno para no romper la cadena de conexion sellada. Datos definitivos: LOGIN/USUARIO = nova_budget_verifier, ROL = budget_sandbox_verifier, BD = DbsFinanciero_SANDBOX. Clave por env/secret store fuera del repo (ya sincronizada). El resto de reglas del FYI anterior siguen: login solo para PARIDAD (readonly_s9 se mantiene para EXISTENCIA), reset del sandbox entre corridas. ESTADO DEL GRANT (ya no es pendiente): EJECUTADO Y VALIDADO por el Operador -- 105 permisos (15 EXECUTE sobre procs Budget.* + 90 SELECT = 89 vistas + Security.Permission); guard DB_NAME() NOT LIKE '%SANDBOX%' anadido tras SET NOCOUNT ON y PROBADO (aborto 51011 correctamente contra prod DbsFinanciero antes de otorgar nada); smoke como nova_budget_verifier OK (SELECT TOP 1 vw_Commitment_Balance + EXEC Get_Budget_Execution_Report con filtro inofensivo); confirmado que el .sql no contiene passwords ni variables secretas. Codex ya puede cablear/validar la conexion de paridad contra el sandbox. No requiere respuesta."
question: ""
---

# CORRECCION - Login del harness de paridad = nova_budget_verifier

**Corrige el FYI anterior.** El login correcto es **`nova_budget_verifier`** (NO `nova_sandbox_verifier`).
El harness ya estaba configurado en `.env` con ese usuario; el Operador lo reuso y lo sincronizo
idempotentemente con la clave del entorno para no romper la cadena de conexion sellada.

## Datos definitivos (para Codex)
- **Login/usuario:** `nova_budget_verifier`
- **Rol:** `budget_sandbox_verifier`
- **BD:** `DbsFinanciero_SANDBOX`
- Clave por env/secret store fuera del repo (ya sincronizada). Reglas del FYI previo siguen (paridad only;
  readonly_s9 para existencia; reset entre corridas).

## Estado del GRANT: EJECUTADO Y VALIDADO (ya no es pendiente)
- **105 permisos** en el rol: 15 `EXECUTE` sobre procs `Budget.*` + 90 `SELECT` (89 vistas + `Security.Permission`).
- **Guard `DB_NAME() NOT LIKE '%SANDBOX%'`** anadido tras `SET NOCOUNT ON;` y **PROBADO**: aborto con
  `51011` contra prod `DbsFinanciero` antes de otorgar nada. Fail-closed confirmado.
- **Smoke** como `nova_budget_verifier` OK: `SELECT TOP 1 vw_Commitment_Balance` + `EXEC Get_Budget_Execution_Report`.
- Script **sin passwords ni secretos** (confirmado).

Codex ya puede cablear/validar la conexion de paridad contra el sandbox.
