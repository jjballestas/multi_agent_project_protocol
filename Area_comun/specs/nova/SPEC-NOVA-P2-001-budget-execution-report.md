# SPEC-NOVA-P2-001 - Reporte de ejecucion presupuestal (Get_Budget_Execution_Report) [miembro BASELINE ANCLADO de PAR-D, spec_prepagado]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo BASELINE, PAR-D (ancla).
> PORTADA al hub desde el SPEC ya diligenciado NOVA_SPEC_Plantilla_Requisitos s.4 (spec_prepagado). Su fase SPEC
> se EXCLUYE del delta del estudio (spec_prepagado=true; NOVA_ESTUDIO_Particion s.2.1). Preparada por el Arquitecto
> (arq+docs), FUERA de la ventana medida; el dev MEDIDO de P2.2 NO abre pre-sello.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P2-001 - task_id (hub): TASK-VISION-NOVA (prep P2, post-sello)
- owner_maker: agente desarrollador de la instancia (Sprint 1 baseline); repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial, nunca
  self-review; DIRECTIVA operador 2026-07-04). En el brazo BASELINE el checker vivo ES el adversarial informal
  (NO el checker formal del Analista; checker_formal=0). tokens_adversarial_informal se taggea a esa sesion separada.
- arm: baseline - unit: P2.2 reporte de ejecucion presupuestal (`Get_Budget_Execution_Report`), miembro ANCLADO de PAR-D
- q4_membership: **FUERA** (unidad baseline mandada por el GOAL, no del pool causal Q4). spec_prepagado=true.
- isolation: PAR-D. Este es el miembro BASELINE anclado; su pareja GOBERNADA es SPEC-NOVA-P2-004 (Get_*_List de
  BR-C3, listados por documento). REGLA DURA: esta SPEC cubre EXCLUSIVAMENTE el REPORTE DE EJECUCION AGREGADO
  (`Get_Budget_Execution_Report`/`fn_Budget_Execution_Report`); los listados por documento son territorio de P2-004.
  La comparacion PAR-D usa SOLO fases post-SPEC (spec_prepagado). No se reusa contenido de P2-004.
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> el brazo baseline y su pareja
  gobernada deben correr con el MISMO tipo de sesion/runtime (dinamica de cache comparable) o declarar el confound;
  captura de tokens = leer el `err.log` (stderr) de la sesion (hallazgo del piloto GOAL-P1); desglose por cubeta no
  capturable -> tokens_total_atribuibles como moneda. checker_formal=0, coordinacion_gobierno=0 (baseline).
- **deuda GOAL-P1 (bloqueante de front P2):** el harness de test del front de Nova-Budget (apps/nova-web) debe
  existir y correr VERDE en clon limpio ANTES de esta unidad si toca UI (evita gate falso-verde tipo TASK-0209).
- db_verified_at: objetos de NOVA-PRES-11 (BD DbsFinanciero readonly 2026-07-02/03; `Get_Budget_Execution_Report`,
  `fn_Budget_Execution_Report` verificados existentes); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025
  via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto obtiene el REPORTE DE EJECUCION PRESUPUESTAL agregado (apropiacion, CDP, compromiso,
obligacion, pago y saldos escalonados por rubro) para una vigencia, parametrizado por los filtros legacy,
sirviendose EXCLUSIVAMENTE del contrato de lectura `Get_Budget_Execution_Report`, sin reimplementar saldos/formulas
en C#.
- Fuente: NOVA-PRES-11 s.3.1-s.3.2 (Get_Budget_Execution_Report, 15 params) + NOVA-GOAL-001 s.8/s.9.
- Calidad: falsable. Bien: "el reporte de vigencia 2026 con params por defecto devuelve exactamente 652 filas
  (467 con account_nature='expense': 229 mayores + 238 auxiliares), en paridad EXEC contra el proc".

## 2. Usuario objetivo definido
Rol **Consulta / Gestion de presupuesto** (solo lectura). Sin matriz de autorizacion por operacion (sin mutaciones);
supuesto temporal: usuario autenticado del modulo puede consultar. Es el usuario del REPORTE AGREGADO (distinto de
los LISTADOS por documento de P2-004).

## 3. Alcance definido
Un contrato de lectura agregado sobre la vigencia:
- **API:** `GET /api/budget/execution-report` -> `Budget.Get_Budget_Execution_Report` (15 parametros): tenant,
  vigencia (id o anio), fechas [default = vigencia completa], naturaleza, rango de rubros [estilo legacy], fuente,
  tipo de vigencia [sobre la vigencia EFECTIVA], seccion, grupo, incluir mayores/auxiliares, agrupar por fuente.
  Orden del resultset: codigo de rubro, mayor antes que auxiliar, fuente. Query params tipados 1:1 a los 15 params;
  DTO 1:1 con el resultset (sin columnas inventadas ni omitidas).
- Saldos escalonados (RN-03 de PRES-11): apropiacion vigente (RN-02) -> CDP -> compromiso -> obligacion -> pago.
- Una fila por vigencia EFECTIVA por rubro (RN-04): "2 Gastos" aparece en 1-Actual / 2-Reservas / 3-CxP; en
  vigencias 2/3 la reserva/CxP constituida cuenta como apropiacion inicial y vigente.

## 4. Fuera de alcance definido
- **LISTADOS POR DOCUMENTO** (`Get_*_List`, CDP/compromisos/obligaciones/pagos por documento): territorio GOBERNADO
  P2-004 (PAR-D) -> FUERA (aislamiento). Esta SPEC no los consume ni replica.
- **Drill-down / libro material** (`vw_Budget_Execution_Movement`, 23 cols): reservado B-01, SPEC separada.
- **Libro oficial** (`Get_Budget_Book`, saldos corridos, B-01 ALTA): SPEC separada.
- **Filtro por BPIN/proyecto/sector:** el proc HOY no filtra por proyecto (PRES-11 B-04); el filtro por BPIN es
  candidato a parametro de la fn -> queda FUERA (gap declarado, va al pipeline nova-hardening; NO se reimplementa
  en C#).
- Cualquier MUTACION (solo lectura) o reimplementacion de saldos/formulas en C# (RN-09).

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; verificados existentes al sello):**
  - `Budget.Get_Budget_Execution_Report` -- el CONTRATO que llama la API (15 params). SIN THROW (lectura;
    vigencia inexistente = 0 filas en silencio).
  - `Budget.fn_Budget_Execution_Report` -- funcion inline, 50 columnas (verificada contra sys.columns);
    backend-only para filtros compuestos; la app llama el PROC, no la fn.
  - Vistas de verificacion de formula (criterio 4): `Budget.vw_Initial_Budget_Line_Balance` + las `*_Balance` (9);
    para acarreo: `Budget.vw_Carryover_Appropriation`. Anios cerrados: `Budget.Execution_Closing_Snapshot`
    (RN-07 inmutabilidad post-cierre; vigencia 2026 se sirve del snapshot).
- **API:** `GET /api/budget/execution-report` con los 15 filtros como query params; ProblemDetails en params
  invalidos; DTO 1:1 con el resultset del proc.
- **UI (apps/nova-web):** grilla del reporte con panel de filtros (15), vigencia explicita, presentacion en miles
  (capa de presentacion, RN-09); en vigencias cerradas el reporte viene del snapshot.
- **Capa Application:** `NOVA.Application/Budget/ExecutionReport/` (GetBudgetExecutionReport: mapea filtros -> 15
  params del proc/gateway tipado).
- **Referencias:** NOVA-PRES-11 (s.3.1 proc, s.3.2 paridad, s.4 RN-01..RN-09, s.6 B-04), NOVA-PRES-02 (formula de
  apropiacion vigente), NOVA-PRES-09 (cierre/snapshot), NOVA-GOAL-001 (GOAL-P2). (NO se referencia P2-004 / los
  listados por documento -- aislamiento PAR-D.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa saldos/formulas/
  numeracion; casos de uso -> gateways tipados; cero DataTable) + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) Solo LECTURA via `Get_Budget_Execution_Report`; jamas DML ni SELECT ad-hoc a tablas de linea; la logica de
    saldo vive en el proc/vistas (RN-02/RN-03), la app NO la recalcula (RN-09, "pecado capital del ambito").
  - (b) **AISLAMIENTO PAR-D:** NO consumir ni referenciar `Get_*_List` / los listados por documento (territorio
    gobernado P2-004); esta unidad es el REPORTE AGREGADO.
  - (c) DTO 1:1 con el resultset del proc (50 cols de la fn subyacente; sin inventar/omitir); orden del proc
    respetado (codigo, mayor-antes-auxiliar, fuente).
  - (d) Vigencia EFECTIVA (RN-04): una fila por (vigencia efectiva, rubro); tipo de vigencia = parametro.
  - (e) ProblemDetails en params invalidos (validacion de aplicacion); vigencia inexistente -> 200 con resultset
    vacio (el proc no lanza; NO convertir en 400).
  - (f) Correlation id + task_id en cada consulta (observabilidad; regla 8/DoD).
  - (g) BPIN/proyecto NO se filtra en C# (gap del proc, B-04): si se pide, va a hardening, no se parchea.

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **Dado** vigencia 2026 con params por defecto, **cuando** consulto, **entonces** el reporte devuelve **652 filas**
   en PARIDAD EXEC contra `Get_Budget_Execution_Report` (comparacion automatizada fila/total).
2. **Dado** vigencia 2026 con `account_nature='expense'`, **entonces** **467 filas** (229 mayores + 238 auxiliares).
3. **Dado** el rubro "2 Gastos", **entonces** aparece una fila por vigencia efectiva (1-Actual / 2-Reservas / 3-CxP),
   RN-04; en 2/3 la reserva/CxP constituida cuenta como apropiacion inicial y vigente.
4. **Dado** cualquier fila, **entonces** apropiacion vigente y saldos escalonados coinciden con
   `vw_Initial_Budget_Line_Balance`/`*_Balance` (verificacion de formula RN-02/RN-03, sin recalculo en C#).
5. **Dado** params invalidos (rango de rubros mal formado), **entonces** 400 ProblemDetails; vigencia inexistente ->
   200 con resultset vacio (el proc no lanza).
6. **Dado** el reporte, **entonces** NO invoca `Get_*_List` ni los listados por documento (verificable en el diff;
   aislamiento PAR-D).
7. **Dado** un resultset grande, **entonces** paginacion/orden en servidor sobre el resultset del proc, sin
   re-consulta SQL propia (RN-09).

## 8. Pruebas / gates definidos
- **Unit:** mapeo filtros -> 15 params del proc; validacion de params -> ProblemDetails; mapeo resultset -> DTO 1:1.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; Mcp sin SQL; cero DataTable; **test de
  aislamiento: ningun proyecto de esta unidad referencia `Get_*_List`** (criterio 6).
- **Integracion vs DbsFinanciero:** criterio 1 (652 filas paridad EXEC), criterio 2 (467/229/238), criterio 3
  (RN-04 por vigencia efectiva), criterio 4 (formula vs `*_Balance`), criterio 5 (400 vs 200-vacio). EXECUTE: el
  conector readonly (`nova_sql_connector_readonly_s9`) tiene SELECT/VIEW DEFINITION pero NO EXECUTE (Msg 229 al
  ejecutar el proc) -> para la paridad EXEC: GRANT EXECUTE del `Get_*` de lectura al rol de verificacion, O SELECT
  directo contra `fn_Budget_Execution_Report` con los mismos params como camino equivalente (documentar cual).
- **Gate final:** APROBADO del **adversarial informal de 12 puntos en SESION SEPARADA / contexto limpio** (checker
  vivo del brazo baseline; dev != adversarial; tokens_adversarial_informal taggeados a esa sesion) + arch tests +
  CI verde + DoD de NOVA-GOAL-001 con evidencia real (paridad 652, ProblemDetails provocado, OpenAPI) + verde de
  gates del hub + atestacion sha256. checker_formal=0 (baseline; el gate FORMAL del Analista NO aplica al codigo de
  esta unidad baseline).

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Reimplementar apropiacion vigente/saldos en C# | Divergencia con la BD (RN-09, pecado capital) | Restriccion 6a; adversarial punto 2; paridad EXEC 652 + formula vs `*_Balance` |
| Consumir/replicar los listados por documento (P2-004) | Contaminacion intra-par PAR-D | Restriccion 6b; architecture test de aislamiento (criterio 6); manifiesto |
| Filtrar por BPIN en C# (gap B-04) | Regla fuera del proc reimplementada | Restriccion 6g: gap a hardening, no se parchea |
| Convertir vigencia-inexistente en 400 | Contrato de lectura incorrecto | Restriccion 6e: 200 vacio (el proc no lanza) |
| DTO que inventa/omite columnas de las 50 | Contrato inestable | Restriccion 6c: DTO 1:1 |
| adversarial en la misma sesion del maker | Contaminacion del brazo (tokens no separables) | DoR: adversarial en SESION SEPARADA (DIRECTIVA operador) |

## 10. Prioridad definida
**GOAL-P2** (read model / reporte), brazo BASELINE, miembro ANCLADO de **PAR-D**. **Pertenencia Q4: FUERA**
(unidad baseline mandada por el GOAL; spec_prepagado). Severidad s.08: superficie de lectura agregada (el reporte
oficial de ejecucion). Dependencias: GOAL-P1 (fundacion) + `Get_Budget_Execution_Report` (existe, verificado al
sello) + el snapshot de cierre para vigencia 2026. **AISLAMIENTO PAR-D:** su fase SPEC se excluye del delta
(spec_prepagado); NO se leyo la fuente gobernada P2-004; los listados por documento quedan fuera. Activa la paridad
DbsFinanciero vs SNJDC. Desbloquea: el reporte de ejecucion, base de la operacion de consulta.
