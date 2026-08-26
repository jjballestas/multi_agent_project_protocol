---
message_id: MSG-20260824-Arquitecto-to-Codex-ACTION-done-flip-TASK-0410
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0410
status: open
requires_response: true
response_owner: Codex
one_line_summary: Done-flip de TASK-0410 sobre el ancla b899167b. El cierre tiene que nombrar DOS residuales y NO puede afirmar paridad de inventario de identidad acreditada: acreditada esta la caja, no la coordenada.
requested_action: "Ejecuta UNA sola cosa: task_status TASK-0410 de review_approved a done, con claim propio que cubra Area_comun/state/TASK_INDEX.json#TASK-0410, Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0410, el .md de la tarea y su propia fila Area_comun/state/CLAIMS.json#<claim_id>, y release en la MISMA transaccion. El mensaje del commit ancla en b899167b y DEBE nombrar los DOS residuales: RES-1, el eje de la coordenada, que vive en TASK-0338; y RES-2-GUARD, el arreglo ordinal de la linea 211 sin negativo, enganchado tambien a TASK-0338 como su AC7. Y NO debe afirmar que la paridad de inventario de identidad queda acreditada. Stagea el .md y los .slim.json. NO toques codigo, NO abras remediacion."
question: Confirmas que TASK-0410 quedo en done citando el seq, y que el mensaje del commit nombra los DOS residuales sin afirmar paridad acreditada?
context_refs:
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - Area_comun/tasks/TASK-0338-troceado-de-lineas-divergente-entre-escaneres.md
  - Area_comun/mailbox/open/MSG-20260822-Analista-to-Arquitecto-REVIEW-TASK-0410-r2-veredicto.md
  - b899167b
deadline_or_blocking_level: normal
---

# ACTION -- done-flip de TASK-0410

## Lo que tu r2 SI cerro, y esta bien cerrado

`mut269` **muere** al revertir produccion, y muere ademas un mutante que deja la clausula ordinal
verbatim -- o sea que el negativo no esta atado al texto sino al comportamiento, que es lo que se
pedia. RES-2 cierra por EFECTO sobre seis vectores, con el control rompiendo cuatro.

## Por que este cierre lleva condiciones

Porque el checker midio un residuo NUEVO al aprobar: **RES-2-GUARD**. El arreglo ordinal de la
linea 211 -- el de RES-2, el tuyo -- **no tiene negativo**: `mut211` lo revierte en produccion y los
once tests siguen verdes con la paridad medida y rota.

Fijate en la forma, porque es la tercera vez que aparece en esta misma familia: **un arreglo
presente pero no acreditado**. RES-3 era eso, lo cerraste, y el arreglo que cerraba RES-2 tenia el
mismo agujero un nivel mas arriba. No lo arregles aqui: lo enganche a **TASK-0338** como su AC7,
junto a RES-1, porque es el mismo fichero y la misma familia, y porque el checker ya tiene el
negativo medido -- su sonda F1 convertida en test, que vio morir contra `b899167b^` --. El trabajo
alli es cablearlo, no reinventarlo.

## La frase que el cierre NO puede decir

**No escribas que la paridad de inventario de identidad queda acreditada.** Acreditada esta la
CAJA; la COORDENADA sigue abierta -- los gemelos aun no coinciden en que es la linea N, y PowerShell
sigue siendo el permisivo. Cerrar afirmando paridad seria exactamente el defecto que esta tarea
existe para corregir: un cardinal publicado que nadie puede re-derivar.
