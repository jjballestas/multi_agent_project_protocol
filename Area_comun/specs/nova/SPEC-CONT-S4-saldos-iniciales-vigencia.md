# SPEC-CONT-S4 - Saldos iniciales de vigencia (Slice 4, mutador)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR: entrada de datos iniciales de una vigencia -- crea/valida/importa/aprueba el
> borrador de saldos iniciales (`*_Opening_Balance_Draft`) y convierte cuentas auxiliares a mayor
> (`Convert_Auxiliary_To_Major`). Los procs YA EXISTEN (hardening del DBA, base congelada
> ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI). PREP de Sprint 1 (DIRECTIVA
> Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 4 + seccion D
> (F-NOVA-01, 2026-07-10) + patron gobernado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S4 - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide. Criticidad de INTEGRIDAD **ALTA** (los saldos
  iniciales fijan el punto de partida de la vigencia; un error se propaga a todo el ejercicio). Si mide como par,
  aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Create_Opening_Balance_Draft`, `Validate_Opening_Balance_Draft`,
  `Import_Opening_Balance_Draft_From_File_Stage`, `Approve_Opening_Balance_Draft`, `Convert_Auxiliary_To_Major`
  EXISTEN, desplegados+verificados en las 3 BD. `GRANT EXECUTE` sobre los 5 procs concedido al rol
  **`accounting_sandbox_verifier`** (estan entre las 33 rutinas). Set REAL de THROW capturado (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD -- "sin divergencia"):**
  - `Accounting.Create_Opening_Balance_Draft` **52420-52421**.
  - `Accounting.Validate_Opening_Balance_Draft` **52430-52437**.
  - `Accounting.Import_Opening_Balance_Draft_From_File_Stage` **52440-52443**.
  - `Accounting.Approve_Opening_Balance_Draft` **52450-52452**.
  - `Accounting.Convert_Auxiliary_To_Major` **52308-52313**.
  - Terceros obligatorios (schema/021, `Account_Structure_Period`/niveles de analisis) **52300-52321**.
  - Mapa legacy: MacoA015f (Entrada de Datos Iniciales) -> `Create/Validate/Approve_Opening_Balance_Draft` +
    `Import_..._From_File_Stage`; MacoA010f (Titulos de Analisis) -> niveles de analisis 52300-52313.
  - El maker RE-CONFIRMA cada set, si `Approve_Opening_Balance_Draft` publica via `Post_Voucher` o escribe saldos
    directo (para saber si toca control de periodo), y los nombres exactos de columna del result-set contra
    `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de fijar criterios; no
    asumir por analogia.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** crear/validar/importar/aprobar saldos iniciales y convertir
  auxiliar a mayor exigen rol de SALDOS INICIALES (setup contable) via `[Authorize]`/`RequireAuthorization` real;
  sin sesion/rol valido -> 401/403 antes de tocar el proc/gateway (patron P4-006 s.6h). Rol distinto del de captura
  (S2) y del de cierre (S3).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs verificados por el DBA (base congelada). El maker RE-VERIFICA contra la BD desplegada el set
  exacto de THROW y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre
  capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario de setup CREA un borrador de saldos iniciales de una vigencia (`Create_Opening_Balance_Draft`,
52420-52421), lo VALIDA (`Validate_Opening_Balance_Draft`, 52430-52437), opcionalmente lo IMPORTA en lote desde un
archivo staged (`Import_Opening_Balance_Draft_From_File_Stage`, 52440-52443) y lo APRUEBA
(`Approve_Opening_Balance_Draft`, 52450-52452), que fija los saldos iniciales del ejercicio. Ademas puede CONVERTIR
cuentas auxiliares a mayor (`Convert_Auxiliary_To_Major`, 52308-52313). Toda la validacion (cuadre de saldos,
terceros obligatorios, niveles de analisis, estado del borrador) vive en los procs; C# NO reimplementa la validacion
contable ni el cuadre.
- Fuente: WS1 Slice 4 + seccion D; NOVA-PRES patron mutador (P4-006).
- Calidad: falsable. Bien: "aprobar un borrador de saldos iniciales que no cuadra (o con un tercero faltante donde la
  cuenta lo exige) devuelve ProblemDetails del THROW real (52430-52437 en validacion, o 52300-52321 de tercero) y NO
  fija los saldos; y la superficie NO reimplementa el cuadre en C#".

## 2. Usuario objetivo definido
Rol **Saldos iniciales / setup contable** (autenticado + verificado, s.6f), DISTINTO del de captura (S2) y del de
cierre (S3). Prepara los saldos iniciales de una vigencia con usuario real (del contexto de auth), motivo y
correlation-id/task_id para auditoria. No captura comprobantes ni opera cierres.

## 3. Alcance definido
- **Crear borrador:** `Create_Opening_Balance_Draft` (52420-52421) -- inicia el borrador de saldos iniciales de la
  vigencia.
- **Validar borrador:** `Validate_Opening_Balance_Draft` (52430-52437) -- comprueba cuadre, terceros, niveles de
  analisis sin aprobar; devuelve el diagnostico.
- **Importar en lote:** `Import_Opening_Balance_Draft_From_File_Stage` (52440-52443) -- carga masiva del borrador
  desde un archivo previamente staged (el staging del archivo es un paso previo; el proc consume el stage).
- **Aprobar:** `Approve_Opening_Balance_Draft` (52450-52452) -- fija los saldos iniciales del ejercicio (RE-CONFIRMAR
  si publica via `Post_Voucher` o escribe directo).
- **Convertir auxiliar a mayor:** `Convert_Auxiliary_To_Major` (52308-52313) -- agrega cuentas auxiliares a su cuenta
  mayor.
- **Terceros obligatorios:** cada saldo con tercero cuando la cuenta lo exige (52300-52321); sin tercero resoluble no
  entra como nulo.
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** esta superficie NUNCA expone, parametriza ni activa la escotilla
  `SESSION_CONTEXT('accounting_annual_close')` (interna del cierre anual, S6B, que genera los saldos iniciales de la
  siguiente vigencia por su cuenta). Los saldos iniciales manuales de S4 son distintos de los que produce el cierre
  anual.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **Captura/publicacion/reverso de comprobantes** (S2), **cierre/apertura mensual** (S3), **cierre anual
  `annual_close`** (S6B, que produce los saldos iniciales de la siguiente vigencia), **CHIP** (S5/S6A), **reportes
  RO** (S1), **causacion de ingresos** (S6C): FUERA.
- **La escotilla annual_close:** NO se expone, parametriza ni activa desde esta superficie; es interna de S6B.
- **El staging del archivo de importacion** como pipeline propio: S4 consume un stage ya cargado; el mecanismo de
  carga del archivo a la tabla stage se especifica donde corresponda (RE-CONFIRMAR el contrato del stage).
- **Reimplementar el cuadre de saldos / los niveles de analisis / la conversion auxiliar-a-mayor en C#:** los
  enforzan los procs; la superficie solo invoca y traduce.
- **Construir/modificar los procs:** ya existen; esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Create_Opening_Balance_Draft`, `Validate_Opening_Balance_Draft`,
  `Import_Opening_Balance_Draft_From_File_Stage`, `Approve_Opening_Balance_Draft` (schema/022),
  `Convert_Auxiliary_To_Major` (schema/021). Firma EXACTA, contrato de la tabla stage de importacion y nombres de
  columna del result-set: extraidos de `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc
  DESPLEGADO, no asumidos.
- **THROW:** el set REAL de la seccion D (DoR). El maker mapea cada codigo a su regla (borrador invalido, saldos que
  no cuadran, tercero faltante, nivel de analisis invalido, estado del borrador, stage invalido, tenant, conversion).
- **API:** `POST /api/accounting/opening-balances/drafts` (crear) · `POST /api/accounting/opening-balances/drafts/
  {id}/validate` · `POST /api/accounting/opening-balances/drafts/{id}/import` (desde stage) · `POST /api/accounting/
  opening-balances/drafts/{id}/approve` · `POST /api/accounting/accounts/convert-auxiliary-to-major`. ProblemDetails
  por THROW; todos bajo `[Authorize]` con rol de saldos iniciales (s.6f).
- **UI (apps/nova-web):** captura/edicion del borrador de saldos iniciales (cuenta, tercero, valores), importacion
  desde archivo, previsualizacion del diagnostico de validacion, aprobacion, y conversion auxiliar-a-mayor; muestra
  ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/OpeningBalances/` (mapea, traduce THROW; NO reimplementa cuadre/
  niveles/conversion).
- **Referencias:** WS1 Slice 4 + seccion D; patron congelado NOVA-SPEC-T-001 (P4-006).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion SOLO por los procs (`Create/Validate/Import/Approve_Opening_Balance_Draft`,
    `Convert_Auxiliary_To_Major`); jamas DML directo sobre las tablas de saldos iniciales ni recalculo de cuadre/
    niveles/conversion en C#.
  - (b) **VALIDAR ANTES DE APROBAR:** la superficie expone `Validate_Opening_Balance_Draft` como paso de
    previsualizacion; la aprobacion es una accion explicita con confirmacion. C# NO decide la validez (la decide el
    proc).
  - (c) **INVARIANTE DE INTEGRIDAD (escotilla annual_close, NO RELAJAR):** la superficie NUNCA setea
    `SESSION_CONTEXT('accounting_annual_close')`; los saldos iniciales manuales de S4 no usan la escotilla (que es
    interna de S6B).
  - (d) **IMPORTACION DESDE STAGE:** la importacion consume un archivo ya staged via el proc
    `Import_..._From_File_Stage`; la superficie no parsea ni valida el contenido contable en C# (lo hace el proc);
    RE-CONFIRMAR el contrato de la tabla stage.
  - (e) DTOs 1:1; THROW->ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario real
    (del contexto de auth) en cada operacion.
  - (f) **AUTORIZACION REAL:** cada endpoint (crear/validar/importar/aprobar/convertir) exige `[Authorize]`/
    `RequireAuthorization` con rol de saldos iniciales real; sin sesion/rol valido -> 401/403 antes de tocar el
    gateway/proc. Test de arquitectura mecanico (falla si se remueve el atributo/policy).
  - (g) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (h) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida (estado del
    borrador, diagnostico de validacion, resultado de importacion) confirmado contra `OBJECT_DEFINITION`; sin
    fallback ni default silencioso; el harness ejercita el MISMO camino.
  - (i) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (crear/validar/importar/aprobar/convertir)
    tiene >=1 test de integracion HTTP (`WebApplicationFactory` + gateway falso).
  - (j) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye los 5 procs
    (`Create/Validate/Import/Approve_Opening_Balance_Draft`, `Convert_Auxiliary_To_Major`) en los literales
    prohibidos; excepciones documentadas, no omitidas.
  - (k) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14):** la lectura del estado del borrador y del diagnostico de
    validacion aisla por tenant de forma DEMOSTRABLE (filtro explicito o vista/RLS que consuma
    `SESSION_CONTEXT('tenant_id')` verificado contra `OBJECT_DEFINITION`); no basta `sp_set_session_context` si el
    objeto leido no lo consume.
  - (l) **TERCEROS OBLIGATORIOS:** cuando la cuenta lo exige, el saldo lleva tercero resoluble; sin tercero resoluble
    no se envia como nulo (52300-52321).

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** un borrador de saldos iniciales cuadrado, con terceros validos y un usuario CON rol de saldos iniciales,
   **cuando** valida y aprueba, **entonces** `Validate_Opening_Balance_Draft` diagnostica OK y
   `Approve_Opening_Balance_Draft` fija los saldos (verificable via lectura), sin que C# calcule el cuadre.
2. **Dado** un borrador que NO cuadra (o con estado invalido, RE-CONFIRMAR la regla), **cuando** se valida/aprueba,
   **entonces** ProblemDetails del THROW real de validacion (52430-52437) o de aprobacion (52450-52452) y NO se
   fijan los saldos.
3. **Dado** un saldo con cuenta que exige tercero SIN tercero resoluble, **entonces** ProblemDetails del THROW de
   tercero obligatorio (52300-52321, RE-CONFIRMAR cual) y NO se aprueba; sin tercero enviado como nulo.
4. **Dado** un archivo staged valido, **cuando** se importa, **entonces** `Import_Opening_Balance_Draft_From_File_
   Stage` carga el borrador (verificable via lectura) sin que C# parsee/valide el contenido contable; un stage
   invalido -> ProblemDetails del THROW real (52440-52443).
5. **Dado** cuentas auxiliares de una cuenta mayor, **cuando** se convierte, **entonces** `Convert_Auxiliary_To_
   Major` agrega correctamente (verificable via lectura); un caso invalido -> ProblemDetails del THROW real
   (52308-52313, RE-CONFIRMAR cual).
6. **Dado** una operacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto).
7. **Dado** un usuario SIN rol de saldos iniciales (o sin autenticar), **cuando** intenta crear/validar/importar/
   aprobar/convertir, **entonces** 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
8. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA limpio)
   -- sin mock/`Recording*`.
9. **Dado** el gateway de produccion, **entonces** lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin
   fallback ni default silencioso; el harness ejercita el MISMO camino (#11).
10. **Dado** cada endpoint (crear/validar/importar/aprobar/convertir), **entonces** tiene >=1 test de integracion
    HTTP (#12).
11. **Dado** el test de aislamiento del frontend, **entonces** incluye los 5 procs; excepciones documentadas (#13).
12. **Dado** la lectura del estado del borrador entre dos tenants A y B, **cuando** A consulta borradores de B por
    IDs, **entonces** el gateway NO devuelve datos de B (filtro tenant o vista/RLS verificada) -- negativo
    cross-tenant explicito (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de crear/validar/importar/aprobar/convertir; traduccion THROW->ProblemDetails; enforcement de que
  el cuadre/niveles/conversion NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA setea la
  escotilla annual_close.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los 5 procs, #13); Mcp sin SQL; cero DataTable;
  test de autorizacion (endpoints con `[Authorize]`/policy); **test mecanico: ningun archivo de la unidad setea
  `SESSION_CONTEXT('accounting_annual_close')`** (integrity invariant, falla si aparece).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1 (happy,
  valida+aprueba), criterio 4 (importar desde stage), criterio 5 (convertir), un caso por THROW ALCANZABLE
  (52420-21, 52430-37, 52440-43, 52450-52, 52308-13, terceros 52300-21, tenant) RE-VERIFICADO contra
  `OBJECT_DEFINITION`, criterio 7 (401/403). El seed arma una vigencia limpia (tenant ACCTVERIFY, fuente TST,
  vigencias 2024/2025, 0 vouchers) y ejerce el borrador dentro de la transaccion con ROLLBACK.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad) + CI + F-NOVA-01 (cada THROW verificado contra el proc desplegado,
  con el comportamiento de `Approve_Opening_Balance_Draft` confirmado) + guard de procedencia + aislamiento de
  tenant + autorizacion real + DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Reimplementar el cuadre de saldos / los niveles de analisis / la conversion en C# | Divergencia con la BD; saldos iniciales incorrectos que se propagan a la vigencia | Restricciones 6a/6b + criterios 1/2/5; adversarial y checker formal verifican el diff |
| Aprobar sin validar (saltarse la previsualizacion) | Se fijan saldos que no cuadran; error de todo el ejercicio | Restriccion 6b + criterios 1/2; validar es paso explicito de la superficie |
| Parsear/validar el contenido del archivo de importacion en C# | Divergencia con la validacion del proc; carga inconsistente | Restriccion 6d + criterio 4; el proc `Import_..._From_File_Stage` valida el stage |
| Asumir el mapeo THROW o el comportamiento de `Approve_Opening_Balance_Draft` (publica via Post_Voucher?) por analogia | Criterio apunta al THROW incorrecto; THROW no alcanzable | F-NOVA-01: RE-CONFIRMAR 52420-52452 + 52308-52313 + 52300-52321 + el comportamiento del approve contra OBJECT_DEFINITION |
| Tercero enviado como nulo cuando no es resoluble | Viola la regla de saldo con tercero obligatorio | Restriccion 6l + criterio 3 |
| Setear la escotilla annual_close desde esta superficie | Confusion con los saldos iniciales que produce S6B; rompe la frontera | Restriccion 6c + test de arquitectura mecanico de integridad (s.8); la escotilla es exclusiva de S6B |
| Autorizacion decorativa sin verificacion real de rol | Setup de saldos sin rol (gap #5/#8) | Restriccion 6f + criterio 7 + test de arquitectura mecanico |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6g): clase SQL real via accounting_sandbox_verifier, sin credenciales |
| Fuga de tenant en la lectura del borrador | Confidencialidad (hallazgo #14) | Restriccion 6k + criterio 12 (negativo cross-tenant) |

## 10. Prioridad definida
**GOAL setup de vigencia** (los saldos iniciales fijan el punto de partida del ejercicio; sostienen la consistencia
de todo el periodo). Pertenencia Q4: segun sorteo del sello si mide (criticidad de INTEGRIDAD alta). Severidad:
mutador que fija el estado inicial de una vigencia completa, con importacion en lote y conversion auxiliar-a-mayor.
Dependencias: procs de saldos iniciales + `Convert_Auxiliary_To_Major` (existen, base congelada), patron congelado
NOVA-SPEC-T-001, diseno de autorizacion real (s.6f). **LINEA ROJA: esta unidad NO SE CONSTRUYE antes del 30-jul**
(pool Q4/gobernado); esta SPEC es DISENO/PREP unicamente. Relacion con S6B: el cierre anual produce los saldos
iniciales de la siguiente vigencia automaticamente; S4 es la entrada MANUAL/inicial de una vigencia. Desbloquea: el
arranque contable de una vigencia sobre la que operan captura (S2), cierre (S3) y reportes (S1).
