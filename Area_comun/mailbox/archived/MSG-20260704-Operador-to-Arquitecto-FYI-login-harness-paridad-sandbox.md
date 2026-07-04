---
message_id: MSG-20260704-Operador-to-Arquitecto-FYI-login-harness-paridad-sandbox
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-grant-sandbox-rol-paridad-harness (superficie + rol)
one_line_summary: "Dato para que Codex cablee la cadena de conexion del harness de paridad sin ambiguedad: LOGIN/USUARIO = nova_sandbox_verifier (SQL login), miembro del rol budget_sandbox_verifier, sobre la BD DbsFinanciero_SANDBOX. La clave sale de la config de entorno FUERA del repo (nunca hardcodear en el harness ni commitear). Ese login REEMPLAZA a nova_sql_connector_readonly_s9 para las pruebas de PARIDAD exec-vs-endpoint (el readonly_s9 sigue para verificacion de EXISTENCIA)."
requested_action: "[FYI-para-Codex] Nombre exacto de la identidad de conexion del harness de PARIDAD (exec-vs-endpoint): LOGIN/USUARIO = nova_sandbox_verifier (SQL login a nivel servidor + usuario en la BD), miembro del rol budget_sandbox_verifier, sobre la BD DbsFinanciero_SANDBOX. Codex cablea la cadena de conexion del harness de paridad a ese login. REGLAS: (1) la CLAVE sale de la config de entorno / secret store FUERA del repo -- NUNCA hardcodear en el harness ni commitear (secretos prohibidos, AGENTS.md s.4). (2) Ese login es SOLO para PARIDAD (requiere EXECUTE, disponible en sandbox); el conector nova_sql_connector_readonly_s9 se mantiene para la verificacion de EXISTENCIA (F-NOVA-01, SELECT/VIEW DEFINITION). (3) El harness debe resetear el sandbox a la linea base sellada ENTRE corridas (los procs mutan). El Operador ejecuta el GRANT + crea el rol/login de su parte (runbook ya definido, con el guard DB_NAME() de hardening). No requiere respuesta."
question: ""
---

# FYI - Login del harness de paridad (para Codex)

Dato para cablear la cadena de conexion del harness de **paridad exec-vs-endpoint** sin ambiguedad:

- **Login/usuario:** `nova_sandbox_verifier` (SQL login a nivel servidor + usuario en la BD).
- **Rol:** miembro de `budget_sandbox_verifier`.
- **BD:** `DbsFinanciero_SANDBOX`.

## Reglas
1. La **clave** sale de la config de entorno / secret store **fuera del repo** -- NUNCA hardcodear ni
   commitear (secretos prohibidos).
2. Este login es **solo para PARIDAD** (requiere EXECUTE, disponible en sandbox). El conector
   `nova_sql_connector_readonly_s9` se mantiene para verificacion de **existencia** (F-NOVA-01).
3. El harness debe **resetear el sandbox** a la linea base sellada **entre corridas** (los procs mutan).

El Operador ejecuta el GRANT + crea rol/login de su parte (runbook definido, con el guard `DB_NAME()`).
