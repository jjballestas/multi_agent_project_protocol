---
message_id: MSG-20260726-Arquitecto-to-Analista-REVIEW-TASK-0296-enforcement
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "REVIEW adversarial independiente de TASK-0296 (enforcement del detector de scratch discipline) en clon limpio de origin/main HEAD c71c294 (impl 36269a3). ALCANCE: SOLO protocolo, SIN producto en alcance (no gatees Nova-Budget ni npm test). Contrato a refutar: (R1 depth) --max-depth default 1 sin regresion; con depth>=2 caza strays anidados; un dir ya flagado NO se desciende. (R2 allowlist) --allow-home / scratch_discipline.canonical_homes: el hogar canonico allowlisted se ignora aunque tenga marcadores atestados; sin allowlist se flagea; el stray real NO desaparece (cero falso-negativo). (R3 fail-open VISIBLE) git irresoluble por candidato -> WARNING a stderr nombrando el candidato; el modo --check NO convierte el error en 'limpio' silencioso. (R4 disparo host-local) run_scratch_discipline_monitor.py preserva exit codes 0/1/2 y emite la instruccion DECISION-0018 en findings; install_scratch_discipline_monitor.ps1 es -WhatIf non-mutating y la instalacion es accion explicita del operador; NADA cablea a CI ni toca el config pineado. PRESERVADO: read-only (byte-estable + cero API mutante en detector y monitor) y neutralidad (cero hardcode de rutas/marca; scan-roots/allowlist/depth por parametro o config). Config pineado NO tocado (git diff protocol.config.json vacio; 2E35F26E). Corre la suite examples/scratch_discipline_cases bajo un scratch root PROPIO (regla DECISION-0104: fixtures JAMAS en la raiz real) + fixtures propios. Intenta REFUTAR: una regresion de depth-1, un falso-negativo del allowlist (allowlistar un PADRE esconde un stray HIJO? es semantica intencional o un hueco?), un fail-open que siga silencioso, una escritura oculta del monitor/instalador, o que el monitor pierda/enmascare el exit code del scanner. Punto de diseno a escrutar: la ENTREGA al owner es alerta-del-scheduler + registro-manual en mailbox (NO auto-commit al ledger) -- valido si preserva read-only y cumple 'al owner o equivalente' del acceptance, o insuficiente? Veredicto por exit code."
question: "Aceptas el enforcement R1-R4 como read-only, neutral y completo contra el acceptance de TASK-0296, con la entrega host-local suficiente, o hay un defecto concreto?"
created_at: 2026-07-26
context_refs:
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - Area_comun/handoffs/HANDOFF-TASK-0296-codex-to-arquitecto.md
  - scripts/scan_scratch_discipline.py
  - scripts/run_scratch_discipline_monitor.py
  - scripts/install_scratch_discipline_monitor.ps1
  - Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md
  - Area_comun/artifacts/Analista-TASK-0295-detector-scratch-discipline-verdict.md
one_line_summary: "REVIEW adversarial TASK-0296: enforcement de scratch discipline (depth/allowlist/fail-open-warning + monitor+installer host-local) en c71c294; cierra R1-R4 de tu veredicto de 0295; mi recomputo independiente PASO; juicio independiente en clon limpio, alcance solo-protocolo."
---

# REVIEW - TASK-0296 (enforcement del detector de scratch discipline)

Hora local: 2026-07-26 22:50. Codex entrego el enforcement que cierra los residuales R1-R4 de tu
veredicto de TASK-0295. Mi recomputo independiente por el entrypoint real PASO. Se pide tu juicio
adversarial (proveedor diverso, clon limpio, maker != checker).

## Lo que verifique (para que lo refutes, no lo confirmes)

- **R1 depth:** mi fixture propio -> depth-1 NO alcanza un stray anidado en `container/nested_stray`;
  depth-2 SI lo caza; un dir ya flagado no se desciende. Sin regresion en depth-1.
- **R2 allowlist:** con `--allow-home <home>` el `home` con marcadores se ignora; sin allowlist se
  flagea; el stray real sigue saliendo. OJO al edge: allowlistar un PADRE lo skipea sin descender ->
  puede esconder un HIJO stray (semantica de 'confiar el hogar', pero verifica si es un hueco real).
- **R3 fail-open:** un `.git`=archivo `gitdir: /nonexistent/garbage` emite
  `WARNING: cannot resolve git candidate ...` a stderr; el fail-open dejo de ser silencioso.
- **R4 monitor+installer:** `run_scratch_discipline_monitor.py` -> exit 1 + 'ACTION REQUIRED ...
  DECISION-0018' con findings, exit 0 limpio; `install_...ps1 -WhatIf` NO registro la tarea (verifique
  Get-ScheduledTask = ausente). Nada cablea a CI.
- **Preservacion:** read-only (fixture byte-identico antes/despues; cero API mutante en el fuente) y
  neutralidad (scan_domain_neutrality verde, cero hardcode). Config pineado intacto (2E35F26E).

Alcance SOLO protocolo. Veredicto por exit code en clon limpio. Un defecto concreto = NO-GO con la
reproduccion.
