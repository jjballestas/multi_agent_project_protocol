# NOVA-Budget - Brief de dominio (para el Asesor, durable)

> Sintesis del paquete fuente D:\Agentes\Ingenas\Budget (absorbido 2026-07-04 via 3 exploradores +
> lectura directa del GOAL y los 2 docs de ESTUDIO). Para no re-correr la exploracion en frio.
> Fuente de verdad del diseno = ese paquete (FUERA del hub). El hub guarda la derivacion gobernada (SPECs).

## Que es
NOVA Financiero Publico: presupuesto, tesoreria, contabilidad, control de pagos, nomina, IA asistida,
para la EMPRESA del operador (entidades publicas colombianas). Empieza por el modulo BUDGET.
NO es green-field: la BD SQL Server ya esta construida, ENDURECIDA y RECONCILIADA AL CENTAVO contra el
legacy (VB6/Access Pres00Xt). 45 tablas / 50 vistas / 14 procs / 35 triggers en DbsFinanciero.Budget.
Modelo HIBRIDO: 2024-2026 historico-fiel read-only (defectos D1-D10 = artefactos de carga documentados,
no se corrigen); 2027 = arranque limpio bajo controles fuertes.

## El corazon: la cadena de gasto presupuestal
Documentos encadenados, cada eslabon consume saldo del anterior, control validado EN LA BD bajo
UPDLOCK/HOLDLOCK + XACT_ABORT (una transaccion; si no hay saldo, falla; jamas se edita un aprobado):

  Apropiacion -> CDP -> Compromiso(RP) -> Obligacion -> Pago(Egreso de Tesoreria)

Las 4 reglas de oro (RN-01 de cada etapa):
1. CDP <= apropiacion vigente - CDP activos G          (Approve_Availability_Certificate_Draft, THROW 50150)
2. RP  <= CDP - RP activos G +- ajustes 11/12           (Approve_Commitment_Draft, THROW 50115)
3. OBL <= RP - OBL activos G +- ajustes 11/12           (Approve_Obligation_Draft, THROW 50134)
4. Pago<= OBL - pagos activos                           (Approve_Payment_Draft, THROW 50187)
Herencia estricta: el RP hereda rubro-fuente-BPIN del CDP; no puede imputar combinaciones nuevas.

## Principio load-bearing (la regla que todo dev puede violar)
LA BD MANDA. Lo transaccional (saldos, cuadres, numeracion, cierre) VIVE en procedimientos SQL
controlados. C# MODELA documentos y DELEGA la mutacion al proc; NUNCA reimplementa la aritmetica de
saldos en C# (= doble verdad, divergencia silenciosa). Es el punto 2 del adversarial de 12 puntos y
causa de RECHAZO inmediato. Mutar = solo via Approve_*/Apply_*/Annul_*/Reverse_*.

## Arquitectura y reglas duras
- Clean Architecture .NET 10: NOVA.Api / Application / Domain / Infrastructure / Contracts / Mcp +
  apps/nova-web (React 18 + TS 5 + Vite). tests: Unit / Integration / Architecture.
- Stack: ASP.NET Core, SQL Server 2025, EF Core 10 + Dapper + gateways de SP, FluentValidation,
  OpenTelemetry, OIDC (usuarios) + JWT scopes (APIs internas: budget:read/write/approve).
- 10 reglas no negociables del GOAL: React/MCP/IA nunca tocan SQL (solo APIs auditadas); C# no duplica
  reglas SQL; cero DataTable entre capas; cero DLLs manuales; THROW -> ProblemDetails (codigo+campo);
  toda mutacion deja auditoria (usuario real + correlation-id con task_id + evidencia); brechas de BD
  NO se parchean en C# (regla 8) -> se reportan; doc curada al dia; evidencia real (paridad EXEC vs endpoint).
- Anti-patrones prohibidos (11, del legacy ExperienciasGH): WebForms/PageMethods, DataTable como contrato,
  DLLs a bin por HintPath, SQL directo desde React/MCP, centinelas -99/"99", conexiones manuales por clase,
  secretos en .config, reimplementar saldos en C#, capa DATABASE generica.
- Architecture tests impiden filtracion de capas (Domain sin Infra; Application sin ASP.NET; Api/Mcp sin SQL).

## Multitenant + seguridad IA/MCP (cross-cutting, obligatorio)
- Todo dato de negocio lleva tenant_id; SESSION_CONTEXT(N'tenant_id') presente en toda transaccion o THROW 50100.
- Terceros != usuarios: Core.Terceros (sujeto economico, sin credenciales) vs Security.Users/TenantUsers.
  Terceros colombianos: NATURAL/JURIDICA, multiples identificaciones (CC/CE/NIT/RUT...) = un solo tercero;
  roles de negocio (beneficiario CDP, proveedor, contribuyente) separados de la identidad.
- IA/MCP = identidades no humanas (Integration.ApiClients, OAuth client-credentials/JWT), scopes por tool,
  McpConsents por tenant, TODO por procs autorizados, auditoria en Audit.McpToolInvocations. Cero SQL libre.

## Estado real: que esta LISTO vs que FALTA (clave para dimensionar el build)
LISTO (BD endurecida, verificada): parametrizacion, apropiacion, CDP, RP, OBL, pago, modificaciones
(01-04 apropiacion, 08-14 cadena), reversos, cierre anual (Constitute_Reserves/Payables, Close_Fiscal_Year,
snapshot, acarreo con exclusion SGR bienal), numeracion por series, 60+ guardas THROW, reconciliacion
legacy al centavo 2024-2026, 30 catalogos regulatorios (30063 items).
FALTA (= el desarrollo NOVA, ~45-55% son SUPERFICIES sobre procs/vistas ya existentes):
- Superficie CRUD de TODOS los borradores (API + DTO + UI + paridad) sobre procs que YA existen.
- Read-model: Get_Budget_Execution_Report (15 params, 50 cols; paridad ~652 filas 2026) = P2, primer valor.
- BRECHAS DE VERDAD (proc NO existe -> dev nuevo, y el dev JAMAS los crea; van a nova-hardening, regla 8):
  Liquidate_Radication / motor de retenciones (PRES_06 B-01/B-05), Annul_Availability_Certificate y
  Annul_Commitment (PRES_08 B-04), generadores regulatorios CUIPO/SIA/CHIP-FUT/APUI (PRES_12, no existen),
  PAC completo (PRES_10), control de saldo por BPIN (PRES_04 B-02), vista CDP con committed_amount real
  (hoy 0 -> saldos inflados, PRES_04 B-01), homologacion regulatoria 6045/7955 pendientes.

## Conexion con el ESTUDIO y GOAL-P1 (mi carril)
- GOAL-P1 = backlog P1 "Fundacion tecnica": NOVA.sln + nova-web + health/OpenAPI/ProblemDetails/logging+
  correlation-id + architecture tests + CI. PURO scaffolding, SIN dominio. EXCLUIDO del contraste del estudio
  y ademas es el PILOTO de la maquinaria de medicion (valida captura de tokens end-to-end). Brazo baseline
  = "NOVA_PROMPT integro" (SPEC 10 campos + pre-vuelo + adversarial informal 12 puntos + DoD), mono-orquestador.
- Implicacion de asesoria: como lo transaccional YA vive en SQL, gran parte del "dev" baseline es SPEC +
  wiring API/DTO/UI + tests de PARIDAD, no logica de negocio novel -> territorio natural de codegen/peon;
  la frontera (logica) esta mayormente en la BD. Refuerza: peones fuera del brazo baseline y de los brazos Q4;
  su efecto se estudia aislado en F6. El riesgo #1 del baseline es reimplementar saldos en C# (adversarial pto 2).
- PAR-2 del estudio (Annul_* superficie) es CONDICIONAL a que nova-hardening entregue esos procs <=15-jul;
  si no, PAR-2 cae. Coherente con "el dev nunca crea el proc" (regla 8).

## Documentos fuente (para citar en SPECs, sin supuestos)
NOVA_GOAL_Desarrollo_Aplicacion.md (contrato + backlog P1-P6 + DoD); NOVA_Arquitectura_y_Estandar_Desarrollo.html
+ apendice DotNet10; NOVA_PRES_00..12 (proceso, RN-XX + THROW por etapa + brechas B-XX); NOVA_SPEC_Plantilla_
Requisitos.md (10 campos + adversarial 12 puntos); NOVA_PROMPT_Arranque_Agente_Desarrollo.md (10 reglas +
acceso BD readonly s9 vs runtime nova_app_budget). Estudio: NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md +
NOVA_ESTUDIO_Protocolo_Medicion.md (redactados por el Asesor).
