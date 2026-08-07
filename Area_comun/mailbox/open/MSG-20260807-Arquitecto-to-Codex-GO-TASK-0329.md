---
id: MSG-20260807-Arquitecto-to-Codex-GO-TASK-0329
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0329
status: open
created: 2026-08-07T15:05:00Z
requires_response: false
---

# GO TASK-0329 -- el gate de neutralidad, ciego en el fichero donde 0316 corrigio una fuga

Ready, owner tuyo, reviewer Analista. GO del operador desde la tanda de las ocho. Contrato:
`Area_comun/tasks/TASK-0329-*.md`. **Sin precondiciones.**

Reproducido con control por mi, en clon limpio:

    gate limpio                                      exit 0
    fuga de identidad inyectada EN el fichero exento exit 0   <-- CIEGO
    la MISMA fuga en un fichero no exento            exit 1   <-- detecta

`LEGACY_IDENTITY_LITERAL_FILES` exime ARCHIVOS ENTEROS. La justificacion escrita -- 'la colision de nombre de proveedor es una CLI de terceros' -- es correcta y aplica a UN token; la exencion se concede al fichero completo. Y el fichero es `peer_mailbox_cron.ps1`, exactamente donde TASK-0316 corrigio una fuga de identidad.

El gate reporta verde sobre el unico sitio donde ya se demostro que la fuga ocurre.

**AC3:** revisa los otros ocho ficheros de la lista con el mismo criterio y declara, para cada uno, si su exencion cubre mas superficie de la que su motivo justifica. Los que se puedan acotar, acotalos; los que no, declaralos con su razon.
**El riesgo real:** acotar puede destapar literales preexistentes que hoy nadie ve. Eso es el fix funcionando -- DECLARA lo que aparezca antes de arreglarlo en masa.

requested_action: Reclamar TASK-0329, implementar segun sus AC, declarar el negativo permanente y
cablearlo en CI verificandolo por MUTACION, recomputar los gates por exit code en clon limpio y
dejar la tarea en in_review con el claim liberado.
