# SPEC-NOVA-P3-004 - Obligation Draft / Obligacion (crear / capturar / aprobar)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, familia P3.
> Generada desde NOVA-PRES-06 (Obligacion) + NOVA-GOAL-001 + arquitectura. Reusa el patron aprobar-via-proc.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P3-004 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly)
- arm: gobernado - family: P3 - unit: P3.4
- q4_membership: **CONDICIONAL** (criticidad media; entra al pool Q4 si su DEC esta cerrada al sello Etapa 2)
- isolation: familia P3 gobernada sin hermano baseline; manifiesto de archivos leidos = PRES-06 (+PRES-05 herencia); leyo_codigo_hermano = NO
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: objetos de NOVA-PRES-06 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01)
- throw_source (verificado OBJECT_DEFINITION + PRES-06 s.3.1): **PROC-DIRECTO** `Approve_Obligation_Draft` = 50128-50134 (regla de oro = 50134) [confirmado en OBJECT_DEFINITION]. **NUMERACION** (`Allocate_Document_Number`): 50220-50223. **TRIGGER/CHECK durante la transaccion** (NO en la def directa del proc; fuente = triggers de Obligation(_Line) per PRES-06 s.3.1): 50116-50121 (coherencia de cabecera: vigencia/uso/catalogos/compromiso), 50210/50211 (no ingreso / solo auxiliares en linea), 50212 (vigencia abierta, trigger trg_obligation__validate_open_year).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto crea el borrador de una obligacion (causacion presupuestal) DENTRO de un compromiso
(heredando sus lineas rubro-fuente-BPIN con saldo), reconociendo el cumplimiento y el deber de pagar, y lo aprueba
via `Budget.Approve_Obligation_Draft`, que valida bajo bloqueo que lo obligado por linea no excede el saldo de la
linea del compromiso y numera por serie.
- Fuente: NOVA-PRES-06 s.1 (Proposito) + s.3.1 (aprobacion) + s.5 (Contrato) + GOAL-P3 (Obligation Draft: crear/editar/validar/aprobar).
- Calidad: falsable. Bien: "obligar una linea por encima del saldo del compromiso es rechazado con THROW 50134; una obligacion valida se aprueba heredando ancla y BPIN de la linea de compromiso".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto** (causacion): captura el borrador de obligacion (beneficiario/solicitante reales de
`Core.Entity`, uso contable, documento fuente por puente), lo envia a aprobacion y lo aprueba. Matriz de
autorizacion por operacion no sembrada (B-05 de Doc 01). CONFIRMADO por el Operador (DD-01), aceptado para Sprint 1:
usuario autenticado con rol presupuesto; policy por operacion via BR-C4 CONFIRMADA post-Sprint-1. Numeracion por la BD.

## 3. Alcance definido
1. Crear/editar el borrador (`Obligation_Draft(_Line)`) en draft -> canal: DML tipado del gateway (NOVA-PRES-06 s.5 fila "Crear/editar").
2. Herencia desde el compromiso: cada linea de la obligacion pertenece a una linea del compromiso (RN-02, THROW en 50128-50133), hereda ancla rubro-fuente + BPIN.
3. Capturar beneficiario/solicitante, uso contable, tipo de vigencia (1/2/3), y el enlace al documento fuente por PUENTE tipificado (`Radication_Obligation` u otro; `reference_type/number` es solo trazabilidad legacy).
4. Transicion `draft -> ready_to_approve`.
5. Aprobar la obligacion -> canal UNICO: `Budget.Approve_Obligation_Draft(@draft,@user[,@code])`.
6. Descartar borrador -> `discarded`.
7. Leer saldos: `vw_Obligation_Commitment_Validation` (pre-validacion contra el compromiso) y `vw_Obligation_Line_Balance` (saldo de la obligacion = techo del pago).

## 4. Fuera de alcance definido
- **Radicacion y liquidacion (PayControl)**: NOVA-PRES-06 s.6 B-01/B-02 (ALTAS): NO existen procs go-forward `Create_Radication`/`Liquidate_Radication`/`Order_Radication`; ahi nace el comprobante contable (causacion via `Post_Voucher`) y las retenciones (B-05). TODO ese circuito es integracion PayControl (GOAL-P5) + hardening -> FUERA de esta SPEC. Esta SPEC cubre la OBLIGACION del esquema Budget, enlazando el documento fuente por el puente EXISTENTE, sin crear la radicacion.
- Reintegro (tipo 14): `Budget.Apply_Obligation_Adjustment`, Doc 03 (SPEC separada; es P4.4, pool Q4).
- Anulacion de la obligacion: `Budget.Annul_Obligation` (Doc 08) -> SPEC de reversos separada (cascada validada 50176-50179).
- Pago (Doc 07), constitucion de CxP al cierre (Doc 09).
- Cualquier escritura directa a `Obligation(_Line)` desde la app o recalculo del saldo del compromiso/obligacion en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada):**
  - Tablas: `Budget.Obligation`, `Obligation_Line`, `Obligation_Draft`, `Obligation_Draft_Line`, `Obligation_Line_Adjustment` (NOVA-PRES-06 s.3.1); puente `PayControl.Radication_Obligation` (rol source; enlace, no FK directa).
  - Proc: `Budget.Approve_Obligation_Draft(@obligation_draft_id, @approved_by_user_id, @obligation_code=NULL)` (bloquea lineas del compromiso; THROW 50128-50134; numeracion 50220-50223).
  - Numeracion: `Allocate_Document_Number` (comun numerica / SGR `G`).
  - Vistas: `vw_Obligation_Commitment_Validation` (pre-validacion del 50134), `vw_Obligation_Line_Balance` (current_obligation - pagado neto = techo del pago), `vw_Commitment_Line_Balance` (saldo del compromiso padre).
  - Terceros: `Core.Entity`.
- **API:** `POST /api/budget/obligation-drafts`, `PUT/PATCH .../{id}/lines`, `POST .../{id}/validate` (previsualiza via `vw_Obligation_Commitment_Validation`), `POST .../{id}/ready`, `POST /api/budget/obligation-drafts/{id}/approve` (invoca el proc), `POST .../{id}/discard`, `GET` de lectura. DTOs 1:1; ProblemDetails.
- **UI (apps/nova-web):** seleccion de compromiso con saldo -> herencia de lineas; captura de beneficiario/uso/documento fuente; previsualizacion del saldo por linea; boton aprobar solo con lineas dentro del saldo del compromiso. Vigencia explicita (F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/Obligations/` (CreateDraft, InheritFromCommitment, CaptureHeaderAndLines, LinkSourceDocument, PreviewValidation, MarkReady, ApproveDraft, DiscardDraft, ReadBalance).
- **Referencias:** NOVA-PRES-06 (s.3-s.6), NOVA-PRES-05 (compromiso), NOVA-PRES-000 s.03/s.08, dictionary/obligations(+paycontrol), NOVA-GOAL-001 (GOAL-P3 + APIs).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La APROBACION es SOLO `Approve_Obligation_Draft`; la app nunca escribe `Obligation(_Line)` ni recalcula la regla de oro/saldo; captura = DML tipado del gateway.
  - (b) Herencia estricta del compromiso: cada linea de la obligacion pertenece a una linea del compromiso (RN-02); hereda ancla rubro-fuente + BPIN; nunca imputa combinaciones fuera del compromiso.
  - (c) **RN-04 / P4:** la obligacion NO contabiliza -- el asiento nace en la LIQUIDACION de la radicacion (causacion, via `Post_Voucher`, puente rol liquidation) y en el pago. Esta SPEC no postea comprobantes.
  - (d) **B-04 / RN-10:** la fecha de la obligacion >= fecha del compromiso NO la fuerza la BD -> validacion dura en el caso de uso; registrar solicitud de elevar al proc.
  - (e) El documento fuente se enlaza por PUENTE tipificado (`Radication_Obligation` u otro), no por FK polimorfica; `reference_type/number` es solo trazabilidad legacy (no logica).
  - (f) Solo rubros auxiliares de gasto; misma vigencia que el compromiso; vigencia abierta; catalogos validos (THROW 50210/50211/50116-50121/50212).
  - (g) Numeracion por serie de la BD; saldo de la obligacion siempre por `vw_Obligation_Line_Balance` (nunca acumulador; el reintegro 14 lo reduce). Toda mutacion: correlation id + usuario real + ProblemDetails.
  - (h) **GUARD DE PROCEDENCIA:** el harness de evidencia F-NOVA-01 usa una clase SQL real, gateada
    por env vars, NA limpio sin credenciales -- jamas un mock/Recording* in-memory (precedente TASK-0253).
  - (i) **LECTURA DE RESULT-SET SIN ADIVINANZA (hereda P4-006):** el gateway de produccion NO debe leer
    columnas del result-set de `Approve_Obligation_Draft` por fallback encadenado de nombres ni caer en
    un DEFAULT SILENCIOSO si la columna no aparece. El nombre EXACTO de cada columna se confirma contra
    `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de escribir el
    gateway; el harness F-NOVA-01 ejercita el MISMO camino de lectura.
  - (j) **COBERTURA HTTP DE INTEGRACION (hereda P4-006):** cada endpoint mutador nuevo (ready/aprobar/
    discard) tiene al menos un test de integracion HTTP real (`WebApplicationFactory` + gateway FALSO).
  - (k) **LISTA DE AISLAMIENTO COMPLETA (hereda P4-006):** el test de arquitectura de aislamiento del
    frontend incluye `Approve_Obligation_Draft` en su lista de literales prohibidos.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un borrador ready_to_approve cuyas lineas <= saldo de las lineas del compromiso, **cuando** apruebo, **entonces** `Approve_Obligation_Draft` inserta la cabecera 'G' con numero de serie, hereda ancla y BPIN, marca el borrador `approved`.
2. **Dado** un borrador con una linea que EXCEDE el saldo de su linea de compromiso (committed +11 -12 - obligado activo neto), **cuando** intento aprobar, **entonces** ProblemDetails del THROW **50134** y no se causa nada.
3. **Dado** un borrador inexistente / no ready / sin lineas / con linea fuera del compromiso, **cuando** intento aprobar, **entonces** THROW **50128-50133** segun el caso.
4. **Dado** una linea con rubro de ingreso o mayor, **cuando** la capturo, **entonces** THROW **50210/50211**; cabecera con vigencia distinta a la del compromiso = **50116**.
5. **Dado** una obligacion con fecha ANTERIOR a la del compromiso, **cuando** intento aprobar, **entonces** el caso de uso lo rechaza (RN-10/B-04, validacion de aplicacion; 400 ProblemDetails) -- la BD hoy NO lo cubre.
6. **Dado** una cabecera sin beneficiario o sin enlace a documento fuente por puente, **cuando** intento crear/aprobar, **entonces** rechazo (RN-03; el puente es la trazabilidad go-forward).
7. **Dado** el saldo tras aprobar, **entonces** `vw_Obligation_Line_Balance` = current_obligation - pagado neto (sin recalculo en C#); techo del pago.
8. **Dado** una cabecera con uso/catalogo/compromiso incoherente (fuera de 50116), **cuando** la creo,
   **entonces** THROW **50117-50121** (segun el chequeo puntual).
9. **Dado** el gateway de produccion, **entonces** lee cada columna del result-set por el nombre EXACTO
   confirmado contra `OBJECT_DEFINITION`, sin fallback encadenado ni default silencioso.
10. **Dado** los endpoints mutadores (ready/aprobar/discard), **entonces** cada uno tiene al menos un test
    de integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica el wiring completo.

## 8. Pruebas / gates definidos
- **Unit:** mapeo DTO->parametros del proc; maquina de estados; herencia de lineas del compromiso; enforcement RN-10 (fecha) y RN-03 (puente) en el caso de uso; traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain sin Infrastructure; Application sin ASP.NET; Api/Mcp sin SQL directo; cero DataTable.
- **Integracion vs DbsFinanciero:** criterio 1 (aprobacion happy: serie + herencia), un caso por THROW (50134, 50128-50133, 50210/50211, 50116), criterio 5 (rechazo fecha via caso de uso), criterio 7 (saldo por vista). EXECUTE: conector readonly sin EXECUTE (Msg 229) -> GRANT EXECUTE al rol de verificacion o SELECT a la vista/fn equivalente, documentado.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=reimplementacion, 3=DML directo, 9=fuera de alcance -- NO radicar/liquidar/contabilizar, NO anular, NO tocar 14) + guard de procedencia + criterio 9 (lectura de columnas) + criterio 10 (test HTTP de integracion) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Implementar radicacion/liquidacion/causacion "de paso" (B-01) | Se sale del alcance y toca el asiento contable sin proc | Campo 4 lo excluye; es GOAL-P5/hardening; el adversarial verifica (punto 9) |
| Fecha obligacion < compromiso no detectada (B-04/RN-10) | Causacion inconsistente | Restriccion 6d: validacion en caso de uso; solicitar elevar al proc |
| Aprobar copiando filas sin el proc | Rompe la regla de oro 50134 y la herencia | Restriccion 6a/6b; el adversarial verifica approve == invocar el proc |
| Postear comprobante desde la obligacion (viola RN-04/P4) | Asiento donde no debe nacer | Restriccion 6c; el asiento nace en liquidacion/pago |
| Enlazar fuente por reference_type/number en vez del puente | Trazabilidad fragil polimorfica | Restriccion 6e: puente tipificado |
| Reimplementar saldo del compromiso/obligacion en C# | Divergencia con la BD | Prohibido (6a/6g); el adversarial lo busca (punto 2) |

## 10. Prioridad definida
**GOAL-P3** (drafts y aprobaciones Budget), brazo GOBERNADO, familia P3 (P3.4). **Pertenencia Q4: CONDICIONAL**
(criticidad media; entra si su DEC esta cerrada al sello Etapa 2). Severidad s.08: tercer eslabon de la cadena de
gasto (la obligacion es el techo del pago). Dependencias: GOAL-P1 (fundacion) + compromiso operable (P3.3, la
obligacion vive dentro de un compromiso con saldo). NO depende de brecha de BD para el camino feliz de la
OBLIGACION (el proc y el 50134 existen y estan verificados); el circuito de radicacion/liquidacion (B-01/B-02) es
otra entrega (GOAL-P5/hardening). Desbloquea: Payment Draft (Doc 07, se paga contra el saldo de la obligacion).

## ENMIENDA FECHADA 2026-07-06T04:52Z (Arquitecto) - Herencia de la guarda BR-C4 (Assert_Permission) en el proc REAL de captura

Contexto: BR-C4 (matriz de autorizacion por operacion) fue entregada por el DBA y VERIFICADA
independientemente en sandbox (sello Etapa 1 s.27): guarda real en aprobar/anular; en
captura-de-borrador se probo con shim Authorize_*_Draft_Capture porque el proc real se
construye en Sprint 1 bajo esta SPEC. Restriccion NUEVA (vinculante, se agrega a s.6):

- El proc REAL de captura de borrador de esta unidad DEBE invocar Security.Assert_Permission
  con el permission_code de su celda (documento x operacion draft_capture) ANTES de cualquier
  mutacion -- HEREDA la guarda desplegada, NUNCA la reimplementa en el proc ni en C#.
- Set THROW de la guarda: 50320-50324 (centralizado en Security.Assert_Permission; incluye
  fail-closed 50320 si falta SESSION_CONTEXT). La superficie C#/API mapea estos codigos a
  ProblemDetails especificos de ESTA superficie (leccion del hallazgo #10: sin etiquetado
  cruzado entre superficies) y agrega el criterio negativo Given/When/Then correspondiente
  en s.7 al construirse.
- La verificacion F-NOVA-01 de esta unidad RE-VERIFICA por OBJECT_DEFINITION que el proc real
  desplegado invoca Assert_Permission (el shim del DBA NO cuenta como evidencia del proc real).
