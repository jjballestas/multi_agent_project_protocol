# Analista -- veredicto TASK-0392 (el vigia que parecia armado)

Ancla canonica: **`546ce539f05b44d5b81d74fa3bc03f49c760202b`** ("fix(TASK-0392): make mailbox the
primary delivery signal"), reproducido en clon limpio bajo
`D:/Aegis_Scratch/multi_agent_project_protocol/analista-0392/clone` (`git clone -s`, checkout del
ancla, arbol sin modificaciones). Alcance declarado por el Arquitecto: SOLO hub, sin producto --
`npm test` no gateado.

## Veredicto

**CHANGE-REQUIRED.** El AC4 esta cumplido de verdad: el texto exportable ya no prescribe el filtro
por modelo. Pero **el AC3 no acredita nada**, y lo demuestro con dos controles que el propio
encargo pedia:

> La prueba entregada sale **exit 0 con la guia PRE-FIX restaurada**, y tambien **exit 0 con la
> guia BORRADA**. No lee el entregable que dice validar.

Y la pregunta del encabezado tiene respuesta afirmativa y medida: **si, un peon puede escribir la
marca**. No necesita adivinarla -- la marca se publica en el cuerpo de cada commit que la usa, asi
que se recupera con un `git log`.

## Puertas de protocolo en el clon limpio (todas verdes)

| Puerta | Comando | Exit |
|---|---|---|
| Estado colaborativo | `python scripts/validate_collaboration_state.py --root .` | **0** -- `OK: collaboration state is valid.` |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** -- `OK: encoding scan is clean.` |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Drift de la cadena | `python runtime/protocol_replay.py --check-drift --root .` | **0** -- `verdict=CLEAN up_to_seq=9338` |
| Prueba entregada | `python scripts/harness/test_session_watchdog_filter.py --scratch-root ...` | **0** -- `OK: 2 coordinator filtered, 2 worker retained, mailbox delivery alerted` |

Ninguna puerta protocolar bloquea. Lo que bloquea es la **conducta** de lo entregado. (Aviso
recibido y comprobado sin coste: no tropece con `run_mailbox_retry_cases.py`; no estaba en mi gate.)

## Tabla vector por vector

| AC | Lo que promete | Veredicto | Evidencia |
|---|---|---|---|
| AC1 | El monitor detecta la entrega por el MAILBOX, no por el commit | **SLIPS** | La prosa (paso 4) es correcta; **la prueba no la ejecuta**. Su "alerta de mailbox" es `MSG-... in git show --name-only HEAD~2`: una posicion de commit fija. Experimento A1a/A1b. |
| AC2 | El descarte va por marca que SOLO el coordinador escribe | **SLIPS** | La regla textual es correcta y explicita. El **mecanismo** no existe: la marca viaja en el cuerpo del commit, luego es publica y copiable. Experimento E. |
| AC3 | Procedimiento EJECUTADO que separa 2 propios de 2 de peon, y que hay que comprobar antes de fiarse del silencio | **FALLA** | La prueba re-declara el filtro dentro de si misma. Verde con la guia pre-fix (Exp. B) y con la guia borrada (Exp. C). Ademas su fixture no reproduce el fallo de NOVA (Exp. D). |
| AC4 | La guia EXPORTABLE corregida, con diff, no con una nota | **PASA** | `skills/session-watchdogs.skill.md` (`neutral_core: true`) sustituye `<SELF_COMMIT_FILTER>` por `<COORDINATOR_COMMIT_MARKER>` y reordena el algoritmo a mailbox-primero; `scripts/harness/README.md` acompana. Es diff, no nota. Neutralidad exit 0. |

## Reproduccion de los hallazgos

### B/C -- la prueba no mira el entregable (bloqueante del AC3)

En el mismo clon limpio, sobre el ancla:

```
# B: restaurar la guia DEFECTUOSA y volver a correr la prueba
git show 546ce539~1:skills/session-watchdogs.skill.md > skills/session-watchdogs.skill.md
grep -n "SELF_COMMIT_FILTER" skills/session-watchdogs.skill.md
   33:- `<SELF_COMMIT_FILTER>`: expression that identifies commits produced by the
   54:5. Ignore commits matching `<SELF_COMMIT_FILTER>`.
python scripts/harness/test_session_watchdog_filter.py --scratch-root .../an0392-b
   EXIT_B=0
   OK: 2 coordinator filtered, 2 worker retained, mailbox delivery alerted

# C: BORRAR la guia y revertir el README, y volver a correr
rm -f skills/session-watchdogs.skill.md
git show 546ce539~1:scripts/harness/README.md > scripts/harness/README.md
python scripts/harness/test_session_watchdog_filter.py --scratch-root .../an0392-c
   EXIT_C=0
   OK: 2 coordinator filtered, 2 worker retained, mailbox delivery alerted
```

La causa esta a la vista en `scripts/harness/test_session_watchdog_filter.py`: el filtro no se
importa de ningun sitio, se vuelve a escribir dentro del test.

```python
MARKER = "coord-session-proof-7f6d"
own     = [r for r in commits if f"Protocol-Monitor-Origin: {MARKER}" in r]
visible = [r for r in commits if f"Protocol-Monitor-Origin: {MARKER}" not in r]
```

`own` y `visible` son complementarios por construccion: `len(own) == 2 and len(visible) == 2` es la
misma afirmacion dicha dos veces, comprobada contra una constante del propio fichero. **El unico
entregable que la prueba puede romper es la prueba.** Es el patron de "mutar produccion, no los
mutantes del runner": un verde que el codigo viejo -- y el codigo ausente -- tambien produce.

### D -- el fixture no reproduce el fallo de NOVA (bloqueante del AC3)

El encargo pedia el control historico: correr la prueba contra el filtro anterior y exigir que
falle. No es ejecutable tal cual, porque el filtro viejo no es un parametro. Lo instrumente aparte,
levantando los MISMOS cuatro commits y pasandoles las dos expresiones:

```
D. fixture ENTREGADO   trailer: Co-Authored-By: Shared Model <shared-model@example.invalid>
   filtro VIEJO  Co-Authored-By: Claude (Opus|Fable|Sonnet)  ->  0/4 propios
   filtro NUEVO  Protocol-Monitor-Origin: <marca>            ->  2/4 propios

D2. fixture con el trailer REAL de NOVA   trailer: Co-Authored-By: Claude (Opus)
   filtro VIEJO  ->  4/4 propios   <- el vigia mudo, reproducido
   filtro NUEVO  ->  2/4 propios
```

NOVA midio **7 de 7 clasificados como propios**. El fixture entregado da **0 de 4**: su trailer
compartido (`Shared Model`) no es aquel por el que el filtro viejo indexaba, asi que el escenario
montado no es el que fallo en campo. Lo que el fixture demuestra es que una marca que solo esta en
dos commits aparece en dos commits. Con el trailer con forma de NOVA (D2) el control si discrimina
-- 4/4 contra 2/2 --, y es la forma que el fixture deberia haber usado.

### E -- la marca es copiable, y se publica al usarla (bloqueante del AC2)

Respuesta directa a la pregunta del encabezado. Un peon no tiene que adivinar la marca: la lee del
historico, porque va en el cuerpo del commit.

```
marker recovered from `git log` by a worker: 'coord-session-proof-7f6d'
commits total                     : 3
commits SILENCED by the new filter: 3   (2 de ellos son commits de PEON)
```

La guia dice "workers must never add it". Eso es una **norma, no un mecanismo** -- exactamente la
frontera que TASK-0386 abre en el gate de claim. Y la reproduccion no exige mala fe: un `--amend`,
un `cherry-pick`, un `squash`, o una plantilla de mensaje copiada arrastran el trailer y silencian
al que lo herede.

Hay un atenuante real y hay que decirlo: el paso 7 de la guia declara que **la alerta de mailbox del
paso 4 nunca la cancela el filtro**, asi que una entrega que ABRE mensaje sigue sonando aunque su
commit lleve la marca copiada. El agujero que queda es la entrega **que no abre mensaje**: commit de
codigo con la marca heredada = silencio total. El filtro viejo fallaba abierto de golpe (lo ocultaba
todo); el nuevo falla abierto en cuanto alguien copia una linea. Es una mejora, no un cierre.

### A1 -- la prueba no ejercita el mailbox (bloqueante del AC1)

La comprobacion de mailbox entregada es, literal:

```python
changed = run(repo, "show", "--name-only", "--format=", "HEAD~2")
mailbox_alert = "MSG-20990101-Worker-to-Coordinator-HANDOFF.md" in changed
```

Dos mutaciones sobre el mismo fixture:

```
A1a. La MISMA entrega de mailbox movida del commit 2 al commit 4
     entrega realmente presente en el arbol : True
     la asercion entregada (HEAD~2) dice    : False     <- rojo con la entrega presente

A1b. SIN directorio de mailbox: un fichero plano en la raiz que solo lleva ese nombre
     Area_comun/mailbox/open existe          : False
     la asercion entregada (HEAD~2) dice     : True      <- verde sin mailbox ninguno
```

Es decir: la asercion sigue una **posicion de commit** y busca un nombre dentro de un **diff de
commit** -- la senal centrada en el commit que justamente el AC1 degrada. El paso 4 de la guia
(diferenciar el LISTADO del directorio de mailbox entre dos sondeos y parsear emisor/destinatario
del nombre) no se ejecuta en ningun punto de la prueba.

## Residuo declarado (no bloqueante, pero deberia viajar en la misma correccion)

**El bucle no se refresca.** El paso 1 fija `base` con `git rev-parse <LOCAL_REF>` ("usually
`HEAD`") y el paso 4 compara el listado del directorio LOCAL de mailbox; "Refresh from the
configured remote" figura bajo *Response after an alert*, es decir **despues** de la alerta, luego
no puede causarla. En una instancia de arbol compartido eso funciona. En una instancia donde el
coordinador vigila un remoto (que es como esta armado el monitor del propio hub, sobre
`origin/main`), un `fetch` no cambia ni el ref local ni los ficheros de `mailbox/open/`: las **dos**
senales quedan muertas y el silencio vuelve a leerse como "los peones trabajan". La guia exportable
deberia o meter el refresco DENTRO del bucle, o declarar explicitamente que asume arbol compartido.

Fuera de mi alcance y no juzgado: TASK-0386 (identidad en la autorizacion), el monitor de la sesion
interactiva del Arquitecto del hub, y cualquier cosa de producto.

## Lazo de correccion esperado

Maximo **2 iteraciones** antes de escalar al operador humano. Puertas a re-verificar en cada vuelta:
`validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`, mas mi re-juicio ANTES del commit de cierre.

- **R1 (AC3, bloqueante).** Que la prueba EJECUTE el filtro del entregable en vez de re-declararlo:
  una unica definicion legible por maquina que compartan guia y prueba (la prueba lee la clave del
  trailer de `skills/session-watchdogs.skill.md`, o la guia apunta a una funcion de filtro embarcada
  que la prueba importa). Gate de mutacion obligatorio: **restaurar `546ce539~1:skills/
  session-watchdogs.skill.md` tiene que dar exit != 0**. Ese es el discriminante que se pidio.
- **R2 (AC3, bloqueante).** Que el trailer compartido del fixture sea aquel por el que el filtro
  viejo indexaba (forma `Co-Authored-By: Claude (Opus)`), y que la prueba pase **los dos** filtros
  sobre los mismos cuatro commits, exigiendo viejo = 4/4 propios (vigia mudo reproducido) y nuevo =
  2/2. Sin eso el control historico no es ejecutable.
- **R3 (AC1, bloqueante).** Que la asercion de mailbox ejercite el paso 4 -- diferencia de LISTADO
  del directorio entre dos sondeos y parseo de emisor/destinatario del nombre -- y no una posicion
  de commit. Tiene que seguir verde cuando la entrega cambia de posicion (A1a) y ponerse roja cuando
  no hay mensaje de mailbox (A1b).
- **R4 (AC2, bloqueante).** Que el texto exportable responda la copiabilidad. O se nombra el
  mecanismo que hace la marca infalsificable -- y hay que tener en cuenta que **un trailer en el
  cuerpo se publica por construccion**, luego el mecanismo tendria que sacarla del mensaje (una git
  note local, un ref que el coordinador no publica) --, o, si no hay mecanismo, se degrada el filtro
  de commits a orientativo y se declara en la guia que una marca copiada o heredada (amend,
  cherry-pick, squash, plantilla) silencia el commit de un peon, de modo que el silencio nunca sea
  evidencia.
- **R5 (residuo, deberia viajar).** Refresco dentro del bucle, o precondicion explicita de arbol
  compartido.

## Nota para el Arquitecto

Lo entregado va en la direccion correcta y el AC4 lo acredita: mailbox-primero es el diseno bueno, y
el texto exportable ya no manda filtrar por proveedor y modelo. NOVA estaria mejor con esta guia que
con la anterior. Lo que no puede cerrarse es el AC3, porque es literalmente el AC que NOVA pidio:
*"hoy nada obliga a validar el vigia antes de fiarse de su silencio"*. La prueba embarcada no valida
el vigia -- se valida a si misma, y seguiria en verde el dia que alguien revierta la guia entera.
Cerrar sobre ese verde exportaria a NOVA la misma clase de defecto que la tarea vino a arreglar, un
piso mas arriba: antes el vigia parecia armado, ahora ademas trae un certificado de que lo esta.

-- Analista, 2026-08-15 (UTC+2)
