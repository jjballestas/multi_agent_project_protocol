# SPEC-CONT-S6B - Cierre anual contable (Slice 6B, mutador atomico + escotilla annual_close)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice MUTADOR ATOMICO: valida integralmente la vigencia, publica el comprobante definitivo
> `annual_close`, genera los saldos iniciales de la siguiente vigencia por cuenta-tercero, actualiza P07 y (solo
> entidad privada parametrizada) aplica reserva legal -- todo en una transaccion. El proc YA EXISTE (migrado
> schema/028, base congelada ACCOUNTING_BASE_SOLID_20260711); esta SPEC cubre SOLO la superficie C#/API(+UI)/MCP.
> PREP de Sprint 1 (DIRECTIVA Operador 2026-07-11, "escribir NO construir"): NO se implementa antes del 30-jul.
> Fuente: SDD accounting_module_requirements.html R7 (Slice 6B) + SPEC-CONT-000 (invariante escotilla) + patron
> gobernado NOVA-SPEC-T-001. R3-b (cierre mensual) es una de las 6 unidades medidas del pre-registro N=6
> (DECISION-0094) y depende de esta invariante; S6B en si NO esta en la muestra medida (queda como diseno del kit).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S6B - task_id (instancia): asignado al registrar la tarea de superficie (Sprint 1, post-30-jul;
  NO `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada; repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio: SPEC + diff + BD readonly, NO la conversacion del
  maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: N/A a la muestra medida N=6 (esta unidad NO se mide; R3-b si). Criticidad de
  INTEGRIDAD **ALTA** (cierre definitivo del ejercicio, saldos de apertura de la siguiente vigencia al centavo,
  reserva legal, unica excepcion controlada al bloqueo de periodo). Si alguna vez midiera, aislamiento CRITICO.
- **base congelada de referencia:** sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (ver SPEC-CONT-000). Al abrir el build se
  ancla en el ledger de la instancia (dual cross-atestacion, DECISION-0088).
- **precondicion / preflight (F-NOVA-01):** `Accounting.Close_Annual_Accounting_Period` y
  `Accounting.Accounting_Annual_Close_Audit` EXISTEN (schema/028, base congelada), desplegados+verificados en las 3
  BD (DbsFinanciero, DbsFinanciero_SANDBOX, SNJDC). `GRANT EXECUTE` sobre `Close_Annual_Accounting_Period` concedido
  al rol **`accounting_sandbox_verifier`** (esta entre las rutinas del verifier; kit index S6B(1)). Set REAL de THROW
  capturado (rango del kit; RE-CONFIRMAR desglose contra el proc DESPLEGADO).
- **F-NOVA-01 (set REAL, kit index/WS1; el maker RE-CONFIRMA contra `OBJECT_DEFINITION` del proc DESPLEGADO):**
  - `Accounting.Close_Annual_Accounting_Period` **54460-54487**, de los cuales **54480-54487 = reserva legal privada
    opcional**. El resto (54460-54479) = prevalidacion + publicacion del comprobante + saldos iniciales + P07.
  - Guardas del bloqueo de periodo que esta unidad DECLARA pero NO relaja: `52204` (`trg_voucher__validate_insert`),
    `52512` (`trg_voucher__date_controls`), guarda dentro de `Post_Voucher` (propuesta ~`52233`, RE-CONFIRMAR), y
    `52252` (bloquea captura MANUAL de tipos proc-only como `annual_close`).
  - Objetos consumidos (MIGRADO): `Accounting.Post_Voucher`, `Accounting.Voucher`, `Accounting.Voucher_Line`,
    `Accounting.Voucher_Relation`, `Accounting.Account_Opening_Balance`, `Accounting.fn_Account_Balance_For_Period`,
    `Accounting.Account_Structure_Period` (schema/021), `Accounting.Accounting_Process_Control` proceso **P07**.
  - Tipo de comprobante (source_type) **`annual_close`** -- activo en las 3 BD; proc-only (no capturable a mano).
  - Escotilla interna de sesion `SESSION_CONTEXT('accounting_annual_close')`: la activa/resetea SOLO
    `Close_Annual_Accounting_Period` (set antes de `Post_Voucher`, reset despues y en CATCH). Es la UNICA excepcion
    controlada al bloqueo P03/P04 para fechar el `annual_close` dentro de meses ya cerrados.
  - Equivalencia legacy: `MacoCieaf`/`MacoCieaf1`.
  - El maker RE-CONFIRMA cada set de THROW, la semantica de P07, las reglas de cierre (que clases/cuentas de
    resultado se saldan y como se traslada el resultado), la reconciliacion de saldos iniciales por cuenta-tercero,
    los parametros de reserva y los nombres exactos de columna del result-set contra `OBJECT_DEFINITION`/
    `sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de fijar criterios; no asumir por analogia.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env (rol
  `accounting_sandbox_verifier`, NA limpio sin credenciales); NINGUN mock/`Recording*` la sustituye (TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** ejecutar el cierre anual exige un rol de CIERRE ANUAL via
  `[Authorize]`/`RequireAuthorization` real, distinto y de privilegio >= al rol de cierre mensual (S3); sin sesion/rol
  valido -> 401/403 antes de tocar el proc/gateway (patron P4-006 s.6h). El nombre exacto del rol lo fija el maker
  (el SDD no lo nombra; RE-CONFIRMAR / decision de diseno del kit, no supuesto).
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs verificados por el DBA (base congelada, schema/028). El maker RE-VERIFICA contra la BD
  desplegada el set exacto de THROW, la semantica de P07 y los nombres exactos de columna.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre
  capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario de cierre PREVALIDA la vigencia y EJECUTA el cierre anual (`Close_Annual_Accounting_Period`, 54460-54487):
el proc valida integralmente (meses cerrados debidamente, sin borradores/descuadres/documentos-fuente-definitivos-
sin-comprobante/saldos-inconsistentes), publica via `Post_Voucher` el comprobante definitivo `annual_close`
(activando la escotilla interna solo para fechar dentro de meses cerrados), genera los saldos iniciales de la
siguiente vigencia por cuenta-tercero (igualan los saldos finales calculados de la vigencia cerrada), actualiza P07 y
-- solo en entidad privada con reserva parametrizada -- calcula la reserva legal. TODO el calculo, la atomicidad y la
escotilla viven en el proc; C# NO reimplementa el cierre, NO inserta comprobantes/saldos/P07 por su cuenta, y NO
expone ni activa la escotilla.
- Fuente: SDD R7 (Slice 6B); NOVA-PRES patron mutador (P4-006); SPEC-CONT-000 (invariante escotilla).
- Calidad: falsable. Bien: "un segundo cierre de la misma vigencia devuelve ProblemDetails del THROW real
  (54460-54487) y NO duplica comprobante ni saldos; los saldos iniciales de la siguiente vigencia igualan al centavo
  los finales por cuenta-tercero (los da el proc, C# no calcula); y ningun archivo de la unidad setea
  `SESSION_CONTEXT('accounting_annual_close')`".

## 2. Usuario objetivo definido
Rol **Cierre anual contable** (autenticado + verificado, s.6f; privilegio >= cierre mensual S3). Prevalida y ejecuta
el cierre anual con usuario real (del contexto de auth), motivo y correlation-id/task_id para auditoria. No captura
comprobantes (S2), no cierra el mes (S3), no importa/aprueba saldos iniciales a mano (S4). NO existe un P13/periodo
anual: el control anual es P07 + el comprobante `annual_close`.

## 3. Alcance definido
- **Prevalidacion:** superficie que dispara la validacion integral del proc (meses abiertos indebidamente,
  borradores/descuadres, documentos fuente definitivos sin comprobante, saldos iniciales inconsistentes, vigencia
  destino inexistente). El resultado es un reporte de bloqueos legible (ProblemDetails por THROW), NO una decision
  en C#.
- **Ejecutar cierre anual:** `Close_Annual_Accounting_Period` (54460-54487) -- atomico: comprobante `annual_close`
  via `Post_Voucher` + saldos iniciales de la siguiente vigencia por cuenta-tercero + P07 + (privado) reserva legal;
  todo confirma o revierte junto.
- **Auditoria:** `Accounting_Annual_Close_Audit` -- lectura del rastro del cierre (quien/cuando/resultado), expuesta
  de solo-lectura.
- **INVARIANTE DE INTEGRIDAD (ver SPEC-CONT-000):** esta superficie es la UNICA que consume el proc que activa la
  escotilla `SESSION_CONTEXT('accounting_annual_close')`, pero NUNCA la setea desde C#/API/UI: la activa/resetea SOLO
  el proc, internamente. C# jamas la expone ni la parametriza.
- **Modo publico vs privado:** publico -> resultado trasladado SIN reserva legal; privado con reserva parametrizada
  (cuentas + porcentaje aprobados) -> reserva sobre utilidad positiva.
- Tenant/auditoria: `SESSION_CONTEXT('tenant_id')` obligatorio; usuario real + correlation-id/task_id por operacion.

## 4. Fuera de alcance definido
- **Cierre/apertura MENSUAL** (S3), **reportes RO** (S1), **captura** (S2), **saldos iniciales** manuales/CSV (S4),
  **CHIP contingencia** (S5), **informe trimestral CGN/CHIP** (S6A), **causacion de ingresos/CxC** (S6C): FUERA.
- **Cierre PRESUPUESTAL, reservas presupuestales, CxP, acarreo de Presupuesto:** FUERA (Presupuesto no contabiliza).
- **Reimplementar en C#:** las reglas de cierre, el traslado del resultado, la reconciliacion de saldos por
  cuenta-tercero, el calculo de reserva, el avance de P07 o la escotilla -- los enforza el proc; la superficie solo
  invoca, traduce THROW y presenta.
- **Insertar saldos de apertura manualmente para simular el cierre** o **INSERT directo** de comprobante/saldos/P07
  desde API: PROHIBIDO (solo por el proc).
- **Construir/modificar el proc:** ya existe (schema/028); esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):** `Close_Annual_Accounting_Period`, `Accounting_Annual_Close_Audit` (schema/028).
  Firma EXACTA, reglas de cierre, reconciliacion de saldos iniciales por cuenta-tercero, parametros de reserva,
  semantica de P07 y nombres de columna del result-set: extraidos de `OBJECT_DEFINITION`/
  `sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no asumidos.
- **THROW:** el set REAL 54460-54487 (54480-487 = reserva privada). El maker mapea cada codigo a su regla (cierre
  duplicado, vigencia destino inexistente, comprobantes pendientes/descuadre, documentos fuente definitivos sin
  comprobante, saldos inconsistentes, meses abiertos indebidamente, reserva sin cuentas/porcentaje, reserva en
  entidad publica).
- **API:** `POST /api/accounting/annual-close/prevalidate` (prevalidacion, solo reporte) |
  `POST /api/accounting/annual-close` (ejecutar; body: vigencia + confirmacion + modo/params de reserva si privado) |
  `GET /api/accounting/annual-close/{vigencia}/audit` (auditoria RO). ProblemDetails por THROW; todos bajo
  `[Authorize]` con rol de cierre anual (s.6f).
- **UI (apps/nova-web):** proceso de cierre anual: prevalidar (mostrar bloqueos), confirmar la ejecucion con doble
  confirmacion explicita (es definitivo), mostrar el comprobante `annual_close` publicado + la confirmacion de saldos
  iniciales de la siguiente vigencia + P07; muestra ProblemDetails.
- **Capa Application:** `NOVA.Application/Accounting/AnnualClose/` (mapea, traduce THROW; NO reimplementa cierre/
  reserva/saldos/P07/escotilla).
- **Referencias:** SDD R7; patron congelado NOVA-SPEC-T-001 (P4-006); SPEC-CONT-000 (invariante escotilla);
  SPEC-CONT-S3 (cierre mensual, que NO puede activar la escotilla).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) Mutacion/generacion SOLO por el proc; jamas DML directo ni recalculo de reglas de cierre / traslado del
    resultado / reserva / saldos iniciales / P07 en C#.
  - (b) **ATOMICIDAD DEL CIERRE (NO PARTIR):** prevalidacion + comprobante `annual_close` + saldos iniciales de la
    siguiente vigencia + P07 (+ reserva si privado) confirman o revierten JUNTOS. C# no ejecuta pasos parciales ni
    "reintenta la mitad".
  - (c) **RECONCILIACION AL CENTAVO SIN RECALCULO:** los saldos iniciales de la siguiente vigencia igualan los saldos
    finales calculados de la vigencia cerrada POR CUENTA-TERCERO; C# NO los calcula ni los redondea, solo lee/presenta
    lo que el proc materializo (preservando tercero por linea/saldo).
  - (d) **INVARIANTE DE INTEGRIDAD (escotilla annual_close, NO RELAJAR):** la superficie NUNCA setea
    `SESSION_CONTEXT('accounting_annual_close')`; la activa SOLO el proc, internamente. Es la unica excepcion al
    bloqueo P03/P04 y no se expone a API/UI/MCP.
  - (e) **P07 LO FIJA EL PROC:** el avance de P07 (que bloquea aperturas mensuales dentro de la vigencia cubierta) lo
    hace el proc de cierre; C# no decide ni escribe P07.
  - (f) **AUTORIZACION REAL:** el endpoint de ejecucion (y el de prevalidacion) exige `[Authorize]`/
    `RequireAuthorization` con rol de cierre anual real (>= S3); sin sesion/rol valido -> 401/403 antes de tocar el
    gateway/proc. Test de arquitectura mecanico (falla si se remueve el atributo/policy).
  - (g) **RESERVA LEGAL SOLO PRIVADA Y PARAMETRIZADA:** en entidad publica NO se aplica reserva; en privada se aplica
    solo con cuentas (puente/utilidad/reserva/capital) + porcentaje aprobados, sobre utilidad positiva, limitada por
    el 50% del capital menos la reserva existente. C# NO calcula la reserva; solo pasa los parametros aprobados y
    presenta el resultado. La activacion indebida en entidad publica es un negativo.
  - (h) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real (rol `accounting_sandbox_verifier`,
    NA limpio); jamas mock/`Recording*`.
  - (i) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** nombre EXACTO de cada columna leida (resultado del
    cierre, comprobante, saldos iniciales, estado de P07, auditoria) confirmado contra `OBJECT_DEFINITION`; sin
    fallback ni default silencioso; el harness ejercita el MISMO camino.
  - (j) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint (prevalidar/ejecutar/auditar) tiene >=1 test
    de integracion HTTP (`WebApplicationFactory` + gateway falso).
  - (k) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test de aislamiento del frontend incluye
    `Close_Annual_Accounting_Period` y `Accounting_Annual_Close_Audit` en los literales prohibidos; excepciones
    documentadas.
  - (l) **AISLAMIENTO DE TENANT (hallazgo #14):** la lectura del resultado/auditoria/saldos aisla por tenant de forma
    DEMOSTRABLE (filtro explicito o vista/RLS que consuma `SESSION_CONTEXT('tenant_id')` verificado contra
    `OBJECT_DEFINITION`).

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (54460-54487) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** una vigencia con todos los meses cerrados debidamente, sin pendientes ni descuadres, una vigencia destino
   existente y un usuario CON rol de cierre anual, **cuando** ejecuta el cierre, **entonces**
   `Close_Annual_Accounting_Period` publica un comprobante `annual_close` definitivo, cuadrado y fechado en el periodo
   permitido, sin que C# calcule ni inserte nada por su cuenta.
2. **Dado** el cierre ejecutado, **cuando** se leen los saldos iniciales de la siguiente vigencia, **entonces**
   igualan al centavo los saldos finales calculados de la vigencia cerrada POR CUENTA-TERCERO (preservando tercero y
   estructura versionada al corte), materializados por el proc.
3. **Dado** el cierre ejecutado, **cuando** se lee `Accounting_Process_Control`, **entonces** P07 queda a la fecha de
   cierre y bloquea aperturas mensuales dentro de la vigencia cubierta (verificable via lectura); C# no escribio P07.
4. **Dado** una vigencia YA cerrada anualmente, **cuando** se intenta un segundo cierre, **entonces** ProblemDetails
   del THROW real (54460-54487, RE-CONFIRMAR el codigo de duplicado) y NO se duplican comprobante ni saldos
   (idempotencia o bloqueo de duplicado).
5. **Dado** una entidad PUBLICA, **cuando** cierra, **entonces** el resultado se traslada SIN reserva legal (un
   intento de forzar reserva en publica -> negativo, ProblemDetails).
6. **Dado** una entidad PRIVADA con reserva parametrizada (cuentas + porcentaje aprobados) y utilidad positiva,
   **cuando** cierra, **entonces** la reserva se calcula sobre utilidad positiva, limitada por el 50% del capital
   menos la reserva existente, el remanente queda en utilidad del ejercicio y queda evidencia en auditoria; sin
   cuentas/porcentaje aprobados -> ProblemDetails del THROW de reserva (54480-54487).
7. **Dado** la prevalidacion sobre una vigencia con meses abiertos indebidamente / borradores / descuadre /
   documentos fuente definitivos sin comprobante / saldos inconsistentes / vigencia destino inexistente, **entonces**
   ProblemDetails del THROW real correspondiente (54460-54479) y NO se ejecuta el cierre.
8. **Dado** el comprobante `annual_close`, **cuando** un usuario intenta capturarlo MANUALMENTE (S2) fijando
   `source_type = annual_close`, **entonces** THROW `52252` y NO se publica (invariante: tipo proc-only no capturable
   a mano).
9. **Dado** esta superficie, **cuando** ejecuta cualquier operacion, **entonces** NUNCA expone, parametriza ni activa
   `SESSION_CONTEXT('accounting_annual_close')` desde API/UI/MCP; test de arquitectura mecanico falla si algun archivo
   de la unidad la setea.
10. **Dado** un `annual_close` fechado en un mes cubierto por cierre mensual, **cuando** se ejecuta, **entonces** la
    UNICA forma de saltar P03/P04 es la escotilla interna del proc; cualquier `Post_Voucher` fuera de periodo sin
    escotilla es rechazado por `52204`/`52512`.
11. **Dado** un usuario SIN rol de cierre anual (o sin autenticar), **cuando** intenta prevalidar/ejecutar/auditar,
    **entonces** 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
12. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (rol `accounting_sandbox_verifier`, NA limpio)
    -- sin mock/`Recording*`; y lee cada columna por nombre EXACTO (`OBJECT_DEFINITION`), sin fallback (#11); cada
    endpoint tiene >=1 test HTTP (#12); el aislamiento del frontend incluye los procs (#13); lectura aislada por
    tenant, negativo cross-tenant (#14).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de prevalidar/ejecutar/auditar; traduccion THROW->ProblemDetails; enforcement de que el cierre/
  reserva/saldos/P07 NO se recalculan en C#; policy de autorizacion presente; la superficie NUNCA setea la escotilla.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con los procs de cierre anual, #13); Mcp sin SQL; cero
  DataTable; test de autorizacion; **test mecanico: ningun archivo de la unidad setea
  `SESSION_CONTEXT('accounting_annual_close')`** (integrity invariant, el mas critico de esta unidad).
- **Integracion vs DbsFinanciero_SANDBOX (via `accounting_sandbox_verifier`, tx con ROLLBACK):** criterio 1 (cierre
  publica el comprobante), criterio 2 (saldos iniciales al centavo por cuenta-tercero), criterio 3 (P07 avanza),
  criterio 4 (doble cierre bloqueado), criterio 5 (publica sin reserva) y 6 (privada con reserva 50%-cap), criterio 7
  (prevalidacion bloquea) y 8/10 (escotilla / 52204/52512/52252), criterio 11 (401/403). Seed limpio (entidad
  publica Y privada, vigencia N con meses cerrados + vigencia N+1 destino) dentro de la transaccion con ROLLBACK.
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests (incl. el de integridad de escotilla) + CI + F-NOVA-01 (cada THROW verificado; reglas de
  cierre, reconciliacion de saldos y semantica de P07 confirmados contra `OBJECT_DEFINITION`) + guard de procedencia
  + aislamiento de tenant + autorizacion real + DoD con evidencia real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| C# activa/expone la escotilla `annual_close` | Se abre un bypass del bloqueo de periodo desde fuera del proc; integridad rota | Restriccion 6d + criterios 9/10 + test de arquitectura mecanico (integrity invariant) |
| Reimplementar el cierre / reserva / saldos iniciales / P07 en C# | Divergencia con el proc; ejercicio mal cerrado; saldos de apertura incorrectos | Restricciones 6a/6b/6c/6e/6g + criterios 1/2/3/6 |
| Cierre parcial (comprobante sin saldos, o P07 sin comprobante) | Estado inconsistente irrecuperable (cierre definitivo) | Restriccion 6b (atomicidad) + el proc confirma/revierte junto |
| Segundo cierre de la misma vigencia | Comprobante/saldos duplicados | Criterio 4 (negativo 54460-54487) |
| Reserva en entidad publica o sin parametros aprobados | Reserva legal indebida / mal calculada | Restriccion 6g + criterios 5/6 (54480-54487) |
| Asumir el mapeo THROW / las reglas de cierre por analogia | Criterio apunta al THROW incorrecto; regla de cierre inventada | F-NOVA-01: RE-CONFIRMAR 54460-54487 + reglas de cierre + P07 contra OBJECT_DEFINITION |
| Autorizacion decorativa (rol de cierre anual no verificado) | Cierre definitivo sin rol adecuado | Restriccion 6f + criterio 11 + test mecanico |
| Mock/fixture disfrazado de evidencia F-NOVA-01 | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6h): clase SQL real via accounting_sandbox_verifier |

## 10. Prioridad definida
**GOAL cierre anual contable** (proceso definitivo del ejercicio: comprobante `annual_close` + saldos iniciales de la
siguiente vigencia + P07 + reserva legal privada; criticidad de INTEGRIDAD ALTA -- unica excepcion controlada al
bloqueo de periodo). Pertenencia Q4: N/A a la muestra medida (esta unidad NO se mide; R3-b cierre mensual si, y
depende de esta invariante). Dependencias: proc de cierre anual (existe, base congelada schema/028), patron congelado
NOVA-SPEC-T-001, diseno de autorizacion real (s.6f), SPEC-CONT-S3 (cierre mensual, que NO activa la escotilla).
**LINEA ROJA: esta unidad NO SE CONSTRUYE antes del 30-jul** (pool Q4/gobernado); esta SPEC es DISENO/PREP unicamente.
**Nota de gaps (RE-CONFIRMAR por el maker contra el proc, no supuestos):** (1) NO hay periodo "P13"/anual -- el
control anual es `annual_close` + P07; (2) el SDD dice "meses abiertos INDEBIDAMENTE", no "los 12 meses cerrados" --
la definicion exacta se re-confirma contra el proc; (3) idempotente O bloquear duplicado -- el mecanismo exacto y su
THROW se re-confirman; (4) que clases/cuentas de resultado se saldan y como se traslada -- se re-confirma contra
`OBJECT_DEFINITION`; (5) el rol de auth del cierre anual (el SDD no lo nombra) lo fija el maker (>= S3).
