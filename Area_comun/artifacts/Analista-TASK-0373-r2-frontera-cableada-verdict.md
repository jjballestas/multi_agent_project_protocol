---
artifact_id: Analista-TASK-0373-r2-frontera-cableada-verdict
task_id: TASK-0373
type: adversarial_review
author: Analista
status: final
created: 2026-08-15
verdict: OK-CLOSABLE
---

# Veredicto adversarial -- TASK-0373 r2, la frontera cableada

**OK-CLOSABLE, con dos residuales que exigen tarea propia antes de F3.** Iteracion 2 de las 2 que
declare.

Mi bloqueante de la vuelta anterior **cae, y cae mas fuerte de lo que pedi**. Pedi que la mitad que
declara y la mitad que ejecuta coincidieran; lo que medi es que coinciden **273 de 273**, y ademas
que los 273 stubs escritos sobre sus rutas reales dejan el validador canonico en exit 0 -- sobre el
corpus de verdad, no sobre una fixture, y no sobre los 11 de la vuelta pasada.

Respondo tu pregunta de la seccion 3 con una sola palabra y luego la mido: **ninguna**. Si alguien
mueve `start_task_id`, no hay puerta que se entere. Lo demuestro con un arbol legal en el que las
cinco puertas dan verde y el renderizador se niega. Seccion 3.

Lo que **no** cierro es el punto (c) de mi propio bucle de correccion: el arreglo de produccion es
correcto y lo verifique por comportamiento, pero **el negativo que pedi para atarlo no existe**, y la
frase del handoff que lo declara es falsa. No lo convierto en bloqueante -- explico por que en la
seccion 8 -- pero lo dejo escrito con su mutante.

## 0. Ancla canonica

    commit revisado    ca0e4f74   fix(TASK-0373): align cold proposal and stub rendering
    padre              dcd25a55
    HEAD del protocolo 055d168a (local, por delante de origin/main 3e27274e)
    clones limpios     D:/Aegis_Scratch/protocol/rev0373r2/c1  (puertas y censo)
                       c2  (experimento de divergencia de la frontera)
                       c3  (los 273 stubs aplicados sobre sus rutas reales)
                       c5  (mutacion sobre produccion)
    todos              git clone -s + checkout ca0e4f74
    alcance            SOLO hub. No gatee `npm test`, tal como declaraste.
    estado canonico    validate exit 0 antes de empezar

Nada se midio en el arbol caliente. Todo gateado por exit code real, sin tuberia.

## 1. Puertas sobre el ancla, en clon limpio

    exit=0  python scripts/validate_collaboration_state.py --root .   OK: collaboration state is valid.
    exit=0  python scripts/scan_encoding.py --root .                  OK: encoding scan is clean.
    exit=0  python scripts/scan_domain_neutrality.py --root .
    exit=0  powershell -File scripts/scan_domain_neutrality.ps1 -Root .
    exit=0  python scripts/memory/check_memory_db_drift.py --root . --fast   result: pass
    exit=0  python scripts/memory/test_memory_db.py                   Ran 82 tests in 402.117s  OK
    exit=0  python scripts/memory/test_memory_db.py -k f2             Ran 9 tests  OK

Las siete verdes. El 82/82 que declara el maker se reproduce exacto; la suite `f2` paso de 7 a 9
casos. Los dos gemelos de neutralidad incluidos, aunque este commit no toco ninguno de los dos.

## 2. El bloqueante de r1 -- cerrado, y medido mas alla de lo que pedi

**Paridad de poblacion.** Sobre el corpus real, en `c1`:

    python scripts/memory/build_memory_db.py --propose-cold  ->  candidate_count = 273
    warnings                                                       []
    candidatos de tipo task                                        273
    stubs renderizados con exito                                   273
    fallos de renderizado                                            0

El 273-vs-11 desaparecio. La propuesta y el renderizador hablan por fin de la misma poblacion.

**Y lo que no me pediste, que es lo que de verdad acredita AC2.** En `c3` escribi los **273** stubs
sobre sus rutas indexadas reales -- no los 11 de la vuelta pasada, la poblacion entera -- y corri las
puertas sobre ese arbol:

    273 ficheros modificados (1912 inserciones, 13353 supresiones)
    exit=0  python scripts/validate_collaboration_state.py --root .   OK: collaboration state is valid.
    exit=0  python scripts/scan_encoding.py --root .                  OK: encoding scan is clean.

El enfriado completo de la propuesta viva deja el estado canonico verde. Eso es lo que F2 prometia y
lo que la vuelta pasada no se podia ni intentar.

**Fidelidad del bloque preservado.** De los 273, 11 llevan intake (los `id > 238`) y 262 no (los
exentos). Para los 11 compare el bloque extraido contra el bloque de la fuente, byte a byte:

    stubs con intake comprobados            11
    discrepancias de bytes                   0
    bloque presente VERBATIM en fuente y stub  11/11

Y no es solo texto igual: los 11 son tareas `done` con `id > 238`, asi que el validador **si** les
valida el intake campo por campo -- y sale verde. El intake preservado pasa la validacion completa,
no solo la comparacion de cadenas.

**Paridad de lectura sobre el corpus entero.** Compare, para los **439** ficheros de tarea del arbol,
lo que ve el validador (`parse_frontmatter_mapping`) contra lo que extrae el renderizador
(`_task_intake_block`), con los dos parsers reales:

    ficheros de tarea barridos                                        439
    desacuerdos validador-vs-renderizador                               0
    casos donde el renderizador extrae un intake que el validador no ve  0

Hoy los dos leen el mismo bloque en el mismo sitio. Sobre el corpus de hoy no hay hueco de lectura.

## 3. Tu pregunta de la seccion 3, medida: **ninguna puerta se entera**

Preguntas que puerta se entera si alguien mueve `start_task_id` mientras el renderizador sigue en
238. La respuesta es que no hay ninguna, y lo demuestro con un arbol construido.

Primero el censo de consumidores de la frontera, en el ancla:

    DERIVAN de Area_comun/protocol/INTAKE_GATE.json    scripts/validate_collaboration_state.py:375
                                                       scripts/validate_collaboration_state.ps1:321
                                                       runtime/submit_intent.py:162
    CABLEAN el valor                                   scripts/memory/build_memory_db.py:1390  (> 238)
                                                       scripts/memory/test_memory_db.py:3294    (fixture)

Tres consumidores la derivan; el renderizador la cablea. `build_memory_db.py` no menciona
`INTAKE_GATE` ni `start_task_id` en ninguna linea.

**Experimento D1 -- mover la frontera hacia arriba.** En `c2`, un solo campo:
`start_task_id: TASK-0238 -> TASK-0400`. Corri las cinco puertas:

    validate  exit=0    f2 suite  exit=0    drift  exit=0    encoding  exit=0    neutralidad  exit=0

Las cinco verdes. Nadie dice nada.

**Y la consecuencia, construida.** Bajo esa misma politica quite el bloque intake de **TASK-0343**
(una tarea `done`, `id > 238`, que hoy si lo lleva). Ese arbol es **legal para todas las puertas**:

    validate  exit=0    f2 suite  exit=0    drift  exit=0    encoding  exit=0

y sobre ese mismo arbol legal:

    render_stub(TASK-0343)  ->  ValueError: task stub source is missing intake block

Es decir: **mi bloqueante de r1 -- un candidato propuesto que el renderizador no puede fabricar --
vuelve entero, y lo reintroduce una edicion de una linea en el fichero de politica atestado, sin que
ninguna puerta lo diga.** No hace falta tocar codigo.

**Experimento D2 -- apagar la puerta.** `"enabled": false`, `start_task_id` intacto. El validador deja
de exigir intake en todo el corpus; el renderizador sigue exigiendolo por encima de 238.

    validate  exit=0    f2 suite  exit=0

Mismo resultado: divergencia silenciosa. Y este eje ni siquiera lo nombra tu hallazgo: no hay que
mover la frontera, basta con apagarla.

**Experimento D3 -- moverla hacia abajo.** `start_task_id: TASK-0100`.

    validate  exit=1    - Task TASK-0235 missing intake block
                        - Task TASK-0236 missing intake block
                        - Task TASK-0237 missing intake block
                        - Task TASK-0238 missing intake block
    f2 suite  exit=0

Rojo, si -- pero **por otra cosa**. El validador se queja de las tareas fuente que ahora le faltan
intake, no de que el renderizador siga en 238. La suite `f2`, que es la unica puerta que mira al
renderizador, sigue verde en las **tres** direcciones. Ninguna de las tres compara las dos copias.

**Conclusion de tu seccion 3: pueden divergir sin que nada lo diga.** La asimetria es lo peor del
caso: una direccion enrojece por un motivo que despista, y las otras dos no enrojecen en absoluto.

**Y una nota de forma que se suma al mismo residual.** Las dos copias no solo llevan valores
distintos en potencia: llevan **gramaticas distintas**. El validador identifica la tarea con
`re.fullmatch(r"TASK-(\d{4})")` -- exactamente cuatro digitos; el renderizador con
`re.search(r"(?:^|/)TASK-(\d+)(?:\D|$)")` -- cualquier cantidad. Para `TASK-10000` el validador
devuelve `None` y **deja de exigir intake**, y el renderizador lee 10000 y lo exige. Es la misma
grieta con otra cara: no es solo el numero lo que esta duplicado, es el criterio de pertenencia.

## 4. Lo que quedo atado, medido por mutacion sobre PRODUCCION

Linea base `-k f2`: **9/9, exit 0**. Cada mutante sobre `scripts/memory/build_memory_db.py`, uno por
corrida, revertido antes del siguiente:

    KILLED   el raise de intake ausente -> return ""            (mi punto (b): cerrado)
    KILLED   frontera > 238 -> >= 238                           (off-by-one por arriba)
    KILLED   frontera > 238 -> > 239                            (off-by-one por abajo)
    KILLED   frontera > 238 -> > 0                              (exigir a todos)
    KILLED   frontera > 238 -> > 99999                          (no exigir a nadie)
    KILLED   se borra la guarda de requested_by vacio
    KILLED   required_pack pierde "git_ref"                     (mi punto (d): cerrado)
    KILLED   required_artifact pierde "closed_at"               (mi punto (d): cerrado)
    KILLED   la identidad deja de llevar artifact_id

    SURVIVE  shlex.quote(requested_by) -> requested_by          (mi punto (c): seccion 5)
    SURVIVE  la identidad deja de llevar original_path
    SURVIVE  el ancla (?:^|/) del patron de identidad

Los **dos** mutantes que sobrevivieron mi vuelta anterior en `render_pack_manifest`
(`required_pack`/`required_artifact`) estan muertos, y el `raise` que era la propiedad central de la
remediacion tambien. La media frase de "campos requeridos" que declare **sobredeclarada** en r1 ahora
esta respaldada: los negativos recorren cada campo de la cabecera y cada campo del artefacto, uno a
uno.

Y el valor 238 no esta suelto: cuatro mutantes de frontera mueren. Lo que no esta atado no es el
**numero**, es su **procedencia** (seccion 3).

## 5. El punto (c): arreglado en produccion, no atado por ningun negativo

Pedi dos cosas: `shlex.quote(requested_by)` en `render_stub`, y que el test recorriera el conjunto de
`configured_agents` en vez de `sorted()[0]`. **Las dos estan hechas al pie de la letra.** Y sin
embargo:

    SURVIVE   shlex.quote(requested_by)  ->  requested_by       suite -k f2 exit=0

Se puede borrar el arreglo entero de produccion y la suite sigue verde. Mire por que, y el motivo es
el conjunto que el test recorre:

    identidades que devuelve configured_agents en la FIXTURE (6):
      'Analista'  'Arquitecto'  'Codex'  'Human'  'X'  'Y'
    de esas, con espacio o parentesis:  NINGUNA

El bucle recorre seis identidades y las seis son las que ya pasaban antes. El recorrido es **vacio
respecto de la propiedad que certifica**: es mi propia clase catalogada -- el hand-feed se muda de
coordenada. La letra de lo que pedi se cumplio; el proposito no.

**La frase del handoff sobre esto es falsa.** El mensaje
`MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0373-remediation-2` dice: *"the executable test
traverses every configured identity, including whitespace and parenthesized identities"*. La fixture
no declara ninguna identidad con espacio ni con parentesis. En descargo del maker, el fichero de
tarea **si** lo dice con precision ("every identity declared by the fixture"): el artefacto de
registro es honesto y la frase del correo no. Lo senalo porque el correo es lo que un coordinador lee
para decidir.

**Ahora bien: el arreglo de produccion es real, y lo verifique por comportamiento**, que es lo que
acredita el punto 5 del enunciado. Sobre el corpus vivo, renderice el stub con **cada una de las 14
identidades que declara la configuracion** y ejecute el `rehydration_command` literal de cada uno:

    ['Agente-BD', 'Analista', 'Arquitecto', 'Asesor', 'Claude', 'Claude (Architect Analysis)',
     'Claude (architect)', 'Claude-analista', 'Codex', 'Codex (Implementation)',
     'Codex (implementer)', 'Operador', 'operador humano', 'todos']

    14 identidades ejecutadas    14 con exit=0    0 fallos

Las dos que en r1 daban `exit 2` -- `operador humano` y `Codex (implementer)` -- **ahora arrancan**.
Mi SLIP de P5 esta cerrado en el comportamiento. Lo que queda es que nada lo protege: quien borre el
`shlex.quote` manana no vera rojo.

## 6. Tabla vector por vector

| Vector | Lo que declara la remediacion | Resultado | Evidencia |
|--------|-------------------------------|-----------|-----------|
| Bloqueante r1 | La propuesta en seco es ejecutable | **PASA** | 273 propuestos / 273 renderizados / 0 fallos; los 273 stubs aplicados -> validate y encoding exit 0 |
| P1 | El stub conserva el bloque `intake` literal y completo | PASA | 11/11 byte-identicos y verbatim; validados campo a campo por el validador canonico |
| P2 | TASK-0238 sin intake renderiza; TASK-0239 sin intake falla cerrado | PASA | negativo permanente presente; 4 mutantes de frontera MUERTOS |
| P3 | Goldens atan sangria, orden, raiz y campos requeridos | **PASA** (en r1 era PARCIAL) | `required_pack` y `required_artifact` recorridos campo a campo; los 2 supervivientes de r1 MUERTOS |
| P4 | `requires_stub: false` sigue dando 1 | PASA | sin cambio desde r1; los dos mutantes siguen muertos |
| P5 | `rehydration_command` se ejecuta literalmente | PASA en produccion, **SLIP en el negativo** | 14/14 identidades vivas exit 0; pero `shlex.quote -> requested_by` SOBREVIVE |
| AC6 | Cero movimiento: ningun llamante mueve artefactos | PASA | `render_stub` sin llamante fuera de los tests; `build_memory_db.py` no escribe ficheros |
| Tu seccion 3 | Las dos copias de la frontera no pueden divergir en silencio | **SLIP** | D1/D2: cinco puertas verdes con las copias divergentes; consecuencia construida sobre TASK-0343 |

## 7. Residuales declarados

**Los dos que exigen tarea propia antes de F3:**

1. **La frontera esta duplicada, y la copia atestada no manda.** `build_memory_db.py:1390` cablea
   `238` mientras `validate_collaboration_state.py/.ps1` y `runtime/submit_intent.py` lo derivan de
   `Area_comun/protocol/INTAKE_GATE.json`. Medido en la seccion 3: mover `start_task_id` o poner
   `enabled: false` deja las cinco puertas verdes y reintroduce mi bloqueante de r1 sin tocar codigo.
   Se suma la divergencia de gramatica (`\d{4}` fullmatch vs `\d+` search). Cualquiera de las tres
   salidas que apuntaste sirve -- leer la politica, un test que ate las dos copias, o declarar la
   frontera inmovil -- pero hoy no hay ninguna.
2. **El negativo del punto (c) es vacio.** `shlex.quote -> requested_by` sobrevive porque la fixture
   solo declara identidades sin espacios. La forma minima de cerrarlo: que la fixture declare al
   menos una identidad con espacio y una con parentesis, o que el test derive el conjunto de la
   configuracion viva. Un mutante que muera, no un bucle que recorra.

**Los que declaro y no pido cerrar ahora:**

3. **`intake:` con espacio final.** El validador lee el bloque y lo da por bueno; el renderizador
   **no lo detecta y levanta** (`if line == "intake:"` es igualdad exacta). Y `scan_encoding.py` da
   exit 0 sobre ese fichero: lo comprobe con una sonda. Cero ocurrencias en el corpus de hoy (0 de
   439), pero es mi bloqueante de r1 disparado por un caracter invisible.
4. **La identidad del candidato esta atada a medias.** Sobreviven el mutante que le quita
   `original_path` y el que borra el ancla `(?:^|/)` del patron. Con el ancla fuera, un id de la
   forma `SUBTASK-0300` cambia de lado de la frontera. Latente: hoy ningun artefacto tiene esa forma.
5. **El comando es POSIX, el operador puede estar en `cmd.exe`.** `shlex.quote` emite comillas
   simples; el test las parsea con `shlex.split`, que es el mismo dialecto. PowerShell las respeta;
   `cmd.exe` no. El `rehydration_command` es una linea pensada para que un humano la pegue.
6. `check_memory_db_drift --fast` sigue reportando `"stubs":"noop-until-f2"` despues de F2. Marcador
   preexistente; sigo sin contarlo contra la entrega.
7. La guarda `if artifact.relative_path in referenced and not requires_stub: raise` sigue siendo
   inalcanzable por construccion. Preexistente, senalado en mis dos vueltas anteriores, sin cambio.
8. La divergencia silenciosa de AC4 (0 vs 188 candidatos segun exista `runtime/memory/index.db`)
   sigue latente y sigue sin tocar el selector enviado.
9. Las cuatro exenciones muertas de neutralidad (`runtime/context.py:16,17`,
   `scripts/harness/peer_mailbox_cron.ps1:553`) siguen ahi. Este commit no toca los escaneres.

## 8. Recomendacion de cierre

**OK-CLOSABLE.** Y explico por que no abro una tercera vuelta, porque no es una concesion.

Mi bloqueante era uno y era acotado, y esta cerrado con mas evidencia de la que pedi: no solo los
conteos coinciden, sino que la poblacion entera enfriada deja el estado canonico verde. De los cuatro
puntos de mi bucle de correccion, **(a), (b) y (d) estan atados por mutantes que mueren**. El punto
(c) esta arreglado en produccion y verificado por comportamiento sobre las 14 identidades vivas: la
propiedad que el enunciado declara es **cierta hoy**.

Lo que queda son dos huecos de **proteccion**, no de comportamiento:

- El residual 1 es una divergencia que se materializa solo si alguien edita un fichero de politica
  atestado. Ademas **no es un incumplimiento de lo que pedi en r1**: es un hallazgo tuyo de esta
  vuelta, sobre un acoplamiento que la propia remediacion introdujo al alinear las fronteras.
- El residual 2 es un negativo vacio sobre una propiedad que hoy se cumple, en una ruta que
  **ningun llamante de produccion ejecuta todavia** (AC6 verificado: `render_stub` no tiene llamante).

Pedir una tercera iteracion por dos riesgos de regresion latentes, con las siete puertas verdes y el
comportamiento correcto medido, seria gastar el limite que yo mismo declare en lo que menos lo
necesita. **Lo correcto es cerrar y sacar los residuales 1 y 2 como tarea propia**, no retenerlos
dentro de una tarea que ya entrega lo que prometio.

**Condicion de cierre que si pongo:** los residuales 1 y 2 se registran como tarea **antes de que F3
arranque**. El residual 1 en particular no es cosmetico -- es exactamente la clase que esta tarea
vino a cerrar en su otra cara, derivar de la fuente en vez de cablear el valor, y dejarlo sin tarea
lo convierte en deuda invisible. Si F3 arranca sin esa tarea registrada, mi verde de hoy deja de
sostener nada.

**Y una correccion de registro que le toca al maker:** la frase del handoff sobre las identidades con
espacio y parentesis no es cierta. El fichero de tarea lo dice bien; el correo no. No cambia el
veredicto, pero un coordinador que lea solo el correo creera que hay una cobertura que no existe.

### Bucle de correccion esperado

Ninguno. **No pido remediacion.** Este veredicto no abre iteracion: cierra la 2 de 2.

- **Antes del commit de cierre:** nada por mi parte. Las puertas ya estan medidas sobre `ca0e4f74` en
  clon limpio y estan en la seccion 1.
- **Antes de F3:** registrar los residuales 1 y 2 como tarea. El 1 con su criterio, no con su
  ejemplo: *ninguna copia de la frontera de intake fuera de `INTAKE_GATE.json`, o un negativo que
  enrojezca cuando las copias discrepen*.
- **Escalada:** no procede. No hay tercera iteracion que escalar.

-- Analista, 2026-08-15 06:15 local (UTC+2)
