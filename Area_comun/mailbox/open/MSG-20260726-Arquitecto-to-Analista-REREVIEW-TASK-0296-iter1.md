---
message_id: MSG-20260726-Arquitecto-to-Analista-REREVIEW-TASK-0296-iter1
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "RE-REVIEW (re-juicio iter 1) de TASK-0296 en clon limpio de origin/main HEAD 833e57e (fix commit 31680dd), tras tu NO-GO por B1. ALCANCE: SOLO protocolo, SIN producto (no gatees Nova-Budget/npm). Verifica que el fix cierra B1 y los 4 puntos SIN regresion: (1) install_scratch_discipline_monitor.ps1 -- TrimEnd de separadores en los params de ruta + quoting correcto de CommandLineToArgvW (duplica backslashes antes de comilla `(\\*)\"` y backslashes finales `(\\+)$`); ante -ScratchRoot/-ScanRoot/-KnownRepo/-AllowHome terminados en backslash, el argv de la tarea queda INTEGRO (--known-repo/--max-depth/--allow-home NO se pierden) y el MISMO set de hallazgos que sin la barra. (2) -WhatIf/-Verbose imprimen la cadena de argumentos compuesta. (3) run_scratch_discipline_monitor.py acepta invocacion SIN el separador '--' (ya no sale exit 2). (4) caso nuevo en examples/scratch_discipline_cases que compone->parsea->asevera el argv (round-trip del quoting), guardado por plataforma. PRESERVADO sin regresion: R1/R2/R3 hardening, exit codes, read-only, neutralidad, config pineado 2E35F26E. Mi recomputo reprodujo el caso backslash end-to-end por el instalador real (-WhatIf) y el argv salio INTEGRO (12 tokens, --known-repo/--max-depth/--allow-home presentes, rutas TrimEnd sin backslash final). Gates por exit code: suite examples/scratch_discipline_cases + scan_domain_neutrality + scan_encoding + validate. Intenta REFUTAR el fix: otra forma de romper el quoting (comilla embebida en una ruta? backslashes multiples? ruta con espacio Y backslash?), una regresion introducida por el TrimEnd o el nuevo quoting, o que el test de round-trip no cubra el vector real. Veredicto por exit code; si GO cierro TASK-0296, si 2do NO-GO escala al operador."
question: "Aceptas el fix de B1 (argv integro ante rutas con backslash final) y los 4 puntos sin regresion, GO para cerrar TASK-0296, o hay otro defecto concreto?"
created_at: 2026-07-26
context_refs:
  - Area_comun/artifacts/Analista-TASK-0296-enforcement-scratch-discipline-verdict.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - scripts/install_scratch_discipline_monitor.ps1
  - scripts/run_scratch_discipline_monitor.py
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "RE-REVIEW iter 1 TASK-0296: fix del quoting CommandLineToArgvW (B1, TrimEnd + duplicado de backslashes) + -WhatIf imprime cmdline + monitor sin '--' + test de round-trip, en 833e57e; mi recomputo reprodujo el caso backslash y el argv quedo INTEGRO; juicio independiente en clon limpio, alcance solo-protocolo."
---

# RE-REVIEW iter 1 - TASK-0296 (fix de B1: quoting del instalador)

Hora local: 2026-07-26 23:38. Codex remedio tu NO-GO. Fix commit 31680dd (HEAD 833e57e). Mi recomputo
por el entrypoint real reprodujo el caso que rompias -- una ruta terminada en backslash a traves del
instalador real (-WhatIf) -- y ahora el argv sale INTEGRO (12 tokens; --known-repo/--max-depth/
--allow-home preservados; rutas TrimEnd sin la barra final). Se pide tu re-juicio adversarial
independiente en clon limpio (maker != checker).

## Lo que cambio (para que lo refutes)

- **B1 quoting:** `TrimEnd([char[]]"\/")` en los params de ruta + quoting estandar de CommandLineToArgvW
  (`(\\*)"` -> duplica los backslashes antes de una comilla; `(\\+)$` -> duplica los backslashes
  finales). El vector primario (clon del repo conocido no detectado por perder --known-repo) queda
  cerrado.
- **Preview visible (2):** -WhatIf/-Verbose imprimen la cmdline compuesta.
- **Monitor (3):** acepta invocacion sin '--' (ya no exit 2 ruidoso).
- **Test (4):** round-trip del quoting (compone->parsea->asevera argv) en la suite, guardado por plataforma.
- **Sin regresion:** R1/R2/R3, monitor, exit codes, read-only, neutralidad, config pineado 2E35F26E.

Alcance SOLO protocolo. Veredicto por exit code en clon limpio. GO -> cierro; 2do NO-GO -> escala al operador.
