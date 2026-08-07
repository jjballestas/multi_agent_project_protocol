# Veredicto Analista -- TASK-0330 re-juicio iteracion 2 (el gate certifica ejecucion que no verifica)

    Revisor            Analista (voz adversarial independiente)
    Tarea              TASK-0330 -- la cobertura declarada no es cobertura verificada
    Commit juzgado     f6d88cb7 fix(TASK-0330): gate actual runner execution
    Handoff juzgado    744d4a1d (origin/main) -- HANDOFF-TASK-0330-codex-to-arquitecto.md,
                       reescrito por f1e302cc; el AC5 se juzga sobre esa version, no sobre
                       la que f6d88cb7 dejo a medias.
    Anclaje protocolo  f6d88cb7 es ancestro de origin/main (744d4a1d). Ningun commit posterior
                       toca .github/workflows/validate.yml, scripts/check_falsification_contracts.py,
                       scripts/test_falsification_contracts.py ni examples/.
    Clon limpio        D:/Aegis_Scratch/mapp/analista-0330-r2/cc (clon --local, checkout f6d88cb7)
    CI real            run 31204963761 (head f6d88cb7)
    Alcance            SOLO el hub. Sin producto en alcance, ningun npm test.
    Fecha              2026-08-07 20:20 hora local (UTC+2) == 18:20Z

    VEREDICTO          CHANGE-REQUIRED  (iteracion 2 de 2 -- escalo al operador humano)

## Resumen en una linea

Los dos puntos bloqueantes que puse estan resueltos y probados en el CI real; el tercero no solo
sigue abierto sino que es mas ancho de lo que mediste: de 14 mutantes del workflow que deberian
poner el gate en rojo, **9 sobreviven**, incluida la forma exacta que produjo el defecto original --
y el gate sigue imprimiendo `contracts=48/48` mientras tanto.

## Estado canonico y arranque

    git fetch origin                                              ok
    git status --short                                            sin cambios ajenos tocados
    python scripts/validate_collaboration_state.py (arbol vivo)   EXIT 0
    HEAD local == origin/main == 744d4a1d                         ok

## Reproduccion (clon limpio en f6d88cb7, gate por exit code)

    python scripts/check_falsification_contracts.py --root . \
        --workflow .github/workflows/validate.yml --inventory      EXIT 0
        FALSIFICATION_EXECUTION runners=8/8 contracts=48/48
        FALSIFICATION_INVENTORY permanent_negatives=48 declared=48 missing=0
    python scripts/test_falsification_contracts.py                 EXIT 0
    python scripts/validate_collaboration_state.py --root .        EXIT 0
    python scripts/scan_encoding.py --root .                       EXIT 0
    python scripts/scan_domain_neutrality.py --root .              EXIT 0
    python runtime/protocol_replay.py --check-drift --root .       EXIT 0
        PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=7622
    python scripts/prune_state.py --root . --check                 EXIT 0
        (la poda vencida que reporte en la iteracion 1 ya no lo esta)

## Tabla punto por punto

    1  un paso por runner; el fallo rompe el job    PASS  (probado en el CI REAL)
    2  jsonschema instalado; el runner ejecuta      PASS  (probado en el CI REAL)
    3  el gate ata "el fallo del runner rompe el
       paso"                                        SLIP  9 de 14 mutantes sobreviven
    AC5 recuento honesto, sin "47 ejecutados"       PASS  (recomputado por mi, exacto)
    AC6 sin regresion en clon limpio                PASS
    4y5 inventario de rojos / negativo vacuo        FUERA DE ESTE CIERRE -- absorbidos por
                                                    TASK-0335 AC7 y AC8, verificado literal

---

## 1 y 2 -- Resueltos. Y la prueba en CI real no necesito mutante: la dio la propia tarea.

Me pediste forzar un fallo en el primer runner y comprobar que el job sale `failure`. No hizo falta
inyectar nada: el primer runner **ya esta rojo** por el sexto rojo asignado a TASK-0335. Eso convierte
la corrida 31204963761 sobre `f6d88cb7` en un experimento natural, que es mejor evidencia que un
mutante mio porque no toca el arbol.

    JOB falsification-runners                                -> failure
      4 Install falsification runner dependencies            -> success
      5 Execute mailbox retry falsification runner           -> failure
      6 Execute runtime turn falsification runner            -> success
      7 Execute post-gate falsification runner               -> success

    log del paso 5:  AssertionError ... run_unreadable_head_case
                     ##[error]Process completed with exit code 1.
    log del paso 6:  OK: authoritative delivery and in-schema friction controls are mutation-proved.
    log del paso 7:  OK: real run-log append rejects red-gate empty obstacles; green gate stays
                     narration-free; mutant is killed

**Punto 1 PASS.** El paso rojo arrastra el job a `failure`. En la iteracion 1 ese mismo rojo salia
dentro de un job `success`; hoy no. La propiedad esta atada en el efecto, no solo en la forma.

**Punto 2 PASS.** El paso 6 imprime su OK final: `jsonschema` esta instalado y el runner de turnos
ejecuta casos de verdad, no muere en el import. En la iteracion 1 no ejecutaba ni uno.

Y confirmo tu lectura del `if: always()`: los tres pasos producen evidencia en una sola pasada y el
job sigue cayendo. Es mejor que el minimo que pedi.

## 3 -- BLOQUEANTE confirmado, y mas ancho que el mutante que trajiste

Tu mutante multi-comando sobrevive. Lo reproduzco y ademas barro la familia entera. Bateria de 14
mutantes sobre `.github/workflows/validate.yml` en clon limpio, cada uno contra
`check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml`:

    mutante                                        gate    esperado   veredicto
    ---------------------------------------------------------------------------------
    M0  baseline (lo entregado)                    EXIT 0  PASS       OK
    M1  multicomando pwsh (LA FORMA DEL DEFECTO)   EXIT 0  FAIL       >>> SOBREVIVE
    M2  multicomando con shell: bash (set -e)      EXIT 0  PASS       OK (legitimo)
    M3  paso con `if: false`                       EXIT 0  FAIL       >>> SOBREVIVE
    M4  paso con `if:` de un evento que no ocurre  EXIT 0  FAIL       >>> SOBREVIVE
    M5  `python r.py || true` con shell: bash      EXIT 0  FAIL       >>> SOBREVIVE
    M6  `python r.py; exit 0` (sin espacio)        EXIT 1  FAIL       MATADO (por accidente, ver abajo)
    M7  `continue-on-error: ${{ true }}`           EXIT 0  FAIL       >>> SOBREVIVE
    M8  `continue-on-error: 'true'` (string)       EXIT 0  FAIL       >>> SOBREVIVE
    M9  `continue-on-error: true` (control)        EXIT 1  FAIL       MATADO
    M10 echo-only (control)                        EXIT 1  FAIL       MATADO
    M11 job con `needs: validate` (job se salta)   EXIT 0  FAIL       >>> SOBREVIVE
    M12 job con `if: false`                        EXIT 0  FAIL       >>> SOBREVIVE
    M13 `on:` reducido a workflow_dispatch         EXIT 0  FAIL       >>> SOBREVIVE

**9 escapes de 14.** Los tres que mueren son exactamente los tres que el contrato
`NEG-FALSIFICATION-RUNNER-WIRING` declara como boundaries. El gate mata lo que se le pidio matar y
nada mas.

M6 merece una nota porque es el mas enganoso: muere **por accidente del regex**, no por diseno. La
invocacion se ancla con `(?:\s|$)` detras de la ruta, asi que `r.py;` no casa. Basta un espacio:

    variante de UN SOLO comando                        gate    veredicto
    ------------------------------------------------------------------------
    V1  `python r.py ; exit 0` (con espacio)           EXIT 0  >>> SOBREVIVE
    V2  `python r.py || exit 0` (pwsh 7 soporta ||)    EXIT 0  >>> SOBREVIVE
    V3  `python r.py 2>$null; exit 0`                  EXIT 0  >>> SOBREVIVE
    V4  `python r.py --help` (no ejecuta ningun caso)  EXIT 0  >>> SOBREVIVE
    V5  `python r.py > out.txt` (redirige, SI gatea)   EXIT 0  OK (legitimo)

O sea: el criterio "un comando por paso" **ni siquiera esta implementado hoy**. Un paso de una sola
linea puede tragarse el codigo de salida (V1, V2, V3) o no ejecutar nada (V4) y el gate lo bendice.

La consecuencia que me preocupa no es que exista un hueco: es que el gate emite una **certificacion
afirmativa** -- `FALSIFICATION_EXECUTION runners=8/8 contracts=48/48` -- que es falsa bajo nueve
formas alcanzables del workflow. Esa linea es la que se va a citar. Es la enfermedad de la tarea una
capa mas arriba, igual que en la iteracion 1: una medida de cobertura que mide la declaracion en vez
del efecto.

### Tu pregunta: ni una cosa ni la otra

> Basta con exigir un comando por paso, o el gate tiene que razonar sobre el shell efectivo?

**Ninguna de las dos, y las dos preguntas comparten el mismo error de encuadre**: ambas miran el
*comando*, y la propiedad que quieres atar no es del comando sino de **la contribucion del paso al
veredicto del job**. Esa propiedad se descompone en cuatro factores independientes:

    (a) el paso llega a ejecutarse           if: del paso, if: del job, needs:, on: del workflow
    (b) el runner se invoca de verdad        no echo, no --help, no una ruta solo mencionada
    (c) el fallo del runner cae al paso      semantica del shell / adornos que traguen el codigo
    (d) el fallo del paso cae al job         continue-on-error en cualquiera de sus grafias

El gate de hoy cubre (b) parcialmente y (d) parcialmente. **(a) y (c) no los mira en absoluto.**
Ninguna cantidad de razonamiento sobre el shell arregla (a): `if: false` no es una cuestion de shell.

Sobre (c), que es donde estaba tu duda, mi juicio con la evidencia delante:

- **"Un comando por paso" no es NECESARIO.** M2 lo demuestra: GitHub invoca `shell: bash` como
  `bash --noprofile --norc -eo pipefail {0}`, asi que un bloque de tres comandos en bash SI gatea.
  Rechazarlo seria una regla comoda y falsa por el otro lado.
- **"Un comando por paso" tampoco es SUFICIENTE tal y como podria implementarse a la ligera.** V1-V4
  son un solo comando y no gatean. La condicion util no es "una linea": es **invocacion unica y sin
  adornos** -- tras quitar comentarios y lineas en blanco queda exactamente una linea, y esa linea
  casa la invocacion **anclada por los dos extremos**, sin operador de shell (`;`, `&&`, `||`, `|`,
  `&`) y sin argumentos que conviertan el runner en no-op.
- **Razonar sobre el shell efectivo es a la vez mas trabajo y menos solido.** Tendrias que resolver
  la precedencia `shell:` del paso > `defaults.run.shell` del job > del workflow > default del
  `runs-on`, y despues modelar los huecos documentados de `set -e`: un fallo a la izquierda de `&&`,
  dentro de un `if`, dentro de una funcion llamada en contexto de condicion, o en una subshell cuyo
  estado se descarta. Un modelo de shell incompleto reparte verdes falsos con cara de rigor.

**Mi recomendacion es la regla de invocacion unica, y es la respuesta a tu "prefiero una regla que
sea cierta a una que sea comoda":** es una **sobre-aproximacion conservadora**. Rechaza formas
legitimas (el bloque bash de M2) y no acepta ninguna que no gatee, **sea cual sea el shell** -- en
pwsh porque GitHub anade `exit $LASTEXITCODE`, en bash/sh por `-e`, en cmd por `errorlevel` del unico
comando. El coste de la sobre-aproximacion lo paga el maker partiendo el paso, que es exactamente lo
que ya hizo aqui y que ademas da mejor diagnostico en el log. El gate no necesita modelo de shell
porque la regla es cierta en todos ellos.

Y (a) y (d) son ortogonales a todo esto y baratos: rechazar `if:` en paso o job salvo ausente o
`always()`/`success()`; rechazar `needs:` sobre un job que puede saltarse; tratar `continue-on-error`
como veto si es cualquier cosa distinta de ausente o `false` literal (hoy `'true'` y `${{ true }}`
pasan); y comprobar que el workflow dispara en `push`/`pull_request`.

Esto no es pedir un gate perfecto. Los 13 mutantes de arriba son el criterio de aceptacion completo y
estan ya construidos: el script vive en `D:/Aegis_Scratch/mapp/analista-0330-r2/probe/mutants.py` y es
reproducible en cualquier clon limpio.

## AC5 -- El recuento es honesto. Recomputado por mi, cuadra.

Comprobado lo que prohibiste expresamente: **el handoff NO afirma "47 ejecutados"**. Al contrario, lo
desmiente de forma explicita ("This is the current count; it is not the historical coincidental `47`")
y declara el limite ("No claim is made that all 25 completed"). El AC5 se respeto.

Recomputo independiente sobre la salida `DECLARED` del gate en `f6d88cb7`:

    runner                                  contratos  fronteras   handoff dice
    run_mailbox_retry_cases.py                     17         37   17 / 37   ok
    run_runtime_turn_obstacle_cases.py              7         20   \
    run_post_gate_obstacle_cases.py                 1          2   /  8 / 22   ok
    los tres, total                                25         59   25 / 59   ok
    repo entero                                    48        ---   48/48     ok

Los cuatro numeros del handoff son exactos. Y la distincion que hace -- "invoked and enforced" para
el runner de retry frente a "executed and enforced" para los dos verdes -- es la distincion correcta
y la que faltaba en la iteracion 1.

## Puntos 4 y 5 -- fuera de este cierre, y la particion es real

No los cuento contra 0330. Verificado que la particion no es solo declarativa:
`TASK-0335-asercion-acoplada-al-formato-del-log.md` (status `ready`, owner Codex) lleva **AC7** con el
inventario incompleto de rojos (7o, 8o, 9o y la cola posterior a la linea 1390) y **AC8** con la
inalcanzabilidad y la vacuidad de `retry-ledger-head-defer-order`, ambos con el detalle tecnico
intacto y la clausula de que no se cierre "sobre la premisa de que el sexto era el ultimo".

## Residuales declarados

1. **El gate de AC4 sigue sin ejecutarse nunca en CI.** En la corrida 31204963761 el job `validate`
   muere en el paso 6 (`Validate repository dogfood instance`, `UnboundLocalError: InvalidSignature`,
   `runtime/eventlog.py:414`, el paquete `cryptography` no esta en el CI) y GitHub salta todo lo
   posterior, incluido el paso 11 `Validate falsification contracts and guardian controls`, que
   aparece `skipped`. Es anterior a esta tarea y el handoff lo declara honestamente; lo repito porque
   mientras siga asi el mecanismo central de AC4 tiene cero enforcement real. Anomalia DECISION-0018
   pendiente de dueno.
2. **Dependencia nueva sin manifiesto.** `check_falsification_contracts.py` ahora hace `import yaml`
   en el modulo. El repo no tiene fichero de requisitos; `pyyaml` solo se instala en el job
   `validate`. Cualquiera que corra el gate en local sin `pyyaml` obtiene ImportError. Falla cerrado,
   asi que no produce verde falso, pero es una dependencia de terceros no declarada.
3. Mis mutantes se aplicaron y revirtieron dentro del clon de scratch
   `D:/Aegis_Scratch/mapp/analista-0330-r2/`, nunca en el arbol canonico. Restauracion verificada:
   gate EXIT 0 con el workflow original tras cada bateria.
4. No inyecte ningun mutante en el CI real: la evidencia del punto 1 sale de la corrida natural.

## Recomendacion de cierre

    CHANGE-REQUIRED

Lo que falta, y solo esto:

1. **(bloqueante) `step_gates_runner` debe atar los cuatro factores, no dos.** Regla de invocacion
   unica y sin adornos para (c); `if:`/`needs:` de paso y job para (a); `continue-on-error` truthy en
   cualquier grafia para (d). El regex de (b) debe anclar por los dos extremos.
2. **(bloqueante) Los 13 mutantes de este veredicto pasan a ser boundaries de
   `NEG-FALSIFICATION-RUNNER-WIRING`**, no solo los tres actuales. Un gate cuyo contrato declara
   exactamente los escapes que ya mueren no es falsable: es una foto de si mismo.
3. Mientras 1 y 2 no esten, **`FALSIFICATION_EXECUTION runners=8/8 contracts=48/48` no debe citarse
   como prueba de ejecucion** en ningun handoff ni reporte -- la misma disciplina que aplicaste al
   "47" y que Codex respeto en el AC5.

Lo que NO hay que tocar: el cableado del job `falsification-runners`. Un paso por runner con
`if: always()` en los dos siguientes es la forma correcta, esta probada en el CI real, y la regla de
invocacion unica que recomiendo la acepta sin cambios.

## Bucle de correccion y escalado

    iteracion     esta es la 2 de las 2 que fije. El punto 3 sigue abierto, asi que
                  **escalo al operador humano**, tal y como acordamos.
    lo que NO es  no es un rechazo del trabajo entregado: AC1, AC2, AC3, AC5 y AC6 estan cumplidos y
                  los dos puntos bloqueantes de la iteracion 1 estan probados en el CI real. El
                  residuo bloqueante es UNO y es estrecho: la solidez de la certificacion afirmativa
                  que emite el gate.
    decision      del operador, no mia: (a) tercera iteracion sobre 0330 con los puntos 1 y 2 de
                  arriba, o (b) particionar el punto 3 a una tarea nueva y cerrar 0330, con la
                  condicion dura de que 0330 no se cierre afirmando "8/8 runners, 48/48 contratos
                  ejecutados" mientras los 9 escapes sigan vivos.
    gates         check_falsification_contracts --workflow --inventory, test_falsification_contracts,
                  los tres runners, validate, scan_encoding, scan_domain_neutrality, drift; y la
                  bateria de 13 mutantes como criterio de aceptacion.
    re-juicio     antes del commit de cierre, no despues.

-- Analista
