# SPEC-CONT-S2 - Comprobante manual y correcciones (Slice 2, mutador)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR: captura de comprobante manual (borrador -> publicacion definitiva) y su
> correccion (reverso). Los procs/triggers YA EXISTEN (hardening del DBA, base congelada
> ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI). PREP de Sprint 1 (DIRECTIVA
> Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 2 + seccion D
> (F-NOVA-01, 2026-07-10) + fix de integridad de periodo cerrado (design-source, verificado estatico) + patron
> gobernado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S2 - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide. Criticidad de INTEGRIDAD **ALTA** (captura +
  publicacion definitiva + reverso, con control de periodo cerrado y la escotilla annual_close). Si mide como par,
  aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Post_Voucher`, `Post_Voucher_Draft`, `Reverse_Voucher`,
  `Get_Next_Accounting_Source_Number` + los 12 triggers de voucher EXISTEN, desplegados+verificados en las 3 BD.
  `GRANT EXECUTE` sobre los 4 procs concedido al rol **`accounting_sandbox_verifier`** (estan entre las 33
  rutinas); **VIEW DEFINITION** concedido para leer el `OBJECT_DEFINITION` de los triggers (least-privilege, sin
  SELECT directo a `Accounting.Voucher`). Set REAL de THROW capturado (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD):**
  - `Accounting.Post_Voucher` **52230-52247, 52252** (el `52252` bloquea la captura MANUAL con tipos proc-only
    como `annual_close`).
  - `Accounting.Post_Voucher_Draft` **52250-52251**.
  - `Accounting.trg_voucher__validate_insert` **52200-52204** (el `52204` exige la escotilla
    `SESSION_CONTEXT('accounting_annual_close')=1` para omitir P03/P04 en `annual_close`).
  - `Accounting.trg_voucher__date_controls` **52510-52514** (el `52512` usa la MISMA escotilla para el unico
    bypass permitido de `annual_close`).
  - `Accounting.Reverse_Voucher` **52600-52607** (ausentes reales 52608-52610 del primer pase).
  - Terceros obligatorios (schema/021) **52300-52321**; numeracion (`Get_Next_Accounting_Source_Number`,
    schema/010) **52100-52102**.
  - El maker RE-CONFIRMA cada set y el codigo EXACTO de la guarda de periodo del `Post_Voucher` (propuesto ~52233)
    contra `OBJECT_DEFINITION` del proc DESPLEGADO antes de fijar criterios; no asumir por analogia.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** la captura/publicacion/reverso exigen rol de captura
  contable via `[Authorize]`/`RequireAuthorization` real; sin sesion/rol valido -> 401/403 antes de tocar el
  proc/gateway (patron P4-006 s.6h).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs+triggers verificados por el DBA (base congelada). El maker RE-VERIFICA contra la BD
  desplegada el set exacto de THROW y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario captura un comprobante contable MANUAL como borrador (`Voucher_Draft` -> `Post_Voucher_Draft`),
lo PUBLICA definitivo (`Post_Voucher`, con numeracion por fuente/vigencia via `Get_Next_Accounting_Source_Number`)
y, si necesita corregir, lo REVIERTE (`Reverse_Voucher`: el definitivo es inmutable -> se genera un comprobante de
reverso relacionado). Toda validacion (partida doble, terceros obligatorios, control de periodo, escotilla de
cierre) vive en los procs/triggers; C# NO reimplementa la validacion contable ni la numeracion.
- Fuente: WS1 Slice 2 + seccion D; NOVA-PRES patron mutador (P4-006).
- Calidad: falsable. Bien: "publicar un comprobante manual cuyo `source_type` es `annual_close` (tipo proc-only)
  devuelve ProblemDetails del THROW `52252` y NO lo publica; y publicar en un periodo cerrado (P03/P04) sin la
  escotilla devuelve `52204`/`52512` -- la escotilla `SESSION_CONTEXT('accounting_annual_close')` NO es exponible
  desde esta superficie".

## 2. Usuario objetivo definido
Rol **Captura contable** (autenticado + verificado, s.6f). Captura/publica/reversa comprobantes manuales con
usuario real (del contexto de auth), motivo y correlation-id/task_id para auditoria. No opera cierres (S3/S6B) ni
tipos proc-only.

## 3. Alcance definido
- **Borrador:** crear/editar `Voucher_Draft`; postear el borrador (`Post_Voucher_Draft`, 52250-52251), que dispara
  los triggers de validacion (partida doble, terceros, fechas) sin publicar definitivo.
- **Publicacion definitiva:** `Post_Voucher` (52230-52247, 52252) con numeracion por fuente/vigencia
  (`Get_Next_Accounting_Source_Number`, 52100-52102). El comprobante definitivo es INMUTABLE.
- **Correccion:** `Reverse_Voucher` (52600-52607) genera un comprobante de reverso relacionado (NUNCA edita el
  original; la "Copia de Comprobantes" legacy NO se reproduce -- correccion = nuevo comprobante).
- **Terceros obligatorios:** cada linea con tercero cuando la cuenta lo exige (52300-52321); excepciones sin
  tercero resoluble NO entran como nulos (regla del WS1 A: mapa `Legacy.Maco009_Entity_Map`).
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** la captura manual NUNCA fija un `source_type` proc-only
  (`annual_close`) -> `52252`; y NUNCA expone/activa la escotilla `SESSION_CONTEXT('accounting_annual_close')`
  (interna del cierre anual, S6B). Publicar fuera de periodo abierto sin escotilla -> `52204`/`52512`.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **Cierre/apertura de periodo** (S3), **cierre anual `annual_close`** (S6B), **saldos iniciales** (S4), **CHIP**
  (S5/S6A), **reportes RO** (S1), **causacion de ingresos** (S6C): FUERA.
- **La escotilla de periodo cerrado** (`SESSION_CONTEXT('accounting_annual_close')`): NO se expone, parametriza ni
  activa desde esta superficie; es interna de `Close_Annual_Accounting_Period` (S6B).
- **Reproducir `Copia de Comprobantes` / `Grabar Temporales` / `Mayorizar` / `Traslado de Cuentas` como formularios
  legacy:** retirados en WS1 (correccion = nuevo comprobante; automaticos contabilizan definitivo; reportes
  mayorizan a fecha de corte). El traslado de cuentas, si aplica, es un comprobante via `Post_Voucher`.
- **Construir/modificar los procs/triggers:** ya existen; esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Post_Voucher`, `Post_Voucher_Draft`, `Reverse_Voucher`,
  `Get_Next_Accounting_Source_Number` + 12 triggers de voucher (`trg_voucher__validate_insert`,
  `trg_voucher__date_controls`, ...). Firma EXACTA y nombres de columna del result-set: extraidos de
  `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no asumidos.
- **THROW:** el set REAL de la seccion D (DoR). El maker mapea cada codigo a su regla (partida descuadrada, tercero
  faltante, periodo cerrado, tipo proc-only bloqueado 52252, numeracion, tenant, no-existe/ya-revertido).
- **API:** `POST /api/accounting/vouchers/drafts` (crear borrador) · `POST /api/accounting/vouchers/drafts/{id}/post`
  (publicar definitivo) · `POST /api/accounting/vouchers/{id}/reverse` (reversar). ProblemDetails por THROW; todos
  bajo `[Authorize]` con rol de captura contable (s.6f).
- **UI (apps/nova-web):** captura del comprobante (lineas, cuenta, tercero, valores D/C), previsualizacion de
  cuadre y de periodo, publicacion y reverso; muestra ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/Vouchers/` (mapea, traduce THROW; NO reimplementa cuadre/
  numeracion/reverso/control de periodo).
- **Referencias:** WS1 Slice 2 + seccion D; fix de integridad de periodo cerrado (design-source); patron congelado
  NOVA-SPEC-T-001 (P4-006).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion SOLO por los procs (`Post_Voucher_Draft`/`Post_Voucher`/`Reverse_Voucher`); jamas DML directo
    sobre `Accounting.Voucher`/`Voucher_Line` ni recalculo de cuadre/numeracion en C#.
  - (b) **INVARIANTE DE INTEGRIDAD (escotilla de periodo cerrado, NO RELAJAR):** la superficie NUNCA envia un
    `source_type` proc-only (`annual_close`) en la captura manual (el proc lo bloquea con `52252`, pero la
    superficie tampoco lo ofrece); NUNCA setea `SESSION_CONTEXT('accounting_annual_close')` desde la API/gateway.
    El control de periodo cerrado (P03/P04) lo enforzan los triggers `52204`/`52512`; la superficie NO lo esquiva.
  - (c) **INMUTABILIDAD del definitivo:** una vez publicado, el comprobante no se edita; corregir = `Reverse_Voucher`
    (comprobante de reverso relacionado) + nuevo comprobante. La app no ofrece "editar publicado".
  - (d) **Terceros obligatorios:** cuando la cuenta lo exige, la linea lleva tercero resoluble; sin tercero
    resoluble no se envia como nulo (52300-52321; mapa `Legacy.Maco009_Entity_Map` para legacy).
  - (e) DTOs 1:1; THROW->ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario
    real (del contexto de auth) en cada operacion.
  - (f) **AUTORIZACION REAL:** cada endpoint mutador exige `[Authorize]`/`RequireAuthorization` con rol de captura
    contable real; sin sesion/rol valido -> 401/403 antes de tocar el gateway/proc. Test de arquitectura mecanico
    (falla si se remueve el atributo/policy).
  - (g) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (h) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida confirmado
    contra `OBJECT_DEFINITION`; sin fallback ni default silencioso; el harness ejercita el MISMO camino.
  - (i) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (crear/publicar/reversar) tiene >=1 test de
    integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica ruta->endpoint->comando->gateway.
  - (j) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye
    `Post_Voucher`/`Post_Voucher_Draft`/`Reverse_Voucher` en los literales prohibidos; excepciones (texto
    descriptivo de auditoria en UI) documentadas, no omitidas.
  - (k) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14):** las lecturas de previsualizacion (estado del
    comprobante, cuadre, periodo) aislan por tenant de forma DEMOSTRABLE (filtro explicito o vista/RLS que consuma
    `SESSION_CONTEXT('tenant_id')` verificado contra `OBJECT_DEFINITION`); no basta `sp_set_session_context` si el
    objeto leido no lo consume.
  - (l) **HARDENING DECLARADO (follow-up, no bypass; backlog PREP s.4):** cuando se construya, la captura manual
    FIJA `source_module_code='accounting'` para que el `52252` no sea esquivable a nivel BD (hoy `Post_Voucher_
    Draft` lo lee del draft). Es hardening DECLARADO en el contrato, NO un bypass; el fix de periodo cerrado NO
    depende de esto (la escotilla lo cubre independientemente).

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** un borrador cuadrado con terceros validos y un usuario CON rol, **cuando** publica, **entonces** el
   proc numera y publica el definitivo (verificable via lectura), sin que C# calcule cuadre ni numeracion.
2. **Dado** un comprobante manual con `source_type = 'annual_close'` (tipo proc-only), **cuando** se intenta
   publicar, **entonces** ProblemDetails del THROW `52252` y NO se publica (la superficie tampoco ofrece ese tipo).
3. **Dado** una publicacion en un periodo CERRADO (P03/P04) SIN la escotilla annual_close, **entonces**
   ProblemDetails de `52204` (validate_insert) o `52512` (date_controls) y NO se publica; la superficie NUNCA
   setea `SESSION_CONTEXT('accounting_annual_close')`.
4. **Dado** un comprobante descuadrado (partida doble no balancea), **entonces** ProblemDetails del THROW real de
   cuadre (dentro de 52200-52247, RE-CONFIRMAR cual) y NO se publica.
5. **Dado** una linea con cuenta que exige tercero SIN tercero resoluble, **entonces** ProblemDetails del THROW de
   tercero obligatorio (52300-52321, RE-CONFIRMAR) y NO se publica; sin tercero enviado como nulo.
6. **Dado** un comprobante definitivo publicado, **cuando** se corrige, **entonces** se hace via `Reverse_Voucher`
   (comprobante de reverso relacionado, 52600-52607); el original queda INMUTABLE (no hay endpoint de edicion).
7. **Dado** una operacion sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto).
8. **Dado** un usuario SIN rol de captura (o sin autenticar), **cuando** intenta capturar/publicar/reversar,
   **entonces** 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
9. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA
   limpio) -- sin mock/`Recording*`.
10. **Dado** el gateway de produccion, **entonces** lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin
    fallback ni default silencioso; el harness ejercita el MISMO camino (#11).
11. **Dado** cada endpoint (crear/publicar/reversar), **entonces** tiene >=1 test de integracion HTTP (#12).
12. **Dado** el test de aislamiento del frontend, **entonces** incluye los 3 procs mutadores; excepciones
    documentadas (#13).
13. **Dado** la previsualizacion de estado/cuadre entre dos tenants A y B, **cuando** A consulta datos de B por
    IDs, **entonces** el gateway NO devuelve datos de B (filtro tenant o vista/RLS verificada) -- negativo
    cross-tenant explicito (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de captura/publicacion/reverso; traduccion THROW->ProblemDetails; enforcement de que cuadre/
  numeracion/reverso/periodo NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA emite
  `annual_close` ni setea la escotilla.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los 3 procs mutadores, #13); Mcp sin SQL; cero
  DataTable; test de autorizacion (endpoints con `[Authorize]`/policy); **test mecanico: ningun archivo de la
  unidad setea `SESSION_CONTEXT('accounting_annual_close')` ni envia `source_type='annual_close'`** (integrity
  invariant, falla si aparece).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1
  (happy, publica+numera), un caso por THROW ALCANZABLE (52252 tipo proc-only, 52204/52512 periodo cerrado, cuadre,
  tercero, tenant) RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio 6 (reverso), criterio 8 (401/403).
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad) + CI + F-NOVA-01 (cada THROW verificado contra el proc
  desplegado, con el codigo EXACTO de la guarda de periodo del Post_Voucher confirmado) + guard de procedencia +
  aislamiento de tenant + autorizacion real + DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Exponer/activar la escotilla `SESSION_CONTEXT('accounting_annual_close')` desde la superficie o permitir `annual_close` en captura manual | Se rompe el fix de integridad de periodo cerrado; comprobantes fuera de periodo | Restriccion 6b + criterios 2/3 + test de arquitectura mecanico de integridad (s.8); el proc bloquea con 52252/52204/52512 pero la superficie tampoco lo ofrece |
| Reimplementar el cuadre/numeracion/reverso/control de periodo en C# | Divergencia con la BD | Restricciones 6a/6c + criterios 1/4/6; adversarial y checker formal verifican el diff |
| Asumir el set de THROW o el codigo EXACTO de la guarda de periodo del Post_Voucher (propuesto ~52233) sin re-confirmar | Criterio apunta al THROW incorrecto; THROW no alcanzable | F-NOVA-01: RE-CONFIRMAR 52230-52247/52252 + el codigo exacto de la guarda contra OBJECT_DEFINITION antes de fijar criterios |
| Ofrecer "editar" un comprobante definitivo | Rompe la inmutabilidad; correccion mal modelada | Restriccion 6c + criterio 6 (correccion solo via Reverse_Voucher) |
| Tercero enviado como nulo cuando no es resoluble | Viola la regla de linea con tercero obligatorio (WS1 A) | Restriccion 6d + criterio 5 + mapa Legacy.Maco009_Entity_Map |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6g): clase SQL real via accounting_sandbox_verifier, sin credenciales |
| Autorizacion decorativa sin verificacion real de rol | Captura/publicacion/reverso sin rol (gap #5/#8) | Restriccion 6f + criterio 8 + test de arquitectura mecanico |
| `52252` esquivable a nivel BD porque `source_module_code` no se fija en la captura manual | El bloqueo de tipos proc-only en captura manual se puede burlar a nivel BD | Restriccion 6l (hardening DECLARADO: fijar `source_module_code='accounting'`); el fix de periodo cerrado NO depende de esto (escotilla) |
| Fuga de tenant en la previsualizacion de estado/cuadre | Confidencialidad (hallazgo #14) | Restriccion 6k + criterio 13 (negativo cross-tenant) |

## 10. Prioridad definida
**GOAL captura contable** (nucleo transaccional del modulo). Pertenencia Q4: segun sorteo del sello si mide
(criticidad de INTEGRIDAD alta). Severidad: mutador con publicacion definitiva inmutable + control de periodo
cerrado + la escotilla annual_close (la superficie la PRESERVA, no la relaja). Dependencias: procs/triggers de
voucher (existen, base congelada), patron congelado NOVA-SPEC-T-001, diseno de autorizacion real (s.6f), fix de
integridad de periodo cerrado (design-source). **LINEA ROJA: esta unidad NO SE CONSTRUYE antes del 30-jul** (pool
Q4/gobernado); esta SPEC es DISENO/PREP unicamente. Desbloquea: la captura contable manual + correcciones sobre la
que se apoyan cierre (S3), CHIP (S5) y cierre anual (S6B).
