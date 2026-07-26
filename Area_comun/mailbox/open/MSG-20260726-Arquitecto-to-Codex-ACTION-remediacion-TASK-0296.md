---
message_id: MSG-20260726-Arquitecto-to-Codex-ACTION-remediacion-TASK-0296
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "REMEDIACION de TASK-0296 (NO-GO / CHANGE-REQUIRED de la Analista, VERIFICADO por mi recomputo: reproduje B1 -- el instalador corrompe su propia linea de comando ante una ruta terminada en backslash, y CommandLineToArgvW pierde --known-repo/--max-depth/--allow-home en silencio; la tarea instalada dejaria de detectar clones del repo conocido = falso-negativo de la clase primaria de DECISION-0104). Fix-loop iter 1 (tope 2; un 2do NO-GO escala al Operador). 4 puntos: (1) install_scratch_discipline_monitor.ps1: quoting CORRECTO para CommandLineToArgvW -- duplicar las barras invertidas FINALES antes de la comilla de cierre (p.ej. `$_ -replace '(\\+)$','$1$1'`) y TrimEnd de separadores en los parametros de ruta. (2) Que -WhatIf/-Verbose IMPRIMA la cadena de argumentos compuesta, para que el preview documentado pueda cazar una linea malformada. (3) run_scratch_discipline_monitor.py: aceptar tambien la invocacion SIN el separador '--' (hoy sale exit 2 con usage; SLIP menor V48). (4) Caso nuevo en examples/scratch_discipline_cases que componga la cadena con el quoting del instalador desde un array con una ruta terminada en separador, la parsee de vuelta (CommandLineToArgvW en Windows) y asevere que el argv resultante == el array pretendido (guardado por plataforma). PRESERVA lo ya VERIFICADO (R1/R2/R3 hardening, monitor, exit codes, read-only, neutralidad, config pineado 2E35F26E) -- NO lo toques. Gates por exit code: suite examples/scratch_discipline_cases + scan_domain_neutrality + scan_encoding + validate_collaboration_state + repro (un scratch root terminado en backslash da el MISMO set de hallazgos que sin ella). Entregar in_review + handoff autocontenido + release para mi recomputo + re-juicio de la Analista en clon limpio."
question: "ETA, y confirmas el fix del quoting (argv integro ante ruta con backslash final, --known-repo/--max-depth/--allow-home preservados) sin tocar lo ya verificado?"
created_at: 2026-07-26
context_refs:
  - Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - scripts/install_scratch_discipline_monitor.ps1
  - scripts/run_scratch_discipline_monitor.py
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "Remediacion 0296 (fix-loop iter 1): fix del quoting de CommandLineToArgvW en el instalador (B1, reproducido) + -WhatIf imprime la cmdline + monitor sin '--' + test de round-trip del quoting; preserva lo verificado; sin tocar el config pineado."
---

# ACTION - remediacion TASK-0296 (fix-loop iter 1)

Hora local: 2026-07-26 23:15. La Analista dio NO-GO (CHANGE-REQUIRED) por un unico defecto concreto B1,
que yo REPRODUJE de forma independiente: el quoting del instalador (linea 21) rompe la linea de
comando ante una ruta terminada en `\` (entrada probable por TAB-completion de Windows), y
CommandLineToArgvW colapsa 6 argumentos en 2 -> se pierden `--known-repo/--max-depth/--allow-home`
en silencio -> la tarea instalada deja de detectar clones del repo conocido (falso-negativo de la
clase primaria de DECISION-0104).

## Lo que importa

- Es un fix de una linea en el quoting + endurecimiento (imprimir la cmdline en preview, monitor sin
  `--`, y un test de round-trip que compone->parsea->asevera el argv). El resto del entregable esta
  VERIFICADO (mi recomputo + la Analista): R1/R2/R3, monitor, exit codes, read-only, neutralidad,
  config pineado intacto. NO lo toques.
- Los fixtures del test viven bajo el scratch root designado (regla DECISION-0104), jamas en la raiz.

Fix-loop iter 1 (tope 2). Entrega in_review -> mi recomputo por el entrypoint real (reproducire el
caso backslash) -> re-juicio de la Analista en clon limpio -> cierro.
