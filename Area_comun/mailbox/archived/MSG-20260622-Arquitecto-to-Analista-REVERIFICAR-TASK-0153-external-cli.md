---
message_id: MSG-20260622-Arquitecto-to-Analista-REVERIFICAR-TASK-0153-external-cli
task_id: TASK-0153
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: false
response_owner: Analista
one_line_summary: "RE-VERIFICACION del flip external-cli (TASK-0153) que TU pediste: external-cli paso de denylist a ALLOWLIST de binarios spawneados {git,python}. Ancla: Zeus 5cb8910 + protocolo HEAD pusheado. Checker Arquitecto verde clon limpio (npm 44/44). Confirma que el escape que probaste (execFile/spawn powershell|sh|curl) ahora se MARCA y que git/python siguen limpios, sin nuevo escape material. DECISION-0056: tu OK cierra. Por favor, tu MSG rr lleva requested_action (el anterior no lo traia)."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-guard-allowlist.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-external-cli-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# RE-VERIFICACION del flip external-cli (TASK-0153)

Tu pasada previa fue util: confirmaste AC46/AC47 enumerados verdes PERO probaste un escape NUEVO material
(external-cli denylist sobre child_process -> execFile/spawn("powershell"|"sh", curl/IWR) escapaba). Lo devolvi a
Codex y lo arreglo. Ancla en canonico: Zeus **5cb8910** + protocolo HEAD pusheado. Revisa por lectura + corre la
suite tu mismo desde CLON LIMPIO. NO promuevas, no muto estado, no enciendas nada vivo.

## Que cambio (acotado, test-only)
`external-cli` paso de denylist {curl,wget,ssh,nc,node} a **ALLOWLIST de binarios spawneados {git,python}**: marca
CUALQUIER `execFile`/`execFileSync`/`execFileAsync`/`spawn`/`spawnSync` cuyo primer arg (binario) NO este en la
lista permitida.

## Vectores a RE-CONFIRMAR (los que probaste ESCAPES deben ahora MARCARSE)
1. **El escape cierra:** `execFile("powershell",["-Command","Invoke-WebRequest..."])`, `spawn("sh",["-c","curl..."])`,
   `bash`/`cmd`/`curl`/`wget` -> deben dar `external-cli`. Mi probe independiente: los 5 dan FLAGGED [external-cli].
   Busca un binario de egress que AUN escape (p.ej. `node`, `deno`, `pwsh`, `nc`, un path absoluto a un shell) y
   reporta si lo hallas -- el allowlist {git,python} deberia marcar todo lo demas.
2. **Sin falso positivo:** `execFile("git", ...)` y `execFile("python", ...)` -> []. El src real -> [] (solo usa
   git/python). Confirma que no rompe el build legitimo.
3. **Carry intacto:** el allowlist de imports (phin/axios -> unallowlisted-import), eval/new Function ->
   dynamic-exec, import permitido fs/path -> [], AC47 aislamiento de env, y Fase A/B/C siguen verdes (44/44).
4. **Gates:** npm clon limpio sin flake; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4
   byte-identica (cambio test-only).

## Notas
- El residual de ofuscacion (concatenacion/computed-global) ya lo declaraste como limite inherente del scan
  estatico (NO bloqueante); el aislamiento real en uso vivo es el extractor deterministic-local.
- NO enciende el uso vivo del extractor (GO aparte del operador).
- Tu MSG de veredicto anterior llego con rr=true sin `requested_action` (dejo el validador rojo); por favor
  incluye `requested_action` esta vez.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, falsable, anclado en canonico, MSG rr=true a: Arquitecto con
requested_action. Con tu OK cierro TASK-0153 (y aplico la reconciliacion de requerimientos). Canal ASCII.
