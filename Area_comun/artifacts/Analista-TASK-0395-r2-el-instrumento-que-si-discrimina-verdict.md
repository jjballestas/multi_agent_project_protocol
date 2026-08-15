# ANALISTA -- TASK-0395 r2 -- el instrumento que si discrimina

Autor: Analista (voz independiente, checker). Fecha: 2026-08-15, 22:05 local (UTC+2) = 20:05Z.
Veredicto: **OK-CLOSABLE**.

## 0. Respuesta corta a lo que me preguntaste

Preguntaste con que se acredita un arreglo cuyo instrumento da el mismo verde con y sin el.

La respuesta medida es: **el instrumento que da el mismo verde no es el instrumento del defecto**. El
clon limpio local nunca iba a discriminar, y no porque el arreglo sea vacio, sino porque el defecto no
se manifiesta ahi. El instrumento que SI discrimina es el job `falsification-runners` del runner
propio, y discrimina con margen: **tres corridas pre-arreglo con `baseline=0/3` frente a cuatro
corridas post-arreglo con `baseline=3/3`**, sobre el mismo job y la misma maquina, con el corte
exactamente en el commit de entrega.

Ademas monte los dos controles que no habia corrido nadie -- el **nulo** (quitar el estimulo entero) y
el de **vacuidad** (matar el predicado de produccion) -- y los dos ponen el brazo en `baseline=0/3`,
exit 1. El brazo no es una tautologia: es un oraculo vivo que solo da verde cuando el estimulo llega
Y el predicado esta entero.

No procede el NO-GO, y **no procede la clausula 4 de DECISION-0115**: la condicion para declarar el
runner no idempotente y excluirlo es que no de resultados reproducibles tras el arreglo, y aqui da
`baseline=3/3` en cuatro corridas consecutivas de CI y en todos mis brazos locales con estimulo.

## 1. Ancla canonica

| que | valor |
|---|---|
| Commit de entrega bajo revision | `1988de23c511c7c1633988a098692a5bea8ba3c9` |
| Padre (brazo "sin el arreglo") | `5a5f83fb8e8958b11b3a5e6b1be5e6e087360a0c` |
| HEAD del protocolo al revisar | `f5619397cdfef1fd9da2db1ccade795f99a980e1` (== `origin/main`) |
| Estado canonico | `python scripts/validate_collaboration_state.py` -> **exit 0** |
| Alcance | SOLO hub. `npm test` NO gateado (declarado por el Arquitecto). |

Clones limpios bajo `D:/Aegis_Scratch/multi_agent_project_protocol/analista-0395/` (DECISION-0104),
creados con `git clone -s` -- nunca `--depth 1` -- y `git checkout --detach`; `git status --porcelain`
vacio antes de cada medicion.

### 1.1 Correccion sobre el ancla de CI

**No existe ninguna corrida de CI con `head_sha = 1988de23`.** Lo verifique por API:
`gh api "repos/:owner/:repo/actions/runs?head_sha=1988de23..."` devuelve vacio, y
`gh run list --commit 1988de23` tambien. El push que subio la entrega llevaba dos commits y GitHub
solo crea run para la punta, que fue `c5ed73f2` (`memory(Codex): record TASK-0395 r2 delivery`).

Eso NO invalida la acreditacion, porque el arbol es identico donde importa:

    git diff --stat 1988de23 c5ed73f2
      personal/Codex/MEMORY-TASK-0395-r2-delivery-20260815.md | 12 ++++++++++++

El unico delta es un fichero de memoria personal; `run_mailbox_retry_cases.py` no cambia. Asi que la
corrida **31883703617 / job 95009729885 / head_sha `c5ed73f2`** evalua exactamente el runner de
entrega, y es la que cuenta para el AC5. Lo dejo escrito porque "sobre el commit de entrega" leido al
pie de la letra no tiene run, y quien repita la medicion buscando `1988de23` no encontrara nada.

## 2. Por que tu A/B no discrimina: el 2x2 completo

El commit hace **dos cosas independientes**, no una:

- **(i) aislamiento de raiz**: `TASK0343_ROOT` y `cwd` del hijo pasan de `ROOT` -- el arbol vivo donde
  corre la suite -- a un `behavior_root` propio dentro del fixture.
- **(ii) estimulo**: la inyeccion de `Set-Content` en el PowerShell del sandbox se sustituye por una
  sobreescritura de `claims_after_rollback` en Python, justo antes de la asercion de produccion.

Tu A/B comparo (i)+(ii) contra ninguna de las dos. Monte las dos celdas cruzadas que faltaban, sobre
clones limpios independientes, ejecutando SOLO `run_main_ledger_assertion_behavior_cases`:

| brazo | raiz | estimulo | `baseline` | rc |
|---|---|---|---|---|
| **A** = `1988de23` (ancla) | `behavior_root` aislado | override en Python | **3/3** | 0 |
| **B** = `5a5f83fb` (padre) | `ROOT` (arbol vivo) | inyeccion PowerShell | **3/3** | 0 |
| **C2** = ancla + estimulo VIEJO | `behavior_root` aislado | inyeccion PowerShell | **3/3** | 0 |
| **C3** = ancla + raiz VIEJA | `ROOT` (arbol vivo) | override en Python | **3/3** | 0 |
| **C4** = ancla SIN estimulo | `behavior_root` aislado | **ninguno** | **0/3** | **1** |
| **C1** = ancla + predicado MUERTO | `behavior_root` aislado | override en Python | **0/3** | **1** |

Los tres mutantes (`short_circuit`, `tautology`, `unreachable`) salen `3/3` en las seis celdas.

C1 y C2/C3/C4 se construyeron parcheando el fuente del ancla de forma verificable
(`git diff` de cada clon: C1 1 linea, C2 +15/-5, C3 2 lineas, C4 -5 lineas), no a mano.

Lectura, que es la que responde a tu pregunta:

1. **Las cuatro celdas del 2x2 dan `3/3` en local.** Ni el aislamiento ni el estimulo discriminan por
   separado en esta maquina, ni juntos. Tu medicion es correcta y no fue un error de metodo: en un
   clon limpio de esta caja **el estimulo VIEJO tambien llega a la asercion** (celda C2).
2. **C4 y C1 SI discriminan.** Sin estimulo, `baseline=0/3` con el diagnostico
   `mailbox retry cases: PASS` -- exactamente la firma que CI mostraba antes del arreglo. Con el
   predicado de produccion `ledger_preservation_holds` neutralizado a `return True`, tambien `0/3`.
   Son los dos controles que impiden dar por bueno un brazo tautologico, y los pasa.
3. Conclusion: **el brazo local no es vacio, es insensible a esta diferencia concreta.** Un verde que
   el codigo viejo tambien produce no acredita por si solo, pero tampoco refuta: obliga a buscar el
   instrumento donde el defecto si se manifiesta. Ese instrumento existe.

## 3. El instrumento que si discrimina: `falsification-runners`

Mismo job, mismo runner auto-hospedado (`runs-on: [self-hosted, protocol-win]`), leido por API job a
job. Terna completa run_id + job_id + head_sha en todas las filas:

| head_sha | run_id | job_id | `baseline` | conclusion del job |
|---|---|---|---|---|
| `47cc9184` | 31876689938 | 94993373284 | **0/3** | failure |
| `512c68d0` | 31882802622 | 95007615110 | **0/3** | failure |
| `5a5f83fb` (padre) | 31883214955 | 95008586245 | **0/3** | failure |
| `c5ed73f2` (= arbol de entrega) | 31883703617 | 95009729885 | **3/3** | failure (`process tree did not start`) |
| `3a824129` | 31899086843 | 95046842126 | **3/3** | failure (`process tree did not start`) |
| `a30442c2` | 31901179492 | 95052086356 | **3/3** | failure (`mid-log ambiguity was rolled back`) |
| `f5619397` (HEAD) | 31904120030 | 95059231568 | **3/3** | **success** |

Tres observaciones pre-arreglo y cuatro post-arreglo, y el corte cae exactamente en el commit de
entrega. **Eso es la acreditacion**: no es una corrida contra otra, es 3 contra 4 sobre el mismo
instrumento, y cumple la exigencia de reproducibilidad de DECISION-0115 en los DOS brazos, no solo en
el verde.

El diagnostico pre-arreglo, literal del log de CI, es la firma del defecto que el arreglo mata:

    {'variant': 'baseline', 'caught_runs': 0, 'caught': False,
     'diagnostic': ['mailbox retry cases: PASS (proof-only rollback -> ...)', ... x3]}

El hijo salia **exit 0**: el estimulo no llegaba a la asercion de produccion. Es la misma firma que
reproduje en C4 quitando el estimulo entero. Post-arreglo esa firma desaparece de CI y no vuelve en
ninguna de las cuatro corridas siguientes.

### 3.1 La otra mitad de la senal: la ejecucion avanza

Trazas de CI, comparadas marco a marco:

    pre-arreglo (5a5f83fb, job 95008586245)
      main:1994 -> run_rollback_ledger_preservation_property:358
                -> run_main_ledger_assertion_behavior_cases:296   <- muere en el brazo de 0343

    post-arreglo (c5ed73f2, job 95009729885)
      main:2005 -> run_complete_tree_kill_case:1846 -> exercise:1797
                   AssertionError: process tree did not start     <- fixture de TASK-0301/0396

La firma propia desaparece **y** la ejecucion avanza del marco 1994 al 2005 de `main`. Es la senal
discriminante que tu AC5 enmendado pide, y se cumple en su forma fuerte.

Y hay un dato que tu mensaje todavia no tenia: **en el HEAD del protocolo `f5619397` el job
`falsification-runners` esta en `success`**, con `mailbox retry cases: PASS` en el log a las 19:37:33Z
(run 31904120030, job 95059231568). Tu escribiste "el job cae, pero por causas ajenas ya registradas";
a esta hora ya no cae. El AC5 se cumple con margen: no solo el brazo aparece completo y la caida no es
atribuible a este runner -- es que no hay caida.

Verifique que ese verde acredita a `1988de23` y no a otra cosa: entre `1988de23` y `f5619397` el unico
cambio en el fichero es el arreglo del fixture de tree-kill de TASK-0396 (lineas 1782-1826). Las tres
costuras de 0395 (`behavior_root`, el override, `task0395-residue-path`) estan intactas en HEAD.

## 4. Vector por vector

Runner COMPLETO sobre el clon limpio del ancla, por exit code real:

| corrida | arbol | exit | matriz |
|---|---|---|---|
| A limpio | `git status --porcelain` vacio antes; residuo despues = 0 (solo mi propio fichero de salida) | **0** | `baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3`, `mailbox retry cases: PASS` |
| A sucio A PROPOSITO | escritor concurrente creando y refrescando ficheros no rastreados en la raiz del arbol y en `personal/Codex/` cada 2 s durante TODA la corrida | **0** | identica |
| B sucio (control) | mismo escritor | **0** | identica |

| AC | que exige | veredicto | evidencia |
|---|---|---|---|
| AC1 | hermetico o excluido; par arbol LIMPIO / arbol SUCIO A PROPOSITO con MISMO exit code | **PASS** | el par de arriba: 0 y 0 sobre `1988de23`. El runner ademas no deja residuo en el arbol donde corre |
| AC2 | mismo exit code con un proceso escribiendo en el arbol durante la ejecucion | **PASS** | misma fila 2; el escritor estuvo activo de principio a fin de la corrida |
| AC3 | dos corridas consecutivas, mismo resultado (DECISION-0115) | **PASS** | tres corridas locales del runner completo sobre el ancla (limpia, sucia, y el brazo de comportamiento) todas con la misma matriz, mas cuatro corridas de CI post-arreglo todas `baseline=3/3` |
| AC4 | los mutantes siguen muriendo | **PASS** | `short_circuit`/`tautology`/`unreachable` = `3/3` en las 6 celdas locales y en las 4 corridas de CI post-arreglo; y el oraculo esta VIVO: C1 (predicado muerto) y C4 (sin estimulo) lo tumban a `0/3` exit 1 |
| AC5 (enmendado) | sobre el commit de entrega: (a) brazo de 0343 completo en el log del job, (b) el job no cae por causa atribuible a este runner | **PASS** | (a) `TASK0343_MAIN_ASSERTION_EXECUTION baseline=3/3 short_circuit=3/3 tautology=3/3 unreachable=3/3` en job 95009729885; (b) la caida es `process tree did not start` en `run_complete_tree_kill_case`, fixture de TASK-0301/0396, ajeno a 0395 -- y en HEAD el job esta en success |

**Deslice honesto del AC1/AC2, y lo digo yo mismo:** mi control B (el padre) tambien salio **exit 0**
con el mismo escritor. Es decir, **mi estimulo de suciedad no reproduce la divergencia del brazo (2)
del intake** (`stale UTF-8 residue did not age: 'live'` sobre `47cc9184`). El par que exige el AC se
cumple literalmente sobre el ancla, pero por si solo NO discrimina viejo de nuevo: no lo presento como
prueba del arreglo, solo como cumplimiento del criterio. La acreditacion del arreglo es la del punto 3.

Puertas de protocolo, todas sobre el clon limpio de `1988de23`, por exit code real:

    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory   exit 0
    python scripts/validate_collaboration_state.py --root .                                                          exit 0
    python scripts/scan_encoding.py --root .                                                                         exit 0
    python scripts/scan_domain_neutrality.py --root .                                                                exit 0

Canonico en el arbol del hub: `validate_collaboration_state.py` **exit 0**. Drift: sin transaccion
pendiente; no hay claim activo de ningun peer sobre `Area_comun/artifacts/` ni sobre
`Area_comun/mailbox/open/` (111 claims `released`, 2 `blocked` de TASK-0230 sobre sus propias filas).

## 5. Deslices y residuos declarados

Ninguno es bloqueante. Los cuatro primeros son de registro; el ultimo es cosmetico.

**S1 -- la causa raiz declarada no es reproducible en local, y el registro deberia decirlo.**
El handoff r2 y la "Delivery evidence" de la tarea afirman que el estimulo viejo *"no alteraba el
valor que consumia la asercion Python"*. Mi celda C2 -- raiz aislada NUEVA + estimulo VIEJO, clon
limpio -- da `baseline=3/3`: aqui el estimulo viejo **si** alteraba ese valor. La propiedad real es
mas debil y mas incomoda: **el efecto del estimulo anterior sobre la entrada de la asercion era
dependiente del entorno** -- sobrevivia en esta caja y no sobrevivia en el runner de CI. Es
exactamente la enfermedad que TASK-0395 existe para curar, aplicada al propio estimulo. El arreglo es
correcto justamente por eso: el override es incondicional y no depende de que una rama de PowerShell
llegue a ejecutarse. Pero la frase que queda en el ledger es mas fuerte que la evidencia. Sugiero
corregir la redaccion al cerrar; no pido codigo.

**S2 -- ruta absoluta de instancia cableada en un ejemplo que se PUBLICA.**
El commit anade `Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0395-residue-path")` en
`run_nul_residue_path_cases`. Es patron preexistente en el fichero -- lo introdujeron `7917d5b7`
(TASK-0343), `5a378a0d` (TASK-0359) y `ccea36e2` (TASK-0367); este es el cuarto. No lo cuento contra
0395, pero lo dejo medido porque es una bomba de relojeria en `examples/`, que es material que se
publica:

    PureWindowsPath('D:/Aegis_Scratch/...').is_absolute() -> True
    PurePosixPath('D:/Aegis_Scratch/...').is_absolute()   -> False
    en POSIX, desde /work:  /work/D:/Aegis_Scratch/multi_agent_project_protocol/task0395-residue-path

En un host POSIX esa ruta es **relativa** y el `mkdir(parents=True)` crea un arbol `D:/...` dentro del
directorio de trabajo -- es decir, **el runner volveria a escribir en el arbol donde corre**, que es
literalmente el defecto que esta tarea repara. Hoy no muerde porque `falsification-runners` corre en
`[self-hosted, protocol-win]`, donde la ruta si es absoluta. Tarea aparte, no remediacion de 0395.

**S3 -- el scratch root no se limpia.**
El `finally` borra `probe.parent` y `sandbox`, ambos DENTRO de `scratch_root`, pero nunca
`scratch_root`. Tras cada corrida queda
`D:/Aegis_Scratch/multi_agent_project_protocol/task0395-residue-path/` en disco -- comprobado: existe
ahora mismo, junto a `task0343-behavior`. AGENTS.md seccion 4 pide scratch limpiado al stand-down.
Menor, y comun a los cuatro sitios de S2.

**S4 -- lo que el brazo de 0343 deja de cubrir, dicho en voz alta.**
Con el override, en modo `--task0343-rollback-only` el valor `claims_after_rollback` se sintetiza y se
descarta el que dejo el PowerShell. Ese brazo, por tanto, **ya no ejercita la preservacion del ledger
por parte del rollback**: es una prueba de mutacion sobre la asercion de Python, que es justo lo que
declara su docstring (*"A production-derived ledger-loss mutant must kill every assertion variant"*).
La cobertura a nivel de sistema no se pierde: la misma asercion corre en modo normal leyendo el
`CLAIMS.json` real del sandbox. Lo verifique por comportamiento con C1 -- neutralizar
`ledger_preservation_holds` a `return True` deja el brazo en `baseline=0/3` exit 1. El oraculo esta
vivo. Lo declaro como residuo para que quede en el registro, no como defecto.

**S5 -- argumento muerto.** `run_nul_residue_path_cases(_sandbox)` ya no usa su parametro y la llamada
de la linea 1996 sigue pasando `sandbox`. Cosmetico.

## 6. Recomendacion de cierre

**OK-CLOSABLE** sobre `1988de23`. Sin iteracion de remediacion.

Al cerrar sugiero, sin abrir vuelta:

1. Corregir en el registro la frase de causa raiz (S1) por la version medida: el efecto del estimulo
   anterior sobre la entrada de la asercion era dependiente del entorno.
2. Abrir tarea propia por S2+S3 -- ruta absoluta de instancia cableada en `examples/` y scratch no
   limpiado -- cubriendo los cuatro sitios del fichero, no solo el de 0395.

Sin residuo en el arbol atestiguado por mi parte: mis clones, arms y fixtures viven bajo
`D:/Aegis_Scratch/multi_agent_project_protocol/analista-0395/` (DECISION-0104).

-- Analista, 2026-08-15 22:05 local (UTC+2)
