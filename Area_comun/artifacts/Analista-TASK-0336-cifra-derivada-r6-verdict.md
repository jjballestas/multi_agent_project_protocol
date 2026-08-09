# Veredicto TASK-0336 r6 (la cifra derivada) -- OK-CLOSABLE. El denominador ya se deriva de la MISMA corrida, en las dos direcciones y con dientes: crece a 38 y baja a 36 sin que nadie edite el token, y re-congelarlo o mirar el contrato equivocado pone la suite ROJA. No hay regresion en A/B/C/E y el alcance se respeto al pie. Cierro declarando dos residuales medidos: el NUMERADOR sigue congelado, y la frontera declarada se mudo de la corrida-fixture a la corrida-canonica.

Analista, 2026-08-09 08:24 hora local (UTC+2). Alcance: **SOLO hub, sin producto en alcance**.
No corri ningun gate de Nova ni de Zeus.

**Cabecera.** Bloquee en r5 por una sola cosa y la dije con nombre propio: *"el bloqueante es el
DENOMINADOR, no el numerador"*. Ese denominador ahora sale de `len(contract.boundaries)` del propio
contrato, en la misma ejecucion que imprime `boundaries=37`, y lo he empujado en las dos direcciones
para comprobar que no es una coincidencia aritmetica. **En la direccion en que se pidio, esto cierra.**

Lo que queda no lo convierto en bloqueante porque seria mover la porteria: el numerador ya lo declare
no-bloqueante en r5 y sigue siendolo. Pero lo dejo medido, con su umbral exacto, porque la pregunta
que me hiciste tiene una respuesta de dos mitades y solo una de ellas es "si".

---

## 1. Anclaje

- Commit juzgado: **`2ed31e87`** (`fix(TASK-0336): derive certification boundary count`).
- HEAD del protocolo al emitir: **`dde65715`**. `2ed31e87` es ancestro de `origin/main`
  (`git merge-base --is-ancestor` -> 0).
- Ancla anterior (r5): `90477ff7`. `git diff --stat 90477ff7 2ed31e87` sobre los dos ficheros de
  alcance -> **2 lineas en `check_falsification_contracts.py`, 3 en `test_falsification_contracts.py`**.
- Clon limpio: `D:/Aegis_Scratch/protocol/analista-0336r6/cc`, detached en `2ed31e87`,
  `git status --short` vacio. Todos los gates corridos AHI, nunca en el arbol caliente.
- Banco de mutacion en clon SEPARADO `D:/Aegis_Scratch/protocol/analista-0336r6/mut`, escrituras y
  restauraciones en BYTES; `git status --porcelain` verificado vacio tras cada mutante.
- Sondas fuera del arbol atestado: `bench_derive.py`, `probe_b.py`, `probe_c.py` en
  `D:/Aegis_Scratch/protocol/analista-0336r6/`.

## 2. Reproduccion -- gates declarados, en el clon limpio (exit codes reales)

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      exit 0
        -> FALSIFICATION_STATIC_WIRING runners=12/12 contracts=68/68
           residuals=...,contract_discrimination_23_of_37,twin_TASK_0338
        -> FALSIFICATION_INVENTORY permanent_negatives=68 declared=68 missing=0
        -> DECLARED NEG-FALSIFICATION-RUNNER-WIRING boundaries=37
    python scripts/test_falsification_contracts.py                 exit 0
    python scripts/validate_collaboration_state.py --root .        exit 0
    python scripts/scan_domain_neutrality.py --root .              exit 0
    python scripts/scan_encoding.py --root .                       exit 0
    python runtime/protocol_replay.py --check-drift --root .       exit 0
                                                 -> PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=8286

La contradiccion de r5 esta cerrada por lectura directa: la misma linea que dice `_of_37` convive con
`boundaries=37` en la misma salida. Pero eso solo prueba que hoy coinciden. Lo que decide es si
coinciden **por construccion**, y eso se mide moviendo el numero.

## 3. Foco A -- la cifra se deriva de la MISMA corrida

Banco `bench_derive.py`. Cada mutante toca **solo** la lista de fronteras o el literal del checker,
se ejecuta el checker y la suite completa, y se restaura en bytes.

    mutante                              checker  token           inventory  suite   lectura
    M0 linea base (lo entregado)          exit 0   23_of_37        37         exit 0  referencia
    M1 +1 frontera (duplico una real)     exit 0   23_of_38        38         exit 0  DERIVA hacia arriba
    M2 -1 frontera                        exit 0   23_of_36        36         exit 0  DERIVA hacia abajo
    M3 -20 fronteras                      exit 0   23_of_17        17         exit 0  ver residual R1
    M4 re-congelo el denominador a 31     exit 0   23_of_31        37         exit 1  TIENE DIENTES
    M5 id de contrato inexistente         exit 0   23_of_0         37         exit 1  TIENE DIENTES
    M7 anado un TERCER contrato           exit 1   23_of_37        --         exit 1  fail-loud, no escape

**Lectura.** El denominador **no es un literal disfrazado**: M1 y M2 lo mueven en las dos direcciones
sin que nadie toque el token, y en cada corrida el `boundaries=N` del inventario y el `_of_N` del
residual salen del mismo `len(contract.boundaries)`, asi que **ya no pueden discrepar**. Esa es
exactamente la propiedad que pedi.

Y **no es una tautologia sin dientes**: la frontera declarada compara la cifra del checker (busqueda
por `id`) contra la del contrato (`FALSIFICATION_CONTRACTS[-1]['boundaries']`), que son dos caminos
independientes al mismo hecho. M4 (volver a clavar 31) y M5 (mirar un contrato que no existe) ponen
la suite en **exit 1**. Un aserto que no se puede romper no vale nada; este se rompe por las dos vias
por las que puede degradarse.

**M7 -- la fragilidad posicional, medida y descartada.** El checker busca por `id` y el contrato por
posicion `[-1]`. Si alguien anade un tercer contrato, esos dos dejan de apuntar al mismo sitio. Lo
probe: **no hay verde silencioso** -- checker `exit 1` (`NEG-UNRELATED-THIRD: declared contract has no
permanent-negative marker`) y suite `exit 1`. La divergencia posicional es fail-loud.

## 4. Foco B -- sin regresion en lo ya cerrado

### B1 -- el decimo escape sigue muerto, y sigue muerto por PROPIEDAD

`probe_b.py`. No repeti mi lista de r5: derive otra vez la clase entera y **le anadi 13 caracteres
que no nombre ni en r4 ni en r5** (BEL 0x07, SUB 0x1A, ESC 0x1B, SOFT HYPHEN, MONGOLIAN VOWEL SEP,
EM QUAD, EM SPACE, FIGURE SPACE, ZWSP, NARROW NBSP, MEDIUM MATHEMATICAL SPACE, INVISIBLE SEPARATOR
U+2061, INTERLINEAR ANNOTATION TERMINATOR U+FFF9).

    clase Python derivada (sys.maxunicode)         9 separadores
    caracteres NUNCA nombrados, anadidos          13
    coordenadas                                    5  (echo-SEP-runner, runner-SEP-echo,
                                                       comentario-SEP-runner, SEP inicial, SEP final)
    fuentes de bash efectivo                       4  (shell:bash, ubuntu implicito,
                                                       defaults de job, defaults de workflow)
    celdas                                       440
    celdas ACEPTADAS por el gate                   0

    control invocacion directa      exit 0   (aceptada, correcto)
    control invocacion con echo     exit 1   (rechazada, correcto)

Cero aceptadas: ninguna celda puede ser verde-silencioso, porque una celda rechazada nunca deja pasar
un runner que no corre. La derivacion sigue en el contrato (`for codepoint in range(sys.maxunicode + 1)`)
y `command.split("\n")` sigue en produccion: el gate sigue preguntando "donde acaba un comando para
bash", no "que caracteres parte Python".

### B2 -- `effective_shell_kind` sigue fallando cerrado

    bloque multilinea con shell: fish (familia desconocida)   gate exit 1   fail closed, correcto
    bloque multilinea equivalente con shell: bash             gate exit 0   aceptado, correcto

La funcion es **byte-identica** a la de r5 (comparacion AST, seccion 5).

### B3 -- la frontera del AC5 sigue muriendo por mutacion

Mutando **produccion** (no el runner), en el clon de mutacion:

    linea base                                                        suite exit 0
    etiqueta afirmativa: STATIC_WIRING -> EXECUTION guaranteed=yes    suite exit 1
    scope ensanchado -> scope=full_execution_guarantee                suite exit 1

Las dos caras del certificador siguen con dientes. (Los cuatro supervivientes que declare en r5
-- decir lo mismo con otras palabras -- siguen vivos y siguen siendo deuda declarada, no bloqueante:
"la salida no afirma ejecucion garantizada" no es mecanicamente decidible.)

## 5. Foco C -- alcance respetado, al pie

Comparacion **por AST** entre `90477ff7` y `2ed31e87` (no por diff de texto: comparo el segmento
fuente de cada funcion top-level):

    scripts/check_falsification_contracts.py   funciones que CAMBIAN = ['main']
        effective_shell_kind        identica
        step_gates_runner           identica
    scripts/test_falsification_contracts.py    funciones que CAMBIAN = ['main']
        bounded_static_certification identica
        run / run_with_checker       identicas

    command.split("\n")                        presente (linea 169)
    derivacion de la clase por sys.maxunicode  presente (contrato, linea 302)

`2ed31e87` **no toca** `.github/workflows/validate.yml`: sus ficheros son `CLAIMS.json`,
`CLAIMS.slim.json`, `events.jsonl`, `snapshot.json` y los dos de alcance. El workflow SI cambio entre
las dos anclas, pero por otras tareas (0340/0345/0346), no por esta; y el gate entregado corre verde
contra el workflow de la punta (`runners=12/12 contracts=68/68`, exit 0).

## 6. Vector por vector

    vector                                                        veredicto
    A  denominador derivado de la misma corrida (M1/M2)           PASS
    A  el token no puede discrepar de boundaries=N                PASS  (mismo len, por construccion)
    A  la frontera tiene dientes (M4 re-congelar, M5 id falso)    PASS
    A  divergencia posicional [-1] vs id (M7)                     PASS  (fail-loud)
    B  decimo escape, clase derivada + 13 caracteres nuevos       PASS  (0/440 aceptadas)
    B  effective_shell_kind falla cerrado                         PASS
    B  frontera del AC5 muere por mutacion                        PASS  (2/2 mutantes)
    C  split("\n"), derivacion, shell efectivo, certificador      PASS  (byte-identicos)
    C  workflow no tocado por este commit                         PASS
    -- numerador 23 congelado                                     RESIDUAL R1 (declarado, no bloqueo)
    -- frontera mudada de wired.stdout a clean.stdout             RESIDUAL R2 (declarado, no bloqueo)

## 7. Residuales declarados

**R1 -- el numerador no deriva, y por eso el cociente puede volverse imposible.** El token es
`contract_discrimination_23_of_{derivado}`: el `23` sigue siendo un literal, medido cuando el contrato
tenia 31 fronteras y nunca recontado sobre 37. Consecuencias medidas:

- **M3**: con 20 fronteras retiradas el programa imprime `contract_discrimination_23_of_17` --
  numerador mayor que denominador, aritmeticamente imposible -- con **checker exit 0 y suite exit 0**.
  Umbral exacto: **a partir de 15 fronteras retiradas** el cociente deja de ser posible.
- **E1**: sobre un repo que no declara `NEG-FALSIFICATION-RUNNER-WIRING`, el `next(..., ())` da 0 y la
  linea imprime `contract_discrimination_23_of_0` con **exit 0**; y `bounded_static_certification`
  devuelve **True** sobre esa salida, es decir el predicado de honestidad acepta un cociente imposible.
  Reproducido sobre el fixture que la propia suite construye.

Alcance real de R1: **no afecta a la corrida canonica del hub** (23 <= 37 hoy) ni a la forma que
`new_instance.py` cablea en el CI de las instancias -- verificado: sin `--workflow` la linea
`FALSIFICATION_STATIC_WIRING` **no se imprime** (`grep -c` = 0), y la instancia se genera con
`check_falsification_contracts.py --root .` a secas. Por eso es residual y no bloqueante.

Lo declaro porque es literalmente la clase que bloquee en r5 -- una linea que se desmiente en su
propia ejecucion -- reducida a un rincon mas estrecho, no eliminada. **Direccion sugerida (no la
impongo): que el numerador se derive de una medida real, o que desaparezca y el residual diga solo
`contract_discrimination_of_37`.** Una cifra que nadie puede recomputar no es una declaracion
falsable; es prosa con numeros.

**R2 -- la frontera declarada se mudo de corrida.** En r5 el aserto miraba `wired.stdout` (la corrida
FIXTURE, controlada); ahora mira `clean.stdout` (la corrida canonica). El motivo es exactamente R1: en
el fixture el token vale `23_of_0` y el aserto derivado no casaria. Es decir, **la frontera se aparto
del unico caso donde la derivacion degenera**. No lo bloqueo -- la frontera conserva dientes (M4/M5) y
el fixture sigue cubierto por `bounded_static_certification(wired.stdout)` -- pero conviene saber que
la region que la frontera vigila se estrecho al mudarse.

**R3 -- heredados de r5, sin cambio:** `safe_forms_outside_whitelist`,
`line_continuation_mechanism_redundancy` (quitar el guardia W06/W07 sigue sin voltear ninguna
frontera), divergencia de PALABRA `\s` vs bash (fail-loud, nunca verde silencioso), y los 4
supervivientes del banco AC5 que dicen lo mismo con otras palabras.

## 8. La pregunta que hiciste

> Si manana cambia el numero de fronteras, el token cambia solo, o vuelve a hacer falta que alguien lo edite?

**El denominador cambia solo. El numerador no, y nunca lo hara.** Medido en las dos direcciones:
anade una frontera y sale `_of_38`, quita una y sale `_of_36`, sin que nadie edite nada y sin que la
suite proteste. Ese era el bloqueante y esta cerrado.

Pero el `23` es un recuento **sobre esas mismas fronteras**, y sigue clavado en el valor que se midio
cuando eran 31. Asi que la respuesta honesta es: manana el token seguira siendo coherente consigo
mismo en la forma (`X_of_N` con N vivo) y **stale en el fondo** (X medido contra otro N). Y si algun
dia se retiran 15 fronteras, el token dira `23_of_22` con todos los gates en verde. Hoy no es el caso
y por eso cierro; lo dejo escrito para que la proxima vez que alguien mire ese numero sepa que la
mitad de el no se ha vuelto a medir desde r4.

## 9. Recomendacion de cierre

**OK-CLOSABLE.** El bloqueante de r5 esta cerrado por propiedad, verificado por comportamiento en las
dos direcciones y con dientes demostrados; A, B y C pasan; el alcance se respeto al pie; los gates
declarados salen exit 0 en clon limpio sobre el commit exacto y el drift es CLEAN.

El cierre (flip a `done` y liberacion de claim) es del orquestador, no mio. Los residuales R1 y R2
quedan declarados aqui; si el Arquitecto quiere el numerador derivado o retirado, eso es tarea nueva
-- no reapertura de esta.

-- Analista
