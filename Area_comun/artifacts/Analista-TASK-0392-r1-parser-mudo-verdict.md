# Analista -- veredicto TASK-0392 r1 (el detector autoritativo que se calla)

Ancla canonica: **`427dd0ef8cbc9daadcd66f2a7a8c2e9565bbd919`** ("fix(TASK-0392): execute the
exportable watchdog contract"), reproducido en clon limpio bajo
`D:/Aegis_Scratch/multi_agent_project_protocol/an0392r1/clone` (`git clone -s`, checkout del ancla,
arbol sin modificaciones). Alcance declarado por el Arquitecto: SOLO hub, sin producto -- `npm test`
no gateado. Iteracion 1 de 2.

## Veredicto

**CHANGE-REQUIRED**, por UN bloqueante, y no es ninguno de los R1-R5: los cinco estan cumplidos en
su letra. El bloqueante es un hueco NUEVO que abre la propia implementacion del R3.

> El detector de mailbox -- que esta guia acaba de declarar la **unica** senal autoritativa --
> **descarta en silencio** todo nombre que su parser no sepa leer, y el contrato de nombre que
> exige **contradice la plantilla que la propia guia publica**. Un adoptante que nombre sus
> mensajes segun `MSG-<date>-<sender>-<recipient>-*.md` -- la plantilla de la guia, y la del AC1 --
> arma un vigia que emite **cero** alertas y no dice nada al respecto.

Es la tesis de TASK-0392 un piso mas arriba: *"En el hub el filtro funciona hoy por accidente"*.
Aqui el detector funciona porque los ficheros del hub llevan `-to-` por costumbre. Cerrar sobre ese
verde exporta el mismo accidente, ahora en la capa que sostiene toda la garantia.

Y ademas hay un **BLOQUEANTE DE PROTOCOLO ajeno a esta tarea** que impide cualquier commit de
cierre: ver seccion 1.

## 1. Puertas de protocolo en el clon limpio -- una en ROJO, y no es de Codex

| Puerta | Comando | Exit |
|---|---|---|
| Estado colaborativo | `python scripts/validate_collaboration_state.py --root .` | **1** -- `Task TASK-0367 status mismatch: index='blocked' file='in_progress'` |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Drift de la cadena | `python runtime/protocol_replay.py --check-drift --root .` | **0** -- `verdict=CLEAN up_to_seq=9359` |

Medido tambien sobre `origin/main` (`9f715fa6`): **mismo error, exit 1**. Trazado por contenido: el
indice marca TASK-0367 `blocked` desde algun punto entre `546ce539` y `c1d79ee8`, mientras el
fichero de la tarea sigue diciendo `in_progress` en el commit. **No lo introdujo `427dd0ef`** y no
es de TASK-0392.

**El arreglo existe pero no esta commiteado**: el arbol compartido tiene
`Area_comun/tasks/TASK-0367-*.md` modificado sin commitear, y ese diff es exactamente
`-status: in_progress` / `+status: blocked` mas un bloque "Remediation r3 evidence". Es residuo de
un exec de Codex que hizo `ROLLBACK_DEFER reason=head_changed` a las 12:32 y quedo a medias.

Nota de metodo, porque me afecta a mi y afectaria a quien mida en caliente: **mi propio
`validate` de arranque sobre el arbol vivo dio exit 0**. Da verde precisamente porque esa
modificacion sin commitear hace que el fichero coincida con el indice. El arbol caliente miente en
la direccion mas peligrosa: dice que esta verde el estado que en canonico esta rojo.

**Efecto sobre esta tarea:** ninguno sobre su contenido, pero **el commit de cierre de TASK-0392
aterrizaria sobre un estado canonico ROJO**. Hay que verdear esto antes, y no es mio ni de Codex
(DECISION-0018: lo senalo, no lo toco).

## 2. Tabla vector por vector

| Vector | Lo que pedi en r0 | Veredicto | Evidencia |
|---|---|---|---|
| R1 | La prueba EJECUTA el filtro del entregable, no lo re-declara; restaurar la guia pre-fix da exit != 0 | **PASA, con limite medido** | `classify()` lee `WATCHDOG_COMMIT_TRAILER` de la guia y el fixture cablea esa clave: cambiar la clave en la guia pone la prueba roja. Pero el discriminante es de **un solo token**: experimento MUT1. |
| R2 | Trailer del fixture con la forma de NOVA; los DOS filtros sobre los mismos 4 commits, viejo 4/4, nuevo 2/2 | **PASA** | `MODEL_TRAILER = "Co-Authored-By: Claude (Opus) <shared-model@example.invalid>"`; asertan `len(old_own)==4`, `2/2` del filtro embarcado y `same_identity` (mismo `%an` y mismo trailer en los cuatro). Responde tu pregunta del R2: **si**, la clave por la que decide el filtro es la que escribe el fixture. |
| R3 | La asercion de mailbox ejercita el LISTADO y el parseo del nombre, no una posicion de commit | **SLIPS -- bloqueante** | El mecanismo si es un delta de listado real e independiente de la posicion (verificado). Pero el parser **falla cerrado y mudo** y su contrato de nombre contradice la plantilla de la guia. Experimentos P1-P8. |
| R4 | El texto exportable responde la copiabilidad: mecanismo infalsificable, o degradacion a orientativo declarada | **PASA, con hueco sin componer** | La guia declara marca publica y copiable, los modos de herencia, "advisory noise filter", "its silence is not evidence" y "only the mailbox signal is authoritative". Lo juzgo **cierto**. Falta la frase que compone el hueco. Experimento E2. |
| R5 | Refresco dentro del bucle, o precondicion explicita de arbol compartido | **PASA, condicional nombrado** | Paso 1 exige despliegue de arbol compartido y prohibe el uso fuera de el. Convierte la garantia en condicional y deja **sin procedimiento** al coordinador que vigila un remoto -- que es como esta armado el monitor de este mismo hub. |

## 3. El bloqueante, reproducido

### P1-P8 -- el detector autoritativo descarta en silencio (R3, AC1)

Extraje `mailbox_additions` y `MESSAGE_RE` del entregable y les pase mis propias cargas. El parser
es:

```python
MESSAGE_RE = re.compile(r"^MSG-[^-]+-(?P<sender>[^-]+)-to-(?P<recipient>[^-]+)-.+\.md$")
...
for name in sorted(current - previous):
    match = MESSAGE_RE.fullmatch(name)
    if match:
        alerts.append({"name": name, **match.groupdict()})
```

El `if match:` sin `else` es el defecto: un fichero **nuevo**, que **si** casa el glob configurado,
y que el parser no sabe leer, no produce alerta **ni diagnostico**. Medido:

```
P1 nombre con forma de hub (control)                 files=1 alerts=1
P2 plantilla LITERAL de la guia (<sender>-<recipient>) files=1 alerts=0   <-- cero
P3 fecha ISO con guiones                              files=1 alerts=0   <-- cero
P4 id de peon con guion (Worker-1)                    files=1 alerts=0   <-- cero
P5 recipient con guion (Coordinator-A)                files=1 alerts=1
P6 fichero ya visto (semantica de delta)              files=1 alerts=0   (correcto)
P7 sin sufijo tras el destinatario                    files=1 alerts=0   <-- cero
P8 dos entregas nuevas, una malformada                files=2 alerts=1   <-- una entrega perdida, sin aviso
```

El P2 es el que decide, y lo mida con los tres globs plausibles del adoptante:

```
glob=*-Coordinator-*     file=MSG-20990101-Worker-Coordinator-HANDOFF.md -> alerts=0
glob=*-to-Coordinator-*  file=MSG-20990101-Worker-Coordinator-HANDOFF.md -> alerts=0
glob=MSG-*               file=MSG-20990101-Worker-Coordinator-HANDOFF.md -> alerts=0
```

La contradiccion esta dentro de la propia guia, en tres sitios que no concuerdan:

- La plantilla publicada: ``MSG-<date>-<sender>-<recipient>-*.md`` -- **sin** `-to-`.
- El ejemplo de `<ALERT_ON_MESSAGES_TO_COORDINATOR>`: ``*-to-<COORDINATOR_ROLE>-*`` -- **con** `-to-`.
- El parser embarcado: exige `-to-` literal **y** prohibe guiones dentro de fecha, emisor y
  destinatario.

El paso 4 dice "parse its sender and recipient from the filename" y **no da la regla**. El AC1 de la
tarea usa la misma plantilla sin `-to-`. Es decir: el entregable detecta una forma de nombre que su
propio criterio de aceptacion no declara.

Y no es hipotetico en esta instancia: **hoy mismo `9f715fa6` archivo un handoff de peon "mal
formado"**. Con este detector, una entrega asi no genera alerta ninguna. Lo comprobe sobre el
listado real:

```
listado real (3 ficheros, 1 con nombre fuera de convencion), glob *-to-Arquitecto-*
  -> 1 alerta   (la malformada desaparece, sin traza)
```

**Por que bloquea.** Porque el R4 acaba de degradar el filtro de commits a orientativo y la guia
declara, con razon, que su silencio no es evidencia. Toda la garantia descansa ahora en esta senal.
Un detector que se calla ante lo que no sabe leer, montado por un adoptante que siguio la plantilla
publicada, es **un vigia mudo armado siguiendo la documentacion** -- la frase literal del intake de
TASK-0392. Y a diferencia del defecto original, este viene con un certificado en verde.

**Coste del arreglo: bajo.** (a) Declarar en la guia el contrato de delimitador, de modo que
plantilla, glob de ejemplo y parser digan lo mismo (y que fecha/emisor/destinatario no admitan el
delimitador). (b) Que el detector **falle ruidoso**: un nombre nuevo que casa el glob y no parsea
emite igualmente una alerta con el nombre crudo. Nunca descartar. (c) Que la prueba lo ejercite: una
carga con nombre no parseable tiene que producir alerta, no silencio.

## 4. Lo que no bloquea pero deberia viajar en la misma vuelta

### MUT1 -- el discriminante de la guia mide un token, no la guia (R1, AC3)

No repeti tu control A/B/C; monte el mutante que falta. Restaure la guia **PRE-FIX entera**
(`546ce539~1`, la que todavia prescribe `<SELF_COMMIT_FILTER>` dos veces y el filtro por modelo) y
le **anadi una sola linea**:

```
$ git show 546ce539~1:skills/session-watchdogs.skill.md > skills/session-watchdogs.skill.md
$ printf '\n    WATCHDOG_COMMIT_TRAILER = Protocol-Monitor-Origin\n' >> skills/session-watchdogs.skill.md
$ grep -c "SELF_COMMIT_FILTER" skills/session-watchdogs.skill.md
2
$ python scripts/harness/test_session_watchdog_filter.py --scratch-root .../s_mut1
OK: old filter silenced 4/4; shipped filter split 2/2; mailbox listing alerted
EXIT_MUT1=0
```

La guia revertida por completo al defecto original pasa la prueba con anadir una linea. Tu control
"guia pre-fix -> exit 1" es real, pero lo que discrimina es **la ausencia de esa linea**, no la
correccion del texto.

**Esto es culpa de mi especificacion, y lo digo con todas las letras**: mi R1 autorizo textualmente
"la prueba lee la clave del trailer de `skills/session-watchdogs.skill.md`". Codex implemento lo que
pedi. El hecho, aun asi, queda en pie, y es justo la propiedad para la que existe el AC3: la guia
manda ejecutar la prueba "before trusting silence", y la prueba no puede detectar que la guia haya
vuelto a mandar filtrar por modelo.

Arreglo barato y suficiente: que la prueba exija ademas que la guia **no** prescriba una regla de
descarte por autor, proveedor, modelo o co-autor (con la pre-fix eso da rojo: contiene
`<SELF_COMMIT_FILTER>`). No pido un analisis semantico del texto, pido un negativo.

### E2 -- el filtro descarta por subcadena, la guia dice "exact trailer" (R4)

`classify()` busca el token dentro del registro completo `%H\x1f%an\x1f%B`. Cargas:

```
worker, commit limpio                -> visible
coordinator, trailer real            -> FILTERED (silenced)
worker, marca en el ASUNTO           -> FILTERED (silenced)
worker, marca citada en la prosa     -> FILTERED (silenced)
worker, marca como NOMBRE DE AUTOR   -> FILTERED (silenced)
```

El paso 6 dice "Ignore a commit only when it has the **exact trailer**". La implementacion de
referencia embarcada no hace eso: cualquier aparicion de la cadena en asunto, cuerpo o nombre de
autor silencia. No hace falta mala fe -- basta un commit que *hable* del monitor citando la marca
para que ese commit desaparezca. Con el filtro ya degradado a orientativo esto es ruido, no
autorizacion, pero la guia y su referencia no dicen lo mismo.

### El hueco del commit-only: declarado en piezas, nunca compuesto (R4)

Respondo tu pregunta del encabezado, que es la buena.

**Que le queda al coordinador.** Le quedan los pasos 5-7 enteros. La degradacion quito la *pretension*
de que el silencio del filtro signifique algo; **no quito la alerta de commit**. Una entrega hecha
solo por commit y **sin** la marca sigue sonando como contexto secundario. El caso realmente
invisible es mas estrecho y mas afilado: **commit-only + marca heredada o copiada = silencio total**,
porque ahi no hay alerta de mailbox que el paso 7 pueda proteger.

**Esta declarado.** En piezas, y todas ciertas: la marca es publica y copiable (paso 6), los modos de
herencia estan listados (amend, cherry-pick, squash, plantilla), "its silence is not evidence", y
"only the mailbox signal is authoritative for delivery alerts". Lo que **no** esta es la
composicion. En ningun punto la guia dice *"una entrega que no abre mensaje puede quedar
completamente invisible para este vigia"*, ni enuncia la contramedida que lo cierra: **que una
instancia que use este vigia exige un mensaje de mailbox por cada entrega**. Hoy el adoptante tiene
que derivar el hueco cruzando tres parrafos.

**Me parece aceptable como residuo**, con esa frase escrita y con la exigencia de mensaje-por-entrega
enunciada. Sin ellas, la guia es un conjunto de verdades del que no se sigue una accion.

**Y sobre tu decision de frontera: la comparto, y creo que es la correcta.** Tus tres razones se
sostienen, en particular la segunda -- un filtro que *parece* infalsificable invita a fiarse de su
silencio. Un mecanismo fuera del cuerpo del mensaje (git note, ref no publicado) seria superficie
nueva cuya infalsificabilidad habria que demostrar, para una capa de conveniencia. Orientativo y
declarado es el trato bueno. Lo unico que la degradacion exige a cambio es que la senal que **si**
es autoritativa no se calle -- que es exactamente lo que bloquea esta vuelta.

## 5. R5: el condicional, nombrado como pediste

Si, convierte una garantia en condicional, y hay que decir cual. El paso 1 exige arbol compartido y
prohibe el uso fuera de el "until a runbook-defined refresh materializes both signals inside the
loop". Ese runbook **no viaja en el paquete exportable**. Consecuencia concreta: el coordinador que
vigila un remoto -- que es como esta armado el monitor de este mismo hub, sobre `origin/main` -- lee
"no uses este vigia" y no encuentra el siguiente paso. La precondicion es honesta y era una de las
dos salidas que ofreci; el residuo es que la salida elegida deja sin procedimiento al despliegue mas
probable.

## 6. Residuos declarados, no bloqueantes

- `len(old_own) == 4` es cierto por construccion de `commit()`: documenta el escenario de NOVA, no
  lo mide de forma independiente. Lo pedi asi; queda dicho.
- El delta de mailbox de la prueba usa `previous = set()` cableado, no una primera lectura real del
  directorio. El mecanismo si es delta (verificado en P6), pero la prueba no ejercita la
  deduplicacion entre sondeos.
- `load_trailer_key` exige **exactamente una** aparicion del contrato en la guia: cualquier segundo
  ejemplo futuro rompe la prueba. Falla cerrado, asi que solo es fragilidad.
- Fuera de mi alcance y no juzgado: TASK-0386, TASK-0395 (avisado y no tocado; no tropece con el),
  el monitor de la sesion interactiva del Arquitecto, y cualquier cosa de producto.

## 7. Lazo de correccion esperado

Iteracion **1 de 2**. Maximo 2 antes de escalar al operador humano.

- **B1 (bloqueante, R3/AC1).** Contrato de nombre declarado en la guia -- plantilla, glob de ejemplo
  y parser diciendo lo mismo, con el delimitador prohibido dentro de fecha/emisor/destinatario -- y
  detector que **falla ruidoso**: nombre nuevo que casa el glob y no parsea emite alerta con el
  nombre crudo. Gate de mutacion: una carga con nombre no parseable tiene que producir alerta.
- **D1 (deberia viajar, R1/AC3).** Que la prueba exija ademas que la guia no prescriba descarte por
  autor/committer/proveedor/modelo/co-autor. Gate: la guia pre-fix **con** la linea de contrato
  anadida tiene que dar exit != 0 (hoy da 0).
- **D2 (deberia viajar, R4).** Componer el hueco en una frase -- una entrega sin mensaje de mailbox
  puede ser invisible -- y enunciar la exigencia de mensaje-por-entrega para instancias que usen el
  vigia. Y alinear paso 6 ("exact trailer") con lo que hace la referencia, o al reves.
- **P0 (bloqueante de protocolo, ajeno a TASK-0392 y a Codex).** `validate_collaboration_state.py`
  da exit 1 en el ancla y en `origin/main` por el desajuste de TASK-0367. Verdear antes de cualquier
  commit de cierre. Owner: Arquitecto (el arreglo esta sin commitear en el arbol compartido).

Puertas a re-verificar en la vuelta 2, en clon limpio y por exit code:
`validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`,
`protocol_replay.py --check-drift`, la prueba embarcada, mas mi re-juicio ANTES del commit de cierre.

## 8. Nota para el Arquitecto

Que quede claro el balance, porque r1 es una vuelta buena: los cinco vectores estan cumplidos en su
letra, el fixture ya reproduce el 4/4 de NOVA con identidad de git y de modelo compartidas, la
asercion de mailbox ya es independiente de la posicion del commit, y el texto exportable ya dice la
verdad sobre lo que el filtro no garantiza. Tu decision de degradar a orientativo la comparto y la
razon 2 es la correcta.

Lo que no puedo cerrar es que, al mover toda la garantia a la senal de mailbox, esa senal haya
quedado con un descarte mudo y con un contrato de nombre que la guia no publica. El defecto que
TASK-0392 vino a cerrar no era "el filtro esta mal elegido": era **"un vigia armado siguiendo la
documentacion no avisa de ninguna entrega, y su silencio se lee como que los peones trabajan"**. Con
la plantilla que la guia publica, eso vuelve a ser cierto -- y ahora ademas con un verde que lo
respalda.

Y sobre tu nota de honestidad del `exit 2`: me parece la parte mas util de tu mensaje. Un codigo
uniforme en los tres brazos es la firma de un instrumento que no llega a medir, y decirlo evita que
el siguiente lo lea como un veredicto. Lo mismo me paso hoy en el otro sentido: mi `validate` en
caliente dio verde sobre un canonico que esta rojo.

-- Analista, 2026-08-15 12:55 local (UTC+2)
