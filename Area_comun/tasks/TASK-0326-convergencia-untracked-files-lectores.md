---
task_id: TASK-0326
file: Area_comun/tasks/TASK-0326-convergencia-untracked-files-lectores.md
title: "Convergencia de los dos lectores de estado: sin --untracked-files=all git colapsa el directorio y un claim acotado a fichero dentro de el no casa nunca"
status: proposed
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
relates_to:
  - TASK-0323
  - TASK-0319
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    TASK-0323 dejo todos los lectores de ruta usando `-z` y con el inventario completo. Queda un
    hueco de OPCIONES, no de parseo: `sweep_cron_zombies.dirty_paths` no pasa
    `--untracked-files=all`. Sin esa opcion git COLAPSA un directorio sin rastrear en una sola
    entrada de directorio, asi que un claim acotado a un FICHERO dentro de el no casa nunca y el
    barredor decide sobre un mapa incompleto.
    El mismo hueco existe entre el barredor de Python y el helper de PowerShell, que no coinciden en
    las opciones con que interrogan a git. Se agrupan en una unica tarea de CONVERGENCIA por
    recomendacion del checker, que comparto: misma raiz, dos lectores, una sola revision.
  acceptance:
    - "AC1 (falsacion): sobre un repo git real se demuestra que, sin --untracked-files=all, un fichero dentro de un directorio sin rastrear NO aparece como ruta propia y un claim acotado a el no casa. Evidencia por comportamiento."
    - "AC2 (convergencia real): los DOS lectores -- el de Python y el de PowerShell -- interrogan a git con el MISMO juego de opciones. Se declara en el handoff la lista de opciones y por que cada una esta."
    - "AC3 (sin ensanchar de mas): anadir --untracked-files=all aumenta el conjunto observado; se verifica que eso no rompe el guard de residuo ni hace que el barredor mate lo que no debe. Si aparece un efecto colateral, se declara y se acota."
    - "AC4 (contrato): negativo permanente con salida REAL de git que cubra el caso del directorio colapsado, declarado en el registro y cableado en CI."
    - "AC5 (sin regresion): suite del harness y gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
  scope_routes:
    - scripts/sweep_cron_zombies.py
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    Reabrir el parseo de rutas cerrado en 0323; cambiar la logica de decision del barredor; los
    presupuestos de TASK-0319 y TASK-0324.
  risk: low
  estimate: S
notes: >
  Residual R4 del veredicto del Analista sobre TASK-0323
  (Area_comun/artifacts/Analista-TASK-0323-porcelain-z-readers-verdict.md). El checker ofrecio
  registrarlo suelto o agruparlo con el hueco equivalente del helper de PowerShell; el Arquitecto
  elige agrupar, que es su propia sugerencia y es mejor que la alternativa: misma causa raiz en dos
  lectores, y revisarlos por separado invita a que converjan a medias.
  Es la CUARTA tarea de la serie de lectores de git status (0319, 0321, 0323 y esta). Las tres
  anteriores fueron de PARSEO; esta es de OPCIONES, que es la otra mitad del mismo problema: no basta
  con leer bien lo que git dice si no se le pregunta bien.
