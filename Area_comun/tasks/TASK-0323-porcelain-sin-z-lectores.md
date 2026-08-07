---
task_id: TASK-0323
file: Area_comun/tasks/TASK-0323-porcelain-sin-z-lectores.md
title: "Lectores de git status --porcelain SIN -z fabrican rutas inexistentes: el barredor de zombis falla ABIERTO"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
relates_to:
  - TASK-0319
  - TASK-0321
created_at: 2026-08-06
intake:
  type: fix
  goal: >
    TASK-0319 y TASK-0321 arreglaron los lectores de `git status --porcelain=v1 -z` del harness. Pero
    hay lectores que NO usan `-z` y tienen el problema simetrico: `scripts/sweep_cron_zombies.py:78`
    corre `git status --porcelain=v1` y parte por lineas. Sin `-z`, git (a) SI usa el formato
    ` -> ` para renombrados y (b) ENTRECOMILLA y escapa en C las rutas con caracteres especiales,
    espacios problematicos o no-ASCII. Trocear por lineas y cortar por posicion produce rutas que no
    existen.
    Direccion del fallo: **ABIERTO**. El barredor de zombis usa esas rutas para decidir que procesos
    son huerfanos; con una ruta fabricada deja de reconocer trabajo vivo o deja de ver un zombi. Un
    barredor que falla abierto no barre, y nadie se entera.
  acceptance:
    - "AC1 (falsacion antes del fix): sobre un repo git REAL en scratch se demuestra que el lector actual fabrica rutas inexistentes en los dos casos -- un renombrado y una ruta que git entrecomilla (con espacio o no-ASCII). Evidencia por comportamiento."
    - "AC2 (el arreglo correcto es -z, no parchear el troceo): los lectores pasan a `--porcelain=v1 -z` y se recorren por pares como ya se hace en el harness, o bien se desentrecomilla y desescapa correctamente si hay razon declarada para no usar -z. Elige y justifica en el handoff."
    - "AC3 (barrido, con criterio propio): busca TODOS los lectores de git status del repo, no solo el del barredor. Declara la lista completa en el handoff y di de cada uno si usa -z o no. Este AC es el que evita una cuarta ronda."
    - "AC4 (contrato de falsacion): negativo permanente que alimente salida REAL de git con un renombrado Y con una ruta entrecomillada, y exija que el lector devuelva la ruta correcta. Declarado en el registro y cableado en CI."
    - "AC5 (sin regresion): la suite del harness y los gates del repo verdes por exit code en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/sweep_cron_zombies.py
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    Reabrir lo cerrado en 0319 o 0321; cambiar la logica de decision del barredor (solo se arregla
    como LEE las rutas, no que hace con ellas); TASK-0320 y TASK-0322.
  risk: low
  estimate: S
notes: >
  Residual R3 del veredicto del Analista sobre TASK-0321
  (Area_comun/artifacts/Analista-TASK-0321-diskproof-pairing-verdict.md). Verificado
  INDEPENDIENTEMENTE por el Arquitecto: `sweep_cron_zombies.py:78` lee sin `-z` y trocea por lineas.
  Se registra como tarea propia y no como residual anotado por la DIRECCION del fallo: es ABIERTO
  (el barredor deja de ver zombis en silencio), no cerrado. Esa es la misma regla que aplicamos en
  TASK-0317, donde un residual "pequeno" resulto grave por fallar abierto en vez de cerrado.
  Nota util para quien lo implemente: la rama ` -> ` que TASK-0319 borro por CODIGO MUERTO era
  correcta AQUI. El repo convive con las dos convenciones -- con `-z` git no la emite, sin `-z` si --
  y esa coexistencia es justo lo que hizo plausible el codigo muerto. No la restaures en los
  lectores con `-z`.
