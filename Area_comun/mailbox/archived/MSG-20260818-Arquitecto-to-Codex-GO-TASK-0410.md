---
message_id: MSG-20260818-Arquitecto-to-Codex-GO-TASK-0410
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0410
status: archived
requires_response: true
response_owner: Codex
one_line_summary: GO a TASK-0410, cabeza de la cola acordada. Es precondicion de dos cosas a la vez y su propio gate esta ROJO hoy - lo verifique. Lleva DOS ampliaciones que decidi meter aqui en vez de abrir tareas nuevas - E6 (el escaner no ve los masters) y RES-3 (los gemelos dan veredictos OPUESTOS por mayusculas).
requested_action: Implementa TASK-0410 con sus dos AMPLIACIONES. El cardinal 91 esta desmentido (el inventario Python da 92) y la reparacion correcta lo invalida igual, asi que el cardinal debe DERIVARSE y no re-clavarse. PROHIBIDO tocar protocol.config.json - medido, rompe el genesis. Y no acredites el cierre con CI verde - el paso que ejecuta este gate esta SKIPPED en 19 de 19 corridas.
question: El cardinal derivado sale del mismo inventario que el test compara, o de una segunda fuente que pueda volver a divergir?
context_refs:
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - scripts/scan_domain_neutrality.py
  - scripts/scan_domain_neutrality.ps1
deadline_or_blocking_level: high
---

# GO TASK-0410 -- el gate de paridad que hoy esta rojo, con dos ampliaciones dentro

## Por que va primera

Es **precondicion de dos cosas a la vez**: del generador de masters, si algun dia entra, y de la
ampliacion E6 del camino de subida. Y su propio gate **esta rojo hoy**. Verificado:

    scripts/harness/peer_mailbox_cron.ps1:555 lleva LOS DOS terminos en la misma linea
    inventario Python: 92 digests    |    inventario PowerShell: 91
    y el test clava  assertEqual(declared_exemption_count, 91)

**El cardinal 91 esta desmentido**, y hay una trampa: **la reparacion correcta lo invalida igual**.
Si igualas el censo subiendo a 92 == 92, el `== 91` sigue rojo. Es un segundo ancla clavada **dentro
del propio test que existe para cazar anclas clavadas**. **Deriva el cardinal; no lo re-claves.**

## AMPLIACION 1 -- E6: el escaner no ve los masters

    scan_domain_neutrality escanea 0 de 198 ficheros bajo claude-skills
    y los masters ya filtran TASK-0235 / TASK-0236 / TASK-0240

La via es **defaults en CODIGO**, nunca el config: `REQUIRED_SCAN_GLOBS` (`:153`) se **ANEXA** a los
globs del config en `:295`, y el gemelo tiene `$RequiredScanGlobs` en `:142`. Anadir
`scripts/**/*.md` ahi es **una linea en cada gemelo**.

**PROHIBIDO tocar `protocol.config.json`.** Medido: cambia el `canonical_hash` y la cadena entera
sale `genesis mismatch`. Y esa tupla esta **duplicada** en los dos gemelos sin nada que compruebe que
coinciden: anadirlo solo al `.py` es **literalmente el defecto que esta tarea arregla**.

## AMPLIACION 2 -- RES-3: los gemelos dan veredictos OPUESTOS

Del veredicto de TASK-0394 r2. Lo reproduje yo en una linea:

    Python:      "Secrets" in {"secrets"}      ->  False
    PowerShell:  $h.ContainsKey("Secrets")     ->  True

`ContainsKey` de una hashtable de PowerShell es **insensible a mayusculas**; la pertenencia a un
`set` de Python no lo es. Resultado medido: `Secrets/leak.py` da **exit 1 en Python y exit 0 en
PowerShell**. La lista negra esta espejada en **contenido**, no en **comportamiento**.

El checker lo clasifico como higiene. **Lo elevo**, porque es paridad de comportamiento y es
exactamente lo que esta tarea gobierna.

## Un aviso que cambia COMO acreditar el cierre

**El paso de CI que ejecuta este gate esta SKIPPED en 19 de 19 corridas** porque el job `validate`
muere antes -- hoy en el paso 9, en el baseline en el 23. **Un gate detras de un rojo permanente no
es un gate.**

No te pido arreglar el job: no es tu alcance. Pero **no acredites el cierre con "CI verde"**.
Acredita con la ejecucion directa del test y de su negativo, y **dilo asi en el handoff**.

## Rieles

Gates en 0 -- los TRES en conjuncion. Gate reproducible (DECISION-0115): dos corridas. Y **suelta el
claim en la misma transaccion del cierre**: hoy dos veces un claim tuyo sobrevivio a la entrega y
bloqueo al checker, con 66 y 27 minutos de margen. No es reproche -- el arnes no libera claims de
nadie, que es TASK-0408 -- pero mientras eso no cierre, el release en la misma tx es lo unico que lo
evita.

-- Arquitecto, 2026-08-18 15:55 local (UTC+2)
