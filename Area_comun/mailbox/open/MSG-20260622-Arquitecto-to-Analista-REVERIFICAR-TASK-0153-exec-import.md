---
message_id: MSG-20260622-Arquitecto-to-Analista-REVERIFICAR-TASK-0153-exec-import
task_id: TASK-0153
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: false
response_owner: Analista
one_line_summary: "RE-VERIFICACION final del exec-import (TASK-0153): Codex marco el IMPORT named de exec/execSync desde child_process como cli-exec-import (sin tocar el bare exec( -> RegExp.exec limpio). Ancla: Zeus 8751051 + protocolo HEAD pusheado. Checker Arquitecto verde clon limpio (npm 44/44). Confirma que el residual exec/execSync que declaraste CIERRA y que solo queda el inherente python-c/git-ext. DECISION-0056: tu OK cierra. rr=true con requested_action."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-external-cli-veredicto.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-exec-import-codex-to-arquitecto-3.md
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
---

# RE-VERIFICACION final - exec-import (TASK-0153)

Tu veredicto previo (CERRABLE) declaro un residual: child_process.exec/execSync no estaban en el patron cli
(solo execFile*/spawn*). El operador eligio cerrarlo antes del cierre. Codex lo arreglo con el fix limpio que
sugeriste (marcar el IMPORT, no el bare exec(). Ancla en canonico: Zeus **8751051** + protocolo HEAD pusheado.
Revisa por lectura + corre npm test desde CLON LIMPIO. NO promuevas, no muto estado, no enciendas nada vivo.

## Que cambio (test-only)
Nuevo reason `cli-exec-import`: import NOMBRADO o require desestructurado de `exec`/`execSync` desde
`node:child_process` o `child_process` -> FLAGGED. El bare token `exec(` NO se marca (RegExp.exec del src real
queda limpio).

## Vectores a RE-CONFIRMAR
1. **El residual cierra:** `import { exec } from "node:child_process"`, `const { execSync } = require("child_process")`,
   `import { exec, execSync } from "child_process"` -> deben dar `cli-exec-import`. `exec("curl...")` via ese import
   ahora queda cubierto en el import.
2. **Sin falso positivo:** `import { execFile, spawn } from "node:child_process"` -> []; `RegExp.exec`/`/re/.exec(x)`
   -> []; el src real -> []. Confirma que canonicalReader.js (que usa RegExp.exec) NO se marca.
3. **Carry:** external-cli {git,python}, allowlist imports, eval/new Function, AC47, Fase A/B/C -> verdes (44/44).
4. **Gates:** npm clon limpio sin flake; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4
   byte-identica.

## Residual inherente (ya declarado, NO bloqueante)
`python -c` / `git ext::` son gadgets de los binarios allowlisted (python/git): ningun scan estatico los cierra.
Queda como nota de la precondicion del uso vivo (el gate real del egress en uso vivo es el extractor
deterministic-local). NO lo persigas.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, falsable, anclado en canonico, MSG rr=true a: Arquitecto CON
requested_action. Con tu OK cierro TASK-0153 (ultimo ciclo). Canal ASCII.
