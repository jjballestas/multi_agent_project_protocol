# SPEC-NOVA-P4-001 - Apply_Budget_Modification (modificaciones de apropiacion 01-04) [PATTERN-SETTER familia ajustes, EXCLUIDA del contraste]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). PATTERN-SETTER de la familia de
> ajustes; EXCLUIDA del contraste A/B (primera_unidad de alcance congelado). Su patron congelado lo heredan los
> miembros de PAR-1 (P4.2/P4.3). Preparada por el Arquitecto (arq+docs) FUERA de la ventana medida; el dev
> MEDIDO NO abre pre-sello. Fuente: NOVA-PRES-03 (Modificaciones) + NOVA-PRES-02 (formula seis-efectos).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-001 - task_id (hub): TASK-0246 (familia SPECs Sprint 1)
- owner_maker: agente desarrollador de la instancia (Sprint 1); repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial,
  nunca self-review; DIRECTIVA operador 2026-07-04). tokens_adversarial_informal taggeados a esa sesion.
- arm: baseline / primera_unidad congelada (pattern-setter). NO tiene hermano baseline que contaminar.
- q4_membership: **FUERA** (pattern-setter EXCLUIDO del contraste; su patron se CONGELA al arrancar el miembro
  baseline de PAR-1). [Declaracion explicita de membresia: OBLIGATORIA -- F-0246-01 bloqueo P3 por omitirla.]
- isolation: pattern-setter sin hermano baseline (leyo_codigo_hermano = NA/NO). La restriccion de aislamiento
  es NO filtrar su patron/implementacion congelado a las unidades de contraste posteriores mas alla del patron
  declarado. Manifiesto de archivos leidos: NOVA-PRES-03/02 (docs de proceso) + arquitectura + GOAL. Plantilla
  estructural: SPEC-NOVA-P4-004.
- **PRECONDICION BLOQUEANTE (sandbox mutadores <=14-jul):** el conector readonly `nova_sql_connector_readonly_s9`
  NO tiene EXECUTE (Msg 229). Como `Apply_Budget_Modification` ESCRIBE, sus criterios (crear acto 'G' +
  numeracion; cada THROW alcanzable; delta de la vista de saldo) NO se ejercen readonly. Requiere el MECANISMO
  SANDBOX SELLADO (backup restaurado con GRANT EXECUTE al rol de verificacion, o BEGIN TRAN / EXEC / ROLLBACK
  contra copia), IDENTICO en ambos brazos, listo <=14-jul (DECISION-0078; precedente DECISION-0041). SIN el
  sandbox, los tests de mutacion son un-runnable y el patron a congelar no se valida -> la unidad se DIFIERE.
- **measurement:** cache-confound -> mismo runtime/tipo de sesion que su comparador o declarar; captura de tokens
  en err.log (stderr); desglose por cubeta no capturable -> tokens_total_atribuibles. checker_formal=0 (baseline).
- **deuda GOAL-P1:** harness test front (apps/nova-web) verde en clon limpio antes de la UI de esta unidad.
- **F-NOVA-01 (clausula de re-verificacion, CRITICA -- precedente F-0246-02):** el maker RE-VERIFICA el set EXACTO
  de THROW del `Budget.Apply_Budget_Modification` DESPLEGADO via OBJECT_DEFINITION/sys.objects al construir. La
  familia documentada 50230-50243 (abajo) es la de PRES-03/schema-139; el proc hermano probo divergencia (P4-004
  cito 50256 pero el desplegado emite 50265). NINGUN codigo se hornea en un criterio falsable sin confirmarlo en
  la definicion desplegada; los codigos de homogeneidad/cuadre son los mas probables de diferir.
- db_verified_at: objetos de NOVA-PRES-03 (BD DbsFinanciero; `Apply_Budget_Modification` schema/139 listado
  verificado); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01) -- ver clausula arriba.
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025
  via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario de presupuesto aplica una MODIFICACION DE APROPIACION (adicion / reduccion / traslado credito-
contracredito) sobre las lineas de presupuesto inicial de una vigencia abierta, mediante una llamada ATOMICA a
`Budget.Apply_Budget_Modification` (proc controlado), traduciendo sus THROW a ProblemDetails, sin reimplementar
en C# el cuadre, la no-negatividad ni la numeracion.
- Fuente: NOVA-PRES-03 s.1/s.3/s.4/s.5 + NOVA-PRES-02 s.3.2 (formula seis-efectos) + NOVA-GOAL-001 s.8 P4.
- Calidad: falsable. Bien: "un traslado con Sigma credito != Sigma contracredito devuelve ProblemDetails del
  THROW de cuadre (50237/50238, A RE-VERIFICAR contra la definicion desplegada) y NO aplica nada".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto (modificaciones)**: prepara/revisa el acto en la capa de aplicacion (no hay
borrador en BD) y lo aplica. Supuesto temporal: usuario autenticado con rol presupuesto aplica; policy por
operacion via BR-C4 post-Sprint-1. Es un MUTADOR de apropiacion (distinto de los ajustes de la cadena P4.2-P4.4).

## 3. Alcance definido
Un contrato de mutacion atomico + su preparacion en aplicacion:
- **Tipos (NOVA-PRES-03 s.1, codigos confirmados):** 01 adicion (+), 02 reduccion (-), 03 traslado credito (+),
  04 contracredito (-). Aplazamiento/desaplazamiento NO los maneja el proc (PRES-02 B-03) -> FUERA (gap declarado).
- **Patron: Apply ATOMICO, SIN borrador->aprobar** (PRES-03 s.5: "el acto se aplica completo o falla completo").
  La preparacion/simulacion vive en la capa de aplicacion, pre-validando contra las MISMAS vistas de saldo; el
  proc es una unica llamada transaccional (XACT_ABORT + UPDLOCK/HOLDLOCK).
- El acto escribe cabecera `Budget.Budget_Adjustment` (numerada A comun / GA SGR via `Allocate_Document_Number`)
  + detalle `Budget.Initial_Budget_Line_Adjustment` (seis efectos, CHECK un-solo-efecto, montos >= 0).
- El saldo de apropiacion se recalcula por la vista (formula seis-efectos), NO en C#.

## 4. Fuera de alcance definido
- **Ajustes de la CADENA** (Apply_Availability/Commitment/Obligation_Adjustment, tipos 08-14): son P4.2/P4.3/P4.4,
  usan otra TVP (`Chain_Adjustment_Line_List`) -> FUERA. Esta unidad es apropiacion (01-04).
- **Aplazamiento/desaplazamiento** (efectos sin proc, PRES-02 B-03): FUERA (gap; no hay camino alcanzable).
- **Anular la modificacion** (no existe `Annul_Budget_Adjustment`, PRES-03 B-02; la anulacion cascada de detalle
  auto-restaura saldos por la vista): FUERA.
- **Contabilidad:** las modificaciones NO postean contabilidad (RN-12, CtasXRubro obsoleto CGN).
- Cualquier reimplementacion en C# del cuadre/no-negatividad/numeracion (regla 3 del GOAL).

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR contra la desplegada; F-NOVA-01):**
  - Proc: `Budget.Apply_Budget_Modification` (schema/139; XACT_ABORT, UPDLOCK/HOLDLOCK). Firma:
    `@fiscal_year_id, @adjustment_date, @description, @created_by_user_id, @lines, @adjustment_code=NULL`.
    Devuelve id, code, type, regimen.
  - TVP: `Budget.Budget_Modification_Line_List` (linea de presupuesto inicial, efecto, monto). [NO la
    `Chain_Adjustment_Line_List`, que es de la cadena.]
  - Numeracion: `Budget.Allocate_Document_Number` (serie A comun / GA SGR).
  - Cabecera `Budget.Budget_Adjustment` (schema/050; UNIQUE por vigencia+adjustment_code; trigger vigencia-abierta
    THROW 50212; trigger cascada `trg_budget_adjustment__cascade_status`). Detalle
    `Budget.Initial_Budget_Line_Adjustment` (schema/065; seis efectos >=0; CHECK `one_effect`; trigger
    mismo-vigencia THROW 50065).
  - Vistas de validacion (validar contra, sin recalcular): `Budget.vw_Initial_Budget_Line_Balance`
    (`current_appropriation_amount`, formula seis-efectos, PRES-02 s.3.2 -- el objetivo canonico); la vista/computo
    de `appropriation_available` (insumo del piso CDP, RN-06/50242); `Budget.vw_Budget_Adjustment` (leer el acto).
  - Catalogo: `Budget.Budget_Movement_Type` (01/02/03/04).
- **THROW (familia DOCUMENTADA 50230-50243; RE-VERIFICAR set exacto desplegado, F-NOVA-01):** 50230/50231
  vigencia inexistente/no-abierta (RN-01); 50212 trigger vigencia-abierta cabecera; 50232-50235 linea
  (monto>0/efecto valido/linea existe-activa-de-vigencia, RN-02); 50236 acto no homogeneo (RN-03); 50237/50238
  traslado no cuadra o sobre no-gasto / 50239 adicion-reduccion no cuadra ingresos=gastos (RN-04, +-0.01);
  50240 regimen no homogeneo SGR-vs-comun (RN-05); 50241 no-negatividad / 50242 piso CDP (RN-06, bajo lock);
  50243 adjustment_code no unico (RN-10); 50065 detalle mismo-vigencia.
- **API:** `POST /api/budget/appropriation-modifications` (aplica; body = tipo + lineas efecto/monto + fecha +
  descripcion); ProblemDetails traduciendo cada THROW; devuelve id/code/type/regimen. Preparacion:
  `POST .../validate` (previsualiza cuadre/saldo contra las vistas, sin escribir).
- **UI (apps/nova-web):** formulario de modificacion (tipo, lineas, montos), previsualizacion de cuadre y saldo
  resultante (desde las vistas), vigencia explicita; en vigencias cerradas, bloqueado (RN-01).
- **Capa Application:** `NOVA.Application/Budget/AppropriationModifications/` (ApplyBudgetModification: mapea
  lineas -> TVP; valida cuadre/homogeneidad en el caso de uso ANTES de llamar el proc; traduce THROW).
- **Referencias:** NOVA-PRES-03 (s.1 tipos, s.3 proc/TVP, s.4 RN-01..RN-12, s.5 contrato), NOVA-PRES-02 (formula
  seis-efectos, RN-08 linea-base-0, RN-10), NOVA-GOAL-001 (P4). (Es pattern-setter; NO consume unidades de contraste.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa cuadre/saldo/
  numeracion; casos de uso -> gateways tipados; cero DataTable) + maestro-P1..P6 + stack del preambulo.
- Propias:
  - (a) La mutacion va SOLO por `Apply_Budget_Modification` (Apply atomico); jamas DML directo ni recalculo del
    cuadre/saldo en C# (RN-04/RN-06 viven en el proc; "pecado capital").
  - (b) **Acto HOMOGENEO** (RN-03): solo adicion, solo reduccion, o traslado (03+04); el caso de uso lo valida
    ANTES del proc y el proc lo re-valida (50236).
  - (c) **CUADRE** (RN-04): traslado Sigma credito = Sigma contracredito (+-0.01), solo gasto; adicion/reduccion
    ingresos=gastos (+-0.01). Validado en aplicacion (previsualizacion) Y en el proc.
  - (d) **NO-NEGATIVIDAD + PISO CDP** (RN-06): no dejar apropiacion negativa ni bajo el CDP emitido (bajo lock,
    en el proc); la app NO lo recalcula.
  - (e) Numeracion SOLO por `Allocate_Document_Number` (serie A/GA); jamas asignar codigo en UI/C# (regla del GOAL).
  - (f) DTOs 1:1; THROW -> ProblemDetails (cada codigo alcanzable, RE-VERIFICADO F-NOVA-01); correlation id +
    task_id en cada mutacion; usuario real.
  - (g) Aplazamiento/desaplazamiento NO se parchean en C# (gap sin proc, PRES-02 B-03).

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> NOTA F-NOVA-01: cada criterio negativo cita el THROW DOCUMENTADO; el maker CONFIRMA el codigo exacto contra
> `OBJECT_DEFINITION` del `Apply_Budget_Modification` DESPLEGADO antes de fijarlo (los codigos de homogeneidad/
> cuadre son los mas probables de diferir, cf. F-0246-02). Los tests de mutacion corren en el SANDBOX sellado.
1. **Dado** una adicion valida (una linea, efecto 01, vigencia abierta), **cuando** aplico, **entonces**
   `Apply_Budget_Modification` crea el acto 'G' numerado (serie A/GA) y `vw_Initial_Budget_Line_Balance`
   incrementa `current_appropriation_amount` en el monto.
2. **Dado** un traslado con Sigma credito != Sigma contracredito, **entonces** ProblemDetails del THROW de cuadre
   (50237/50238 doc; RE-VERIFICAR) y NO aplica nada.
3. **Dado** un acto que mezcla adicion y reduccion (no homogeneo), **entonces** THROW 50236 (doc; RE-VERIFICAR).
4. **Dado** una reduccion que dejaria la apropiacion negativa o bajo el CDP emitido, **entonces** THROW
   50241/50242 (doc; RE-VERIFICAR) bajo lock; sin cambio.
5. **Dado** una vigencia cerrada, **entonces** THROW 50230/50231 (o el trigger 50212 en la cabecera).
6. **Dado** un acto que mezcla fuentes SGR y comunes, **entonces** THROW 50240 (regimen no homogeneo).
7. **Dado** un `adjustment_code` override duplicado en la vigencia, **entonces** THROW 50243 (RN-10).
8. **Dado** cualquier acto, **entonces** el saldo se lee de la vista (formula seis-efectos), NO recalculado en C#
   (verificable en el diff); y NO postea contabilidad (RN-12).

## 8. Pruebas / gates definidos
- **Unit:** mapeo lineas -> TVP; validacion de homogeneidad/cuadre en el caso de uso -> ProblemDetails; traduccion
  THROW->ProblemDetails; enforcement de numeracion-solo-por-proc.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; Mcp sin SQL; cero DataTable.
- **Integracion vs DbsFinanciero (EN SANDBOX; EXECUTE via GRANT o TRAN/ROLLBACK):** criterio 1 (adicion happy:
  acto 'G' + serie + delta de saldo), un caso por THROW ALCANZABLE (cuadre 50237/38, homogeneo 50236, no-neg/piso
  50241/42, vigencia 50230/31/50212, regimen 50240, codigo 50243) RE-VERIFICADO contra OBJECT_DEFINITION, criterio
  8 (saldo por vista). **PRECONDICION: sandbox mutadores listo <=14-jul; sin el, la unidad se DIFIERE (no se
  degrada a leer OBJECT_DEFINITION en silencio).**
- **Gate final:** APROBADO del **adversarial informal de 12 puntos en SESION SEPARADA / contexto limpio** (dev !=
  adversarial) + arch tests + CI verde + **F-NOVA-01: cada THROW verificado falsable contra el proc desplegado** +
  DoD de NOVA-GOAL-001 con evidencia real (delta de saldo, ProblemDetails provocado por THROW, OpenAPI) + verde de
  gates del hub + atestacion sha256. checker_formal=0 (baseline/primera_unidad).

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Citar THROW documentado que el proc desplegado NO emite | Criterio falso (precedente F-0246-02) | F-NOVA-01: RE-VERIFICAR cada codigo contra OBJECT_DEFINITION antes de fijarlo |
| Sandbox mutadores no listo <=14-jul | Criterios de mutacion un-runnable | Precondicion bloqueante declarada; la unidad se DIFIERE (DECISION-0078) |
| Reimplementar cuadre/no-negatividad/saldo en C# | Divergencia con la BD (RN-04/06) | Restricciones 6a/6c/6d; adversarial punto 2; validar contra la vista |
| Asignar numero de acto en UI/C# | Rompe la numeracion controlada | Restriccion 6e: solo `Allocate_Document_Number` |
| Tratar aplazamiento en C# (gap sin proc) | Regla fuera del proc reimplementada | Restriccion 6g: gap declarado, no se parchea |
| adversarial en la misma sesion del maker | Contaminacion (tokens no separables) | DoR: adversarial en SESION SEPARADA |

## 10. Prioridad definida
**GOAL-P4** (ajustes/mutadores), **PATTERN-SETTER de la familia de ajustes**, EXCLUIDA del contraste A/B.
**Pertenencia Q4: FUERA** (primera_unidad congelada; su patron se congela al arrancar el miembro baseline de
PAR-1). Severidad s.08: mutador de apropiacion (mueve el techo del gasto). Dependencias: GOAL-P1 (fundacion) +
`Apply_Budget_Modification` (existe, verificado; RE-VERIFICAR THROW) + **SANDBOX mutadores <=14-jul (precondicion
BLOQUEANTE)**. AISLAMIENTO: pattern-setter sin hermano baseline (leyo_codigo_hermano=NA); su patron congelado
(Apply atomico + TVP + pre-validacion por vista + THROW->ProblemDetails + verificacion en sandbox) lo heredan
P4.2/P4.3. Desbloquea: la familia de ajustes de la cadena (PAR-1) y las modificaciones de apropiacion operativas.
