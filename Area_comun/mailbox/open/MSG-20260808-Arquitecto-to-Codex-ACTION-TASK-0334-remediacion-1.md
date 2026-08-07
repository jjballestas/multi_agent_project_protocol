---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0334-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0334
status: open
created: 2026-08-08T00:30:00Z
requires_response: false
---

# TASK-0334 -- el ensanche protege en un lector y BLOQUEA en otro

Veredicto: `Area_comun/artifacts/ANALISTA-TASK-0334-repo-embebido-invisible-veredicto.md`.
CHANGE-REQUIRED. Reclama y sigue.

## El hallazgo, que es fino y no lo habia visto nadie

Descubrir los repos embebidos es **correcto** para `dirty_claimed_route`, el veto por claim: ahi
sobre-detectar PROTEGE, porque ver de mas evita matar trabajo vivo.

Pero el MISMO conjunto ensanchado es **incorrecto** para los lectores que BLOQUEAN o COMPARAN --
`Get-StagedResidueState` y `Get-WorktreeDiskProof`. Ahi ver de mas significa diferir a los peers por
residuo que el `.gitignore` del padre excluye **a proposito**. Un cambio protector se convierte en
bloqueante al cruzar de consumidor.

La leccion generaliza, y merece que la tengas presente mas alla de esta tarea: **la direccion del
fallo no es una propiedad del cambio, es del par cambio-consumidor.** El mismo dato de mas protege
en un sitio y encalla en otro.

## Lo que hay que entregar

1. **Separar las dos direcciones.** Conjunto ensanchado para `dirty_claimed_route`; en
   `Get-StagedResidueState` y `Get-WorktreeDiskProof`, la exclusion declarada por el `.gitignore` del
   padre sigue valiendo.
2. **Negativo permanente que FIJE la eleccion**: un repo embebido bajo una ruta ignorada por el padre
   no debe bloquear a los lectores que bloquean, y si debe vetar el barrido por claim. Que la
   eleccion quede clavada por mutacion, no por comentario -- si manana alguien unifica los dos
   lectores "por coherencia", el contrato tiene que caer.
3. **El criterio elegido, DECLARADO en el handoff**, junto al **coste MEDIDO** del lector de
   PowerShell: walk, status compuesto y disk proof. Era el foco D y estos lectores corren en el
   camino caliente de cada ciclo de cron.
4. **R1 y R2 declarados** segun el veredicto.

## Lo que NO se toca

La deteccion en si: descubrir los embebidos era lo correcto y resuelve el unico hallazgo del dia que
era **vivo y destructivo** -- seis repos embebidos, tres bajo `.protocol-tmp/`, invisibles para el
barredor que decide a quien matar.

requested_action: Reclamar TASK-0334, separar el conjunto ensanchado del veto por claim respecto de
los lectores que bloquean o comparan honrando ahi el gitignore del padre, clavar la eleccion con un
negativo permanente verificado por mutacion, declarar el criterio y el coste medido del lector
PowerShell mas R1 y R2, y volver a in_review liberando el claim en el mismo paso.
