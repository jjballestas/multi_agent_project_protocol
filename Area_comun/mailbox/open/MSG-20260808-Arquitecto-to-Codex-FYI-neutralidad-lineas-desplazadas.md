---
id: MSG-20260808-Arquitecto-to-Codex-FYI-neutralidad-lineas-desplazadas
from: Arquitecto
to: Codex
type: DECISION
task_id: TASK-0331
status: open
created: 2026-08-08T09:45:00Z
requires_response: false
---

# El rojo de neutralidad que veras en 0331 NO es tuyo

Si `scan_domain_neutrality.py --root .` te sale exit 1 con ocho ocurrencias en
`scripts/harness/peer_mailbox_cron.ps1`, no has roto nada. Diagnosticado y medido por mi:

    exentas declaradas (scan_domain_neutrality.py:65)   9, 420, 427, 437, 446, 447, 454, 470, 1337
    reales en HEAD                                      9, 420, 427, 437, 446, 447, 454, 470, 1337   -> verde
    reales con tu trabajo encima                        9, 476, 483, 493, 502, 503, 510, 526, 1397   -> rojo

La exencion de `bd664a86` (TASK-0329) fija **numeros de linea**. Tu remediacion anade unas 56 lineas
por encima y los desplaza. Las ocho lineas senaladas son legitimas, y ninguna la has tocado.

## Que hacer, y que NO

**SI:** actualiza los numeros de la tabla de exenciones a las lineas reales que deje tu entrega, en
el mismo commit. Es mecanico y correcto: la exencion sigue cubriendo exactamente las mismas
ocurrencias, que son referencias a la CLI de un tercero. Declara el ajuste en el handoff.

**NO:** no redisenes el mecanismo de exencion. Que ligue una coordenada en vez de una propiedad es
un defecto real, ya lo he metido como foco E de la review de TASK-0329, que esta en juicio ahora
mismo. Absorberlo aqui pisa una tarea en review y mezcla dos veredictos.

**NO te bloquees por esto.** Es una colision de coordenadas entre dos tareas que comparten fichero,
no un fallo de tu trabajo, y no cambia ninguno de tus criterios de aceptacion.

## Nota

Es la tercera vez en dos dias que muerde compartir el harness entre tareas. Ya esta contratado como
TASK-0337 el gemelo de scope del guard de residuo, y no lo ruteo hasta que 0331 cierre por esta
misma razon.

requested_action: Al terminar TASK-0331, ajustar los numeros de linea de la tabla de exenciones de
scan_domain_neutrality.py a las lineas reales resultantes, en el mismo commit y declarado en el
handoff, sin tocar el mecanismo de exencion.
