---
task_id: TASK-0325
file: Area_comun/tasks/TASK-0325-endurecimiento-exencion-fecha.md
title: "Endurecimiento de la exencion de fecha: chequeo AST contra bypass por continue + los dos residuales R5-1 y R5-2"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
spec_id: SPEC-MEMORIA-HIBRIDA
relates_to:
  - TASK-0317
created_at: 2026-08-07
intake:
  type: infra
  goal: >
    TASK-0317 cerro con el contrato de colocacion y el barrido de familia aprobados: la exencion de
    `DATE_RE` esta fijada DENTRO del bloque del heuristico de telefono y el mutante que la movia cae.
    Quedan tres endurecimientos del MISMO area, todos medidos por el checker y ninguno bloqueante:
    (a) el chequeo AST de una linea que el checker dejo medido -- que no exista un `continue` en el
    bucle de `contains_pii` capaz de saltarse los chequeos posteriores sin mover la exencion, que es
    un bypass DISTINTO del que el contrato actual cubre; y (b) los residuales R5-1 y R5-2 declarados
    en su veredicto r5.
    Se agrupan aqui a proposito: son tres endurecimientos del mismo mecanismo y una sola revision
    los cubre mejor que una sexta iteracion de 0317 mas dos seguimientos sueltos.
  acceptance:
    - "AC1 (chequeo AST): se anade el chequeo que el checker dejo medido en la seccion 3 de su veredicto r5, verificando por AST que el bucle de contains_pii no contiene un continue capaz de saltarse los chequeos posteriores. Con su mutacion correspondiente."
    - "AC2 (R5-1 y R5-2): se atienden los dos residuales del veredicto r5 tal como estan descritos ahi, o se declara con razon medida por que uno de ellos no procede."
    - "AC3 (contratos con dientes): cada guarda nueva va con su negativo permanente declarado en el registro y cableado en CI, y se verifica por MUTACION que cae al revertir la guarda. Es el estandar que ha regido todo este hilo."
    - "AC4 (sin regresion): no se toca el comportamiento aprobado en 0317 -- la exencion sigue anclada en DATE_RE dentro del bloque del telefono, los 11 vectores de cola siguen rechazados y la familia sigue en 333. Suite y gates exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope: >
    Cambiar el anclaje en DATE_RE ni la colocacion de la exencion (aprobados en 0317); estrechar
    DATE_RE con rangos (eso es TASK-0322); reabrir el barrido de familia.
  risk: low
  estimate: S
notes: >
  Residuales del veredicto r5 del Analista sobre TASK-0317
  (Area_comun/artifacts/Analista-TASK-0317-barrido-familia-r5-verdict.md). El checker ofrecio dos
  opciones -- meter el chequeo AST antes del done-flip o registrarlo como seguimiento -- y el
  Arquitecto elige lo segundo: el fix y su contrato ya estan aprobados y verificados, y el AST
  protege contra un bypass DISTINTO del que el contrato cubre, asi que es endurecimiento adicional y
  no completar lo entregado.
  0317 llevaba cinco iteraciones; agrupar tres endurecimientos en una unidad revisable rinde mas que
  una sexta.
