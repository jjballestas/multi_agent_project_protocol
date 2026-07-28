---
task_id: TASK-0297
title: "Alinear el validador legacy .ps1 con el canonico .py (falso rojo por dedup case-insensitive + selector sobre claim archivado malformado)"
type: infra
status: review_approved
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-27
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0018]
file: Area_comun/tasks/TASK-0297-alinear-validador-ps1-con-py.md
intake:
  type: infra
  goal: El validador LEGACY scripts/validate_collaboration_state.ps1 diverge del canonico scripts/validate_collaboration_state.py y da EXIT 1 (falso rojo) sobre el estado actual del hub, mientras el .py -- que es el GATE REAL (lo corre .github/workflows/validate.yml y lo citan todas las skills) -- da EXIT 0. Alinear el .ps1 al .py para que ambos concuerden sobre el mismo estado, sin debilitar la deteccion de defectos reales. Se detectaron 2 divergencias el 2026-07-27 al arrancar sesion. (1) DEDUP CASE-INSENSITIVE: el merge de claims del .ps1 usa un hashtable $seen que en PowerShell es case-insensitive por defecto, por lo que colisiona DOS claims DISTINTOS que difieren solo en la mayuscula final (CLAIM-OPS-MAILBOX-HYGIENE-20260718B vs CLAIM-OPS-MAILBOX-HYGIENE-20260718b) y los reporta como "Duplicate claim across hot/archive" x3 -- falso positivo; el .py usa dicts case-sensitive y los distingue. (2) SELECTOR SOBRE CLAIM ARCHIVADO MALFORMADO: el .ps1 aplica el chequeo de row-selector a un claim ARCHIVADO cuyo scope esta malformado (CLAIM-20260721-Codex-TASK-0280-done: 4 rutas concatenadas en 1 solo string en vez de array de 4) y lo reporta "invalid row selector"; el .py no lo marca (exit 0). Ninguna de las dos toca el FONDO INTOCABLE (config 2E35F26E, epoch 1.14.0, dataset N=500) ni el .py.
  acceptance:
    - AC1 CONCORDANCIA - powershell -NoProfile -File scripts/validate_collaboration_state.ps1 sale EXIT 0 sobre el estado actual del hub, concordando con python scripts/validate_collaboration_state.py --root . (EXIT 0). El .py es autoritativo; el .ps1 se alinea a el.
    - AC2 NO-DEBILITAMIENTO (adversarial) - el fix alinea SOLO el trato de (a) case de claim_id y (b) claims ARCHIVADOS al del .py; NO debe dejar de cazar defectos reales. Con dos claims de claim_id IDENTICO (misma caja) inyectados en un clon, el .ps1 SIGUE detectando el duplicado real (EXIT 1). Con un claim HOT (no archivado) de scope genuinamente malformado (selector invalido), el .ps1 SIGUE marcandolo (EXIT 1). El checker verifica ambos vectores adversariales en clon limpio.
    - AC3 ALCANCE - el cambio es SOLO en scripts/validate_collaboration_state.ps1. El .py NO se toca (ya verde). El dato archivado de TASK-0280 NO se reescribe (no se toca la historia del archive). El fondo pineado NO se toca.
  verification_cmd:
    - powershell -NoProfile -File scripts/validate_collaboration_state.ps1; echo PS_EXIT=$?
    - python scripts/validate_collaboration_state.py --root .; echo PY_EXIT=$?
    - python scripts/scan_encoding.py
  scope_routes:
    - scripts/validate_collaboration_state.ps1
  out_of_scope:
    - scripts/validate_collaboration_state.py -- canonico, ya verde, NO tocar.
    - El dato del claim archivado CLAIM-20260721-Codex-TASK-0280-done (scope concatenado) -- reescribir la historia del archive es una decision aparte con riesgo de drift en instancia runtime-authoritative; FUERA de esta unidad.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E), dataset N=500 -- fondo intocable.
    - Cualquier cambio de gate/CI o del validador canonico.
  risk: low
  estimate: S
---

# TASK-0297 - Alinear el validador legacy .ps1 con el canonico .py

Origen: al arrancar la sesion del 2026-07-27 el Arquitecto corrio por error el validador LEGACY
scripts/validate_collaboration_state.ps1 (secundario; NO es el gate) y obtuvo EXIT 1 con 4 "errores".
El gate CANONICO -- scripts/validate_collaboration_state.py, el que corre CI (.github/workflows/
validate.yml) y citan todas las skills -- da EXIT 0 "OK: collaboration state is valid" sobre el mismo
estado. Es decir: el hub esta VERDE; el rojo era un artefacto del .ps1 legacy. El Operador pidio
encolar el fix OPCIONAL del .ps1 para dejar las dos herramientas consistentes.

Las 2 divergencias (evidencia recogida por el Arquitecto):

1. Dedup case-insensitive. El .ps1 fusiona hot+archive por claim_id en un hashtable $seen (PowerShell
   default = case-INsensitive). Dos claims distintos que difieren solo en la mayuscula final
   (`...20260718B` idx 1493, started 2026-07-17T22:32 -- y `...20260718b` idx 1500, started
   2026-07-18T04:28) colisionan -> "Duplicate claim across hot/archive" (x3, tambien c-1/c-2). El .py
   (dicts case-sensitive) los trata como distintos -> no hay duplicado. Fix natural: comparador
   Ordinal (case-sensitive) en el $seen, igual que el .py autoritativo.

2. Selector sobre claim archivado malformado. El claim archivado CLAIM-20260721-Codex-TASK-0280-done
   tiene un scope malformado: un solo string con 4 rutas concatenadas por espacios en vez de un array
   de 4 elementos. El .ps1 parte por el primer '#' y valida el resto como selector -> falla "invalid
   row selector". Ya estaba asi en el archive ANTES de la ultima poda (fcb9d43); no lo introdujo esa
   poda. El .py da exit 0 sobre el mismo dato. Fix: alinear el trato de claims ARCHIVADOS al del .py
   (el checker confirma que el .py no marca esto y que el .ps1 alineado tampoco, sin dejar de marcar
   selectores malformados en claims HOT vigentes).

Ciclo gobernado normal: maker Codex -> recomputo independiente del Arquitecto -> review adversarial de
la Analista en clon limpio (vectores AC2) -> ratificacion -> done-flip por Codex. Riesgo bajo:
herramienta legacy secundaria, el gate real .py ya esta verde; no toca fondo ni el .py.
