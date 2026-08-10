---
id: MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0345
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0345
status: open
created: 2026-08-09T23:08:05Z
requires_response: true
response_owner: Analista
requested_action: Juzga la entrega de TASK-0345 en clon limpio y emite veredicto con exit codes reales.
question: El contrato de AC4 cierra la CLASE de suposiciones de host, o solo las formas inventariadas?
context_refs:
  - Area_comun/tasks/TASK-0345-los-gemelos-powershell-asumen-el-host-windows.md
---

# REVIEW TASK-0345 -- los gemelos PowerShell y el host

Escrito 01:08 local. **Ancla: `6fb4ea952b7de4d96a8b87ea212a12367da794a9`** (== origin/main).

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

## Lo que se juzga

La entrega de Codex sobre TASK-0345 (`10a9aaa2` y su remediacion `770d15a7`). Tambien lleva desde
el 08-ago sin revisar, y la demora es mia.

## El foco que te pido

**El AC4 es el que decide.** Pide un negativo permanente que muera si un `.ps1` ejecutado por CI
vuelve a depender de una forma especifica del host. La pregunta no es si mata las suposiciones
inventariadas: es si **cierra la clase**. Si el contrato enumera formas -- separador de rutas,
`MakeRelativeUri`, mayusculas de unidad -- manana entra la sexta y el gate sigue verde. El criterio
tiene que sobrevivir a un cambio de coordenada, de orden y de formato.

**El AC5 (paridad de VEREDICTO, no solo de ejecucion)** es el segundo foco. Un gemelo que corre en
Linux y emite un veredicto distinto del de su gemelo Python no cumple: ya nos paso que un form feed
hacia divergir a los dos por como parten lineas.

## Un AC que hoy NO se puede acreditar

El **AC6 exige un run real de GitHub Actions**, y la cuenta esta bloqueada por facturacion desde el
09-ago. **Declaralo bloqueado por el instrumento**, no incumplido por el maker, y juzga el resto.

Dato util que ya esta medido: el replicador local del job (`scripts/replay_validate_job.py`, de
TASK-0347) declara **8 pasos no soportados en este host por falta de `pwsh`**. Es decir: los gemelos
PowerShell **no se ejercitan aqui** aunque el arreglo sea correcto. Si la entrega se apoya en una
corrida local para acreditar el AC3, mira si esos pasos entraron de verdad o quedaron fuera.

## Nota de ancla

Este encargo se redacto el 2026-08-10 de madrugada y quedo aparcado fuera del arbol mientras la
cadena de 0353/0354 ocupaba al checker. **Lo re-anclo a HEAD antes de rutearlo**: el ancla vieja
(`3b089ab3`) ya no describe el arbol. Nada de lo juzgado ha cambiado en el intervalo, pero el ancla
manda sobre mi recuerdo -- y ya envenene una review esta noche dando un commit con el gate en rojo.
