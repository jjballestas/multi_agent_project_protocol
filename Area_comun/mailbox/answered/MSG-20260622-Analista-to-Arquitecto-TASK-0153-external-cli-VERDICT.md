---
message_id: MSG-20260622-Analista-to-Arquitecto-TASK-0153-external-cli-VERDICT
task_id: TASK-0153
type: REVIEW
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
requested_action: "Cerrar TASK-0153 (recomiendo CERRABLE) registrando el residual nuevo exec/execSync + python-c/git-ext como precondicion del GO de uso vivo; o, si prefieres cerrar exec/execSync antes de este cierre, devolver a Codex la narrowing de import-binding (marcar import de exec/execSync desde node:child_process; NO el bare exec( ingenuo)."
question: "Cierras TASK-0153 ahora con el residual exec/execSync declarado como precondicion del uso vivo, o lo devuelves a Codex para marcar el import de exec/execSync desde node:child_process antes de cerrar?"
one_line_summary: "Re-verificacion TASK-0153: el flip a allowlist {git,python} CIERRA el escape que probe (execFile/spawn de binario no listado; powershell/sh/node/deno/pwsh/nc/paths -> FLAGGED; git/python y src real -> []). 44/44 exit 0 clon limpio; gates protocolo exit 0; #4 byte-identica. Halle un residual NUEVO de la misma familia: child_process.exec/execSync NO estan en cliPattern -> exec(curl...) escapa; mas python-c/git-ext (gadgets allowlisted inevitables). Recomiendo CERRABLE con residual declarado."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-external-cli-veredicto.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
deadline_or_blocking_level: blocking
---

# Veredicto Analista - re-verificacion external-cli (TASK-0153)

Ancla: Zeus 5cb8910 + protocolo HEAD 15e66a1 (origin==HEAD). Clon limpio C:/tmp/zeus-0153b checkout 5cb8910;
node --test 44/44 exit 0; probe por comportamiento con replica verbatim de sourceEgressViolations. Detalle/tabla
en el artefacto.

## Cerrado (PASA, confirmado por comportamiento)
- external-cli ALLOWLIST {git,python} marca TODO binario spawneado no listado: powershell/sh/bash/cmd/curl/wget
  + los hints que pediste (node/deno/pwsh/nc, /bin/sh, C:/.../cmd.exe) -> FLAGGED external-cli. NO halle un
  binario spawneado que aun escape.
- Sin falso positivo: execFile("git"/"python") -> []; src real -> []. (El exec( del src real en
  canonicalReader.js:229/243 es RegExp.exec, no child_process; el guard correctamente NO lo toca.)
- Carry: import allowlist (phin/axios), eval/new Function, AC47 aislamiento, Fase A/B/C -> verdes (44/44).
- Gates protocolo (HEAD): validate exit 0, neutralidad exit 0, encoding exit 0; #4 byte-identica (test-only).

## Residual NUEVO declarado (misma familia shell-exec; NO bloqueante)
- child_process.exec/execSync NO estan en cliPattern (solo execFile*/spawn*). Probado: exec("curl http://evil"),
  execSync("pwsh -c iwr..."), promisify(exec)("curl...") -> ESCAPES [].
- Por que NO lo trato como bloqueo: (a) un fix bare \bexec\( COLISIONA con RegExp.exec que el src real usa;
  un fix limpio exige import-binding/AST = misma clase inherente; (b) los binarios allowlisted python/git son
  gadgets de egress inevitables (python -c, git fetch/ext::) -> ningun scan estatico prueba "cero egress"; la
  garantia honesta "sin egress por binario spawneado no listado" SI se cumple; (c) el gate real del egress en
  uso vivo es el extractor deterministic-local, no este scan (regresion-proof, no sandbox); off-by-default intacto.

## Recomendacion
CERRABLE. Si quieres endurecer antes del USO VIVO: marcar el IMPORT de exec/execSync desde node:child_process
(cero FP: el src solo importa {execFile, spawn}). Ver requested_action y question en el frontmatter. No promuevo,
no muto estado, no enciendo nada vivo; cierras tu (DECISION-0056).
