---
artifact_id: Analista-TASK-0296-volume-root-iter2-verdict
task_id: TASK-0296
reviewer: Analista
role: adversarial checker (maker != checker)
iteration: 2
created_at: 2026-07-27
local_time: "2026-07-27 01:25 (UTC+2)"
anchor_commit: 12b8d77ec949c58a762ba15565f6c1cf42505ce0
cited_commit: 94cdb27d1e28f9f08a4c5e4b4f0b2c782ee0038e
fix_commit: 9691312fa9745b4af80272bf921284de26a74d98
iter1_commit: 31680dd14b322a99a707c6322919cc0f7c30f535
verdict: OK-CLOSABLE
scope: protocol only (no product in scope; Nova-Budget / npm test NOT gated)
blocking_slips: 0
declared_residuals: 4
---

# VEREDICTO Analista - TASK-0296 iter 2 (raiz de volumen: retirada del TrimEnd)

**OK-CLOSABLE (GO).** **B2 esta cerrado** y lo esta por comportamiento, no por nombre de test: con
los 4 `.TrimEnd` retirados, `-ScanRoot 'D:/'` y `-ScanRoot 'D:\'` componen `--scan-root D:/` y
`--scan-root D:\` respectivamente, ambos resuelven a `D:\` (la raiz REAL), y la linea compuesta
ejecutada **como la ejecutaria el Task Scheduler** (`CreateProcess` con la cadena cruda y
`cwd = <raiz del repo>`, que es lo que fija `-WorkingDirectory $repoRoot`) escanea el **disco**:
exit 1 y las 2 violaciones reales de DECISION-0104 que hay en esta maquina, byte-identico a la
invocacion directa del monitor.

**B1 no se reabrio; quedo estrictamente mejor que en iter 1.** Sin el TrimEnd, una ruta terminada
en separador ya no llega *recortada* sino **verbatim**: `-ScanRoot 'D:\...\vol\'` produce el
argumento `D:\...\vol\` con el backslash final intacto, y `--known-repo` / `--max-depth` /
`--allow-home` siguen presentes (12 tokens, 3/3 flags). Lo mismo con un `-AllowHome` que combina
**espacio y backslash final** (`D:\home dir\`), que es el caso que rompia el argv antes del quoting.

**No encontre un B3.** Ataque el algoritmo de quoting con 14 payloads (raiz de share UNC, tres
backslashes finales, espacio + backslash final, comilla embebida, backslashes antes de comilla,
solo-separadores, barra unix final, espacio despues del backslash, `D:sub`, binding nativo de array
de dos raices) y no consegui romperlo: round-trip exacto en todos.

Los 4 residuales declarados abajo son **no bloqueantes**: ninguno es regresion, ninguno lo introduce
esta remediacion y ninguno afecta la ruta documentada en el runbook (`--scan-root <host-root>`).

## 1. Ancla canonica y reproduccion

La instruccion cita `94cdb27` (fix `9691312`). `origin/main` al arrancar: `12b8d77`. El delta
`94cdb27..12b8d77` es **solo** el MSG de RE-REVIEW (1 archivo, 35 lineas) y
`git diff 94cdb27 12b8d77 -- scripts/ examples/ Area_comun/protocol/ runtime/ protocol.config.json`
= **vacio**: lo juzgado es byte-identico en codigo a lo citado. Juzgo sobre `12b8d77`.

Clon limpio bajo el scratch root designado (DECISION-0104), nunca en la raiz del disco:

| Clon / directorio | Commit | Uso |
|---|---|---|
| `D:/Aegis_Scratch/multi_agent_project_protocol/an96i2` | `12b8d77` | objeto de revision (`git status --porcelain` vacio antes y despues; HEAD sin mover) |
| `.../an96bank` | -- | mi banco adversarial (instalador real + `CommandLineToArgvW` real + `CreateProcess` real) |
| `.../an96neg` | -- | esqueleto de mutacion (falsabilidad del test entregado) |
| `.../an96base` | -- | instaladores `c71c294` y `31680dd` extraidos para el diff de 3 vias |
| `.../an96fx2`, `.../an96fx3`, `.../an96negfx` | -- | fixtures (borrados al terminar) |

Cero artefactos fuera del scratch root. El clon revisado no se muto.

### Gates por exit code (todos en el clon limpio `an96i2`)

| Gate | Comando | Exit |
|---|---|---|
| Suite del maker | `python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/an96fx2` | **0** |
| Estado canonico | `python scripts/validate_collaboration_state.py` | **0** |
| Encoding | `python scripts/scan_encoding.py` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** |
| Drift del ledger | `python runtime/protocol_replay.py --check-drift` | **0** (`verdict=CLEAN up_to_seq=6450`) |
| Config pineado | `git diff --exit-code c71c294 12b8d77 -- protocol.config.json` | **0** (intacto, `sha256[:8]=2E35F26E`) |
| Banco adversarial propio (21 vectores) | `python an96bank/bank.py` | **0 SLIPS bloqueantes** |

La suite corre en 3-4 s y es estable: 3 corridas consecutivas exit 0, y deja **0 entradas
residuales** en su scratch.

## 2. B2 cerrado - medido end-to-end sobre el disco real

Metodo: componer con el **instalador real** (`-WhatIf`), parsear la linea con el
**`CommandLineToArgvW` real** (ctypes) y **ejecutar la linea compuesta tal cual** via
`CreateProcess` con `cwd = <raiz del repo>` (simulacion fiel de `-WorkingDirectory $repoRoot`).

| Vector | argumento compuesto | resuelve a | exit de la tarea | hallazgos | == invocacion directa |
|---|---|---|---|---|---|
| `-ScanRoot 'D:/'` | `D:/` | `D:\` | **1** | 2 (disco) | **si** (stdout/stderr/exit identicos) |
| `-ScanRoot 'D:\'` | `D:\` | `D:\` | **1** | 2 (disco) | **si** |

Los 2 hallazgos son violaciones **reales** de DECISION-0104 en esta maquina
(`D:\Agentes\multi_agent_project_protocol` y `D:\Agentes\runtime-test-instance`). Esa es la
diferencia con iter 1, donde la tarea instalada reportaba `exit 0` + `OK: no anomalies` de forma
permanente y silenciosa.

### Diff de 3 vias del instalador (mismo vector, misma maquina)

| Instalador | vector B1 (`...\vol\`) | vector B2 (`D:/`) | vector B2 (`D:\`) |
|---|---|---|---|
| `31680dd` iter1 | 12 tokens, valor **recortado** `...\vol` | `D:` (colapsada) | `D:` (colapsada) |
| `12b8d77` iter2 | 12 tokens, valor **verbatim** `...\vol\` | **`D:/`** | **`D:\`** |

(`c71c294` no aparece en la tabla porque el `-WhatIf` que imprime la linea compuesta no existia
todavia ahi; su estado de B1 quedo medido en el veredicto de iter 1.)

## 3. Vector por vector (banco propio, instalador real + parser real)

| Vec | Vector | Resultado |
|---|---|---|
| V1a | los 4 params de ruta terminados en separador -> argv exacto | **PASS** (12 tokens, valores byte-exactos) |
| V1b | tarea instalada == invocacion directa del monitor (fixture) | **PASS** (exit 1, `{nested-stray, stray-clone, stray-markers}` en ambos) |
| V1c | `--known-repo` / `--max-depth` / `--allow-home` sobreviven | **PASS** (3/3) |
| V2 | `-ScanRoot 'D:/'` sobre el disco real | **PASS** (preservada, resuelve `D:\`, exit 1, == directa) |
| V3 | `-ScanRoot 'D:\'` sobre el disco real | **PASS** (idem) |
| V4 | `-ScanRoot 'D:'` (designador de unidad pelado) | **RES-1** (pass-through; sigue siendo relativa a la unidad) |
| V5 | `'D:'` vs `'D:/'` dan el mismo comportamiento instalado | **RES-1** (no: 1 hallazgo del repo vs 2 del disco) |
| V6 | raiz de share UNC `\\server\share\` | **PASS** (round-trip exacto) |
| V7 | tres backslashes finales | **PASS** |
| V8 | espacio en la ruta + backslash final | **PASS** |
| V9 | comilla doble embebida | **PASS** |
| V10 | backslashes antes de una comilla embebida | **PASS** |
| V11 | argumento que son solo separadores (`\`) | **PASS** (ya no queda cadena vacia: cierra RES-8 de iter 1) |
| V12 | barra unix final | **PASS** |
| V13 | espacio despues del backslash final | **PASS** |
| V14 | ruta relativa a unidad con subdir (`D:sub`) | **PASS** (pass-through correcto) |
| V15 | binding nativo de array `-ScanRoot 'D:\','E:\'` | **PASS** (`"D:\\" "E:\\"`, ambas intactas) |
| V16 | `--scratch-root` / `--allow-home` con separador final normalizan aguas abajo | **PASS** (exit 1, set correcto) |
| V17 | `--known-repo` con barra final sigue casando el clon | **PASS** |
| V18 | detector read-only sobre el fixture | **PASS** (sha256 estable) |
| V19 | `-WhatIf` no registra tarea programada | **PASS** (`Get-ScheduledTask` count=0) |

El algoritmo de escape (`(\\*)"` -> duplicar + `\"`; `(\\+)$` -> duplicar) es correcto para
`CommandLineToArgvW` y no cedio ante ningun payload. Retirar el TrimEnd **no** rompio nada aguas
abajo: el scanner normaliza separadores finales por su cuenta (`_resolved()` en scan-root,
scratch-root y allow-home; `rstrip` / `urlparse().path.rstrip('/')` en `_repo_identity`), asi que
el cinturon era redundante, no protector (V16, V17).

## 4. Falsabilidad del test entregado (mutacion)

Criterio (c) exige que el test **enrojezca si la raiz se colapsa**. Lo verifique mutando el fix y
corriendo la suite entregada contra cada mutante (control sin mutar: exit 0).

| Mutante | Suite | Detalle |
|---|---|---|
| N1 - TrimEnd de vuelta solo en `--scan-root` | **exit 1 KILLED** | `installer argv round-trip mismatch` |
| N2 - TrimEnd de vuelta en los 4 params | **exit 1 KILLED** | `installer argv round-trip mismatch` |
| **N3 - revert COMPLETO a iter 1 (TrimEnd + `rstrip` de vuelta en la expectativa)** | **exit 1 KILLED** | `installer changed volume-root vector: 'D:' != 'D:/'` |
| N4 - romper el doblado de backslash final (reabrir B1) | **exit 1 KILLED** | `installer argv round-trip mismatch` |
| N5 - romper el escape de comilla embebida | exit 0 **SOBREVIVE** | ver RES-2 |

**N3 es la prueba decisiva:** el vector de raiz de volumen mata exactamente el defecto de iter 1
*aunque el maker vuelva a ajustar la expectativa del test*, que es como B2 paso en verde la primera
vez. Criterio (c) **cumplido**.

## 5. Residuales declarados (no bloqueantes)

**RES-1 - designador de unidad pelado `D:` sigue siendo relativo a la unidad.** No es regresion (se
comporta igual en toda la historia de la unidad) y `D:` **no es una raiz de volumen** en Windows
(`Path('D:').is_absolute()` es `False`); el instalador ahora hace pass-through fiel de lo que
escribio el operador. Pero el modo de fallo es el silencioso: con la configuracion del runbook,

```text
--scan-root "D:"   (cwd = raiz del repo)  -> exit 0, "OK: no scratch-discipline anomalies found."
--scan-root "D:/"  (cwd = raiz del repo)  -> exit 1, 2 ANOMALY reales
```

Matiz relevante para el seguimiento: el test entregado **fija** este comportamiento
(`for root_variant in (volume_root, ROOT.anchor, ROOT.drive)` asevera que `D:` se preserva como
`D:`, y la guarda `endswith(":")` solo se aplica a `volume_root`), de modo que (i) nada enrojecera
nunca si alguien instala con `D:`, y (ii) el endurecimiento natural -- que el instalador **rechace**
un `-ScanRoot` que sea un designador de unidad pelado, o lo normalice a `D:\` -- pondria ese test en
rojo y habria que actualizarlo junto con el guard. Fix sugerido: una linea de validacion en el
`param`/cuerpo del instalador. No bloquea porque el runbook documenta `--scan-root <host-root>` y
ambas grafias de host-root funcionan.

**RES-2 - el escape de comilla embebida no esta cubierto por la suite entregada.** El mutante N5
sobrevive en verde. El comportamiento **es correcto** (mis V9/V10 dan round-trip exacto), y `"` es
un caracter ilegal en rutas NTFS, asi que la severidad practica es minima; lo declaro para que no se
confunda "no cubierto" con "no funciona".

**RES-3 - la asercion de equivalencia del test es casi tautologica y escanea el volumen del host
dos veces.** En `run_scratch_discipline_cases.py:145-156`, `direct` y `composed` terminan siendo
**el mismo argv** cuando las aserciones previas pasan, asi que compara el programa consigo mismo;
lo que si aporta es riesgo: dos escaneos completos de la unidad del host, comparados
**byte-a-byte** en stdout/stderr. Si un directorio aparece o desaparece entre ambas corridas (maquina
de desarrollo con agentes concurrentes) la suite enrojece por una razon ajena al fix. Medido estable
3/3 hoy (3-4 s), pero es un vector de flake real y hace que un `examples/` deje de ser
host-independiente. La guarda que de verdad muerde es la de las lineas 134-144.

**RES-4 - `endswith(":")` en la linea 143 es codigo muerto** dado que `volume_root` (`D:/`) nunca
termina en `:` y la comparacion previa ya cubre el caso. Inocuo; lo anoto para que no se lea como
una teeth adicional que no es.

## 6. Recomendacion de cierre

**OK-CLOSABLE (GO)** para cerrar TASK-0296.

- B2 cerrado por comportamiento sobre el disco real, con las dos grafias de raiz de volumen.
- B1 no reabierto; el valor llega ahora verbatim (mejor que iter 1).
- Sin B3: 14 payloads de quoting y 21 vectores en total, 0 slips bloqueantes.
- Sin regresion en R1/R2/R3, monitor sin `--`, exit codes, read-only, neutralidad ni en el config
  pineado `2E35F26E`.
- El test entregado tiene teeth verificadas por mutacion (N1-N4 KILLED, incluido el revert completo).
- RES-1..RES-4 quedan declarados para una unidad de endurecimiento posterior, a criterio del
  Arquitecto y del Operador; ninguno bloquea este cierre.

---
Analista - checker adversarial independiente (maker != checker).
