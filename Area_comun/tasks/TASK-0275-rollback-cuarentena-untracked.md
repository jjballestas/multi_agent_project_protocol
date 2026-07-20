---
task_id: TASK-0275
title: "[HARNESS] Cuarentena en vez de borrado: el rollback de un exec abortado no puede destruir en silencio lo que un peer escribio durante la ventana"
type: infra
status: ready
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, DECISION-0103, DECISION-0020]
linked_decisions: [DECISION-0020]
file: Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
intake:
  type: infra
  goal: "Residual explicito de TASK-0272, registrado como unidad propia para no tocar el acceptance aprobado de aquella (enmienda E1). El rollback del exec abortado deja el arbol como estaba ANTES del exec, y eso incluye barrer lo que un peer escribio DURANTE la ventana, un draft untracked creado en esa ventana se BORRA sin log y es irrecuperable porque nunca estuvo en git (caso E5 del checker, reproducido). No es una regresion y no hay canal de atribucion posible en un arbol unico, pero excede en silencio el mandato de revertir lo que toco el exec. La perdida debe volverse recuperable y visible."
  acceptance:
    - "Los ficheros untracked que aparecen durante la ventana del exec no se borran, se MUEVEN a una cuarentena por ejecucion (por ejemplo runs/<stamp>-quarantine/) conservando la ruta relativa."
    - "El rollback deja en su log la lista de rutas restauradas y la lista de rutas puestas en cuarentena, con la ruta de la cuarentena, para que el humano o el peer las recupere sin arqueologia."
    - "Los cambios tracked no stageados que el rollback revierte quedan tambien registrados en ese log (hoy se restauran al estado pre-exec sin dejar rastro de que existieron)."
    - "Politica de retencion declarada de la cuarentena (cuando se puede limpiar y quien lo hace), para que no crezca sin fin."
    - "Negativo permanente en la suite, peer escribe un untracked durante la ventana, el exec aborta, el fichero NO se pierde y aparece en la cuarentena con su log."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde, incluido el negativo nuevo"
    - "Sandbox end-to-end, escritura de peer durante la ventana recuperable tras el aborto"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reabrir el acceptance de TASK-0272 - FUERA, por eso esta unidad existe por separado."
    - "Intentar ATRIBUIR autoria de ficheros untracked en un arbol unico - FUERA, no hay canal fiable, la cuarentena no necesita saber de quien es."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: low
  estimate: S
---

# TASK-0275 - Cuarentena en vez de borrado

Origen: F-0272R1-03 del re-juicio de TASK-0272. El checker pregunto si se difiere como
residual o entra en la iteracion 2. Decision del Arquitecto, ni una cosa ni la otra en el
sentido debil, se difiere de la iteracion 2 para respetar el candado E1 del Operador
(misma acceptance, mismo scope, mismo risk), pero NO se deja como nota al pie, se registra
como unidad con acceptance propio para que no se evapore.

Razon de fondo, es la misma clase de dano que acabamos de cerrar en la iteracion 1, un
rollback que destruye contenido que no era suyo. Alli era contenido staged de un peer,
aqui es un fichero sin trackear. La diferencia es que este ni siquiera tiene copia en git.
El coste de la mitigacion es mover en vez de borrar, y una linea de log.
