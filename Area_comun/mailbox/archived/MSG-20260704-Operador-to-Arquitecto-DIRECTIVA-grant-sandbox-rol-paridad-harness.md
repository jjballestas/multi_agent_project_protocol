---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-grant-sandbox-rol-paridad-harness
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-grant-execute.sql (script GRANT, fuera del hub)"
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-procedures-list.txt (15 procs)"
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/sandbox-views-list.txt (89 vistas)"
  - MSG-20260704-Operador-to-Arquitecto-RESPUESTA-P2-espera-PAR2-difiere (deferral PAR-2)
one_line_summary: "GRANT EXECUTE del estudio DEFINIDO por el Operador: rol budget_sandbox_verifier sobre DbsFinanciero_SANDBOX, superficie IDENTICA baseline/gobernado (15 GRANT EXECUTE procs + 89 GRANT SELECT vistas + 1 dep Security.Permission). El Operador ejecuta el GRANT de su parte. ACCION para Codex: cablear el harness de PARIDAD (exec-vs-endpoint) al sandbox con ese rol (reemplaza el conector readonly_s9 que solo verificaba existencia, F-NOVA-01). HARDENING recomendado: anadir un guard IF DB_NAME() NOT LIKE '%SANDBOX%' THROW al inicio del script (el THROW actual solo verifica que el rol exista, no la identidad de la BD; footgun si se corre contra prod). NOTA integridad: Annul_Availability_Certificate/Annul_Commitment NO estan en la superficie (brechas B-04, no existen aun) -> PAR-2 exige ENMIENDA FECHADA al script cuando hardening los entregue (<=15-jul); resetear el sandbox entre corridas para paridad determinista. Prioridad: por debajo del fix-loop de F3.3; es prep para cuando abra la medicion."
requested_action: "[DIRECTIVA] El Operador definio y ejecutara de su parte el GRANT EXECUTE del estudio. Rutea a Codex el cableado del harness de paridad. DATOS: (1) ROL = budget_sandbox_verifier; TARGET = DbsFinanciero_SANDBOX (sandbox restaurado, NO produccion). (2) SUPERFICIE (identica para baseline y gobernado, por diseno = no confound): 15 GRANT EXECUTE sobre procs (Allocate_Document_Number, Annul_Obligation, Apply_Availability_Adjustment, Apply_Budget_Modification, Apply_Commitment_Adjustment, Apply_Obligation_Adjustment, Approve_Availability_Certificate_Draft, Approve_Commitment_Draft, Approve_Initial_Budget_Draft, Approve_Obligation_Draft, Approve_Payment_Draft, Close_Fiscal_Year, Constitute_Payables, Constitute_Reserves, Get_Budget_Execution_Report) + 89 GRANT SELECT sobre vistas + 1 GRANT SELECT sobre Security.Permission (dependencia cross-schema de la vista de Navigation). Script y listas en el paquete fuente del Operador (context_refs, FUERA del hub). ACCION CODEX: cablear el harness de PARIDAD exec-vs-endpoint a la cadena de conexion del sandbox usando el rol budget_sandbox_verifier; ese rol reemplaza al conector readonly nova_sql_connector_readonly_s9 para las pruebas de PARIDAD (el readonly_s9 solo tenia SELECT/VIEW DEFINITION y servia para verificar EXISTENCIA, F-NOVA-01; la paridad requiere EXECUTE, ahora disponible en sandbox). La columna del schema es paridad_exec_vs_endpoint (pass/fail/NA). HARDENING RECOMENDADO (relayar al Operador/DBA): el script tiene un THROW 51010 que solo valida que el rol exista, pero NO valida la identidad de la BD -> si se corriera por error conectado a prod otorgaria EXEC de mutadores en produccion. Anadir al inicio un guard tipo: IF DB_NAME() NOT LIKE '%SANDBOX%' THROW 51011, 'Refuse: not a SANDBOX database', 1; (o exigir que budget_sandbox_verifier exista SOLO en el sandbox). Fail-closed barato que elimina el footgun. NOTAS DE INTEGRIDAD DE ESTUDIO: (a) Annul_Availability_Certificate y Annul_Commitment NO estan en la superficie porque son brechas de verdad B-04 (aun no existen; los crea nova-hardening) -> cuando lleguen (<=15-jul) se anaden por ENMIENDA FECHADA al script (regla sellada s.5), NO se meten ahora; PAR-2 sigue diferido. (b) los procs de la superficie MUTAN el sandbox (Approve_*/Apply_*/Annul_Obligation/Close_Fiscal_Year/Constitute_*) -> el harness debe RESETEAR el sandbox a la linea base sellada ENTRE corridas para que la paridad sea repetible y un brazo no contamine al otro (el sandbox ya esta sellado con RESET verificado; solo asegura que el harness lo invoque por corrida). PRIORIDAD: por DEBAJO del fix-loop de F3.3 (TASK-0249); esto es prep para cuando abra el dev medido P2/la paridad, no compite con F3.3. FRONTERA: el script SQL y el dominio Nova viven en el paquete fuente / instancia, NUNCA en el core neutral."
question: ""
---

# DIRECTIVA - GRANT sandbox definido + cableado del harness de paridad + hardening DB_NAME()

El Operador **definio y ejecutara de su parte** el GRANT EXECUTE del estudio. Rutea a Codex el cableado.

## Datos del GRANT (para Codex)
- **Rol:** `budget_sandbox_verifier`. **Target:** `DbsFinanciero_SANDBOX` (sandbox restaurado, NO prod).
- **Superficie (IDENTICA baseline/gobernado = no confound):** 15 `GRANT EXECUTE` sobre procs + 89
  `GRANT SELECT` sobre vistas + 1 `GRANT SELECT` sobre `Security.Permission` (dep cross-schema de la vista
  de Navigation). Script + listas en el paquete fuente del Operador (context_refs, FUERA del hub).

## Accion Codex
Cablear el harness de **paridad exec-vs-endpoint** a la cadena de conexion del **sandbox** con el rol
`budget_sandbox_verifier`. Ese rol **reemplaza** a `nova_sql_connector_readonly_s9` para PARIDAD: el
readonly_s9 solo tenia SELECT/VIEW DEFINITION (verificacion de EXISTENCIA, F-NOVA-01); la paridad exige
EXECUTE, ahora disponible en sandbox. Columna del schema: `paridad_exec_vs_endpoint` (pass/fail/NA).

## Hardening recomendado (relayar al Operador/DBA)
El script tiene `THROW 51010` que solo valida que el rol exista, **no** la identidad de la BD -> si se
corre por error contra prod, otorga EXEC de mutadores en produccion. Anadir al inicio:

    IF DB_NAME() NOT LIKE '%SANDBOX%' THROW 51011, 'Refuse: not a SANDBOX database', 1;

(o exigir que `budget_sandbox_verifier` exista SOLO en el sandbox). Fail-closed barato, elimina el footgun.

## Notas de integridad de estudio
- `Annul_Availability_Certificate` / `Annul_Commitment` **no** estan en la superficie (brechas B-04, aun no
  existen). Cuando hardening los entregue (`<=15-jul`) se anaden por **enmienda fechada** (s.5); PAR-2 sigue
  diferido. NO meterlos ahora.
- Los procs de la superficie **mutan** el sandbox -> el harness debe **resetear a la linea base sellada
  entre corridas** para paridad repetible (sandbox ya sellado con RESET verificado; asegura la invocacion).

## Prioridad
Por **debajo** del fix-loop de F3.3 (TASK-0249). Es prep para cuando abra el dev medido P2 / la paridad;
no compite con F3.3. Frontera: el SQL y el dominio Nova viven en el paquete fuente / instancia, NUNCA en
el core neutral.
