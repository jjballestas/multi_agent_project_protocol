# SPEC-NOVA-P3-003 - Commitment Draft / Compromiso RP (crear / capturar / aprobar)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, familia P3.
> Generada desde NOVA-PRES-05 (Compromiso) + NOVA-GOAL-001 + arquitectura. Reusa el patron aprobar-via-proc.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P3-003 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly)
- arm: gobernado - family: P3 - unit: P3.3
- q4_membership: **CONDICIONAL** (criticidad media; entra al pool Q4 si su DEC esta cerrada al sello Etapa 2)
- isolation: sin hermano baseline en P3; manifiesto de archivos leidos + leyo_codigo_hermano = NO
- db_verified_at: objetos de NOVA-PRES-05 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01)
- throw_source (verificado OBJECT_DEFINITION + PRES-05 s.4): **PROC-DIRECTO** `Approve_Commitment_Draft` = 50109-50115 (regla de oro = 50115, herencia CDP = 50114) [confirmado en OBJECT_DEFINITION]. **NUMERACION** (`Allocate_Document_Number`): 50220-50223. **TRIGGER/CHECK durante la transaccion** (NO en la def directa del proc; fuente = triggers de Commitment(_Line) per PRES-05 s.4): 50091-50094 (cabecera: misma vigencia CDP / uso / catalogos), 50210/50211 (no ingreso / solo auxiliares en linea), 50212 (vigencia abierta, trigger trg_commitment__validate_open_year).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto crea el borrador de un compromiso (registro presupuestal, RP) a favor de un beneficiario,
DENTRO de un CDP (heredando sus lineas rubro-fuente-BPIN con saldo), con objeto/fecha/referencia SECOP, y lo
aprueba via `Budget.Approve_Commitment_Draft`, que valida bajo bloqueo que lo comprometido por linea no excede el
saldo disponible de la linea del CDP y numera por serie segun regimen.
- Fuente: NOVA-PRES-05 s.1 (Proposito) + s.3.2 (aprobacion controlada) + s.5 (Contrato) + GOAL-P3 (Commitment Draft: crear/editar/validar/aprobar).
- Calidad: falsable. Bien: "aprobar un RP cuya linea excede el saldo del CDP es rechazado con THROW 50115; un RP valido se perfecciona con numero de serie y hereda ancla y BPIN del CDP".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto** (ordenador del gasto / delegado): captura el borrador del RP (con beneficiario y
solicitante reales de `Core.Entity`), lo envia a aprobacion y lo aprueba. Matriz de autorizacion por operacion no
sembrada (NOVA-PRES-001 s.6 B-05). CONFIRMADO por el Operador (DD-01), aceptado para Sprint 1: usuario autenticado
con rol presupuesto; policy por operacion via BR-C4 CONFIRMADA post-Sprint-1. Numeracion asignada por la BD.

## 3. Alcance definido
1. Crear/editar el borrador (`Commitment_Draft(_Line)`) en draft -> canal: DML tipado del gateway (NOVA-PRES-05 s.5 fila "Crear/editar").
2. Herencia desde el CDP: al elegir el CDP (con saldo), pre-poblar las lineas del CDP con saldo en el borrador (conveniencia legacy util, B-03); cada linea del RP DEBE pertenecer a una linea del CDP (RN-02).
3. Capturar beneficiario y solicitante (terceros reales), objeto (min. 20 chars, norma del Operador DD-02; 400 ProblemDetails si <20), tipo de vigencia (1/2/3), referencia SECOP (vacia -> 'N/A', DD-03).
4. Transicion `draft -> ready_to_approve`.
5. Aprobar (perfeccionar el RP) -> canal UNICO: `Budget.Approve_Commitment_Draft(@draft,@user[,@code])`.
6. Descartar borrador -> `discarded`.
7. Leer saldos: pre-validacion `vw_Commitment_Availability_Validation`; saldo del RP (techo de obligaciones) `vw_Commitment_Line_Balance`.

## 4. Fuera de alcance definido
- Ajustes credito/contracredito (11/12): `Budget.Apply_Commitment_Adjustment`, Doc 03 (SPEC separada).
- **Anulacion del compromiso**: no existe `Annul_Commitment` (NOVA-PRES-05 s.6 B-02) -> NO se implementa aqui; se especifica aparte simetrica a `Annul_Obligation` (Doc 08: sin obligaciones activas -> estado 'A' -> restaura saldo del CDP); jamas anulacion por convencion de texto legacy.
- Obligaciones (Doc 06), pagos (Doc 07), constitucion de reservas al cierre (Constitute_Reserves, Doc 09), impresion del RP (reemplazo = reporte Doc 11).
- Cualquier escritura directa a `Commitment(_Line)` desde la app o recalculo del saldo del CDP en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada):**
  - Tablas: `Budget.Commitment`, `Commitment_Line`, `Commitment_Draft`, `Commitment_Draft_Line`, `Commitment_Line_Adjustment` (NOVA-PRES-05 s.3.1).
  - Proc: `Budget.Approve_Commitment_Draft(@commitment_draft_id, @approved_by_user_id, @commitment_code=NULL)` (XACT_ABORT; THROW 50109-50115; numeracion 50220-50223; bloquea lineas del CDP y recalcula saldo por linea).
  - Numeracion: `Allocate_Document_Number` (serie comun numerica / SGR prefijo `G`).
  - Vistas: `vw_Commitment_Availability_Validation` (saldo de CDP consumible = pre-validacion del 50115; ES la vista correcta del disponible real, ver P3-002 B-01), `vw_Commitment_Line_Balance` (saldo del RP, techo de obligaciones, views/140 netea reintegro 14).
  - Terceros: `Core.Entity` (beneficiario, solicitante). Conversion a letras: `dbo.ConvertirNumero`.
- **API:** `POST /api/budget/commitment-drafts` (crea; opcional pre-poblar desde CDP), `PUT/PATCH .../{id}/lines`, `POST .../{id}/validate` (previsualiza via `vw_Commitment_Availability_Validation`), `POST .../{id}/ready`, `POST /api/budget/commitment-drafts/{id}/approve` (invoca el proc), `POST .../{id}/discard`, `GET` de lectura. DTOs 1:1; ProblemDetails.
- **UI (apps/nova-web):** seleccion de CDP con saldo -> herencia de lineas; captura de beneficiario/solicitante/objeto/SECOP/tipo vigencia; previsualizacion de saldo por linea; boton aprobar habilitado solo con todas las lineas dentro del saldo del CDP. Vigencia explicita (F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/Commitments/` (CreateDraft, InheritFromCertificate, CaptureHeaderAndLines, PreviewValidation, MarkReady, ApproveDraft, DiscardDraft, ReadBalance).
- **Referencias:** NOVA-PRES-05 (s.3-s.6), NOVA-PRES-04 (CDP), NOVA-PRES-000 s.03/s.08, dictionary/commitments(+operations), NOVA-GOAL-001 (GOAL-P3 + APIs).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La APROBACION es SOLO `Approve_Commitment_Draft`; la app nunca escribe `Commitment(_Line)` ni recalcula la regla de oro/saldo del CDP; captura = DML tipado del gateway.
  - (b) Herencia estricta del CDP: cada linea del RP pertenece a una linea del CDP del borrador (RN-02, THROW 50114); hereda ancla rubro-fuente + BPIN; no imputa combinaciones que el CDP no traiga.
  - (c) **B-01 (Alta) / RN-10:** la fecha del compromiso >= fecha del CDP NO la fuerza la BD (ni proc ni triggers) -> validacion DURA en el caso de uso; registrar solicitud de elevar al proc (hardening). Declarar el limite.
  - (d) Beneficiario y solicitante obligatorios (terceros reales `Core.Entity`); objeto min. 20 chars (norma del Operador DD-02; la validacion de aplicacion rechaza <20 con 400 ProblemDetails); SECOP vacio -> default 'N/A' declarada (decision del Operador DD-03); jamas el `'0'` magico legacy sin significado.
  - (e) Solo rubros auxiliares de gasto; misma vigencia que el CDP; vigencia abierta; catalogos validos (THROW 50210/50211/50091-50094/50212).
  - (f) Numeracion por serie de la BD dentro de la transaccion; la UI no propone numero. Saldo del RP siempre por `vw_Commitment_Line_Balance` (nunca columna acumuladora); el reintegro 14 libera RP (RN-09).
  - (g) Toda mutacion: correlation id + usuario real + THROW traducido a ProblemDetails.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un borrador ready_to_approve cuyas lineas <= saldo disponible de las lineas del CDP, **cuando** apruebo, **entonces** `Approve_Commitment_Draft` inserta la cabecera 'G' con numero de serie, hereda ancla y BPIN de las lineas del CDP, marca el borrador `approved` con el enlace al compromiso.
2. **Dado** un borrador con una linea que EXCEDE el saldo disponible de su linea de CDP (neto de compromisos 'G' de otros RP y ajustes 08/09/11/12), **cuando** intento aprobar, **entonces** ProblemDetails del THROW **50115** y no se perfecciona nada.
3. **Dado** un borrador con una linea que NO pertenece a una linea del CDP, **cuando** intento aprobar, **entonces** THROW **50114**; borrador inexistente/no-ready/sin lineas = **50109/50110/50111**.
4. **Dado** una linea con rubro de ingreso o mayor, **cuando** la capturo, **entonces** THROW **50210/50211**; cabecera con vigencia distinta a la del CDP = **50091**.
5. **Dado** un compromiso con fecha ANTERIOR a la del CDP, **cuando** intento aprobar, **entonces** el caso de uso lo rechaza (RN-10/B-01, validacion de aplicacion; 400 ProblemDetails) -- criterio que la BD hoy NO cubre.
6. **Dado** una cabecera sin beneficiario o sin solicitante, **cuando** intento crear, **entonces** violacion FK NOT NULL / rechazo del caso de uso (RN-03).
7. **Dado** la seleccion de un CDP con saldo, **cuando** creo el borrador con pre-poblado, **entonces** el borrador trae las lineas del CDP con saldo (herencia B-03), editables a la baja.
8. **Dado** el saldo del RP tras aprobar, **entonces** `vw_Commitment_Line_Balance` = committed + creditos(11) - contracreditos(12) - obligado_neto (sin recalculo en C#).
9. **Dado** un RP con objeto de 19 caracteres o menos (norma del Operador DD-02, min. 20 chars), **cuando** intento crear o actualizar el borrador, **entonces** la validacion de APLICACION lo rechaza con **400 ProblemDetails** y NO invoca la aprobacion en BD (criterio falsable: la norma vive en el caso de uso, no en el proc).

## 8. Pruebas / gates definidos
- **Unit:** mapeo DTO->parametros del proc; maquina de estados; herencia de lineas del CDP; enforcement RN-10 (fecha), RN-03 (terceros) y objeto min-20 chars (DD-02, criterio 9) en el caso de uso; traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain sin Infrastructure; Application sin ASP.NET; Api/Mcp sin SQL directo; cero DataTable.
- **Integracion vs DbsFinanciero:** criterio 1 (aprobacion happy: serie + herencia), un caso por THROW (50115, 50114, 50109-50111, 50210/50211, 50091), criterio 5 (rechazo fecha via caso de uso), criterio 7 (herencia de lineas), criterio 8 (saldo RP por vista). EXECUTE: conector readonly sin EXECUTE (Msg 229) -> GRANT EXECUTE al rol de verificacion o SELECT a la vista/fn equivalente, documentado.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=reimplementacion, 3=DML directo, 5=paridad, 9=fuera de alcance -- NO anular, NO tocar 11/12) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Fecha del RP anterior al CDP no detectada (B-01/RN-10) | RP inconsistente con su respaldo | Restriccion 6c: validacion en caso de uso; solicitar elevar al proc |
| Aprobar copiando filas sin el proc | Rompe la regla de oro 50115 y la herencia del CDP | Restriccion 6a/6b; el adversarial verifica approve == invocar el proc |
| Reimplementar el saldo del CDP/RP en C# | Divergencia silenciosa con la BD | Prohibido (6a/6f); el adversarial lo busca (punto 2) |
| Imputar combinacion que el CDP no trae | Compromiso sin respaldo | RN-02/THROW 50114; herencia estricta (6b) |
| Tentacion de anular el RP (B-02) | Fuera de alcance; sin proc de anulacion | Campo 4 lo excluye; el adversarial verifica (punto 9) |
| Objeto/SECOP con centinelas magicos legacy ('0') | Datos sin significado de dominio | Restriccion 6d: defaults documentados, no centinelas -99/'0' |

## 10. Prioridad definida
**GOAL-P3** (drafts y aprobaciones Budget), brazo GOBERNADO, familia P3 (P3.3). Elegible al pool Q4 (criticidad
media) si su DEC esta cerrada al sello Etapa 2. Severidad s.08: segundo eslabon de la cadena de gasto (el RP es el
techo de la obligacion). Dependencias: GOAL-P1 (fundacion) + CDP operable (P3.2, el RP vive dentro de un CDP con
saldo). NO depende de brecha de BD para el camino feliz (el proc y el 50115 existen y estan verificados); B-01/B-02
se compensan/excluyen y se registran como hardening. Desbloquea: Obligation Draft (Doc 06, se expide con cargo a
un RP).
