# SPEC-NOVA-P4-004 - Apply Obligation Adjustment / Reintegro de obligacion (tipo 14)

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Brazo GOBERNADO, pool Q4.
> Generada desde NOVA-PRES-03 (Modificaciones) + NOVA-PRES-06 (Obligacion) + NOVA-GOAL-001 + arquitectura.

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-004 - task_id (hub): TASK-0246
- owner_maker: agente desarrollador de la instancia gobernada (Sprint 1); repo producto Nova-Budget
- checker: Analista (adversarial, contexto limpio, SPEC + diff + BD readonly)
- arm: gobernado - unit: P4.4 (Apply_Obligation_Adjustment)
- q4_membership: **DENTRO** (criticidad media; enumerada nominalmente en el pool Q4 del estudio)
- **isolation: CRITICA.** P4.4 es item de POOL Q4 gobernado SIN hermano baseline. Manifiesto de archivos leidos:
  NOVA-PRES-03 (doc de proceso COMPARTIDO de modificaciones) + NOVA-PRES-06 (obligacion). ESTA SPEC se acota
  ESTRICTAMENTE al ajuste de OBLIGACION (tipo 14, reintegro). Los ajustes de CDP (08/09) y de compromiso (11/12)
  -- que son el TERRITORIO de los miembros BASELINE de par P4.2 (Apply_Availability_Adjustment) y P4.3
  (Apply_Commitment_Adjustment) -- y la modificacion de apropiacion (01-04, P4.1 baseline) quedan FUERA de
  alcance. NO se leyo codigo/implementacion de ningun miembro baseline: `leyo_codigo_hermano = NO`. PRES-03 es
  documentacion de dominio compartida (los procs existen en la BD), no la fuente de la tarea baseline.
- **PRECONDICION: READY (sandbox mutadores sellado, adelantado <=14-jul).** Mecanismo construido y sellado por
  el Operador (2026-07-04): ver `SANDBOX-MUTADORES-mecanismo-sellado.md` (BD `DbsFinanciero_SANDBOX` + rol
  `budget_sandbox_verifier` con EXECUTE real, aislamiento verificado, IDENTICO en ambos brazos + RESET
  obligatorio entre miembros/brazos, DECISION-0078). Ya NO bloquea la unidad.
- **measurement (DIRECTIVA operador medicion-real 2026-07-04):** cache-confound -> ambos brazos MISMO runtime/tipo de sesion (cache comparable) o declarar el confound; captura de tokens = err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 en el brazo baseline.
- db_verified_at: objetos de NOVA-PRES-03/06 (BD DbsFinanciero readonly 2026-07-03); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01)
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025 via SPs con gateways tipados (incluye TVP) / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto REINTEGRA (disminuye) el valor de una o varias lineas de una obligacion mediante un acto
de ajuste tipo 14, aplicado atomicamente via `Budget.Apply_Obligation_Adjustment`, que valida bajo bloqueo que el
reintegro no excede el saldo no pagado de la linea y LIBERA saldo del compromiso padre.
- Fuente: NOVA-PRES-03 s.1/s.3/s.4 (RN-08/RN-09) + s.5 (Contrato, fila reintegro 14) + NOVA-PRES-06 RN-07.
- Calidad: falsable. Bien: "reintegrar mas que (obligacion - pagado) es rechazado con THROW 50264; un efecto distinto de reintegro con THROW 50265; un reintegro valido crea el acto 'G' numerado por serie y el saldo del compromiso aumenta (se libera) en la vista".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto** (ajustes de ejecucion): prepara el acto (selecciona lineas de obligacion y montos a
reintegrar, simula el tope) y lo aplica. Matriz de autorizacion por operacion no sembrada (B-05 Doc 01). SUPUESTO
TEMPORAL: usuario autenticado con rol presupuesto; policy por operacion (BR-C4) post-Sprint-1. NO hay borrador: la
preparacion/simulacion vive en la aplicacion; aplicar es atomico (el acto se aplica completo o falla completo).

## 3. Alcance definido
1. Preparar el acto en la aplicacion: seleccionar lineas de obligacion activas, montos de reintegro (>0, efecto unico), y previsualizar el tope con `vw_Obligation_Line_Balance` (mismos numeros que validara el proc).
2. Aplicar el reintegro -> canal UNICO: `Budget.Apply_Obligation_Adjustment(@fiscal_year_id,@adjustment_date,@description,@created_by_user_id,@lines,@adjustment_code=NULL)` con TVP `Budget.Chain_Adjustment_Line_List` (linea de documento, efecto=14, monto).
3. Leer el resultado: id/codigo/tipo/regimen devueltos; el saldo de la obligacion (`vw_Obligation_Line_Balance`) baja y el del compromiso (`vw_Commitment_Line_Balance`) sube (reintegro libera compromiso).

## 4. Fuera de alcance definido
- **Modificacion de apropiacion (01-04)**: `Apply_Budget_Modification` = unidad P4.1 (BASELINE) -> FUERA.
- **Ajuste de CDP (08/09)**: `Apply_Availability_Adjustment` = territorio de P4.2 (miembro BASELINE de par) -> FUERA.
- **Ajuste de compromiso (11/12)**: `Apply_Commitment_Adjustment` = territorio de P4.3 (miembro BASELINE de par) -> FUERA.
- **Anulacion del acto de ajuste**: no existe `Annul_Budget_Adjustment` con validacion aguas abajo (NOVA-PRES-03 s.6 B-02) -> FUERA (SPEC separada; hoy la cascada del trigger restaura saldos pero sin validar no-negatividad aguas abajo).
- Aumentar una obligacion (RN-09: solo se disminuye por ajuste; aumentar exige obligacion nueva = P3-004).
- Contabilizar (RN-12/P4: las modificaciones no contabilizan).
- Cualquier escritura directa a las tablas de ajuste o recalculo de topes/saldos en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada):**
  - Cabecera: `Budget.Budget_Adjustment` (unica por vigencia+adjustment_code; tipo contra `Budget_Movement_Type`; series computadas; trigger vigencia abierta 50212 + cascada de anulacion).
  - Detalle: `Budget.Obligation_Line_Adjustment` (SOLO reintegro 14; un efecto por fila; monto >=0; triggers 50160-50163 incl. no reducir por debajo de lo pagado).
  - Proc: `Budget.Apply_Obligation_Adjustment(@fiscal_year_id, @adjustment_date, @description, @created_by_user_id, @lines, @adjustment_code=NULL)` (schema/141; XACT_ABORT). THROW REALES (OBJECT_DEFINITION verificado readonly en DbsFinanciero): 50250, 50251, 50252, 50253, 50255, 50257, 50258, 50264, 50265 -- efecto distinto de reintegro (effect_code != counter_credit) = **50265**; tope obligacion-pagado = **50264**. El proc NO emite 50254 ni 50256 (F-NOVA-01: se cita la definicion real, no la familia generica de PRES-03).
  - TVP: `Budget.Chain_Adjustment_Line_List` (obligation_line_id, effect=14, amount).
  - Numeracion: `Allocate_Document_Number` (serie comun `''` / SGR `G` segun fuentes de las lineas).
  - Vistas: `vw_Obligation_Line_Balance` (tope = obligacion - pagado neto), `vw_Commitment_Line_Balance` (views/140: el reintegro 14 LIBERA compromiso), `vw_Budget_Adjustment`.
- **API:** `POST /api/budget/obligation-adjustments` (aplica; body = fecha/descripcion/lineas TVP), `GET .../{obligationLineId}/reintegro-preview` (previsualiza tope via `vw_Obligation_Line_Balance`), `GET` de lectura de actos. DTOs 1:1; ProblemDetails; el endpoint devuelve id/codigo/tipo/regimen.
- **UI (apps/nova-web):** seleccion de obligacion y lineas, captura del monto a reintegrar por linea, simulacion del tope (obligacion - pagado) con la misma vista, aviso de que el reintegro libera el compromiso padre; aplicar es atomico. Vigencia explicita (F-NOVA-05).
- **Capa Application:** `NOVA.Application/Budget/Obligations/Adjustments/` (PrepareObligationReintegro, PreviewCap, ApplyObligationAdjustment, ReadAdjustment).
- **Referencias:** NOVA-PRES-03 (s.3-s.6), NOVA-PRES-06 (obligacion RN-07), NOVA-PRES-000 s.03/s.08, dictionary/budget_adjustments, NOVA-GOAL-001 (GOAL-P4 + APIs).

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La aplicacion es SOLO `Apply_Obligation_Adjustment`; la app nunca escribe `Obligation_Line_Adjustment`/`Budget_Adjustment` ni recalcula topes/saldos; captura del acto = preparacion + TVP tipada.
  - (b) SOLO tipo 14 (reintegro = contracredito de obligacion); toda linea debe ser efecto reintegro. Un efecto distinto de reintegro (effect_code != counter_credit) -> **THROW 50265** (verificado en el proc real; NO 50256).
  - (c) Tope RN-08: reintegro <= obligacion - pagado (**THROW 50264**); RN-09: la obligacion solo se disminuye; el reintegro libera el compromiso (views/140). No reducir por debajo de lo pagado (triggers 50160-50163).
  - (d) Vigencia abierta (RN-01, THROW 50250/50251); lineas activas de la vigencia (RN-02, 50252/50253/50255); regimen homogeneo (RN-05, 50257); codigo unico por vigencia (RN-10, 50258).
  - (e) Numeracion por serie de la BD dentro de la transaccion; la UI no propone numero. Saldos siempre por vista (nunca acumuladores). Vigencia explicita.
  - (f) NO borrador compartido: el acto se aplica completo o falla completo (atomicidad del proc; corrige el hallazgo legacy de inserciones a medias).
  - (g) Toda mutacion: correlation id + usuario real + THROW del proc (50250-50253, 50255, 50257, 50258, 50264, 50265) traducido a ProblemDetails con mensaje de negocio.
  - (h) **GUARD DE PROCEDENCIA:** el harness de evidencia F-NOVA-01 usa una clase SQL real, gateada
    por env vars, NA limpio sin credenciales -- jamas un mock/Recording* in-memory (precedente TASK-0253).
  - (i) **LECTURA DE RESULT-SET SIN ADIVINANZA (hereda P4-006):** el gateway de produccion NO debe leer
    columnas del result-set de `Apply_Obligation_Adjustment` por fallback encadenado de nombres ni caer en
    un DEFAULT SILENCIOSO si la columna no aparece. El nombre EXACTO de cada columna se confirma contra
    `OBJECT_DEFINITION`/`sys.dm_exec_describe_first_result_set` del proc DESPLEGADO antes de escribir el
    gateway; el harness F-NOVA-01 ejercita el MISMO camino de lectura que el gateway de produccion.
  - (j) **COBERTURA HTTP DE INTEGRACION (hereda P4-006):** cada endpoint mutador nuevo (preview +
    reintegro) tiene al menos un test de integracion HTTP real (`WebApplicationFactory` + gateway FALSO
    inyectado) que ejercita ruta -> endpoint -> mapeo de comando -> gateway.
  - (k) **LISTA DE AISLAMIENTO COMPLETA (hereda P4-006):** el test de arquitectura de aislamiento del
    frontend DEBE incluir `Apply_Obligation_Adjustment` en su lista de literales prohibidos. Exhibicion
    como texto descriptivo en UI = excepcion explicita documentada, nunca omision silenciosa.
  - **NOTA DE CONVERGENCIA (post-P4-006):** esta unidad hereda el supuesto temporal DD-01 (sin wiring
    real de autorizacion), igual que el baseline. Antes de promover a Sprint 1, evaluar si esta unidad
    debe adoptar el patron de autorizacion real de s.6h de SPEC-NOVA-P4-006 (converge #5/#7/#8), dado que
    es brazo GOBERNADO y muta saldo de obligacion/compromiso.

## 7. Criterios de aceptacion definidos (Given/When/Then; + un negativo por THROW alcanzable)
1. **Dado** un acto tipo 14 cuyas lineas reintegran <= (obligacion - pagado) por linea, **cuando** aplico, **entonces** `Apply_Obligation_Adjustment` crea la cabecera 'G' con numero de serie (comun/SGR), inserta el detalle 14 y devuelve id/codigo/tipo/regimen; el saldo de la obligacion baja y el del compromiso sube en las vistas.
2. **Dado** un reintegro que EXCEDE (obligacion - pagado) en alguna linea, **cuando** aplico, **entonces** ProblemDetails del THROW **50264** y no se aplica nada (atomico).
3. **Dado** un acto con una linea de efecto distinto de reintegro (effect_code != counter_credit), **cuando** aplico, **entonces** THROW **50265**.
4. **Dado** una linea de obligacion inexistente/inactiva/de otra vigencia, **cuando** la referencio, **entonces** THROW **50252/50253/50255** (segun el chequeo; el proc no emite 50254).
5. **Dado** una vigencia cerrada/inexistente, **cuando** intento aplicar, **entonces** THROW **50250/50251**.
6. **Dado** un codigo de acto duplicado en la vigencia, **cuando** aplico con override, **entonces** THROW **50258**.
7. **Dado** el reintegro aplicado, **entonces** `vw_Commitment_Line_Balance` refleja el saldo del compromiso LIBERADO (aumentado) por el reintegro 14 (sin recalculo en C#).
8. **Dado** un acto que mezcla fuentes SGR y comunes en las lineas de reintegro, **cuando** aplico,
   **entonces** THROW **50257** (regimen no homogeneo).
9. **Dado** el gateway de produccion, **entonces** lee cada columna del result-set por el nombre EXACTO
   confirmado contra `OBJECT_DEFINITION`, sin fallback encadenado ni default silencioso; el harness
   F-NOVA-01 ejercita el MISMO camino de lectura.
10. **Dado** los endpoints de preview y reintegro, **entonces** cada uno tiene al menos un test de
    integracion HTTP (`WebApplicationFactory` + gateway falso) que verifica el wiring completo.

## 8. Pruebas / gates definidos
- **Unit:** mapeo del acto -> TVP `Chain_Adjustment_Line_List`; homogeneidad del efecto (solo 14); traduccion THROW->ProblemDetails.
- **Architecture tests:** Domain sin Infrastructure; Application sin ASP.NET; Api/Mcp sin SQL directo; cero DataTable; el paso de TVP es via gateway tipado (no DataTable como contrato).
- **Integracion vs DbsFinanciero:** criterio 1 (reintegro happy: acto + liberacion de compromiso), un caso por THROW real del proc (50265 efecto!=reintegro, 50264 tope, 50252/50253/50255 linea, 50250/50251 vigencia, 50257 regimen, 50258 codigo), criterio 7 (liberacion del compromiso por vista), **criterio 9 (lectura de columnas confirmada, sin adivinanza)**, **criterio 10 (test HTTP de integracion con gateway falso por endpoint)**. EXECUTE: conector readonly sin EXECUTE (Msg 229) -> GRANT EXECUTE al rol de verificacion o SELECT a la vista/fn equivalente, documentado.
- **Gate final:** APROBADO del Analista (12 puntos, enfasis en 2=reimplementacion, 3=DML directo, 9=fuera de alcance -- que NO toque 01-04/08/09/11/12 ni anule actos) + guard de procedencia (evidencia SQL real, sin mock) + DoD de NOVA-GOAL-001 con evidencia real + verde de gates del hub + atestacion sha256. VERIFICACION DE AISLAMIENTO: el manifiesto declara que NO se implemento ni copio codigo de P4.1/P4.2/P4.3 (baseline); la lista de literales prohibidos del frontend incluye `Apply_Obligation_Adjustment`.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Implementar de paso los ajustes de CDP/compromiso (08/09/11/12) | CONTAMINACION intra-par (territorio baseline P4.2/P4.3) | Campo 4 los excluye; el adversarial + manifiesto de aislamiento lo verifican (punto 9) |
| Reintegrar por encima de obligacion-pagado | Saldo inconsistente | RN-08/THROW 50264 bajo bloqueo; la app no recalcula (6a/6c) |
| Linea con efecto distinto de reintegro | Mezcla de efectos | THROW 50265 del proc real (6b) |
| Repetir los huecos de calidad hallados en el hermano baseline PAR-2 (quality-data #11/#12/#13, DECISION-0018 2026-07-06): lectura de columnas por adivinanza+default silencioso, cero test HTTP de integracion, omision del proc en la lista de aislamiento del frontend | Mismo patron de gaps no cazados por el GO informal, esta vez en un miembro gobernado | Restricciones 6i/6j/6k + criterios 9/10 (fix-forward explicito, hereda P4-006) |
| Recalcular topes/saldos o liberacion del compromiso en C# | Divergencia con la BD | Prohibido (6a/6e); el adversarial lo busca (punto 2) |
| Pasar las lineas como DataTable | Viola regla 5 del GOAL | TVP via gateway tipado (restriccion stack); architecture test |
| Intentar anular el acto sin validar aguas abajo (B-02) | Saldos negativos aguas abajo | Anulacion fuera de alcance (campo 4); SPEC separada con validacion |

## 10. Prioridad definida
**GOAL-P4** (ajustes y reversos), brazo GOBERNADO, unidad P4.4. **Pertenencia Q4: DENTRO** (criticidad media,
enumerada nominalmente en el pool Q4). Severidad s.08: ajuste de ejecucion (reintegro), no estructural.
Dependencias: GOAL-P1 (fundacion) + obligacion operable (P3-004, hay obligaciones que reintegrar) + compromiso
(P3-003, el reintegro libera su saldo). NO depende de brecha de BD para el camino feliz (el proc y los topes
50264/50265 existen y estan verificados); el acto administrativo estructurado (B-01) y la anulacion (B-02) son
hardening/SPEC aparte. AISLAMIENTO: sin hermano baseline (item de pool, no de par); no se toca el territorio de
P4.1/P4.2/P4.3 (baseline).
