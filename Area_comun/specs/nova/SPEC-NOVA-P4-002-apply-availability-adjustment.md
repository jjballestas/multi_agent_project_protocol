# SPEC-NOVA-P4-002 - Apply_Availability_Adjustment (ajuste de CDP, tipos 08/09) [miembro de PAR-1, isomorfo con P4-003]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro de PAR-1 (par FIRME,
> isomorfo con P4.3 Apply_Commitment_Adjustment). HEREDA el patron congelado de P4.1 (SPEC-NOVA-P4-001).
> El sorteo del sello asigna cual miembro es baseline y cual gobernado. Preparada por el Arquitecto (arq+docs)
> FUERA de la ventana medida; el dev MEDIDO NO abre pre-sello. Fuente: NOVA-PRES-03 + NOVA-PRES-04 (CDP).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-002 - task_id (hub): TASK-0246 (familia SPECs Sprint 1)
- owner_maker: agente desarrollador de la instancia; repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial;
  DIRECTIVA operador 2026-07-04). En el brazo baseline el checker vivo ES el adversarial informal
  (checker_formal=0); en el brazo gobernado aplica ADEMAS el checker FORMAL del Analista. tokens_adversarial_
  informal taggeados a la sesion separada.
- arm: **PAR-1 (asignado por el sorteo del sello)** - unit: P4.2 Apply_Availability_Adjustment (ajuste de CDP)
- q4_membership: **DENTRO** (miembro de par del contraste; criticidad media, proc existente S). [Declaracion
  explicita OBLIGATORIA -- F-0246-01 bloqueo P3 por omitirla.]
- **isolation: CRITICA (PAR-1).** Isomorfo con P4.3 (Apply_Commitment_Adjustment). leyo_codigo_hermano = **NO**:
  esta SPEC se redacta SOLO de docs de proceso COMPARTIDOS (NOVA-PRES-03 + NOVA-PRES-04) + el patron congelado
  declarado de P4.1; NO se lee la implementacion del hermano ni su repo. Manifiesto de archivos leidos:
  NOVA-PRES-03/04 + arquitectura + P4-001 (patron) + P4-004 (plantilla estructural). Riesgo: implementar los
  tipos del hermano (11/12) "de paso" = CONTAMINACION intra-par -> par CONTAMINADO fuera del confirmatorio.
- **PRECONDICION BLOQUEANTE (sandbox mutadores <=14-jul):** el conector `nova_sql_connector_readonly_s9` NO tiene
  EXECUTE (Msg 229). Como este proc ESCRIBE, sus criterios (crear acto 'G' + numeracion; cada THROW; delta de la
  vista de saldo) NO se ejercen readonly -> requiere el SANDBOX SELLADO (backup+GRANT EXECUTE o BEGIN TRAN/EXEC/
  ROLLBACK), IDENTICO en ambos brazos, listo <=14-jul (DECISION-0078). Sin el, la unidad se DIFIERE.
- **measurement:** cache-confound -> mismo runtime que su pareja de par (dinamica de cache comparable) o declarar;
  captura de tokens en err.log (stderr); desglose no capturable -> tokens_total_atribuibles. checker_formal=0 en
  el brazo baseline; en el gobernado el checker formal SI cuenta.
- **deuda GOAL-P1:** harness test front (apps/nova-web) verde en clon limpio antes de la UI de esta unidad.
- **F-NOVA-01 (re-verificacion, CRITICA -- precedente F-0246-02):** el maker RE-VERIFICA el set EXACTO de THROW
  del `Apply_Availability_Adjustment` DESPLEGADO via OBJECT_DEFINITION. La familia documentada 50250-50261 es de
  PRES-03/schema-141; el proc hermano `Apply_Obligation_Adjustment` probo divergencia (50256->50265; 50254 no
  existe). Codigos de MAYOR riesgo de diferir: **50256** (homogeneidad) y **50254**. NINGUN codigo se hornea en
  un criterio falsable sin confirmarlo en la definicion desplegada.
- db_verified_at: objetos de NOVA-PRES-03/04 (BD DbsFinanciero; proc schema/141; 435 CDP reconciliados); el maker
  RE-VERIFICA contra la BD desplegada (F-NOVA-01).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025
  via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario ajusta un CDP existente (ampliar credito 08 / reducir contracredito 09) mediante una llamada ATOMICA
a `Budget.Apply_Availability_Adjustment`, con los topes de la BD (credito <= apropiacion disponible; contracredito
<= CDP - comprometido), traduciendo THROW a ProblemDetails, sin reimplementar los saldos/topes en C#.
- Fuente: NOVA-PRES-03 s.1/s.3/s.4/s.5 + NOVA-PRES-04 (saldos de CDP) + patron congelado P4.1.
- Calidad: falsable. Bien: "un contracredito 09 que dejaria el CDP bajo lo comprometido devuelve ProblemDetails
  del THROW 50261 (RE-VERIFICAR contra el proc desplegado) y NO ajusta nada".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto (ajustes de cadena)**: prepara/revisa el acto en la capa de aplicacion (no hay
borrador) y lo aplica. Supuesto temporal: usuario autenticado con rol presupuesto; policy por operacion via
BR-C4 post-Sprint-1. Isomorfo al usuario del ajuste de compromiso (P4.3).

## 3. Alcance definido
Un contrato de mutacion atomico + su preparacion:
- **Tipos (PRES-03 s.1):** 08 credito (ampliar CDP) / 09 contracredito (reducir CDP). SOLO ajusta LINEAS
  EXISTENTES (no incorpora rubro-fuente-BPIN nuevos; B-04, hereda el ancla de la linea del CDP padre).
- **Patron congelado de P4.1: Apply ATOMICO, SIN borrador** (PRES-03 s.5; XACT_ABORT + UPDLOCK/HOLDLOCK). La
  preparacion/previsualizacion vive en la capa de aplicacion.
- Escribe cabecera `Budget.Budget_Adjustment` (serie '' comun / G SGR via `Allocate_Document_Number`) + detalle
  `Budget.Availability_Certificate_Line_Adjustment` (solo 08/09; un efecto por fila; misma vigencia).
- El saldo del CDP se recalcula por vista, NO en C#. **HOMOGENEIDAD (RN-03): el acto es TODO credito o TODO
  contracredito.** NO hay cuadre cross-linea (eso es regla de P4.1, no de la cadena).

## 4. Fuera de alcance definido
- **Ajuste de COMPROMISO (11/12), tipos de OBLIGACION (14):** territorio de P4.3 (hermano de par) y P4.4 ->
  FUERA (AISLAMIENTO PAR-1). Esta unidad es SOLO CDP (08/09).
- **Modificacion de APROPIACION (01-04):** es P4.1 -> FUERA.
- **Aprobar/crear el CDP** (`Approve_Availability_Certificate_Draft`, P3.2): FUERA (esto ajusta un CDP existente).
- **Anular:** no hay proc de anulacion de ajuste (la cascada auto-restaura); FUERA.
- Contabilidad (los ajustes de cadena no postean por movimiento) y reimplementacion de saldos/topes en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):**
  - Proc: `Budget.Apply_Availability_Adjustment` (schema/141; XACT_ABORT, UPDLOCK/HOLDLOCK). Firma:
    `@fiscal_year_id, @adjustment_date, @description, @created_by_user_id, @lines, @adjustment_code=NULL`.
    Devuelve id, code, type, regimen.
  - TVP: `Budget.Chain_Adjustment_Line_List` (document_line_id, effect, amount). [NO Budget_Modification_Line_List,
    que es de P4.1.]
  - Cabecera `Budget.Budget_Adjustment` (schema/050; UNIQUE vigencia+code; trigger 50212 vigencia-abierta; cascada
    `trg_budget_adjustment__cascade_status`). Detalle `Budget.Availability_Certificate_Line_Adjustment` (solo
    08/09, triggers 50083/50084). Numeracion `Budget.Allocate_Document_Number` (serie ''/G).
  - Vistas de validacion: `Budget.vw_Availability_Certificate_Line_Balance` (**CAVEAT B-01: `committed_amount`=0
    hard-coded en la vista -> saldo INFLADO; el tope 50261 SI existe en el proc, el defecto es de la vista**) ->
    para el saldo REAL disponible del CDP en la previsualizacion usar **`vw_Commitment_Availability_Validation`**;
    `Budget.vw_Budget_Adjustment` (leer el acto).
- **THROW (familia DOCUMENTADA 50250-50261; RE-VERIFICAR desplegado):** 50250/50251 vigencia inexistente/no-abierta
  (+ trigger 50212); 50252-50255 linea (monto>0/efecto valido/existe-activa-vigencia); **50256 acto no homogeneo
  (RIESGO de diferir -> 50265)**; 50257 regimen no homogeneo; 50258 codigo no unico; **50260 credito 08 > apropiacion
  disponible**; **50261 contracredito 09 > (CDP - comprometido)**.
- **API:** `POST /api/budget/availability-certificates/{id}/adjustments` (aplica; body = tipo 08/09 + lineas +
  fecha + descripcion); ProblemDetails por THROW; devuelve id/code/type/regimen. `POST .../validate` previsualiza
  contra `vw_Commitment_Availability_Validation` (saldo real).
- **UI (apps/nova-web):** formulario de ajuste de CDP (tipo 08/09, lineas, monto), previsualizacion del saldo REAL
  y el resultante, vigencia explicita; en vigencias cerradas bloqueado.
- **Capa Application:** `NOVA.Application/Budget/AvailabilityAdjustments/` (ApplyAvailabilityAdjustment: mapea
  lineas -> Chain_Adjustment_Line_List; valida homogeneidad ANTES; traduce THROW).
- **Referencias:** NOVA-PRES-03 (s.1/s.3/s.4/s.5), NOVA-PRES-04 (saldos CDP, B-01), P4-001 (patron congelado),
  NOVA-GOAL-001 (P4). (NO se lee el hermano P4.3 ni su implementacion -- aislamiento PAR-1.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa saldos/topes/
  numeracion; gateways tipados; cero DataTable) + stack + **patron congelado de P4.1**.
- Propias:
  - (a) Mutacion SOLO por `Apply_Availability_Adjustment` (Apply atomico); jamas DML ni recalculo de topes/saldo en C#.
  - (b) **HOMOGENEIDAD (RN-03):** el acto es todo 08 o todo 09; validado en aplicacion Y en el proc (50256, RE-VERIFICAR).
  - (c) **TOPES (RN-07/08):** credito 08 <= apropiacion disponible (50260); contracredito 09 <= CDP - comprometido
    (50261, bajo lock, en el proc). La app NO los recalcula.
  - (d) **PREVISUALIZACION usa `vw_Commitment_Availability_Validation`** (saldo real), NO
    `vw_Availability_Certificate_Line_Balance` (inflada por B-01, committed=0).
  - (e) Solo LINEAS EXISTENTES (B-04): no incorporar rubro-fuente-BPIN nuevos; hereda el ancla del CDP padre.
  - (f) Numeracion solo por `Allocate_Document_Number`; DTOs 1:1; THROW->ProblemDetails (RE-VERIFICADO); correlation
    id + task_id + usuario real en cada mutacion.
  - (g) **AISLAMIENTO PAR-1:** NO tocar/leer los tipos 11/12 (compromiso, P4.3) ni su implementacion.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW documentado; el maker CONFIRMA el codigo exacto contra OBJECT_DEFINITION
> del proc desplegado antes de fijarlo (50256/50254 = mayor riesgo). Los tests de mutacion corren en el SANDBOX.
1. **Dado** un credito 08 valido sobre una linea de CDP con apropiacion disponible, **cuando** aplico, **entonces**
   el proc crea el acto 'G' numerado y `vw_Commitment_Availability_Validation` refleja el CDP ampliado.
2. **Dado** un credito 08 que EXCEDE la apropiacion disponible, **entonces** ProblemDetails del THROW 50260
   (RE-VERIFICAR) y nada se ajusta.
3. **Dado** un contracredito 09 que dejaria el CDP bajo lo COMPROMETIDO, **entonces** THROW 50261 (RE-VERIFICAR),
   bajo lock; sin cambio. (Nota: el tope vive en el proc aunque la vista `_Line_Balance` muestre committed=0, B-01.)
4. **Dado** un acto que mezcla 08 y 09 (no homogeneo), **entonces** THROW 50256 (RE-VERIFICAR; posible 50265).
5. **Dado** una vigencia cerrada, **entonces** THROW 50250/50251 (o trigger 50212 en cabecera).
6. **Dado** un acto que mezcla fuentes SGR y comunes, **entonces** THROW 50257 (regimen no homogeneo).
7. **Dado** una linea que introduce un rubro-fuente-BPIN NO existente en el CDP, **entonces** se rechaza (B-04;
   solo lineas existentes).
8. **Dado** cualquier acto, **entonces** el saldo se lee de la vista, NO recalculado en C# (diff); NO toca los
   tipos 11/12 (aislamiento PAR-1, verificable en el diff).

## 8. Pruebas / gates definidos
- **Unit:** mapeo lineas -> Chain TVP; validacion de homogeneidad -> ProblemDetails; traduccion THROW; enforcement
  numeracion-solo-proc; que la previsualizacion use `vw_Commitment_Availability_Validation`.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; Mcp sin SQL; cero DataTable; **test de
  aislamiento: ningun proyecto de esta unidad referencia los tipos/procs de compromiso (11/12)**.
- **Integracion vs DbsFinanciero (EN SANDBOX; EXECUTE via GRANT o TRAN/ROLLBACK):** criterio 1 (08 happy), un caso
  por THROW ALCANZABLE (50260, 50261, 50256, 50250/51/50212, 50257) RE-VERIFICADO, criterio 3 (floor real vs la
  vista inflada), criterio 8 (saldo por vista). **PRECONDICION: sandbox <=14-jul; sin el, DIFERIR.**
- **Gate final:** APROBADO del adversarial informal en SESION SEPARADA (baseline) [+ checker FORMAL del Analista
  si el sorteo la asigna al gobernado] + arch tests + CI + **F-NOVA-01: cada THROW verificado contra el proc
  desplegado** + verificacion de AISLAMIENTO (manifiesto: no se leyo el hermano) + DoD con evidencia real +
  gates del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Citar 50256/50254 que el proc desplegado NO emite | Criterio falso (F-0246-02) | F-NOVA-01: RE-VERIFICAR contra OBJECT_DEFINITION |
| Usar la vista `_Line_Balance` (committed=0, B-01) para el floor | Saldo inflado, criterio 3 falso-verde | Restriccion 6d: previsualizar con `vw_Commitment_Availability_Validation` |
| Implementar los tipos 11/12 del hermano | CONTAMINACION intra-par PAR-1 | Restriccion 6g + architecture test de aislamiento; manifiesto |
| Sandbox no listo <=14-jul | Criterios de mutacion un-runnable | Precondicion bloqueante; DIFERIR |
| Recalcular topes/saldo en C# | Divergencia con la BD | Restricciones 6a/6c; adversarial punto 2 |
| adversarial en la misma sesion del maker | Contaminacion (tokens no separables) | DoR: adversarial en SESION SEPARADA |

## 10. Prioridad definida
**GOAL-P4** (ajustes de cadena), miembro de **PAR-1** (par FIRME, isomorfo con P4.3). **Pertenencia Q4: DENTRO**
(miembro de par del contraste; criticidad media; proc existente S; 08=10 / 09=7 actos vivos). Severidad s.08:
mutador de disponibilidad. Dependencias: GOAL-P1 + P4.1 (patron congelado, arranca antes) + `Apply_Availability_
Adjustment` (existe, RE-VERIFICAR THROW) + **SANDBOX mutadores <=14-jul (BLOQUEANTE)** + las vistas de saldo de CDP.
AISLAMIENTO PAR-1: leyo_codigo_hermano=NO; hereda SOLO el patron congelado de P4.1; el sorteo asigna baseline/
gobernado; violacion de aislamiento = par CONTAMINADO. Desbloquea: los ajustes operativos de CDP de la cadena.
