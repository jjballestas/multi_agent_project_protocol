# DRAFT-SPEC F3.3 -- Instrumentacion del estudio (lado-medicion automatizado)

> Autor: Asesor (Vision Nova). Carril: DISENO. Estado: DRAFT para que el Arquitecto lo formalice
> a NOVA-SPEC-T-001 y lo rutee a Codex-maker / Analista-checker.
> Fecha: 2026-07-04. Prior art: DECISION-0033 + SPEC-0079 (cost-attribution-por-handoff, ACEPTADA,
> TASK-0111). Schema congelado: schema_medicion.json v1.0 (52 cols) + schema_defectos.json v1.0 (9 cols),
> sellados en DECISION-0091 (Etapa 1). Plan de analisis: SELLO-ETAPA-1 s.7 (Q1-Q5).

## 0. Por que (proposito del gate)

El sello congelo el SCHEMA y el PLAN de analisis, pero la captura sigue siendo MANUAL
(`medicion_ledger.py` llena filas a mano). Medir a mano el brazo baseline y el gobernado durante
la ventana 3-25 jul es la fuente #1 de error de medicion y el punto ciego de falsabilidad del propio
estudio. F3.3 = la CAPA DE INSTRUMENTACION que automatiza la captura encima de las primitivas ya
aceptadas (SPEC-0079 `cost.attributed`) + el journal congelado, de modo que:

1. el costo se atribuye por `tarea_id` sin transcripcion manual (menos error, mas auditable);
2. los defectos post-entrega entran como evento validado contra el schema (Q2 con paridad de detector);
3. la remediacion de maquinaria se marca como overhead-fijo AUTOMATICAMENTE (aislamiento de teething, s.10);
4. las preguntas Q1-Q5 se computan DETERMINISTAS desde las filas + defectos, con golden.

**Debe estar VIVO antes de que abra el dev medido P2** (baseline se corre con captura automatica,
no reconstruida). Si no llega a tiempo: fallback = captura manual sellada (medicion_ledger.py), sin
bloquear P2 -- pero el objetivo es que P2 sea el primer brazo instrumentado.

## 1. Alcance (3 eventos + 1 motor)

### 1.1 `cost.attributed` AUTOMATICO por tarea_id (extiende SPEC-0079, no reinventa)
- REUSA la primitiva aceptada de SPEC-0079/DECISION-0033 (`applied:false`, plano de protocolo sin texto
  libre, off-by-default). F3.3 anade solo el CABLEADO del lado-estudio, no un evento nuevo.
- Captura: lee el CUMULATIVO de tokens del `err.log` (STDERR) del runtime codex-exec al cierre de la
  sesion de una tarea. **Hallazgo del piloto GOAL-P1, sellado:** el runtime da UN solo cumulativo en
  STDERR (no separa cubetas dev/adversarial/checker/coordinacion). Por tanto:
  - dimension = `task` (subject = `{tarea_id}`), actor = agente emisor;
  - escribe `tokens_total_atribuibles` en la fila de la tarea (columna del schema v1.0);
  - **degradacion EX-ANTE sellada (s.8):** el desglose por cubeta NO se captura del runtime -> las 4
    cubetas por-rol quedan NA salvo cuando el rol corre en SESION SEPARADA. La unica cubeta separable
    hoy es `tokens_adversarial_informal` (adversarial en sesion separada desde P2, DIRECTIVA operador)
    y `tokens_coordinacion_gobierno` (sesion del Arquitecto). El motor NO inventa un split.
- IDEMPOTENCIA: una tarea cerrada dos veces no doble-cuenta (idempotency_key determinista por tarea_id +
  sesion_ids, reusa `cost_attribution_idempotency_key` de SPEC-0079).
- CONFOUND declarado: el total incluye cache no aislable entre brazos -> ambos brazos MISMO tipo de
  sesion/runtime, o `notas_confound = cache-confound` (columna del schema). El motor NO corrige; anota.

### 1.2 `defect.reported` (evento validado vs schema_defectos v1.0)
- Un evento por defecto post-entrega, imputado a la `tarea_id_origen`, VALIDADO contra schema_defectos
  v1.0 (9 cols): taxonomia D1-D4, severidad, `detector` (enum: gate_determinista / adversarial_informal
  / checker_formal / operador_uso_real / herencia_gobernada), `paridad_detector` (bool), `clase` (a/b).
- **PARIDAD DE DETECTOR (clave de Q2):** solo la serie con `paridad_detector=true` es confirmatoria
  limpia (mismo detector disponible en ambos brazos). El evento OBLIGA a declarar el detector; un
  defecto encontrado por un detector que solo existe en el brazo gobernado (checker_formal) se marca
  `paridad_detector=false` y NO entra a la serie confirmatoria -- entra al descriptivo.
- Rechazo: evento que no valida contra el schema (enum fuera de rango, campo de apertura faltante) se
  RECHAZA y se cuenta en `rejected` (nunca se escribe una fila de defecto malformada).

### 1.3 `manual.intervention` (aislamiento de teething, s.10)
- Registra remediacion de incidentes de maquinaria / intervencion manual como fila OVERHEAD-FIJO con
  `tag_incidente_maquinaria` (enum: regimen / arranque / incidente / NA), `rol_en_par=overhead_fijo`.
- REGLA DURA (s.10): estos tokens/tiempo van a una fila OVERHEAD-FIJO, JAMAS a la cubeta de una tarea de
  producto. Instrumentacion pre-30-jul cuenta aparte; regimen cuenta desde 30-jul. El evento fuerza el
  tag para que Q1 separe regimen-vs-arranque sin juicio posterior.

### 1.4 `study_metrics.py` (motor determinista + golden)
Lee el journal materializado (filas v1.0) + los defectos y computa las preguntas del plan s.7. **Cero
aleatoriedad, cero fecha-de-hoy interna** (parametrizar `now`/ventana por argumento -> reproducible):

- **Q1 (costo):** costo MARGINAL del paquete de gobierno por tarea = suma cubetas (3) checker_formal +
  (4) coordinacion_gobierno, vs costo FIJO (overhead-fijo). Reporta CON y SIN overhead, y regimen vs
  arranque SEPARADOS por `tag_incidente_maquinaria`. Como el desglose por cubeta degrada (1.1), Q1 cae a
  total-marginal cuando las cubetas 3/4 no son separables -- el motor lo REPORTA como degradado, no lo oculta.
- **Q2 (calidad):** defectos post-entrega clase (b) con `paridad_detector=true` (unica serie confirmatoria)
  + FUGA DE OBSERVACIONES = `observaciones_emitidas_n` vs `observaciones_registradas_con_dueno_n`. Plan B
  automatico si `defectos_post_n ~ 0` (efecto techo): reporta hallazgos pre-integracion por severidad como
  metrica DISTINTA, etiquetada como tal.
- **Q3 (descriptivo, NO confirmatorio):** dot plot par-a-par + mediana de diferencias PAREADAS por `par_id`.
  PROHIBIDO por diseno: medias, IC, regresiones, tests inferenciales (max 3 pares). El motor se NIEGA a
  emitir un p-value para Q3 (guard duro). Toda lectura = cota condicionada.
- **Q4 (causal, la unica):** ligero vs completo, ITT, aleatorizado (s.6.1). SOLO computable post-30-jul con
  n>=10; antes, el motor emite el ESQUELETO pre-registrado (contraste, brazos, n objetivo) y marca
  `Q4: PENDIENTE (ventana no abierta)`. Regla dura sellada: si Sprint 1 ejecuta <10, Q4 = SUBPOTENCIADO
  declarado (no se rellena). El hallazgo del sorteo 8/2 (Q4 subpotenciado) se reporta como poder efectivo.
- **Q5 (transferibilidad, descriptivo):** segunda instancia dominio real vs N=500 auto-dogfood; conteos
  descriptivos, sin afirmacion causal.

## 2. Fuera de alcance
- PROV-AGENT / export W3C PROV / firma por agente (queda en SPEC-0079 futuro).
- Activacion del loop / subagents / peones (F6, DECISION-0078). El motor MIDE `orchestration_mode` como
  dimension pero NO ejecuta peones.
- Tocar `enforce`/`authoritative` o el escritor unico. Los eventos son `applied:false` (no mutan estado,
  no pasan por submit_intent). El journal de medicion es un artefacto de estudio, NO el ledger #4.
- NO re-congelar el schema: F3.3 CONSUME schema_medicion.json v1.0 / schema_defectos.json v1.0 tal cual.

## 3. Contrato de aceptacion (para el checker formal)
1. **Determinista:** misma entrada (journal + defectos + `now` param) => misma salida (golden estable).
2. **cost.attributed:** captura EN CALIENTE de un err.log real -> `tokens_total_atribuibles` escrito ==
   el cumulativo leido (no un literal); idempotente (doble-cierre no doble-cuenta); degradacion por-cubeta
   a NA verificada (no inventa split).
3. **defect.reported:** valida contra schema_defectos v1.0; rechaza malformados a `rejected`; `paridad_detector`
   particiona confirmatorio vs descriptivo correctamente (caso de cada detector).
4. **manual.intervention:** produce fila OVERHEAD-FIJO con tag; NUNCA carga a una cubeta de tarea (test que
   asierta que ninguna tarea de producto recibe los tokens de un incidente).
5. **study_metrics.py:** Q1 con/sin overhead + regimen/arranque separados; Q2 solo paridad-true confirmatorio
   + Plan B efecto-techo; Q3 guard duro NO-inferencial (se niega a emitir p-value / IC / regresion); Q4
   esqueleto pre-ventana + subpotenciado declarado; Q5 descriptivo. GOLDEN con un journal sintetico que
   ejercita cada rama.
6. **Off-by-default / no-regresion:** hereda el off-by-default de SPEC-0079; con flag off el event log queda
   byte-equivalente; sin regresion en intent_flow / runtime_budget / hard-gate (drift 0).
7. **Gates:** validate_collaboration_state verde; scan_encoding (ASCII) verde; scan_domain_neutrality verde
   -- OJO: este motor vive en la instancia (personal/.../medicion/ o runtime/ del estudio), NO en el core
   neutral; NO introducir terminos de dominio Nova en archivos del core (frontera CLAUDE.md #1).

## 4. Traza a las preguntas del sello
| Pregunta (s.7) | Fuente en el schema | Rama del motor | Criterio de cierre |
|----------------|---------------------|----------------|--------------------|
| Q1 costo marginal | cubetas 3+4, overhead-fijo, tag_incidente | q1_costo() | con/sin overhead, regimen/arranque, degradacion reportada |
| Q2 calidad | defectos clase(b) paridad_detector, obs emitidas/registradas | q2_calidad() | solo paridad-true confirmatorio + Plan B techo |
| Q3 pares | par_id, deltas pareados | q3_pares() | dot plot + mediana pareada, NO inferencial (guard) |
| Q4 causal | brazo ligero/completo, ITT | q4_causal() | esqueleto pre-ventana; subpotenciado declarado |
| Q5 transferibilidad | instancia vs N=500 | q5_transfer() | descriptivo, sin causal |

## 5. Nota de carril (Asesor)
Esto es DISENO + STUDY-INTEGRITY. La VERIFICACION EMPIRICA (correr el motor contra err.log reales y la BD
desplegada) es del Analista-checker-formal, no mia (leccion sellada: checker formal > informal; mi revision
informal dejo pasar 2 bugs de falsabilidad que el gate formal cazo). El maker es Codex; el checker es el
Analista; NUNCA auto-verificacion.
