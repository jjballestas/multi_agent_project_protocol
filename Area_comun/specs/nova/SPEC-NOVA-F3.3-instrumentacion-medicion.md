# SPEC-NOVA-F3.3 - Instrumentacion del estudio (motor de medicion automatizado) [INFRA, NO es unidad de contraste A/B]

> Formato UNIFICADO NOVA-SPEC-T-001 v1.1 + intake-v2/DoR (DECISION-0084). Formalizada por el Arquitecto
> a partir de `personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md` (Asesor, disenador; DIRECTIVA operador
> cola-F3.3-lista-no-idle, item Q1 CRITICAL-PATH). Esta unidad es INFRAESTRUCTURA del propio estudio
> (instrumentacion de medicion), NO una unidad de contraste baseline-vs-gobernado; no entra al pool Q4, no
> tiene par_id, no consume el sandbox de mutadores. Prior art reusado: SPEC-0079/DECISION-0033
> (`cost.attributed`, ACEPTADA, TASK-0111, off-by-default).

## Preambulo de gobierno (DoR)
- spec_id: SPEC-NOVA-F3.3 - task_id (hub): TASK-0249
- owner_maker: Codex (implementa en la capa de instrumentacion del estudio, Python, fuera del core neutral)
- checker: Analista, **gate FORMAL** (es infraestructura gobernada del hub, no unidad de contraste baseline;
  NO aplica el convenio checker_formal=0/adversarial-informal-en-sesion-separada de las unidades P2-P6).
- arm: N/A (no es baseline ni gobernado; es la instrumentacion que MIDE ambos brazos).
- q4_membership: **FUERA** (infra del estudio, no unidad de contraste; declaracion explicita por
  precedente F-0246-01).
- isolation: N/A (no hay hermano de par que contaminar; consume el schema v1.0 ya sellado, tal cual,
  sin re-interpretarlo).
- measurement: N/A para esta unidad misma (es la HERRAMIENTA de medicion, no una tarea medida); SI debe
  producir, para las unidades que instrumente, `tokens_total_atribuibles` con la degradacion por-cubeta
  a NA ya sellada en DECISION-0091 (schema v1.0, hallazgos del piloto GOAL-P1).
- **deuda GOAL-P1:** ninguna (esta unidad no toca el front de Nova-Budget).
- **F-NOVA-01:** N/A (no invoca ningun proc/objeto de `DbsFinanciero`; consume solo `err.log`/STDERR del
  runtime de agentes, `schema_medicion.json`/`schema_defectos.json` v1.0, y el journal materializado).
- db_verified_at: N/A (sin objetos de BD de dominio).
- attestation: sha256 de esta SPEC via intent del hub en el gate del estudio.
- stack (obligatorio, DISTINTO de las unidades de dominio): Python puro (misma familia que
  `medicion_ledger.py` ya existente), sin dependencias del stack .NET/React de Nova-Budget; vive en la
  capa de instrumentacion de la INSTANCIA del estudio (`personal/Arquitecto/TFM-medicion/` o equivalente
  de runtime del estudio), **NUNCA en el core neutral** (frontera CLAUDE.md #1: cero terminos de dominio
  Nova en archivos genericos del protocolo). Los 3 eventos (`cost.attributed`, `defect.reported`,
  `manual.intervention`) son artefactos de estudio `applied:false` (NO mutan el ledger #4, NO pasan por
  `submit_intent`, NO tocan `enforce`/`authoritative`/el escritor unico).

## 1. Objetivo definido
Automatizar la captura de medicion del estudio NOVA Etapa 1 (hoy 100% manual via `medicion_ledger.py`),
para que el brazo baseline (y luego el gobernado) corran con instrumentacion automatica en vez de
transcripcion manual, eliminando la fuente #1 de error de medicion antes de que abra el dev medido P2.
- Fuente: `personal/asesor/DRAFT-SPEC-F3.3-instrumentacion.md` s.0-s.1 + SELLO-ETAPA-1 s.7 (plan Q1-Q5)
  + s.8/s.10 (schema + reglas duras) + SPEC-0079/DECISION-0033 (cost-attribution, prior art aceptado).
- Calidad: falsable. Bien: "cerrar una sesion de tarea real escribe `tokens_total_atribuibles` igual al
  cumulativo leido del `err.log`, y una segunda escritura de la misma tarea NO duplica la fila."

## 2. Usuario objetivo definido
El propio ARQUITECTO/OPERADOR como operador de la medicion del estudio (no un usuario final de Nova-Budget):
cierra tareas del dev medido y necesita que la fila de medicion se llene sola, con defectos y overhead-fijo
clasificados automaticamente, y con Q1-Q5 computables bajo demanda sin recalculo manual.

## 3. Alcance definido
3 eventos + 1 motor, TODOS `applied:false` (no mutan el ledger #4):
- **`cost.attributed` automatico por `tarea_id`:** extiende SPEC-0079/DECISION-0033 (no reinventa el
  evento); lee el cumulativo de tokens del `err.log` (STDERR) del runtime `codex-exec` al cierre de
  sesion; escribe `tokens_total_atribuibles`; degradacion EX-ANTE sellada (4 cubetas por-rol -> NA salvo
  que el rol corra en sesion separada, ya sellado en schema v1.0); idempotente (idempotency_key
  determinista por `tarea_id`+`sesion_ids`, reusa el de SPEC-0079); confound de cache declarado
  (`notas_confound=cache-confound` si aplica), nunca corregido por el motor.
- **`defect.reported`:** un evento por defecto post-entrega, validado contra `schema_defectos.json` v1.0
  (9 columnas: taxonomia D1-D4, severidad, `detector` enum, `paridad_detector` bool, `clase` a/b);
  malformados se RECHAZAN a `rejected` (nunca se escribe una fila invalida); `paridad_detector=true`
  particiona la serie confirmatoria de Q2 (mismo detector disponible en ambos brazos) de la descriptiva.
- **`manual.intervention`:** fila OVERHEAD-FIJO con `tag_incidente_maquinaria` (regimen/arranque/
  incidente/NA) y `rol_en_par=overhead_fijo`; regla dura (s.10 del sello): estos tokens NUNCA cargan a la
  cubeta de una tarea de producto.
- **`study_metrics.py`:** motor DETERMINISTA (sin `Date.now()`/aleatoriedad; `now`/ventana parametrizados)
  con golden, que computa Q1 (costo con/sin overhead, regimen/arranque separados, degradado si cubetas
  3/4 no separables), Q2 (defectos clase-b con `paridad_detector=true` unicamente + Plan B efecto-techo),
  Q3 (dot plot + mediana pareada, GUARD DURO que se niega a emitir p-value/IC/regresion), Q4 (esqueleto
  pre-ventana + `PENDIENTE`/`SUBPOTENCIADO` declarado segun n), Q5 (descriptivo, sin causal).

## 4. Fuera de alcance definido
- PROV-AGENT / export W3C PROV / firma por agente (SPEC-0079 futuro, no esta unidad).
- Activacion del loop / subagents / peones (F6, DECISION-0078); el motor MIDE `orchestration_mode` como
  dimension pero NO ejecuta peones.
- Tocar `enforce`/`authoritative` o el escritor unico del ledger #4. Los eventos son `applied:false`.
- Re-congelar el schema: F3.3 CONSUME `schema_medicion.json`/`schema_defectos.json` v1.0 tal cual (ya
  sellados en DECISION-0091); no los edita.
- Cualquier codigo de dominio Nova (Budget/CDP/RP/etc.) -- esta unidad no toca `DbsFinanciero` ni el repo
  Nova-Budget.

## 5. Contenido / assets definidos
- **Motor Python** (misma familia que `medicion_ledger.py`): 3 handlers de evento (`cost_attributed`,
  `defect_reported`, `manual_intervention`) + `study_metrics.py` (funciones `q1_costo()`, `q2_calidad()`,
  `q3_pares()`, `q4_causal()`, `q5_transfer()`).
- **Entrada:** journal materializado v1.0 (filas de `medicion_ledger.py` o de los nuevos eventos
  automaticos), `schema_defectos.json` v1.0, `err.log`/STDERR de las sesiones de agente.
- **Salida:** filas de journal actualizadas (`tokens_total_atribuibles`, overhead-fijo con tag), filas de
  defectos validadas, y el reporte Q1-Q5 (determinista, con golden fixture).
- **Referencias:** `DRAFT-SPEC-F3.3-instrumentacion.md` (Asesor, diseno completo), SPEC-0079/DECISION-0033
  (`cost.attributed` prior art), SELLO-ETAPA-1 s.7/s.8/s.10, DECISION-0091 (schema v1.0 sellado).

## 6. Restricciones tecnicas definidas
- (a) Reusa la primitiva `cost.attributed` de SPEC-0079/DECISION-0033; NO inventa un evento nuevo para el
  mismo proposito.
- (b) `applied:false` en los 3 eventos: NUNCA pasan por `submit_intent`, NUNCA tocan el escritor unico ni
  `enforce`/`authoritative`.
- (c) Determinismo: `study_metrics.py` NO usa `Date.now()`/`Math.random()`/fecha-de-hoy interna; `now` y la
  ventana de analisis son argumentos explicitos -> reproducible con golden.
- (d) Degradacion por-cubeta a NA es una DECISION SELLADA (DECISION-0091), no una limitacion a "arreglar":
  el motor JAMAS inventa un split de tokens que el runtime no provee.
- (e) Neutralidad: el motor vive en la capa de INSTANCIA del estudio (fuera de `Area_comun/protocol/` y de
  cualquier archivo `*.template.*` del core); `scan_domain_neutrality.py` debe quedar verde igual (esta
  SPEC misma vive en `specs/nova/`, namespaced, ya excluida del scan del core).

## 7. Criterios de aceptacion definidos (Given/When/Then; contrato de aceptacion s.3 del draft)
1. **Dado** el mismo journal+defectos+`now`, **cuando** corre `study_metrics.py` dos veces, **entonces**
   la salida es BYTE-IGUAL (determinismo, golden estable).
2. **Dado** un `err.log` real de una sesion de tarea, **cuando** cierra `cost.attributed`, **entonces**
   `tokens_total_atribuibles` == el cumulativo leido (no un literal hardcodeado); un segundo cierre de la
   MISMA tarea NO duplica la fila (idempotente); las 4 cubetas por-rol quedan NA salvo sesion separada
   verificada.
3. **Dado** un `defect.reported` malformado (enum fuera de rango o campo de apertura faltante),
   **entonces** se RECHAZA a `rejected` y NUNCA se escribe una fila de defecto invalida; dado uno valido
   con `paridad_detector=true`, entra a la serie confirmatoria de Q2; con `paridad_detector=false` entra
   solo al descriptivo.
4. **Dado** un `manual.intervention`, **entonces** produce una fila OVERHEAD-FIJO con `tag_incidente_
   maquinaria`; test explicito que ASIERTA que NINGUNA tarea de producto recibe tokens de un incidente.
5. **Dado** el plan Q1-Q5 del sello, **cuando** corre `study_metrics.py` sobre un journal sintetico
   (golden) que ejercita cada rama, **entonces**: Q1 reporta con/sin overhead y regimen/arranque
   separados (degradado si aplica); Q2 usa SOLO `paridad_detector=true` + Plan B automatico si
   `defectos_post_n~0`; Q3 se NIEGA a emitir p-value/IC/regresion (guard duro, test que verifica el
   rechazo); Q4 emite esqueleto pre-ventana + `SUBPOTENCIADO` declarado (coherente con el hallazgo del
   sorteo 8/2 de DECISION-0091); Q5 es descriptivo sin afirmacion causal.
6. **Dado** el flag off-by-default de los eventos, **entonces** el event log queda BYTE-EQUIVALENTE (sin
   regresion en `intent_flow`/`runtime_budget`/hard-gate; drift 0).

## 8. Pruebas / gates definidos
- **Unit:** cada handler de evento (`cost_attributed`, `defect_reported`, `manual_intervention`) +
  `study_metrics.py` con golden fixture que ejercita las 5 preguntas y sus ramas degradadas/guard.
- **Idempotencia:** test que cierra la misma tarea dos veces y verifica NO-doble-conteo.
- **Rechazo de malformados:** test que valida el enum/campo-de-apertura faltante y verifica `rejected`.
- **No-regresion del hub:** `validate_collaboration_state.py` + `scan_encoding.py` + `scan_domain_
  neutrality.py` verdes en clon limpio; drift 0; `protocol.config.json` byte-identico; el flag off-by-
  default deja el event log byte-equivalente (sin nuevas entradas si esta apagado).
- **Gate final:** gate FORMAL del Analista (checker-only, NO informal; es infraestructura gobernada, no
  unidad de contraste baseline) + DoD de NOVA-GOAL-001 con evidencia real (golden, idempotencia probada,
  rechazo probado) + verde de gates del hub + atestacion sha256.

## 9. Riesgos definidos
| Riesgo | Impacto | Mitigacion |
|---|---|---|
| Confundir esta unidad con una de contraste A/B (baseline/gobernado) | Contamina el pool Q4 o el par | Declarado explicito: arm=N/A, q4_membership=FUERA, sin par_id (preambulo DoR) |
| Introducir dominio Nova en archivos del core neutral | Rompe DECISION-0002 (neutralidad del core) | Vive en `specs/nova/` (namespaced) + capa de instrumentacion de instancia; scan_domain_neutrality gatea |
| El motor "arregla" la degradacion por-cubeta inventando un split | Rompe la degradacion EX-ANTE sellada en DECISION-0091 | Restriccion 6d + criterio 2 (NA verificado, no split inventado) |
| Eventos tocan el escritor unico / `submit_intent` | Rompe el gate B.3 / integridad del ledger #4 | `applied:false` obligatorio (restriccion 6b), test de no-regresion drift 0 |
| Verificacion informal (self-review del Asesor) deja pasar bugs de falsabilidad | Precedente ya sellado (2 bugs cazados por el gate formal en otra unidad) | Checker FORMAL del Analista obligatorio (no informal); maker Codex != checker Analista, nunca auto-verificacion |

## 10. Prioridad definida
**CRITICAL-PATH** (DIRECTIVA operador cola-F3.3-lista-no-idle, item Q1): debe estar VIVA antes de que abra
el dev medido P2.1/P2.2 (ventana baseline 3-25-jul), para que P2 sea el primer brazo con captura
automatica. Si no llega a tiempo, el fallback ya probado (`medicion_ledger.py` manual) NO bloquea la
apertura de P2, pero el objetivo es que P2 abra ya instrumentado. Dependencias: schema v1.0 sellado
(DECISION-0091, YA listo) + SPEC-0079/DECISION-0033 (`cost.attributed`, YA aceptada). Desbloquea: captura
automatica del dev medido completo (P2 en adelante) + Q1-Q5 computables bajo demanda para el sello Etapa 2.
