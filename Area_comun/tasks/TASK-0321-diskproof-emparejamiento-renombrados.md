---
task_id: TASK-0321
file: Area_comun/tasks/TASK-0321-diskproof-emparejamiento-renombrados.md
title: "El mismo defecto de emparejamiento de renombrados sigue vivo en Get-WorktreeDiskProof: la prueba de disco se corrompe con un git mv"
status: done
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
relates_to:
  - TASK-0319
created_at: 2026-08-06
intake:
  type: fix
  goal: >
    TASK-0319 corrigio el emparejamiento de registros del stream `git status --porcelain=v1 -z` en
    `Get-StagedResidueState`, pero el MISMO defecto sigue vivo en `Get-WorktreeDiskProof`
    (`scripts/harness/peer_mailbox_cron.ps1`, lineas 660-663): recorre los registros uno a uno,
    aplica `Substring(3)` a TODOS y conserva la rama muerta ` -> ` que git jamas emite bajo `-z`.
    Ante un renombrado, el segundo registro -- la ruta de ORIGEN, que viene SIN prefijo de estado --
    pierde tres caracteres, `Test-Path` falla sobre la ruta amputada y la prueba de disco registra
    `exists=false` con un nombre que no existe. La funcion existe para PROBAR el estado del arbol,
    asi que una entrada corrupta la convierte en una prueba que miente.
  acceptance:
    - "AC1 (falsacion antes del fix): sobre un repo git REAL en scratch se hace un git mv y se demuestra que Get-WorktreeDiskProof emite una entrada con ruta amputada y exists=false. Evidencia de partida por comportamiento, no por lectura -- es el mismo metodo que cazo S1."
    - "AC2 (mismo remedio, no uno nuevo): se recorre el stream por pares con la MISMA logica ya aprobada en Get-StagedResidueState: si los dos primeros caracteres son [RC], el registro siguiente es la ruta de origen y se trata como unidad; si falta, se devuelve el valor de fallo de la funcion en vez de inventarse una ruta."
    - "AC3 (rama muerta fuera): se borra el ` -> `. Codigo muerto que parece cobertura es exactamente lo que produjo el miss de S1 y ya nos costo una iteracion."
    - "AC4 (boundary con git real): el contrato de falsacion cubre esta funcion con salida REAL de git tras un renombrado, no un mock. Declarado en el registro y cableado en CI."
    - "AC5 (barrido, no parche puntual): se revisa si queda ALGUNA otra lectura de `git status --porcelain -z` en el harness con el mismo patron. Si aparece, entra aqui. El objetivo es que no quede una tercera."
    - "AC6 (sin regresion): suite del harness verde, validate y scan exit 0, todo por exit code en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    Reabrir nada de lo que TASK-0319 cerro; cambiar el presupuesto de diferimientos; TASK-0320.
  risk: low
  estimate: S
notes: >
  Hallazgo S4 del veredicto r2 del Analista sobre TASK-0319
  (Area_comun/artifacts/Analista-TASK-0319-r2-record-pairing-verdict.md). Verificado
  INDEPENDIENTEMENTE por el Arquitecto antes de registrarlo: lineas 660-663 tienen el patron
  identico al que S1 corrigio.
  Se abre como tarea aparte y no como iteracion de 0319 por recomendacion del propio checker, que
  comparto: 0319 esta aprobada por las dos capas y entrega valor ya (el harness dejo de matar colas);
  extenderla obligaria a re-revisar todo lo aprobado por un defecto separable.
  AC5 es mio y no del checker: dos apariciones del mismo patron en el mismo archivo hacen sospechar
  de una tercera. Barrer es mas barato que descubrirla en produccion dentro de dos semanas.
