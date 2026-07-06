# SPEC-NOVA-P3-001 - Initial Budget Draft (crear / capturar / aprobar)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, familia P3, primera
> unidad (alcance congelado). Generada desde NOVA-PRES-02 (Presupuesto Inicial) + NOVA-GOAL-001 + arquitectura.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P3-001
- task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, estructuralmente independiente; recibe SPEC + diff + BD readonly, NO la conversacion del maker)
- arm: gobernado - family: P3 - unit: P3.1 (alcance CONGELADO, no se redefine sin enmienda fechada del Operador)
- q4_membership: **FUERA** (primera unidad de la familia, alcance congelado; NO enumerada en el pool Q4 del estudio -- es el opener del brazo gobernado, no item del contraste causal Q4)
- isolation: sin hermano baseline (familia P3 es gobernada completa); igual se declara manifiesto de archivos leidos + columna leyo_codigo_hermano = NO
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: la SPEC cita objetos verificados en NOVA-PRES-02 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada al construir (OBJECT_DEFINITION/sys.objects) -- ver F-NOVA-01
- throw_source (verificado OBJECT_DEFINITION + PRES-02 s.4): **PROC-DIRECTO** `Approve_Initial_Budget_Draft` = 50270-50278 (cuadre por fuente = 50277) [confirmado en OBJECT_DEFINITION por el Analista]. **TRIGGER/CHECK durante la transaccion** (NO en la def directa del proc; fuente = triggers de Initial_Budget/_Draft(_Line) per PRES-02 s.4): 50054 (catalogo doc soporte), 50057/50059 (vigencia), 50058/50062 (solo auxiliares), 50060/50061 (naturaleza ingreso/gasto). Estos disparan durante la captura/insert, no desde el Approve_*.
- **NOTA F-NOVA-01 (mapeo incompleto, hardening pass 2026-07-06):** de los 9 codigos del rango
  PROC-DIRECTO 50270-50278 solo 50277 (cuadre) esta mapeado a una regla de negocio verificable con
  criterio de aceptacion propio. El maker DEBE mapear/RE-CONFIRMAR el resto (50270-50276, 50278) contra
  `OBJECT_DEFINITION` antes de fijar los criterios finales; si algun codigo resulta inalcanzable desde
  el flujo de esta SPEC, declararlo explicitamente (no dejarlo huerfano).
- attestation: sha256 de esta SPEC atestado via intent del hub en el gate del estudio
- stack (obligatorio, F-NOVA-03): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas NOVA.Api/Application/Domain/Infrastructure/Contracts + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados (EF Core/Dapper) / OpenTelemetry / errores de negocio = ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales/HintPath, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto crea el acto administrativo del presupuesto inicial de una vigencia, captura su borrador
recuperable (ingresos aforados y gastos apropiados por rubro auxiliar x fuente, con equilibrio por fuente) y lo
APRUEBA materializando el detalle definitivo inmutable, sirviendose EXCLUSIVAMENTE del procedimiento controlado
`Budget.Approve_Initial_Budget_Draft` -- sin copiar filas ni recalcular saldos en C#.
- Fuente: NOVA-PRES-02 s.1 (Proposito) + s.5 (Contrato) + GOAL-P3 (Initial Budget Draft: crear/editar/aprobar).
- Calidad: falsable. Bien: "aprobar un borrador cuadrado por fuente materializa N lineas definitivas via el proc y sella usuario/fecha; un borrador descuadrado es rechazado con THROW 50277".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto** (secretaria de hacienda): captura y edita el borrador (draft), lo marca
ready_to_approve y ejecuta la aprobacion. La matriz de autorizacion por operacion aun NO esta sembrada en BD
(brecha NOVA-PRES-001 s.6 B-05; maestro s.08-C: emitir != aprobar != anular). CONFIRMADO por el Operador (DD-01),
aceptado para Sprint 1: cualquier usuario autenticado del modulo con rol presupuesto puede capturar y aprobar;
policy por operacion via BR-C4 CONFIRMADA post-Sprint-1.

## 3. Alcance definido
1. Crear la cabecera del acto (`Initial_Budget`) y su borrador (`Initial_Budget_Draft`) -> canal: DML tipado del gateway (NOVA-PRES-02 s.5 fila "Crear").
2. Capturar/editar lineas del borrador (`Initial_Budget_Draft_Line`, income/expense separados) mientras esta en `draft` -> canal: DML tipado (s.5 fila "Capturar/editar").
3. Transicion de estado `draft -> ready_to_approve` del borrador (maquina de estados; sin atajos).
4. Aprobar el borrador -> canal UNICO: `Budget.Approve_Initial_Budget_Draft` (s.5 fila "Aprobar"; RN-06 cuadre por fuente; copia a `Initial_Budget_Line`; sella usuario/fecha).
5. Descartar/retirar un borrador -> estado `discarded` (nunca DELETE) (s.5 fila "Anular/retirar").
6. Lectura de acto, borrador, cuadre por fuente y apropiacion vigente -> vistas (s.5 fila "Leer").

## 4. Fuera de alcance definido
- Modificaciones (adicion/reduccion/traslado): `Budget.Apply_Budget_Modification`, ambito Doc 03 (SPEC separada).
- Aplazamientos/desaplazamientos: brecha NOVA-PRES-02 s.6 B-03 (ningun proc los alimenta hoy) -> NO se implementan; si el municipio los usa, van por hardening/Doc 03.
- Correccion de `is_current` y arranque real 2027: NOVA-PRES-02 s.6 B-02 (item de hardening/datos, ALTA) -> fuera; la SPEC solo exige vigencia explicita (ver campo 6).
- Cierre/liquidacion de vigencia: `Close_Fiscal_Year`, Doc 09.
- Contabilidad de la aprobacion: RN-12 -- la aprobacion NO genera asiento (norma CGN); prohibido replicar el tipo legacy '00'.
- Saneo del documento soporte UNKNWN de 2026 (B-05): operacion de dato, SPEC aparte.
- Cualquier acceso directo a tablas o reimplementacion de la formula de saldo (6 efectos) en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada antes de codificar):**
  - Tablas: `Budget.Initial_Budget`, `Initial_Budget_Draft`, `Initial_Budget_Draft_Line`, `Initial_Budget_Line`, `Initial_Budget_Line_Adjustment` (5 tablas, NOVA-PRES-02 s.3.1).
  - Proc de aprobacion: `Budget.Approve_Initial_Budget_Draft` (schema/142; THROW 50270-50278; transaccional bajo UPDLOCK/HOLDLOCK; valida RN-06 cuadre por fuente, copia lineas, sella).
  - Vistas: `vw_Initial_Budget`, `vw_Initial_Budget_Draft_Line`, `vw_Initial_Budget_Draft_Balance` (cuadre por fuente = ingreso-gasto=0), `vw_Initial_Budget_Line`, `vw_Initial_Budget_Line_Balance` (apropiacion vigente, 6 efectos), `vw_Initial_Budget_Line_Adjustment`.
  - Catalogo: `budget_support_document_type` (01 Resolucion, 02 Acuerdo, 03 Decreto) -- THROW 50054.
- **API (crear en NOVA.Api, contratos en NOVA.Contracts):**
  - `POST /api/budget/initial-budget-drafts` (crea cabecera+borrador; body tipado; ProblemDetails).
  - `PUT/PATCH /api/budget/initial-budget-drafts/{id}/lines` (captura/edita lineas en estado draft).
  - `POST /api/budget/initial-budget-drafts/{id}/ready` (draft -> ready_to_approve).
  - `POST /api/budget/initial-budget-drafts/{id}/approve` (invoca `Approve_Initial_Budget_Draft`).
  - `POST /api/budget/initial-budget-drafts/{id}/discard`.
  - `GET` de lectura del acto/borrador/cuadre/apropiacion. DTOs 1:1 con los resultsets; sin columnas inventadas.
- **UI (apps/nova-web):** pantalla "Presupuesto inicial" -- captura de lineas (income/expense separados con bloqueo por naturaleza mostrado desde la BD, no por teclado), tablero de cuadre por fuente (`vw_Initial_Budget_Draft_Balance` visible), boton aprobar habilitado solo con cuadre exacto. Vigencia EXPLICITA (sin default, F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/InitialBudget/` (casos de uso: CreateInitialBudgetDraft, CaptureDraftLines, MarkReadyToApprove, ApproveInitialBudgetDraft, DiscardDraft, ReadAppropriation).
- **Referencias:** NOVA-PRES-02 (s.3-s.6), NOVA-PRES-000 s.03 (maestro-Pn) y s.08, dictionary/initial_budget, NOVA-GOAL-001 (GOAL-P3 + catalogo de APIs).

## 6. Restricciones tecnicas definidas
- Heredadas (citar): 10 reglas no negociables de NOVA-GOAL-001 (React nunca SQL; MCP/IA nunca SQL directo; C# no reimplementa reglas transaccionales SQL; casos de uso -> gateways tipados; cero DataTable entre capas; cero DLLs manuales a bin; errores de negocio = ProblemDetails; auditoria+usuario+fecha+correlation id en toda mutacion; cadenas fuente no se ajustan aisladas; documentacion curada al dia). Principios maestro-P1..P6 (NOVA-PRES-000 s.03). Stack del preambulo.
- Propias de la tarea:
  - (a) La APROBACION es SOLO `Budget.Approve_Initial_Budget_Draft`; ninguna superficie copia filas ni valida el cuadre por su cuenta (NOVA-PRES-02 s.5 "Regla operativa").
  - (b) La creacion/captura del borrador es DML tipado del gateway (no hay proc de create hoy); jamas SELECT/DML ad-hoc a tablas fuera del gateway tipado.
  - (c) El saldo/apropiacion vigente se LEE de `vw_Initial_Budget_Line_Balance` (formula 6 efectos); NUNCA se recalcula en C# ni se materializa en columna (RN-09).
  - (d) La UI pre-valida el cuadre con `vw_Initial_Budget_Draft_Balance` (mismos numeros que validara el proc); la pre-validacion NUNCA sustituye al proc.
  - (e) Bloqueo income/expense por naturaleza del rubro viene de la BD (THROW 50060/50061), no del teclado; solo rubros auxiliares (THROW 50058/50062).
  - (f) Vigencia SIEMPRE explicita en la UI (F-NOVA-05: is_current apunta a 2026 cerrada).
  - (g) Toda mutacion: correlation id + usuario real (no usuario tecnico compartido) + THROW traducido a ProblemDetails (codigo + mensaje de negocio + campo culpable si se conoce).
  - (h) **GUARD DE PROCEDENCIA:** el harness de evidencia F-NOVA-01 usa una clase SQL real, gateada
    por env vars, NA limpio sin credenciales -- jamas un mock/Recording* in-memory (precedente TASK-0253).
  - (i) **LECTURA DE RESULT-SET SIN ADIVINANZA (hereda P4-006):** el gateway de produccion NO debe leer
    columnas del result-set de `Approve_Initial_Budget_Draft` por fallback encadenado de nombres ni caer
    en un DEFAULT SILENCIOSO si la columna no aparece. El nombre EXACTO de cada columna se confirma
    contra `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de
    escribir el gateway; el harness F-NOVA-01 ejercita el MISMO camino de lectura que el gateway de
    produccion.
  - (j) **COBERTURA HTTP DE INTEGRACION (hereda P4-006):** cada endpoint mutador nuevo (ready/approve/
    discard) tiene al menos un test de integracion HTTP real (`WebApplicationFactory` + gateway FALSO
    inyectado) que ejercita ruta -> endpoint -> mapeo de comando -> gateway.
  - (k) **LISTA DE AISLAMIENTO COMPLETA (hereda P4-006):** el test de arquitectura de aislamiento del
    frontend (crear si no existe aun para la familia P3) incluye `Approve_Initial_Budget_Draft` en su
    lista de literales prohibidos. Exhibicion como texto descriptivo en UI = excepcion explicita
    documentada, nunca omision silenciosa.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un borrador con Sigma ingresos = Sigma gastos por CADA fuente, **cuando** apruebo, **entonces** `Approve_Initial_Budget_Draft` materializa las lineas en `Initial_Budget_Line`, marca el borrador `approved` y sella usuario/fecha; el conteo de lineas definitivas = lineas activas del borrador (RN-06/RN-07; ref NOVA-PRES-02 s.3.3: borrador 2026 cuadra $54.697.000.000 ingreso = gasto).
2. **Dado** un borrador DESCUADRADO en al menos una fuente, **cuando** intento aprobar, **entonces** la API responde ProblemDetails del THROW **50277** y no se materializa nada.
3. **Dado** una linea con rubro de naturaleza ingreso, **cuando** capturo `expense_amount>0`, **entonces** THROW **50061** (y simetrico **50060** para gasto con income); ProblemDetails.
4. **Dado** una linea con rubro **mayor** (no auxiliar), **cuando** la inserto, **entonces** THROW **50062** (borrador) / **50058** (definitivo).
5. **Dado** una linea con par rubro-fuente de OTRA vigencia que la cabecera, **cuando** la inserto, **entonces** THROW **50057/50059**.
6. **Dado** una cabecera con (vigencia, approval_code) ya existente o con tipo de documento soporte fuera del catalogo, **cuando** la creo, **entonces** violacion UNIQUE / THROW **50054**.
7. **Dado** un borrador ya `approved`, **cuando** intento editar `approved_amount`, **entonces** se rechaza (inmutabilidad RN-07; todo cambio posterior es ajuste via Doc 03).
8. **Dado** un segundo borrador editable activo para la misma cabecera, **cuando** lo creo, **entonces** violacion del indice unico filtrado (RN-02).
9. **Dado** cualquier lectura de apropiacion vigente, **entonces** el valor coincide con `vw_Initial_Budget_Line_Balance` (formula 6 efectos), sin recalculo en C# (muestreo automatizado, tolerancia 0.01).
10. **Dado** el gateway de produccion, **entonces** lee cada columna del result-set por el nombre EXACTO
    confirmado contra `OBJECT_DEFINITION`, sin fallback encadenado ni default silencioso; el harness
    F-NOVA-01 ejercita el MISMO camino de lectura.
11. **Dado** los endpoints mutadores (ready/approve/discard), **entonces** cada uno tiene al menos un test
    de integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica el wiring completo.

## 8. Pruebas / gates definidos
- **Unit (Domain/Application):** mapeo DTO->parametros del proc; maquina de estados draft/ready_to_approve/approved/discarded (transiciones validas e invalidas); traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain no depende de Infrastructure; Application no depende de ASP.NET; Api/Mcp sin SQL directo; cero DataTable en contratos.
- **Integracion contra DbsFinanciero (BD real):** criterio 1 (aprobacion happy: cuadre por fuente -> materializa), y un caso por THROW alcanzable (50277, 50060/50061, 50058/50062, 50057/50059, 50054); criterio 9 (paridad de apropiacion vista vs endpoint). Nota EXECUTE: el conector readonly no ejecuta procs (Msg 229) -> el gate de paridad exige GRANT EXECUTE al rol de verificacion o SELECT a la `fn_*`/vista equivalente, documentado.
- **Gate final:** veredicto APROBADO del Analista (checklist 12 puntos, enfasis en 2=reimplementacion prohibida, 3=DML directo, 4=cobertura THROW, 5=paridad) + guard de procedencia (evidencia SQL real, sin mock) + criterio 10 (lectura de columnas confirmada) + criterio 11 (test HTTP de integracion) + DoD de NOVA-GOAL-001 con evidencia real (tests, OpenAPI, sin SQL desde React/MCP, docs curadas) + verde de los gates del hub (validate/encoding/neutralidad) sobre la SPEC + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Recalcular cuadre/saldo en C# "para la UI" | Divergencia silenciosa con la BD (pecado capital del ambito) | Prohibido (restriccion 6c/6d); el adversarial lo busca (punto 2); pre-validacion solo con las vistas |
| Aprobar copiando filas sin el proc | Rompe la unica frontera transaccional | Restriccion 6a; el adversarial verifica que approve == invocar `Approve_Initial_Budget_Draft` |
| `is_current` apunta a 2026 cerrada (B-02) | Defaults de vigencia enganosos | Vigencia explicita en UI (6f); arranque 2027 y correccion de is_current = hardening, fuera de alcance |
| Matriz de autorizacion por operacion ausente (B-05) | emitir/aprobar sin separacion de permisos | Confirmado por el Operador para Sprint 1 (DD-01, campo 2): usuario autenticado con rol presupuesto captura/aprueba/emite; policy por operacion via BR-C4 post-Sprint-1 |
| Aplazamientos en el modelo pero sin proc (B-03) | Tentacion de "completarlo" en C# | Fuera de alcance explicito (campo 4); no se parchea en aplicacion |
| Skew GOAL vs BD (F-NOVA-01) | Declarar brecha inexistente | RE-verificar cada objeto contra la BD desplegada al construir (preambulo db_verified_at) |

## 10. Prioridad definida
**GOAL-P3** (drafts y aprobaciones Budget), brazo GOBERNADO, primera unidad de la familia P3 (alcance CONGELADO).
Severidad s.08: base de la cadena de gasto (el detalle aprobado es el techo de CDP/compromiso/obligacion/pago).
Dependencias: GOAL-P1 (fundacion tecnica: sln, capas, architecture tests, CI) terminada; NO depende de ninguna
brecha de BD abierta para el camino feliz (el proc existe y esta verificado, B-01 cerrada). Desbloquea: el resto
de la familia P3 (drafts de disponibilidad/compromiso/obligacion/pago reutilizan el patron aprobacion-via-proc) y
la validacion de techo de la cadena de gasto (Doc 04).
