---
message_id: MSG-20260704-Operador-to-Arquitecto-ACTION-sandbox-mutadores-construido-documentar-sellar
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/specs/nova/SPEC-NOVA-P4-001-apply-budget-modification.md (PRECONDICION BLOQUEANTE sandbox)
  - Area_comun/specs/nova/SPEC-NOVA-P4-002-apply-availability-adjustment.md (PAR-1, misma precondicion)
  - Area_comun/specs/nova/SPEC-NOVA-P4-003-apply-commitment-adjustment.md (PAR-1)
one_line_summary: "El Operador CONSTRUYO el sandbox de mutadores (Opcion A: restore + rol GRANT EXECUTE, aislamiento VERIFICADO -- el verifier NO puede abrir produccion). Cierra la PRECONDICION BLOQUEANTE <=14-jul de P4.x, adelantada. ACCION: DOCUMENTA Y SELLA el mecanismo (identico ambos brazos + PROCEDIMIENTO DE RESET = re-restore del seed .bak antes de cada miembro/brazo, para MISMO estado inicial), voltea la precondicion de P4.x a READY, y NO metas el secreto al repo (solo nombres de env var). SIN secreto."
requested_action: "[DIRECTIVA] El Operador CONSTRUYO el sandbox de mutadores (Opcion A) -- cierra la PRECONDICION BLOQUEANTE <=14-jul de las P4.x, adelantada. Detalle (SIN secreto -- solo nombres de env var): (a) BD sandbox = DbsFinanciero_SANDBOX, restaurada de un seed backup DbsFinanciero_SANDBOX_20260704_050932.bak en el contenedor ingenas-sqlserver; (b) login/rol SOLO-sandbox = nova_budget_verifier / budget_sandbox_verifier, con EXECUTE sobre 15 procs Budget.* + SELECT sobre 89 vistas; credenciales en D:/Agentes/Ingenas/.env como SQLSERVER_SANDBOX_DATABASE / SQLSERVER_SANDBOX_VERIFIER_USER / SQLSERVER_SANDBOX_VERIFIER_PASSWORD (NOMBRES; el valor NUNCA va al repo); (c) VERIFICADO por el Operador: ambas BD ONLINE; existen Apply_Availability_Adjustment / Apply_Commitment_Adjustment / Apply_Obligation_Adjustment en sandbox; conexion real OK; EXECUTE sobre Apply_Obligation_Adjustment OK; SELECT sobre vw_Commitment_Line_Balance OK; y AISLAMIENTO VERIFICADO -- el login verifier NO puede abrir DbsFinanciero (produccion), falla como se espera. ACCION: DOCUMENTA Y SELLA este mecanismo como la PRECONDICION del estudio (Particion s.1: 'definido y documentado <=14-jul, IDENTICO en ambos brazos; jamas degradado en silencio a leer OBJECT_DEFINITION'). Requisitos del doc sellado: (1) IDENTICO EN AMBOS BRAZOS -- baseline y gobernado usan ESTE sandbox (misma BD, mismo seed). (2) PROCEDIMIENTO DE RESET (critico para MISMO estado inicial): re-restaurar DbsFinanciero_SANDBOX desde el seed backup DbsFinanciero_SANDBOX_20260704_050932.bak ANTES de los tests de cada miembro y ENTRE brazos, para que ambos corran contra el MISMO estado inicial -- 'identico en ambos brazos' incluye estado inicial identico, no solo la conexion. Sin reset, el segundo miembro corre contra una BD ya mutada = confound. (3) NO degradado a OBJECT_DEFINITION: hay EXECUTE real -> los tests de mutacion corren DE VERDAD (paridad EXEC vs endpoint viable). (4) VOLTEA la PRECONDICION BLOQUEANTE de P4-001/002/003 (y las P4 restantes) de 'riesgo de diferir' a READY -- el sandbox existe. (5) NO metas el secreto al repo: referencia solo los nombres de env var. RESPONDE con: doc del mecanismo sellado commiteado (sin secreto) + precondicion P4.x volteada a READY + procedimiento de reset documentado. NOTA: con esto los DOS pendientes del Operador quedan cerrados (estimates lockeados + sandbox construido); el sello 08-jul solo necesita el sorteo-del-dia."
question: ""
---

# ACTION - Sandbox de mutadores CONSTRUIDO (Operador): documenta y sella

El Operador construyo el sandbox de mutadores (Opcion A), con aislamiento VERIFICADO (el verifier NO abre
produccion). Cierra la precondicion <=14-jul de las P4.x, adelantada. Detalle (SIN secreto):

- **BD sandbox:** DbsFinanciero_SANDBOX (restore del seed `DbsFinanciero_SANDBOX_20260704_050932.bak`, contenedor ingenas-sqlserver).
- **Login/rol solo-sandbox:** nova_budget_verifier / budget_sandbox_verifier; EXECUTE 15 procs Budget.* + SELECT 89 vistas. Env vars: SQLSERVER_SANDBOX_DATABASE / _VERIFIER_USER / _VERIFIER_PASSWORD (nombres; valor NUNCA al repo).
- **Verificado:** ambas BD ONLINE; procs Apply_* presentes; conexion + EXECUTE + SELECT OK; **aislamiento OK (verifier NO abre produccion).**

## Documenta + sella el mecanismo (requisitos)
1. **Identico en ambos brazos** (baseline + gobernado, misma BD/seed).
2. **RESET (critico):** re-restaurar desde el seed `.bak` ANTES de cada miembro y ENTRE brazos -> mismo estado inicial. Sin reset = confound.
3. **No degradado a OBJECT_DEFINITION** (hay EXECUTE real).
4. **Voltea la precondicion de P4-001/002/003 (+ restantes) a READY.**
5. **NO metas el secreto al repo** (solo nombres de env var).

Con esto los DOS pendientes del Operador quedan cerrados (estimates lockeados + sandbox); el sello 08-jul solo necesita el sorteo-del-dia.
