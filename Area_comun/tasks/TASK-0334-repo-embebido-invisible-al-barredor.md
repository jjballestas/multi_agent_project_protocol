---
task_id: TASK-0334
file: Area_comun/tasks/TASK-0334-repo-embebido-invisible-al-barredor.md
title: "git status no desciende a un repo git EMBEBIDO con ninguna opcion: el barredor ve limpio un directorio con trabajo vivo y lo mata -- y esa forma existe HOY en el hub"
status: in_review
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0326
  - TASK-0323
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    Residual R2 del veredicto de TASK-0326, medido por el checker, y **existe en el arbol vivo hoy**.
    El checker cito `personal/Codex/task0294_runtime/`; al inventariar encontre que **son SEIS**, y
    tres de ellos estan en el camino CALIENTE del harness:
    `.protocol-tmp/task0267-speed/79507b2b-.../`, `.protocol-tmp/zc/`, `.protocol-tmp/zc-proto/`,
    `personal/Codex/task0294_attested/`, `personal/Codex/task0294_generated_sample/` y
    `personal/Codex/task0294_runtime/`. `.protocol-tmp/` es donde viven el estado de los crons y las
    leases de exec, es decir justo lo que el barredor consulta.
    `git status` NO desciende a un repo embebido, y **ninguna opcion lo arregla**. Falsado:
    con `work/inner` como repo anidado y `work/inner/live_work.md` sin commitear,
    `status --porcelain=v1 -z` da `['?? work/']`; anadiendo `--untracked-files=all` da
    `['?? work/inner/']` -- baja UN nivel y para; anadiendo ademas `--ignored`, igual.
    Consecuencia medida con el lector YA ARREGLADO de TASK-0326:
    `dirty_claimed_route(root, owner)` devuelve **False** para un claim acotado a
    `work/inner/live_work.md`. `False` significa que el barredor de zombis **mata el trabajo vivo**.
    No es un defecto del arreglo de 0326 ni se corrige con opciones: exige otro mecanismo --
    interrogar cada repo embebido por separado y componer el resultado.
  acceptance:
    - "AC1 (falsacion previa): se reproduce con git real que ninguna combinacion de opciones de git status desciende a un repo embebido, y que dirty_claimed_route devuelve False para un claim a un fichero vivo dentro de el. Se declara la lista de opciones probadas."
    - "AC2 (el mecanismo nuevo): los lectores detectan los repos embebidos bajo la raiz y los interrogan por separado, componiendo rutas relativas a la raiz del hub. Se declara el criterio de deteccion y su coste."
    - "AC3 (los casos REALES del hub, en plural): se inventarian TODOS los repos embebidos bajo la raiz -- hoy son seis, tres de ellos bajo .protocol-tmp/ -- y se demuestra sobre al menos uno de personal/ y uno de .protocol-tmp/ que un claim a un fichero suyo VETA la terminacion. No vale cerrarla solo con el fixture sintetico ni con un unico caso."
    - "AC4 (direccion del fallo, explicita): hoy el barredor MATA trabajo vivo por no verlo. Tras el arreglo debe VETAR ante la duda. Si la deteccion de repos embebidos falla o es ambigua, el comportamiento es NO MATAR -- fail-closed, nunca al reves."
    - "AC5 (limite declarado): se declara hasta que profundidad de anidamiento se cubre y que pasa mas alla. Un mecanismo que solo baja un nivel mas que git deja la misma familia abierta un escalon mas arriba; si se acota, se dice."
    - "AC6 (contrato POR COMPORTAMIENTO): negativo permanente con un repo embebido real que exija que el claim vete la terminacion, verificado por mutacion y cableado en CI."
    - "AC7 (sin regresion): suites del harness y gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/sweep_cron_zombies.py
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    No se toca la convergencia de opciones de TASK-0326, que es correcta y suficiente para lo suyo.
    No entra el tercer lector de `runtime/orchestrator.py` (va en su propia tarea). No se BORRA ni se
    reubica `personal/Codex/task0294_runtime/`: mover el sintoma no arregla el mecanismo, y ademas es
    area personal de otro owner.
  risk: high
  estimate: M
---

# TASK-0334 -- lo que git no mira, el barredor no ve, y lo que no ve lo mata

## Lo medido (checker, veredicto de TASK-0326)

    fixture: work/inner es un repo git anidado con work/inner/live_work.md sin commitear
    claim:   work/inner/live_work.md

    status --porcelain=v1 -z                          -> ['?? work/']
    status --porcelain=v1 -z --untracked-files=all    -> ['?? work/inner/']   <-- baja UN nivel
    status ... --untracked-files=all --ignored        -> ['?? work/inner/']   <-- tampoco

    dirty_claimed_route(root, owner)  con el lector ARREGLADO  ->  False

## Por que es distinto de todo lo demas de esta familia

0323, 0326 y 0333 son defectos NUESTROS: parseabamos mal o preguntabamos mal. Este no. Aqui
preguntamos bien y **git contesta lo que puede contestar**: un repo embebido es opaco para el
`status` del repo padre por diseno. No hay opcion que lo arregle, asi que no es un fix de una linea
sino un mecanismo nuevo.

## Y no es teorico: la forma existe hoy

`personal/Codex/task0294_runtime/` tiene su propio `.git`. Es exactamente la fila `False/False` de la
tabla del checker. Es decir: hoy mismo, si un claim cubriera un fichero vivo ahi dentro, el barredor
lo veria limpio y mataria el trabajo.

Por eso el AC3 exige cerrar con el caso REAL del hub y no solo con el fixture sintetico: un
mecanismo que funciona en el laboratorio y no en el arbol donde se descubrio el problema no ha
cerrado nada.

## AC4 es la linea que no se cruza

Hoy el fallo es **destructivo**: no es que se pierda una deteccion, es que se mata trabajo vivo. El
arreglo tiene que dejar el sistema vetando ante la duda. Si la deteccion de repos embebidos falla,
es ambigua o se queda sin presupuesto, el comportamiento correcto es **no matar**.

## Riesgo declarado (high)

Escanear repos embebidos tiene coste por invocacion de git; medirlo y declararlo, porque estos
lectores corren en el camino caliente de cada ciclo de cron. Riesgo mayor: una deteccion
incompleta que haga creer que la familia esta cerrada. Por eso el AC5 exige declarar el limite
de profundidad en vez de dejarlo implicito.

## Remediation iteration 1 - consumer-specific safety direction

The expanded embedded-repository set remains available to the destructive claim-veto path, where
over-detection prevents termination. `Get-StagedResidueState` and `Get-WorktreeDiskProof` use the
parent repository view, so paths deliberately excluded by the parent's `.gitignore` do not create
exec deferrals or rollback-drift comparisons.

`NEG-HARNESS-PARENT-IGNORE-BOUNDARY` fixes both sides by behavior: an uncommitted file inside an
embedded repository below a parent-ignored route still makes the file-scoped claim veto true, while
the blocking residue reader remains `none` and the disk proof excludes that path. A mutant that
feeds the expanded set into both blocking readers makes residue `live` and adds the ignored path to
the proof.

Known limits remain explicit:

- R1: a live file ignored by the embedded repository's own `.gitignore` remains invisible to Git
  status and can therefore escape the claim veto. This pre-existing family is not closed here.
- R2: a partial or empty `.git` marker can resolve status against the parent and generate prefixed
  phantom routes. The direction remains fail-safe for termination but may over-detect.
