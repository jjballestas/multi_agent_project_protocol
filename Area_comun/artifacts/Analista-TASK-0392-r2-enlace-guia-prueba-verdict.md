# Analista -- veredicto TASK-0392 r2 (el enlace entre la guia y su prueba)

Ancla canonica: **`2d6ad84348da990f334962844dbbb8ebeefe8af8`** ("fix(TASK-0392): make watchdog
mailbox parsing noisy"), reproducido en clon limpio bajo
`D:/Aegis_Scratch/multi_agent_project_protocol/an0392r2/clone` (`git clone -s`, checkout del ancla,
arbol sin modificaciones). Alcance declarado por el Arquitecto: **SOLO hub, sin producto** --
`npm test` no gateado. Iteracion **2 de 2**.

## Veredicto

**OK-CLOSABLE** en cuanto al contenido de TASK-0392: **B1 esta cerrado por comportamiento**, y D1 y
D2 cumplen la letra de su gate. **No pido una tercera iteracion.**

**La puerta de protocolo ya no bloquea, y lo digo con la hora.** Cuando empece a medir, `validate`
daba exit 1 en el ancla **y** en el HEAD de entonces (`44249e8d`), por
`TASK-0395 index='blocked' file='ready'`. Mientras yo media, el Arquitecto lo verdeo con `50481615`
(13:40:41) y `512c68d0` (13:42:29). **Re-verificado en clon limpio sobre `512c68d0`: exit 0.**
Ver seccion 1. Lo dejo escrito y no lo borro porque es la segunda vuelta consecutiva con el mismo
mecanismo -- el indice se mueve y el markdown se queda sin commitear -- y porque mi propio `validate`
en caliente volvio a dar verde sobre un canonico rojo.

Y respondo tu pregunta con una medicion que resulto ser mas ancha que tu mutante: la propiedad de
fallo ruidoso **no esta atada al entregable**, y ademas, **en el tier por defecto la prueba no viaja
con la guia**. Secciones 3 y 4.

## 1. Puertas en clon limpio, por exit code

| Puerta | Comando | Exit |
|---|---|---|
| Estado colaborativo | `python scripts/validate_collaboration_state.py --root .` | **1** -- `Task TASK-0395 status mismatch: index='blocked' file='ready'` |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Drift de la cadena | `python runtime/protocol_replay.py --check-drift --root .` | **0** -- `verdict=CLEAN up_to_seq=9378` |
| Prueba embarcada | `python scripts/harness/test_session_watchdog_filter.py --scratch-root <scratch>` | **0** |

El rojo estaba **tambien en el HEAD de entonces, `44249e8d`**, no solo en el ancla:

    2d6ad843: TASK_INDEX.json -> 'blocked'   fichero de la tarea -> 'ready'   validate exit 1
    44249e8d: TASK_INDEX.json -> 'blocked'   fichero de la tarea -> 'ready'   validate exit 1
    512c68d0: TASK_INDEX.json -> 'in_progress'  fichero -> 'in_progress'      validate exit 0

El indice se habia movido y el markdown no; el arreglo estaba **sin commitear** en el arbol
compartido (`-status: ready` / `+status: blocked` mas un bloque "Blocked evidence - 2026-08-15",
residuo de un exec de Codex que libero el claim). **No lo toque** (DECISION-0018: lo senalo, no lo
arreglo), y el Arquitecto lo commiteo a las 13:40:41 (`50481615`, "commiteo el fichero que dejaba el
canonico ROJO") y lo dejo consistente en 13:42:29 (`512c68d0`). Confirmado por mi en clon limpio
sobre `512c68d0`: `OK: collaboration state is valid`, **exit 0**.

Repito la nota de metodo de r1 porque volvio a pasar, identica: **mi `validate` de arranque sobre el
arbol vivo dio exit 0**. Da verde precisamente porque esa modificacion sin commitear hace que el
fichero coincida con el indice. El arbol caliente miente en la direccion peligrosa: dice verde sobre
un canonico rojo. Dos vueltas seguidas, dos tareas distintas, mismo mecanismo.

## 2. Tabla vector por vector

| Vector | Lo que pedi en r1 | Veredicto | Evidencia |
|---|---|---|---|
| **B1** (bloqueante r1) | Contrato de nombre declarado y coherente + detector que falla RUIDOSO | **PASA** | Experimentos P/N, seccion 3.1. Plantilla, glob de ejemplo y parser dicen los tres `-to-`; el delimitador queda prohibido dentro de fecha/emisor/destinatario; toda carga que casa el glob y no parsea emite alerta con el nombre crudo. |
| **D1** (deberia viajar) | La prueba exige que la guia no prescriba descarte por identidad. Gate: guia pre-fix + linea de contrato -> exit != 0 | **PASA en su letra; SLIPS en su proposito** | Gate literal medido: **exit 1** (`guide still prescribes an identity-based self-filter: <SELF_COMMIT_FILTER>`). Pero el negativo es un token literal: experimento **M3**, seccion 3.3. |
| **D2** (deberia viajar) | Componer el hueco en una frase + mensaje-por-entrega + alinear "exact trailer" | **PASA en su letra; SLIPS parcial en el trailer** | Las dos frases estan en la guia y en el README. El filtro arreglo 2 de las 4 fugas de E2; **quedan 2** en la coordenada real: experimentos C2/C3, seccion 3.2. |
| **P0** (bloqueante de protocolo r1) | Verdear el canonico antes de cualquier commit de cierre | **RESUELTO** (el de r1 y el que reaparecio) | TASK-0367 ya concordaba. TASK-0395 reaparecio con el mismo mecanismo y quedo verde en `512c68d0`, verificado exit 0. Seccion 1. |

## 3. Lo medido

### 3.1 B1 -- la familia entera, bajo el glob que la propia guia propone

No repeti tu mutante. Extraje `mailbox_additions` y `MESSAGE_RE` del entregable en el ancla y les
pase mis cargas, **con el glob de ejemplo de la guia** (`*-to-<COORDINATOR_ROLE>-*`), que es el que
usaria el adoptante, no el `MSG-*` que usa la prueba:

    glob = *-to-Coordinator-*
    P1 forma de hub (control)                   alerts=1  parsed
    P3 fecha ISO con guiones                    alerts=1  UNPARSED  <-- antes: 0
    P4 id de peon con guion (Worker-1)          alerts=1  UNPARSED  <-- antes: 0
    P5 recipient con guion (Coordinator-A)      alerts=1  parsed
    N1 prefijo no-MSG (NOTE-...)                alerts=1  UNPARSED
    N2 minusculas (msg-...)                     alerts=1  UNPARSED
    N4 doble extension (.md.bak)                alerts=1  UNPARSED
    P8 dos entregas nuevas, una malformada      alerts=2  (1 parsed + 1 unparsed)  <-- antes: 1

La rama ruidosa cubre **toda** la familia que llega al parser, y el control parseado sigue dando
**exactamente una** alerta normal. El bloqueante de r1 esta cerrado; no es un caso, es la clase.

**Limite honesto, medido y declarado.** Lo que sigue cayendo en silencio ya no es el parser sino el
**glob**, un filtro aguas arriba:

    glob = *-to-Coordinator-*
    P2 plantilla PRE-FIX (sin -to-)             alerts=0  <-- silencio
    P7 sin sufijo tras el destinatario          alerts=0  <-- silencio
    N3 delimitador en mayusculas (-TO-)         alerts=0  <-- silencio

Las mismas tres cargas, bajo `MSG-*`, dan **alerts=1 UNPARSED**. No lo llamo defecto: el glob define
"entrega dirigida a mi", y r2 hizo que plantilla y glob por fin concuerden, de modo que el adoptante
que sigue la guia nombra con `-to-` y el glob lo captura. Queda dicho porque **estrecha la clase, no
la elimina**: quien viole el contrato de nombre recien declarado sigue sin recibir aviso, y no hay
mecanismo que lo detecte.

**Y una nota sobre la prueba, no sobre la propiedad:** la asercion ruidosa embarcada se mide con
`MSG-*` y con la carga `MSG-2099-01-01-Worker-Coordinator-HANDOFF.md`, que **bajo el glob de ejemplo
de la guia no casaria y nunca llegaria al parser**. La propiedad la verifique yo en la coordenada
buena y esta; la prueba la acredita en una coordenada que el despliegue real no usa.

### 3.2 D2 -- el "exact trailer", en la coordenada donde vive el sujeto

`classify()` ahora parte el registro en 3 campos y busca `^CLAVE: MARCA$` **solo en el campo 2**. Lo
ejercite con **commits reales** y el formato real `%H\x1f%an\x1f%B`, no con cadenas sinteticas:

    C0 coordinador, bloque de trailer real          -> FILTERED   (correcto)
    C1 peon, marca MID-LINE en la prosa             -> visible    <-- ARREGLADO
    C4 peon, marca como NOMBRE DE AUTOR             -> visible    <-- ARREGLADO
    C5 peon, commit limpio                          -> visible    (correcto)
    C2 peon, el ASUNTO es la linea del trailer      -> FILTERED   <-- SIGUE OCULTO
    C3 peon, el cuerpo CITA el trailer a principio de linea -> FILTERED   <-- SIGUE OCULTO

Dos de las cuatro fugas de E2 estan cerradas. Las otras dos siguen, y la razon es de coordenada: en
`%H\x1f%an\x1f%B` el **asunto es la primera linea del campo 2**, dentro de lo que el regex escanea.

Aqui esta el detalle que importa. La prueba **afirma** cubrir el caso del asunto:

    f"subject Protocol-Monitor-Origin: {MARKER}\x1fShared Actor\x1fclean body"

pero pone la marca en el **campo 0**, que en el formato real es el **hash**. Un asunto nunca vive
ahi. La asercion pasa, y en la coordenada real el caso **falla**. Es un verde que certifica una
propiedad que la implementacion no tiene: la misma familia que TASK-0392 vino a cerrar, un piso mas
abajo.

**No lo llamo bloqueante**, y digo por que: el filtro de commits esta declarado orientativo, el paso
7 garantiza que una alerta de mailbox **nunca** la cancela este filtro, y la guia ya exige
mensaje-por-entrega. Un commit de peon oculto pierde contexto secundario, no la entrega. Pero la
asercion hay que corregirla o retirarla: como esta, es falso-seguro.

### 3.3 Tu pregunta, medida: cuanto de la guia es portante

Mute la **guia** dejando prueba y arnes intactos, y mire el exit. Rojo = la linea es portante; verde
= la prueba no lee esa parte del entregable.

    M0 intacto                                                         exit 0
    M1 revertir la PLANTILLA a la forma pre-fix (sin -to-)
       y borrar la frase del delimitador                               exit 0   <-- SOBREVIVE
    M2 borrar "Every delivery ... must open one mailbox message"       exit 0   <-- SOBREVIVE
    M3 reescribir el paso 6 para filtrar por AUTOR/co-autor de git,
       sin usar el literal <SELF_COMMIT_FILTER>                        exit 0   <-- SOBREVIVE
    M4 borrar la instruccion de alertar con el nombre crudo            exit 0   <-- SOBREVIVE (tu medicion)
    M5 quitar la clave WATCHDOG_COMMIT_TRAILER                         exit 1   (portante)

**Respuesta directa: la prueba lee el entregable para exactamente dos cosas** -- que la clave del
trailer aparezca una sola vez, y que el literal `<SELF_COMMIT_FILTER>` no aparezca. Todo lo demas --
el contrato de nombre, el fallo ruidoso, mensaje-por-entrega, el "exact trailer" del paso 6 -- se
afirma en el arnes. Tu mutante B no era un caso aislado: es la regla, y **el enlace es de dos
tokens**.

**M3 es el que me preocupa mas, y no es el tuyo.** Reescribi el paso 6 para que prescriba
exactamente el defecto que TASK-0392 vino a cerrar -- descartar commits por identidad de git -- y la
prueba sale **verde**. El negativo de D1 caza el placeholder literal del texto viejo, no la clase.
**Esto es culpa de mi especificacion, y lo digo con todas las letras**: mi D1 nombro la clase en la
prosa pero puso el gate sobre la instancia ("la guia pre-fix con la linea de contrato tiene que dar
exit != 0"). Codex construyo contra el gate, y el gate se cumple. El hecho queda en pie: la guia
ordena ejecutar esta prueba "before trusting silence", y la prueba no puede detectar que la guia haya
vuelto a ordenar el filtro por identidad.

## 4. Lo que encontre buscando la respuesta a tu pregunta: la prueba no viaja

Tu pregunta presupone que la guia viaja y el arnes se queda. Lo medi generando instancias reales con
`scripts/new_instance.py` en los tres tiers:

| tier | `skills/session-watchdogs.skill.md` | `scripts/harness/test_session_watchdog_filter.py` |
|---|---|---|
| `coordination` (**por defecto**) | PRESENTE | **AUSENTE** |
| `runtime` | PRESENTE | presente en `scripts/harness/` |
| `attested` | bajo `Aegis/` | presente en `Aegis/scripts/harness/` |

En el tier por defecto, el adoptante recibe una guia que le ordena:

    Before trusting silence, execute the shipped discrimination proof:
    python scripts/harness/test_session_watchdog_filter.py --scratch-root ...

y ese fichero **no existe en la instancia generada**. Medido:

    python <inst>/scripts/harness/test_session_watchdog_filter.py --scratch-root <s>
    -> exit 2 : can't open file ... [Errno 2] No such file or directory

`COPIED_DIRS` incluye `skills`; el arnes solo lo copia `copy_runtime_tier_files`, que no corre en
coordination. **La guia y su prueba se separan en el reparto.**

Y esto responde tu pregunta de forma mas dura que mi seccion 3.3: para el adoptante por defecto, el
fallo ruidoso no solo no esta atado al entregable -- es que **la prueba entera es el arnes que se
queda aqui**, y la unica instruccion que el AC3 le da al adoptante para no fiarse del silencio le
llega como una ruta rota.

**Para NOVA en concreto, no aplica**: su disposicion (`.../Aegis/scripts/...`) es la del tier
attested, donde la prueba si viaja. Por eso no lo convierto en bloqueante de esta tarea. Pero es un
defecto real del paquete exportable y `new_instance.py` **no esta en `scope_routes`** de TASK-0392,
asi que no es de Codex arreglarlo en esta vuelta.

## 5. Por que cierro en vez de pedir una tercera vuelta

Lo digo explicito para que no se lea como sello de goma.

El defecto que TASK-0392 vino a cerrar era: *"un vigia armado siguiendo la documentacion no avisa de
ninguna entrega, y su silencio se lee como que los peones trabajan"*. Sobre `2d6ad843` **ese defecto
no se reproduce**: el texto entregado es coherente consigo mismo -- plantilla, glob y parser dicen lo
mismo --, el detector entregado grita ante todo lo que casa el glob y no parsea, el filtro de commits
ya no descarta por identidad, y la guia declara que su silencio no es evidencia y exige
mensaje-por-entrega. Los cuatro puntos de mi lazo de r1 estan atendidos en su letra, y B1 -- el
unico bloqueante -- lo esta tambien en su proposito, verificado con mis cargas y no con las suyas.

Lo que queda es de otra naturaleza: **la prueba es un instrumento mas debil de lo que la guia
anuncia**. Ninguno de esos hallazgos hace falso el artefacto entregado hoy; hacen falso el grado de
confianza que un lector le concede al verde. Ninguno esta en la letra de AC1-AC4, y uno de ellos (el
reparto) esta fuera de `scope_routes`. Gastar la iteracion 3 -- que por tu declaracion escala al
operador -- en defectos que mi propia especificacion de r1 no nombro seria cobrarle a Codex mi
imprecision.

Van como tareas nuevas, no como remediacion.

## 6. Residuos declarados y seguimiento propuesto

Bloqueante de cierre: **ninguno**. El que detecte (`P0'`: `validate` exit 1 por
`TASK-0395 index='blocked' file='ready'` en el ancla y en `44249e8d`) lo verdeo el Arquitecto durante
esta misma revision con `50481615` + `512c68d0`; re-verificado en clon limpio, exit 0. Nada me impide
recomendar el flip.

Tareas nuevas propuestas (no remediacion de 0392):

- **N-A (la de mas peso).** El enlace guia<->prueba es de dos tokens: la prueba no detecta que la
  guia vuelva a prescribir filtrado por identidad si no usa el literal `<SELF_COMMIT_FILTER>` (M3).
  Pedir un negativo por **clase** -- que la guia no ordene descartar por autor, committer, proveedor,
  modelo o co-autor -- con gate de mutacion sobre una reescritura, no sobre el texto viejo.
- **N-B.** El reparto separa la guia de su prueba en el tier `coordination`: o el arnes viaja, o la
  guia deja de citar una ruta que en esa instancia no existe. Ruta afectada: `scripts/new_instance.py`
  (fuera del scope de 0392).
- **N-C.** La asercion de falsos positivos mide el asunto en el campo 0 (posicion del hash). En la
  coordenada real (primera linea del campo 2) los casos C2 y C3 siguen filtrados. Corregir la
  asercion o retirarla; el comportamiento es residuo aceptable, el verde que lo certifica no.

Residuos ya declarados en r1 que siguen vigentes y no bloquean:

- `len(old_own) == 4` es cierto por construccion de `commit()`; documenta el escenario de NOVA, no lo
  mide de forma independiente.
- El delta de mailbox usa `previous` cableado, no una primera lectura real del directorio.
- `load_trailer_key` exige exactamente una aparicion del contrato: cualquier segundo ejemplo futuro
  rompe la prueba. Falla cerrado, asi que solo es fragilidad.
- Un cuerpo con CRLF hace fallar `^...$` y **no** filtraria un commit propio: ruido, no ocultacion.
- Fuera de mi alcance y no juzgado: TASK-0386, TASK-0395 (avisado, no tocado), el monitor de la
  sesion interactiva del Arquitecto, y cualquier cosa de producto (`npm test` no gateado por
  instruccion explicita).

## 7. Lazo de correccion

**Iteracion 2 de 2, y la cierro.** No pido tercera, y no queda nada pendiente de re-juzgar: el
entregable esta medido sobre `2d6ad843` y la puerta de protocolo esta verde sobre `512c68d0`, que no
toca ninguna ruta del entregable (`skills/`, `scripts/harness/`). **Puedes flipear a done.** Si antes
del flip aparecieran cambios en esas dos rutas, entonces si quiero verlos.

## 8. Nota para el Arquitecto

Tu mutante era correcto y tu instinto tambien: no lo despachaste como cosmetico y tenias razon en no
hacerlo. Solo era mas pequeno que el hueco. Medido en los dos ejes -- que lineas de la guia son
portantes, y que ficheros llegan realmente al adoptante -- el resultado es que la prueba acredita dos
tokens del entregable, y que en el tier por defecto ni siquiera llega junto a el.

Aun asi cierro, y quiero que quede claro el balance: **el defecto de campo de NOVA esta arreglado en
lo que NOVA recibe**. El texto exportable es hoy coherente y honesto, el detector es ruidoso, el
filtro ya no discrimina por identidad y el hueco del commit-only esta compuesto en una frase con su
contramedida. Lo que he medido no es que el arreglo sea falso: es que **el certificado vale menos de
lo que dice valer**, y eso merece tarea propia y no otra vuelta de esta.

Una ultima cosa, porque es la segunda vez seguida: mi `validate` en caliente dio verde sobre un
canonico rojo, otra vez, por un fichero de tarea sin commitear. El clon limpio no es una formalidad
del procedimiento; es lo unico que me separo del error las dos veces. Que tu lo verdearas a los tres
minutos no cambia el diagnostico: el mecanismo -- el indice avanza por `submit_intent` y el markdown
se queda en el arbol -- ya ha producido dos rojos canonicos en dos vueltas seguidas, y ninguna de las
dos veces lo vio nadie hasta que alguien clono limpio.

-- Analista, 2026-08-15 14:05 local (UTC+2)
