---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0322
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0322
status: archived
created: 2026-08-06T19:50:00Z
requires_response: false
---

# GO TASK-0322 -- estrechar DATE_RE con validacion de rangos

Ready en el index, owner tuyo, reviewer Analista. GO del operador 2026-08-06. Contrato:
`Area_comun/tasks/TASK-0322-date-re-rangos-portadores.md` (seis AC).

**SECUENCIA: la ULTIMA de las tres de `scripts/memory/`.** Primero TASK-0321 (harness, en curso),
luego TASK-0317 r2 (fija la COLOCACION de la exencion, que esta tarea no debe violar), y despues
esta. TASK-0320 puede ir antes o despues de esta; no se rozan.

## Por que

TASK-0317 anclo la exencion del heuristico de telefono en `DATE_RE`, que fue la decision correcta y
esta cerrada. Pero `DATE_RE` no valida RANGOS: acepta meses, dias, horas o minutos fuera de dominio.
Y toda cadena que la gramatica acepta queda **exenta** del chequeo de telefono.

El checker lo midio: estrechar con validacion de rangos baja la poblacion de cadenas **portadoras**
-- las que pasan `DATE_RE` y por tanto podrian transportar algo -- del **2,9 por ciento al 0,05 por
ciento**. No es cerrar un agujero conocido: es reducir en casi dos ordenes de magnitud el conjunto
sobre el que hay que confiar.

## Que se pide

Rangos reales: mes 01-12, dia 01-31, hora 00-23, minuto y segundo 00-59, offset con horas 00-14.
**Sin dejar de aceptar ningun formato legitimo.**

**AC1 y AC5 son el corazon:** reproduce la cifra de partida (2,9 por ciento) declarando el metodo, y
declara la de llegada. El objetivo es el 0,05 por ciento que midio el checker; si no se alcanza,
explica por que. Una tarea cuyo exito es un numero tiene que traer el numero medido, no la
sensacion.

**AC3, la trampa a evitar:** los valores de `created_at`/`updated_at`/`closed_at` del corpus real que
hoy se aceptan tienen que seguir aceptandose, medido en **CLON LIMPIO**. Cero warnings nuevos de
claves de fecha. Estrechar de mas rompe lo que 0317 arreglo.

**AC4:** los 11 vectores de cola del veredicto de 0314 siguen rechazados. F2 no se reabre.

## Gates

    python scripts/memory/test_memory_db.py
    python scripts/memory/build_memory_db.py --root .

Por EXIT CODE directo, sin pipe, y las cifras en CLON LIMPIO.

requested_action: Tras cerrar TASK-0321 y TASK-0317, reclamar TASK-0322, flipearla a in_progress,
medir la poblacion de portadoras de partida, estrechar DATE_RE con validacion de rangos sin perder
ningun formato legitimo, verificar en clon limpio que el corpus no gana warnings de fecha y que los
11 vectores siguen rechazados, declarar la cifra de llegada y dejar la tarea en in_review con el
claim liberado.
