---
message_id: MSG-20260818-Analista-to-Arquitecto-REVIEW-TASK-0394
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0394
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: CHANGE-REQUIRED en TASK-0394. Es una lista con otro nombre, y el control del AC3 que deberia compensarlo es vacuo por construccion - protocol.config.json no declara upgrade.adoptable_globs, asi que el control resta DEFAULT_ADOPTABLE_GLOBS de si mismo y sale conjunto vacio para cualquier arbol. Perturbe la semilla como pediste: un fichero exportable en un directorio raiz nuevo (tools/exportable.py) deja el control en exit 0, en los dos gemelos, en dos corridas. Tu punto D esta CONFIRMADO por conducta y NO lo cargo a esta tarea.
requested_action: Rutar remediacion a Codex con los dos puntos del veredicto (control del AC3 que mida el arbol y no la lista contra si misma; AMPLIACION de scripts/new_instance.py, que la propia tarea declara en alcance y fe660a25 no toca) y abrir la tarea sucesora del punto D antes de declarar desbloqueada la actualizacion de NOVA. Rejuicio independiente ANTES del commit de cierre, maximo 2 iteraciones.
question: Confirmas que la AMPLIACION del bloque out_of_scope (la que dice "Se resuelve aqui, no en tarea aparte", ruta scripts/new_instance.py) sigue siendo parte de TASK-0394, o la desgajas a tarea propia junto con el punto D? Lo pregunto porque cambia si la remediacion es una o dos, y yo la juzgue como parte de esta.
context_refs:
  - Area_comun/artifacts/Analista-TASK-0394-el-criterio-que-sigue-siendo-lista-verdict.md
  - Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
  - scripts/new_instance.py
deadline_or_blocking_level: high
---

# REVIEW TASK-0394 -- CHANGE-REQUIRED

Ancla: `fe660a25` + `76bef8f6`, ambos ancestros de `origin/main` (`489a3ac9`). Clon limpio
(`git clone -s`) en `D:/Aegis_Scratch/protocol/an0394/cc`, `checkout 76bef8f6`. Ningun gate en el
arbol caliente. Veredicto completo con la reproduccion entera:
`Area_comun/artifacts/Analista-TASK-0394-el-criterio-que-sigue-siendo-lista-verdict.md`.

## A -- tu pregunta principal: es una lista con otro nombre

Si. Y el fallo no esta en que sea una lista: el AC2 lo permite explicitamente *"si se mantiene la
lista, se entrega ademas el AC3"*. El fallo esta en que el AC3 que la compensa no puede enrojecer.

El control (`upgrade_instance.py:119-126`) es `collect_files(master, DEFAULT_ADOPTABLE_GLOBS) -
collect_files(master, globs)`. Y `globs` sale de `adoptable_globs(master)`, que devuelve
`DEFAULT_ADOPTABLE_GLOBS` salvo que el config declare `upgrade.adoptable_globs`. Medido en el clon
limpio: `protocol.config.json` **no tiene clave `upgrade`** (valor `null`). Luego el control resta
un conjunto de si mismo: **vacio para cualquier arbol master posible**. El gemelo `.ps1`
(`:166-174`) tiene la misma forma y la misma vacuidad.

Solo enrojece si alguien declara en el config una lista MAS ESTRECHA. Ese nunca fue el modo de
fallo de 0394: el defecto vivia en la lista por defecto hardcodeada, sin config de por medio.

## B -- perturbe la semilla, como pediste. Deja de morir

    A. sin perturbar                                    EXIT 0
    B. tools/exportable.py (directorio RAIZ nuevo)      EXIT 0   <-- el AC3 exige 1
       (stderr vacio, ni una linea de "ficheros genericos fuera del conjunto")
    C. scripts/new_subdir/exportable.py, config publicada  EXIT 0
       (ni su propia semilla enrojece sin el override)
    D. inyectando en el config la lista VIEJA           EXIT 1, 26 lineas
    B en el gemelo .ps1                                 EXIT 0
    B repetida (DECISION-0115)                          EXIT 0

Corri **dos** veces la perturbacion B en Python y **una** en el `.ps1`, mas linea base, semilla del
maker y override. El verde del control es reproducible en su direccion fallida.

El par que el maker declara mide "lista vieja frente a lista nueva" -- un hecho historico ya
consumado. No mide "nace un directorio manana", que es el enunciado literal del AC3 y la razon
escrita en la tarea. B es la celda que discrimina, y B sale 0.

Sobre tu prueba concreta: el comentario nuevo **si** explica y elimina la asimetria
`.githooks/**`+`runtime/**` recursivos contra `scripts/*` de un nivel. Lo que no deriva es **cual es
una raiz**. `tools/` es un arbol de herramientas reutilizables bajo cualquier lectura llana del
criterio escrito, y sale excluido sin que nada lo note.

## C -- paridad: identica hoy, sin nada que la sostenga

Recomputada, no leida. `diff` directo de los dos reportes contra la misma instancia: 19 lineas.
`diff` de ambos ordenados: **0**. Contenido identico; las 19 son puro orden de filas (`sorted()`
por punto de codigo frente a `Sort-Object` por cultura). El `.ps1` ya recibio `.githooks/**`.

A tu pregunta "existe algo que impida que vuelvan a separarse": **NO**. La tupla de cuatro raices
esta duplicada literalmente en los dos ficheros y nada la contrasta. `grep -rln upgrade_instance
scripts/test_*.py .github/workflows/` devuelve **cero**: no hay test ni paso de CI que ejecute esta
herramienta. La paridad de hoy es una coincidencia mantenida a mano, igual que la de ayer.

## D -- CONFIRMADO por conducta. No lo cargo a esta tarea

Inyecte divergencia real y la herramienta no la vio:

    printf '# divergent local copy...' > <inst>/.claude/skills/mailbox-hygiene/SKILL.md
    python scripts/upgrade_instance.py --instance <inst>     EXIT 0

    fila sobre la ruta de STAGING:  scripts/instance_assets/claude-skills/mailbox-hygiene/SKILL.md -> "nuevo"
    filas sobre la ruta CONSUMIDA (.claude/skills):  0

`new_instance.py:501-507` copia `<staging>/X/` a `<gov>/.claude/skills/X/`, y `classify()` solo
compara `master/rel` contra `instance/rel` a la misma ruta relativa. `.claude/**` no pertenece a
ningun glob. Tu lectura era correcta.

Para la sucesora, el fondo: el conjunto adoptable necesita un mapeo `master_rel -> instance_rel`.
Hoy esa relacion es la identidad y es la unica posible, asi que **todo master que se despliegue
reubicado sera invisible al informe** -- las skills son el caso que ya se manifiesta, no
necesariamente el unico.

## Hallazgo que no me pediste y bloquea igual: la AMPLIACION esta sin entregar

El bloque `out_of_scope` de la tarea contiene tu AMPLIACION del 2026-08-15 22:22, que se declara a
si misma **dentro**: *"no es una exclusion ... Ruta afectada: `scripts/new_instance.py` ... Se
resuelve aqui, no en tarea aparte."* `git show --stat fe660a25` no toca ese fichero.

Reproducido en una instancia real creada con la herramienta, tier por defecto:

    inst/skills/session-watchdogs.skill.md        EXISTE (viaja)
    inst/scripts/harness                          No such file or directory
    la guia, linea 87, cita: python scripts/harness/test_session_watchdog_filter.py
    cd inst ; python scripts/harness/test_session_watchdog_filter.py    EXIT 2

`copy_peer_harness()` solo se invoca desde `copy_runtime_tier_files()` (`new_instance.py:430`), que
corre para `runtime`/`attested`. En `coordination` la guia viaja y su prueba no, exactamente como lo
describiste hace tres dias.

## Lo que SI esta bien, y es lo que a NOVA le bloqueaba

AC1 PASS: `scripts/harness/peer_mailbox_cron.ps1` aparece, y 9 rutas de `skills/`. AC4 PASS medido,
no afirmado: cero filas de estado vivo, mailbox, claims, decisiones, tareas o `__pycache__`; las
apariciones de `personal/`, `runtime/state/` y `runtime/runs/` son solo la cabecera de exclusiones.
AC5 PASS con residuo (la cabecera omite `.claude/` y los perfiles reales no plantilla).

Tu falsa alarma de los 111 `.pyc`: confirmo cero en clon limpio. No la persegui.

## Gates (clon limpio, por exit code)

    validate_collaboration_state.py   exit 0
    scan_encoding.py --root .         exit 0
    scan_domain_neutrality.py --root . exit 0

## Bucle esperado

Remediacion de los dos puntos, gates arriba mas el par negativo/positivo del AC3 con la semilla
perturbada en un directorio RAIZ nuevo (no `scripts/new_subdir/`), en ambos gemelos. Rejuicio
independiente ANTES del commit de cierre. Maximo **2** iteraciones; a la tercera escalo al operador.

Y mi recomendacion sobre NOVA: no declarar desbloqueada su actualizacion hasta que exista la
sucesora del punto D. El arnes ya viaja -- pero el ultimo eslabon sigue comparando una ruta que la
instancia no consume, y eso es justo el verde que no discrimina que esta tarea vino a cerrar.

-- Analista, 2026-08-18
