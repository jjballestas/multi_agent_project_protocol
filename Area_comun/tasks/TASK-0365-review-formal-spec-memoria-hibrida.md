---
id: TASK-0365
title: Review formal de SPEC-MEMORIA-HIBRIDA v0.3.0 -- falsar los nueve invariantes contra el motor ya portado
status: ready
owner: Analista
type: review
file: Area_comun/tasks/TASK-0365-review-formal-spec-memoria-hibrida.md
created: 2026-08-12
reviewer: Arquitecto
intake:
  type: doc
  goal: >
    SPEC-MEMORIA-HIBRIDA lleva desde el 2026-07-14 en `status: draft-reviewed-informal`. Su unica
    revision adversarial fue INFORMAL (subagente anti-rubber-stamp: 2 BLOCKER + 7 MAJOR + 5 MINOR,
    todos reales y todos incorporados, registro en la s.15); la review formal del checker quedo
    aplazada porque su harness estaba caido. Ya no lo esta, y ha cambiado lo esencial: el motor dejo
    de ser un plan. TASK-0314 (F1-PORT) cerro y el hub tiene su `scripts/memory/` con los seis
    ficheros, asi que cada uno de los nueve invariantes tiene codigo detras que lo cumple o no lo
    cumple. Esta tarea es esa review formal, y su criterio es que los invariantes se FALSEN contra el
    motor, no que se juzgue el texto. Salida: si la SPEC puede dejar `draft-reviewed-informal` y, si
    no, que invariante lo impide y con que medicion.
  acceptance:
    - "AC1 (los nueve, uno a uno, contra el motor): veredicto invariante por invariante de I1 a I9
      falsado contra el codigo real de `scripts/memory/`, con mutante de produccion donde el
      invariante lo admita. Un invariante declarado cumplido sin haber intentado romperlo no
      acredita; el reporte dice para cada uno que se intento y que resistio."
    - "AC2 (I5 se falsa BORRANDO la DB, no leyendo el codigo): la garantia de fallo seguro sin DB se
      mide corriendo los flujos vivos (validate, submit_intent, crons) con la base ausente. Si algun
      flujo vivo depende de ella, la cache dejo de ser cache y el hallazgo es BLOCKER."
    - "AC3 (I8 con I1: round-trip por BLOB de git): el round-trip canon -> DB -> canon se acredita
      byte a byte y con hashes por BLOB de git, nunca por copia de trabajo. Es el gap que mato a
      Engram; medirlo en clon limpio, porque los `.pyc` del arbol caliente ya descuadraron un conteo
      en esta instancia."
    - "AC4 (I3: por criterio o por lista): se determina si la neutralizacion del lexico de dominio
      del detector de PII quedo por CRITERIO de pertenencia o por LISTA de terminos. La s.16
      documenta que el detector llevaba lexico de nomina y que un termino generico daba falso
      positivo sobre cualquier titulo en espanol. Si la neutralizacion es una lista, se declara como
      tal: es la clase de defecto que esta instancia lleva semanas desterrando."
    - "AC5 (la regla del port se verifica, no se acepta): la s.16 declara que ningun hallazgo se
      resuelve relajando una garantia, sino ampliando el conjunto de valores ACEPTADOS conservando la
      validacion por VALOR. Se verifica hallazgo por hallazgo de los doce, en vez de aceptarla como
      declaracion."
    - "AC6 (residuales honestos y direccion de la correccion): se declara lo que NO se pudo medir y
      por que. Si un invariante esta bien escrito pero el motor no lo cumple, se dice explicitamente
      que la correccion va al MOTOR y no al texto, para que no se cierre por el lado facil."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/memory/test_memory_db.py"
  scope_routes:
    - Area_comun/mailbox/open/
  out_of_scope:
    - "Corregir codigo: el checker es checker-only (DECISION-0099); los hallazgos vuelven al maker
      como remediacion."
    - "TASK-0350 (marcadores sin resolver en la instancia generada): ya esta censada y ruteada a
      Codex; no se gasta vuelta en ella. Solo interesa si al medir resulta MAS ancha que su titulo."
    - "El producto: alcance SOLO hub, sin producto en alcance -- no se gatea npm test."
    - "protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y el dataset N=500: fondo
      intocable."
    - "Activar el archivado o mover historia canonica: exige la DECISION de activacion que el REQ
      s.0.4 requiere, y no es esta tarea."
  risk: low
  estimate: M
---

# TASK-0365 -- review formal de SPEC-MEMORIA-HIBRIDA v0.3.0

Gate formal de la SPEC. El encargo completo, con el detalle de los nueve invariantes y de los tres
que se senalan por su peso (I5, I8 con I1, e I3), va en el mensaje de review; esta tarea existe para
darle al encargo una identidad numerada, que es lo que el arnes necesita para reservar su ejecucion.

## Por que la tarea existe ademas del mensaje

El primer intento de rutear esta review se encolo el 2026-08-12 con `task_id: none`. El arnes de los
peones deriva el alcance de trabajo de un mensaje a partir de su `task_id`: exige la forma
`TASK-NNNN`, busca su fila en el indice y lee los `scope_routes` de su fichero. Un mensaje sin tarea
numerada no produce descriptor, no puede reservar ejecucion, y se difiere en bucle hasta morir por
tiempo -- sin que nadie lo lea. Se observo en vivo: `RETRY_DEFER reason=message_scope_ambiguous`.

Por eso la review va numerada. El defecto del arnes -- que esa muerte sea SILENCIOSA -- se censa
aparte en TASK-0366.

## Los nueve invariantes

    I1  la DB es CACHE, el canon gana siempre; reconstruible byte a byte
    I2  cero writers paralelos al estado gobernado (el indexador es read-only)
    I3  PII default-CERRADO (`plain_text_excerpt` y FTS solo con permiso explicito)
    I4  la historia no se mueve sin decision
    I5  fallo seguro SIN DB: ningun flujo vivo (validate, submit_intent, crons) depende de ella
    I6  identidad de memoria derivada del chokepoint
    I7  decision activa jamas invisible
    I8  hashes por BLOB de git, nunca por working copy
    I9  F1 NO infiere: toda arista se extrae, no se deduce
