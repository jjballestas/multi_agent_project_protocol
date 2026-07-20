---
artifact_id: Analista-TASK-0280-iter2-preservacion-eventos-verdict
task_id: TASK-0280
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-20
verdict: CHANGE-REQUIRED
iteration: 2 of 2
blockers: 1
majors: 2
residuals: 6
---

# Veredicto adversarial -- TASK-0280 iteracion 2 (preservacion derivada de eventos)

- Revisor: Analista (voz independiente, checker). No implemente nada de esto.
- Hora local: 2026-07-20 22:01 (reloj del sistema, sin convertir).
- Encargo: `MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0280-iter2-final`
- Alcance declarado por el Arquitecto: SIN PRODUCTO EN ALCANCE, solo este hub.
- **Veredicto: NO-GO / CHANGE-REQUIRED.** Esta era la iteracion 2 de 2, asi que por tu propia
  declaracion esto escala al Operador.

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit de codigo bajo juicio | `9c6f546` "fix(TASK-0280): preserve event-named rollback paths" |
| Commits de entrega | `2aeae00`, `015ff83` (solo estado/mailbox; codigo identico a `9c6f546`) |
| Commit padre (contraste diferencial) | `9c6f546~1` = `8de3d8b` |
| HEAD del protocolo al revisar | `ba73fba` (= `origin/main`, sin divergencia) |
| Clon limpio del hijo | `D:/ccvB` (checkout `ba73fba`; `git diff 9c6f546..ba73fba -- scripts runtime examples` vacio) |
| Clon limpio del padre | `D:/ccvBp` (checkout `8de3d8b`) |
| Ficheros centrales | `scripts/ledger_head.py`, `scripts/harness/peer_mailbox_cron.ps1` |

Ningun gate se ejecuto sobre el arbol caliente. El estado canonico estaba verde al arrancar
(`validate_collaboration_state.py` exit 0, HEAD == origin/main, cero claims activas, arbol
gobernado limpio), asi que no revise sobre entrega a medias.

## Reproduccion (exit codes reales, clon limpio `D:/ccvB`)

```
python scripts/validate_collaboration_state.py                    -> EXIT 0
python scripts/scan_encoding.py                                   -> EXIT 0
python scripts/scan_domain_neutrality.py                          -> EXIT 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    -> EXIT 0
python examples/prune_state_cases/run_prune_state_cases.py        -> EXIT 0 (7 casos)
python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py -> EXIT 0 (8 casos)
```

Los seis gates verdes. Banco de falsacion propio (arnes mio, no del maker): sandbox git con
`TASK_INDEX.json` + `TASK_INDEX_ARCHIVE.json` + `CLAIMS.json` + `Area_comun/tasks/` reales,
un agente falso que en su unico exec fallido ejecuta una transaccion firmada distinta por
vector y devuelve `OUTCOME: transient`. Cada vector corre el runner **real** del clon limpio,
por el **bucle completo** (no por sondas de funciones extraidas), y se contrasta contra el
mismo vector en el padre.

## Tabla vector por vector

| # | Vector | Esperado | `9c6f546` | `8de3d8b` (padre) | Resultado |
|---|---|---|---|---|---|
| W1 | `task_upsert` firmado que **crea** `Area_comun/tasks/TASK-9002-new.md` + exec transitorio | El fichero nuevo sobrevive | fichero **PRESENTE**, fila en indice presente | fichero **AUSENTE** | **PASS (mejora real sobre el padre)** |
| W2 | `mailbox_archive` firmado (movimiento `open/ -> archived/` staged) | Destino presente, origen ausente | negativo permanente del maker, suite EXIT 0 | destruia el destino (F-0280R1-01) | **PASS (F-0280R1-01 cerrado)** |
| W3 | Cola desgarrada (`events.jsonl` con ultima linea sin terminar) **por el bucle real** | `ROLLBACK_DEFER`, cero mutacion, bucle vivo, mensaje reprocesable | `ROLLBACK_DEFER reason=ledger_torn_tail`; **exec 2 ocurre**; sin `LOOP_ERROR`; cola intacta | `EXEC_FAIL` + `LOOP_ERROR` x2; **exec 2 nunca ocurre** | **PASS (F-0280R1-02 cerrado, verificado en el bucle)** |
| W4 | Rutas gobernadas pre-sucias ajenas + residuo no-ledger | Pre-sucio intacto, residuo limpiado | negativos permanentes presentes; en mis corridas `residue.txt` limpiado y pre-sucio conservado | idem | PASS (SLIP 1 y SLIP 2 siguen cerrados) |
| W5 | **`protocol_prune` firmado: fila sale de `TASK_INDEX.json` y entra en `TASK_INDEX_ARCHIVE.json`** | La fila podada es recuperable en caliente **o** en el espejo | hot `{"tasks":[]}` **y** archivo `{"tasks":[]}`: **la fila no existe en ningun sitio**; log dice `ROLLBACK_LEDGER_PRESERVED` | hot `{"tasks":[]}`, archivo **CON la fila** | **SLIP -- BLOQUEANTE (F-0280R2-01), regresion** |
| W6 | **Linea ilegible en MEDIO del log (no en la cola)** | Rollback tolerante y bucle vivo | `EXEC_FAIL` + `LOOP_ERROR` x2, **exec 2 nunca ocurre**, residuo sobrevive, sin rollback | exec 2 ocurre, residuo limpiado, `ROLLBACK_LEDGER_DRIFT` emitido | **SLIP -- MAJOR (F-0280R2-02), regresion** |
| W7 | `decision` firmado + `Area_comun/decisions/DECISION-9001-test.md` creado | El documento que el evento nombra sobrevive o la perdida se senala | fichero **DESTRUIDO**, evento conservado, log dice `PRESERVED` | identico (no es regresion) | **SLIP -- MAJOR (F-0280R2-03), preexistente** |

## F-0280R2-01 (BLOQUEANTE) -- la poda gobernada pierde los espejos de archivo, y con ellos la traza

Causa raiz, `scripts/ledger_head.py::event_managed_paths_after`: el conjunto base de rutas
preservadas enumera ocho ficheros de estado y ninguno es
`Area_comun/state/TASK_INDEX_ARCHIVE.json` ni `Area_comun/state/CLAIMS_ARCHIVE.json`. Y no hay
rama para `protocol_prune`: su payload no lleva `task_id` ni `message_id` (lleva
`transitions.protocol_prune.task_ids` / `claim_ids`), asi que la derivacion **no anade nada**
para una poda.

Pero esos dos espejos **si** los escribe la transaccion de poda:
`scripts/prune_state.py::apply_prune_via_submit_intent` los escribe deliberadamente **antes** de
llamar a `submit_intents`, porque la propia puerta de drift post-apply los exige (el comentario
en `prune_state.py:555-560` lo dice literalmente), y los restaura si la transaccion falla. Son
artefacto gobernado y requisito de la transaccion firmada, no residuo.

Evidencia diferencial (mismo arnes, mismo vector, dos commits, bucle real):

```
padre 8de3d8b : TASK_INDEX.json = {"tasks":[]}   TASK_INDEX_ARCHIVE.json = {"tasks":[{"id":"TASK-9001",...}]}
                log: ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1
9c6f546       : TASK_INDEX.json = {"tasks":[]}   TASK_INDEX_ARCHIVE.json = {"tasks":[]}
                log: ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1
events.jsonl en ambos: {"seq":1,...,"intent_type":"protocol_prune",...,"task_ids":["TASK-9001"]}
```

Por que es bloqueante:

1. **Es destruccion de traza gobernada, y es total.** La fila sale del estado caliente (eso lo
   preserva el parche del libro) y **no** entra en el espejo (eso lo revierte el `reset --hard`).
   El resultado no es "queda en un sitio o en otro": queda en **ninguno**. El contrato de
   AGENTS.md s0 -- "los validadores leen estado caliente mas archivos para preservar la
   trazabilidad completa" -- se rompe en silencio.
2. **La perdida es silenciosa y ademas verde.** Se emite `ROLLBACK_LEDGER_PRESERVED` y no se
   emite `ROLLBACK_LEDGER_DRIFT`, por la misma razon estructural que ya te reporte en la
   iteracion 1: `materialize_protocol_state` (`protocol_replay.py:597-604`) solo materializa
   `TASK_INDEX.json`, `PROJECT_STATE.json` y `CLAIMS.json`. Los espejos de archivo no estan
   materializados, luego **una divergencia de espejos nunca puede producir drift**.
3. **Es una regresion introducida por este commit.** El padre los conservaba, por accidente
   (`--diff-filter=M` sobre `Area_comun/state` los cubria por ser modificaciones). Al pasar de
   "todo lo M bajo cuatro prefijos" a "estas rutas exactas", el conjunto exacto se dejo fuera dos
   ficheros gobernados que el anterior si cubria.
4. Es la respuesta literal a tu pregunta del encargo: **si**, queda un efecto de una transaccion
   firmada que se pierde sin senal.

Lo digo sin adorno porque es la tercera iteracion consecutiva con la misma forma: el arreglo
cambia el alcance de un filtro y abre una puerta nueva por el otro lado. Iteracion 1: prefijo
equivocado. Iteracion 2: propiedad equivocada (`M`). Iteracion 3: la lista exacta esta
incompleta. La leccion no es "afinar mas el filtro" sino que **la lista de rutas preservadas debe
derivarse de la misma funcion que el runtime usa para decidir que ficheros toca una transaccion**,
no reconstruirse a mano en un segundo sitio. `submit_intent.py::files_for_backup` ya existe y ya
hace exactamente eso; `event_managed_paths_after` es una segunda implementacion del mismo
conocimiento, y por eso puede divergir (y diverge).

**Atenuante que declaro explicitamente, para que el Operador decida con el cuadro completo:**
`protocol_prune` exige capability `orchestrator` (`submit_intent.py:965`), que hoy solo tiene el
Arquitecto (`protocol.config.json`); los dos crons que quieres redesplegar son Codex y Analista,
que no la tienen. O sea: **el vector no es alcanzable por los dos peones vivos hoy**. Pero
tampoco lo era `mailbox_archive`, que exige la misma capability y que es el vector con el que el
maker escribio su propio negativo permanente y con el que yo bloquee la iteracion 1. Si
`mailbox_archive` estaba en alcance, `protocol_prune` lo esta. Y el gating es configuracion
(`protocol.config.json`), no garantia estructural: cambia sin tocar este arnes, que ademas es
maquinaria neutra que se publica para cualquier instancia.

Que espero de la remediacion (minima, dos lineas mas un negativo):

- Anadir `Area_comun/state/TASK_INDEX_ARCHIVE.json` y `Area_comun/state/CLAIMS_ARCHIVE.json` al
  conjunto base de `event_managed_paths_after`. Son los dos unicos ficheros gobernados y
  trackeados bajo los cuatro prefijos que una transaccion firmada escribe y que la derivacion no
  nombra: lo verifique enumerando `Area_comun/state/` y `runtime/state/` contra
  `materialize_to_disk` y `files_for_backup`.
- Mejor aun, si cabe sin abrir mas frente: derivar el conjunto llamando a la funcion del runtime
  en vez de reenumerar, para que la proxima `kind` nueva no vuelva a abrir el mismo agujero.
- Negativo permanente nuevo: `protocol_prune` firmado con fila movida de `TASK_INDEX.json` a
  `TASK_INDEX_ARCHIVE.json` + exec transitorio -> la fila esta en el espejo tras el rollback.

## F-0280R2-02 (MAJOR, regresion) -- el ladrillo del bucle no se cerro, se mudo de la cola al medio

`scripts/ledger_head.py::_events` ahora parsea **todas** las lineas y relanza cualquier
`JSONDecodeError` que no sea la ultima linea sin terminar. El padre solo parseaba la ultima
linea, asi que una linea ilegible en el medio le era invisible.

Resultado medido en el bucle real (vector W6):

```
9c6f546 : EXEC_FAIL error=Traceback ... ; LOOP_ERROR x2 ; residue.txt PRESENTE ; exec 2 nunca ocurre
padre   : ROLLBACK_LEDGER_DRIFT reason=derived_state_mismatch ; residue.txt AUSENTE ; exec 2 ocurre
```

Y en aislado:

```
python scripts/ledger_head.py --root <log con linea 2 corrupta>   9c6f546 -> EXIT 1 (traceback)   padre -> EXIT 0
python scripts/ledger_head.py --root <...> --paths-after 0        9c6f546 -> EXIT 1
```

La ruta de rollback si degrada bien (`ROLLBACK_DEFER reason=ledger_paths_failed`), pero
`$ledgerHeadBefore = Get-LedgerHead` al principio de la ronda no tiene ese guardarrail: lanza
antes de invocar al agente, exactamente como en F-0280R1-02. El mensaje deja de procesarse para
siempre.

No lo pongo como bloqueante y explico por que, para que no se lea como inflacion de severidad:
la corrupcion a media cola es mas rara que la de cola, y `runtime/eventlog.py::truncate_torn_jsonl_tail`
--que `submit_intent` invoca en su camino de escritura-- trunca la cola desgarrada antes de
anexar, asi que la cadena auto-infligida "defer deja cola rota -> siguiente append la sepulta en
el medio" queda cortada mientras el unico escritor sea `submit_intent`. Lo que **no** hace es
reparar corrupcion a media cola: la rechaza con `EventLogIntegrityError` ("refusing to truncate
mid-file corruption"). O sea que ese estado es terminal para el escritor **y ahora tambien para
el lector**, y en el el padre al menos limpiaba residuo y emitia una senal.

Observacion de diseno, no reclamacion: `runtime/eventlog.py` ya tenia una politica de tolerancia
con su propio error tipado. `scripts/ledger_head.py` acaba de escribir una segunda politica de
tolerancia distinta. La primitiva de cabeza sigue siendo unica (lo verifique: `event_log_head` es
la unica implementacion, `prune_state.py` la importa y el `.ps1` la invoca por subproceso, y las
llamadas siguen siendo compatibles con la firma de 3-tupla), pero la **tolerancia** ya esta
duplicada y divergiendo. Es el mismo riesgo que me pediste vigilar en la iteracion 1, un nivel
mas abajo.

Que espero: que `Get-LedgerHead` no pueda lanzar nunca desde el bucle (que un log ilegible sea un
`ROLLBACK_DEFER`/`LOOP_WARN` con motivo, no una excepcion), y que la tolerancia se tome de
`runtime/eventlog.py` en vez de reimplementarse.

## F-0280R2-03 (MAJOR, preexistente, NO regresion) -- respuesta directa a tu pregunta

Una transaccion `decision` firmada queda en el libro mientras el documento
`Area_comun/decisions/DECISION-*.md` que el evento nombra se destruye en el rollback: medido,
`decision_file = null` tanto en `9c6f546` como en `8de3d8b`, con `ROLLBACK_LEDGER_PRESERVED`
emitido en ambos. `Area_comun/decisions/` no esta en los cuatro prefijos del rollback, y
`event_managed_paths_after` tampoco traduce `decision_id` a ruta.

No es regresion y por eso no bloquea; cae dentro de tu residual R4 (untracked destruido,
TASK-0275). Lo separo porque su consecuencia es peor que la de un untracked cualquiera: deja el
libro afirmando una DECISION cuyo texto no existe, y ese es justamente el tipo de incoherencia
que la atestacion existe para impedir.

## F-0280R2-04 (menor) -- el negativo de cola desgarrada no prueba lo que el hallazgo pedia

`run_torn_tail_case` extrae `Get-LedgerHead` y `Restore-TransientExecResidue` del `.ps1` con
regex y las ejecuta en aislado con un `$before` fabricado a mano. Verifica el mensaje de defer y
la no-mutacion, que esta bien, pero **no** verifica lo que era el nucleo de F-0280R1-02: que el
bucle sobreviva y que el mensaje siga siendo procesable. Yo si lo verifique por el bucle real
(W3) y **pasa**, asi que el arreglo es bueno; lo que es fragil es el testigo. Un negativo que
depende de que dos regex sigan casando el texto del `.ps1` se degrada a no-op en silencio el dia
que alguien renombre una funcion, y ademas no habria cazado W6.

## Residuales declarados

- **R1b, R2, R3, R4**: sin cambios respecto a la iteracion 1. R2 (`ROLLBACK_LEDGER_DRIFT` sigue
  siendo solo log local en `.protocol-tmp/`, gitignorado) pesa mas ahora, porque es la unica
  senal que quedaria si se corrige F-0280R2-01 por la via de senalar en vez de preservar.
- **R5 (nuevo).** Tras un `ROLLBACK_DEFER`, el residuo del exec fallido sobrevive por diseno
  (cero mutacion). Medido: `residue.txt` presente en W3 y W6. Correcto, pero si la causa del
  defer es persistente (cola rota), el residuo se acumula sin techo.
- **R6 (nuevo).** La derivacion resuelve el fichero de una tarea leyendo `TASK_INDEX.json`
  caliente. Una tarea cuya fila ya solo vive en `TASK_INDEX_ARCHIVE.json` no resuelve a ninguna
  ruta. Hoy no es alcanzable (la validacion rechaza tareas ausentes), por eso es residual y no
  hallazgo; queda como fragilidad si la poda y el rollback se cruzan.

## Lo que si esta bien, y quiero que se lea con el mismo peso

Los dos hallazgos que reporte estan cerrados de verdad, no de nombre, y en dos de los tres
vectores el hijo es **estrictamente mejor** que el codigo que hoy tienes desplegado:

- F-0280R1-01 cerrado. El `task_upsert` que crea un fichero de tarea nuevo (W1) sobrevive en
  `9c6f546` y se destruia en el padre. La derivacion por eventos es el discriminador correcto y
  esta bien construida para las `kind`s que si cubre.
- F-0280R1-02 cerrado y verificado donde importa: en el bucle real (W3), no en la sonda. El
  padre ladrillaba; el hijo difiere, mantiene la cola intacta y **vuelve a procesar el mensaje**.
- La cola desgarrada **no** puede confundirse con un log legitimo mas corto: lo probe con los dos
  logs que producen el mismo `seq` y el mismo `hash`, y el flag `torn_tail` los distingue
  (`true` vs `false`). El `seq` devuelto bajo cola rota es el del ultimo evento **completo**, asi
  que la cabeza no retrocede en silencio.
- La primitiva de cabeza sigue unica y las dos llamadas de `prune_state.py` siguen siendo
  compatibles con la firma nueva de 3-tupla (lo verifique explicitamente, porque cambiar la
  aridad de una funcion compartida es un sitio clasico donde se rompe un peer callado).
- Los tres negativos permanentes existen, la suite entera pasa en clon limpio, y la clasificacion
  de outcome de 0278 no se movio.

## Recomendacion de cierre

**CHANGE-REQUIRED.** TASK-0280 no puede pasar a `done` y **no** redesplegaria los dos crons con
este codigo sin la correccion de F-0280R2-01, que son dos rutas mas en una lista.

Sobre el redespliegue, que es tu decision real y no la mia: el hijo es mejor que el padre en
todo lo medido salvo dos vectores, y ninguno de los dos es alcanzable por Codex ni por el
Analista con las capabilities de hoy. Si el Operador decide que el coste de seguir en ventanas
exclusivas supera ese riesgo acotado, mi veredicto no es el argumento para impedirlo; pero
entonces quiero que quede escrito que se redespliega **sabiendo** que una poda gobernada
interrumpida borra la traza sin senal, y que la correccion es de dos lineas.

Bucle de arreglo esperado:

1. F-0280R2-01: anadir los dos espejos de archivo al conjunto base (o derivar el conjunto de la
   funcion del runtime). F-0280R2-02: que `Get-LedgerHead` no lance nunca desde el bucle.
2. Negativos permanentes nuevos: (a) `protocol_prune` firmado con fila movida al espejo + exec
   transitorio -> la fila esta en el espejo; (b) linea ilegible a media cola -> `ROLLBACK_DEFER`
   con motivo, residuo limpiado, sin `LOOP_ERROR` y mensaje aun procesable. Los dos por el bucle
   real, no por sonda de funcion extraida.
3. Gates a reejecutar en clon limpio: los seis de arriba.
4. Re-juicio independiente mio ANTES del commit de cierre.
5. **Tope agotado.** Esta era la iteracion 2 de 2 que declaraste, asi que esto va al Operador
   con este veredicto como evidencia. La decision de si se hace una iteracion 3 acotada a
   F-0280R2-01, o si se redespliega asumiendo el riesgo documentado, es suya, no mia.

-- Analista
