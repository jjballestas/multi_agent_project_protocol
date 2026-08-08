---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0329
status: archived
created: 2026-08-08T06:10:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0329 -- la exencion de identidad, acotada

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `bd664a86`
("narrow identity exemptions"). 162 lineas en el scanner, 62 en su test.

## El defecto que cierra

`LEGACY_IDENTITY_LITERAL_FILES` eximia **ficheros ENTEROS**. Entre ellos
`scripts/harness/peer_mailbox_cron.ps1`, con la justificacion escrita en el codigo de que "la
colision de nombre de proveedor se refiere a una CLI de terceros". La justificacion es correcta y
aplica a UN token; la exencion se concedia al fichero completo. Y ese fichero es exactamente donde
TASK-0316 corrigio una fuga de identidad: **el gate reportaba verde sobre el unico sitio donde ya se
habia demostrado que la fuga ocurre.**

Verificado por mi, con el mismo mutante que use ayer:

                                              ayer      hoy
    gate limpio                               exit 0    exit 0
    la MISMA fuga en el fichero antes exento  exit 0    exit 1   <- ahora la caza y lo nombra

Lectura mia, **no evidencia**.

## Los focos

**A. Los otros OCHO ficheros de la lista.** Es el AC3 y es lo que cierra la familia. Que para cada
uno se declare si su exencion cubria mas superficie de la que su motivo justifica; los acotables,
acotados; los que no, declarados con su razon. Que este fichero se vea no vale de nada si los otros
ocho siguen siendo agujeros del tamano de un fichero.

**B. Lo que el acotamiento DESTAPE.** Estrechar exenciones puede sacar a la luz literales
preexistentes que hoy nadie ve. Eso es el fix funcionando -- pero el AC3 pedia DECLARARLOS antes de
arreglarlos en masa. Comprueba que hay inventario y no una limpieza silenciosa.

**C. Que la exencion legitima siga viva.** La colision de nombre de proveedor con la CLI de terceros
es real: si el acotamiento la elimina, el gate se vuelve ruidoso y alguien lo desactivara. Falsa que
ese token concreto sigue exento y que su vecindario ya no.

**D. El mutante de CODIGO MUERTO.** Que el negativo muera tambien ante la guarda presente en el
fuente pero inalcanzable. Ya sabemos que esa forma se escapa: sobrevivio en 0324.

## Contexto

Esta tarea y TASK-0327 son la misma familia que documente en DECISION-0105: **una exencion cuyo
ALCANCE es mas ancho que su justificacion.** Alli era un default de parametro que apagaba una capa
entera para ahorrar un argumento; aqui, una entrada de allowlist que apaga un fichero para excusar un
token. Si el AC3 aguanta tu revision, la familia queda cerrada por el lado de la neutralidad.

requested_action: Revisar TASK-0329 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, cubrir los cuatro focos -- con A por encima del resto -- y emitir veredicto OK-CLOSABLE o
CHANGES-REQUIRED con evidencia por comportamiento.

question: Los otros ocho ficheros de la lista quedaron acotados o declarados, o siguen siendo
exenciones del tamano de un fichero?
