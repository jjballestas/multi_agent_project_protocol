# SPEC-CONT-S6A - Informe trimestral CGN/CHIP (Slice 6A, mutador + export)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR + EXPORT: importa el catalogo de cuentas validas CGN/CHIP versionado, crea el
> reporte trimestral (suma D/C del trimestre, calcula saldo final con signo CHIP), lo exporta al centavo y confirma
> el envio (actualiza P05). Los procs YA EXISTEN (hardening del DBA en schema/027, base congelada
> ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI). PREP de Sprint 1 (DIRECTIVA
> Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 6A + seccion D
> (F-NOVA-01, 2026-07-10) + patron gobernado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S6A - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide. Criticidad de INTEGRIDAD **ALTA** (reporte
  regulatorio al centavo + confirmacion que avanza P05). Si mide como par, aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Import_Cgn_Chip_Valid_Account_Catalog`, `Create_Cgn_Chip_Quarterly_
  Report`, `Get_Cgn_Chip_Quarterly_Report_Export`, `Confirm_Cgn_Chip_Quarterly_Report_Submission` EXISTEN
  (schema/027, nuevos en la base congelada), desplegados+verificados en las 3 BD. `GRANT EXECUTE` sobre los 4 procs
  concedido al rol **`accounting_sandbox_verifier`** (estan entre las 33 rutinas). Set REAL de THROW capturado
  (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD -- "nuevo en schema/027"):**
  - `Accounting.Import_Cgn_Chip_Valid_Account_Catalog` **54400-54413**.
  - `Accounting.Create_Cgn_Chip_Quarterly_Report` **54420-54441**.
  - `Accounting.Get_Cgn_Chip_Quarterly_Report_Export` **54450-54451**.
  - `Accounting.Confirm_Cgn_Chip_Quarterly_Report_Submission` **54452-54457** (actualiza P05 al confirmar envio).
  - Mapa legacy: ContA045f (Proceso Chip, informe trimestral) -> import catalogo -> create report -> get export ->
    confirm submission; MacoR033f/MaCGn002f (Impresion CGN / Reporte CGN002) = export encabezado/detalle al centavo.
  - El proceso schema/027: carga catalogo CHIP versionado, carga saldos iniciales CHIP validados, suma D/C del
    trimestre, calcula saldo final con signo CHIP, exporta al centavo y actualiza P05 al confirmar envio.
  - El maker RE-CONFIRMA cada set, la semantica de P05, el versionado del catalogo, el formato de export al centavo
    y los nombres exactos de columna del result-set contra `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_
    set` del proc DESPLEGADO antes de fijar criterios; no asumir por analogia.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** importar catalogo / crear reporte / exportar / confirmar
  envio exigen rol de REPORTE REGULATORIO CGN/CHIP via `[Authorize]`/`RequireAuthorization` real; sin sesion/rol
  valido -> 401/403 antes de tocar el proc/gateway (patron P4-006 s.6h). La confirmacion (que avanza P05) puede
  exigir un rol/paso adicional (RE-CONFIRMAR).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs verificados por el DBA (base congelada, schema/027). El maker RE-VERIFICA contra la BD
  desplegada el set exacto de THROW y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre
  capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario regulatorio IMPORTA el catalogo de cuentas validas CGN/CHIP (versionado,
`Import_Cgn_Chip_Valid_Account_Catalog`, 54400-54413), CREA el reporte trimestral que suma D/C del trimestre y
calcula el saldo final con signo CHIP (`Create_Cgn_Chip_Quarterly_Report`, 54420-54441), OBTIENE el export al
centavo (`Get_Cgn_Chip_Quarterly_Report_Export`, 54450-54451) y CONFIRMA el envio
(`Confirm_Cgn_Chip_Quarterly_Report_Submission`, 54452-54457), que actualiza P05. Toda la logica (versionado del
catalogo, suma D/C, signo CHIP, formato de export al centavo, avance de P05) vive en los procs; C# NO reimplementa
el calculo ni el formato.
- Fuente: WS1 Slice 6A + seccion D; NOVA-PRES patron mutador/export (P4-006).
- Calidad: falsable. Bien: "confirmar el envio de un reporte trimestral no creado (o ya confirmado) devuelve
  ProblemDetails del THROW real (54452-54457) y NO avanza P05; y C# no calcula la suma D/C ni el signo CHIP ni el
  redondeo al centavo -- los da el proc".

## 2. Usuario objetivo definido
Rol **Reporte regulatorio CGN/CHIP** (autenticado + verificado, s.6f). Importa el catalogo, genera y exporta el
reporte trimestral y confirma el envio con usuario real (del contexto de auth), motivo y correlation-id/task_id para
auditoria. No captura comprobantes (S2) ni concilia CHIP de contingencia (S5).

## 3. Alcance definido
- **Importar catalogo:** `Import_Cgn_Chip_Valid_Account_Catalog` (54400-54413) -- carga el catalogo de cuentas
  validas CGN/CHIP versionado.
- **Crear reporte:** `Create_Cgn_Chip_Quarterly_Report` (54420-54441) -- suma D/C del trimestre, calcula el saldo
  final con signo CHIP.
- **Exportar:** `Get_Cgn_Chip_Quarterly_Report_Export` (54450-54451) -- devuelve el export al centavo
  (encabezado/detalle).
- **Confirmar envio:** `Confirm_Cgn_Chip_Quarterly_Report_Submission` (54452-54457) -- marca el envio y ACTUALIZA
  P05 (control de periodo trimestral). Accion explicita con confirmacion.
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** esta superficie NUNCA expone ni activa la escotilla
  `SESSION_CONTEXT('accounting_annual_close')` (interna del cierre anual, S6B). El avance de P05 lo hace el proc de
  confirmacion, no C#.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **CHIP contingencia** (S5), **captura general** (S2), **cierre mensual/anual** (S3/S6B), **saldos iniciales**
  (S4), **reportes RO** (S1), **causacion de ingresos** (S6C): FUERA.
- **La escotilla annual_close:** NO se expone ni activa desde esta superficie.
- **Reimplementar la suma D/C / el signo CHIP / el redondeo al centavo / el versionado del catalogo / el avance de
  P05 en C#:** los enforzan los procs; la superficie solo invoca, traduce y presenta el export.
- **El ajuste de un peso `Cuadrar_Dbt_Crd`:** retirado en WS1 (el proc no lo reproduce).
- **Construir/modificar los procs:** ya existen (schema/027); esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Import_Cgn_Chip_Valid_Account_Catalog`, `Create_Cgn_Chip_Quarterly_Report`,
  `Get_Cgn_Chip_Quarterly_Report_Export`, `Confirm_Cgn_Chip_Quarterly_Report_Submission` (schema/027). Firma EXACTA,
  formato del export al centavo, semantica de P05 y nombres de columna del result-set: extraidos de
  `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no asumidos.
- **THROW:** el set REAL de la seccion D (DoR). El maker mapea cada codigo a su regla (catalogo invalido/version,
  reporte sin catalogo, export sin reporte, confirmacion invalida/ya-confirmada, P05, tenant).
- **API:** `POST /api/accounting/cgn-chip/catalog/import` · `POST /api/accounting/cgn-chip/quarterly-reports` (crear)
  · `GET /api/accounting/cgn-chip/quarterly-reports/{id}/export` · `POST /api/accounting/cgn-chip/quarterly-reports/
  {id}/confirm-submission`. ProblemDetails por THROW; todos bajo `[Authorize]` con rol regulatorio (s.6f).
- **UI (apps/nova-web):** proceso CHIP trimestral: importar catalogo, generar el reporte, previsualizar/descargar el
  export al centavo, confirmar el envio con confirmacion; muestra ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/CgnChip/` (mapea, traduce THROW; NO reimplementa suma/signo/
  redondeo/versionado/P05).
- **Referencias:** WS1 Slice 6A + seccion D; patron congelado NOVA-SPEC-T-001 (P4-006).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion/generacion SOLO por los procs; jamas DML directo ni recalculo de suma D/C / signo CHIP / redondeo /
    versionado / P05 en C#.
  - (b) **EXPORT AL CENTAVO SIN RECALCULO:** el export lo produce `Get_..._Export`; C# NO redondea ni reformatea los
    montos (solo serializa lo que el proc entrega, al centavo). Un redondeo en C# divergiria del export regulatorio.
  - (c) **CONFIRMACION EXPLICITA QUE AVANZA P05:** la confirmacion de envio es una accion explicita con
    confirmacion; el avance de P05 lo hace el proc. C# NO decide el avance del periodo.
  - (d) **INVARIANTE DE INTEGRIDAD (escotilla annual_close, NO RELAJAR):** la superficie NUNCA setea
    `SESSION_CONTEXT('accounting_annual_close')`.
  - (e) DTOs 1:1; THROW->ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario real
    (del contexto de auth) en cada operacion.
  - (f) **AUTORIZACION REAL:** cada endpoint (importar/crear/exportar/confirmar) exige `[Authorize]`/
    `RequireAuthorization` con rol regulatorio real; sin sesion/rol valido -> 401/403 antes de tocar el gateway/proc.
    Test de arquitectura mecanico (falla si se remueve el atributo/policy).
  - (g) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (h) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida (catalogo,
    reporte, export, estado de confirmacion) confirmado contra `OBJECT_DEFINITION`; sin fallback ni default
    silencioso; el harness ejercita el MISMO camino.
  - (i) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (importar/crear/exportar/confirmar) tiene
    >=1 test de integracion HTTP (`WebApplicationFactory` + gateway falso).
  - (j) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye los 4 procs
    CGN/CHIP en los literales prohibidos; excepciones documentadas, no omitidas.
  - (k) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14):** la lectura del catalogo, del reporte y del export aisla
    por tenant de forma DEMOSTRABLE (filtro explicito o vista/RLS que consuma `SESSION_CONTEXT('tenant_id')`
    verificado contra `OBJECT_DEFINITION`); no basta `sp_set_session_context` si el objeto leido no lo consume.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** un catalogo valido y un usuario CON rol regulatorio, **cuando** importa el catalogo y crea el reporte,
   **entonces** `Import_Cgn_Chip_Valid_Account_Catalog` versiona el catalogo y `Create_Cgn_Chip_Quarterly_Report`
   genera el reporte con la suma D/C y el signo CHIP (verificable via lectura), sin que C# calcule.
2. **Dado** un reporte creado, **cuando** obtiene el export, **entonces** `Get_..._Export` devuelve el export al
   centavo (encabezado/detalle) y C# lo serializa SIN redondear ni reformatear.
3. **Dado** un reporte listo, **cuando** confirma el envio, **entonces** `Confirm_..._Submission` marca el envio y
   avanza P05 (verificable via lectura); un intento de confirmar un reporte no creado o YA confirmado ->
   ProblemDetails del THROW real (54452-54457) y NO avanza P05.
4. **Dado** un catalogo invalido o version incorrecta (RE-CONFIRMAR la regla), **entonces** ProblemDetails del THROW
   real de `Import_Cgn_Chip_Valid_Account_Catalog` (54400-54413) y NO se importa.
5. **Dado** un reporte sobre un trimestre sin catalogo cargado (o precondiciones no cumplidas, RE-CONFIRMAR),
   **entonces** ProblemDetails del THROW real de `Create_Cgn_Chip_Quarterly_Report` (54420-54441) y NO se crea.
6. **Dado** una operacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto).
7. **Dado** un usuario SIN rol regulatorio (o sin autenticar), **cuando** intenta importar/crear/exportar/confirmar,
   **entonces** 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
8. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA limpio)
   -- sin mock/`Recording*`.
9. **Dado** el gateway de produccion, **entonces** lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin
   fallback ni default silencioso; el harness ejercita el MISMO camino (#11).
10. **Dado** cada endpoint (importar/crear/exportar/confirmar), **entonces** tiene >=1 test de integracion HTTP
    (#12).
11. **Dado** el test de aislamiento del frontend, **entonces** incluye los 4 procs CGN/CHIP; excepciones
    documentadas (#13).
12. **Dado** la lectura del reporte/export entre dos tenants A y B, **cuando** A consulta datos de B por IDs,
    **entonces** el gateway NO devuelve datos de B (filtro tenant o vista/RLS verificada) -- negativo cross-tenant
    explicito (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de importar/crear/exportar/confirmar; traduccion THROW->ProblemDetails; enforcement de que la
  suma/signo/redondeo/P05 NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA setea la
  escotilla annual_close.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los 4 procs CGN/CHIP, #13); Mcp sin SQL; cero
  DataTable; test de autorizacion (endpoints con `[Authorize]`/policy); **test mecanico: ningun archivo de la unidad
  setea `SESSION_CONTEXT('accounting_annual_close')`** (integrity invariant).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1
  (importar+crear), criterio 2 (export al centavo), criterio 3 (confirmar + P05), un caso por THROW ALCANZABLE
  (54400-413, 54420-441, 54450-451, 54452-457, tenant) RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio 7
  (401/403). Seed limpio (tenant ACCTVERIFY, fuente TST, vigencias 2024/2025) dentro de la transaccion con ROLLBACK.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad) + CI + F-NOVA-01 (cada THROW verificado; el formato del export al
  centavo y la semantica de P05 confirmados) + guard de procedencia + aislamiento de tenant + autorizacion real +
  DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Recalcular la suma D/C / el signo CHIP / el redondeo al centavo en C# | Divergencia con el export regulatorio; reporte incorrecto | Restricciones 6a/6b + criterios 1/2; adversarial y checker formal verifican el diff |
| Avanzar P05 desde C# en vez del proc de confirmacion | Estado de periodo inconsistente; confirmacion sin sustento | Restriccion 6c + criterio 3; el avance de P05 lo hace `Confirm_..._Submission` |
| Confirmar un reporte no creado o ya confirmado (doble envio) | Envio regulatorio duplicado/invalido | Criterio 3 (negativo 54452-54457) |
| Asumir el mapeo THROW o el formato del export por analogia | Criterio apunta al THROW incorrecto; export mal formado | F-NOVA-01: RE-CONFIRMAR 54400-54457 + el formato del export + P05 contra OBJECT_DEFINITION |
| Autorizacion decorativa sin verificacion real de rol | Reporte/confirmacion sin rol (gap #5/#8) | Restriccion 6f + criterio 7 + test de arquitectura mecanico |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6g): clase SQL real via accounting_sandbox_verifier, sin credenciales |
| Fuga de tenant en la lectura del reporte/export | Confidencialidad (hallazgo #14) | Restriccion 6k + criterio 12 (negativo cross-tenant) |

## 10. Prioridad definida
**GOAL reporte regulatorio CGN/CHIP** (obligacion externa trimestral; export al centavo + confirmacion que avanza
P05). Pertenencia Q4: segun sorteo del sello si mide (criticidad de INTEGRIDAD alta). Severidad: mutador + export
regulatorio con confirmacion que avanza el control de periodo trimestral. Dependencias: procs CGN/CHIP (existen,
base congelada schema/027), patron congelado NOVA-SPEC-T-001, diseno de autorizacion real (s.6f). **LINEA ROJA:
esta unidad NO SE CONSTRUYE antes del 30-jul** (pool Q4/gobernado); esta SPEC es DISENO/PREP unicamente. Relacion:
consume los saldos conciliados de CHIP contingencia (S5) y el catalogo versionado.
