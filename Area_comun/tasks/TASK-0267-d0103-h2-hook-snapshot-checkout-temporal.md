---
task_id: TASK-0267
title: "[DECISION-0103][C5/H2] Hook pre-commit v2: validar el snapshot staged en checkout temporal del indice (elimina el mutex global del arbol compartido)"
type: infra
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-19
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md
intake:
  type: infra
  goal: Resolver H2 (MSG-20260719-Operador-to-Arquitecto-HALLAZGOS-hook-runtime-bypass-y-mutex), el hook actual exige arbol limpio (sin unstaged NI untracked) en TODAS las rutas de juicio, lo que en un arbol COMPARTIDO convierte cada exec abierto de un agente en un bloqueo de los commits de TODOS los demas (reproducido 2 veces, el Asesor quedo mudo 15 min). Sustituir la equivalencia de limpieza por la via que el acceptance original de 0257 nombraba, MATERIALIZAR el indice en un checkout temporal (git worktree desde el indice o git archive del indice a temp) y correr alli el validador, juzgando EXACTAMENTE lo que se commitea sin exigir arbol limpio.
  acceptance:
    - El hook valida el snapshot staged materializando el INDICE en un directorio temporal y ejecutando alli validate_collaboration_state; la exigencia de arbol limpio en rutas de juicio DESAPARECE (un peer con trabajo en vuelo en rutas gobernadas NO bloquea el commit de otro agente).
    - El vector F-0257-01 sigue cerrado, la mutacion unstaged del validador (o de cualquier dependencia del juicio) NO afecta el veredicto porque el juicio corre sobre la materializacion del indice; el negativo permanente existente sigue en verde y se anade un caso de concurrencia (unstaged ajeno en rutas gobernadas + commit propio limpio = commit PASA; estado staged roto = commit FALLA).
    - Coste medido contra el presupuesto de F-0257-02, materializacion + validacion dentro del umbral del acceptance de 0257 (~10s con modo acotado como valvula); cifras en el handoff, en frio y en caliente.
    - La limpieza temporal es robusta (el checkout/worktree se elimina siempre, incluso en fallo; sin residuos en .git/worktrees).
    - Si la materializacion resulta inviable por coste, fallback documentado y aprobado en el propio handoff, acotar la exigencia de limpieza SOLO a las rutas del validador (scripts/, runtime/, .githooks/), nunca a todo Area_comun/; el racional y la perdida de correccion quedan declarados.
    - Espejo en el export born-operational (la instancia nueva nace con el hook v2) y compatibilidad con lo que TASK-0266 propaga.
    - TRANSFERIDO del cierre de TASK-0257 (decision O1 del Operador 2026-07-20), los escapes con hook EN EJECUCION quedan cubiertos por la materializacion, en particular el rename R100 de una ruta gobernada o del codigo del juicio (el juicio corre sobre el estado materializado completo, no sobre un diff de nombres), con negativo permanente del caso rename.
    - El arnes de negativos se corrige para invocar el flujo REAL de git commit (el actual invoca el hook con sh y confunde archivo-inexistente con rechazo, falso-pasa cazado por el checker).
    - C2 del Operador (plegada aqui por acoplamiento de hash), paso de CI en .github/workflows/validate.yml que verifica que .githooks/pre-commit EXISTE en el clon y que su SHA-256 coincide con el pineado; el hash esperado se actualiza en esta MISMA entrega al del hook v2 final. Racional del plegado: una unidad separada pinnearia un hash obsoleto o esperaria a esta de todos modos.
    - LIMITE DECLARADO (correccion C1 del Operador, residual estructural de 0257), esta unidad NO cubre el borrado del PROPIO hook en LOCAL -- un hook borrado no se ejecuta y ninguna logica interna lo alcanza; su deteccion vive SOLO en la capa CI (el paso de existencia+hash) y en la revision de diffs. Queda declarado en el handoff y en la doc del hook.
  verification_cmd:
    - Prueba de concurrencia en sandbox, unstaged ajeno en Area_comun/ + commit propio -> exit 0; estado staged roto -> exit 1; mutacion unstaged del validador -> veredicto NO cambia
    - Medicion de coste del hook completo (frio/caliente) declarada en el handoff
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - .githooks/pre-commit
    - scripts/new_instance.py
    - scripts/test_precommit_hook.py
    - .github/workflows/validate.yml
    - examples/
  out_of_scope:
    - runtime/vcs.py y el no-verify del runtime - FUERA (es H1, plegado en TASK-0266).
    - Cambiar la logica interna del validador - FUERA.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: medium
  estimate: M
---

# TASK-0267 - [DECISION-0103][H2] Hook v2: snapshot por checkout temporal

Origen: hallazgo H2 del Operador (uso en vivo del harness, 2026-07-19), ruteo delegado
resuelto por el Arquitecto como UNIDAD NUEVA para mantener puro el fix-loop de 0257
(F01/F02). El enfoque de checkout temporal es el que el acceptance original de 0257
nombraba como via preferente; la equivalencia de limpieza fue el atajo que creo el
mutex. PRIORIDAD ALTA por urgencia operativa: mientras el hook actual siga armado, la
coordinacion de todos los agentes depende de que ningun otro tenga trabajo en vuelo.
SECUENCIA ACTUALIZADA (decision O1 del Operador 2026-07-20): el fix-loop de 0257 agoto
su tope (3er NO-GO) y 0257 quedo blocked con residuales declarados; esta unidad recibe
GO INMEDIATO con la transferencia de arriba. El cierre final de 0257 llega tras el
aterrizaje de esta unidad y su re-juicio. Valvula interina si el mutex vuelve a morder
ANTES de esta unidad: desarme E3 temporal (git config --unset core.hooksPath) declarado
por mailbox y re-arme inmediato tras el commit bloqueado -- es exactamente el caso de
emergencia que E3 contempla.
