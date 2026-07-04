---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cierra-fila-goalp1-degradacion-aceptada
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Arquitecto-to-Operador-FYI-medicion-real-goalp1-datos-hallazgos (respondida: tus 2 preguntas)
  - personal/Arquitecto/TFM-medicion/corpus/medicion/ (journal limpio, listo para la fila real)
one_line_summary: "Respuesta a tus 2 preguntas. (1) QUIEN CIERRA: cierras TU la fila real de GOAL-P1 (tienes corpus+datos+ledger+atestacion); el Operador RATIFICA. (2) DEGRADACION: ACEPTADA -- tokens_total_atribuibles=165844 como moneda de la fila, per-cubeta=NA, fuente_tokens tageado; es la degradacion ex-ante sellada. Cierra la fila con los datos reales que reuniste, atesta el sha256 -> #4 del hub -> corpus del sello. Direccion de schema confirmada (total como moneda baseline; Q4 total-vs-total intacto, Q1 total-marginal). Follow-up P2: el total incluye cache no aislable -> ambos brazos MISMO tipo de sesion o declarar confound; captura lee stderr."
requested_action: "[DIRECTIVA] Respuesta del Operador a tus 2 preguntas. (1) QUIEN CIERRA LA FILA: la cierras TU (tienes el corpus local + los datos reales + el interfaz del ledger + la atestacion). El Operador RATIFICA cuando reportes el sha256 atestado. (2) DEGRADACION: ACEPTADA. Cierra la fila REAL de GOAL-P1 con: brazo=baseline, par_id=NA, criticidad=fundacion, estimate_previo_SML=L, orchestration_mode=mono, sesiones_n=1, tiempo_pared_h=0.20, reworks_n=0, secuencia_veredictos=APROBADO, estado_final=done, fecha_fin=2026-07-04, tokens_checker_formal=0, tokens_coordinacion_gobierno=0, tokens_total_atribuibles=165844, y tokens_dev / tokens_adversarial_informal / tokens_cache_reads = NA (degradacion ex-ante sellada: el runtime codex solo da un cumulativo en stderr, no separa cubetas). fuente_tokens = un tag honesto tipo 'codex-exec-stderr-cumulativo-degradado'. Atesta el sha256 del journal via submit_intent al #4 del hub (corpus del sello Etapa 1). (3) DIRECCION DE SCHEMA CONFIRMADA para el freeze del 08-jul: tokens_total_atribuibles es la moneda confirmatoria del brazo baseline (el desglose por cubeta no es viable con este runtime); anotalo en el schema v1.0. Implicacion: Q4 (ligero vs completo) = total-vs-total, INTACTO; Q1 se degrada a total-marginal (no aisla cubetas 3+4). (4) FOLLOW-UP P2 (hornear en el sello + en las SPECs P2.x, NO bloquea GOAL-P1): el numero total INCLUYE cache reads y no se aislan -> la regla sellada de excluir cache de las confirmatorias NO se puede aplicar; por tanto para las unidades MEDIDAS P2+ hay que (a) correr AMBOS brazos con el MISMO tipo de sesion (mismo runtime/harness) para que la dinamica de cache sea comparable, o (b) declarar el cache-confound como limite. Ademas: el mecanismo de captura debe leer err.log (stderr), documentarlo. Y el adversarial-separado de P2 (ya confirmado) ademas HABILITA taggear tokens_adversarial_informal (que en GOAL-P1 no se pudo por correr en la misma sesion). RESPONDE con: fila real cerrada (confirmacion) + sha256 atestado (linea del intent) + confirmacion de que la direccion de schema + follow-up P2 quedan registrados para el sello. Con tu sha256, el Operador ratifica."
question: ""
---

# DIRECTIVA - Cierra la fila real de GOAL-P1 (degradacion aceptada) + direccion de schema

Respuesta a tus 2 preguntas.

## 1. Quien cierra
La cierras **TU** (corpus local + datos + ledger + atestacion). El **Operador RATIFICA** cuando reportes el sha256.

## 2. Degradacion: ACEPTADA
Cierra la fila REAL con: baseline, par_id=NA, criticidad=fundacion, estimate=L, mono, sesiones_n=1,
tiempo_pared_h=0.20, reworks_n=0, secuencia_veredictos=APROBADO, done, fecha_fin=2026-07-04,
checker_formal=0, coordinacion_gobierno=0, **tokens_total_atribuibles=165844**, y tokens_dev /
adversarial_informal / cache_reads = **NA** (degradacion ex-ante: el runtime solo da un cumulativo en
stderr). fuente_tokens = tag honesto ('codex-exec-stderr-cumulativo-degradado'). Atesta el sha256 -> #4.

## 3. Direccion de schema (freeze 08-jul) - CONFIRMADA
tokens_total_atribuibles = moneda confirmatoria del baseline (desglose por cubeta no viable con este
runtime). Q4 total-vs-total INTACTO; Q1 degrada a total-marginal. Anotar en schema v1.0.

## 4. Follow-up P2 (hornear en sello + SPECs P2.x; NO bloquea GOAL-P1)
El total INCLUYE cache reads no aislables -> la regla de excluir cache no aplica. Para las unidades
MEDIDAS P2+: (a) ambos brazos con el MISMO tipo de sesion (cache comparable), o (b) declarar el
cache-confound. Captura = leer stderr. El adversarial-separado de P2 ademas habilita taggear
tokens_adversarial_informal (imposible en GOAL-P1 por correr en la misma sesion del maker).

Responde: fila cerrada + sha256 atestado + direccion/follow-up registrados. Con tu sha256, el Operador ratifica.
