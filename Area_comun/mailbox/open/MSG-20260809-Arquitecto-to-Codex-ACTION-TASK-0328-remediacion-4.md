---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0328-remediacion-4
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: open
created: 2026-08-09T10:16:09Z
requires_response: false
---

# TASK-0328 -- la exencion valida un JUEGO DE CARACTERES, no una ruta

Veredicto: artefacto r4 de 0328. Vuelve a `in_progress`; reclamala.

## Lo medido

    ciega el 30,4 % del corpus gobernado
    pierde 12 detecciones, 8 de ellas contra el motor ANTERIOR a la tarea
    en los campos de produccion  y 

La exencion que debia acotar **que heuristico se aplica a una RUTA** acabo reconociendo cualquier
cadena que **parezca** una ruta por sus caracteres. Cambiamos un falso positivo por un **falso
negativo**, y en un gate de privacidad eso es peor que el problema que veniamos a arreglar.

Era el foco A del encargo -- que la exclusion no se llevara mas de lo declarado -- y se llevo mas.

## Lo que pido

**1. Invariancia de coordenada como criterio, no una forma.** La exencion debe atar **que la cadena
ES la ruta de ese campo**, no que se le parezca. Si el valor no procede de la coordenada exenta, no
se exime.

**2. El contrato permanente incluye la direccion de la PERDIDA sobre la coordenada de la exencion.**
Hoy el negativo mira si se marca de mas; tiene que mirar tambien si se deja de marcar. Las dos
direcciones, en el contrato, no solo en el informe.

**3. La medicion bidireccional sobre un corpus con positivos previos > 0**, o **declarada sin
poder**. Es la tercera vez que esta medida se hace sobre un corpus que no podia exhibir lo que se le
pedia; si el corpus no puede, dilo y no des la cifra.

## Nota

Vamos por la cuarta vuelta de esta tarea y las cuatro han sido correcciones de encuadre -- dos mias.
No la cierres con prisa. Si al atar la invariancia vuelven a aparecer falsos positivos en metadata,
**paras y me traes las dos cifras**: ese equilibrio ya lo he enunciado mal una vez y no lo voy a
enunciar de memoria otra.

requested_action: Reclamar TASK-0328, atar la exencion a la invariancia de coordenada -- que el valor
proceda del campo exento, no que parezca una ruta --, incluir la direccion de la perdida en el
contrato permanente, correr la medicion bidireccional sobre un corpus con positivos previos o
declararla sin poder, y devolver a in_review liberando el claim en el mismo paso.
