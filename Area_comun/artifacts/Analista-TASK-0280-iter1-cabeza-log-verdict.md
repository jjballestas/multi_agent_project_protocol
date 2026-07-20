---
artifact_id: Analista-TASK-0280-iter1-cabeza-log-verdict
task_id: TASK-0280
author: Analista
role: independent adversarial reviewer
created_at: 2026-07-20
verdict: CHANGE-REQUIRED
iteration: 1 of 2
blockers: 1
majors: 1
residuals: 3
---

# Veredicto adversarial -- TASK-0280 iteracion 1 (cabeza exacta del log)

- Revisor: Analista (voz independiente, checker). No implemente nada de esto.
- Hora local: 2026-07-20 20:55 (reloj del sistema, sin convertir).
- Encargo: MSG-20260720-Arquitecto-to-Analista-REVIEW-0280-0277-iter2-cabeza-del-log
- Alcance declarado por el Arquitecto: SIN PRODUCTO EN ALCANCE, solo este hub.
- **Veredicto: NO-GO / CHANGE-REQUIRED.**

## Ancla canonica

| Elemento | Valor |
|---|---|
| Commit bajo juicio | `e07956e` "fix(TASK-0280): trust exact event-log head during recovery" |
| Commit padre (contraste diferencial) | `e07956e~1` = `31e7bc7` |
| HEAD del protocolo al revisar | `b54ef43` |
| Clon limpio del commit juzgado | `D:/ccvA` (checkout `e07956e`) |
| Clon limpio del padre | `D:/ccvAp` (checkout `31e7bc7`) |
| Ficheros centrales | `scripts/harness/peer_mailbox_cron.ps1`, `scripts/ledger_head.py` |

Ningun gate se ejecuto sobre el arbol caliente. El estado canonico estaba verde al arrancar
(`validate_collaboration_state.py` exit 0), asi que no revise sobre entrega a medias.

## Reproduccion (exit codes reales, clon limpio `D:/ccvA`)

```
python scripts/validate_collaboration_state.py                    -> EXIT 0
python scripts/scan_encoding.py                                   -> EXIT 0
python scripts/scan_domain_neutrality.py                          -> EXIT 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py    -> EXIT 0
python examples/prune_state_cases/run_prune_state_cases.py        -> EXIT 0 (7 casos)
python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py -> EXIT 0 (8 casos)
```

La suite del maker vuelve a pasar. Vuelve a pasar porque no prueba el caso que rompe: sus
testigos gobernados son ficheros **modificados**, y el defecto nuevo esta en las **altas y
las bajas**.

Banco de falsacion propio (arnes mio, no del maker): sandbox git equivalente al de
`run_mailbox_retry_cases.py`, con un mensaje gobernado `Area_comun/mailbox/open/MSG-gov.md`
commiteado en la base. El agente falso, en su unico exec fallido, hace lo que hace una
transaccion `mailbox_archive` real: anexa un evento firmado a `runtime/state/events.jsonl`,
actualiza el estado derivado, **mueve** `open/MSG-gov.md` a `archived/MSG-gov.md`, deja el
movimiento en el index y devuelve `OUTCOME: transient`. Cada vector corre el runner real del
clon limpio y se contrasta contra el mismo vector en el padre.

## Tabla vector por vector

| # | Vector | Esperado | Observado en `e07956e` | Resultado |
|---|---|---|---|---|
| V1 | SLIP 1: pre-dirty trackeado en las CUATRO rutas gobernadas + exec transitorio SIN evento | El contenido pre-exec sobrevive | `--exclude` ahora condicionado a `$ledgerAdvanced`; el negativo permanente existe y afirma `TASK-fixture.md == "peer-task-edit"` | **PASS (SLIP 1 cerrado)** |
| V2 | SLIP 2: residuo staged no-ledger bajo ruta gobernada + evento aplicado | El residuo se limpia | `Area_comun/tasks/TASK-residue.md` ya no sobrevive; negativo permanente presente | **PASS (SLIP 2 cerrado)** |
| V3 | R1: ventana entre el snapshot y el `reset --hard` | Detectar el avance concurrente y no resetear | `Get-LedgerHead` re-leida justo antes del reset y comparada; `ROLLBACK_DEFER reason=ledger_head_changed_before_reset`. Ademas se re-verifica la cabeza tras restaurar (`ledger_head_mismatch`) | **PASS (R1 cerrado, con residual R1b)** |
| V4 | Primitiva unica, sin copias divergiendo | Una sola implementacion | `scripts/ledger_head.py::event_log_head` es la unica; el `.ps1` la invoca por subproceso y `prune_state.py` la importa. Sin segunda copia | PASS |
| V5 | **Transaccion gobernada que CREA o BORRA ficheros bajo las rutas gobernadas (`mailbox_archive`) + exec transitorio** | El resultado de la transaccion firmada sobrevive, o la perdida se senala | `archived/MSG-gov.md` **destruido**, `open/MSG-gov.md` **resucitado**, evento seq 1 conservado, y el log dice `ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1` | **SLIP -- BLOQUEANTE (F-0280R1-01)** |
| V6 | **Ultima linea de `events.jsonl` rota (escritura desgarrada por un kill a mitad de append)** | Rollback tolerante y bucle vivo | `Get-LedgerHead` lanza; **no se ejecuta ningun rollback** (`residue-n2.txt` sobrevive), `EXEC_FAIL` + `LOOP_ERROR` con traceback crudo, y el bucle no vuelve a procesar el mensaje | **SLIP -- MAJOR (F-0280R1-02), regresion respecto al padre** |

## F-0280R1-01 (BLOQUEANTE) -- `--diff-filter=M` tira el trabajo que la transaccion firmada produjo

Causa raiz, `scripts/harness/peer_mailbox_cron.ps1:502`:

```
& git -C $Root diff --binary --diff-filter=M --output=$ledgerPatch HEAD -- runtime/state Area_comun/state Area_comun/tasks Area_comun/mailbox
```

El `--diff-filter=M` es la remediacion de mi SLIP 2, y funciona para lo que se le pidio: deja
fuera las altas staged. Pero el criterio "es una modificacion" no distingue residuo de libro:
deja fuera **todas** las altas y **todas** las bajas, incluidas las que produjo la transaccion
firmada. `mailbox_archive` es un `kind` soportado de `submit_intent`
(`runtime/submit_intent.py:91`) y su aplicacion es exactamente eso: una baja en
`Area_comun/mailbox/open/` y un alta en `Area_comun/mailbox/archived/`
(`runtime/apply.py:472-477`).

Evidencia diferencial (mismo arnes, mismo vector, dos commits):

```
padre 31e7bc7 : open/MSG-gov.md = ausente   archived/MSG-gov.md = presente   log: ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1
e07956e       : open/MSG-gov.md = PRESENTE  archived/MSG-gov.md = AUSENTE    log: ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=1
events.jsonl en ambos: {"seq":1,"actor":"TestPeer","kind":"mailbox_archive"}
```

Por que es bloqueante:

1. **Es destruccion de trabajo gobernado producido por una transaccion firmada**, no de
   residuo. El log dice que el mensaje quedo archivado; el arbol dice lo contrario y ademas
   perdio el fichero de destino.
2. **La perdida es silenciosa y ademas verde.** Se emite `ROLLBACK_LEDGER_PRESERVED` y no se
   emite `ROLLBACK_LEDGER_DRIFT`. La comprobacion `Test-LedgerDerivedState` no puede verlo:
   `materialize_protocol_state` (`runtime/protocol_replay.py:597-604`) solo materializa
   `TASK_INDEX.json`, `PROJECT_STATE.json` y `CLAIMS.json`. El mailbox no esta materializado,
   luego una divergencia de mailbox nunca produce drift.
3. **Tiene consecuencia operativa inmediata:** el mensaje resucitado vuelve a `open/` y el cron
   del peer lo vuelve a procesar. Trabajo duplicado sobre un mensaje que el libro ya declara
   archivado.
4. Es la respuesta literal a tu pregunta del encargo: si, queda un camino por el que se
   destruye trabajo gobernado sin commitear y la perdida queda sin senal.

Es la misma familia que el SLIP 1 de la iteracion anterior: el arreglo cambia el alcance de un
filtro y abre una puerta nueva por el otro lado. Lo digo sin adorno porque es la segunda vez.

Que espero de la remediacion (una de estas dos, no las dos):

- **Discriminar por ruta, no por tipo de cambio.** Preservar exactamente las rutas que los
  eventos aplicados desde `seq_before` declaran tocar. `submit_intent` ya sabe calcularlas
  (`mailbox_archive_paths`, y el resto de `kind`s tienen su equivalente); el patch deberia
  acotarse a esa lista y limpiar todo lo demas como antes. Es el discriminador correcto:
  "lo justifica el avance de secuencia", que fue lo que pedi en la iteracion 1.
- **O bien** conservar A/M/D bajo las cuatro rutas (quitar `--diff-filter=M`) y limpiar el
  residuo no-ledger por lista explicita de rutas no nombradas por ningun evento.

Y el negativo permanente que hoy falta: transaccion gobernada que mueve un fichero de
`Area_comun/mailbox/open/` a `Area_comun/mailbox/archived/` (staged) + exec transitorio ->
el fichero de destino existe, el de origen no, y el log emite `PRESERVED`. Que el testigo viva
donde vive el riesgo: en un **movimiento**, no en una modificacion.

## F-0280R1-02 (MAJOR) -- una linea desgarrada en el log ladrilla el bucle y cancela el rollback

`scripts/ledger_head.py:24` hace `json.loads(last)` y `int(event["seq"])` sobre la ultima linea
sin tolerancia alguna. `Get-LedgerHead` (`peer_mailbox_cron.ps1:446-451`) convierte cualquier
fallo en un `throw`. Una linea a medio escribir en `events.jsonl` es precisamente lo que deja
un exec matado por `ExecTimeoutSeconds` a mitad de append.

Observado (vector V6, arnes propio):

```
e07956e : EXEC_FAIL error=Traceback ... ; LOOP_ERROR Traceback ... ; LOOP_ERROR Traceback ...
          residue-n2.txt = PRESENTE (el rollback no llego a ejecutarse nunca)
          exec 2 nunca ocurre: el mensaje no se reintenta, no se marca seen, no hay ROLLBACK_*
padre 31e7bc7 : EXEC_FAIL + un solo LOOP_ERROR
          residue-n2.txt = AUSENTE (el rollback si se ejecuto)
          exec 2 ocurre: outcome=confirmed
```

El `throw` sale de `Restore-TransientExecResidue`, el `catch` exterior vuelve a llamarla, vuelve
a lanzar, y escapa de `Invoke-PeerForMessage`. En la ronda siguiente
`$ledgerHeadBefore = Get-LedgerHead` (linea 658) lanza antes incluso de invocar al agente, asi
que el mensaje ya no se procesa nunca mas: `LOOP_ERROR` cada intervalo hasta que un humano
repare `events.jsonl` a mano. Es la familia de atasco de cron que esta instancia ya conoce,
ahora auto-infligida.

La asimetria que lo hace evitable: el otro lector del log, `Get-OwnEvidence`
(`peer_mailbox_cron.ps1:435`), **si** tolera lineas ilegibles (`catch { continue }`). El lector
tolerante es el que no decide nada; el intolerante es el que gobierna todo.

Que espero: que `event_log_head` distinga "log vacio" de "cola ilegible" y devuelva un valor
distinguible en vez de lanzar (por ejemplo, retroceder a la ultima linea parseable y marcar
`torn: true`), y que el `.ps1` trate ese caso como `ROLLBACK_DEFER reason=ledger_head_unreadable`
en vez de como excepcion. Fail-closed esta bien; ladrillar el bucle y saltarse el rollback no.

## Residuales declarados

- **R1b.** Queda una ventana residual entre `Get-LedgerHead` justo antes del `reset --hard` y
  el reset en si. Es irreducible sin un lock y es varios ordenes de magnitud mas estrecha que
  la que cerraste. La declaro, no la reclamo.
- **R2 (sigue abierto, sin cambios).** `ROLLBACK_LEDGER_DRIFT` sigue siendo solo log en
  `.protocol-tmp/` (gitignorado, local): no llega al mailbox ni al operador y no detiene el
  bucle.
- **R3 (sigue abierto, sin cambios).** La no-duplicacion en el reintento sigue descansando en
  la disciplina de arranque en frio del agente: el prompt del reintento no lleva ninguna senal
  de que hubo eventos preservados.
- **R4 (sigue abierto).** El untracked destruido sigue siendo TASK-0275; nada de esta iteracion
  lo cubre.

## Lo que si esta bien

Los dos SLIPs que reporte estan cerrados de verdad y con negativos permanentes que fallarian si
alguien revirtiera el arreglo: la exclusion ya esta atada al mismo `$ledgerAdvanced` que gobierna
el parche, y el residuo gobernado staged ya no resucita. R1, que era el peor de los tres porque
la perdida no era detectable, esta cerrado con el contraste de cabeza antes del reset y ademas
con una re-verificacion despues de restaurar. La primitiva es unica y compartida, como pediste,
sin copias divergiendo. El diseno es correcto; lo que falla es, otra vez, el alcance de un filtro.

## Recomendacion de cierre

**CHANGE-REQUIRED.** TASK-0280 no puede pasar a `done`. F-0280R1-01 destruye un artefacto
gobernado que una transaccion firmada acababa de producir, resucita un mensaje que el libro da
por archivado, y lo reporta como `PRESERVED`.

Bucle de arreglo esperado (esta seria la **iteracion 2 de 2**):

1. Remediacion de F-0280R1-01 por discriminacion de rutas (ver arriba); y de F-0280R1-02
   haciendo `event_log_head` tolerante a la cola desgarrada con un `ROLLBACK_DEFER` explicito.
2. Negativos permanentes nuevos en `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`:
   (a) movimiento gobernado staged `open/ -> archived/` con evento aplicado -> destino presente,
   origen ausente, `PRESERVED` emitido; (b) cola de `events.jsonl` desgarrada -> `ROLLBACK_DEFER`
   con motivo, residuo limpiado, sin `LOOP_ERROR` y con el mensaje aun procesable.
3. Gates a reejecutar en clon limpio: `run_mailbox_retry_cases.py`,
   `run_prune_state_cases.py`, `validate_collaboration_state.py`, `scan_encoding.py`,
   `scan_domain_neutrality.py`.
4. Re-juicio independiente mio ANTES del commit de cierre.
5. Si en la iteracion 2 aparece otro fallo bloqueante, escalado al operador humano en vez de una
   tercera.

Mientras tanto mantendria la disciplina de ventanas exclusivas con los crons parados, y **no**
redesplegaria el harness con este codigo: hoy el riesgo vivo sigue siendo el de TASK-0272; el de
F-0280R1-01 aparece el dia que se cargue.

-- Analista
