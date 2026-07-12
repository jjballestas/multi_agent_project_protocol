# SPEC-CONT-S3 - Cierre y apertura mensual de periodo (Slice 3, mutador)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR: valida y CIERRA un periodo contable mensual (P03/P04) y valida y ABRE un
> periodo; el cierre hace que el control de fecha de comprobante (`trg_voucher__date_controls`) rechace la captura
> en el periodo cerrado. Los procs/triggers YA EXISTEN (hardening del DBA, base congelada
> ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI). PREP de Sprint 1 (DIRECTIVA
> Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 3 + seccion D
> (F-NOVA-01, 2026-07-10) + invariante de integridad de periodo cerrado (design-source, verificado estatico) +
> patron gobernado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S3 - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide. Criticidad de INTEGRIDAD **ALTA** (el cierre de
  periodo es el mecanismo que veda la captura fuera de periodo; su superficie NUNCA relaja la escotilla). Si mide
  como par, aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Validate_Period_Close`, `Close_Accounting_Period`,
  `Validate_Period_Open`, `Open_Accounting_Period` EXISTEN, desplegados+verificados en las 3 BD.
  `trg_voucher__date_controls` (dispara via DML sobre `Accounting.Voucher`) EXISTE. `GRANT EXECUTE` sobre los 4
  procs concedido al rol **`accounting_sandbox_verifier`** (estan entre las 33 rutinas); **VIEW DEFINITION**
  concedido para leer el `OBJECT_DEFINITION` del trigger (least-privilege, sin SELECT directo a `Accounting.Voucher`).
  Set REAL de THROW capturado (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD -- "sin divergencia"):**
  - `Accounting.Validate_Period_Close` **53800-53804**.
  - `Accounting.Close_Accounting_Period` **53820-53826**.
  - `Accounting.Validate_Period_Open` **53840-53844**.
  - `Accounting.Open_Accounting_Period` **53860-53867**.
  - `Accounting.trg_voucher__date_controls` **52510-52514** (el `52512` usa la MISMA escotilla
    `SESSION_CONTEXT('accounting_annual_close')=1` para el UNICO bypass permitido; ver invariante). Controles de
    fecha de comprobante en el rango P03-P07 (schema/023, 52500-52514).
  - Mapa legacy: MacoCiemf (Cierre Mensual) -> `Validate_Period_Close`+`Close_Accounting_Period` (P03/P04);
    MacoA006f/MacoAbrcf (Abrir Periodo) -> `Validate_Period_Open`+`Open_Accounting_Period`.
  - El maker RE-CONFIRMA cada set, la semantica EXACTA de los niveles P03-P07 y los nombres exactos de columna del
    result-set contra `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de fijar
    criterios; no asumir por analogia con S2 ni por el nombre del nivel.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** validar/cerrar/abrir periodo exige rol de CIERRE contable
  via `[Authorize]`/`RequireAuthorization` real; sin sesion/rol valido -> 401/403 antes de tocar el proc/gateway
  (patron P4-006 s.6h). El rol de cierre es DISTINTO y superior al de captura (S2).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs+trigger verificados por el DBA (base congelada). El maker RE-VERIFICA contra la BD desplegada
  el set exacto de THROW y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre
  capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario de cierre VALIDA que un periodo contable mensual puede cerrarse (`Validate_Period_Close`, 53800-53804) y
lo CIERRA (`Close_Accounting_Period`, 53820-53826); y VALIDA que un periodo puede abrirse (`Validate_Period_Open`,
53840-53844) y lo ABRE (`Open_Accounting_Period`, 53860-53867). Una vez cerrado, el control de fecha de comprobante
(`trg_voucher__date_controls`, 52510-52514) RECHAZA la captura de comprobantes en ese periodo (P03-P07) -- ese es el
efecto que el cierre produce y que la captura manual (S2) ya respeta. Toda la validacion de cierre/apertura (estado
del periodo, saldos pendientes, secuencia P03-P07, escotilla annual_close) vive en los procs/triggers; C# NO
reimplementa la validacion de periodo ni el control de fecha.
- Fuente: WS1 Slice 3 + seccion D; NOVA-PRES patron mutador (P4-006).
- Calidad: falsable. Bien: "tras cerrar un periodo por esta superficie, capturar un comprobante con fecha en ese
  periodo cerrado (S2) devuelve ProblemDetails del THROW `52512` y NO lo publica; y esta superficie NUNCA setea
  `SESSION_CONTEXT('accounting_annual_close')` -- la escotilla es interna del cierre anual (S6B), no de esta unidad".

## 2. Usuario objetivo definido
Rol **Cierre contable** (autenticado + verificado, s.6f), DISTINTO y superior al de captura (S2). Valida y ejecuta
cierre/apertura de periodos mensuales con usuario real (del contexto de auth), motivo y correlation-id/task_id para
auditoria. No captura comprobantes (S2), no ejecuta el cierre anual `annual_close` (S6B) ni activa su escotilla.

## 3. Alcance definido
- **Validar cierre:** `Validate_Period_Close` (53800-53804) -- comprueba precondiciones del cierre mensual (estado
  del periodo, pendientes) sin mutar; devuelve el diagnostico.
- **Cerrar periodo:** `Close_Accounting_Period` (53820-53826) -- cierra el periodo mensual (P03/P04). Efecto: la
  captura en ese periodo queda vedada por `trg_voucher__date_controls` (52512) salvo la escotilla annual_close
  (interna de S6B).
- **Validar apertura:** `Validate_Period_Open` (53840-53844) -- comprueba precondiciones de la apertura sin mutar.
- **Abrir periodo:** `Open_Accounting_Period` (53860-53867) -- abre el periodo (reversa el estado vedado del control
  de fecha para ese periodo, dentro de la secuencia P03-P07 que el proc controla).
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** esta superficie NUNCA expone, parametriza ni activa la escotilla
  `SESSION_CONTEXT('accounting_annual_close')` (interna del cierre anual, S6B); el `52512` es el UNICO bypass y lo
  concede SOLO `Close_Annual_Accounting_Period`. El cierre mensual de S3 NO usa la escotilla.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **Captura/publicacion/reverso de comprobantes** (S2), **cierre anual `annual_close`** (S6B), **saldos iniciales**
  (S4), **CHIP** (S5/S6A), **reportes RO** (S1), **causacion de ingresos** (S6C): FUERA.
- **La escotilla de periodo cerrado** (`SESSION_CONTEXT('accounting_annual_close')`): NO se expone, parametriza ni
  activa desde esta superficie; es interna de `Close_Annual_Accounting_Period` (S6B). S3 la cierra/abre a nivel
  mensual, NO la relaja.
- **Reimplementar los controles de fecha P03-P07 / la secuencia de periodos en C#:** los enforzan el trigger y los
  procs; la superficie solo invoca y traduce.
- **Construir/modificar los procs/trigger:** ya existen; esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Validate_Period_Close`, `Close_Accounting_Period`, `Validate_Period_Open`,
  `Open_Accounting_Period` (schema/025) + `trg_voucher__date_controls` (schema/023). Firma EXACTA, semantica de los
  niveles P03-P07 y nombres de columna del result-set: extraidos de `OBJECT_DEFINITION`/
  `sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no asumidos.
- **THROW:** el set REAL de la seccion D (DoR). El maker mapea cada codigo a su regla (precondicion de cierre no
  cumplida, periodo ya cerrado/abierto, secuencia P03-P07 invalida, pendientes, tenant, control de fecha 52510-52514).
- **API:** `POST /api/accounting/periods/{period}/validate-close` · `POST /api/accounting/periods/{period}/close` ·
  `POST /api/accounting/periods/{period}/validate-open` · `POST /api/accounting/periods/{period}/open`.
  ProblemDetails por THROW; todos bajo `[Authorize]` con rol de cierre contable (s.6f).
- **UI (apps/nova-web):** panel de periodos: estado por periodo, previsualizacion del diagnostico de validacion,
  accion de cierre y de apertura con confirmacion, y muestra de ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/Periods/` (mapea, traduce THROW; NO reimplementa la validacion
  de cierre/apertura ni el control de fecha).
- **Referencias:** WS1 Slice 3 + seccion D; invariante de integridad de periodo cerrado (design-source); patron
  congelado NOVA-SPEC-T-001 (P4-006).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion SOLO por los procs (`Close_Accounting_Period`/`Open_Accounting_Period`; validacion via
    `Validate_Period_Close`/`Validate_Period_Open`); jamas DML directo sobre el estado del periodo ni sobre
    `Accounting.Voucher`, ni recalculo de la secuencia de periodos en C#.
  - (b) **INVARIANTE DE INTEGRIDAD (escotilla de periodo cerrado, NO RELAJAR):** la superficie NUNCA setea
    `SESSION_CONTEXT('accounting_annual_close')` ni ofrece un modo que la active; el `52512` (bypass annual_close) es
    exclusivo de `Close_Annual_Accounting_Period` (S6B). El cierre mensual de S3 no la usa.
  - (c) **VALIDAR ANTES DE MUTAR:** la superficie expone la validacion (`Validate_Period_Close`/`_Open`) como paso
    de previsualizacion; el cierre/apertura definitivo es una accion explicita del usuario con confirmacion. C# NO
    decide la validez (la decide el proc).
  - (d) **EFECTO SOBRE LA CAPTURA:** el criterio de aceptacion demuestra el efecto real del cierre -- tras cerrar,
    un `Post_Voucher`/`Post_Voucher_Draft` (S2) con fecha en el periodo cerrado devuelve `52512`. La superficie de
    S3 NO reimplementa el control de fecha; solo produce el estado que el trigger enforza.
  - (e) DTOs 1:1; THROW->ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario real
    (del contexto de auth) en cada operacion.
  - (f) **AUTORIZACION REAL:** cada endpoint (validar/cerrar/abrir) exige `[Authorize]`/`RequireAuthorization` con
    rol de cierre contable real; sin sesion/rol valido -> 401/403 antes de tocar el gateway/proc. Test de
    arquitectura mecanico (falla si se remueve el atributo/policy). El rol de cierre es distinto del de captura (S2).
  - (g) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (h) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida (estado del
    periodo, diagnostico de validacion) confirmado contra `OBJECT_DEFINITION`; sin fallback ni default silencioso;
    el harness ejercita el MISMO camino.
  - (i) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (validar-cierre/cerrar/validar-apertura/
    abrir) tiene >=1 test de integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica
    ruta->endpoint->comando->gateway.
  - (j) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye
    `Validate_Period_Close`/`Close_Accounting_Period`/`Validate_Period_Open`/`Open_Accounting_Period` en los
    literales prohibidos; excepciones (texto descriptivo de auditoria en UI) documentadas, no omitidas.
  - (k) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14):** la lectura del estado del periodo y del diagnostico de
    validacion aisla por tenant de forma DEMOSTRABLE (filtro explicito o vista/RLS que consuma
    `SESSION_CONTEXT('tenant_id')` verificado contra `OBJECT_DEFINITION`); no basta `sp_set_session_context` si el
    objeto leido no lo consume.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** un periodo abierto y sin pendientes y un usuario CON rol de cierre, **cuando** valida y cierra,
   **entonces** `Validate_Period_Close` diagnostica OK y `Close_Accounting_Period` cierra el periodo (verificable via
   lectura de estado), sin que C# decida la validez ni mute el estado por su cuenta.
2. **Dado** un periodo recien cerrado por esta superficie, **cuando** se intenta capturar un comprobante (S2) con
   fecha en ese periodo SIN la escotilla annual_close, **entonces** ProblemDetails del THROW `52512`
   (`trg_voucher__date_controls`) y NO se publica; esta superficie NUNCA setea
   `SESSION_CONTEXT('accounting_annual_close')`.
3. **Dado** un periodo que NO cumple las precondiciones de cierre (p.ej. ya cerrado, o con pendientes, RE-CONFIRMAR
   la regla exacta), **cuando** se intenta cerrar, **entonces** ProblemDetails del THROW real de `Close_Accounting_
   Period` (dentro de 53820-53826, RE-CONFIRMAR cual) o de `Validate_Period_Close` (53800-53804) y NO se cierra.
4. **Dado** un periodo cerrado, **cuando** valida y abre con rol, **entonces** `Validate_Period_Open` (53840-53844)
   diagnostica OK y `Open_Accounting_Period` (53860-53867) lo abre (verificable via lectura), y la captura en ese
   periodo vuelve a ser posible.
5. **Dado** una apertura que viola la secuencia P03-P07 (p.ej. abrir un periodo fuera de orden, RE-CONFIRMAR la
   regla), **entonces** ProblemDetails del THROW real de `Open_Accounting_Period`/`Validate_Period_Open`
   (53840-53867, RE-CONFIRMAR cual) y NO se abre.
6. **Dado** una operacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto).
7. **Dado** un usuario SIN rol de cierre (o sin autenticar), **cuando** intenta validar/cerrar/abrir, **entonces**
   401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
8. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA limpio)
   -- sin mock/`Recording*`.
9. **Dado** el gateway de produccion, **entonces** lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin
   fallback ni default silencioso; el harness ejercita el MISMO camino (#11).
10. **Dado** cada endpoint (validar-cierre/cerrar/validar-apertura/abrir), **entonces** tiene >=1 test de
    integracion HTTP (#12).
11. **Dado** el test de aislamiento del frontend, **entonces** incluye los 4 procs de cierre/apertura; excepciones
    documentadas (#13).
12. **Dado** la lectura de estado de periodo entre dos tenants A y B, **cuando** A consulta el estado de periodos de
    B por IDs, **entonces** el gateway NO devuelve datos de B (filtro tenant o vista/RLS verificada) -- negativo
    cross-tenant explicito (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de validar/cerrar/abrir; traduccion THROW->ProblemDetails; enforcement de que la validacion de
  cierre/apertura y el control de fecha NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA
  setea la escotilla annual_close.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los 4 procs de cierre/apertura, #13); Mcp sin SQL;
  cero DataTable; test de autorizacion (endpoints con `[Authorize]`/policy); **test mecanico: ningun archivo de la
  unidad setea `SESSION_CONTEXT('accounting_annual_close')`** (integrity invariant, falla si aparece).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1 (happy,
  valida+cierra), criterio 2 (efecto real: capturar en periodo cerrado -> `52512`), criterio 4 (valida+abre), un
  caso por THROW ALCANZABLE (53800-804, 53820-826, 53840-844, 53860-867, tenant) RE-VERIFICADO contra
  `OBJECT_DEFINITION`, criterio 7 (401/403). El seed arma un periodo abierto limpio (tenant ACCTVERIFY, fuente TST,
  vigencias 2024/2025, 0 vouchers) y ejerce cierre/apertura dentro de la transaccion con ROLLBACK.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad) + CI + F-NOVA-01 (cada THROW verificado contra el proc desplegado,
  con la semantica exacta de los niveles P03-P07 confirmada) + guard de procedencia + aislamiento de tenant +
  autorizacion real + DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Setear/activar la escotilla `SESSION_CONTEXT('accounting_annual_close')` desde la superficie de cierre mensual | Se rompe el fix de integridad de periodo cerrado; el 52512 deja de vedar la captura | Restriccion 6b + criterio 2 + test de arquitectura mecanico de integridad (s.8); el `52512`/escotilla es exclusivo de S6B |
| Reimplementar la validacion de cierre/apertura o el control de fecha P03-P07 en C# | Divergencia con la BD; cierre incorrecto | Restricciones 6a/6c + criterios 1/3/4/5; adversarial y checker formal verifican el diff |
| Asumir la semantica de los niveles P03-P07 o el mapeo THROW por analogia con S2 sin re-confirmar | Criterio apunta al THROW/nivel incorrecto; THROW no alcanzable | F-NOVA-01: RE-CONFIRMAR 53800-53867 + 52510-52514 + la semantica de P03-P07 contra OBJECT_DEFINITION antes de fijar criterios |
| Cerrar/abrir sin validar (saltarse el paso de previsualizacion) | Cierre sobre precondiciones no cumplidas; error operativo | Restriccion 6c + criterios 1/3; validar es paso explicito de la superficie |
| Autorizacion decorativa sin verificacion real de rol de cierre | Cierre/apertura sin rol (gap #5/#8); un rol de captura cerraria periodos | Restriccion 6f + criterio 7 + test de arquitectura mecanico; rol de cierre distinto del de captura |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6g): clase SQL real via accounting_sandbox_verifier, sin credenciales |
| Fuga de tenant en la lectura de estado de periodo | Confidencialidad (hallazgo #14) | Restriccion 6k + criterio 12 (negativo cross-tenant) |

## 10. Prioridad definida
**GOAL control de periodo** (el cierre/apertura es el mecanismo que veda la captura fuera de periodo; sostiene la
integridad temporal del modulo). Pertenencia Q4: segun sorteo del sello si mide (criticidad de INTEGRIDAD alta).
Severidad: mutador que cambia el estado de captura de periodos completos, con la escotilla annual_close como unico
bypass (interna de S6B; S3 la PRESERVA, no la relaja). Dependencias: procs de cierre/apertura + `trg_voucher__date_
controls` (existen, base congelada), patron congelado NOVA-SPEC-T-001, diseno de autorizacion real (s.6f),
invariante de integridad de periodo cerrado (design-source). **LINEA ROJA: esta unidad NO SE CONSTRUYE antes del
30-jul** (pool Q4/gobernado); esta SPEC es DISENO/PREP unicamente. Depende de: la captura contable (S2, para el
negativo del efecto 52512). Desbloquea: el cierre anual (S6B, que se apoya en el cierre mensual + la escotilla).
