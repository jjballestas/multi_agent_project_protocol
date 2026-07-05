# SELLO ETAPA 1 - Estudio NOVA Budget (pre-registro)

**Referencia:** NOVA-ESTUDIO-SELLO-1 - v0.1 DRAFT del asesor - fecha de redaccion 2026-07-03
**Companeros:** NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md (NOVA-ESTUDIO-001) +
NOVA_ESTUDIO_Protocolo_Medicion.md (NOVA-ESTUDIO-002) + Anexo_Diseno_Completo.json.
**Estado:** DRAFT. Se SELLA <=08-jul (mismo dia que el sorteo), DESPUES del piloto GOAL-P1
(3-8 jul). El sello lo redacta el asesor; el Arquitecto lo ATESTA por sha256 via intent barato
del ledger del hub (entra a la cadena #4). Congela: schema del CSV, nomenclatura, listas por
brazo, pares, pool Q4, plan de analisis. Los campos [LLENAR-AL-SELLAR] se completan el 08-jul.

> REGLA DE ORO DEL SELLO: nada se decide despues de ver datos. Lo que aqui queda congelado no se
> re-abre; cambios post-sello = enmienda fechada via Operador con causa (jamas silenciosa).

---

## 0. Proposito y ancla externa

Este sello pre-registra el diseno confirmatorio ANTES de ver resultados, para que el estudio sea
defendible (anti-HARKing, anti semilla-moldeable). Ancla externa del sello y del sorteo:

- **T (timestamp del commit de sello):** `cbc1ee2d6a344d4db5b69c2f7823cc0bc0aa8b0c` / `2026-07-04T03:52:25Z`
  (commit que introdujo la s.6.1 completa: par_ids + estimates + algoritmo).
- **Semilla del sorteo:** primer pulso del **NIST Randomness Beacon** (chain 2) posterior a T. **pulseIndex
  1844242, timeStamp 2026-07-04T03:53:00.000Z** (el pulso previo, 1844241, es 2026-07-04T03:52:00.000Z,
  ANTERIOR a T; 1844242 es el primero ESTRICTAMENTE posterior). `outputValue` (semilla usada en el
  algoritmo, s.6.1):
  `9CD3E6A0B366DFD164BA63C18CAE7D09B1CD76867DAD8912AEA1061D41E95226A2B0FCB937542D1DC80BC49AA00FE562B030866E9B1706CD76A26A6E5C7379EF`.
  Verificable por terceros en `https://beacon.nist.gov/beacon/2.0/chain/2/pulse/1844242`.
- **Atestacion:** sha256 de este documento (commit `14ecefa`, `46d3fc02...`) + del manifiesto de corpus
  (`bf91b094...`), registrado via `submit_intent` (type `decision`, `DECISION-0091`) en el hub.
  `idempotency_key`: `arquitecto-atesta-DECISION-0091-sello-etapa1-20260704T113700Z`; `seq: 3831`
  (commit `eb30152`). Ver `Area_comun/decisions/DECISION-0091-sello-etapa1-nova-budget.md` para el
  registro completo (corpus, schema v1.0, sorteo).

---

## 1. Snapshot sha256 del corpus (manifiesto)

El corpus del sello = el conjunto de artefactos cuyo estado se congela. Se computa sha256 de cada
uno + un hash de manifiesto (sha256 del listado ordenado `path  sha256`). Procedimiento el 08-jul:
`sha256sum <archivos> | sort > CORPUS-MANIFEST-etapa1.txt; sha256sum CORPUS-MANIFEST-etapa1.txt`.

> PRE-ARMADO por el Arquitecto (ensayo 2026-07-04, RUNBOOK-ENSAYO-atestacion-sello-etapa1.md s.6). Los 6
> artefactos ESTABLES ya tienen su sha256 FINAL (no cambian). Solo se RECOMPUTAN el dia del sello: los 2
> schema (freeze v-piloto->v1.0) + el auto-hash de ESTE SELLO (tras llenar) + el HASH DE MANIFIESTO.

| Artefacto | sha256 | estado |
|---|---|---|
| NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md | ef1e56e7c1b950559d8e3952231662040a1008999baf6002eb28d7671b2e2a41 | FINAL |
| NOVA_ESTUDIO_Protocolo_Medicion.md | de38530acfd927bb9c4683224a85863ca8b6ae85de5b8cd0ab09c172185969b1 | FINAL |
| NOVA_ESTUDIO_Anexo_Diseno_Completo.json | 4a52ff58f1363f005ee8daaa72800cad065a3d0da3408422fb4c4a59be835c7c | FINAL |
| schema_medicion.json (v1.0 congelado, 2026-07-04) | 700565a206d7066fdb08e48abceed249014569937c86ac202b3d0f57b154c23e | **FINAL (v1.0)** |
| schema_defectos.json (v1.0 congelado, 2026-07-04) | 737fd4f5c379b9e96ceb160891ba6117a4d589d96fb8f5b0c612f1e74e36e8dd | **FINAL (v1.0)** |
| medicion_ledger.py (scripts nueva-fila/cerrar-fila) | 3e92cca5962f88ff3e77286e263ea20d2b5f461e6555454fec776c99e5595344 | FINAL |
| este SELLO-ETAPA-1 (auto-hash tras congelar) | [SE COMPUTA AL FINAL, tras este ultimo commit del doc -- ver DECISION del sello para el valor atestado] | dia-de |
| medicion_journal.csv del piloto GOAL-P1 (fila REAL cerrada+atestada+ratificada) | d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5 | **FINAL (REAL, ratificado)** |
| **HASH DE MANIFIESTO** | **SE COMPUTA sobre las 9 filas finales -- ver DECISION del sello para el valor atestado y el archivo CORPUS-MANIFEST-etapa1.txt** | dia-de |

NOTA: el codigo de producto Nova-Budget YA EXISTE (GOAL-P1 done, commit 02f5d5a); su primer snapshot atestado
es el journal REAL de GOAL-P1 (fila d2a13216, tokens_total_atribuibles=165844, degradacion ex-ante). El corpus
del hub sigue separado del N=500 sellado (Zeus-Protocol, FONDO INTOCABLE): capas distintas, no se mezclan.

**HALLAZGOS DEL PILOTO GOAL-P1 (para el freeze del schema v1.0):** (1) tokens_total_atribuibles = moneda
confirmatoria del brazo baseline (el desglose por cubeta NO es capturable del runtime codex-exec; solo el total
cumulativo en STDERR/err.log). Q4 total-vs-total INTACTO; Q1 degrada a total-marginal. (2) El mecanismo de
captura lee err.log (no out.log). (3) tokens_adversarial_informal NO separable en GOAL-P1 (adversarial in-session);
de P2 en adelante el adversarial es SESION SEPARADA -> taggable; cache no aislable -> ambos brazos MISMO runtime o
declarar cache-confound. Al congelar schema v1.0 el 08-jul, hornear estos 3 puntos.

---

## 2. Tabla de nomenclatura (congelada)

| Campo | Valores / formato |
|---|---|
| tarea_id | `NB-<familia>-<n>` (p.ej. NB-P4-2); GOAL-P1 y unidades del NOVA_PROMPT conservan su id de origen |
| brazo | baseline / gobernado / gobernado_ligero / gobernado_completo |
| familia | P1..P6 (fase del proceso presupuestal), BR-Cx, DOC-xx |
| par_id | PAR-1 / PAR-2 / PAR-D / NA |
| rol_en_par | miembro / primera_unidad / fundacion / calibracion / no_par / overhead_fijo / frontera_fix |
| orchestration_mode | mono / peones / mixto (medicion de peones; ver s.9) |
| estado_final | done / abandonada / truncada / bloqueada |
| tag_incidente_maquinaria | regimen / arranque / incidente / NA (overhead-fijo) |
| detector (defectos) | gate_determinista / adversarial_informal / checker_formal / operador_uso_real / herencia_gobernada |

El schema completo (52 columnas medicion + 9 defectos) se congela por referencia a
`schema_medicion.json` / `schema_defectos.json` v1.0 (s.8).

---

## 3. Lista cerrada por brazo con criticidades

### 3.1 Regla determinista de criticidad (sellada)
La criticidad es de la **TAREA**, NO de la brecha: la severidad Alta de una brecha seccion-08 NO
se hereda a la tarea. Clasificacion determinista:
- **ALTA:** mutadores de frontera de dominio sensible (Treasury/Payroll/Pagos), cierres de
  vigencia, cross-dominio. -> FUERA del pool Q4 (solo descriptivas).
- **MEDIA:** mutadores de ajuste sobre procs existentes (Apply_*_Adjustment), drafts con DEC.
- **BAJA:** lecturas / Get_*_List sobre vistas existentes, UI de exploracion.
Solo MEDIA y BAJA entran al pool Q4.

### 3.2 BASELINE (ventana 3-25 jul, repo de producto NOVA baseline)
| Unidad | Criticidad | Nota |
|---|---|---|
| GOAL-P1 completo (sln, React, health/OpenAPI/ProblemDetails/correlation-id+task_id, arch tests, CI) | fundacion | EXCLUIDA del contraste. Unica que abre antes del sello (03-jul). Piloto de medicion. |
| P2.1 read model de parametros (M) | media | mandada por el GOAL; fuera de contraste |
| P2.2 reporte de ejecucion presupuestal (M) | media | miembro baseline ANCLADO de PAR-D; spec_prepagado=true; activa paridad DbsFinanciero vs SNJDC |
| P4.1 Apply_Budget_Modification (M) | media | pattern-setter familia ajustes; EXCLUIDA del contraste; patron se CONGELA al arrancar miembro PAR-1; PRECONDICION sandbox mutadores <=14-jul |
| Miembro baseline PAR-1 (sorteo) | media | {P4.2 Apply_Availability_Adjustment, P4.3 Apply_Commitment_Adjustment} (S/S, procs existentes, 435 CDP/488 compromisos); inicia <=17-jul |
| Miembro baseline PAR-2 (CONDICIONAL) | media | {Annul_Availability_Certificate, Annul_Commitment} (M/M) SOLO superficie API; condicion: nova-hardening entrega ambos procs <=15-jul; si no, PAR-2 cae |

### 3.3 GOBERNADO (Sprint 1, post-30-jul, instancia Nova-Budget)
- Miembros gobernados de PAR-1 / PAR-2 (si vive), REGLA DE AISLAMIENTO: prohibido leer fuentes del
  hermano baseline (rutas selladas), manifiesto verificado por el Analista, columna
  leyo_codigo_hermano; heredan SOLO el patron congelado de P4.1. Violacion = par CONTAMINADO.
- Miembro gobernado de PAR-D: Get_*_List de BR-C3 sobre vistas existentes (verificadas readonly en
  el sello); criticidad baja; fase SPEC excluida del delta (simetria con spec_prepagado de P2.2).
- FAMILIA P3 COMPLETA: P3.1 Initial Budget Draft (primera_unidad, alcance congelado), P3.2/P3.3/P3.4
  Drafts (elegibles al pool Q4 si su DEC cerrada al sello Etapa 2), P3.5 Payment Draft (alta, fuera Q4).
- BR-C4 autorizacion por operacion: preasignada al gobernado post-Sprint-1.
- Fila FRONTERA-FIX: remediacion de hallazgos de la revision de frontera P1; fuera de AMBOS contrastes.

---

## 4. Tabla de pares (Q3 descriptivo)

| Par | Fuerza | Miembros | Condicion / trigger de caida |
|---|---|---|---|
| PAR-1 | FIRME (incondicional) | P4.2 Apply_Availability_Adjustment vs P4.3 Apply_Commitment_Adjustment (S/S isomorfas, procs existentes) | ninguna; es el par ancla |
| PAR-2 | CONDICIONAL-hardening | Annul_Availability_Certificate vs Annul_Commitment (M/M, solo superficie API) | nova-hardening entrega ambos procs verificados <=15-jul; si no, PAR-2 CAE completo (trigger objetivo registrado). El dev JAMAS crea los procs (regla 8) |
| PAR-D | DEBIL (tipo-emparejado no isomorfo) | P2.2 reporte (baseline, anclado, spec_prepagado) vs Get_*_List BR-C3 (gobernado, baja) | comparacion SOLO sobre fases post-SPEC |

ESCENARIO BASE HONESTO: 1 par firme (PAR-1) + PAR-D; PAR-2 es upside.
ANALISIS Q3: dot plot par-a-par + mediana de diferencias pareadas. **SIN tests inferenciales**
(max 3 pares); prohibido medias/IC/regresiones. Toda lectura Q3 = COTA condicionada, no puntual.
PAR-3/PAR-4/PAR-5 ELIMINADOS (grupo-A prohibido / peso muerto).

---

## 5. Enumeracion nominal Q4 (n>=10) + verificacion readonly

Pool Q4 (contraste causal ligero-vs-completo, contemporaneo post-30-jul, ITT, solo media/baja),
ENUMERADO NOMINALMENTE demostrando n>=10 SIN items grupo-A:

| # | Unidad | Criticidad | Verificacion readonly (vista/proc existe) |
|---|---|---|---|
| 1 | P4.4 Apply_Obligation_Adjustment | media | SI -- verificado via conector readonly (NOVA-PRES-03/06, 2026-07-03); db_verified_at en SPEC-NOVA-P4-004 |
| 2 | P3.2 Availability Draft | media (cond. DEC cerrada) | SI -- verificado readonly (NOVA-PRES-04, 2026-07-03); db_verified_at en SPEC-NOVA-P3-002 |
| 3 | P3.3 Commitment Draft | media (cond. DEC cerrada) | SI -- verificado readonly (NOVA-PRES-05, 2026-07-03); db_verified_at en SPEC-NOVA-P3-003 |
| 4 | P3.4 Obligation Draft | media (cond. DEC cerrada) | SI -- verificado readonly (NOVA-PRES-06, 2026-07-03); db_verified_at en SPEC-NOVA-P3-004 |
| 5 | P2.3 UI de exploracion | baja (calibra taxonomia D1-D4) | N/A -- frontend, no consume BD directo; verifica contra contratos OpenAPI del vertical slice P1 (SPEC-NOVA-P2-003) |
| 6 | P6.3 OpenTelemetry | baja | N/A -- infra, no consume objetos BD; verifica contra instrumentacion desplegada del vertical slice P1 (SPEC-NOVA-P6-003) |
| 7..10 | Get_Availability_Certificate_List / Get_Commitment_List / Get_Obligation_List / Get_Payment_List (BR-C3) | baja (fabrica de tareas S) | SI -- las 4 vistas de saldo verificadas existentes via conector readonly (NOVA-PRES-11, 2026-07-03); db_verified_at en SPEC-NOVA-P2-004. Los procs Get_*_List AUN NO existen (se crean en Sprint 1); solo las vistas que consultan son readonly-verificadas. |

Items dependientes de hardening entran SOLO por enmienda fechada con entrega comprometida.
Asignacion ligero/completo: hash + ancla externa, por-unidad (reportada por estrato M/S, NO balanceada
dentro de estrato), sellada aqui (s.6). REGLA DURA: si el Sprint 1 no ejecuta >=10, Q4 se reporta
SUBPOTENCIADO (no se rellena).

NOTA DE INDEPENDENCIA (cosecha NOVA-DEV ronda 8, SPEC-NOVA-P2-004, commit e6cd82b): los items #7..N
(Get_*_List de BR-C3) son una FAMILIA CASI ISOMORFA (~4 tareas: Availability/Commitment/Obligation/
Payment List; mismo patron de lectura 15-param sobre distintas vistas de saldo). Son LOAD-BEARING para
n>=10 (6 unidades nombradas + 4 Get_*_List = 10). REGLA DE ANALISIS SELLADA: se tratan como CLUSTER
CORRELACIONADO en Q4; el n EFECTIVO independiente es < 10 (aleatorizar ligero/completo sobre 4 tareas de
la misma forma prueba la misma forma 4 veces). El reporte por estrato (s.6) organiza la LECTURA de la
asignacion, no equilibra ni corrige la correlacion (el algoritmo es paridad por-unidad, no ajustada por
estrato, s.6.1); Q4 declara el n efectivo reducido (anti-sobreventa). El Get_*_List cumple DOBLE ROL
(miembro gobernado de PAR-D en Q3 + fabrica en Q4): NO es doble-conteo, son contrastes pre-registrados
distintos (Q3 descriptivo/cota vs Q4 causal ligero/completo); su fase SPEC se excluye del delta (simetria
con el spec_prepagado de P2.2). Los procs Get_*_List NO existen aun (se crean); su paridad se verifica
contra las VISTAS existentes (readonly), sin GRANT EXECUTE.

NOTA DE VERIFICACION (cosecha NOVA-DEV F-NOVA-01, commit ff68ee8): el conector readonly
`nova_sql_connector_readonly_s9` tiene SELECT/VIEW DEFINITION pero NO EXECUTE (Msg 229). Por tanto la
verificacion de EXISTENCIA de cada proc/vista de este pool (OBJECT_DEFINITION/sys.objects) es realizable
YA sin GRANT EXECUTE -> los `[LLENAR-AL-SELLAR: proc existe]` se completan al sellar por existencia. Las
pruebas de PARIDAD (ejecutar el proc/Get_*) requieren GRANT EXECUTE al rol de verificacion (pendiente del
Operador, checklist s.12). P3.1 NO pertenece a este pool (es primera_unidad/pattern-setter, excluida del
contraste central; su patron congelado = aprobacion-via-proc + gateway tipado + saldo-de-vista, no el
supuesto temporal de autorizacion B-05).

---

## 6. Sorteo con ancla externa (anti semilla-moldeable)

1. Commit atestado (T) de: par_ids + estimates S/M/L + algoritmo + timestamp. **PRE-COMMIT LISTO (s.6.1
   abajo); solo falta la semilla-del-dia.**
2. Semilla = primer pulso NIST Beacon posterior a T (fallback: hash primer bloque BTC posterior a T).
3. Asignacion ligero/completo = paridad del primer byte de SHA-256(unidad_id + semilla), POR-UNIDAD
   (no ajustada por estrato); REPORTADA por estrato (M/S) para legibilidad, pero NO balanceada dentro de
   estrato -- con n=6/n=4 el azar puede rendir un estrato desbalanceado (p.ej. 5-1 o 4-0) y eso se
   REPORTA honesto, no se corrige ni se re-sortea. Verificable por terceros. Convencion EXACTA en s.6.1
   (paso 2-3).
4. ORDEN DE ARRANQUE SELLADO (anti supervivencia-endogena): P4.1 -> miembro PAR-1 -> miembro PAR-2.
   Desviarse = enmienda fechada con causa; cada par anulado registra QUE trigger lo mato.
5. DISJUNCION DURA: cada tarea se implementa UNA vez en UN brazo; los pares caen COMPLETOS.

**Resultado del sorteo (asignacion por unidad, SELLADO):** semilla = pulso NIST 1844242 (s.0). Computado
con el algoritmo exacto de s.6.1 (orden alfabetico, `h=SHA-256(tarea_id+"|"+semilla)`, `h[0] mod 2`):

| tarea_id | h (SHA-256 completo) | h[0] | asignacion |
|---|---|---|---|
| NB-BRC3-1 | `9dced029a19554937646ce2c25e15b801c4c9ca1a730a386890f6eae20755039` | `0x9d` (157, impar) | **ligero** |
| NB-BRC3-2 | `11bdb4bc209380bb2767c103c16cb198e093f7cd42fe65c213b26913fe254b33` | `0x11` (17, impar) | **ligero** |
| NB-BRC3-3 | `1b1409e62cc5f540ff63ac7762f653f1b461b97c38702339be93ba0e34ece7bd` | `0x1b` (27, impar) | **ligero** |
| NB-BRC3-4 | `3c8db091612154effa41a63997ad3873d2a9085ac20521eb5954b0c9a223f7a4` | `0x3c` (60, par) | **completo** |
| NB-P2-3 | `7e36c48811198e8edebffe379a1d2fe4ff742cdcecec1a7f94f283590717e3b2` | `0x7e` (126, par) | **completo** |
| NB-P3-2 | `6b23a918406abc4550d826dd537426a5642e9dc62d63ea0080811f106faeb4e4` | `0x6b` (107, impar) | **ligero** |
| NB-P3-3 | `4906ca958436ab3ffe149e02f008d604e0cdd65ec4bf9b7f117e5a5f9d22fc6e` | `0x49` (73, impar) | **ligero** |
| NB-P3-4 | `ff050df100b0b50891c5938b32239072a3647bfe05630ffaf2eb102772f3b7cb` | `0xff` (255, impar) | **ligero** |
| NB-P4-4 | `e5b20665ed3a42c06c97e44a1c758778f5a618e9ad637b218f5b4c22fe8adc50` | `0xe5` (229, impar) | **ligero** |
| NB-P6-3 | `111503133d717f5a12be246ef19e3892ae2661ce02c0339c5f0d20bbbb5a9620` | `0x11` (17, impar) | **ligero** |

**Reporte por estrato (honesto, sin corregir, s.6.1 paso 3):**
- Estrato S (BR-C3 cluster, n=4): 1 completo (NB-BRC3-4) / 3 ligero (NB-BRC3-1/2/3).
- Estrato M (diversas, n=6): 1 completo (NB-P2-3) / 5 ligero (NB-P3-2, NB-P3-3, NB-P3-4, NB-P4-4, NB-P6-3)
  -- desbalance 5-1 real por azar de la semilla. Se REPORTA sin corregir (regla ex-ante de s.6.1 paso 3:
  n=6 es insuficiente para forzar paridad sin introducir un criterio ad-hoc post-semilla).

**Total global: 2 completo (NB-BRC3-4, NB-P2-3) / 8 ligero, de 10 unidades.** Resultado FINAL, verificable
por terceros recomputando con la semilla publicada arriba.

### 6.1 Artefacto PRE-COMMIT del sorteo (par_ids + estimates + algoritmo + timestamp)

> Preparado por el Arquitecto (DIRECTIVA operador 2026-07-04, profundiza-cola-sello-e-infra). Congela
> TODO lo que no depende de la semilla; el UNICO pendiente-del-dia es la semilla NIST (paso 3 abajo).
> Fuente de los 10 tarea_id/estimates: `ESTIMATES-Q4-para-sorteo.md` (LOCKEADOS por el Operador,
> 2026-07-03; no se re-generan aqui, solo se incorporan con su tarea_id y par_id formales).

**Tabla congelada (10 unidades, par_id + estrato + estimate, orden alfabetico por tarea_id):**

| tarea_id | Unidad | familia | estrato | par_id | criticidad | estimate S/M/L |
|---|---|---|---|---|---|---|
| NB-BRC3-1 | Get_Availability_Certificate_List | BR-C3 | S (cluster) | PAR-D | baja | S |
| NB-BRC3-2 | Get_Commitment_List | BR-C3 | S (cluster) | PAR-D | baja | S |
| NB-BRC3-3 | Get_Obligation_List | BR-C3 | S (cluster) | PAR-D | baja | S |
| NB-BRC3-4 | Get_Payment_List | BR-C3 | S (cluster) | PAR-D | baja | S |
| NB-P2-3 | P2.3 UI de exploracion (shell) | P2 | M (diversa) | NA | baja | M |
| NB-P3-2 | P3.2 Availability Draft / CDP | P3 | M (diversa) | NA | media (cond. DEC) | M |
| NB-P3-3 | P3.3 Commitment Draft / RP | P3 | M (diversa) | NA | media (cond. DEC) | M |
| NB-P3-4 | P3.4 Obligation Draft | P3 | M (diversa) | NA | media (cond. DEC) | M |
| NB-P4-4 | P4.4 Apply_Obligation_Adjustment (reintegro 14) | P4 | M (diversa) | NA | media | M |
| NB-P6-3 | P6.3 OpenTelemetry / Observabilidad | P6 | M (diversa) | NA | baja | M |

- **par_id = PAR-D** para los 4 `Get_*_List` (doble rol sellado en s.5 NOTA DE INDEPENDENCIA: miembro
  gobernado de PAR-D en Q3 + fabrica/cluster de tareas S en Q4). **par_id = NA** para las 6 unidades
  restantes: no son miembro de ningun par Q3 (PAR-1/PAR-2 se resuelven aparte, s.3.2/s.4); son SOLO
  pool Q4.
- **Estratos:** M = 6 unidades diversas (una por familia/unidad distinta); S = las 4 `Get_*_List`
  (cluster casi-isomorfo, n efectivo <10 declarado en s.5). El sorteo corre POR ESTRATO.
- GOAL-P1, P2.1, P2.2 y P4.1 (fundacion/pattern-setter/PAR-D-baseline-anclado) **NO entran a este pool**
  (s.3.2; excluidos del contraste). PAR-1/PAR-2 (miembro baseline-vs-gobernado) usan el ORDEN DE ARRANQUE
  sellado de s.6 paso 4, no esta tabla.

**Algoritmo (convencion EXACTA, fijada AHORA, antes de conocer la semilla):**

1. Para cada `tarea_id` de la tabla, en ORDEN ALFABETICO (evita eleccion de orden post-hoc), computar
   `h = SHA-256(tarea_id + "|" + semilla)` (concatenacion UTF-8 literal, separador `|`).
2. Tomar el primer byte de `h` (`h[0]`, 0-255). Si `h[0] mod 2 == 0` -> asignacion **completo**
   (gobierno completo); si `h[0] mod 2 == 1` -> asignacion **ligero** (gobierno ligero). Convencion
   fija, sin discrecion el dia del sorteo.
3. El sorteo corre POR ESTRATO (M y S por separado) solo para que la asignacion sea LEGIBLE por
   estrato; el algoritmo del paso 2 NO se ajusta por estrato (mismo hash, misma regla de paridad en
   ambos). **Declaracion ex-ante (anti-HARKing):** con n=6 y n=4 el paso 2 puede rendir un estrato
   desbalanceado (p.ej. 5-1 o 4-0) por puro azar de la semilla; eso NO se re-sortea ni se fuerza a
   50/50 -- se REPORTA como hallazgo honesto del sorteo (ver s.11 riesgo 1, Q3-pares/Q4 potencia).
4. Verificable por terceros: cualquiera puede recomputar `h` con la semilla publicada (NIST Beacon) y
   los `tarea_id` de esta tabla, y reproducir la tabla de asignacion resultante byte a byte.

**Timestamp T = `cbc1ee2d6a344d4db5b69c2f7823cc0bc0aa8b0c` / `2026-07-04T03:52:25Z`** (commit que introdujo
esta tabla 6.1 completa: par_ids + estimates + algoritmo, ver s.0). Queda anclado externamente cuando
se registre via `submit_intent` type `decision` (sha256 de este documento + este hash) en el ledger del
hub -- pendiente de ejecutar como parte del checklist s.12 (no bloquea seguir completando el resto del
sello). Desde este momento, la semilla que se use para el sorteo DEBE ser de un pulso NIST posterior a
este timestamp; una semilla anterior invalida el sorteo (seria pre-T, manipulable).

---

## 7. Plan de analisis (Q1-Q5) + que afirma / NO afirma

**Preguntas confirmatorias e INCONDICIONALES:**
- **Q1 (costo):** costo MARGINAL del paquete de gobierno por tarea (cubetas 3+4) vs costo FIJO, por
  SEPARADO, con y sin overhead. 4 cubetas de tokens; regimen vs arranque separados (tag incidente).
- **Q2 (calidad):** defectos post-entrega clase (b) con PARIDAD DE DETECTOR (unica serie confirmatoria
  limpia) + FUGA DE OBSERVACIONES (emitidas vs registradas-con-dueno). Plan B si defectos_post~0
  (efecto techo): hallazgos pre-integracion por severidad, como metrica DISTINTA.
- **Q4 (causal, la unica):** ligero vs completo, contemporaneo post-30-jul, aleatorizado (s.6), ITT,
  n>=10. Mide el valor marginal de MAS gobierno, no gobierno-vs-nada.

**Descriptivo (NO confirmatorio):** Q3 par-a-par (dot plot, sin tests); conteos governado-vs-baseline
como COTA condicionada (confound de orden bidireccional, s.5 del Particion).

**QUE AFIRMA Y QUE NO (delimitacion sellada, anti-sobreventa):**
- El estudio da: instrumentacion probada + Q4 causal + una serie honesta de calidad (el checker
  formal atrapa lo que el gate informal dejo pasar) + evidencia de transferibilidad (segunda
  instancia en dominio real, distinta del N=500 auto-dogfood de Zeus-Protocol).
- El estudio NO da: un veredicto causal "el gobierno mejora la calidad". OJO: maker!=checker YA existe
  en AMBOS brazos (el baseline tiene gate adversarial informal); el tratamiento medido es el checker
  FORMAL atestado + la maquinaria, no "separar maker de checker". El veredicto definitivo de compra
  se DIFIERE a una replica employee-run pre-registrada en Nova Accounting.

---

## 8. Schema del CSV congelado

Se congela por referencia a `schema_medicion.json` v1.0 (52 columnas: identidad/diseno, ciclo,
peones, costo, calidad, defectos/trazas) y `schema_defectos.json` v1.0 (9 columnas). Reglas duras:
- 6 campos para ABRIR (tarea_id, brazo, par_id, estimate_previo_SML, criticidad, fecha_commit_estimate);
  el resto es de cierre; campo sin artefacto-fuente = NA sin culpa. par_id admite valor "NA".
- CSV APPEND-ONLY via journal + vista materializada (nueva-fila/cerrar-fila); jamas editar a mano.
- 4 CUBETAS de tokens: dev / adversarial_informal / checker_formal (0 baseline) / coordinacion_gobierno
  (0 baseline). tokens_cache_reads y tokens_peones = SUBSETS informativos, EXCLUIDOS de confirmatorias.
- DEGRADACION EX-ANTE: si el desglose por rol es incapturable en baseline, la confirmatoria cae a
  tokens_total_atribuibles AHORA por sello, no por improvisacion en agosto.

---

## 9. Medicion de peones + regla de aislamiento (sellada)

- Campos: orchestration_mode (mono/peones/mixto), peones_n, peon_revivals_n, peon_modelos, tokens_peones
  (subset, no doble-contar, fuera de confirmatorias).
- REGLA DE AISLAMIENTO: los peones son VARIABLE DISTINTA del gobierno atestado. El brazo gobernado del
  contraste central se mantiene MONO-orquestado; si aparece un peon se REGISTRA (descriptivo) pero NO
  convierte el brazo en tratamiento peones. El EFECTO de los peones se mide SOLO en F6 (mono-vs-peones
  bajo gobierno completo), aislado. Mezclarlos en el contraste central confunde Q1/Q4: prohibido.

---

## 10. Reglas duras + degradacion ex-ante (selladas)

- sesion = tarea; multiples se suman; las fallidas son costo real; sesion mixta se atribuye completa a
  la principal con sesion_contaminada=true; prohibido prorratear overhead oculto.
- AISLAMIENTO DE TEETHING: remediacion de incidentes de maquinaria -> filas OVERHEAD-FIJO con tag
  incidente, JAMAS a la cubeta de una tarea. Cuentan desde 30-jul; instrumentacion pre-30-jul aparte.
- RECONCILIACION post-ventana (26-29 jul, Analista read-only): mapea todo commit/rama/log del repo
  producto contra los tarea_id; sesiones sin fila = abandonada retroactiva; huerfanos se PUBLICAN como
  metrica de integridad del propio estudio.
- SLA del gate: adversarial en 48h, veredicto integracion 48h, una gracia de 72h/ventana. STOP TOTAL si
  la latencia supera SLA post-gracia en 2 entregas seguidas. PISO MINIMO VIABLE: P1 completa + miembro
  baseline PAR-1. La ventana NO se extiende. Tarea que excede 2x su estimate: se registra, JAMAS cambia
  de brazo.

---

## 11. Riesgos declarados (5 mayores; lista completa en el anexo del sello)

1. Q3-pares casi anecdotico por diseno honesto (1 par firme): aceptado.
2. ABIERTA: el aislamiento intra-par atrapa lecturas de fuente, no el conocimiento latente del modelo;
   la degradacion condicional a exploratorio acota, no cierra.
3. La capacidad real del Sprint 1 manda sobre Q4: <10 tareas -> Q4 subpotenciado (sellado), no se rellena.
4. Sello del 08-jul denso para operador con R9 vigente; sello apurado con estimates malos = modo de
   fallo mas toxico restante.
5. Veredictos baseline auto-reportados (pseudo-atestacion git): asimetria de calidad de dato entre
   brazos, declarada como limite, no corregible por diseno.

---

## 11.1 Calendario y triggers consolidado (sin decisiones nuevas; consolida fechas ya selladas arriba)

| Fecha / ventana | Evento | Trigger / condicion | Fuente |
|---|---|---|---|
| 2026-07-03 a 08 | Piloto GOAL-P1 (fundacion) corre; unico item que abre antes del sello | Ya cerrado (done, journal real d2a13216) | s.3.2, s.1 |
| <=2026-07-08 | SELLO Etapa 1: sorteo + atestacion sha256 | Commit T (s.6.1) + semilla NIST posterior a T | s.6, s.12 |
| <=2026-07-14 | Sandbox de mutadores sellado (precondicion P4.x) | Construido y sellado (2026-07-04, adelantado); ver SANDBOX-MUTADORES-mecanismo-sellado.md | Area_comun/specs/nova/ |
| <=2026-07-15 | PAR-2 (Annul_Availability_Certificate / Annul_Commitment) confirma o cae | nova-hardening entrega AMBOS procs verificados; si no, PAR-2 CAE completo | s.4 |
| <=2026-07-17 | Miembro baseline PAR-1 inicia (P4.2 o P4.3, sorteo) | Tras P4.1 (patron congelado) | s.3.2 |
| 2026-07-26 a 29 | Reconciliacion post-ventana (Analista, read-only) | Mapea commits/ramas del repo producto contra tarea_id; huerfanos = abandonada retroactiva | s.10 |
| 2026-07-30 | Abre Sprint 1 gobernado (dev MEDIDO de P2/P3/P4 + Q4) | Piso minimo viable: P1 completa + miembro baseline PAR-1 (s.10); si no se cumple, STOP-total por SLA | s.4, s.10, s.12 |
| Post-30-jul, contemporaneo | Q4 causal ligero-vs-completo ejecuta (n>=10 si el Sprint lo permite) | Asignacion de s.6.1 aplicada tras revelar semilla | s.5, s.6 |
| Continuo desde 30-jul | SLA de gate: adversarial 48h, veredicto integracion 48h, 1 gracia 72h/ventana | STOP TOTAL si excede SLA post-gracia en 2 entregas seguidas | s.10 |
| Post-sello (sin fecha fija) | Migracion Nova a instancia Aegis propia; cross-atestacion hub<->instancia | DECISION-0088 (asiento escalonado); pre-diseno en curso (P3 de esta cola) | DECISION-0088 |

Ningun triger nuevo se introduce aqui; esta tabla solo reune fechas/condiciones YA selladas en las
secciones 1/3/4/6/10/12 de este documento, para lectura rapida del operador.

---

## 12. Checklist del sello (ejecutado 2026-07-04, adelantado del 08-jul por DIRECTIVA del Operador)

- [x] Piloto GOAL-P1 corrido (2026-07-03/04); su `medicion_journal.csv` (fila real) en el corpus.
- [x] schema_medicion/defectos congelados a v1.0 (sha256 registrado en s.1).
- [x] Estimates S/M/L de las 10 unidades emitidos por el Operador ANTES del sorteo (`ESTIMATES-Q4-para-sorteo.md`, 2026-07-03).
- [x] Enumeracion Q4 verificada UNA A UNA contra el conector readonly (s.5 completa).
- [x] Commit de sello (T) con par_ids + estimates + algoritmo + timestamp (`cbc1ee2`, s.0/s.6.1).
- [x] Pulso NIST Beacon posterior a T capturado -> sorteo ejecutado -> tabla de asignacion (s.6, pulso 1844242).
- [x] sha256 del manifiesto de corpus (s.1) + de este documento, registrados via submit_intent del hub (DECISION-0091, seq 3831).
- [x] GRANT EXECUTE resuelto; mecanismo sandbox de mutadores decidido (sellado 2026-07-04, adelantado <=14-jul).

---

## 13. ENMIENDA FECHADA 2026-07-05T00:26Z (Arquitecto) - PAR-2 CONDICIONAL -> CONFIRMADO

**No reabre el sello; registra el cumplimiento de la condicion ya sellada en s.4/s.11.1.**

- **Trigger de caida NO se disparo.** La condicion sellada ("nova-hardening entrega AMBOS procs
  verificados <=15-jul, s.4/s.11.1, fila `<=2026-07-15` de la tabla s.11.1") esta **CUMPLIDA y
  ADELANTADA ~10 dias**: el DBA del Operador construyo `Budget.Annul_Availability_Certificate` +
  `Budget.Annul_Commitment` (+ tablas de reverso `Availability_Certificate_Reversal/_Line`,
  `Commitment_Reversal/_Line`, estado `'A'` via MERGE) en `DbsFinanciero_SANDBOX`, con 10/10 pruebas OK:
  existencia, guarda bloqueante hijos-vivos (THROW **50293** anular-CDP-con-RP-activo / THROW **50283**
  anular-RP-con-OBL-viva), camino feliz con cuadre CDP/RP, idempotencia, rollback forzado,
  `SESSION_CONTEXT('tenant_id')` faltante. Smoke con `nova_budget_verifier` OK (ambos ejecutan y
  devuelven los THROW de guarda esperados).
- **PAR-2 flip: CONDICIONAL -> CONFIRMADO.** Fuente: FYI/DIRECTIVA del Operador
  `MSG-20260705-Operador-to-Arquitecto-FYI-PAR2-hardening-entregado-confirmado.md`. Ya NO esta en
  riesgo de caer (s.3.2 fila 110 / s.4 fila 130 quedan HISTORICAS -- su condicion se resolvio a
  CONFIRMADO, no se re-escriben, esta enmienda es la fuente de verdad del estado actual).
- **Enmienda del grant surface (dated, s.5):** `budget_sandbox_verifier` pasa de 105 a **107 permisos**
  (17 EXECUTE + 90 SELECT), sumando las 2 lineas GRANT EXECUTE de `Annul_Availability_Certificate` /
  `Annul_Commitment`. Superficie identica en ambos brazos (regla s.5), verificado por el Operador.
- **Frontera (sin cambio):** los procs `Annul_*` son HARDENING de BD (fuera del estudio medido, regla 8).
  La SUPERFICIE C#/API sobre ellos SI es la unidad MEDIDA (miembro baseline de PAR-2); **construible en
  la ventana, EN COLA detras de P4.1 + el miembro baseline de PAR-1** (orden de arranque sellado s.4/s.6,
  "P4.1 -> miembro PAR-1 -> miembro PAR-2"). NO se promueve antes que P4.1/PAR-1.
- **Nota de dominio (study-relevant, no defecto):** tramo contable NO-OP en CDP/RP es CORRECTO (CDP/RP =
  reserva presupuestal, no movimiento contable; el comprobante inverso solo aplica de
  Obligacion/Pago hacia abajo); auditoria presupuestal (usuario+motivo+task_id) documentada por el DBA.
- **THROW 50293/50283:** anotados para el mapeo a ProblemDetails cuando se construya la superficie C#
  de PAR-2 (no antes).
- **Confirmacion read-only del Analista (opcional, s.14 FYI del Operador):** NO despachada esta sesion
  (P4.1 + TASK-0252 tienen prioridad; el hardening es maker=DBA auto-probado, aceptable por estar fuera
  del estudio). Puede pedirse mas adelante sin bloquear la ruta critica.

---

Firmado (pre-registro): asesor del Operador. Atesta: Arquitecto (sha256 via intent del hub).
