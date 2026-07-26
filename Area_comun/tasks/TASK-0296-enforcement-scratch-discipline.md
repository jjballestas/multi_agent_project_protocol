---
task_id: TASK-0296
title: "[DECISION-0104] Enforcement del detector de scratch discipline: disparo automatico + hardening (depth/allowlist/fail-open warning) -- de detectable a enforced"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-26
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0104, DECISION-0098, DECISION-0018, TASK-0295]
linked_decisions: [DECISION-0104]
file: Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
intake:
  type: infra
  goal: Cerrar la brecha R1-R4 del veredicto de TASK-0295 (Analista-TASK-0295-detector-scratch-discipline-verdict). El detector scripts/scan_scratch_discipline.py esta ENTREGADO y read-only pero "detectable, no enforced": nada lo invoca automaticamente, por lo que DECISION-0104 cl.5b tiene teeth construidos que no muerden solos. Esta unidad (a) cablea un DISPARO AUTOMATICO del detector que entrega las anomalias DECISION-0018 al owner, y lo endurece con (b R1) --max-depth para cazar strays anidados, (c R2) allowlist de hogares canonicos para no flagear el propio repo-hub como ruido, y (d R3) warning visible cuando git es irresoluble (el fail-open deja de ser silencioso). Read-only y neutralidad se PRESERVAN; el config pineado (2E35F26E) NO se toca.
  acceptance:
    - DISPARO AUTOMATICO (R4): un mecanismo host-local (cron/higiene o runbook enforced con la scan-root correcta) invoca el detector de forma periodica o en un gate apropiado y ENTREGA los hallazgos como anomalia DECISION-0018 al owner (mailbox o equivalente). Documentado en el runbook. NO se cablea a CI (la raiz del disco es host-local; CI corre en clon limpio sin litter). NO se toca protocol.config.json pineado ni se anade el campo scratch_root al config pineado.
    - R1 --max-depth: flag opcional (default 1 = comportamiento actual, sin regresion) que permite escanear a profundidad N; con depth>=2 caza un stray anidado (dir con .git-a-conocido o marcadores atestados dentro de otra carpeta fuera del scratch root). Suite cubre depth-1 (igual que hoy) y depth-2 (caza el anidado que hoy se escapa).
    - R2 allowlist: --allow-home (repetible) y/o scratch_discipline.canonical_homes en config; un dir que sea un hogar canonico allowlisted NO se flagea aunque tenga marcadores atestados fuera del scratch root. Suite: el hub-home allowlisted se ignora, el stray real se sigue flagenado (cero falsos negativos por el allowlist).
    - R3 fail-open visible: cuando git es irresoluble para un candidato (gitfile corrupto, dubious ownership/safe.directory, git ausente del PATH), el detector emite un WARNING a stderr nombrando el candidato; el fail-open deja de ser silencioso. Suite reproduce el caso (p.ej. .git = archivo gitdir apuntando a basura) y asevera el warning en stderr.
    - Read-only y neutralidad PRESERVADAS: cero nuevos paths de escritura (auditoria de API mutante limpia); cero hardcode de rutas/marca; scan-roots/allowlist/depth por parametro CLI o config. Fixtures del test SIEMPRE bajo el scratch root designado (regla DECISION-0104), jamas en la raiz real del disco.
    - Gates verdes por exit code: suite extendida (examples/scratch_discipline_cases), scan_domain_neutrality, scan_encoding, validate_collaboration_state.
  verification_cmd:
    - python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root <scratch-root propio bajo Aegis_Scratch>
    - Demo dry-run del disparo automatico (mecanismo de cron/higiene) mostrando la entrega de la anomalia
    - python scripts/scan_domain_neutrality.py
    - python scripts/scan_encoding.py
    - python scripts/validate_collaboration_state.py
  scope_routes:
    - scripts/scan_scratch_discipline.py
    - scripts/
    - examples/scratch_discipline_cases/
    - personal/ (mecanismo de disparo si es un cron/higiene del runbook)
  out_of_scope:
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E), dataset N=500, reservadas N=6 -- FUERA (fondo intocable). En particular NO anadir scratch_root al config pineado (rompe el genesis).
    - Borrar/mover/reapear cualquier directorio -- el detector sigue READ-ONLY; la limpieza es manual, autorizada por el operador.
    - Cablear a CI/GitHub Actions -- FUERA (la raiz del disco es host-local; CI no la ve).
    - R5 (regla de marcadores 2-de-3) -- opcional, no requerido; si se aborda, con suite propia.
  risk: low
  estimate: M
---

# TASK-0296 - [DECISION-0104] Enforcement del detector de scratch discipline

Origen: residuales R1-R4 del veredicto de la Analista sobre TASK-0295
(`Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md`), declarados FUERA
del acceptance de 0295 (no lo bloquearon) pero materiales para que los teeth de DECISION-0104 cl.5b
muerdan de verdad. Hoy el detector es "detectable, no enforced". Esta unidad lo lleva a enforced:
disparo automatico (host-local, NO CI) + hardening de profundidad, allowlist de hogar canonico y
warning de fail-open. Preserva read-only y neutralidad; jamas toca el config pineado. Ciclo gobernado
normal: maker Codex -> recomputo del Arquitecto -> review adversarial de la Analista (clon limpio) ->
cierre.
