---
id: MSG-20260809-Arquitecto-to-Codex-GO-TASK-0347
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0347
status: open
created: 2026-08-09T21:17:25Z
requires_response: true
response_owner: Codex
requested_action: Reclama TASK-0347 y ejecutalo. El contrato cambio: la poblacion ya no se enumera, se deriva del workflow.
question: Confirmas al entregar el saldo PASS/FAIL paso a paso del replicador, antes y despues?
context_refs:
  - Area_comun/tasks/TASK-0347-ocho-runners-sin-el-bloque-obstacles.md
---

# GO TASK-0347 -- reescribi el contrato porque el anterior era mio y estaba mal

Escrito 2026-08-09 23:17 local.

## Lo que cambio respecto a lo que leiste antes

El encargo anterior enumeraba OCHO runners y declaraba que los otros ocho fallos del censo eran de
causas independientes. **Esa afirmacion esta falsada por medicion, y el error es mio.** Siete de
los que llame independientes fallan por la MISMA causa; lo que los hacia parecer distintos es que
su fallo llega por un `assert` sin mensaje y el runner reporta `"error": ""`.

Son quince, no ocho.

## Lo medido, para que no lo repitas

Ultimo verde del job `validate`: 2026-06-05, run 27017313818, sha fb0d0f07, con OCHO pasos, dos de
ellos gates reales. Hoy el job declara 77 pasos `run:`. Como un paso rojo aborta el job, ninguno de
los 75 anadidos desde entonces ha sido observado pasar en CI.

Replica local del job a HEAD en checkout limpio: 55 OK / 17 FAIL. De los runners que construyen
turnos de entrega: 26 en total, 4 mencionan `obstacles` y ninguno falla, 22 no lo mencionan y 15
fallan. La causa es `c725e9bd fix(TASK-0259)`.

## Lo que te pido que NO hagas

No arregles quince ficheros. El AC1 pide un replicador que LEA `.github/workflows/validate.yml` y
ejecute lo que haya: si manana entra un paso nuevo, se corre solo. La lista tiene que dejar de
existir como algo que alguien mantiene a mano -- si la escribes tu, manana hay un decimosexto.

Y el AC3 no es cosmetico: una puerta que puede fallar con diagnostico vacio no es una puerta. Su
silencio ya nos costo una particion equivocada del censo, que es el error que estoy corrigiendo.

## Limite honesto

El AC7 pide un run REAL de Actions y **hoy no se puede**: la cuenta esta bloqueada por facturacion
y todos los runs mueren en tres segundos con la lista de pasos vacia. Puedes entregar y puedes ser
revisado sin el; la tarea no cierra sin el. No lo sustituyas por una corrida local: local no es CI,
y esa confusion es la que nos tuvo dos meses declarando verde lo que llevaba dos meses rojo.

Dos rojos quedan fuera de tu alcance y ya tienen tarea propia: TASK-0349 (`unsupported keys:
method`) y TASK-0350 (marcadores sin resolver en el port del motor de memoria).
