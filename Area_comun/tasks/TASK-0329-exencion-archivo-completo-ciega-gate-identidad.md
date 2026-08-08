---
task_id: TASK-0329
file: Area_comun/tasks/TASK-0329-exencion-archivo-completo-ciega-gate-identidad.md
title: "La exencion de identidad se concede por ARCHIVO COMPLETO: el gate de neutralidad esta ciego en el mismo fichero donde TASK-0316 acaba de corregir una fuga de identidad"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0316
  - TASK-0314
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    `LEGACY_IDENTITY_LITERAL_FILES` de `scan_domain_neutrality.py` exime archivos ENTEROS. Entre
    ellos `scripts/harness/peer_mailbox_cron.ps1`, con la justificacion escrita en el propio
    codigo de que "la colision de nombre de proveedor se refiere a una CLI de terceros, no a un
    agente del protocolo". La justificacion es correcta y aplica a UN token; la exencion se
    concede al ARCHIVO. Resultado: cualquier literal de identidad, en cualquier linea de ese
    fichero, es invisible para el gate -- incluida exactamente la clase de fuga que TASK-0316
    acaba de corregir EN ESE MISMO FICHERO.
    El gate reporta verde sobre el unico sitio donde ya se demostro que la fuga ocurre.
  acceptance:
    - "AC1 (falsacion previa, ya reproducida): inyectar en el fichero exento un literal de identidad de la misma clase que 0316 corrigio deja el gate en exit 0; el MISMO literal en un fichero no exento da exit 1. Se reproduce con control, no se acepta de palabra."
    - "AC2 (la exencion se acota a lo que la justifica): la exencion deja de ser por archivo y pasa a nombrar el token concreto (o la linea concreta) que la merece. Todo lo demas del fichero vuelve a estar bajo el gate. La justificacion escrita y el alcance real de la exencion pasan a coincidir."
    - "AC3 (revision del resto del inventario): los otros ocho archivos de LEGACY_IDENTITY_LITERAL_FILES se revisan con el mismo criterio. Para cada uno se declara si su exencion cubre mas superficie de la que su motivo justifica; los que se puedan acotar se acotan, y los que no, se declaran con su razon."
    - "AC4 (contrato): negativo permanente que falle si un literal de identidad fuera del alcance exento entra en un fichero de la lista, declarado en el registro y cableado en CI, verificado por MUTACION que cae al revertir la guarda."
    - "AC5 (sin regresion): scan_domain_neutrality, su suite, contratos de falsacion y gates del repo exit 0 en clon limpio, y ningun falso positivo nuevo sobre el arbol actual."
  verification_cmd:
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/test_scan_domain_neutrality.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_domain_neutrality.py
    - scripts/scan_domain_neutrality.ps1
    - scripts/test_scan_domain_neutrality.py
  out_of_scope: >
    No se toca `REQUIRED_EXEMPT_GLOBS` (`runtime/memory/**`), que exime artefactos generados y
    tiene otra naturaleza. No se renombra ningun agente ni se cambia identidad alguna en el
    harness: lo que cambia es el ALCANCE de la exencion del gate, no el codigo exento.
  risk: medium
  estimate: M
---

# TASK-0329 -- la exencion de archivo completo ciega el gate donde mas duele

## Reproducido con control (2026-08-07, clon limpio en `origin/main` = 8bbff772)

    gate limpio                                                         exit 0
    fuga de identidad inyectada EN el fichero exento                    exit 0   <-- ciego
    la MISMA fuga en un fichero no exento                               exit 1   <-- detecta

El literal inyectado fue `$DefaultCoordinator = "Arquitecto"`, es decir, un valor de identidad
por defecto embebido en el harness: la clase de defecto que TASK-0316 corrigio, en el fichero
donde la corrigio.

## El patron, que es lo que importa

Es el mismo defecto de forma que TASK-0327: una exencion cuyo alcance es mas ancho que su
justificacion. Alli era un default de parametro que apagaba una capa entera; aqui es una entrada
de allowlist que apaga un fichero entero para excusar un token. En ambos casos el mecanismo
funciona, la razon escrita es correcta, y la superficie desprotegida es mucho mayor que la que
alguien decidio desproteger.

Merece la pena mirarlo junto: si aparece por tercera vez, deja de ser un bug y pasa a ser una
propiedad del estilo del repo que hay que gatear.

## Riesgo declarado (medium)

Acotar la exencion puede destapar literales de identidad preexistentes en esos nueve ficheros
que hoy nadie ve. Eso es el fix funcionando, pero puede convertir una tarea corta en una cola
de correcciones: por eso AC3 pide DECLARAR lo que aparezca antes de arreglarlo en masa, y
permite dejar exenciones acotadas con su razon en vez de forzar una limpieza total.
