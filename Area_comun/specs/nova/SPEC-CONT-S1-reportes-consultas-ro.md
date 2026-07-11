# SPEC-CONT-S1 - Reportes y consultas de solo lectura de Contabilidad (Slice 1, RO)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro del kit SPEC-CONT (ver
> SPEC-CONT-000-index). Slice de SOLO LECTURA: estados financieros, libros, comprobantes, saldos y certificados.
> Los procs de reporte YA EXISTEN (hardening del DBA, desplegados+verificados en las 3 BD); esta SPEC cubre SOLO la
> superficie C#/API(+UI) sobre esos procs/vistas. PREP de Sprint 1 (DIRECTIVA Operador 2026-07-11, "escribir NO
> construir"): NO se implementa antes del 30-jul. Fuente: WS1 Slice 1 + seccion D (F-NOVA-01, 2026-07-10) +
> patron congelado NOVA-SPEC-T-001 (SPEC-NOVA-P4-006, P2-001/002 read-model).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-CONT-S1 - task_id (hub/instancia): asignado al registrar la tarea de superficie (Sprint 1,
  post-30-jul; NO registrar `ready`/GO antes -- linea roja pool Q4/gobernado).
- owner_maker: agente desarrollador de la instancia gobernada (Contabilidad); repo producto Nova-Contabilidad.
- checker: **Analista (adversarial FORMAL, contexto limpio, estructuralmente independiente: SPEC + diff + BD
  readonly, NO la conversacion del maker)** + adversarial informal en sesion separada.
- arm / q4_membership / isolation: segun sorteo del sello si mide; RO -> criticidad de INTEGRIDAD baja, de
  CONFIDENCIALIDAD alta (aislamiento de tenant en lecturas, hallazgo #14). Si se mide como par, aislamiento CRITICO.
- **precondicion / preflight (F-NOVA-01, patron Presupuesto):** los 11 procs de reporte + `Get_Bank_Retention_
  Crossing_Report` EXISTEN y estan desplegados+verificados en las 3 BD; `GRANT EXECUTE` + `VIEW DEFINITION` +
  `SELECT` sobre las vistas/objetos leidos concedidos al rol verifier; set REAL de THROW capturado (seccion D).
- **F-NOVA-01 (set REAL, seccion D WS1, re-verificado 2026-07-10, identico en las 3 BD):**
  - `Get_Account_Monthly_Accumulated_Balance_Report` 52700-52707 · `Get_Auxiliary_Ledger_Report` 52800-52810 ·
    `Get_General_Ledger_Report` 52900-52908 · `Get_Daily_Book_Report` 53000-53005 · `Get_Balance_Annex_Report`
    53100-53110 · `Get_Daily_Voucher_Report` 53200-53206 · `Get_Trial_Balance_Report` 53300-53306 ·
    `Get_Financial_Position_Statement_Report` 53400-53406 · `Get_Income_Statement_Report` 53500-53506 ·
    `Get_Equity_Changes_Statement_Report` 53600-53607 (**divergencia real: extra `53607`** frente al primer pase
    53600-53606) · `Get_Withholding_Certificate_Report` 53700-53708 · `Get_Bank_Retention_Crossing_Report`
    (MODELADO) 51000-51004.
  - El maker RE-CONFIRMA cada set contra `OBJECT_DEFINITION` del proc DESPLEGADO al construir; los codigos de
    arriba son el punto de partida real, no un rango sin base.
- **guard de procedencia:** evidencia F-NOVA-01 con clase SQL real gateada por env vars, NA limpio sin
  credenciales; NINGUN mock/`Recording*` la sustituye (precedente TASK-0250/0253).
- **diseno de autorizacion (real, no supuesto DD-01):** los endpoints RO exigen autenticacion + rol de consulta
  contable via `[Authorize]`/`RequireAuthorization` real; sin sesion/rol valido -> 401/403 antes de tocar el
  proc/gateway. (Hereda el patron real de P4-006 s.6h.)
- **measurement:** captura de tokens en err.log; checker_formal cuenta; separar tokens_adversarial_informal de
  tokens_checker_formal.
- db_verified_at: procs de reporte verificados por el DBA en las 3 BD (seccion D WS1). El maker RE-VERIFICA contra
  la BD desplegada (F-NOVA-01) el set exacto de THROW y los nombres exactos de columnas de cada result-set.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET en capas + NOVA.Mcp / SQL Server via
  gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en `.config`, centinelas -99.

## 1. Objetivo definido
El usuario CONSULTA (solo lectura) el estado contable -- estados financieros (Prueba/Posicion/Resultados/Cambios en
patrimonio), libros (Auxiliar/Mayor/Diario), comprobantes, anexos de balance, saldos por cuenta/nivel/periodo y
certificados de retencion -- mediante llamadas a los procs/vistas de reporte YA existentes, expuestos como
endpoints RO tipados. La superficie C# NO calcula saldos ni mayoriza ni recalcula acumulados: el proc/vista lo hace
"a la fecha de corte"; C# solo mapea parametros -> proc y result-set -> DTO.
- Fuente: WS1 Slice 1 + seccion D; NOVA-PRES read-model (P2-001/002) para el patron de consulta.
- Calidad: falsable. Bien: "pedir el Libro Mayor con una cuenta inexistente devuelve ProblemDetails del THROW real
  del proc (dentro de 52900-52908, RE-CONFIRMAR cual) y ningun dato; y un llamador del tenant A que pide saldos de
  lineas del tenant B por sus IDs NO recibe datos de B".

## 2. Usuario objetivo definido
Rol **Consulta contable** (autenticado). Visualiza reportes por fecha de corte / cuenta / nivel / tercero /
vigencia. A diferencia del baseline DD-01, el rol se VERIFICA realmente (s.6e). No muta nada.

## 3. Alcance definido
Un conjunto de endpoints RO, uno por reporte de la seccion D, cada uno superficie sobre su proc/vista:
- 11 reportes `Get_*_Report` (estados financieros, libros, comprobantes, anexo, saldos acumulados, certificados de
  retencion) + consultas por vista (`vw_Voucher`/`vw_Voucher_Line`, `vw_Accounting_Source`, `fn_Account_Balance_
  For_Period`).
- `Get_Bank_Retention_Crossing_Report` (MODELADO): queda como REPORTE (51000-51004), NUNCA como asiento
  `withholding_crossing` (decision de dominio del WS1 A; no operacionalizar en esta tanda).
- Cada endpoint: valida/mapea parametros, invoca el proc/vista, mapea result-set -> DTO 1:1, traduce THROW ->
  ProblemDetails. Aislamiento de tenant DEMOSTRABLE en cada lectura (s.6d).

## 4. Fuera de alcance definido
- **Mutacion de comprobantes** (captura/correccion -> SPEC-CONT-S2), **cierre/apertura** (S3), **saldos iniciales**
  (S4), **CHIP** (S5), **informe trimestral CGN/CHIP** (S6A), **cierre anual** (S6B), **causacion de ingresos**
  (S6C, frontera del modulo fuente): FUERA.
- **Reproducir `Mayorizar`/`Grabar Temporales`/`Copia de Comprobantes`** (formularios legacy RETIRADOS en WS1: los
  reportes mayorizan a la fecha de corte; los automaticos contabilizan definitivo; correccion = nuevo comprobante):
  NO se reproducen.
- **Operacionalizar el cruce de retenciones como asiento** (`withholding_crossing`): FUERA (decision futura, WS1 A).
- **Construir/modificar los procs/vistas de reporte:** ya existen; esta unidad SOLO consume el contrato.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; F-NOVA-01):** los 11 procs `Get_*_Report` + `Get_Bank_Retention_
  Crossing_Report` + `fn_Account_Balance_For_Period` + vistas `vw_Voucher`/`vw_Voucher_Line`/`vw_Accounting_Source`.
  Firma EXACTA (parametros, tipos) y nombres EXACTOS de columnas del result-set: el maker los extrae de
  `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO, no los asume.
- **THROW:** el set REAL de la seccion D (arriba, DoR). El maker mapea cada codigo a su regla (parametro invalido,
  rango de fechas invalido, cuenta/nivel inexistente, tenant faltante, etc.) confirmando el texto real del proc.
- **API:** un `GET /api/accounting/reports/<reporte>` por reporte (query params tipados); ProblemDetails por THROW;
  devuelve el DTO del reporte. Todos bajo `[Authorize]` con rol de consulta contable (s.6e).
- **UI (apps/nova-web):** pantallas de consulta (seleccion de reporte + parametros + fecha de corte); render del
  reporte; muestra ProblemDetails si el proc rechaza o si falta rol.
- **Capa Application:** `NOVA.Application/Accounting/Reports/` (mapea la solicitud, traduce THROW; NO recalcula
  saldos/acumulados).
- **Referencias:** WS1 Slice 1 + seccion D; NOVA-PRES read-model P2-001/002 (patron de consulta RO); patron
  congelado NOVA-SPEC-T-001.

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no recalcula saldos/acumulados;
  gateways tipados; cero DataTable) + stack + preambulo compartido del kit (SPEC-CONT-000).
- Propias:
  - (a) **SOLO LECTURA:** jamas DML; ninguna llamada muta estado. (Si un reporte requiere `sp_set_session_context`
    para tenant, es lectura de contexto, no mutacion de negocio.)
  - (b) **C# NO recalcula saldos/acumulados/mayorizacion:** el proc/vista los produce a la fecha de corte; C# mapea
    result-set -> DTO. Verificable en el diff (sin aritmetica de saldos en la capa Application).
  - (c) DTOs 1:1; THROW -> ProblemDetails, cada codigo ALCANZABLE re-verificado; correlation-id/task_id + usuario
    real (del contexto de auth) en el log de la consulta.
  - (d) **AISLAMIENTO DE TENANT EN LECTURAS (hallazgo #14, seguridad ALTA -- el defecto exacto vivia en gateways de
    LECTURA):** toda query de reporte aisla por tenant de forma DEMOSTRABLE: (i) filtra explicitamente
    `WHERE tenant_id=@tenant_id` (u equivalente por celda), O (ii) la vista/RLS que consulta consume
    `SESSION_CONTEXT('tenant_id')` verificado contra `OBJECT_DEFINITION` de la vista + existencia de `SECURITY
    POLICY`. NO basta `sp_set_session_context('tenant_id')` ANTES de la query si el objeto leido NO lo consume. Si
    una vista no expone `tenant_id` ni tiene RLS, el fix exige cambiar la vista/camino de lectura o cablear RLS (se
    decide con el DBA); la unidad lo cablea desde el inicio.
  - (e) **AUTORIZACION REAL:** cada endpoint RO exige `[Authorize]`/`RequireAuthorization` con rol de consulta
    contable real; sin sesion/rol valido -> 401/403 antes de tocar el gateway/proc. Test de arquitectura mecanico:
    el endpoint tiene el atributo/policy presente (falla si se remueve).
  - (f) **GUARD DE PROCEDENCIA:** el harness F-NOVA-01 usa una clase SQL real, gateada por env vars, NA limpio sin
    credenciales; jamas un mock/`Recording*` in-memory.
  - (g) **LECTURA DE RESULT-SET SIN ADIVINANZA (hallazgo #11):** el gateway lee cada columna por el nombre EXACTO
    confirmado contra `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set`; sin fallback encadenado de
    nombres ni default silencioso; el harness F-NOVA-01 ejercita el MISMO camino de lectura que produccion.
  - (h) **COBERTURA HTTP DE INTEGRACION (hallazgo #12):** cada endpoint de reporte tiene >=1 test de integracion
    HTTP (`WebApplicationFactory` + gateway FALSO inyectado) que ejercita ruta -> endpoint -> mapeo -> gateway.
  - (i) **LISTA DE AISLAMIENTO DEL FRONTEND (hallazgo #13):** el test `React_app_does_not_contain_sql_or_procedure_
    calls` incluye los nombres exactos de los procs de reporte en la lista de literales prohibidos del frontend; si
    un nombre se exhibe como texto descriptivo en la UI, es EXCEPCION explicita documentada, no omision silenciosa.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW real (seccion D) re-confirmado contra `OBJECT_DEFINITION`.
1. **Dado** parametros validos y un usuario CON rol de consulta, **cuando** pide un reporte (p.ej. Libro Mayor a
   una fecha de corte), **entonces** recibe el DTO con los datos que el proc/vista produce a esa fecha, sin que C#
   recalcule saldos (verificable en el diff).
2. **Dado** un parametro invalido (p.ej. rango de fechas invalido o cuenta inexistente), **entonces** ProblemDetails
   del THROW real del proc (dentro del set de la seccion D del reporte, RE-CONFIRMAR cual) y ningun dato.
3. **Dado** una consulta sin `SESSION_CONTEXT('tenant_id')`, **entonces** ProblemDetails del THROW de tenant
   faltante (RE-VERIFICAR el numero exacto por proc).
4. **Dado** dos tenants A y B con datos, **cuando** un llamador del tenant A pide saldos/reportes de lineas del
   tenant B por sus IDs, **entonces** el gateway NO devuelve datos de B (query filtra tenant o la vista/RLS lo
   enforcea, verificado contra `OBJECT_DEFINITION`). Una lectura que solo hace `sp_set_session_context` pero
   consulta un objeto que no lo consume FALLA este criterio (hallazgo #14). Harness con caso NEGATIVO cross-tenant.
5. **Dado** un usuario SIN rol de consulta (o sin autenticar), **cuando** pide cualquier reporte, **entonces** la
   API responde 401/403 y el proc NUNCA se invoca (cero llamadas al gateway).
6. **Dado** el gateway de produccion, **entonces** lee cada columna por el nombre EXACTO confirmado contra
   `OBJECT_DEFINITION`, sin fallback ni default silencioso; el harness F-NOVA-01 ejercita el MISMO camino (#11).
7. **Dado** cada endpoint de reporte, **entonces** tiene >=1 test de integracion HTTP (`WebApplicationFactory` +
   gateway falso) que verifica el wiring ruta->endpoint->gateway (#12).
8. **Dado** el harness F-NOVA-01, **entonces** usa una clase SQL real (gateada por env, NA limpio) -- sin mock/
   `Recording*` sustituyendo la evidencia.
9. **Dado** el test de aislamiento del frontend, **entonces** incluye los nombres de los procs de reporte en la
   lista de literales prohibidos; excepciones (texto descriptivo en UI) documentadas, no omitidas (#13).
10. **Dado** `Get_Bank_Retention_Crossing_Report`, **entonces** se expone SOLO como reporte (51000-51004); NO existe
    endpoint ni comando que lo convierta en asiento `withholding_crossing` (decision de dominio WS1 A).

## 8. Pruebas / gates definidos
- **Unit:** mapeo de parametros; traduccion THROW->ProblemDetails; enforcement de que saldos/acumulados NO se
  recalculan en C#; verificacion de policy de autorizacion presente.
- **Architecture tests:** Api sin SQL directo; React sin SQL (con la lista de procs de reporte, #13); Mcp sin SQL;
  cero DataTable; test de autorizacion (endpoints RO con `[Authorize]`/policy presente).
- **Integracion vs DbsFinanciero_SANDBOX (EXECUTE via GRANT):** criterio 1 (happy, datos por fecha de corte), un
  caso por THROW ALCANZABLE (parametro invalido, tenant faltante) RE-VERIFICADO contra `OBJECT_DEFINITION`, criterio
  4 (negativo cross-tenant), criterio 5 (401/403 sin rol).
- **Gate final:** APROBADO del checker FORMAL del Analista (contexto limpio) + adversarial informal en sesion
  separada + arch tests + CI + F-NOVA-01 (cada THROW verificado contra el proc desplegado) + guard de procedencia
  (SQL real, sin mock) + aislamiento de tenant demostrado (caso negativo) + autorizacion real + DoD con evidencia
  real + gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Recalcular saldos/acumulados/mayorizacion en C# en vez de leer el proc/vista a la fecha de corte | Divergencia con la BD; reporte incorrecto no cazado | Restriccion 6b + criterio 1; adversarial y checker formal verifican el diff |
| Fuga de tenant en lecturas: `sp_set_session_context` ANTES de consultar una vista que NO consume el contexto ni tiene RLS (el defecto exacto del baseline) | Saldos/reportes enumerables cross-tenant por IDs (confidencialidad ALTA) | Restriccion 6d + criterio 4 (negativo cross-tenant explicito, verificado contra OBJECT_DEFINITION de la vista) |
| Asumir el set de THROW o los nombres de columna sin re-confirmar contra el proc desplegado | Criterio falso; THROW no alcanzable; lectura por adivinanza (#11) | F-NOVA-01: RE-CONFIRMAR set REAL (seccion D) + nombres exactos de columna antes de fijar criterios; restriccion 6g |
| Mock/fixture in-memory disfrazado de evidencia F-NOVA-01 real | Falso-verde no detectado (TASK-0250/0253) | Guard de procedencia (6f): clase SQL real, sin credenciales; checker formal + adversarial |
| Autorizacion decorativa sin verificacion real de rol (repetir gap #5/#8 del baseline) | Reportes accesibles sin rol | Restriccion 6e + criterio 5 + test de arquitectura mecanico |
| Operacionalizar el cruce de retenciones como asiento "de paso" | Rompe la decision de dominio del WS1 (queda como reporte) | Criterio 10 + alcance s.3/s.4 |
| Divergencia real ignorada: `Get_Equity_Changes_Statement_Report` tiene `53607` extra vs primer pase | THROW alcanzable no mapeado | F-NOVA-01 re-confirma el set 53600-53607 completo; el maker mapea `53607` |

## 10. Prioridad definida
**GOAL lectura de Contabilidad** (primer slice del kit SPEC-CONT). Pertenencia Q4: segun sorteo del sello si mide
(RO -> criticidad de confidencialidad por el aislamiento de tenant). Severidad: solo lectura (sin mutacion), pero
la fuga de tenant en lecturas es un riesgo de seguridad ALTO (hallazgo #14). Dependencias: procs/vistas de reporte
(existen, verificados por el DBA, seccion D) + patron congelado NOVA-SPEC-T-001 + diseno de autorizacion real
(s.6e). **LINEA ROJA: esta unidad NO SE CONSTRUYE antes del 30-jul** (pool Q4/gobernado); esta SPEC es DISENO/PREP
unicamente. Desbloquea: la capa de consulta del modulo Contabilidad en Sprint 1 (base para que S2-S6 muestren
estado antes/despues de mutar).
