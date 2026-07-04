# SPEC-NOVA-P3-005 - Payment Draft / Pago presupuestal (crear / capturar / aprobar)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, familia P3.
> CRITICIDAD ALTA (frontera Treasury/Pagos). Generada desde NOVA-PRES-07 (Pago/Egreso) + NOVA-GOAL-001 + arquitectura.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P3-005 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly)
- arm: gobernado - family: P3 - unit: P3.5
- q4_membership: **FUERA** (criticidad ALTA, frontera Treasury/Pagos -> por la regla de criticidad sellada NO entra al contraste causal Q4; se especifica igual, solo descriptiva)
- isolation: familia P3 gobernada sin hermano baseline; manifiesto de archivos leidos = PRES-07 (+PRES-06 herencia); leyo_codigo_hermano = NO
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: objetos de NOVA-PRES-07 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01)
- throw_source (verificado OBJECT_DEFINITION + PRES-07): **PROC-DIRECTO** `Approve_Payment_Draft` = 50180-50187 (regla de oro = 50187) [confirmado en OBJECT_DEFINITION; el proc NO emite 50188-50190]. **TRIGGER/CHECK durante la transaccion** (NO en la def directa del proc): 50188-50190 (coherencias de vigencia/pertenencia de Payment_Draft(_Line), PRES-07 s.3.1), 54257 (trigger de `Payment_Order_Budget_Line`: obligacion de la misma vigencia que la orden).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto crea el borrador de un pago presupuestal DENTRO de una obligacion (heredando sus lineas
rubro-fuente-BPIN con saldo) y lo aprueba via `Budget.Approve_Payment_Draft`, que valida bajo bloqueo que lo pagado
por linea no excede el saldo de la linea de obligacion y MATERIALIZA la orden de pago (egreso) con sus lineas
presupuestales (el pago presupuestal ES la linea del egreso, `Treasury.Payment_Order_Budget_Line`).
- Fuente: NOVA-PRES-07 s.1 (Proposito) + s.3.2 (aprobacion) + s.5 (Contrato) + GOAL-P3 (Payment Draft: crear/editar/validar/aprobar).
- Calidad: falsable. Bien: "pagar una linea por encima del saldo de la obligacion es rechazado con THROW 50187; un pago valido crea la Payment_Order 'G' con source_module_code='budget_payment_draft' y sus lineas presupuestales".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto / Tesoreria** (ordenacion del pago presupuestal): captura el borrador de pago,
lo envia a aprobacion y lo aprueba (control presupuestal). El egreso REAL (banco, retenciones, comprobante) es del
circuito Tesoreria/PayControl (fuera de alcance, B-01). Matriz de autorizacion por operacion no sembrada.
CONFIRMADO por el Operador (DD-01), aceptado para Sprint 1: usuario autenticado con rol presupuesto; policy por
operacion via BR-C4 CONFIRMADA post-Sprint-1. Numeracion por la BD.

## 3. Alcance definido
1. Crear/editar el borrador (`Budget.Payment_Draft(_Line)`) en draft -> canal: DML tipado del gateway (NOVA-PRES-07 s.5 fila "Crear/editar").
2. Herencia desde la obligacion: cada linea del pago pertenece a una linea de obligacion (RN-03, THROW 50186 proc-directo; 50188-50190 triggers de coherencia del borrador), hereda vigencia/rubro/fuente/BPIN.
3. Transicion `draft -> ready_to_approve`.
4. Aprobar el pago presupuestal (control presupuestal + materializar la orden) -> canal UNICO: `Budget.Approve_Payment_Draft(@draft,@user[,@number])`; devuelve `payment_order_id, payment_number`.
5. Descartar borrador -> `discarded`.
6. Leer: `vw_Payment_Obligation_Validation` (pre-validacion del 50187), `vw_Obligation_Line_Balance` (saldo de obligacion = techo del pago), `vw_Payment_Amount_Validation` (cuadre auditado del egreso).

## 4. Fuera de alcance definido
- **El egreso REAL go-forward** (NOVA-PRES-07 s.6 B-01, ALTA): banco/cuenta, medio de pago, retenciones prorrateadas, giro por el neto y COMPROBANTE contable NO tienen proc; `Approve_Payment_Draft` deja la orden con banco NULL, metodo 'O', por el bruto, sin comprobante. Todo el egreso real es circuito Tesoreria/PayControl (GOAL-P5) + hardening -> FUERA. Esta SPEC cubre el CONTROL PRESUPUESTAL del pago.
- **Notas de tesoreria** (B-02, ALTA): creacion/partida-doble/posteo/generacion de egreso desde nota (`Create_Treasury_Note`) sin proc -> FUERA (Treasury go-forward).
- Anulacion/reintegro del egreso: `treasury.Annul_Payment_Order`/`Reverse_Payment_Order` (Doc 08) -> SPEC de reversos separada.
- Conciliacion y posicion bancaria (B-06): release siguiente.
- Cualquier posteo contable desde este flujo (P4: el asiento nace en causacion/pago via Post_Voucher en Tesoreria) o recalculo del saldo de obligacion en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada):**
  - Tablas: `Budget.Payment_Draft`, `Budget.Payment_Draft_Line` (schema/127), `treasury.Payment_Order`, `treasury.Payment_Order_Budget_Line` (EL pago presupuestal; `paid_amount`/`reversed_amount`, origen tipificado). (`Budget.Payment/Payment_Line` fueron ELIMINADAS -- no existen.)
  - Proc: `Budget.Approve_Payment_Draft(@payment_draft_id, @approved_by_user_id, @payment_number=NULL)` (bloqueo sobre borrador+lineas de obligacion+pagos; THROW PROC-DIRECTO 50180-50187 -- ver throw_source; 50188-50190 son triggers de Payment_Draft; materializa `Payment_Order` 'G' source_module_code='budget_payment_draft').
  - Numeracion: `MAX(TRY_CONVERT(int, payment_number))+1` por vigencia bajo bloqueo (el egreso NO usa `Document_Series` hoy, B-04).
  - Vistas: `vw_Payment_Obligation_Validation` (pre-validacion del 50187), `vw_Obligation_Line_Balance`, `vw_Payment_Amount_Validation`, `vw_Payment_Order`/`vw_Payment_Line`.
- **API:** `POST /api/budget/payment-drafts`, `PUT/PATCH .../{id}/lines`, `POST .../{id}/validate` (previsualiza via `vw_Payment_Obligation_Validation`), `POST .../{id}/ready`, `POST /api/budget/payment-drafts/{id}/approve` (invoca el proc; retorna payment_order_id/number), `POST .../{id}/discard`, `GET`. DTOs 1:1; ProblemDetails.
- **UI (apps/nova-web):** seleccion de obligacion con saldo -> herencia de lineas; captura del monto solicitado por linea; previsualizacion del saldo; boton aprobar solo con lineas dentro del saldo de la obligacion; **advertencia clara de que el egreso real (banco/retenciones/comprobante) es un paso Tesoreria posterior** (no lo hace este flujo). Vigencia explicita (F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/PaymentDrafts/` (CreateDraft, InheritFromObligation, CaptureLines, PreviewValidation, MarkReady, ApprovePaymentDraft, DiscardDraft, ReadBalance).
- **Referencias:** NOVA-PRES-07 (s.3-s.6), NOVA-PRES-06 (obligacion), NOVA-PRES-000 s.03/s.08, dictionary/payments(+treasury_*), NOVA-GOAL-001 (GOAL-P3 + APIs).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La APROBACION es SOLO `Approve_Payment_Draft`; la app nunca escribe `Payment_Order(_Budget_Line)` ni recalcula la regla de oro/saldo; captura = DML tipado del gateway.
  - (b) Herencia estricta: cada linea del pago pertenece a una linea de obligacion (RN-03); obligacion de la MISMA vigencia que la orden (RN-02, trigger 54257).
  - (c) **B-01 (Alta):** el egreso queda con banco NULL, metodo 'O', bruto, SIN comprobante ni retenciones -> la UI/caso de uso DECLARA que el egreso real es un paso Tesoreria posterior; JAMAS improvisa banco/retenciones/comprobante en este flujo.
  - (d) **P4 / RN-10:** este flujo NO postea comprobante contable; el asiento del pago nace en Tesoreria (Post_Voucher via puente).
  - (e) **B-03:** el proc deja `budget_payment_source_type`/`source_reference_*`/`created_by_user_id` en NULL; el caso de uso que orqueste debe poblarlos (o registrarse la solicitud de extender el proc) -- no dejar centinelas magicos.
  - (f) Numeracion del egreso por la BD (MAX+1 bajo bloqueo hoy; B-04 recomienda migrar a series -- registrar como hardening, no cambiar esquema en esta SPEC). Vigencia explicita; el egreso hoy no tiene guarda de vigencia abierta (B-05) -> validar vigencia abierta en el caso de uso y solicitar el trigger.
  - (g) Saldo de obligacion siempre por `vw_Obligation_Line_Balance` (netea paid-reversed). Toda mutacion: correlation id + usuario real + ProblemDetails.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un borrador ready_to_approve cuyas lineas <= saldo de las lineas de obligacion, **cuando** apruebo, **entonces** `Approve_Payment_Draft` crea la `Payment_Order` 'G' (source_module_code='budget_payment_draft', metodo 'O', fondos 'SI', bank NULL) + las lineas presupuestales consolidadas por linea de obligacion, y retorna payment_order_id/payment_number.
2. **Dado** un borrador con una linea que EXCEDE el saldo de su linea de obligacion (obligado neto - pagado neto), **cuando** intento aprobar, **entonces** ProblemDetails del THROW **50187** y no se materializa egreso.
3. **Dado** un borrador inexistente/no ready/sin lineas/con linea fuera de la obligacion/numero duplicado, **cuando** intento aprobar, **entonces** THROW **50180-50186/50185** segun el caso.
4. **Dado** una obligacion de vigencia distinta a la orden, **cuando** intento aprobar, **entonces** THROW **54257**.
5. **Dado** el egreso creado, **entonces** la UI declara que el pago bancario real (banco/retenciones/comprobante) es un paso Tesoreria posterior; el flujo NO postea comprobante ni calcula retenciones (verificable: el comprobante no existe tras aprobar).
6. **Dado** el saldo tras pagar, **entonces** `vw_Obligation_Line_Balance` refleja paid-reversed sin recalculo en C#; el cuadre del egreso se lee de `vw_Payment_Amount_Validation`.

## 8. Pruebas / gates definidos
- **Unit:** mapeo DTO->parametros del proc; maquina de estados; herencia de lineas de obligacion; enforcement de vigencia abierta (B-05) en el caso de uso; traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain sin Infrastructure; Application sin ASP.NET; Api/Mcp sin SQL directo; cero DataTable.
- **Integracion vs DbsFinanciero:** criterio 1 (aprobacion happy: crea Payment_Order + lineas), un caso por THROW (50187, 50180-50186, 54257), criterio 5 (sin comprobante/retenciones tras aprobar), criterio 6 (saldo por vista). EXECUTE: conector readonly sin EXECUTE (Msg 229) -> GRANT EXECUTE al rol de verificacion o SELECT a la vista/fn equivalente, documentado.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=reimplementacion, 3=DML directo, 9=fuera de alcance -- NO egreso real/retenciones/comprobante, NO notas, NO anular) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Implementar el egreso real (banco/retenciones/comprobante) "de paso" (B-01) | Toca dinero real y contabilidad sin proc, fuera de alcance | Campo 4 lo excluye; es Tesoreria/PayControl go-forward; el adversarial verifica (punto 9) |
| Postear comprobante desde este flujo (viola P4/RN-10) | Asiento donde no debe nacer | Restriccion 6d; el asiento nace en Tesoreria |
| Pagar por encima del saldo de la obligacion | Sobre-ejecucion | RN-01/THROW 50187 bajo bloqueo; la app no recalcula (6a/6g) |
| Egreso sin guarda de vigencia abierta (B-05) | Pago en vigencia cerrada | Restriccion 6f: validar en caso de uso + solicitar trigger |
| Numeracion MAX+1 fuera de series (B-04) | Inconsistencia con el resto de documentos | Registrar hardening; no cambiar esquema en esta SPEC |
| Atributos de linea en NULL (B-03) | Trazabilidad del origen incompleta | Restriccion 6e: poblarlos en el caso de uso; no centinelas |

## 10. Prioridad definida
**GOAL-P3** (drafts y aprobaciones Budget), brazo GOBERNADO, familia P3 (P3.5, ULTIMA de la cadena de gasto).
**Pertenencia Q4: FUERA** (criticidad ALTA por ser frontera Treasury/Pagos; por la regla de criticidad sellada del
estudio NO entra al contraste causal Q4 -- solo descriptiva). Severidad s.08: cuarto/ultimo eslabon (ejecuta la
obligacion). Dependencias: GOAL-P1 (fundacion) + obligacion operable (P3.4, el pago vive dentro de una obligacion
con saldo). El CONTROL PRESUPUESTAL del pago (el proc y el 50187) existe y esta verificado; el egreso real
(B-01/B-02) es Tesoreria/PayControl go-forward (GOAL-P5/hardening). Cierra la familia P3 (presupuesto -> CDP -> RP
-> obligacion -> pago).
