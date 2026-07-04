# SPEC-NOVA-P2-002 - Read model de parametros (rubros / fuentes / rubro-fuente / BPIN / series) [BASELINE, fuera de contraste]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo BASELINE, unidad P2.1 mandada por
> el GOAL, FUERA del contraste (no es miembro de par ni del pool Q4). Preparada por el Arquitecto (arq+docs) FUERA
> de la ventana medida; el dev MEDIDO de P2.1 NO abre pre-sello. SPEC NUEVA (no preexistia).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P2-002 - task_id (hub): TASK-VISION-NOVA (prep P2, post-sello)
- owner_maker: agente desarrollador de la instancia (Sprint 1 baseline); repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial, nunca
  self-review; DIRECTIVA operador 2026-07-04). Brazo baseline: checker vivo = adversarial informal (NO checker
  formal del Analista; checker_formal=0). tokens_adversarial_informal taggeados a esa sesion separada.
- arm: baseline - unit: P2.1 read model de parametros (M). NO es miembro de par.
- q4_membership: **FUERA** (unidad baseline mandada por el GOAL, fuera del contraste y del pool Q4).
- isolation: NA (no es unidad de par; es lectura de catalogos de parametrizacion, no consume codigo hermano).
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> misma clase de sesion/runtime
  que su comparador o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable
  -> tokens_total_atribuibles. checker_formal=0, coordinacion_gobierno=0 (baseline).
- **deuda GOAL-P1 (bloqueante de front P2):** el harness de test del front de Nova-Budget (apps/nova-web) debe
  correr VERDE en clon limpio ANTES de la UI de esta unidad (evita gate falso-verde tipo TASK-0209).
- db_verified_at: vistas de NOVA-PRES-01 (BD DbsFinanciero readonly; parametrizacion es solo lectura via vistas,
  sin procs salvo el numerador); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025
  via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto CONSULTA los catalogos de parametrizacion sobre los que se apoya toda la cadena de gasto
-- rubros (jerarquia, naturaleza, rol), fuentes de financiacion, cruces rubro-fuente, proyectos de inversion (BPIN)
con su detalle/saldo, y series documentales -- sirviendose EXCLUSIVAMENTE de las vistas `vw_*` existentes, sin
reimplementar logica ni tocar CRUD.
- Fuente: NOVA-GOAL-001 s.8 (P2 read model) + s.9 (endpoints) + NOVA-PRES-01 (Parametrizacion) s.3/s.5.
- Calidad: falsable. Bien: "el endpoint de rubros por vigencia devuelve exactamente las filas de
  `vw_Budget_Account_Fiscal_Year` para esa vigencia (paridad de conteo 1940 filas / 970 rubros)".

## 2. Usuario objetivo definido
Rol **Consulta / Gestion de presupuesto** (solo lectura). Sin matriz de autorizacion por operacion (sin mutaciones);
supuesto temporal: usuario autenticado del modulo puede consultar los catalogos. Es la superficie de lectura de
parametros que alimenta los formularios de la cadena de gasto (drafts P3+).

## 3. Alcance definido
Endpoints de lectura (GOAL s.9), UNO por catalogo, con `fiscal_year_id` + `tenant_id` como filtro comun:
1. **Rubros** -> `GET /api/budget/parameters/accounts` sobre `Budget.vw_Budget_Account_Fiscal_Year` (jerarquia,
   naturaleza income/expense RN-01, tipo 0-Funcionamiento/1-Inversion, rol major/auxiliary, parent self-FK,
   is_active RN-18).
2. **Fuentes de financiacion** -> `GET /api/budget/parameters/funding-sources` sobre `Budget.vw_Funding_Source_*`
   (funding_source_code unico, tipo catalogo `budget_funding_source_type`, flag `excludes_annual_carryover` SGR).
3. **Rubro-fuente** -> `GET /api/budget/parameters/account-funding-sources` sobre
   `Budget.vw_Budget_Account_Funding_Source` (el par imputable; filtrable por rubro y por fuente).
4. **Proyectos de inversion (BPIN)** -> `GET /api/budget/parameters/investment-projects` sobre
   `Budget.vw_Investment_Project*` + `Budget.vw_Investment_Project_Detail_Balance` (project_code; valor por
   rubro-fuente; saldo = valor + Sigma aumentos - Sigma disminuciones).
5. **Series documentales** -> `GET /api/budget/parameters/document-series` sobre `Budget.Document_Series`
   (document_type/regime unico, series_code, pad_length default 5, is_user_allocatable). **GAP declarado:** NO
   existe `vw_Document_Series` citada -> se sirve de la tabla catalogo `Budget.Document_Series`; se declara el gap
   de la vista de lectura (candidato a hardening), NO se hace SELECT ad-hoc a tablas transaccionales.
Filtros por catalogo: naturaleza/tipo/rol/parent (rubros), tipo/SGR (fuentes), rubro|fuente (cruce), project_code
(BPIN), tipo/regimen (series). `is_active` (soft-delete RN-18) explicito en todos.

## 4. Fuera de alcance definido
- **CRUD de parametros** (crear/editar rubros/fuentes/proyectos, B-01 de PRES-01): FUERA (solo lectura).
- **Enforcement BPIN-requerido** (B-02, RN-13 "SPEC"), **austeridad** (B-03), **programas/subprogramas** (B-04),
  **autorizacion por operacion** (B-05), **homologaciones pendientes** (B-06), **roll-forward de vigencia** (B-07):
  todo el s.6 de PRES-01 esta FUERA (P2.1 es solo el read model).
- **El numerador** `Budget.Allocate_Document_Number` (mutacion usada solo dentro de aprobaciones): FUERA del read
  model; NO se invoca aqui.
- Cualquier MUTACION o reimplementacion de saldos/jerarquia en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; parametrizacion = lectura via vistas):**
  - Vistas (canal de lectura, PRES-01 s.5): `vw_Budget_Account_Fiscal_Year`, `vw_Budget_Account_Funding_Source`,
    `vw_Budget_Account_Integrations`, `vw_Funding_Source_*`, `vw_Investment_Project*` + `vw_Investment_Project_Detail_Balance`,
    `vw_Budget_Movement_Type`, `vw_Budget_Accounting_Use`, `vw_Reporting_Catalog_Usage`.
  - Series: tabla catalogo `Budget.Document_Series` (24 filas) -- GAP de vista de lectura declarado.
  - Tablas base (referencia/verificacion, NO consultar directo): `Budget.Budget_Account` (970),
    `Budget.Budget_Account_Fiscal_Year` (1940), `Budget.Funding_Source` (65), `Budget.Funding_Source_Fiscal_Year`
    (130), `Budget.Budget_Account_Funding_Source` (1812), `Budget.Investment_Project` (600),
    `Budget.Investment_Project_Detail` (2936), `Budget.Budget_Movement_Type` (30), `Budget.Document_Series` (24).
- **API:** 5 endpoints GET de lectura con los filtros por query; DTO 1:1 con la vista; ProblemDetails en params
  invalidos.
- **UI (apps/nova-web):** grillas de catalogo con filtros (naturaleza/tipo/rol; SGR; rubro/fuente; BPIN; serie);
  vigencia explicita; is_active como filtro.
- **Capa Application:** `NOVA.Application/Budget/Parameters/` (GetAccounts, GetFundingSources,
  GetAccountFundingSources, GetInvestmentProjects, GetDocumentSeries; cada uno mapea filtros -> params del gateway
  sobre la vista).
- **Referencias:** NOVA-PRES-01 (s.3 semantica, s.5 contrato de lectura, s.6 fuera de alcance), NOVA-GOAL-001
  (GOAL-P2 s.8/s.9). (Read-only; no consume procs de mutacion.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa; gateways tipados; cero
  DataTable) + stack del preambulo.
- Propias:
  - (a) Solo LECTURA via las vistas `vw_*`; jamas DML ni SELECT ad-hoc a tablas base; la jerarquia/naturaleza vive
    en la vista, la app NO la recalcula (RN-09 de PRES-11 aplicado al read model).
  - (b) Cada catalogo se sirve de SU vista canonica; si falta la vista (series), se declara el GAP y se usa la
    tabla catalogo, NO un SELECT a tablas transaccionales.
  - (c) DTOs 1:1 con las columnas de la vista (sin inventar/omitir); `is_active` explicito (soft-delete RN-18).
  - (d) Filtro comun `fiscal_year_id`+`tenant_id` obligatorio (todo esta versionado por vigencia, RN-04/07/09/10).
  - (e) ProblemDetails en params invalidos (validacion de aplicacion); consulta valida sin datos = 200 vacio.
  - (f) Correlation id + task_id en cada consulta (observabilidad; regla 8/DoD).

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **Dado** el endpoint de rubros por `fiscal_year_id`, **cuando** consulto, **entonces** recibo exactamente las
   filas de `vw_Budget_Account_Fiscal_Year` de esa vigencia -- paridad de conteo (referencia: 1940 filas / 970
   rubros; ajustar a la vigencia).
2. **Dado** rubros con `account_nature='income'` vs `'expense'`, **entonces** el filtro segrega correctamente
   (RN-01; ningun rubro es ambos).
3. **Dado** el cruce rubro-fuente, **entonces** las filas coinciden con `vw_Budget_Account_Funding_Source`
   (referencia 1812) filtradas por rubro/fuente.
4. **Dado** un BPIN, **entonces** su detalle y saldo coinciden con `vw_Investment_Project_Detail_Balance`
   (valor + aumentos - disminuciones), sin recalculo en C#.
5. **Dado** las series documentales, **entonces** devuelve las 24 filas de `Budget.Document_Series` con series_code
   y pad_length; el GAP de vista de lectura queda declarado (no SELECT ad-hoc a transaccionales).
6. **Dado** `is_active=0`, **entonces** el comportamiento de soft-delete es explicito (incluye/excluye por
   parametro, RN-18).
7. **Dado** params invalidos (vigencia inexistente), **entonces** 400 ProblemDetails; consulta valida sin datos =
   200 con resultset vacio.

## 8. Pruebas / gates definidos
- **Unit:** mapeo filtros -> params del gateway por catalogo; validacion -> ProblemDetails; mapeo vista -> DTO 1:1;
  soft-delete.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; Mcp sin SQL; cero DataTable.
- **Integracion vs DbsFinanciero:** criterios 1-6 (paridad de conteo/columnas de cada catalogo contra su vista;
  BPIN saldo vs `vw_Investment_Project_Detail_Balance`; series vs tabla catalogo). EXECUTE: NO requerido -- son
  vistas readonly (SELECT + VIEW DEFINITION del conector `nova_sql_connector_readonly_s9` bastan; el adversarial
  verifica existencia de cada `vw_*` via sys.columns/OBJECT_DEFINITION y corre SELECT para el conteo).
- **Gate final:** APROBADO del **adversarial informal de 12 puntos en SESION SEPARADA / contexto limpio** (checker
  vivo del brazo baseline; dev != adversarial) + arch tests + CI verde + DoD de NOVA-GOAL-001 con evidencia real
  (paridad de conteos, ProblemDetails, OpenAPI) + verde de gates del hub + atestacion sha256. checker_formal=0.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| SELECT ad-hoc a tablas base (por la vista de series ausente) | Rompe el canal de lectura | Restriccion 6b: usar la tabla catalogo `Document_Series` + declarar el gap de vista |
| Recalcular jerarquia/saldo BPIN en C# | Divergencia con la BD | Restriccion 6a; adversarial punto 2; paridad vs vistas |
| Omitir `fiscal_year_id` (datos cruzados entre vigencias) | Resultado incorrecto | Restriccion 6d: filtro obligatorio |
| Soft-delete no explicito (is_active) | Filas fantasma/faltantes | Restriccion 6c/criterio 6 |
| DTO que inventa/omite columnas | Contrato inestable | Restriccion 6c: DTO 1:1 |
| adversarial en la misma sesion del maker | Contaminacion del brazo | DoR: adversarial en SESION SEPARADA (DIRECTIVA operador) |

## 10. Prioridad definida
**GOAL-P2** (read model / parametros), brazo BASELINE, unidad mandada por el GOAL. **Pertenencia Q4: FUERA**
(fuera del contraste y del pool Q4). Severidad s.08: superficie de lectura de catalogos (fundacion de datos de los
formularios de la cadena). Dependencias: GOAL-P1 (fundacion) + las vistas de parametrizacion (existen). GAP
declarado: vista de lectura de series documentales (candidato a hardening; no bloquea el read model, se sirve del
catalogo). Desbloquea: los formularios de la cadena de gasto (P3) que consumen los catalogos.
