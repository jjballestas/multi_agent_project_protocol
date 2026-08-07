---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0326
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0326
status: archived
created: 2026-08-07T03:44:00Z
requires_response: false
---

# GO TASK-0326 -- convergencia de los dos lectores: --untracked-files=all

Ready, owner tuyo, reviewer Analista. GO del operador. Contrato:
`Area_comun/tasks/TASK-0326-convergencia-untracked-files-lectores.md` (cinco AC).

**Sin precondiciones. Tomala cuando te venga.**

## Es la otra mitad del problema

0319, 0321 y 0323 arreglaron el **PARSEO** de lo que git dice. Esta es de **OPCIONES**: no basta con
leer bien la respuesta si no se hace bien la pregunta.

`sweep_cron_zombies.dirty_paths` no pasa `--untracked-files=all`. Sin esa opcion git **colapsa un
directorio sin rastrear en una sola entrada de directorio**, asi que un claim acotado a un FICHERO
dentro de el no casa nunca y el barredor decide sobre un mapa incompleto. Y el mismo desajuste existe
entre el barredor de Python y el helper de PowerShell, que no interrogan a git con las mismas
opciones.

Va agrupado en una sola tarea por recomendacion del propio checker, y la comparto: misma raiz, dos
lectores, y revisarlos por separado invita a que converjan a medias.

## AC3, la vigilancia en la otra direccion

Anadir `--untracked-files=all` **ensancha** el conjunto observado. Verifica que eso no rompe el
guard de residuo ni hace que el barredor mate lo que no debe. Si aparece un efecto colateral,
declaralo y acotalo en vez de absorberlo en silencio: ensanchar de mas tiene su propio coste, y
llevamos toda la noche viendo que los arreglos mueven el problema de lado si no se miran las dos
caras.

**AC2:** los dos lectores acaban con el MISMO juego de opciones, y el handoff declara cual es y por
que cada opcion esta.

requested_action: Reclamar TASK-0326, flipearla a in_progress, falsar el caso del directorio
colapsado con git real, converger las opciones de los dos lectores, verificar que el ensanche no
rompe el guard ni el barrido, declarar el negativo y cablearlo, recomputar los gates por exit code en
clon limpio y dejar la tarea en in_review con el claim liberado.
