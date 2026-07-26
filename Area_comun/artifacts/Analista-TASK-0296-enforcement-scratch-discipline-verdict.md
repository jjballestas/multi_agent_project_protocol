---
artifact_id: Analista-TASK-0296-enforcement-scratch-discipline-verdict
task_id: TASK-0296
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-07-26
local_time: "2026-07-26 23:04 (UTC+2)"
anchor_commit: c71c2948bae6bae391b6cf6c94a8a5471930796f
implementation_commit: 36269a3e271494818279c19c4a051063f91d3a93
verdict: CHANGE-REQUIRED
scope: protocol only (no product in scope; Nova-Budget / npm test NOT gated)
---

# VEREDICTO Analista - TASK-0296 (enforcement de scratch discipline)

**CHANGE-REQUIRED.** 51/52 vectores adversariales PASS y los cuatro residuales R1-R4 de mi veredicto
de TASK-0295 estan **cerrados por comportamiento** -- lo comprobe end-to-end contra la maquina real:
el entrypoint de enforcement caza hoy el stray real `D:\Agentes\runtime-test-instance` que el
detector de 0295 no veia, sin ruido del hogar canonico y con el fail-open ya visible. El hardening
del scanner es solido y read-only.

El bloqueo es **uno solo y esta en el instalador**, no en el detector: bajo la entrada de operador
mas natural en Windows (una ruta de directorio completada con TAB, que PowerShell termina en `\`),
`install_scratch_discipline_monitor.ps1` compone una linea de comando **corrupta** y registra una
tarea programada que **silenciosamente pierde `--known-repo`, `--max-depth`, `--allow-home` y
`--json`**. El resultado es una revocacion de facto del hardening R1+R2 y un **falso negativo** sobre
la clase primaria de DECISION-0104 (clon del repo conocido fuera del scratch root) -- mientras la
tarea sigue saliendo con exit 1 y `ACTION REQUIRED`, o sea indistinguible de una corrida sana. El
`-WhatIf` documentado como verificacion **no imprime la cadena de argumentos**, asi que la
verificacion que se ofrece al operador es ciega a este defecto.

Es el modo de fallo exacto que esta unidad existe para eliminar: teeth instalados que no muerden.

## 1. Ancla canonica y reproduccion

Ancla: `c71c294` (HEAD citado). `origin/main` local al arrancar: `0a5ede8`; el delta
`c71c294..0a5ede8` es **solo** el MSG de REVIEW del Arquitecto (1 archivo, 45 lineas). `git diff
36269a3 c71c294 -- scripts/ examples/ Area_comun/protocol/` = **vacio**: lo revisado es
byte-identico al commit de implementacion.

Clon limpio bajo el scratch root designado (DECISION-0104):
`D:/Aegis_Scratch/multi_agent_project_protocol/an0296` (`git status --porcelain` vacio antes y
despues). Baseline de no-regresion: segundo clon `.../an0296old` en `3aa332d` (detector pre-0296,
0 ocurrencias de `max-depth`/`allow-home`/`WARNING`). Fixtures propios en `.../an0296fx`,
`.../an0296fxsuite`; banco adversarial en `.../an0296adv`. Cero artefactos fuera del scratch root.

Gates por exit code, todos en el clon limpio:

| Gate | Comando | Exit |
|---|---|---|
| Suite del maker | `python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/an0296fxsuite` | **0** |
| Estado canonico | `python scripts/validate_collaboration_state.py` | **0** |
| Encoding | `python scripts/scan_encoding.py` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py` | **0** |
| Config pineado | `git diff --exit-code 3aa332d c71c294 -- protocol.config.json` | **0** (intacto) |
| Banco adversarial propio (52 vectores) | `python adversarial_0296.py <clon> <fixtures>` | **1** (1 SLIP: R4-V48, ver 4) |

La suite del maker limpia sus fixtures: el scratch de la suite queda con 0 entradas.

## 2. Prueba de que los teeth muerden (maquina real, read-only)

```
python scripts/run_scratch_discipline_monitor.py -- --scan-root D:/ --scratch-root D:/Aegis_Scratch \
  --known-repo D:/Agentes/multi_agent_project_protocol --known-repo D:/Agentes/Zeus/Zeus-protocol-Aegis \
  --allow-home D:/Agentes/multi_agent_project_protocol --allow-home D:/Agentes/Zeus/Zeus-protocol-Aegis \
  --max-depth 2 --json
-> exit 1
   findings: D:\Agentes\runtime-test-instance  (contains attested tree markers)
   stderr:   WARNING: cannot resolve git candidate D:\Agentes\audit-anchor: git exited 1
             WARNING: cannot resolve git candidate D:\Agentes\protocol_research: git exited 1
             WARNING: cannot resolve git candidate D:\Agentes\runtime-test-instance: git exited 1
             WARNING: cannot inspect candidate D:\System Volume Information: [WinError 5] ...
             ACTION REQUIRED: deliver these host-local findings to the responsible owner as a
             DECISION-0018 anomaly.
```

Contra la misma maquina, el detector de 0295 daba `exit 0, FINDINGS 0` apuntando a `D:/`, y
`exit 1, FINDINGS 2` (uno de ellos el propio hub como ruido) apuntando a `D:/Agentes`. R1, R2, R3 y
R4 quedan cerrados por comportamiento, no por nombre de test.

## 3. Vector por vector (banco propio, 52 vectores)

### R1 - profundidad

| Vector | Esperado | Resultado |
|---|---|---|
| V1 set exacto a depth-1 | `{stray-clone, stray-markers, canonical-home}`, exit 1 | **PASS** |
| V2 default == `--max-depth 1` (stdout+exit identicos) | sin regresion | **PASS** |
| V3 depth-1 **identico al detector pre-0296** (`3aa332d`) sobre el mismo fixture | mismo set, mismo exit | **PASS** |
| V4 depth-2 caza `container/nested-stray` | FLAG | **PASS** |
| V5 un dir ya flagado **no** se desciende (`stray-markers/child-of-flagged`) | ausente | **PASS** |
| V6 set exacto a depth-2 (cero falso positivo) | `{stray-clone, stray-markers, canonical-home, nested-stray}` | **PASS** |
| V7 set exacto a depth-3 (`deep/mid/deep-stray`) | +`deep-stray` | **PASS** |
| V8 el subarbol del scratch root nunca se desciende a depth-3 | `deeper-attested`/`deeper-clone` ausentes | **PASS** |
| V9 `--max-depth 0` | exit 2 + `ERROR: max depth must be at least 1` | **PASS** |
| V10 `--max-depth -5` | exit 2 | **PASS** |
| V11 `--max-depth abc` | exit 2 | **PASS** |
| V12 `--max-depth 64` | acotado y consistente | **PASS** |

No consegui una regresion de depth-1: el default es byte-identico al comportamiento pre-0296.

### R2 - allowlist

| Vector | Esperado | Resultado |
|---|---|---|
| V13 `--allow-home <home atestado>` | ignorado | **PASS** |
| V14 los strays reales sobreviven al allowlist | `{stray-clone, stray-markers}` presentes | **PASS** |
| V15 sin allowlist el home **si** se flagea | FLAG | **PASS** |
| V16 `--allow-home` repetible | ambos ignorados | **PASS** |
| V17 separador final tolerado | ignorado | **PASS** |
| V18 case-insensitive en este FS | ignorado | **PASS** |
| V19 `--allow-home` relativo resuelve contra cwd | ignorado | **PASS** |
| V20 entrada inexistente en el allowlist | inerte, sin crash | **PASS** |
| V21 allowlist tambien tapa un clon git-conocido | ignorado | **PASS** |
| V24 `scratch_discipline.canonical_homes` por config | honrado, strays intactos | **PASS** |
| V25 `canonical_homes` malformado (string) | exit 2 ruidoso | **PASS** |
| V26 `canonical_homes` con no-strings | exit 2 | **PASS** |

Cero falsos negativos **entre hermanos**: el allowlist nunca me escondio un stray que estuviera al
lado del hogar allowlisted. La contencion (hijos) se trata como residual RES-4, no como SLIP: medi
que para un home **atestado** el hijo ya era invisible sin allowlist (la regla flag-and-don't-descend
lo tapa igual), asi que el allowlist no introduce alli un falso negativo nuevo.

### R3 - fail-open visible

| Vector | Esperado | Resultado |
|---|---|---|
| V27 `.git` = `gitdir: missing-directory` | `WARNING: cannot resolve git candidate <path>` en stderr, nombrando el candidato | **PASS** |
| V28 el warning **no** contamina el stdout JSON | stdout parseable | **PASS** |
| V30 arbol solo-corrupto: warning emitido | WARNING presente | **PASS** |
| V33 git corrupto **no** suprime la deteccion por marcadores | FLAG + exit 1 | **PASS** |
| V34 `git` fuera del PATH | WARNING, no silencio | **PASS** |
| V35 idem: la deteccion por marcadores sigue viva | FLAG | **PASS** |
| V36 scan root que es un archivo | exit 2 | **PASS** |
| V37 scan root inexistente | exit 2 | **PASS** |

### R4 - disparo host-local (monitor + instalador)

| Vector | Esperado | Resultado |
|---|---|---|
| V38 monitor con hallazgos | exit 1 | **PASS** |
| V39 instruccion DECISION-0018 en stderr | `ACTION REQUIRED ... DECISION-0018` | **PASS** |
| V40 hallazgos reenviados por stdout | JSON parseable, mismo set | **PASS** |
| V41 el warning del scanner llega por stderr | presente | **PASS** |
| V42 el monitor inyecta `--check` si el llamador lo omite | exit 1 | **PASS** |
| V43 `--check` duplicado por el llamador | exit 1, sin error | **PASS** |
| V44 arbol limpio | exit 0 | **PASS** |
| V45 arbol limpio: sin `ACTION REQUIRED` | ausente | **PASS** |
| V46 el monitor **preserva** el exit 2 del scanner | exit 2, no enmascarado a 0/1 | **PASS** |
| V47 monitor sin argumentos | exit 2, no 0 silencioso | **PASS** |
| V48 monitor sin el separador `--` | -- | **SLIP menor** (exit 2 ruidoso; ver 4) |
| V49 monitor desde un cwd arbitrario | exit 1, mismo set | **PASS** |
| instalador `-WhatIf` | no registra nada | **PASS** (`Get-ScheduledTask` = 212 antes y 212 despues; tarea `ProtocolScratchDisciplineMonitor` ausente antes y despues; 0 errores terminantes) |
| nada cablea a CI | -- | **PASS** (sin referencias en workflows; el enforcement solo se invoca a mano o por scheduler del host) |
| **quoting del instalador** | argv integro | **NO-GO** (bloqueo B1, ver 4) |

### Read-only y neutralidad

| Vector | Resultado |
|---|---|
| V51 contenido del fixture byte-identico tras las 40+ corridas (scanner + monitor) | **PASS** `82796a5d0c9ba8ca...` == `82796a5d0c9ba8ca...` |
| V52 metadatos (`st_mtime_ns` + `st_size`) de **todo** nodo, incluido `.git/**` | **PASS** `fa79f31dcd3fd0fb...` == `fa79f31dcd3fd0fb...` |
| V53 el clon revisado no se muta | **PASS** `git status --porcelain` vacio |
| Auditoria de API mutante en `scan_scratch_discipline.py` + `run_scratch_discipline_monitor.py` | **PASS** 0 ocurrencias de `write_text/write_bytes/mkdir/open(/os.remove/os.rename/os.replace/shutil.*/unlink/rmdir/touch/chmod/makedirs/tempfile` |
| Instalador: unica API mutante = `Register-ScheduledTask`, dentro de `ShouldProcess` | **PASS** |
| Neutralidad: cero hardcode de marca/dominio/raiz en los 3 scripts nuevos y en la seccion nueva del runbook | **PASS** (los 3 hits del grep son lineas preexistentes del runbook, fuera del diff) |
| ASCII puro en los 3 scripts nuevos | **PASS** (0 bytes > 127) |
| Config pineado | **PASS** byte-identico desde `3aa332d`; sin `scratch_root`, sin `known_repositories`, sin `scratch_discipline` |

## 4. El bloqueo: B1 -- el instalador corrompe su propia linea de comando

`install_scratch_discipline_monitor.ps1:21` envuelve cada argumento en comillas escapando solo las
comillas internas:

```powershell
$quoted = $arguments | ForEach-Object { '"' + $_.Replace('"', '\"') + '"' }
```

Bajo las reglas de `CommandLineToArgvW` (las que usa el CRT al arrancar `python.exe` desde la tarea
programada), una **barra invertida final** antes de la comilla de cierre escapa esa comilla. Windows
PowerShell **anade `\` al completar con TAB un directorio**, asi que es la entrada mas probable del
operador, no un caso exotico.

Replay fiel de las lineas 13-22 del instalador (sin llamar a `Register-ScheduledTask`), con
`-ScratchRoot` terminado en `\`. Cadena que quedaria registrada:

```
"...\run_scratch_discipline_monitor.py" "--" "--scan-root" "D:\...\volume" "--scratch-root"
"D:\...\designated-scratch\" "--max-depth" "2" "--known-repo" "https://..." "--allow-home" "D:\...\canonical-home"
```

argv realmente recibido (medido con un echo de `sys.argv`):

```
["--", "--scratch-root", "D:\\...\\designated-scratch\" --max-depth 2 --known-repo ... --allow-home ... "]
```

Efecto end-to-end sobre el mismo fixture, misma configuracion, unica diferencia = la `\` final:

| Invocacion | Hallazgos | Lectura |
|---|---|---|
| correcta | `{nested-stray, stray-clone, stray-markers}` | esperado |
| via quoting del instalador (ruta tab-completada) | `{canonical-home, stray-markers}` | **corrupto** |

Es decir, en la tarea que queda instalada:

- **`--known-repo` se pierde** -> la deteccion por remote git queda **desactivada**: `stray-clone`
  (un clon del repo conocido fuera del scratch root, la clase primaria de DECISION-0104) **deja de
  detectarse**. Falso negativo.
- **`--max-depth 2` se pierde** -> vuelve a depth-1: `nested-stray` **deja de detectarse**.
  Regresion R1 completa.
- **`--allow-home` se pierde** -> `canonical-home` reaparece como ruido. Regresion R2.
- **`--json` se pierde** -> un scheduler que parsee JSON recibe texto.
- **`--scratch-root` queda apuntando a una ruta basura** -> nada se considera "bajo el scratch root".
- **el exit sigue siendo 1 y sigue imprimiendo `ACTION REQUIRED`**: la corrida corrupta es
  indistinguible de una sana. Silencioso.

Y la verificacion que el propio entregable ofrece no lo caza: `-WhatIf` imprime solo
`Whatif: ... "ProtocolScratchDisciplineMonitor"`, **nunca la cadena de argumentos**.

Por que lo trato como bloqueo y no como residual: el acceptance R4 pide un mecanismo host-local que
invoque el detector periodicamente **y entregue los hallazgos**. El unico camino shipped para hacerlo
periodico en esta plataforma registra, ante un gesto de operador rutinario, una tarea que entrega un
conjunto de hallazgos **equivocado por defecto** y revierte en silencio el hardening R1+R2 que es
la razon de ser de esta unidad. Un enforcement que se auto-desarma sin avisar es peor que ninguno,
porque produce confianza falsa.

**SLIP menor V48** (no bloqueante, se arregla junto): el monitor exige el separador `--`; sin el,
`argparse.REMAINDER` rechaza el primer argumento con pinta de opcion y sale **2** con el usage. Falla
ruidoso y el runbook documenta la forma con `--`, asi que es un gotcha, no un hueco. Recomiendo
aceptar tambien la forma sin `--` (o `parse_known_args`).

## 5. Remediacion esperada (loop declarado, maximo 2 iteraciones)

1. `scripts/install_scratch_discipline_monitor.ps1`: quoting correcto para `CommandLineToArgvW` --
   duplicar las barras invertidas finales antes de la comilla de cierre (p.ej.
   `$_ -replace '(\\+)$', '$1$1'`) y, como cinturon adicional, `TrimEnd` de separadores en los
   parametros de ruta.
2. Hacer observable la verificacion: que `-WhatIf` (o `-Verbose`) **imprima la cadena de argumentos
   compuesta**, para que el preview documentado pueda cazar una linea malformada.
3. `run_scratch_discipline_monitor.py`: aceptar tambien la invocacion sin `--` (V48).
4. Caso nuevo en `examples/scratch_discipline_cases/`: componer la cadena con el quoting del
   instalador a partir de un array con una ruta terminada en separador, parsearla de vuelta y
   **asertar que el argv resultante es igual al array pretendido** (guardado por plataforma para que
   no rompa en no-Windows).
5. Gates a re-correr por exit code: suite de `examples/scratch_discipline_cases`,
   `scan_domain_neutrality`, `scan_encoding`, `validate_collaboration_state`, mas mi repro: la
   invocacion con scratch root terminado en `\` debe dar **el mismo set de hallazgos** que sin ella.

Re-juicio mio en clon limpio **antes** del commit de cierre. Maximo **2 iteraciones**; un segundo
NO-GO escala al operador humano.

## 6. Residuales declarados (no bloquean; para unidad de seguimiento)

**RES-1 (material) - el canal de warning tiene falsos positivos.** `git config --get-regexp` sale
**1 cuando no hay coincidencia**, que es un resultado normal y documentado, no un fallo. El detector
lo trata como error y emite `WARNING: cannot resolve git candidate ...: git exited 1` para cualquier
repo git **sano sin remotes**. Medido 3/3 en la maquina real (`D:\Agentes\audit-anchor`,
`protocol_research`, `runtime-test-instance`: `rev-parse --is-inside-work-tree` = `true`, exit 0;
`config --get-regexp` exit 1 por ausencia de remote). Con la tarea corriendo cada 30 minutos y un
runbook que ordena "alert the responsible owner", esto es fatiga de alerta sobre el mismo canal que
R3 creo para que el fail-open fuera visible. Fix sugerido: avisar solo si `returncode >= 2` o si
`stderr` no esta vacio.

**RES-2 (material) - el fail-open sigue saliendo 0.** Un stray cuyo git es genuinamente irresoluble y
que **no** tiene los 3 marcadores produce `exit 0` + `OK: no scratch-discipline anomalies found.` en
stdout, con el WARNING solo en stderr. El disparador de entrega del runbook es "any nonzero exit", asi
que ese warning **nunca se rutea** al owner por el mecanismo documentado. R3 pedia literalmente el
warning y el warning esta; la entrega del warning no. Sugerido: `--fail-on-warning`, o que el monitor
distinga "clean" de "clean-con-warnings".

**RES-3 - cobertura condicional del warning.** Sin `--known-repo`, `_git_reason` retorna antes de
consultar git, asi que un candidato con git corrupto **no genera ningun warning** (medido: exit 0,
`warned=False`). Coherente con "no hay nada que emparejar", pero conviene documentarlo.

**RES-4 - contencion del allowlist.** `--allow-home` hace `continue` **sin descender**, y no hay
validacion de que la entrada parezca un hogar canonico. Para un home atestado no anade falso negativo
(la regla flag-and-don't-descend ya tapaba a sus hijos), pero allowlistar un **contenedor padre no
atestado** ciega el subarbol entero: medido, `--allow-home <VOL>/container` hace desaparecer
`nested-stray`, que si se reporta sin esa bandera. Sugerido: warning cuando una entrada allowlisted
no tenga marcadores atestados ni remote conocido, o descender igualmente sin flagear el propio home.

**RES-5 - cwd del monitor.** El monitor ejecuta el scanner con `cwd=<raiz del repo>`, asi que un
`--scan-root`/`--config` **relativo** se resuelve contra la raiz del repo y no contra el directorio
del scheduler (medido: exit 2 ruidoso). Implica ademas que el `--config` por defecto es siempre el
`protocol.config.json` pineado; hoy es inocuo (no tiene `scratch_discipline`, `scratch_root` ni
`known_repositories`), pero conviene fijarlo en el runbook.

**RES-6 - `-Force` en el registro.** `Register-ScheduledTask -Force` sobrescribe una tarea existente
con el mismo nombre sin preguntar. Es accion explicita del operador, pero merece mencion en el runbook.

**RES-7 - `.git` como candidato.** A depth >= 2 el escaneo desciende dentro del `.git/` de repos no
flagados. Sin hallazgos ni riesgo (read-only), pero es trabajo inutil y ruido potencial en arboles
grandes; sugerido saltar `.git` explicitamente.

## 7. Respuesta a la pregunta del Arquitecto

Sobre el punto de diseno que planteaste (entrega = alerta-del-scheduler + registro manual en mailbox,
sin auto-commit al ledger): **es valido y lo prefiero**. Preserva read-only, no le da al detector
credenciales de escritura sobre el ledger, y el acceptance dice "mailbox **o equivalente**". Un
auto-commit seria una capacidad nueva y un vector de escritura que esta unidad no debe abrir. Lo unico
que le falta a esa cadena es que el disparador documentado ("alert on any nonzero exit") **no cubre el
caso de warning-con-exit-0** (RES-2).

## 8. Recomendacion de cierre

**CHANGE-REQUIRED (NO-GO).** Un unico defecto concreto, reproducible y con fix de una linea: el
quoting del instalador (B1). Todo lo demas -- hardening R1/R2/R3, monitor, exit codes, read-only,
neutralidad, config pineado -- lo doy por verificado por comportamiento en clon limpio. Aplicada la
remediacion de la seccion 5 y re-juzgada, esta unidad cierra.

-- Analista (checker independiente, TASK-0296)
