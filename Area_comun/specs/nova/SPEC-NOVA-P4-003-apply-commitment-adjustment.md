# SPEC-NOVA-P4-003 - Apply_Commitment_Adjustment (ajuste de compromiso/RP, tipos 11/12) [miembro de PAR-1, isomorfo con P4-002]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Miembro de PAR-1 (par FIRME,
> isomorfo con P4.2 Apply_Availability_Adjustment). HEREDA el patron congelado de P4.1 (SPEC-NOVA-P4-001).
> El sorteo del sello asigna cual miembro es baseline y cual gobernado. Preparada por el Arquitecto (arq+docs)
> FUERA de la ventana medida; el dev MEDIDO NO abre pre-sello. Fuente: NOVA-PRES-03 + NOVA-PRES-05 (Compromiso).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-P4-003 - task_id (hub): TASK-0246 (familia SPECs Sprint 1)
- owner_maker: agente desarrollador de la instancia; repo producto Nova-Budget
- checker: adversarial informal de 12 puntos en **SESION SEPARADA / contexto limpio** (dev != adversarial;
  DIRECTIVA operador 2026-07-04). Brazo baseline: checker vivo = adversarial informal (checker_formal=0); brazo
  gobernado: ADEMAS checker FORMAL del Analista. tokens_adversarial_informal taggeados a la sesion separada.
- arm: **PAR-1 (asignado por el sorteo del sello)** - unit: P4.3 Apply_Commitment_Adjustment (ajuste de compromiso)
- q4_membership: **DENTRO** (miembro de par del contraste; criticidad media, proc existente S). [Declaracion
  explicita OBLIGATORIA -- F-0246-01 bloqueo P3 por omitirla.]
- **isolation: CRITICA (PAR-1).** Isomorfo con P4.2 (Apply_Availability_Adjustment). leyo_codigo_hermano = **NO**:
  redactada SOLO de docs COMPARTIDOS (NOVA-PRES-03 + NOVA-PRES-05) + el patron congelado declarado de P4.1; NO se
  lee la implementacion del hermano. Manifiesto: NOVA-PRES-03/05 + arquitectura + P4-001 (patron) + P4-004
  (plantilla). Riesgo: implementar los tipos del hermano (08/09) "de paso" = CONTAMINACION intra-par.
- **PRECONDICION: READY (sandbox mutadores sellado, adelantado <=14-jul).** Mecanismo construido y sellado por
  el Operador (2026-07-04): ver `SANDBOX-MUTADORES-mecanismo-sellado.md` (BD `DbsFinanciero_SANDBOX` + rol
  `budget_sandbox_verifier` con EXECUTE real, aislamiento verificado, IDENTICO en ambos brazos + RESET
  obligatorio entre miembros/brazos, DECISION-0078). Ya NO bloquea la unidad.
- **measurement:** cache-confound -> mismo runtime que su pareja de par o declarar; captura en err.log (stderr);
  tokens_total_atribuibles. checker_formal=0 baseline; en gobernado el checker formal cuenta.
- **deuda GOAL-P1:** harness test front (apps/nova-web) verde en clon limpio antes de la UI de esta unidad.
- **F-NOVA-01 (re-verificacion, CRITICA -- F-0246-02):** el maker RE-VERIFICA el set EXACTO de THROW del
  `Apply_Commitment_Adjustment` DESPLEGADO via OBJECT_DEFINITION. La familia documentada 50250-50258 + 50262/50263
  es de PRES-03/schema-141; el hermano `Apply_Obligation_Adjustment` probo divergencia (50256->50265; 50254 no
  existe). Codigos de MAYOR riesgo: **50256** (homogeneidad), **50254**. Ningun codigo se hornea sin confirmarlo.
- db_verified_at: objetos de NOVA-PRES-03/05 (BD DbsFinanciero; proc schema/141; 488 compromisos / 635 lineas
  reconciliados); el maker RE-VERIFICA contra la BD desplegada (F-NOVA-01).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio): React+TS+Vite (front sin SQL) / ASP.NET Core .NET 10 en capas + NOVA.Mcp / SQL Server 2025
  via gateways tipados / OpenTelemetry / ProblemDetails. Anti-patrones PROHIBIDOS: WebForms/PageMethods, DataTable
  entre capas, DLLs manuales, capa DATABASE generica, secretos en .config, centinelas -99.

## 1. Objetivo definido
El usuario ajusta un compromiso/RP existente (ampliar credito 11 / reducir contracredito 12) mediante una llamada
ATOMICA a `Budget.Apply_Commitment_Adjustment`, con los topes de la BD (credito <= saldo del CDP padre;
contracredito <= compromiso - obligado), traduciendo THROW a ProblemDetails, sin reimplementar saldos/topes en C#.
- Fuente: NOVA-PRES-03 s.1/s.3/s.4/s.5 + NOVA-PRES-05 (saldos de compromiso) + patron congelado P4.1.
- Calidad: falsable. Bien: "un contracredito 12 que dejaria el compromiso bajo lo OBLIGADO devuelve ProblemDetails
  del THROW 50263 (RE-VERIFICAR contra el proc desplegado) y NO ajusta nada".

## 2. Usuario objetivo definido
Rol **Gestion de presupuesto (ajustes de cadena)**: prepara/revisa el acto en la aplicacion (no hay borrador) y lo
aplica. Supuesto temporal: usuario autenticado con rol presupuesto; policy por operacion via BR-C4 post-Sprint-1.
Isomorfo al usuario del ajuste de CDP (P4.2).

## 3. Alcance definido
Un contrato de mutacion atomico + su preparacion:
- **Tipos (PRES-03 s.1):** 11 credito (ampliar compromiso) / 12 contracredito (reducir compromiso). SOLO ajusta
  LINEAS EXISTENTES (no incorpora rubro-fuente-BPIN nuevos; B-04, hereda el ancla de la linea del compromiso padre).
- **Patron congelado de P4.1: Apply ATOMICO, SIN borrador** (PRES-03 s.5; XACT_ABORT + UPDLOCK/HOLDLOCK).
- Escribe cabecera `Budget.Budget_Adjustment` (serie '' comun / G SGR) + detalle `Budget.Commitment_Line_Adjustment`
  (solo 11/12; un efecto por fila; misma vigencia).
- El saldo del RP se recalcula por vista (`saldo_RP = committed + creditos(11) - contracreditos(12) - obligado_neto`),
  NO en C#. **HOMOGENEIDAD (RN-03): el acto es TODO credito o TODO contracredito.** NO hay cuadre cross-linea (P4.1).

## 4. Fuera de alcance definido
- **Ajuste de CDP (08/09), tipos de OBLIGACION (14):** territorio de P4.2 (hermano de par) y P4.4 -> FUERA
  (AISLAMIENTO PAR-1). Esta unidad es SOLO compromiso (11/12).
- **Modificacion de APROPIACION (01-04):** es P4.1 -> FUERA.
- **Aprobar/crear el compromiso** (`Approve_Commitment_Draft`, P3.3): FUERA (esto ajusta un compromiso existente).
- **Anular:** no hay proc de anulacion de ajuste; FUERA.
- Contabilidad (los ajustes de cadena no postean por movimiento) y reimplementacion de saldos/topes en C#.

## 5. Contenido / assets definidos
- **BD (RE-VERIFICAR; F-NOVA-01):**
  - Proc: `Budget.Apply_Commitment_Adjustment` (schema/141; XACT_ABORT, UPDLOCK/HOLDLOCK). Firma:
    `@fiscal_year_id, @adjustment_date, @description, @created_by_user_id, @lines, @adjustment_code=NULL`. Devuelve
    id, code, type, regimen.
  - TVP: `Budget.Chain_Adjustment_Line_List` (document_line_id, effect, amount).
  - Cabecera `Budget.Budget_Adjustment` (schema/050; UNIQUE vigencia+code; trigger 50212; cascada). Detalle
    `Budget.Commitment_Line_Adjustment` (solo 11/12, triggers 50099/50100). Numeracion `Allocate_Document_Number`
    (serie ''/G).
  - Vistas de validacion: `Budget.vw_Commitment_Line_Balance` (saldo del RP = techo de obligaciones; reescrita en
    views/140 para netear el reintegro 14) + `Budget.vw_Commitment_Availability_Validation` (saldo del CDP padre,
    para el tope del credito 11). `Budget.vw_Budget_Adjustment` (leer el acto).
- **THROW (familia DOCUMENTADA 50250-50258 + 50262/50263; RE-VERIFICAR desplegado):** 50250/50251 vigencia
  inexistente/no-abierta (+ trigger 50212); 50252-50255 linea; **50256 acto no homogeneo (RIESGO -> 50265)**;
  50257 regimen no homogeneo; 50258 codigo no unico; **50262 credito 11 > saldo del CDP padre**; **50263
  contracredito 12 > (compromiso - obligado)**.
- **API:** `POST /api/budget/commitments/{id}/adjustments` (aplica; body = tipo 11/12 + lineas + fecha +
  descripcion); ProblemDetails por THROW; devuelve id/code/type/regimen. `POST .../validate` previsualiza contra
  `vw_Commitment_Line_Balance` + `vw_Commitment_Availability_Validation`.
- **UI (apps/nova-web):** formulario de ajuste de compromiso (tipo 11/12, lineas, monto), previsualizacion del
  saldo del RP y el del CDP padre, vigencia explicita; en vigencias cerradas bloqueado.
- **Capa Application:** `NOVA.Application/Budget/CommitmentAdjustments/` (ApplyCommitmentAdjustment: mapea lineas ->
  Chain_Adjustment_Line_List; valida homogeneidad ANTES; traduce THROW).
- **Referencias:** NOVA-PRES-03 (s.1/s.3/s.4/s.5), NOVA-PRES-05 (saldos compromiso, formula RP), P4-001 (patron
  congelado), NOVA-GOAL-001 (P4). (NO se lee el hermano P4.2 ni su implementacion -- aislamiento PAR-1.)

## 6. Restricciones tecnicas definidas
- Heredadas: 10 reglas de NOVA-GOAL-001 (React nunca SQL; MCP nunca SQL; C# no reimplementa saldos/topes/
  numeracion; gateways tipados; cero DataTable) + stack + **patron congelado de P4.1**.
- Propias:
  - (a) Mutacion SOLO por `Apply_Commitment_Adjustment` (Apply atomico); jamas DML ni recalculo en C#.
  - (b) **HOMOGENEIDAD (RN-03):** el acto es todo 11 o todo 12; validado en aplicacion Y en el proc (50256, RE-VERIFICAR).
  - (c) **TOPES (RN-07/08):** credito 11 <= saldo del CDP padre (50262); contracredito 12 <= compromiso - obligado
    (50263, bajo lock, en el proc). La app NO los recalcula.
  - (d) **PREVISUALIZACION usa `vw_Commitment_Line_Balance` (saldo RP) + `vw_Commitment_Availability_Validation`
    (saldo CDP padre para el tope del 11).** El saldo del RP netea obligado (formula PRES-05 s.3.2).
  - (e) Solo LINEAS EXISTENTES (B-04): no incorporar rubro-fuente-BPIN nuevos; hereda el ancla del compromiso padre.
  - (f) Numeracion solo por `Allocate_Document_Number`; DTOs 1:1; THROW->ProblemDetails (RE-VERIFICADO); correlation
    id + task_id + usuario real.
  - (g) **AISLAMIENTO PAR-1:** NO tocar/leer los tipos 08/09 (CDP, P4.2) ni su implementacion.

## 7. Criterios de aceptacion definidos (Given/When/Then; +un negativo por THROW ALCANZABLE, re-verificado)
> F-NOVA-01: cada negativo cita el THROW documentado; el maker CONFIRMA el codigo exacto contra OBJECT_DEFINITION
> antes de fijarlo (50256/50254 = mayor riesgo). Los tests de mutacion corren en el SANDBOX.
1. **Dado** un credito 11 valido sobre una linea de compromiso con saldo de CDP padre suficiente, **cuando** aplico,
   **entonces** el proc crea el acto 'G' numerado y `vw_Commitment_Line_Balance` refleja el RP ampliado; el saldo
   del CDP padre (`vw_Commitment_Availability_Validation`) baja.
2. **Dado** un credito 11 que EXCEDE el saldo del CDP padre, **entonces** THROW 50262 (RE-VERIFICAR); nada se ajusta.
3. **Dado** un contracredito 12 que dejaria el compromiso bajo lo OBLIGADO, **entonces** THROW 50263 (RE-VERIFICAR),
   bajo lock; sin cambio.
4. **Dado** un acto que mezcla 11 y 12 (no homogeneo), **entonces** THROW 50256 (RE-VERIFICAR; posible 50265).
5. **Dado** una vigencia cerrada, **entonces** THROW 50250/50251 (o trigger 50212).
6. **Dado** un acto que mezcla fuentes SGR y comunes, **entonces** THROW 50257 (regimen no homogeneo).
7. **Dado** una linea con rubro-fuente-BPIN NO existente en el compromiso, **entonces** se rechaza (B-04; solo
   lineas existentes).
8. **Dado** cualquier acto, **entonces** el saldo se lee de la vista (formula RP netea obligado), NO recalculado en
   C#; NO toca los tipos 08/09 (aislamiento PAR-1, verificable en el diff).

## 8. Pruebas / gates definidos
- **Unit:** mapeo lineas -> Chain TVP; homogeneidad -> ProblemDetails; traduccion THROW; numeracion-solo-proc; que
  la previsualizacion use las vistas de saldo del RP + CDP padre.
- **Architecture tests:** Api no accede SQL directo; React sin SQL; Mcp sin SQL; cero DataTable; **test de
  aislamiento: ningun proyecto de esta unidad referencia los tipos/procs de CDP (08/09)**.
- **Integracion vs DbsFinanciero (EN SANDBOX; EXECUTE via GRANT o TRAN/ROLLBACK):** criterio 1 (11 happy + baja del
  CDP padre), un caso por THROW ALCANZABLE (50262, 50263, 50256, 50250/51/50212, 50257) RE-VERIFICADO, criterio 3
  (floor compromiso-obligado), criterio 8 (saldo por vista). **PRECONDICION: READY (sandbox sellado; ver SANDBOX-MUTADORES-mecanismo-sellado.md).**
- **Gate final:** APROBADO del adversarial informal en SESION SEPARADA (baseline) [+ checker FORMAL del Analista si
  el sorteo la asigna al gobernado] + arch tests + CI + **F-NOVA-01: cada THROW verificado contra el proc
  desplegado** + verificacion de AISLAMIENTO (manifiesto: no se leyo el hermano) + DoD con evidencia real + gates
  del hub verdes + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Citar 50256/50254 que el proc desplegado NO emite | Criterio falso (F-0246-02) | F-NOVA-01: RE-VERIFICAR contra OBJECT_DEFINITION |
| Recalcular el saldo del RP (que netea obligado) en C# | Divergencia con la BD | Restriccion 6a/6d: leer `vw_Commitment_Line_Balance` |
| Implementar los tipos 08/09 del hermano | CONTAMINACION intra-par PAR-1 | Restriccion 6g + architecture test de aislamiento; manifiesto |
| Sandbox no disponible al abrir el dev MEDIDO | Criterios de mutacion un-runnable | Mecanismo sellado READY desde 2026-07-04; si se degradara, DIFERIR |
| No verificar el tope del 11 contra el saldo del CDP padre | Compromiso sobre CDP inexistente | Restriccion 6c: 50262 contra `vw_Commitment_Availability_Validation` |
| adversarial en la misma sesion del maker | Contaminacion (tokens no separables) | DoR: adversarial en SESION SEPARADA |

## 10. Prioridad definida
**GOAL-P4** (ajustes de cadena), miembro de **PAR-1** (par FIRME, isomorfo con P4.2). **Pertenencia Q4: DENTRO**
(miembro de par del contraste; criticidad media; proc existente S; 11=2 / 12=7 actos vivos). Severidad s.08:
mutador de compromiso. Dependencias: GOAL-P1 + P4.1 (patron congelado) + `Apply_Commitment_Adjustment` (existe,
RE-VERIFICAR THROW) + **SANDBOX mutadores READY** (mecanismo sellado) + las vistas de saldo de compromiso/CDP.
AISLAMIENTO PAR-1: leyo_codigo_hermano=NO; hereda SOLO el patron congelado de P4.1; el sorteo asigna baseline/
gobernado; violacion = par CONTAMINADO. Desbloquea: los ajustes operativos de compromiso de la cadena.
