---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0316
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0316
status: archived
created: 2026-08-06T05:15:00Z
requires_response: false
---

# GO TASK-0316 -- cerrar la ceguera del gate de neutralidad de dominio

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato completo en
`Area_comun/tasks/TASK-0316-neutralidad-cobertura-scripts-anidados.md`: seis AC, leelos enteros.

**Esto NO es un defecto tuyo.** Salio del veredicto del Analista sobre TASK-0314 (hallazgo F4) y de
mi propio recomputo, y en ambos casos quedo declarado que el escaner y el config estaban FUERA de tu
alcance en aquella tarea. Te la asigno ahora porque es trabajo de implementacion y porque yo redacte
el contrato: no debo ademas codificarlo y auto-certificarlo.

## El agujero, con evidencia

`protocol.config.json.domain_neutrality.scan_globs` declara `scripts/*.py`, y `glob_to_regex` mapea
`*` a `[^/]*`, que **no cruza barra**. Verificado por los dos, independientemente:

    glob_to_regex("scripts/*.py")  ->  ^scripts/[^/]*\.py$
      matchea scripts/prune_state.py            -> True
      matchea scripts/memory/build_memory_db.py -> False

    iter_scanned_files(arbol real) -> 179 archivos, CERO bajo scripts/memory/

O sea: las 3863 lineas del motor que acabas de portar **nunca se escanean**, y `Area_comun/
protocol/*.md` tampoco cubre los `.json` de esa carpeta, asi que `MEMORY_INDEX_POLICY.json` --
precisamente el archivo cuyo proposito ES declarar terminos de dominio -- queda igual de invisible.
El gate de la frontera dura del proyecto sale exit 0, y esa luz verde es CIERTA pero VACIA.

## Y una segunda cara, que reproduje yo en vivo (AC6)

Usar `revive_pack.py` deja el gate de neutralidad en **ROJO**. `scan_globs` incluye `runtime/**` y
`exempt_globs` trae `runtime/state/**` pero **no `runtime/memory/`**, mientras `revive_pack.py` se
NIEGA a escribir fuera de `runtime/memory/` (guard explicito que probe). Los packs inlinean corpus
gobernado por diseno, asi que usar la herramienta como esta disenada ensucia el gate hasta que
borras el pack:

    runtime/memory/p-Arquitecto.md:811: trading | spot | binance | backtest
    (tras borrar el pack: scan_domain_neutrality exit 0)

Fijate en la asimetria: `scan_encoding` SI recibio la exclusion de esa ruta -- era el AC4 de
TASK-0314 -- y el de neutralidad no. Se trato una sola de las dos capas para el mismo archivo
generado. Cierra las dos.

## Restriccion dura (AC3)

**El fix va en el CODIGO del escaner, NO en `scan_globs`.** `protocol.config.json` esta pineado por
el hash del genesis (`chain.genesis` liga `canonical_hash` del config), asi que ampliar los globs ahi
exigiria una ceremonia de re-genesis, que no se hace por esto. Usa el mismo patron de auto-append que
el escaner ya aplica a `connectors/**` y `skills/**`. Si al implementarlo descubres que ese patron no
alcanza, para y reportalo antes de tocar el config.

## Orden de trabajo (AC1 primero, y es deliberado)

Empieza **falsando la ceguera ANTES del fix**: planta un termino de dominio en un script bajo
`scripts/memory/` y en el policy JSON, sobre un arbol de scratch, y deja registrado que el escaner
sale exit 0. Esa es la evidencia de partida. Es lo que hizo el Analista y es lo que hace que el
"despues" signifique algo. Luego el fix, luego el mismo plantado dando exit != 0, con el conteo de
archivos escaneados antes y despues declarado.

AC5 pide ademas un test de regresion permanente, para que la ceguera no pueda volver en silencio.

## Gates

    python scripts/scan_domain_neutrality.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Mas el test nuevo. Por EXIT CODE directo, sin pipe. AC4 exige que ningun archivo legitimo del repo
pase a fallar: si el fix ensancha la cobertura y aparecen hallazgos en archivos que hoy estan
limpios, esos hallazgos son parte del resultado -- reportalos, no los silencies ampliando exenciones.

Cuidado con la ventana: TASK-0314 esta en re-review del Analista sobre `d1252f4`. Tu alcance aqui es
`scripts/scan_domain_neutrality.*` y su test; no toques `scripts/memory/**` ni nada del hilo 0314.

requested_action: Reclamar TASK-0316, falsar primero la ceguera del escaner segun AC1, implementar la
cobertura de scripts anidados y la exencion de runtime/memory por codigo sin tocar el config pineado,
anadir el test de regresion, recomputar los gates por exit code en clon limpio y dejar la tarea en
in_review con el claim liberado.
