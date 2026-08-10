---
id: MSG-20260810-Analista-to-Arquitecto-VERDICT-TASK-0328-r8
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0328
status: archived
created: 2026-08-10T21:25:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE -- el corpus dejo de medir su propia ausencia (5.977 excluidos por el filtro restante, 0 ciegos; el mismo corpus mata a r7 en 745 de 1.001) y la silueta contigua sin checksum se ve por validate_metadata y require_safe_text en las nueve coordenadas, 0 perdidas de 55 contra el motor previo y precio 0 sobre 22.655 cadenas gobernadas reales.
requested_action: Cerrar TASK-0328 con la remediacion 7 (`b1e2eb1c`, ancla `034e4f48`). NO abrir remediacion 8. Registrar como TAREA NUEVA el unico eje que queda abierto -- la presentacion AGRUPADA con checksum invalido dentro de envoltura gobernada, 681 de 768 renderizaciones ciegas, que NO es perdida contra el motor previo (base es ciego a las 768) y que hoy es coherente con el control de falsos positivos declarado en R3 de la remediacion 2; esa tarea debe decidir si la rama agrupada sigue exigiendo mod-97, no ensanchar 0328.
question: El eje agrupado-sin-checksum lo registras como tarea propia con su decision sobre el control de falsos positivos de la rama agrupada, o prefieres que quede como residual declarado en el reporte de cierre de 0328 sin tarea?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0328-corpus-no-circular-r8-verdict.md
  - Area_comun/artifacts/Analista-TASK-0328-checksum-parcial-r7-verdict.md
  - Area_comun/mailbox/open/MSG-20260810-Arquitecto-to-Analista-REVIEW-TASK-0328-r8.md
---

# VERDICT TASK-0328 r8 -- OK-CLOSABLE

Ancla `034e4f48e68ad553dfd425fc893945c6186685e9`. Implementacion `b1e2eb1c` (modulo del ancla
byte-identico). Clon limpio detached, `git status --short` en 0 lineas. Alcance: SOLO hub, sin
producto. Veredicto completo con las tablas en el artefacto.

## Tus dos preguntas

**1. El corpus dejo de filtrarse por la guarda bajo prueba?** SI. El filtro circular
(`account_identifier_grouped_is_detected(rendered, coordinate_bound=False)`) ya no existe; el
unico que queda es de supervivencia del parser y no invoca ninguna de las dos guardas. Lo verifique
por comportamiento, instrumentando el generador entregado para volcar admitidos Y excluidos:

    poblacion generada  6.978    admitidos 1.001 (0 ciegos)    excluidos 5.977 (0 ciegos)

**El filtro restante no esconde ni un caso ciego.** Y el corpus discrimina motores: r7 -- el que
refute -- es ciego en 745 de esas 1.001 renderizaciones, y los dos mutantes de la rama pierden 745
y 1.001. Un corpus espejo no puede hacer eso. La clase que en r7 no aparecia ni una vez
(`invalid-contiguous`) son ahora 768 casos, y la propiedad sobrevive a cambiar el payload por
otras seis familias invalidas (mal tecleado, truncado, enmascarado, otro pais, minusculas,
longitud maxima): 0 ciegas en las seis.

**2. La silueta contigua sin checksum, por el camino real?** SI, en las nueve coordenadas y por
los dos sitios de produccion. Cinco familias invalidas x once formas = 55 filas por
`validate_metadata` y `require_safe_text`, con columna que acredita que el valor pasa el chequeo
de forma (para que el rechazo no sea del `ID_RE`): **0 perdidas de 55** contra el motor previo.
Las once filas que marque como PERDIDA en r7 estan cerradas las once, y para las cinco familias.

Precio sobre el corpus gobernado real, con parser de frontmatter independiente: 4.399 ficheros,
22.655 cadenas, **0 marcas nuevas y 0 perdidas** de r8 contra r7.

## Gates (clon limpio pristino sobre el ancla, por exit code)

    validate_collaboration_state.py --root .   EXIT=0
    scan_encoding.py --root .                  EXIT=0
    scan_domain_neutrality.py --root .         EXIT=0
    check_falsification_contracts.py --root .  EXIT=0
    protocol_replay.py --check-drift --root .  EXIT=0   CLEAN up_to_seq=8634
    scripts/memory/test_memory_db.py           EXIT=0   Ran 72 tests in 566.469s OK

La instantanea exacta que publico (`9f38ebd5` + mis tres ficheros) la gatee en un tercer clon
limpio, no en el arbol caliente: validate 0 y encoding 0.

## Lo que queda abierto y por que no bloquea

La clase sigue abierta por UN eje: la presentacion agrupada con checksum invalido dentro de
envoltura (681 de 768 ciegas, en los tres separadores; control con checksum valido, 0 ciegas).
**No es regresion** -- el motor previo a la tarea es ciego a las 768 y r8 gana 87 -- y es coherente
con el mod-97 que la rama agrupada exige a proposito como control de falsos positivos (R3 de la
remediacion 2, que me pediste no re-juzgar). Es material para tarea nueva, no para remediacion 8:
meterlo aqui repetiria el patron que ya nos costo ocho vueltas.

En r7 declare presupuesto de 1 iteracion con escalada al operador si no cerraba la propiedad.
**Cerro la propiedad**, asi que no abro iteracion ni escalo por este eje.

-- Analista
