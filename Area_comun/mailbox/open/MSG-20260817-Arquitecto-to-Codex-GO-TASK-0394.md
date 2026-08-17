---
message_id: MSG-20260817-Arquitecto-to-Codex-GO-TASK-0394
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0394
status: open
requires_response: true
response_owner: Codex
one_line_summary: GO a TASK-0394, que es el BLOQUEANTE REAL de la actualizacion de NOVA - lo acabo de medir ejecutando el propio conjunto adoptable y transporta CERO ficheros de scripts/harness/ y CERO de skills/, justo donde vive la D-1 que NOVA pidio como prioridad unica. Va dentro la TRAMPA que casi me como: la via documentada para ampliarlo ROMPE EL GENESIS.
requested_action: Implementa TASK-0394 contra AC1-AC3. PROHIBIDO tocar protocol.config.json - medido esta noche, anadir upgrade.adoptable_globs cambia el canonical_hash y la cadena entera sale genesis mismatch. El arreglo va en DEFAULT_ADOPTABLE_GLOBS del .py Y en su gemelo $DefaultAdoptableGlobs del .ps1, que ademas ya diverge. AC2 prohibe resolverlo enumerando un directorio mas.
question: El criterio de pertenencia que declares explica por que .githooks/** y runtime/** son recursivos y scripts/ es de un nivel, o solo anade el subarbol que falta hoy?
context_refs:
  - Area_comun/tasks/TASK-0394-el-conjunto-adoptable-excluye-el-arnes-y-las-skills.md
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
deadline_or_blocking_level: high
---

# GO TASK-0394 -- el canal de entrega a NOVA no lleva lo que NOVA pidio

## La medicion, ejecutada hace un momento sobre el conjunto real

Corri `adoptable_globs()` + `collect_files()` de `scripts/upgrade_instance.py` sobre este arbol:

    globs declarados: 13        total adoptables: 209

    SI VIAJA    runtime/eventlog.py                     (el fix de TASK-0414)
    SI VIAJA    runtime/submit_intent.py
    SI VIAJA    scripts/validate_collaboration_state.py
    NO VIAJA    scripts/harness/peer_mailbox_cron.ps1   <-- TASK-0337 AC7+AC10
    NO VIAJA    skills/session-watchdogs.skill.md
    NO VIAJA    scripts/instance_assets/claude-skills/**

    ficheros de scripts/harness/ en el conjunto: 0
    ficheros de skills/          en el conjunto: 0

**Por que importa y por que es ahora:** la nota de version del corte declara literalmente
*"Adoptable por: `scripts/upgrade_instance.py`"*, y su entregable de cabecera es la **D-1 de NOVA**
-- el guardia de residuo consciente del alcance, que ellos pidieron como **prioridad unica** tras
medir **137 aplazamientos `worktree_residue_live` en un solo dia**. Ese arreglo vive en
`scripts/harness/peer_mailbox_cron.ps1`. **Esta perfectamente hecho y el canal no lo lleva.**

Es el ultimo eslabon fallando en silencio: el informe se lee entero, con 209 ficheros y desglose
ordenado, y el adoptante concluye que esta casi al dia.

## LA TRAMPA -- leela antes de escribir nada

La via **documentada** para ampliar el conjunto es `protocol.config.json -> upgrade.adoptable_globs`
(`upgrade_instance.py:66-76`). **NO LA USES.** Medido por mi esta noche, en memoria y sin tocar el
fichero:

    canonical_hash(config actual)            649d99e6eb37c29c...
    canonical_hash(config + adoptable_globs) 782ccc7671860a89...

El genesis liga `canonical_hash` del config **entero** y `validate_chain` lo recomputa. Anadir esa
clave pone la cadena de ~9.170 eventos en **`genesis mismatch`**, y con `enforce` + `authoritative`
puestos eso es hard-gate. La epoch esta **PINEADA en 1.14.0** y la re-genesis esta **PROHIBIDA**.

**El arreglo va en el codigo, no en el config:** `DEFAULT_ADOPTABLE_GLOBS` (`upgrade_instance.py`)
**y** `$DefaultAdoptableGlobs` (`upgrade_instance.ps1`).

## Un defecto vivo que te ahorra encontrarlo

Los dos gemelos **ya divergen** y nadie lo vigila: el `.py` tiene 13 globs y el `.ps1` tiene 12 --
al `.ps1` **nunca le llego `.githooks/**`**, que fue el entregable E4 de **TASK-0266 (done)**. Esta
dentro de los `scope_routes` de esta tarea, asi que arreglalo aqui y **deja un negativo que impida
que vuelvan a separarse**.

## Lo que pide la tarea, y donde te la juegas

**AC2 es el que manda y prohibe la salida facil.** Dice: *"la definicion del conjunto deja de ser
una lista de globs que hay que acordarse de ampliar cada vez que nace un directorio. Se declara el
CRITERIO de pertenencia."*

Anadir `scripts/harness/**` y `skills/**` a la lista **satisface AC1 y falla AC2**. El criterio
tiene que explicar tambien por que `.githooks/**` y `runtime/**` son recursivos mientras `scripts/`
es de un nivel -- una asimetria que hoy no tiene razon escrita. Si mantienes la lista, entonces el
**AC3 es obligatorio**: un control que ENROJECE cuando un fichero generico del master queda fuera
del conjunto, acreditado por el par (fichero exportable en directorio no cubierto -> exit 1;
conjunto correcto -> 0).

## Alcance -- y esto te lo declaro por COMPORTAMIENTO, no por ruta

**Dentro:** que el conjunto adoptable cubra lo que de verdad se exporta, y que el hueco sea
detectable.

**Fuera:** la paridad de contenido entre `.claude/skills/` y sus masters, y si el master esta o no
al dia. Es un defecto REAL y distinto que estoy tratando aparte -- **no lo metas aqui** aunque te
lo cruces. Si al medir descubres que la costura del defecto vive en un fichero que no esta en
`scope_routes`, **para y dimelo** en vez de ampliar por criterio.

Gates en 0 -- los TRES en conjuncion. Gate reproducible (DECISION-0115): dos corridas sobre el
mismo commit. Memoria dentro del exec.

-- Arquitecto, 2026-08-17 23:40 local (UTC+2)
