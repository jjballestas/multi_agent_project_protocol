# SPEC-CONT-S5 - CHIP contingencia: conciliacion y ajuste (Slice 5, mutador)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR: revision CHIP de contingencia -- arma un lote de saldos para el reporte CHIP
> (`Create_Chip_Report_Balance_Batch`), obtiene la diferencia de conciliacion (`Get_Chip_Reconciliation_Difference`)
> y publica un comprobante de ajuste CHIP (`Post_Chip_Adjustment_Voucher`). Los procs YA EXISTEN (hardening del DBA,
> base congelada ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI). PREP de Sprint 1
> (DIRECTIVA Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 5 +
> seccion D (F-NOVA-01, 2026-07-10) + patron gobernado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S5 - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide. Criticidad de INTEGRIDAD **ALTA** (el ajuste CHIP
  publica un comprobante de ajuste; su superficie no reimplementa la conciliacion ni el signo CHIP). Si mide como
  par, aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Create_Chip_Report_Balance_Batch`, `Get_Chip_Reconciliation_Difference`,
  `Post_Chip_Adjustment_Voucher` EXISTEN, desplegados+verificados en las 3 BD. `GRANT EXECUTE` sobre los 3 procs
  concedido al rol **`accounting_sandbox_verifier`** (estan entre las 33 rutinas). Set REAL de THROW capturado
  (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD -- "sin divergencia"):**
  - `Accounting.Create_Chip_Report_Balance_Batch` **53900-53910**.
  - `Accounting.Get_Chip_Reconciliation_Difference` **53920-53923**.
  - `Accounting.Post_Chip_Adjustment_Voucher` **53940-53953**.
  - Mapa legacy: ContA044f (Revision Chip) -> `Create_Chip_Report_Balance_Batch` -> `Get_Chip_Reconciliation_
    Difference` -> `Post_Chip_Adjustment_Voucher`. schema/026. El proc de reporte NO reproduce el ajuste de un peso
    `Cuadrar_Dbt_Crd` (retirado en WS1).
  - El maker RE-CONFIRMA cada set, si `Post_Chip_Adjustment_Voucher` publica via `Post_Voucher` (por tanto sujeto a
    control de periodo / escotilla) o escribe directo, el signo CHIP, y los nombres exactos de columna del
    result-set contra `OBJECT_DEFINITION` del proc DESPLEGADO antes de fijar criterios; no asumir por analogia.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** armar lote / obtener diferencia / publicar ajuste exigen rol
  de CONCILIACION CHIP via `[Authorize]`/`RequireAuthorization` real; sin sesion/rol valido -> 401/403 antes de
  tocar el proc/gateway (patron P4-006 s.6h).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs verificados por el DBA (base congelada). El maker RE-VERIFICA contra la BD desplegada el set
  exacto de THROW y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre
  capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario de conciliacion ARMA un lote de saldos para el reporte CHIP de contingencia
(`Create_Chip_Report_Balance_Batch`, 53900-53910), OBTIENE la diferencia de conciliacion contra el saldo esperado
(`Get_Chip_Reconciliation_Difference`, 53920-53923) y, si procede, PUBLICA un comprobante de ajuste CHIP
(`Post_Chip_Adjustment_Voucher`, 53940-53953) que corrige la diferencia. Toda la logica (armado del lote, calculo de
la diferencia con signo CHIP, generacion del ajuste) vive en los procs; C# NO reimplementa la conciliacion ni el
signo CHIP ni el ajuste de un peso.
- Fuente: WS1 Slice 5 + seccion D; NOVA-PRES patron mutador (P4-006).
- Calidad: falsable. Bien: "publicar un ajuste CHIP para una diferencia inexistente (o fuera de las precondiciones)
  devuelve ProblemDetails del THROW real (53940-53953) y NO publica el comprobante; y C# no calcula la diferencia ni
  el signo CHIP -- los da el proc".

## 2. Usuario objetivo definido
Rol **Conciliacion CHIP** (autenticado + verificado, s.6f). Arma el lote, revisa la diferencia y publica el ajuste
con usuario real (del contexto de auth), motivo y correlation-id/task_id para auditoria. No captura comprobantes
generales (S2) ni emite el informe trimestral (S6A).

## 3. Alcance definido
- **Armar lote:** `Create_Chip_Report_Balance_Batch` (53900-53910) -- construye el lote de saldos para el reporte
  CHIP de contingencia.
- **Obtener diferencia:** `Get_Chip_Reconciliation_Difference` (53920-53923) -- calcula la diferencia de
  conciliacion (con signo CHIP); lectura/diagnostico.
- **Publicar ajuste:** `Post_Chip_Adjustment_Voucher` (53940-53953) -- genera el comprobante de ajuste que corrige
  la diferencia (RE-CONFIRMAR si publica via `Post_Voucher`).
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** si `Post_Chip_Adjustment_Voucher` publica via `Post_Voucher`, el
  ajuste queda sujeto al control de periodo (52204/52512) como cualquier comprobante; la superficie NUNCA setea la
  escotilla `SESSION_CONTEXT('accounting_annual_close')` (interna de S6B) para forzar el ajuste en periodo cerrado.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **Informe trimestral CGN/CHIP** (S6A), **captura general** (S2), **cierre mensual/anual** (S3/S6B), **saldos
  iniciales** (S4), **reportes RO** (S1), **causacion de ingresos** (S6C): FUERA.
- **Reproducir el ajuste de un peso `Cuadrar_Dbt_Crd`** como formulario legacy: retirado en WS1; el ajuste CHIP es
  el comprobante de `Post_Chip_Adjustment_Voucher`.
- **La escotilla annual_close:** NO se expone ni activa desde esta superficie.
- **Reimplementar la conciliacion / el signo CHIP / el calculo de la diferencia en C#:** los enforzan los procs; la
  superficie solo invoca y traduce.
- **Construir/modificar los procs:** ya existen; esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Create_Chip_Report_Balance_Batch`, `Get_Chip_Reconciliation_Difference`,
  `Post_Chip_Adjustment_Voucher` (schema/026). Firma EXACTA, semantica del signo CHIP y nombres de columna del
  result-set: extraidos de `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no
  asumidos.
- **THROW:** el set REAL de la seccion D (DoR). El maker mapea cada codigo a su regla (lote invalido, diferencia
  inexistente, ajuste fuera de precondiciones, periodo cerrado si publica via Post_Voucher, tenant).
- **API:** `POST /api/accounting/chip/report-balance-batches` (armar lote) · `GET /api/accounting/chip/
  reconciliation-difference` (obtener diferencia) · `POST /api/accounting/chip/adjustment-vouchers` (publicar
  ajuste). ProblemDetails por THROW; todos bajo `[Authorize]` con rol de conciliacion CHIP (s.6f).
- **UI (apps/nova-web):** revision CHIP: armado del lote, muestra de la diferencia de conciliacion, publicacion del
  ajuste con confirmacion; muestra ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/Chip/` (mapea, traduce THROW; NO reimplementa conciliacion/
  signo/ajuste).
- **Referencias:** WS1 Slice 5 + seccion D; patron congelado NOVA-SPEC-T-001 (P4-006).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion SOLO por los procs (`Create_Chip_Report_Balance_Batch`, `Post_Chip_Adjustment_Voucher`;
    `Get_Chip_Reconciliation_Difference` es lectura); jamas DML directo ni recalculo de conciliacion/signo/ajuste en
    C#.
  - (b) **INVARIANTE DE INTEGRIDAD (escotilla annual_close, NO RELAJAR):** la superficie NUNCA setea
    `SESSION_CONTEXT('accounting_annual_close')`; si el ajuste publica via `Post_Voucher`, respeta el control de
    periodo (no lo esquiva).
  - (c) **CONCILIAR ANTES DE AJUSTAR:** la superficie obtiene la diferencia (`Get_..._Difference`) antes de ofrecer
    el ajuste; el ajuste es accion explicita con confirmacion. C# NO decide si hay diferencia (la da el proc).
  - (d) DTOs 1:1; THROW->ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario real
    (del contexto de auth) en cada operacion.
  - (e) **AUTORIZACION REAL:** cada endpoint (armar/obtener/publicar) exige `[Authorize]`/`RequireAuthorization` con
    rol de conciliacion CHIP real; sin sesion/rol valido -> 401/403 antes de tocar el gateway/proc. Test de
    arquitectura mecanico (falla si se remueve el atributo/policy).
  - (f) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (g) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida (lote,
    diferencia con signo CHIP) confirmado contra `OBJECT_DEFINITION`; sin fallback ni default silencioso; el harness
    ejercita el MISMO camino.
  - (h) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (armar/obtener/publicar) tiene >=1 test de
    integracion HTTP (`WebApplicationFactory` + gateway falso).
  - (i) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye los 3 procs
    CHIP en los literales prohibidos; excepciones documentadas, no omitidas.
  - (j) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14):** la lectura del lote y de la diferencia aisla por tenant
    de forma DEMOSTRABLE (filtro explicito o vista/RLS que consuma `SESSION_CONTEXT('tenant_id')` verificado contra
    `OBJECT_DEFINITION`); no basta `sp_set_session_context` si el objeto leido no lo consume.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** un periodo con saldos y un usuario CON rol de conciliacion, **cuando** arma el lote y obtiene la
   diferencia, **entonces** `Create_Chip_Report_Balance_Batch` construye el lote y `Get_Chip_Reconciliation_
   Difference` devuelve la diferencia con signo CHIP (verificable via lectura), sin que C# calcule la conciliacion.
2. **Dado** una diferencia real, **cuando** publica el ajuste con confirmacion, **entonces**
   `Post_Chip_Adjustment_Voucher` genera el comprobante de ajuste (verificable via lectura) sin que C# calcule el
   ajuste.
3. **Dado** un intento de ajuste sin diferencia (o fuera de precondiciones, RE-CONFIRMAR la regla), **entonces**
   ProblemDetails del THROW real de `Post_Chip_Adjustment_Voucher` (53940-53953, RE-CONFIRMAR cual) y NO se publica.
4. **Dado** un armado de lote invalido (RE-CONFIRMAR la regla), **entonces** ProblemDetails del THROW real de
   `Create_Chip_Report_Balance_Batch` (53900-53910) y NO se arma el lote.
5. **Dado** un ajuste que publica via `Post_Voucher` en un periodo cerrado SIN escotilla (si aplica), **entonces**
   ProblemDetails de `52204`/`52512` y NO se publica; la superficie NUNCA setea la escotilla annual_close.
6. **Dado** una operacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto).
7. **Dado** un usuario SIN rol de conciliacion (o sin autenticar), **cuando** intenta armar/obtener/publicar,
   **entonces** 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
8. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA limpio)
   -- sin mock/`Recording*`.
9. **Dado** el gateway de produccion, **entonces** lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin
   fallback ni default silencioso; el harness ejercita el MISMO camino (#11).
10. **Dado** cada endpoint (armar/obtener/publicar), **entonces** tiene >=1 test de integracion HTTP (#12).
11. **Dado** el test de aislamiento del frontend, **entonces** incluye los 3 procs CHIP; excepciones documentadas
    (#13).
12. **Dado** la lectura del lote/diferencia entre dos tenants A y B, **cuando** A consulta datos de B por IDs,
    **entonces** el gateway NO devuelve datos de B (filtro tenant o vista/RLS verificada) -- negativo cross-tenant
    explicito (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de armar/obtener/publicar; traduccion THROW->ProblemDetails; enforcement de que la conciliacion/
  signo/ajuste NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA setea la escotilla
  annual_close.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los 3 procs CHIP, #13); Mcp sin SQL; cero
  DataTable; test de autorizacion (endpoints con `[Authorize]`/policy); **test mecanico: ningun archivo de la unidad
  setea `SESSION_CONTEXT('accounting_annual_close')`** (integrity invariant).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1 (armar+
  diferencia), criterio 2 (ajuste), un caso por THROW ALCANZABLE (53900-910, 53920-923, 53940-953, tenant)
  RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio 7 (401/403). Seed limpio (tenant ACCTVERIFY, fuente TST,
  vigencias 2024/2025) dentro de la transaccion con ROLLBACK.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad) + CI + F-NOVA-01 (cada THROW verificado; comportamiento del
  `Post_Chip_Adjustment_Voucher` confirmado) + guard de procedencia + aislamiento de tenant + autorizacion real +
  DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Reimplementar la conciliacion / el signo CHIP / el ajuste en C# | Divergencia con la BD; ajuste incorrecto | Restricciones 6a/6c + criterios 1/2; adversarial y checker formal verifican el diff |
| Publicar el ajuste sin obtener la diferencia (saltarse la conciliacion) | Ajuste sin sustento; correccion arbitraria | Restriccion 6c + criterios 1/2/3 |
| Asumir el mapeo THROW o si `Post_Chip_Adjustment_Voucher` publica via Post_Voucher por analogia | Criterio apunta al THROW incorrecto; THROW no alcanzable | F-NOVA-01: RE-CONFIRMAR 53900-53953 + el comportamiento del proc contra OBJECT_DEFINITION |
| Forzar el ajuste en periodo cerrado seteando la escotilla annual_close | Rompe el fix de integridad de periodo cerrado | Restriccion 6b + criterio 5 + test de arquitectura mecanico de integridad; la escotilla es exclusiva de S6B |
| Autorizacion decorativa sin verificacion real de rol | Ajuste CHIP sin rol (gap #5/#8) | Restriccion 6e + criterio 7 + test de arquitectura mecanico |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6f): clase SQL real via accounting_sandbox_verifier, sin credenciales |
| Fuga de tenant en la lectura del lote/diferencia | Confidencialidad (hallazgo #14) | Restriccion 6j + criterio 12 (negativo cross-tenant) |

## 10. Prioridad definida
**GOAL conciliacion CHIP** (contingencia: reconcilia y ajusta saldos para el reporte CHIP). Pertenencia Q4: segun
sorteo del sello si mide (criticidad de INTEGRIDAD alta). Severidad: mutador que publica un comprobante de ajuste;
si publica via `Post_Voucher` respeta el control de periodo. Dependencias: procs CHIP (existen, base congelada),
patron congelado NOVA-SPEC-T-001, diseno de autorizacion real (s.6f). **LINEA ROJA: esta unidad NO SE CONSTRUYE
antes del 30-jul** (pool Q4/gobernado); esta SPEC es DISENO/PREP unicamente. Relacion: alimenta el informe
trimestral CGN/CHIP (S6A) con saldos conciliados.
