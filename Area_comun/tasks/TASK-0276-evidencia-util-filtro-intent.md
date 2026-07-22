---
task_id: TASK-0276
title: "[HARNESS] Evidencia propia con TRABAJO UTIL: filtrar por intent_type y applied, exigir keyid coherente, y gatear los dos caminos de git que quedaron sin exit-code"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: medium
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0275, DECISION-0103, DECISION-0020]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0276-evidencia-util-filtro-intent.md
intake:
  type: infra
  goal: "Residuales acotados del re-juicio de la iteracion 2 de TASK-0272 (F-0272R2-01 a F-0272R2-04), registrados como unidad propia para no reabrir una unidad ya cerrada. El filo principal, la capa de evidencia acepta CUALQUIER evento propio firmado en la ventana del exec sin mirar de que tipo es, asi que un exec que solo adquiere y suelta un claim, sin token y con exit 0, se marca como confirmado y quema el mensaje (repro determinista E04 del checker). No es el burn de campo, las tres recurrencias reales eran abortos PRE-claim y esos ya quedan en unconfirmed, y este caso deja siempre traza firmada atribuible; pero es el mismo modo de fallo con menos filo y tiene un fix de pocas lineas."
  acceptance:
    - "Solo cuenta como evidencia de trabajo util un evento propio con applied true y cuyo payload.intent_type este en {task_status, task_upsert, decision} o que traiga payload.commit; el par de puro claim acquire/release y los exception.recorded dejan de confirmar."
    - "El patron real de entrega de los peers (transaccion con task_status mas commit) sigue confirmando: negativo y positivo permanentes en la suite que lo demuestren."
    - "El chequeo de firma deja de ser solo de PRESENCIA: se exige applied true y coherencia entre el prefijo del keyid y el actor, de modo que un evento rechazado por fencing o firmado con la clave de otro no confirme."
    - "El git ls-files de untracked pre-exec queda gateado por exit code igual que los dos snapshots binarios; si falla, el exec no arranca (hoy una lista vacia por fallo haria que el rollback tratase TODOS los untracked previos como creados por el exec y los borrase)."
    - "Un git apply fallido tras el reset deja un APPLY_FAIL visible en el log en vez de perder en silencio el pre-sucio del peer."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde, incluidos los negativos nuevos"
    - "Sandbox E2E con autor uniforme, exec de puro claim sin token NO consume el mensaje"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reabrir el acceptance de TASK-0272 - FUERA, la unidad se cierra con estos residuales declarados."
    - "Verificacion criptografica completa de firmas en el harness del cron - FUERA, eso vive en el validador del ledger."
    - "Cambiar la frontera de outcome decidida (token > exit > evidencia > regex) - FUERA."
    - "protocol.config.json pineado y dataset N=500 - FUERA (fondo intocable)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: low
  estimate: S
---

# TASK-0276 - Evidencia propia con trabajo util

Origen: hallazgos F-0272R2-01 a 04 del re-juicio de la iteracion 2 de TASK-0272 (41
pruebas unitarias y 23 asserts end-to-end en once sandboxes de autor uniforme).

Por que no bloqueo el cierre de 0272 y sin embargo esto existe: el caso exige que el
propio exec rompa a la vez el contrato del token, que va inyectado en cada prompt, y la
disciplina de entregar o declararse bloqueado. Y cuando ocurre deja siempre un rastro
firmado y atribuible, un par acquire/release sin entrega en medio, visible en la revision
de la demora. El caso de la iteracion 1 no dejaba nada. Pero el mandato de la unidad madre
es que un exec sin trabajo util no consuma el mensaje, y un claim vacio no es trabajo
util aunque el ledger lo registre como un flip.
