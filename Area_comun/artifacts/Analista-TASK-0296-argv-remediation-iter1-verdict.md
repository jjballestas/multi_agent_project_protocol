---
artifact_id: Analista-TASK-0296-argv-remediation-iter1-verdict
task_id: TASK-0296
reviewer: Analista
role: adversarial checker (maker != checker)
iteration: 1
created_at: 2026-07-27
local_time: "2026-07-27 00:02 (UTC+2)"
anchor_commit: 833e57e18819bba7792a7fbec9eb4d9dd06c8c9f
fix_commit: 31680dd14b322a99a707c6322919cc0f7c30f535
baseline_commit: c71c2948bae6bae391b6cf6c94a8a5471930796f
verdict: CHANGE-REQUIRED
escalation: second NO-GO -- declared loop exhausted, escalates to the human owner
scope: protocol only (no product in scope; Nova-Budget / npm test NOT gated)
---

# VEREDICTO Analista - TASK-0296 iter 1 (remediacion del argv del instalador)

**CHANGE-REQUIRED (segundo NO-GO).** B1 esta **cerrado**: con el quoting corregido, una ruta
terminada en separador atraviesa `CommandLineToArgvW` **integra** y la tarea instalada produce el
**mismo set de hallazgos** que la invocacion limpia. Los puntos 2, 3 y 4 estan entregados y
verificados por comportamiento. No encontre regresion en R1/R2/R3, exit codes, read-only,
neutralidad ni en el config pineado.

El bloqueo nuevo es **B2, y lo introduce la propia remediacion**: el `TrimEnd([char[]]"\/")` que se
agrego como cinturon adicional **destruye la raiz de volumen**. `-ScanRoot 'D:\'` (y `'D:/'`, y
`'D:'`) se convierte en el argumento `--scan-root D:`, que en Windows **no** es la raiz del disco
sino el *directorio actual de esa unidad*. Como la tarea se registra con
`-WorkingDirectory $repoRoot` y el monitor lanza el scanner con `cwd=<raiz del repo>`, la tarea
programada termina escaneando **la propia raiz del repo** en vez del volumen entero, y reporta
`exit 0` + `OK: no scratch-discipline anomalies found.` de forma **permanente y silenciosa**.

Escanear la raiz del disco no es un caso exotico: es **el** caso de DECISION-0104 ("nunca en la raiz
del disco"), es lo que documenta el runbook (`--scan-root <host-root>`) y es exactamente lo que
usamos tanto tu recomputo como mi repro de iter 0 (`D:/`). Y `D:/` **funcionaba antes del fix**.

Es la misma familia de fallo que B1 -- teeth instalados que no muerden -- pero **estrictamente peor
en detectabilidad**: B1 dejaba la corrida corrupta con `exit 1` y `ACTION REQUIRED` (ruidosa, aunque
con el set equivocado); B2 la deja en `exit 0`, stdout "limpio" y stderr vacio. El disparador de
entrega que documenta el runbook ("alert the responsible owner on any nonzero exit") **nunca se
dispara**.

## 1. Ancla canonica y reproduccion

Ancla citada: `833e57e` (fix `31680dd`). `origin/main` al arrancar: `8f93429`; el delta
`833e57e..8f93429` es **solo** el MSG de RE-REVIEW (1 archivo, 40 lineas), y
`git diff 833e57e 8f93429 -- scripts/ examples/ Area_comun/protocol/` = **vacio**: lo juzgado es
byte-identico a `origin/main` en codigo. `git diff 31680dd 833e57e -- scripts/ examples/` = vacio.

Clones (bajo el scratch root designado, DECISION-0104):

| Clon | Commit | Uso |
|---|---|---|
| `D:/Aegis_Scratch/multi_agent_project_protocol/an96r1` | `833e57e` | objeto de revision (`git status --porcelain` vacio antes y despues) |
| `D:/Aegis_Scratch/multi_agent_project_protocol/an96pre` | `c71c294` | baseline pre-fix para medir regresion |

Fixtures propios en `.../an96fx`, `.../an96mfx`, `.../an96b1`. Cero artefactos fuera del scratch
root. El clon revisado no se muto.

Gates por exit code, todos en el clon limpio `an96r1`:

| Gate | Comando | Exit |
|---|---|---|
| Suite del maker | `python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/an96fx` | **0** |
| Estado canonico | `python scripts/validate_collaboration_state.py` | **0** |
| Encoding | `python scripts/scan_encoding.py` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** |
| Drift del ledger | `python runtime/protocol_replay.py --check-drift` | **0** (`verdict=CLEAN up_to_seq=6440`) |
| Config pineado | `git diff --exit-code c71c294 833e57e -- protocol.config.json` | **0** (intacto, `sha256[:8]=2E35F26E`) |
| Banco adversarial propio (quoting) | `python adv0296r1.py` + `adv2.py` + `e2e.py` + `b1check.py` | **1 SLIP bloqueante (B2)** |

La suite deja 0 entradas residuales en su scratch.

## 2. B1 esta cerrado (credito donde toca)

Metodo: componer con el **instalador real** (`-WhatIf`), leer la linea que ahora imprime, parsearla
con el **`CommandLineToArgvW` real** (ctypes), y ademas **ejecutar la linea compuesta tal cual la
ejecutaria el Task Scheduler** (`CreateProcess` con la cadena cruda `"<python>" <Arguments>` y
`cwd=<raiz del repo>`), contra un fixture propio.

| Invocacion del instalador | argv resultante | exit | hallazgos |
|---|---|---|---|
| `-ScanRoot <fix>/vol` (sin separador final) | 12 tokens, 5/5 flags | **1** | `{nested-stray, stray-clone}` |
| `-ScanRoot <fix>/vol\` (con backslash final) | 12 tokens, 5/5 flags | **1** | `{nested-stray, stray-clone}` |
| idem con el instalador **pre-fix** `c71c294` | argv corrupto | **2** | -- |

Set identico con y sin la barra: **B1 cerrado por comportamiento**, no por nombre de test.

## 3. Vector por vector del quoting (banco propio, instalador real + parser real)

| Vector | Entrada | Resultado |
|---|---|---|
| W1 | los 4 params de ruta terminados en `\` | **PASS** argv exacto (12 tokens; `--known-repo`/`--max-depth`/`--allow-home` presentes) |
| W3 | ruta con **espacio** y `\` final | **PASS** valor intacto |
| W4 | comilla embebida en la ruta | **PASS** round-trip exacto |
| W5 | 3 backslashes finales | **PASS** |
| W6 | backslashes **antes** de una comilla embebida | **PASS** round-trip exacto |
| W7 | `/` final (estilo unix) | **PASS** |
| W8 | raiz de recurso UNC `\\server\share\` | **PASS** conserva el share |
| W9 | `-KnownRepo` como ruta local con separador final | **PASS** |
| W12 | comilla **y** backslash final en el mismo argumento | **PASS** |
| W13 | argumento que son solo separadores | PASS (queda cadena vacia; residual RES-8) |
| W14 | espacio despues del backslash final | **PASS** |
| W15 | `-WhatIf` no registra nada | **PASS** (`Get-ScheduledTask` = 0 antes y despues, rc=0) |
| W10 | array `-ScanRoot 'D:\','E:\'` desde prompt nativo | binding correcto (2 ocurrencias), pero ambos colapsan por B2 |
| **W2 / W7b** | **`-ScanRoot 'D:\'` / `'D:/'` / `'D:'`** | **SLIP BLOQUEANTE (B2)** -- ver 4 |

El algoritmo de escape en si (`(\\*)"` -> duplicar + `\"`; `(\\+)$` -> duplicar) es **correcto** para
`CommandLineToArgvW`; no consegui romperlo con ningun payload.

## 4. El bloqueo: B2 -- el TrimEnd destruye la raiz de volumen

`install_scratch_discipline_monitor.ps1:16-19` aplica `.TrimEnd([char[]]"\/")` a `-ScanRoot`,
`-ScratchRoot`, `-KnownRepo` y `-AllowHome`. Para cualquier ruta con componentes eso es inocuo. Para
una **raiz de volumen** no lo es: `'D:\'.TrimEnd('\','/')` = `'D:'`, y `D:` es una ruta
**relativa a la unidad**, no la raiz.

Medido (`Path('D:').expanduser().resolve(strict=False)` con `cwd` = clon):

```
'D:'   -> 'D:\Aegis_Scratch\multi_agent_project_protocol\an96r1'   <- el cwd del proceso
'D:\'  -> 'D:\'
'D:/'  -> 'D:\'
```

### 4.1 Efecto end-to-end (simulacion fiel del Task Scheduler, host real, read-only)

Cadena completa: instalador real `-WhatIf` -> linea compuesta -> `CreateProcess` con esa cadena
cruda -> `cwd = <raiz del repo>` (que es lo que fija `-WorkingDirectory $repoRoot`).

| Instalador | `-ScanRoot` | argumento compuesto | exit de la tarea | salida |
|---|---|---|---|---|
| **pre-fix `c71c294`** | `D:/` | `--scan-root D:/` | **1** | `ANOMALY: D:\Agentes\runtime-test-instance` + `ACTION REQUIRED` |
| **fix `833e57e`** | `D:/` | `--scan-root D:` | **0** | `OK: no scratch-discipline anomalies found.` |
| **fix `833e57e`** | `D:\` | `--scan-root D:` | **0** | `OK: no scratch-discipline anomalies found.` |

`D:\Agentes\runtime-test-instance` es una violacion **real** de DECISION-0104 en esta maquina (es la
que el detector de 0295 no veia y que 0296 existe para cazar). Con la tarea instalada segun el fix,
**desaparece**, sin warning, sin stderr, con exit 0.

Confirmado tambien por el monitor directo:

```
python scripts/run_scratch_discipline_monitor.py --scan-root "D:/" ...  -> exit 1, findings=[D:\Agentes\runtime-test-instance]
python scripts/run_scratch_discipline_monitor.py --scan-root "D:"  ...  -> exit 0, findings=[], stderr vacio
```

### 4.2 Es una regresion, no un hueco preexistente

`-ScanRoot 'D:/'` (sin backslash final) **no pasaba por el defecto B1** y por tanto **funcionaba** en
`c71c294`: argv de 12 tokens, 5/5 flags, `--scan-root D:/`. El fix lo rompe. Comparacion directa
(replay mecanico del bloque de composicion del instalador pre-fix, extraido del propio archivo):

| Instalador | `-ScanRoot 'D:/'` | `-ScanRoot 'D:\'` | `-ScanRoot 'D:/Agentes/'` |
|---|---|---|---|
| pre-fix `c71c294` | `D:/` (**correcto**) | corrupto, argc=4, 1/5 flags | `D:/Agentes/` (correcto) |
| fix `833e57e` | **`D:`** (roto, silencioso) | **`D:`** (roto, silencioso) | `D:/Agentes` (correcto) |

Y no queda **ninguna** forma documentada de expresar "escanea el volumen entero" a traves del
instalador: `D:\`, `D:/` y `D:` colapsan todos a `D:`. Solo funcionan trucos no documentados
(`D:\.`, `D:\..`), que ningun runbook menciona.

### 4.3 El test de round-trip nuevo no puede cazarlo (respuesta a tu tercera hipotesis)

El caso nuevo calcula su expectativa como `scan_arg.rstrip("\\/")`, es decir **asume el TrimEnd como
la intencion**. Aplicado a una raiz de volumen, `parsed == intended` y el test **pasa en verde**
mientras la tarea instalada queda ciega:

```
B) asercion del maker aplicada a -ScanRoot 'D:\':
   parsed  = [... '--scan-root', 'D:', ...]
   intended= [... '--scan-root', 'D:', ...]
   ASSERTION RESULT: PASSES (green)
   el operador pidio escanear 'D:\' y la tarea escaneara 'D:\Aegis_Scratch\multi_agent_project_protocol'
```

El test compara el argv contra **el array ya recortado**, no contra **lo que el operador pidio**. Es
tautologico respecto del recorte: cubre el quoting (bien) pero no la intencion.

### 4.4 El TrimEnd no hace falta

Extraje el bloque de escape real del instalador y lo aplique a un array **sin recortar**:

```
composed: "--scan-root" "D:\Aegis_Scratch\fix\vol\\" "--scratch-root" "D:\\" "--max-depth" "2" "--allow-home" "D:\home dir\\"
parsed  == intended  -> True   (round-trip EXACTO, incluida la raiz 'D:\' y una ruta con espacio)
```

El quoting corregido **por si solo** resuelve B1, raices de volumen y rutas con espacios. El
`TrimEnd` es redundante para el objetivo y es la **causa unica** de B2. (Lo propuse yo en iter 0 como
cinturon adicional; retiro la sugerencia: el cinturon es el que rompe el pantalon.)

## 5. Puntos 2, 3 y 4: verificados

| Punto | Verificacion | Resultado |
|---|---|---|
| (2) preview visible | `-WhatIf` imprime `Scheduled task arguments: <linea>`; `-Verbose` tambien (2 emisiones medidas) | **PASS** |
| (3) monitor sin `--` | `--scan-root ...` sin separador -> exit 1, **stdout byte-identico** a la forma con `--` | **PASS** |
| (3) exit codes preservados | sin args -> **2**; `--check` duplicado por el llamador -> **1**; `--max-depth 0` -> **2**; arbol limpio -> **0** sin `ACTION REQUIRED` | **PASS** |
| (4) test de round-trip | ejecuta el instalador **real** y parsea con `CommandLineToArgvW` **real**; guardado por `sys.platform != "win32"` | **PASS** como mecanismo; **insuficiente** en cobertura (4.3) |

## 6. Sin regresion (verificado)

| Item | Evidencia |
|---|---|
| R1/R2/R3 hardening | `git diff c71c294 833e57e -- scripts/scan_scratch_discipline.py` = **vacio** (el detector no se toco); suite del maker exit 0; fixture propio a depth 2 devuelve `{canonical-home, nested-stray, stray-clone}` |
| Read-only | 0 ocurrencias de API mutante en `run_scratch_discipline_monitor.py`; unica API mutante del instalador sigue siendo `Register-ScheduledTask` dentro de `ShouldProcess`; `-WhatIf` no registro nada |
| Neutralidad | `scan_domain_neutrality.py` exit 0 |
| ASCII | 0 bytes > 127 en los 3 archivos tocados |
| Config pineado | byte-identico, `2E35F26E` |
| Estado canonico | `validate` exit 0, drift `CLEAN` |

## 7. Remediacion esperada (loop declarado agotado -- ver 9)

1. `install_scratch_discipline_monitor.ps1`: **quitar los cuatro `.TrimEnd([char[]]"\/")`** (el
   quoting corregido ya cubre el caso, seccion 4.4). Si se quiere conservar la normalizacion, hacerla
   **consciente de la raiz**: no recortar cuando el resultado deje de ser una ruta absoluta con
   componentes, p.ej. saltar el recorte si
   `[System.IO.Path]::GetPathRoot($p) -eq (Join-Path $p '')` o simplemente si el recorte produce algo
   que termina en `:`.
2. Test: cambiar la expectativa del caso nuevo para que compare contra **el valor que el operador
   paso** (sin `rstrip`), y **anadir un vector de raiz de volumen** (`<unidad>:\`) que asegure que el
   argumento compuesto sigue resolviendo a la raiz y **no** al cwd. Sin ese vector el test seguira
   verde sobre un instalador roto.
3. Gate de comportamiento a re-correr, por exit code: la linea compuesta por el instalador con
   `-ScanRoot <raiz de volumen>` debe producir **el mismo set de hallazgos y el mismo exit** que la
   invocacion directa `--scan-root <raiz de volumen>` del monitor, ejecutada con
   `cwd = <raiz del repo>`.
4. Gates: suite `examples/scratch_discipline_cases`, `scan_domain_neutrality`, `scan_encoding`,
   `validate_collaboration_state`, drift.

## 8. Residuales declarados (no bloquean)

Siguen vigentes **RES-1 .. RES-7** de mi veredicto de iter 0
(`Analista-TASK-0296-enforcement-scratch-discipline-verdict.md`), ninguno tocado por esta
remediacion. Anado:

**RES-8 - argumento de ruta vacio.** `-ScanRoot '\\\\'` (solo separadores) queda como cadena vacia
tras el TrimEnd; el scanner la resuelve al cwd. Mismo mecanismo que B2, menor probabilidad.

**RES-9 - el test nuevo falla (no salta) sin PowerShell.** En un host Windows sin `powershell` ni
`pwsh` el caso lanza `AssertionError` en vez de saltarse. En CI no aplica (guardado por plataforma),
pero es un falso rojo posible en un host de desarrollo.

**RES-10 - `--help` del monitor.** Al retirar `argparse`, `--help` se reenvia al scanner y muestra el
usage de `scan_scratch_discipline.py` con exit 0. Cosmetico, sin impacto en el contrato.

## 9. Recomendacion de cierre y escalada

**CHANGE-REQUIRED. NO-GO.** No es cerrable: bajo la configuracion canonica de DECISION-0104 (escanear
la raiz del disco) la tarea instalada reporta limpio para siempre, en silencio, y ademas es una
**regresion** respecto de `c71c294`.

Mi loop declarado en iter 0 era de **maximo 2 iteraciones**; esta es la iteracion 1 y su re-juicio es
NO-GO, luego **por regla escala al operador humano**. Contexto justo para esa decision, no soy yo
quien la toma:

- B1, el bloqueo original, **si quedo cerrado**; B2 es un defecto **nuevo**, introducido por el
  cinturon adicional que yo mismo sugeri, no un fallo en corregir B1.
- El fix es una **supresion** de cuatro llamadas `.TrimEnd(...)` mas un vector de test; no hay diseno
  que rehacer.

Si el operador autoriza una iteracion 2 acotada a los puntos 7.1-7.3, la re-juzgo con el mismo banco
y el mismo gate de comportamiento. Si no, la unidad queda abierta con B2 documentado.

-- Analista (checker independiente, TASK-0296 iter 1)
