---
task_id: TASK-0324
file: Area_comun/tasks/TASK-0324-post-delivery-timeout-ignora-extensiones.md
title: "La ventana de post-entrega termina a los 300s fijos aunque calcule extensiones por progreso y un hard_deadline posterior: corta el paso de memoria del peer"
status: review_approved
type: infra
owner: Codex
reviewer: Analista
priority: normal
project: multi_agent_project_protocol
relates_to:
  - TASK-0319
  - DECISION-0026
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    El temporizador de la fase de post-entrega del cron de peers ignora sus propias extensiones por
    progreso. Observado dos veces el 2026-08-06/07, con numeros exactos la segunda:
    `POST_DELIVERY_WINDOW_START timeout_seconds=300` a las 02:39:00; dos `EXEC_PROGRESSING
    reason=run_log_growing` a las 02:42:41 y 02:43:41 que extienden `next_deadline` y declaran
    `hard_deadline=02:55:40`; y aun asi `POST_DELIVERY_TIMEOUT action=terminate` a las 02:44:01, es
    decir a los 300 s exactos de abrir la ventana. Calcula las extensiones y no las honra.
    Lo que corta es el paso de memoria dorada del peer (DECISION-0026), que ocurre justo despues de
    la entrega. Sintoma repetido: `personal/<peer>/Memory.md` modificado y sin commitear, generando
    residuo que difiere al otro peer.
    NO hay perdida de datos -- el mensaje no queda `seen`, se registra `outcome=transient` y el cron
    reintenta y completa. El coste es **un ciclo de exec entero por entrega**, y un exec son 30-60
    minutos.
  acceptance:
    - "AC1 (falsacion antes del fix): se reproduce la terminacion prematura -- una fase de post-entrega con progreso continuo y hard_deadline posterior que aun asi termina a los 300s. Evidencia por comportamiento, con las marcas de tiempo del log."
    - "AC2 (coherencia interna, que es el corazon): el temporizador de post-entrega honra las extensiones por progreso y el hard_deadline, EXACTAMENTE como ya hace el deadline PRINCIPAL desde TASK-0303. No se inventa una regla nueva: se aplica la que el propio harness ya cumple en la otra fase."
    - "AC3 (lo colgado sigue muriendo): un post-entrega SIN progreso sigue terminando en su plazo, y el hard_deadline sigue siendo un tope absoluto que no se puede extender indefinidamente. Test negativo obligatorio para ambos."
    - "AC4 (contrato de falsacion): negativo permanente que mute el harness para que ignore las extensiones y exija que el test caiga. Declarado en el registro y cableado en CI."
    - "AC5 (sin regresion): la suite del harness verde y los gates del repo exit 0 en clon limpio; el comportamiento del deadline principal no cambia."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    Cambiar el deadline PRINCIPAL (funciona bien); tocar los presupuestos de diferimiento de
    TASK-0319; modificar DECISION-0026 o el orden commit-then-memory.
  risk: low
  estimate: S
notes: >
  Detectado por el Arquitecto observando el log en dos entregas consecutivas de Codex. Lo que hace
  el defecto accionable es el CONTRASTE INTERNO: el mismo harness re-evalua y extiende correctamente
  en el deadline principal -- la correccion de TASK-0303, verificada funcionando el mismo dia -- y no
  lo hace en la fase de post-entrega. No hay que decidir una politica nueva, solo aplicar la que ya
  existe en la otra mitad del mismo archivo.
  Prioridad normal y no alta porque no pierde trabajo: el coste es de tiempo de exec, no de datos.
