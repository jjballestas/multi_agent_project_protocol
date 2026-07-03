# SPEC-NOVA-P3-002 - Availability Certificate Draft / CDP (crear / capturar / emitir)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, familia P3.
> Generada desde NOVA-PRES-04 (CDP) + NOVA-GOAL-001 + arquitectura. Reusa el patron aprobar-via-proc de P3.1.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P3-002 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly, NO la conversacion del maker)
- arm: gobernado - family: P3 - unit: P3.2
- q4_membership: **CONDICIONAL** (criticidad media; entra al pool Q4 si su DEC esta cerrada al sello Etapa 2)
- isolation: sin hermano baseline en P3; manifiesto de archivos leidos + leyo_codigo_hermano = NO
- db_verified_at: objetos citados de NOVA-PRES-04 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada al construir (F-NOVA-01)
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto crea y captura el borrador de un CDP (certificado de disponibilidad) que ampara uno o
varios pares rubro-fuente (y proyecto BPIN en inversion/regalias) por un valor por linea, y lo EMITE via
`Budget.Approve_Availability_Certificate_Draft`, que valida bajo bloqueo la regla de oro (lo solicitado por
rubro-fuente no excede la apropiacion vigente menos el CDP ya emitido) y numera por serie segun regimen.
- Fuente: NOVA-PRES-04 s.1 (Proposito) + s.3.2 (emision controlada) + s.5 (Contrato) + GOAL-P3 (Availability Draft).
- Calidad: falsable. Bien: "emitir un CDP cuyo solicitado por rubro-fuente supera el disponible es rechazado con THROW 50150; un borrador cuadrado se emite con numero de serie asignado por la BD".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto** (ordenador del gasto / su delegado): captura el borrador, previsualiza la validacion
y emite. Matriz de autorizacion por operacion aun no sembrada en BD (NOVA-PRES-001 s.6 B-05). SUPUESTO TEMPORAL:
usuario autenticado con rol presupuesto puede capturar y emitir; se sustituye por policy por operacion (BR-C4)
post-Sprint-1. La numeracion la asigna la BD; el usuario nunca propone numero.

## 3. Alcance definido
1. Crear/editar el borrador (`Availability_Certificate_Draft(_Line)`) en estado draft -> canal: DML tipado del gateway (NOVA-PRES-04 s.5 fila "Crear/editar").
2. Anclar cada linea a un par rubro-fuente activo de la vigencia; si el rubro es inversion/regalias, exigir BPIN (RN-07, enforcement de SPEC) y anclar (rubro-fuente, proyecto).
3. Previsualizar la validacion antes de emitir -> `vw_Availability_Certificate_Draft_Line_Validation` (bit `appropriation_balance_is_valid` por linea; los mismos numeros del 50150).
4. Transicion `draft -> ready_to_approve`.
5. Emitir el CDP -> canal UNICO: `Budget.Approve_Availability_Certificate_Draft(@draft,@user[,@code])`.
6. Descartar borrador -> estado `discarded`.
7. Leer saldos del CDP para mostrar disponible real (ver campo 6, restriccion B-01).

## 4. Fuera de alcance definido
- Ajustes de credito/contracredito (08/09): `Budget.Apply_Availability_Adjustment`, Doc 03 (SPEC separada).
- **Anulacion del CDP**: no existe `Annul_Availability_Certificate` (NOVA-PRES-04 s.6 B-03) -> NO se implementa aqui; se especifica aparte, simetrica al patron de reversos (Doc 08); jamas se "anula" con DELETE ni descripcion magica legacy.
- **Validacion de saldo por proyecto BPIN** (RN-08 / B-02): el proc NO la hace; ver campo 6 (compensacion en caso de uso) y riesgos; elevarla al proc es solicitud de hardening.
- CDP desde nomina (B-05): integracion Payroll (GOAL-P5), fuera.
- Espejos de cierre (Constitute_Reserves/Payables via Close_Fiscal_Year, Doc 09); impresion/kardex legacy (reemplazo = Doc 11).
- Cualquier acceso directo a `Availability_Certificate(_Line)` desde la app (la app nunca escribe la tabla definitiva) o reimplementacion del saldo en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada):**
  - Tablas: `Availability_Certificate`, `Availability_Certificate_Line`, `Availability_Certificate_Draft`, `Availability_Certificate_Draft_Line`, `Availability_Certificate_Line_Adjustment` (NOVA-PRES-04 s.3.1).
  - Proc de emision: `Budget.Approve_Availability_Certificate_Draft(@availability_certificate_draft_id, @approved_by_user_id, @availability_code=NULL)` (THROW 50145-50150; numeracion 50220-50223; bloqueo al validar regla de oro).
  - Numeracion: `Allocate_Document_Number` (serie comun `P` / SGR `G` segun `excludes_annual_carryover`).
  - Vistas: `vw_Availability_Certificate_Draft_Line_Validation` (preview del 50150), `vw_Availability_Certificate_Line_Balance`/`_Balance` (OJO B-01: committed=0), `vw_Commitment_Availability_Validation` (saldo REAL para UI, restriccion 6b), `vw_Investment_Project_Detail_Balance` (saldo por BPIN, restriccion 6c), `vw_Initial_Budget_Line_Balance` (apropiacion vigente, Doc 02).
  - Conversion a letras: `dbo.ConvertirNumero` (la usa el proc; `amount_in_words` persistido).
- **API:** `POST /api/budget/availability-drafts` (crea/captura), `PUT/PATCH .../{id}/lines`, `POST .../{id}/ready`, `GET .../{id}/validation` (previsualizacion), `POST /api/budget/availability-drafts/{id}/approve` (emite; invoca el proc), `POST .../{id}/discard`, `GET` de lectura. DTOs 1:1 con resultsets; ProblemDetails.
- **UI (apps/nova-web):** captura de lineas (rubro-fuente, BPIN cuando aplica), tablero de previsualizacion (`vw_..._Draft_Line_Validation`), **saldo disponible mostrado desde `vw_Commitment_Availability_Validation`** (no desde la vista de balance con committed=0), boton emitir habilitado solo con todas las lineas validas. Vigencia explicita (F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/AvailabilityCertificates/` (CreateDraft, CaptureLines, PreviewValidation, MarkReady, ApproveDraft, DiscardDraft, ReadBalance).
- **Referencias:** NOVA-PRES-04 (s.3-s.6), NOVA-PRES-02 (apropiacion vigente), NOVA-PRES-000 s.03/s.08, dictionary/availability_certificates(+operations), NOVA-GOAL-001 (GOAL-P3 + APIs).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + maestro-P1..P6 (NOVA-PRES-000 s.03) + stack del preambulo.
- Propias:
  - (a) La EMISION es SOLO `Approve_Availability_Certificate_Draft`; la app nunca escribe `Availability_Certificate(_Line)` ni recalcula la regla de oro; captura del borrador = DML tipado del gateway.
  - (b) **B-01 (Alta):** `vw_Availability_Certificate_Line_Balance` tiene `committed_amount=0` (no descuenta compromisos) -> la UI JAMAS muestra saldo de CDP desde esa vista; usa `vw_Commitment_Availability_Validation` para el disponible real. El control duro (50115) vive en el proc de compromiso (Doc 05); esto es un defecto de LECTURA. Registrar solicitud de hardening: recrear la vista integrando `Commitment_Line` + ajustes.
  - (c) **B-02 (Alta) / RN-08:** ni el proc ni el 50150 validan que los CDP de un proyecto BPIN no excedan su valor asignado (colapsan lineas de distinto BPIN por rubro-fuente). Compensacion en el CASO DE USO: validar contra `vw_Investment_Project_Detail_Balance` antes de emitir cuando hay BPIN, y registrar solicitud de elevar la validacion al proc. Declarar el limite (la BD no lo fuerza).
  - (d) **RN-07:** BPIN obligatorio cuando el rubro es inversion/regalias/2.3* -> enforcement del SPEC/caso de uso (la BD solo valida el par si el BPIN viene).
  - (e) Solo rubros auxiliares de gasto; vigencia abierta; catalogos validos (THROW 50210/50211/50212, 50066-50068).
  - (f) Numeracion por serie de la BD dentro de la transaccion; la UI no propone/reserva numero. Vigencia explicita.
  - (g) Toda mutacion: correlation id + usuario real + THROW traducido a ProblemDetails.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un borrador ready_to_approve con lineas cuyo solicitado por rubro-fuente <= disponible, **cuando** emito, **entonces** `Approve_Availability_Certificate_Draft` inserta la cabecera 'G' con numero de serie asignado (P/G segun regimen), agrupa lineas por rubro-fuente-BPIN, marca el borrador `approved` y persiste `amount_in_words`.
2. **Dado** un borrador cuyo solicitado por algun rubro-fuente EXCEDE el disponible (apropiacion vigente - CDP activos 'G' netos de 08/09), **cuando** intento emitir, **entonces** ProblemDetails del THROW **50150** y no se emite nada.
3. **Dado** un borrador NO en ready_to_approve o sin lineas activas, **cuando** intento emitir, **entonces** THROW **50146**/**50147** (y borrador inexistente = **50145**).
4. **Dado** una linea con rubro de ingreso o rubro mayor (no auxiliar), **cuando** la capturo, **entonces** THROW **50210**/**50211**; par rubro-fuente de otra vigencia = **50076**.
5. **Dado** un rubro de inversion/regalias SIN BPIN, **cuando** intento capturar/emitir, **entonces** el caso de uso lo rechaza (RN-07, validacion de aplicacion; 400 ProblemDetails).
6. **Dado** un CDP con BPIN cuyo acumulado excederia el valor asignado del proyecto, **cuando** intento emitir, **entonces** el caso de uso lo rechaza validando `vw_Investment_Project_Detail_Balance` (B-02; 400 ProblemDetails) -- criterio que la BD hoy NO cubre y la aplicacion SI debe cubrir.
7. **Dado** la previsualizacion, **entonces** `vw_Availability_Certificate_Draft_Line_Validation` marca `appropriation_balance_is_valid` por linea con los MISMOS numeros que el 50150 (paridad preview vs emision).
8. **Dado** el disponible mostrado en UI, **entonces** proviene de `vw_Commitment_Availability_Validation` (no de la vista con committed=0) -- verificable comparando contra el saldo real con compromisos.

## 8. Pruebas / gates definidos
- **Unit:** mapeo DTO->parametros del proc; maquina de estados draft/ready/approved/discarded; enforcement RN-07 (BPIN obligatorio) y B-02 (saldo BPIN) en el caso de uso; traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain sin Infrastructure; Application sin ASP.NET; Api/Mcp sin SQL directo; cero DataTable.
- **Integracion vs DbsFinanciero:** criterio 1 (emision happy: numero de serie + agrupacion), un caso por THROW (50150, 50146/50147/50145, 50210/50211, 50076), criterio 6 (rechazo BPIN via vista), criterio 7 (paridad preview vs 50150), criterio 8 (disponible real vs vista committed=0). EXECUTE: conector readonly sin EXECUTE (Msg 229) -> GRANT EXECUTE al rol de verificacion o SELECT a la vista/fn equivalente, documentado.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=reimplementacion, 3=DML directo, 5=paridad de numeros, 9=fuera de alcance respetado -- que NO intente anular ni tocar 08/09) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| UI muestra saldo inflado (vw balance committed=0, B-01) | El usuario cree que hay disponible que ya esta comprometido | Restriccion 6b: usar `vw_Commitment_Availability_Validation`; registrar hardening de la vista |
| CDP de un BPIN excede su valor asignado (B-02/RN-08) | Sobre-reserva por proyecto no detectada por la BD | Restriccion 6c: validacion en caso de uso vs `vw_Investment_Project_Detail_Balance`; solicitar elevar al proc |
| Emitir copiando filas sin el proc | Rompe la regla de oro y la numeracion | Restriccion 6a; el adversarial verifica emit == invocar el proc |
| Reimplementar el disponible/regla de oro en C# | Divergencia silenciosa con la BD | Prohibido (6a); el adversarial lo busca (punto 2) |
| BPIN faltante en inversion/regalias (RN-07) | CDP sin control de proyecto | Enforcement de aplicacion (6d); criterio 5 |
| Tentacion de implementar anulacion (B-03) | Fuera de alcance; sin proc de anulacion | Campo 4 lo excluye; el adversarial verifica (punto 9) |

## 10. Prioridad definida
**GOAL-P3** (drafts y aprobaciones Budget), brazo GOBERNADO, familia P3 (P3.2). Elegible al pool Q4 (criticidad
media) si su DEC esta cerrada al sello Etapa 2. Severidad s.08: primer eslabon de la cadena de gasto (el CDP es el
techo del compromiso). Dependencias: GOAL-P1 (fundacion) + apropiacion vigente disponible (Doc 02, presupuesto de
la vigencia aprobado -- por eso P3.1 antecede logicamente). NO depende de brecha de BD para el camino feliz (el
proc y el 50150 existen y estan verificados); B-01/B-02 se compensan en el caso de uso y se registran como
hardening. Desbloquea: Commitment Draft (Doc 05, se expide con cargo a un CDP).
