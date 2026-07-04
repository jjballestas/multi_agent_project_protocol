# SPEC-NOVA-P2-004 - Get_*_List / Listados operativos por documento (BR-C3) [miembro GOBERNADO de PAR-D]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, pool Q4, PAR-D.
> Generada desde NOVA-PRES-11 (Ejecucion/Consultas s.5-s.6, brecha B-02/BR-C3) + NOVA-GOAL-001 + arquitectura.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P2-004 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly)
- arm: gobernado - unit: Get_*_List de BR-C3 (miembro GOBERNADO de PAR-D)
- q4_membership: **DENTRO** (criticidad BAJA por regla determinista; sobre vistas YA existentes; fabrica de tareas S)
- **isolation: CRITICA (PAR-D).** Este es el MIEMBRO GOBERNADO de PAR-D, cuya pareja es la unidad BASELINE **P2.2
  (reporte de ejecucion, `Get_Budget_Execution_Report`, spec_prepagado SPEC-NOVA-P2-001)**. REGLA DURA: esta SPEC
  cubre EXCLUSIVAMENTE los LISTADOS POR DOCUMENTO (Get_*_List sobre vistas de saldo existentes); el REPORTE DE
  EJECUCION AGREGADO (`Get_Budget_Execution_Report`/`fn_Budget_Execution_Report`) es TERRITORIO BASELINE (P2.2) y
  queda FUERA de alcance. Manifiesto de archivos leidos: NOVA-PRES-11 (doc de proceso COMPARTIDO) + arquitectura +
  GOAL. **NO se leyo el repo/implementacion de P2.2** (`leyo_codigo_hermano = NO`). NOTA DE INTEGRIDAD: SPEC-NOVA-
  P2-001 (el spec_prepagado de P2.2) aparece como EJEMPLO diligenciado dentro de la plantilla compartida
  NOVA_SPEC_Plantilla (s.4) -> exposicion INCIDENTAL via el doc del paquete, NO lectura de la fuente de la tarea
  baseline; esta SPEC no reusa su contenido ni su read model agregado. Su fase SPEC se excluye del delta (simetria
  con el spec_prepagado de P2.2, per NOVA_ESTUDIO_Particion s.2.2).
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: objetos de NOVA-PRES-11 (BD DbsFinanciero readonly 2026-07-03; las vistas de saldo se verificaron existentes via conector readonly en el sello); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01)
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto obtiene los LISTADOS OPERATIVOS por documento -- CDP sin comprometer, compromisos sin
obligar, obligaciones sin pagar, y pagos realizados con numero de egreso -- parametrizados por los filtros legacy
(tercero, fechas, rubros, fuente, uso, vigencia, con/sin saldo), sirviendose EXCLUSIVAMENTE de las vistas de saldo
que YA existen, sin reimplementar la logica en C# ni tocar el reporte de ejecucion agregado.
- Fuente: NOVA-PRES-11 s.1 (Listados operativos) + s.5 (fila "Listados con saldo") + s.6 B-02/BR-C3.
- Calidad: falsable. Bien: "el listado de CDP con `saldo>0` devuelve exactamente las filas de `vw_Availability_Certificate_Balance` con disponible positivo, filtradas por los parametros, con paridad contra la vista".

## 2. Usuario objetivo definido
Rol **Consulta / Gestion de presupuesto** (herramienta diaria del operador para encadenar la cadena de gasto): solo
lectura. No exige matriz de autorizacion por operacion (sin mutaciones); supuesto temporal: usuario autenticado del
modulo puede consultar. Simetrico al usuario del reporte de ejecucion pero para LISTADOS por documento.

## 3. Alcance definido
Familia de contratos de lectura `Get_*_List` (patron de `Get_Budget_Execution_Report`: proc con parametros tipados
sobre la vista canonica), UNO por documento de la cadena:
1. **CDP sin comprometer** -> sobre `vw_Availability_Certificate_Balance` (+ `_Line_`), disponible = valor +/- ajustes 08/09 - comprometido (equivale a PresLsDsp).
2. **Compromisos sin obligar** -> sobre `vw_Commitment_Balance`/`_Line_` (por obligar; equivale a PresLsCmp).
3. **Obligaciones sin pagar** -> sobre `vw_Obligation_Balance`/`_Line_` (por pagar, con/sin saldo; equivale a PresLsObl).
4. **Pagos realizados** -> sobre `treasury.Payment_Order_Budget_Line` (+ `vw_Payment_Line`) con numero de egreso y tercero (equivale a PresLsEje).
Filtros comunes (parametros tipados): tercero, rango de fechas, rango de rubros, fuente, uso contable, vigencia,
bandera con/sin saldo. Orden y presentacion (miles de pesos) = capa de presentacion (RN-09 de PRES-11).

## 4. Fuera de alcance definido
- **REPORTE DE EJECUCION AGREGADO** (`Get_Budget_Execution_Report`, `fn_Budget_Execution_Report`, `vw_Budget_Execution_Movement`): TERRITORIO BASELINE P2.2 (PAR-D) -> FUERA (aislamiento). Esta SPEC NO lo consume ni lo replica.
- **Libro oficial** (saldos corridos, `Get_Budget_Book`, PRES-11 B-01, ALTA): SPEC separada.
- **Comparativo por fuente** (superavit/deficit, B-03) y variantes contraloria/austeridad/sector-BPIN (B-04): SPECs separadas / confirmacion normativa.
- Cualquier MUTACION (esto es solo lectura) o reimplementacion de saldos/formulas en C# (RN-09).

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; las vistas se verificaron existentes al sello):**
  - Vistas de saldo (existentes): `vw_Availability_Certificate_Balance`/`_Line_Balance`, `vw_Commitment_Balance`/`vw_Commitment_Line_Balance`, `vw_Obligation_Balance`/`vw_Obligation_Line_Balance`; pagos via `treasury.Payment_Order_Budget_Line` + `vw_Payment_Line`.
  - Procs a CREAR (BR-C3, hoy inexistentes): `Get_Availability_Certificate_List`, `Get_Commitment_List`, `Get_Obligation_List`, `Get_Payment_List` (contratos de lectura parametrizados; patron de `Get_Budget_Execution_Report`, 15-param style). NO tienen THROW (lectura).
- **API:** `GET /api/budget/availability-certificates` (list, filtros query), `GET /api/budget/commitments`, `GET /api/budget/obligations`, `GET /api/budget/payments` -- cada uno con los filtros comunes + con/sin saldo; DTO 1:1 con el resultset; paginacion/orden en servidor sobre el resultset (sin re-consulta SQL propia). ProblemDetails en parametros invalidos.
- **UI (apps/nova-web):** 4 grillas de listado con panel de filtros comun; export de lo consultado; vigencia explicita (F-NOVA-05); en vigencias cerradas, comportamiento consistente con el snapshot (B-05, deshabilitar filtros de periodo si aplica).
- **Capa Application:** `NOVA.Application/Budget/DocumentLists/` (GetAvailabilityCertificateList, GetCommitmentList, GetObligationList, GetPaymentList; cada uno mapea filtros -> parametros del proc/gateway).
- **Referencias:** NOVA-PRES-11 (s.3.3 catalogo de vistas, s.5 listados con saldo, s.6 B-02), NOVA-PRES-04/05/06/07 (saldos de cada documento), NOVA-PRES-000 s.03/s.08, NOVA-GOAL-001 (GOAL-P2 read model + APIs). (NO se referencia SPEC-NOVA-P2-001 / el reporte agregado -- aislamiento.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (esp. React nunca SQL; C# no reimplementa saldos; casos de uso -> gateways tipados; cero DataTable) + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) Solo LECTURA: los listados consumen las vistas de saldo/los procs Get_*_List; jamas DML ni SELECT ad-hoc a tablas de linea; la logica de saldo vive en las vistas (RN-01..RN-03 de PRES-11), la app no la recalcula (RN-09).
  - (b) **AISLAMIENTO:** NO consumir ni referenciar `Get_Budget_Execution_Report`/`fn_Budget_Execution_Report`/`vw_Budget_Execution_Movement` (territorio baseline P2.2); los listados son por DOCUMENTO, no el reporte agregado.
  - (c) Los procs Get_*_List siguen el patron del contrato de lectura (parametros tipados; sin THROW; resultset estable); la UI pagina/ordena en servidor sobre el resultset.
  - (d) Vigencia explicita (F-NOVA-05); con/sin saldo es un parametro; el disponible de CDP usa la vista correcta (recordar B-01 de PRES-04: si se muestra saldo de CDP, la vista de validacion adecuada es `vw_Commitment_Availability_Validation`).
  - (e) DTOs 1:1 con el resultset (sin columnas inventadas ni omitidas); ProblemDetails en parametros invalidos.
  - (f) Correlation id en cada consulta (observabilidad; regla 8/DoD).

## 7. Criterios de aceptacion definidos (Given/When/Then)
1. **Dado** el listado de CDP con bandera `con_saldo=true` y filtros de vigencia/fuente, **cuando** consulto, **entonces** recibo exactamente las filas de `vw_Availability_Certificate_Balance`/`_Line_Balance` con disponible > 0 que cumplen los filtros -- paridad total contra la vista (comparacion automatizada de filas/totales).
2. **Dado** el listado de compromisos "por obligar", **entonces** las filas y el saldo por obligar coinciden con `vw_Commitment_Line_Balance` (paridad).
3. **Dado** el listado de obligaciones "por pagar" con `con_saldo=false`, **entonces** incluye tambien las de saldo 0 (parametro respetado).
4. **Dado** el listado de pagos, **entonces** cada fila trae el numero de egreso y el tercero, desde `Payment_Order_Budget_Line`/`vw_Payment_Line` (equivale a PresLsEje).
5. **Dado** parametros invalidos (vigencia inexistente, rango de rubros mal formado), **entonces** 400 ProblemDetails (validacion de aplicacion); una consulta valida sin datos = 200 con resultset vacio.
6. **Dado** cualquier listado, **entonces** NO invoca `Get_Budget_Execution_Report` ni el read model agregado (verificable en el diff; aislamiento PAR-D).
7. **Dado** un resultset grande, **entonces** la paginacion es en servidor sobre el resultset, sin re-consulta SQL propia (RN-09).

## 8. Pruebas / gates definidos
- **Unit:** mapeo filtros -> parametros de cada Get_*_List; paginacion/orden en memoria de servidor; validacion de parametros -> ProblemDetails.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; cero DataTable; **test de aislamiento: ningun proyecto de esta unidad referencia `Get_Budget_Execution_Report`/`fn_Budget_Execution_Report`** (criterio 6).
- **Integracion vs DbsFinanciero:** criterios 1-4 (paridad de cada listado contra su vista de saldo, comparacion automatizada), criterio 5 (400 vs 200-vacio). EXECUTE: conector readonly tiene SELECT/VIEW DEFINITION; para los procs Get_*_List nuevos, la paridad se verifica contra las VISTAS (SELECT) que ya son readonly-accesibles -- no requiere EXECUTE de procs de mutacion.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=no reimplementacion de saldos, 5=paridad de numeros contra las vistas, 9=fuera de alcance -- que NO toque el reporte agregado P2.2) + **VERIFICACION DE AISLAMIENTO explicita** (manifiesto: no se consumio ni leyo P2.2) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Consumir/replicar el reporte de ejecucion agregado (P2.2) | CONTAMINACION intra-par PAR-D (territorio baseline) | Restricciones 6b; architecture test de aislamiento (criterio 6); manifiesto verificado por el Analista |
| Reimplementar saldos/disponibles en C# | Divergencia con la BD (RN-09) | Restriccion 6a; el adversarial lo busca (punto 2); paridad contra vistas |
| Mostrar saldo de CDP desde la vista con committed=0 (PRES-04 B-01) | Saldo inflado en el listado | Restriccion 6d: usar la vista de validacion correcta |
| Re-consultar SQL propio para paginar | Rompe el contrato de lectura | Restriccion 6c/criterio 7: paginacion en servidor sobre el resultset |
| DTO que inventa/omite columnas | Contrato inestable | Restriccion 6e: DTO 1:1 |

## 10. Prioridad definida
**GOAL-P2** (read model / consultas), brazo GOBERNADO, miembro GOBERNADO de **PAR-D**. **Pertenencia Q4: DENTRO**
(criticidad BAJA por regla determinista -- la severidad de la BRECHA no se hereda a la TAREA; sobre vistas ya
existentes; fabrica de tareas S que calibra el pool). Severidad s.08: superficie de lectura operativa.
Dependencias: GOAL-P1 (fundacion) + las vistas de saldo de la cadena (existen, verificadas al sello). NO depende de
brecha de BD (las vistas existen; los Get_*_List son superficie). **AISLAMIENTO PAR-D:** su fase SPEC se excluye del
delta (simetria con el spec_prepagado de P2.2); NO se leyo la fuente baseline; el reporte agregado queda fuera.
Desbloquea: la operacion diaria de encadenamiento de la cadena de gasto.
