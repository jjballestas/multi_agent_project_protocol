---
artifact_id: Analista-TASK-0333-tercer-lector-inventario-verdict
task_id: TASK-0333
reviewer: Analista
role: checker
verdict: OK-CLOSABLE
implementation_commit: 303a1d70
protocol_head: 330ef691
created_at: 2026-08-07T17:39:18Z
created_local: 2026-08-07 19:39 (UTC+2)
---

# Veredicto TASK-0333 -- el tercer lector converge, y el inventario aguanta con tres precisiones

**Recomendacion de cierre: OK-CLOSABLE**, con siete residuales declarados. Ninguno reabre la
maquinaria entregada; dos merecen tarea propia y uno ya la tiene abierta.

## Anclaje canonico

| Elemento | Valor |
|---|---|
| Commit de implementacion revisado | `303a1d70` |
| HEAD protocolar al revisar | `330ef691` (== `origin/main`) |
| Rutas gobernadas sucias al arrancar | ninguna |
| Claims activos sobre las rutas | ninguno |
| Clon limpio | `D:/Aegis_Scratch/mapp/rv0333`, detached en `303a1d70`, `git status --short` vacio |

Revise en clon limpio, no en el arbol caliente. Alcance declarado por el Arquitecto: **solo el hub,
sin producto**. Lo respete.

## Gates por exit code, en el clon limpio

| Comando | Exit |
|---|---|
| `python scripts/test_exec_lease_harness.py` | 0 (21/21) |
| `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` | 0 |
| `python scripts/check_falsification_contracts.py --root .` | 0 (48/48) |
| `python scripts/validate_collaboration_state.py --root .` | 0 |
| `python scripts/scan_encoding.py --root .` | 0 |
| `python scripts/scan_domain_neutrality.py --root .` | 0 |

Un aviso honesto sobre el primero: en una primera pasada con los seis gates encadenados,
`test_exec_lease_harness.py` salio **exit 1** en
`test_post_delivery_window_honors_main_progress_extensions`
(`assert live["post_delivery_timeout_fired"] is False`). Aislado y repetido, sale 0. Es una prueba
sensible a la carga de la maquina, no una regresion de 0333 -- no toca ninguna ruta de esta tarea.
Lo dejo como residual R7 porque un gate que se cae bajo carga es un gate que algun dia mentira en CI.

## No confie en los nombres de los tests: banco propio

Extraje verbatim las cinco funciones decodificadoras de `runtime/orchestrator.py` y de su espejo, y
las corri contra repositorios git reales creados por mi, con mis propios payloads. Tambien construi
mis propios mutantes y los aplique **al fichero real** antes de correr el runner enviado.

| Vector | Que probe | Resultado |
|---|---|---|
| V1 (AC1) | Falsacion previa con git real: declarar `work/` | **PASS** -- el lector legacy ve `['work/']`, no-declarados `[]`, el turno **PASA** con 2 ficheros ocultos |
| V2 (AC2) | El lector arreglado sobre el mismo repo | **PASS** -- ve las 3 rutas exactas, las 3 salen no-declaradas, el turno se **RECHAZA** |
| V3 (AC4) | Declaracion exacta de las 3 rutas | **PASS** -- no-declarados `[]`, el turno legitimo sigue pasando |
| V4 (foco D) | Busqueda activa del "acepta mas" | **PASS** -- el legacy **RECHAZABA** una declaracion exacta honesta (`unreported=['work/']`); el arreglo la acepta. La unica direccion de aceptacion nueva es la reparacion de un falso positivo |
| V4b (foco D) | Monotonia de la resta contra baseline | **PASS** -- con `work/` untracked preexistente, el baseline legacy `['work/']` **enmascara** el fichero nuevo (`unreported=[]`); el arreglado `['work/a.md']` lo delata (`unreported=['work/b.md']`). El baseline enmascara estrictamente **menos** |
| V5 (fuga nueva) | Ficheros ignorados, incluso **debajo** del directorio untracked | **SLIP** -- ver R1 |
| V6 (foco B) | Espejo enviado contra el **mismo** repo real | **PASS** -- veredictos identicos en las dos fixtures; ademas las 5 funciones son **byte-identicas** live vs mirror |
| V7 (AC3) | `dirty_tracked_worktree_paths` intacto | **PASS** -- sigue con `--untracked-files=no`, devuelve `[]` con el subarbol untracked presente |

### Matriz de mutacion contra el contrato enviado (AC5, foco E)

Aplique cada mutante **al fichero real del clon** y corri
`run_runtime_turn_obstacle_cases.py` por exit code:

| Mutante | Fichero | Exit del runner |
|---|---|---|
| M0 sin mutar | -- | **0** |
| M1 opcion borrada | `runtime/orchestrator.py` | **1 (muerto)** |
| M2 **CODIGO MUERTO** `[...][:4]` | `runtime/orchestrator.py` | **1 (muerto)** |
| M3 opcion borrada | `examples/full_runtime_instance/runtime/orchestrator.py` | **1 (muerto)** |
| M4 **CODIGO MUERTO** `[...][:4]` | `examples/full_runtime_instance/runtime/orchestrator.py` | **1 (muerto)** |
| M5 barrido de simetria: `--untracked-files=no` -> `all` en el lector tracked-only | `runtime/orchestrator.py` | 0 aqui, pero **1** en `run_runtime_loop_cases.py` |

M2 y M4 son la forma que se escapo en TASK-0324: el literal
`'--untracked-files=all'` **sigue presente en el fuente** (un `grep` o un `assert linea in source`
pasaria) y sin embargo el runtime queda ciego. Mueren los dos, y mueren **tambien en el espejo
enviado** -- el contrato ejerce el mirror contra el repositorio real
(`assert mirror_paths == expected_paths`), no lo compara por texto. Esto es lo que la familia pedia
desde 0324.

M5 responde al foco C con mas de lo que pedia: el AC3 solo exigia **declarar** por que el lector
tracked-only no se toca, y el handoff lo declara (razon: su consumidor decide si un apply fallido
ensucio rutas **preexistentes**). Pero ademas hay dientes: un barrido de convergencia que lo
"arreglara" por simetria pone en rojo `run_runtime_loop_cases.py`, que CI ejecuta en su **propio
paso** (`validate.yml:208`). El AC3 esta cubierto por declaracion **y** por comportamiento.

## Foco A -- el inventario, recorrido por mi y no leido del handoff

Barri el repo entero por mi cuenta (`git grep` sobre `*.py`, `*.ps1`, `*.mjs`, `*.js`, `*.ts`,
`*.sh`), no solo los ficheros que el handoff nombra.

**Confirmo el inventario: los cinco son TODOS los lectores de `git status` que decodifican rutas
operativas**, y los cinco llevan hoy el juego convergido:

| Lector | Opciones verificadas en fuente |
|---|---|
| `runtime/orchestrator.py:680 dirty_worktree_paths` | `--porcelain=v1 -z --untracked-files=all` |
| `runtime/orchestrator.py:692 dirty_tracked_worktree_paths` | `--porcelain=v1 -z --untracked-files=no` (a proposito) |
| `examples/full_runtime_instance/runtime/orchestrator.py:155/167` | el mismo par, byte-identico |
| `scripts/sweep_cron_zombies.py:100 dirty_paths` | `--porcelain=v1 -z --untracked-files=all` |
| `scripts/harness/peer_mailbox_cron.ps1:643 Get-GitStatusPorcelainUtf8` | `--porcelain=v1 -z --untracked-files=all` |

Verifique ademas que el `.ps1` tiene **un unico** punto de entrada a `git status` (`:643`), con dos
consumidores (`:674` residuo, `:706` admision): no hay una segunda invocacion inline que se hubiera
quedado atras.

**Tres precisiones sobre la frontera del handoff.** La frase "todo lo demas es clasificacion de
conectores o sondas de test" no es exhaustiva, y la clase "sonda" si decide cosas:

1. **Falta un llamador tracked que no es ninguna de las dos clases.**
   `personal/Codex/archive/runtime/2026-06-19-monitors/coord_cron.ps1:22` corre
   `git -C $Root status --short`. No es conector ni sonda de test: es un cron archivado. Decodifica
   nada -- solo **cuenta** entradas para una linea de heartbeat -- y esta archivado, asi que no
   siembra la cuarta vez. Pero un inventario que existe para que no aparezca un cuarto no deberia
   dejar una clase entera sin nombrar. Residual R3.

2. **La clase "sonda" si decide algo: el veredicto de una prueba, y esta ciega en la misma forma.**
   Medido: con `work/` ya untracked, inyecte `work/hidden/INJECTED.py` y
   `git status --short` da **exactamente la misma salida antes y despues**. Las aserciones
   de solo-lectura que comparan antes/despues
   (`examples/runtime_observability_cases/run_runtime_observability_cases.py:207-210`,
   `run_runtime_loop_cases.py:241`, `scripts/memory/test_memory_db.py`) pueden por tanto **certificar
   "no toco el arbol" mientras un fichero se escribio**. No es una puerta de gobernanza; es una
   prueba de solo-lectura que puede mentir. Residual R4.

3. **La familia no se cierra con `git status`.** Hay otro decodificador de rutas operativas fuera
   del alcance literal del AC2: `scripts/harness/peer_mailbox_cron.ps1:1086` y `:1251`, con
   `git ls-files --others --exclude-standard -z` (cuarentena y rollback de untracked del exec).
   Lo probe: `ls-files --others` **enumera fichero a fichero** dentro de un directorio untracked
   (`['work/declared_note.md','work/hidden/backdoor.py','work/hidden/deep/more.py']`), asi que **no
   es ciego a este colapso**. No hay cuarto por esta via. Residual R5, informativo.

## R1 -- la fuga que sobrevive al arreglo (medida, no razonada)

`--untracked-files=all` **no muestra ficheros ignorados**, ni siquiera los que cuelgan del propio
directorio untracked. Sobre un repo real con `.gitignore = "*.log\nrt_state/"`:

    en disco:            work/declared_note.md, work/hidden/backdoor.py, work/hidden/deep/more.py,
                         work/hidden/payload.log, rt_state/injected.py
    lector arreglado ve: work/declared_note.md, work/hidden/backdoor.py, work/hidden/deep/more.py
    el turno declara:    esas 3 rutas exactas
    no-declarados:       []            <-- el turno PASA
    ocultos al gate:     work/hidden/payload.log, rt_state/injected.py

El `.gitignore` real de este repo cubre `runtime/runs/`, `runtime/memory/`, `.protocol-tmp/`,
`.agents/`, `secrets/`, `__pycache__/` y `*.env`. Un turno puede escribir ahi sin declararlo y el
gate lo acepta.

Esto **falsifica literalmente** la frase del handoff "the turn gate now sees every file below an
untracked directory": `work/hidden/payload.log` esta debajo del directorio untracked y no se ve.

Lo declaro como **residual, no como bloqueo**: es un mecanismo distinto (reglas de ignore, no
colapso de directorio), el `out_of_scope` de la tarea solo excluia el repo git embebido, y cerrarlo
exige una decision de diseno (los ignorados estan **deliberadamente** fuera de gobernanza; abrirlos
con `--ignored` metria `__pycache__` en cada turno). Merece tarea propia, no una iteracion de 0333.

## R2 -- el conector sanciona la forma ciega

`connectors/git_readonly/connector.py:49` declara
`ALLOWED_FLAGS["status"] = {"--short", "--porcelain", "--branch"}`. Ejecutado:

| Comando | Decision |
|---|---|
| `git status --porcelain=v1 -z --untracked-files=all` | **DENY** (`unsafe_argument`) |
| `git status --porcelain --untracked-files=all` | **DENY** (`unsafe_argument`) |
| `git status --porcelain=v1` | **DENY** (`unsafe_argument`) |
| `git status --porcelain` | ALLOW |
| `git status --short` | ALLOW |

El handoff lo clasifica como "clasificacion de conectores", y es cierto que no decodifica rutas.
Pero **si decide algo**: por el canal sancionado de solo-lectura, la forma convergida es
**inalcanzable**, y las dos unicas formas permitidas son precisamente las ciegas. Hoy no abre
agujero -- los cinco lectores llaman a `subprocess` directamente, sin pasar por el conector -- pero
es la superficie que se exporta, y deja el canal oficial anclado a la forma que esta familia lleva
tres tareas corrigiendo. Residual, no bloqueo.

## R6 -- el cableado en CI existe, pero hoy no puede poner el job en rojo

El contrato esta declarado y cableado: `check_falsification_contracts.py --inventory` lo lista
(`DECLARED NEG-TURN-UNTRACKED-SUBTREE-MUST-BE-DECLARED boundaries=7 runner=...obstacle_cases.py`) y
`validate.yml:283` lo ejecuta. Pero el paso es:

    falsification-runners:
      runs-on: windows-latest          # sin `shell:` -> pwsh
        - name: Execute every previously dormant falsification runner
          run: |
            python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
            python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py     # <-- 2 de 3
            python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py

El runner de 0333 es el **segundo de tres** en un unico bloque PowerShell. Reproduje el envoltorio
exacto de GitHub localmente (`$ErrorActionPreference='stop'` + `exit $LASTEXITCODE`) con un
fallo seguido de un exito: **exit 0**. Es la misma causa que yo misma medi en el CI real de este
repo en TASK-0330 (run 31195169744, job `falsification-runners` en `success` con dos runners rojos
dentro).

Consecuencia exacta para esta tarea: **si el contrato de 0333 se pone rojo y el tercer runner pasa,
CI sale verde**. El contrato nace con dientes reales -- M1..M4 lo demuestran -- pero con la
propagacion amordazada.

No lo convierto en CHANGE-REQUIRED de 0333 por dos razones verificadas: el defecto es de
**TASK-0330** (que creo ese job), y su remediacion 2 ya esta **enrutada** en `b8caf658`, el commit
padre inmediato de esta entrega. Cobrarselo a 0333 seria cobrar dos veces el mismo defecto. Lo que
si dejo escrito, porque el AC5 dice "cableado en CI" y el handoff dice "already CI-wired" sin
matizarlo: **el cierre de 0333 no certifica eficacia en CI hasta que aterrice la remediacion 2 de
TASK-0330.**

## Residuales declarados

| Id | Que es | Severidad | Duenno propuesto |
|---|---|---|---|
| R1 | Las reglas de ignore ocultan ficheros al gate incluso bajo el directorio untracked; falsifica la frase "every file below an untracked directory" del handoff | media | tarea nueva (decision de diseno: que parte de lo ignorado debe ser gobernada) |
| R2 | `connectors/git_readonly` DENIEGA `--untracked-files=all` y `--porcelain=v1`: el canal sancionado solo permite las formas ciegas | media-baja | tarea nueva (superficie exportada) |
| R3 | `personal/Codex/archive/.../coord_cron.ps1:22` es un llamador de `git status` que no cae en ninguna de las dos clases del handoff (solo cuenta, archivado) | baja | precision del inventario |
| R4 | Las sondas de solo-lectura `status --short` antes/despues son ciegas a un fichero inyectado en un directorio ya untracked: pueden certificar "no toque nada" en falso | baja-media | tarea nueva (endurecer las aserciones de solo-lectura) |
| R5 | `peer_mailbox_cron.ps1:1086/:1251` (`ls-files --others`) decodifica rutas operativas y no esta en el inventario; **verificado no ciego** a este colapso, pero comparte la ceguera de R1 | informativo | ampliar el inventario a "decodificadores de rutas", no solo a `git status` |
| R6 | El cableado en CI no puede poner el job en rojo (2 de 3 en un bloque pwsh) | media | **ya abierto**: TASK-0330 remediacion 2, enrutada en `b8caf658` |
| R7 | `test_exec_lease_harness.py` cae bajo carga concurrente (`post_delivery_timeout_fired`); aislado sale 0 | baja | higiene de gates |

## Discrepancia menor de medida

El handoff declara "the tracked JSON turn corpus contains 16 reports". Recontando sobre todo el
arbol rastreado del clon limpio encuentro **15** objetos con `changed_paths`. La afirmacion de fondo
del AC4 si se sostiene y la verifique: hay **exactamente una** declaracion con forma de directorio
(`examples/context_cost_cases/` en `examples/runtime_turn_cases/valid_in_review.json`) y ninguna
lleva un subarbol untracked sucio asociado, luego el replay exacto del corpus anade **0 turnos
rechazados**. El 16 vs 15 no cambia la conclusion; lo anoto porque una cifra en un handoff se cita
despues como si fuera medida.

## Respuesta a tu pregunta

**Si, los cinco son todos los lectores de `git status` que decodifican rutas operativas** -- lo
recorri yo, y los cinco llevan hoy el juego convergido. No hay un sexto lector de `git status`
escondido como sonda.

Pero la respuesta larga es la que importa para que no haya cuarta vez, y son tres cosas:

1. **Si queda algo clasificado como sonda que decide algo**: las aserciones de solo-lectura
   `status --short` antes/despues. Deciden un veredicto de prueba, no un turno, y estan ciegas en
   exactamente esta forma (medido). No es la cuarta aparicion de la raiz en una puerta de
   gobernanza, pero es la misma ceguera certificando que no se toco nada.
2. **El inventario esta trazado sobre el sustantivo equivocado.** Lo que hay que inventariar no es
   "lectores de `git status`" sino "decodificadores de rutas operativas": `ls-files --others` ya
   esta fuera de la lista y hace ese trabajo. Verifique que no es ciego a este colapso, asi que hoy
   no hay cuarto -- pero el inventario no lo cubriria si lo hubiera.
3. **Y la raiz tiene una hermana viva que este arreglo no toca**: las reglas de ignore (R1). Ver
   mas ficheros no es ver todos los ficheros.

Mi recomendacion es cerrar 0333 y abrir R1, R2 y R4 como tareas, redefiniendo el inventario del AC2
por "decodificador de rutas operativas". La familia del **colapso de directorio** queda cerrada; la
familia del **punto ciego del gate** no.

## Recomendacion

**OK-CLOSABLE** sobre `303a1d70`. AC1..AC6 verificados por comportamiento en clon limpio, con los
dos mutantes -- incluido el de codigo muerto -- muertos tanto en el runtime vivo como en el espejo
enviado. Siete residuales declarados, ninguno bloqueante, uno (R6) ya con tarea abierta.

Analista -- checker independiente. No implemente, no promovi, no cerre nada.
