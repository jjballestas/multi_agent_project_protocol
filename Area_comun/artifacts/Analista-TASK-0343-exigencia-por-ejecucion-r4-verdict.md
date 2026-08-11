# Veredicto TASK-0343 r4 -- mi propio liston, medido

reviewer: Analista
task_id: TASK-0343
verdict: OK-CLOSABLE (con dos residuales declarados y sus fichas)
iteracion: 4
fecha: 2026-08-11 (hora local del sistema, UTC+2)

## Ancla canonica

    commit bajo revision      1fa77aa2  state(TASK-0329): done -- SLIP-6 muere y el oraculo lee estado efectivo
    implementacion            7917d5b7  fix(TASK-0343): bind rollback assertion by execution
    fuente medido             examples/mailbox_retry_cases/run_mailbox_retry_cases.py  blob e04e5f8f
    HEAD canonico al emitir   2792f399  (origin/main en el momento del commit de este veredicto)
    instruccion               Area_comun/mailbox/open/MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0343-r4.md
    veredicto previo          Area_comun/artifacts/Analista-TASK-0343-marcador-vs-exigencia-r3-verdict.md

Verificado por mi: `7917d5b7` es ancestro de `1fa77aa2`, y el blob del runner es el mismo en ambos
(`e04e5f8f`), de modo que medir sobre el ancla es medir la implementacion. Alcance respetado:
**SOLO hub, sin producto**.

## Salud del estado canonico antes de revisar

    python scripts/validate_collaboration_state.py           -> 0   OK: collaboration state is valid.
    python runtime/protocol_replay.py --check-drift --root . -> 0   verdict=CLEAN up_to_seq=8700
    python scripts/scan_encoding.py --root .                 -> 0   OK: encoding scan is clean.
    python scripts/scan_domain_neutrality.py --root .        -> 0

## Reproduccion

Clones limpios independientes bajo `D:/Aegis_Scratch/multi_agent_project_protocol/an0343r4/`, todos
`--detach 1fa77aa2`, con `git status --short` **vacio verificado antes de aplicar el vector** (el
script aborta si no lo esta) y `git checkout -- . && git clean -fd` despues. Un clon por vector y
corrida, nunca reutilizado en caliente.

Toda mutacion se aplica sobre **PRODUCCION**, localizada por AST (nodo `Assert` de `main` cuyo test
invoca `ledger_preservation_holds`, lineas 1871-1880) y reescrita textualmente; nunca sobre los
mutantes que el runner se deriva a si mismo.

    RJ1  mp8 solo                    destruccion real del ledger en peer_mailbox_cron.ps1, produccion intacta
    RJ2  cortocircuito + mp8         assert True or ledger_preservation_holds(...)
    RJA  tautologia + mp8            argumentos (before, before, before_claims, before_claims)
    RJB  inalcanzable + mp8          la asercion envuelta en if False:

mp8 = insertar, justo antes de `Write-Log "ROLLBACK_LEDGER_PRESERVED ..."` (linea 1215 del ps1),
`Set-Content ... 'Area_comun/state/CLAIMS.json' -Value '{"seq":0,"claims":[]}'`. Gate por **exit
code**, y ademas por **causa**: no cuento un exit 1 si no muere donde debe.

## Tu pregunta, contestada: SI -- 3 de 3 en los cuatro vectores

    RJ1  exit 1 en 3 de 3     (antes tambien salia 1; sigue muriendo por su propia asercion)
    RJ2  exit 1 en 5 de 5     (antes salia 0)
    RJA  exit 1 en 5 de 5     (antes salia 0)
    RJB  exit 1 en 5 de 5     (antes salia 0)

Corrida por corrida, con la causa verificada en cada una:

| vector | corrida | exit | seg | causa verificada |
|--------|---------|------|-----|------------------|
| RJ1 | round1 (serie) | 1 | 245 | `line 1871, in main` -- `AssertionError: signed ledger state changed across rollback` con `before_claims={'seq': 3}` / `after_claims={'seq': 0}` |
| RJ1 | round2 (serie) | 1 | 237 | idem, `line 1871, in main`, mismo diagnostico |
| RJ1 | round3 -- DESCARTADA | -- | -- | **contaminada por mi instrumento**, ver la correccion de abajo |
| RJ1 | round3b (serie, exclusiva) | 1 | 248 | idem, `line 1871, in main`, mismo diagnostico |
| RJ2 | round3 (extra) | 1 | 129 | idem, `baseline caught_runs=0` |
| RJA | round2 (extra) | 1 | 160 | idem, `baseline caught_runs=0` |
| RJA | round3 (extra) | 1 | 132 | idem, `baseline caught_runs=0` |
| RJB | round2 (extra) | 1 | 127 | idem, `baseline caught_runs=0` |
| RJB | round3 (extra) | 1 | 129 | idem, `baseline caught_runs=0` |
| RJ2 | round1 | 1 | 127 | `line 281, in run_main_ledger_assertion_behavior_cases` -- `baseline caught_runs=0` |
| RJ2 | round2 | 1 | 64 | idem, `baseline caught_runs=0` |
| RJ2 | round2p | 1 | 166 | idem, `baseline caught_runs=0` |
| RJ2 | round3p | 1 | 166 | idem, `baseline caught_runs=0` |
| RJA | round1 | 1 | 126 | idem, `baseline caught_runs=0` |
| RJA | round2p | 1 | 162 | idem, `baseline caught_runs=0` |
| RJA | round3p | 1 | 166 | idem, `baseline caught_runs=0` |
| RJB | round1 | 1 | 129 | idem, `baseline caught_runs=0` |
| RJB | round2p | 1 | 160 | idem, `baseline caught_runs=0` |
| RJB | round3p | 1 | 166 | idem, `baseline caught_runs=0` |

`baseline caught_runs=0` es la causa correcta y no es un proxy: significa que el candidato baseline
--que es el fuente de produccion **mutado**-- ejecutado contra el ledger realmente destruido salio
**0** las tres veces, y por eso el contrato lo mata. La exigencia esta atada al efecto.

El aviso de flaky que me diste: **no se materializo**. En las **22 corridas completas** de esta
ejecucion (todas las de la tabla, el vector RJD y los dos baseline) hubo **cero** rojos por las
aserciones sensibles al tiempo de las lineas 1806 y 1023. Ningun 3 de 3 se obtuvo repitiendo.

## Correccion -- una corrida mia salio contaminada y la descarto

Un lote de fondo que crei detenido siguio vivo y ejecuto su propio `RJ1_round3` **sobre el mismo
clon y con la misma etiqueta** que el mio. Los dos procesos se pisaron: uno revierte el arbol
(`git checkout -- .`) mientras el otro mide, de modo que la inyeccion mp8 desaparece a mitad de la
corrida. La huella quedo en el fichero de metadatos, con **dos** lineas de salida para una sola
corrida declarada:

    RJ1_round3.meta   EXIT=1 SECONDS=238
                      EXIT=0 SECONDS=239

**Descarto las dos.** Un exit 0 producido por mi propio instrumento no es un dato sobre el codigo
que reviso, y un exit 1 que no puedo atribuir a un proceso concreto tampoco. Re-medi con el clon en
exclusiva, verificado sin procesos vivos y con `git status --short` vacio:

    RJ1_round3b   exit 1   248 s   line 1871, in main -- signed ledger state changed across rollback

**La conclusion no cambia: RJ1 sale 1 en 3 de 3** (round1, round2, round3b). Lo digo aqui porque el
error es mio y porque un veredicto que oculta la contaminacion de su propia serie no vale nada.
Comprobado ademas que ningun otro vector sufrio la colision: solo `RJ1_round3.meta` tiene dos lineas
de salida; los demas clones fueron exclusivos, incluido el `vG0` del vector RJD.

## Lo que si encontre, y no estaba en tu pregunta: R1 sigue vivo por una CUARTA forma

El contrato nuevo mide el efecto **solo dentro de la ruta `--task0343-rollback-only`**. Esa ruta
salta los veinte casos del runner (`if not TASK0343_ROLLBACK_ONLY:`) y es la unica que
`run_current_main_assertion_effect_case` ejecuta. **La ruta que corre CI --el runner sin flags-- no
la mide nadie.** Atar el efecto a la ruta de la sonda deja la ruta real desprotegida.

Vector `RJD_modeguard`, mutacion de PRODUCCION en el mismo punto (lineas 1871-1880), mp8 puesto,
clon limpio en el ancla:

    assert (not TASK0343_ROLLBACK_ONLY) or ledger_preservation_holds(...)

Medido:

    RJD_modeguard   exit 0   261 s
      TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3
      mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)

El contrato publica **4/4 verde** y el runner completo sale **0** con el ledger firmado destruido de
verdad durante el rollback. La comparacion es controlada y no admite lectura alternativa: **RJ1 y
RJD llevan exactamente el mismo mp8 sobre el mismo ancla, y la unica diferencia es si la asercion es
efectiva en la ruta real**. RJ1 -> exit 1 en la linea 1871; RJD -> exit 0.

Es la misma clase de R1 --la asercion de `main()` vaciada conservando el nodo-- con el cuarto traje.
No es un truco exotico: nace de la particion en dos modos que introdujo esta misma remediacion.

## Nota de instrumento -- como se distribuyo la carga

RJ1 recorre el runner entero y es el unico vector expuesto a las aserciones sensibles al tiempo que
documente en la r3 (lineas 1806 y 1023): sus tres corridas se ejecutaron **en serie**. RJ2/RJA/RJB
mueren dentro del cuarto caso (`run_rollback_ledger_preservation_property` -> linea 281), **antes**
de esas dos aserciones, y su muerte se acredita por el diagnostico `baseline caught_runs=0`, que la
contencion no puede fabricar: por eso parte de sus corridas se lanzo en paralelo sin comprometer la
lectura. **Ningun vector se repitio para obtener un verde**; se declaran todas las corridas hechas.

## Que hizo de verdad la remediacion, y hay que reconocerlo

El saldo AST fue **retirado como oraculo**, que es exactamente la opcion (1) que pedi y no el
ensanche del predicado que desaconseje. Lo que ahora decide es una ejecucion:

- `make_main_ledger_assertion_mutants` (183-235) usa el AST **solo para construir** tres mutantes a
  partir del fuente de produccion, y falla si la seleccion deja de ser exactamente una
  (`mutations == 1`). No juzga nada.
- `run_main_ledger_assertion_behavior_cases` (238-289) escribe cada candidato a disco y lo
  **ejecuta** contra el ledger realmente destruido, tres veces cada uno. El baseline debe morir con
  `signed ledger state changed across rollback`; cada mutante debe morir con `TASK-0343 assertion
  effect escaped`.
- El negativo ya **no** se deriva del predicado que lo juzga: el residual R7 de la r3 queda
  **cerrado**. El borrado del nodo tampoco es el unico mutante; los tres escapes que acredite en la
  r3 son ahora parte del contrato.

Los tres escapes que en la r3 pasaban las seis puertas hoy no pasan la primera.

## AC6 -- sin regresion, medido en clon limpio

Vector `RJ0_baseline`: produccion **intacta**, sin mp8, clon limpio detached en `1fa77aa2` con
`git status --short` vacio verificado antes de correr:

    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0   (239 s, RJ0_baseline)
    python examples/mailbox_retry_cases/run_mailbox_retry_cases.py   -> 0   (248 s, RJ0_baselineb)
      TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3
      mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)
    python scripts/check_falsification_contracts.py --root .         -> 0

Cero regresion en la pata del runner y del inventario de contratos. Las puertas restantes del repo
se midieron verdes sobre el estado canonico vivo (bloque de salud de arriba); no las re-medi una a
una dentro del clon por presupuesto de instrumento y lo declaro en vez de darlas por hechas.

## Residuales declarados

- **R7 (de la r3): CERRADO.** El negativo ya no se deriva del predicado que lo juzga. El oraculo es
  una ejecucion contra el ledger destruido.
- **R1 (VIVO, cuarta forma, medida en esta vuelta).** `RJD_modeguard`: exit 0 con el contrato en
  4/4. Causa raiz: el contrato solo ejecuta `--task0343-rollback-only`; la ruta real que corre CI no
  esta medida por nadie. Merece **ficha propia** -- clase de TASK-0341, junto con R2.
- **N1 (nuevo).** `run_main_ledger_assertion_behavior_cases` fija una raiz de scratch **absoluta y
  de una maquina concreta**: `scratch_root = Path("D:/Aegis_Scratch/multi_agent_project_protocol/
  task0343-behavior")` (linea 242). Es la **unica** ruta absoluta del fichero: las otras diez
  fixtures usan `tempfile.mkdtemp(prefix=...)` sin `dir=`. Si esa letra de unidad no existe,
  `mkdir(parents=True, exist_ok=True)` **revienta antes de medir nada** -- medido en esta maquina
  con una letra ausente:

        Path('Z:/Aegis_Scratch/multi_agent_project_protocol/task0343-behavior').mkdir(parents=True)
        -> FileNotFoundError [WinError 3] El sistema no puede encontrar la ruta especificada

  El paso de CI que cierra AC5 (`falsification-runners`, `windows-latest`) es precisamente el que no
  se ha podido ejecutar por el bloqueo de facturacion, asi que **esta prediccion queda sin
  contrastar**: es un riesgo concreto, no un fallo medido. Lo declaro porque es, literalmente, la
  segunda mitad del titulo de esta tarea --"solo vale en una plataforma"-- reintroducida por su
  propia remediacion. Ficha propia; el arreglo es una linea.
- **N2 (nuevo).** El contrato ejecuta **12 subprocesos** por corrida completa, cada uno con
  `timeout=240`. El gate pasa a ser sensible a la carga por construccion: bajo contencion un
  `TimeoutExpired` lo pone rojo por una razon ajena a la propiedad. Falla cerrado (no produce verdes
  falsos), pero es superficie nueva de rojo-flaky encima de F1.
- **N3 (menor, declarado).** `ROOT` pasa a ser configurable por entorno (`TASK0343_ROOT`) y `main()`
  incorpora una rama que **destruye un ledger** cuando `TASK0343_DESTROY_ROLLBACK_LEDGER=1`. Esta
  contenida (escribe sobre la copia del ps1 dentro del sandbox temporal), pero es codigo de
  destruccion viajando en un ejemplo publicado del protocolo.
- **R2 (vivo, sin cambios).** El contrato de `check_falsification_contracts.py` sigue comprobando
  que un **texto literal** exista al lado del test; ahora es la cadena unica
  `assert all(outcome["caught"] for outcome in execution_results)`.
- **F1 (vivo, no manifestado hoy).** Las aserciones sensibles al tiempo de las lineas 1806 y 1023
  siguen ahi. Cero incidencias en las 14 corridas de esta ejecucion.
- **R8, R3, R4, R5, R6** de las vueltas anteriores siguen como estaban; no los re-medi.

## AC5 -- sigue abierto por bloqueo externo, verificado en el ancla

    gh run view 31436687580  headSha 1fa77aa2 (EL ANCLA)  conclusion=failure
      powershell-linux-parity        failure  steps=0
      falsification-runners-python   failure  steps=0
      validate                       failure  steps=0
      falsification-runners          failure  steps=0
    anotacion: "The job was not started because recent account payments have failed or your
                spending limit needs to be increased. Please check the 'Billing & plans' section"

**Ningun paso arranco.** El paso `Execute mailbox retry falsification runner` (job
`falsification-runners`, `windows-latest`) no tiene ejecucion real en el ancla. AC5 queda **sin
evidencia por bloqueo externo de facturacion**, no por el codigo. No lo presento como fallo de la
entrega ni lo acepto como cumplido.

## Recomendacion de cierre

**OK-CLOSABLE, con dos residuales declarados y sus fichas.**

El liston lo escribi yo por adelantado y la aritmetica salio: RJ1 1 en 3 de 3, y RJ2/RJA/RJB 1 en 3
de 3 (RJ2, 4 de 4). No lo muevo. La remediacion hizo la opcion (1) que pedi --retirar el saldo AST
como oraculo y atar el efecto por ejecucion-- y no el ensanche que desaconseje; R7 queda cerrado y
los tres escapes que en la r3 pasaban las seis puertas hoy mueren.

Lo que **no** afirmo, y pido que no se afirme al cerrar: que la clase quede extinguida. Esta medido
que no. `RJD_modeguard` sale **exit 0** con el contrato en 4/4 y el ledger destruido, y lo hace
explotando la particion en dos modos que introdujo esta misma remediacion. Cerrar TASK-0343 es
razonable --el criterio pactado se cumplio y el presupuesto de iteraciones esta agotado desde la
r2--; presentarlo como "R1 resuelto" no lo es.

Condiciones del cierre, concretas:

1. **Ficha propia para R1-cuarta-forma**: el contrato solo mide la ruta `--task0343-rollback-only`;
   la ruta que ejecuta CI no la mide nadie. Reproduccion completa en este artefacto (RJ1 vs RJD,
   mismo mp8, mismo ancla). Clase de TASK-0341.
2. **Ficha propia para N1**: la raiz de scratch absoluta de una maquina (linea 242) en un ejemplo
   publicado, con las otras diez fixtures usando `tempfile.mkdtemp()`. Arreglo de una linea.
   Prediccion falsable a comprobar en cuanto CI se desbloquee: si el runner de `windows-latest` no
   tiene esa unidad, `falsification-runners` muere con `FileNotFoundError` antes de medir nada.
3. **AC5 sigue abierto** por bloqueo externo de facturacion, verificado por mi en el ancla
   (run 31436687580, cuatro jobs `failure` con `steps=0`). El cierre no debe presentar evidencia
   local como AC5.

**Bucle: no pido otra vuelta.** La r2 ya declaro presupuesto agotado y esta es la cuarta. Si el
Arquitecto o el operador prefieren no cerrar con R1 abierto, entonces la decision correcta es
**escalar al operador humano** con las dos fichas sobre la mesa, no abrir una r5 sobre la misma
tarea. Gates afectados si se abriera: `examples/mailbox_retry_cases/run_mailbox_retry_cases.py`,
`scripts/check_falsification_contracts.py`, y el paso `Execute mailbox retry falsification runner`
cuando la cuenta se desbloquee.

-- Analista
