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

- **T (timestamp del commit de sello):** [LLENAR-AL-SELLAR: commit hash + ISO-8601 UTC].
- **Semilla del sorteo:** primer pulso del **NIST Randomness Beacon** posterior a T
  (fallback: hash del primer bloque Bitcoin posterior a T). [LLENAR-AL-SELLAR: pulseIndex + valor].
- **Atestacion:** sha256 de este documento + del manifiesto de corpus, registrado via
  `submit_intent` en el hub. [LLENAR-AL-SELLAR: idempotency_key + seq].

---

## 1. Snapshot sha256 del corpus (manifiesto)

El corpus del sello = el conjunto de artefactos cuyo estado se congela. Se computa sha256 de cada
uno + un hash de manifiesto (sha256 del listado ordenado `path  sha256`). Procedimiento el 08-jul:
`sha256sum <archivos> | sort > CORPUS-MANIFEST-etapa1.txt; sha256sum CORPUS-MANIFEST-etapa1.txt`.

| Artefacto | sha256 |
|---|---|
| NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md | [LLENAR-AL-SELLAR] |
| NOVA_ESTUDIO_Protocolo_Medicion.md | [LLENAR-AL-SELLAR] |
| NOVA_ESTUDIO_Anexo_Diseno_Completo.json | [LLENAR-AL-SELLAR] |
| schema_medicion.json (v1.0 congelado) | [LLENAR-AL-SELLAR] |
| schema_defectos.json (v1.0 congelado) | [LLENAR-AL-SELLAR] |
| medicion_ledger.py (scripts nueva-fila/cerrar-fila) | [LLENAR-AL-SELLAR] |
| este SELLO-ETAPA-1 (auto-hash tras congelar) | [LLENAR-AL-SELLAR] |
| medicion_journal.csv del piloto GOAL-P1 (3-8 jul) | [LLENAR-AL-SELLAR] |
| **HASH DE MANIFIESTO** | **[LLENAR-AL-SELLAR]** |

NOTA: el codigo de producto (NOVA/Nova-Budget) NO existe aun (lazy, DECISION-0085); su primer
snapshot atestado es el de GOAL-P1 cuando arranque. El corpus del hub sigue separado del N=500
sellado (Zeus-Protocol, FONDO INTOCABLE): son capas distintas, no se mezclan.

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
| 1 | P4.4 Apply_Obligation_Adjustment | media | [LLENAR-AL-SELLAR: proc existe si/no] |
| 2 | P3.2 Availability Draft | media (cond. DEC cerrada) | [LLENAR-AL-SELLAR] |
| 3 | P3.3 Commitment Draft | media (cond. DEC cerrada) | [LLENAR-AL-SELLAR] |
| 4 | P3.4 Obligation Draft | media (cond. DEC cerrada) | [LLENAR-AL-SELLAR] |
| 5 | P2.3 UI de exploracion | baja (calibra taxonomia D1-D4) | [LLENAR-AL-SELLAR] |
| 6 | P6.3 OpenTelemetry | baja | [LLENAR-AL-SELLAR] |
| 7..N | Get_*_List de BR-C3 / DOC-11 sobre vistas existentes | baja (fabrica de tareas S) | [LLENAR-AL-SELLAR: enumerar UNO A UNO contra el conector readonly; cada vista verificada existente] |

Items dependientes de hardening entran SOLO por enmienda fechada con entrega comprometida.
Asignacion ligero/completo: hash + ancla externa, ESTRATIFICADA por familia/tamano, sellada aqui
(s.6). REGLA DURA: si el Sprint 1 no ejecuta >=10, Q4 se reporta SUBPOTENCIADO (no se rellena).

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

1. Commit atestado (T) de: par_ids + estimates S/M/L + algoritmo + timestamp. [LLENAR-AL-SELLAR].
2. Semilla = primer pulso NIST Beacon posterior a T (fallback: hash primer bloque BTC posterior a T).
3. Asignacion ligero/completo = paridad del primer byte de SHA-256(unidad_id + semilla),
   ESTRATIFICADA por familia/tamano. Verificable por terceros.
4. ORDEN DE ARRANQUE SELLADO (anti supervivencia-endogena): P4.1 -> miembro PAR-1 -> miembro PAR-2.
   Desviarse = enmienda fechada con causa; cada par anulado registra QUE trigger lo mato.
5. DISJUNCION DURA: cada tarea se implementa UNA vez en UN brazo; los pares caen COMPLETOS.

Resultado del sorteo (asignacion por unidad): [LLENAR-AL-SELLAR: tabla unidad -> ligero/completo].

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

## 12. Checklist del dia del sello (08-jul)

- [ ] Piloto GOAL-P1 corrido (3-8 jul); su medicion_journal.csv en el corpus.
- [ ] schema_medicion/defectos congelados a v1.0 (sha256 registrado).
- [ ] Estimates S/M/L de las ~10 unidades emitidos por el Operador ANTES del sorteo.
- [ ] Enumeracion Q4 verificada UNA A UNA contra el conector readonly (s.5 completa).
- [ ] Commit de sello (T) con par_ids + estimates + algoritmo + timestamp.
- [ ] Pulso NIST Beacon posterior a T capturado -> sorteo ejecutado -> tabla de asignacion (s.6).
- [ ] sha256 del manifiesto de corpus (s.1) + de este documento, registrados via submit_intent del hub.
- [ ] GRANT EXECUTE resuelto; mecanismo sandbox de mutadores decidido (<=14-jul, no bloquea el sello).

---

Firmado (pre-registro): asesor del Operador. Atesta: Arquitecto (sha256 via intent del hub).
