# Veredicto Analista -- TASK-0321: emparejamiento de renombrados en Get-WorktreeDiskProof

**Revisor:** Analista (voz adversarial independiente, checker-only)
**Fecha:** 2026-08-06 (hora local del sistema, UTC+2)
**Instruccion:** `Area_comun/mailbox/open/MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0321.md`
**Contrato:** `Area_comun/tasks/TASK-0321-diskproof-emparejamiento-renombrados.md` (seis AC)
**Origen:** hallazgo S4 de mi veredicto r2 de TASK-0319.
**Alcance de producto:** NINGUNO. Hub, gates de Python y PowerShell.

## Recomendacion de cierre

**OK-CERRABLE.** Los seis AC pasan. Ningun SLIP. Cuatro residuales declarados abajo, ninguno
bloqueante; el mas sustantivo (R3) es un hallazgo NUEVO fuera del alcance de esta tarea.

## Anclaje canonico

| Cosa | Valor |
|------|-------|
| Commit del arreglo | `0a008f06` (`fix(TASK-0321): pair disk proof rename records`) |
| Commit de entrega | `2fb770cc` (`chore(TASK-0321): deliver disk proof pairing`) |
| Codigo pre-arreglo (falsacion) | `0a008f06^` = `38b46096` |
| HEAD al recomputar gates | `53e380f6` |
| Clon limpio A (codigo) | `git clone --depth 1 file:///D:/Agentes/multi_agent_project_protocol` -> `D:/Aegis_Scratch/mapp/an0321` @ `6dfdd4c7` |
| Clon limpio B (gates) | `git clone --shared` -> `D:/Aegis_Scratch/mapp/full` @ `53e380f6` |
| Arbol caliente | NO usado para gatear. Solo lectura de estado. |

Metodo: las funciones reales se cargan por AST desde el `.ps1` (`Parser::ParseFile` +
`FunctionDefinitionAst` + `Invoke-Expression`), se ejecutan contra repos git creados al vuelo bajo
`D:/Aegis_Scratch/mapp/probes/` (DECISION-0104), y se comparan lado a lado NUEVO vs VIEJO en el
mismo repo y en el mismo instante. Las rutas imposibles en NTFS se cubren con streams sinteticos
inyectados por un `Get-GitStatusPorcelainUtf8` de doble.

## Gates, por exit code, en clon limpio

| Gate | Comando | Exit |
|------|---------|------|
| Estado colaborativo | `python scripts/validate_collaboration_state.py --root .` | **0** |
| Encoding | `python scripts/scan_encoding.py --root .` | **0** |
| Neutralidad de dominio | `python scripts/scan_domain_neutrality.py --root .` | **0** |
| Inventario de falsacion | `python scripts/check_falsification_contracts.py --root . --inventory` | **0** |
| Guardian de falsacion | `python scripts/test_falsification_contracts.py` | **0** |
| Suite del harness | `python scripts/test_exec_lease_harness.py` | **0** (14/14 PASS) |
| Poda de estado | `python scripts/prune_state.py --root . --check` | **0** (ver R4) |
| Drift del ledger | `protocol_state_drift(.)` | `has_drift=False`, `up_to_seq=7251`, hot_hash == replay_hash |

Nota de conteo: la suite tiene **14** casos, no 8. El exit code es lo que gatea; lo digo solo para
que el recomputo del Arquitecto y el mio citen el mismo numero.

## AC por AC

| AC | Veredicto | Evidencia |
|----|-----------|-----------|
| AC1 falsacion antes del arreglo | **PASA** | S4 reproducido por COMPORTAMIENTO en repos git reales con la funcion de `38b46096`. Ver tabla de vectores: la ruta de ORIGEN sale amputada en los siete vectores reales de renombrado, con `exists=false` sobre un nombre que no existe. |
| AC2 mismo remedio, no uno nuevo | **PASA** | Misma forma ya aprobada en `Get-StagedResidueState`: bucle por indice, `Substring(0,2) -match '[RC]'`, el registro siguiente se consume como unidad con `$index++`, y si falta se devuelve `$null` en vez de inventar ruta. Verificado por comportamiento en 25 vectores. Falla cerrada probada: S3 da `$null` donde el viejo inventaba `moved.md`. |
| AC3 rama muerta fuera | **PASA** | Mi propio `grep -c "' -> '"` sobre el harness: **0**. Y la eliminacion no es cosmetica: S1/S2 demuestran que la rama muerta CORROMPIA rutas que contienen ` -> ` de forma legitima (creables en POSIX, no en NTFS). |
| AC4 boundary con git real | **PASA** (con residual R1) | Contrato `NEG-HARNESS-WORKTREE-DISK-PROOF-RENAME-PAIRING` declarado, inventario exit 0, runner cableado en CI (`.github/workflows/validate.yml:238` y `:47`). El camino sano usa `git init` + `git mv` REALES, sin mock; el mock solo aparece en el caso malformado, donde es el unico modo de fabricar un stream que git nunca emite. Mi bateria de mutacion independiente: la mutacion nuclear muere. |
| AC5 barrido, no parche puntual | **PASA** (con hallazgo nuevo R3) | Barrido con mi criterio, no solo `Substring(3)`. No queda una cuarta lectura ciega del stream `-z` en el harness. |
| AC6 sin regresion | **PASA** | Tabla de gates arriba, toda en clon limpio y por exit code. |

## Vectores ejercitados (25). NUEVO = `0a008f06`; VIEJO = `38b46096`

### Repos git reales (`git init` + `git mv`)

| # | Vector | Registros que emite git | NUEVO | VIEJO | Resultado |
|---|--------|-------------------------|-------|-------|-----------|
| V1 | `git mv` simple en subdirectorio | `R  docs/disk-new.md` + `docs/disk-old.md` | `[docs/disk-new.md, docs/disk-old.md]` exists `[true,false]` | `[docs/disk-new.md, s/disk-old.md]` | **PASA** / S4 reproducido |
| V2 | renombrado con espacios en carpeta y fichero | `R  a folder/new name.md` + `a folder/old name.md` | ambas intactas | `[..., older/old name.md]` | **PASA** |
| V4 | copia con `status.renames=copies` | git emitio `A  dst.md`, **no** `C` | n/a | n/a | inaplicable en esta maquina; cubierto por S5 sintetico |
| V5 | renombrado + modificado + borrado + untracked entremezclados | 5 registros | 5 rutas reales, sin desalineo | `.md` en lugar de `aaa.md` | **PASA** |
| V6 | dos renombrados consecutivos | 4 registros | `[dos.md, one.md, two.md, uno.md]` | `[.md, .md, dos.md, uno.md]` (dos rutas destruidas) | **PASA** |
| V7 | origen de 3 caracteres (`a.c` -> `b.c`) | `R  b.c` + `a.c` | `[a.c, b.c]` | **`$null`** (perdia la prueba entera) | **PASA** + arregla regresion previa |
| V8b | renombrado con nombre no-ASCII (`cafe` con acento) | `-z` no cita ni escapa | ambas intactas | origen amputado | **PASA** |
| V9 | fichero llamado `0` (verdad booleana de PowerShell) | `R  1` + `0` | `[0, 1]` | `$null` | **PASA** (`Where-Object { $_ }` conserva `"0"`; comprobado aparte) |
| V10 | renombrado y destino borrado del disco (`RD`) | `RD gone-new.md` + `gone-old.md` | ambas, `exists [false,false]` | `[e-old.md, gone-new.md]` | **PASA** |
| V11 | renombrado profundo entre directorios | `R  x/y/z/deep-new.md` + `a/b/c/deep-old.md` | ambas intactas | `/c/deep-old.md` | **PASA** |

### Streams sinteticos (rutas imposibles en NTFS o que git no emite aqui)

| # | Vector | NUEVO | VIEJO | Resultado |
|---|--------|-------|-------|-----------|
| S1 | origen que contiene ` -> ` literal | `[new.md, old -> weird.md]` | `[new.md, weird.md]` | **PASA** -- valor real de AC3 |
| S2 | destino que contiene ` -> ` literal | `[new -> weird.md, old.md]` | `[.md, weird.md]` | **PASA** |
| S3 | registro de renombrado al final, sin origen | **`$null`** (falla cerrada) | `[moved.md]` (inventaba) | **PASA** |
| S4s | origen que es un solo espacio (nombre legal en POSIX) | `$null` (falla cerrada) | `$null` | **PASA**, conservador |
| S5 | registro `C` (copia) seguido de origen | `[copy.md, origin.md]` | `[copy.md, gin.md]` | **PASA** -- la rama C funciona hoy |
| S6 | renombrado del lado del arbol (` R`) | `[new.md, old.md]` | `[.md, new.md]` | **PASA** |
| S7 | `RM` (renombrado en indice, modificado en arbol) | `[new.md, old.md]` | `[.md, new.md]` | **PASA** |
| S8 | par de renombrado seguido de registro normal | 3 rutas reales | 1 destruida | **PASA**, sin desalineo |
| S9 | registro normal, par, registro normal | 4 rutas reales | 1 destruida | **PASA**, sin desalineo |
| S10 | origen mas corto que 4 caracteres | `[a, bb.md]` | `$null` | **PASA** |
| S11 | dos pares de renombrado seguidos | 4 rutas reales | `[md, md, n1.md, n2.md]` | **PASA** |
| S12 | registro corto (`?? a`) | `[a]` | `[a]` | **PASA**, sin cambio |
| S13 | `UU` no fusionado | `[conflict.md]` sin emparejar | igual | **PASA**, sin falso par |
| S14 | `T` cambio de tipo | `[link.md]` sin emparejar | igual | **PASA**, sin falso par |

Sin SLIPS en 25 vectores. El desalineo por corrimiento -- que es el modo de fallo que de verdad
duele, porque contamina TODAS las rutas posteriores y no solo la del par -- lo busque explicitamente
en V5, V6, S8, S9 y S11 y no aparece.

## AC5: el barrido, con mi criterio

Lectores del stream `-z` de git en TODO el repo (no solo `Substring(3)`, no solo el harness):

| Ruta | Lectura | Necesita emparejar? | Estado |
|------|---------|---------------------|--------|
| `scripts/harness/peer_mailbox_cron.ps1:659` `Get-WorktreeDiskProof` | `status --porcelain=v1 -z` | SI | **arreglado aqui** |
| `scripts/harness/peer_mailbox_cron.ps1:691` `Get-StagedResidueState` | `status --porcelain=v1 -z` | SI | arreglado en TASK-0319 |
| `scripts/harness/peer_mailbox_cron.ps1:907` y `:1072` | `ls-files --others --exclude-standard -z` | NO -- `ls-files` emite una ruta por registro, jamas pares | correcto |
| `scripts/memory/build_memory_db.py:380` | `ls-tree -r --name-only -z` | NO -- una ruta por registro | correcto |
| `scripts/test_exec_lease_harness.py:321,352` | sondas de test | n/a | n/a |

**No queda una cuarta lectura ciega del stream `-z`.** Confirmo ademas los cuatro `Substring(3)` del
harness (664, 696, 716, 736) uno a uno: los cuatro estan dentro de bucles que emparejan. En el de
736 el `$index++` es la ULTIMA sentencia del cuerpo, catorce lineas despues del `Substring(3)`, y las
unicas salidas anticipadas del bucle son `return`, asi que no hay camino que se salte el
emparejamiento y siga iterando. Confirmo el aviso metodologico del Arquitecto: un grep de ventana
corta da falso positivo aqui.

Tambien descarte la hipotesis del duplicado obsoleto: `find` da **una sola** copia de
`peer_mailbox_cron.ps1` en el repo, y `test_new_instance_exports_identical_harness` pasa, asi que el
exportador no publica una version vieja del parser.

## Residuales declarados

**R1 -- la cobertura de mutacion del contrato es mas estrecha que el propio AC2.**
Bateria independiente de seis mutaciones sobre el codigo entregado, gatando la suite completa:

| Mutacion | Suite | Lectura |
|----------|-------|---------|
| M1 quitar el `$index++` que consume el origen | **exit 1, MUERE** | el nucleo del emparejamiento esta clavado |
| M3 `-match '[RC]'` -> `-match '[R]'` (cae la clase copia) | exit 0, SOBREVIVE | **hueco real**: la rama `C` que AC2 exige por nombre no la ejercita ninguna frontera |
| M5 reintroducir la rama muerta ` -> ` | exit 0, SOBREVIVE | **hueco real**: nada impide que AC3 se deshaga; S1/S2 prueban que reintroducirla corrompe rutas |
| M6 quitar el rechazo de origen en blanco | exit 0, SOBREVIVE | hueco menor: solo el caso origen-en-blanco queda sin fijar |
| M2 quitar la guarda de limites | exit 0, SOBREVIVE | **mutante equivalente, no es hueco**: lo verifique aparte -- sin la guarda, `$records[$i+1]` da `$null`, el `.Replace` falla de forma no terminante y `IsNullOrWhiteSpace($null)` devuelve `$null` igual. Solo quitando LAS DOS guardas se fabrica `[null, moved.md]`. La guarda de limites es redundancia defensiva; la que carga el peso es la de blanco |
| M4 invertir el orden del par | exit 0, SOBREVIVE | **mutante equivalente, no es hueco**: la funcion hace `Sort-Object { $_.path }` antes de serializar, asi que el orden interno no es observable |

No pido remediacion: el contrato mata la mutacion que destruye la garantia, y M3/M5/M6 son
ampliaciones de frontera, no defectos del entregable. Lo dejo escrito para que si alguien amplia
este contrato sepa exactamente que tres fronteras faltan.

**R2 -- la rama `C` solo esta probada de forma sintetica.** El `git status --porcelain=v1 -z` de
esta maquina **no emite `C`** ni con `status.renames=copies` puesto: en V4 reporto `A  dst.md`. La
rama de copia funciona (S5 sintetico lo prueba), pero nadie puede ejercitarla con git real aqui.
Coincide con lo que ya observe en el ciclo de TASK-0319.

**R3 -- HALLAZGO NUEVO, fuera del alcance de TASK-0321: los lectores de porcelain SIN `-z` no
desescapan y fabrican rutas que no existen.** El Arquitecto me pidio barrer "otros scripts del
repo", asi que esto sale del barrido, pero NO es el defecto S4 y NO cabe en `scope_routes`: aqui
` -> ` si lo emite git de verdad, y el emparejamiento no aplica. El defecto es otro. En
`scripts/sweep_cron_zombies.py:77-87` (`dirty_paths`), medido por comportamiento:

```
git status --porcelain=v1  ->  'R  personal/old.md -> personal/new.md\n?? "personal/caf\303\251.md"\n'
dirty_paths()              ->  ['"personal/caf/303/251.md"', 'personal/new.md']
```

El renombrado sale bien. La ruta no-ASCII no: git la entrecomilla y la escapa en octal C (porque sin
`-z` manda `core.quotepath`), y el `.replace("\\", "/")` de la funcion convierte las barras de escape
en separadores, fabricando `"personal/caf/303/251.md"`, que no coincide con ninguna ruta ni con
ningun `scope` de claim. Su consumidor es `dirty_claimed_route()`, que decide si el barredor de
zombis respeta un claim activo. Una ruta sucia invisible hace que devuelva `False`: **falla ABIERTA
en un camino destructivo** (`taskkill` sobre un peer que puede estar escribiendo una ruta
reclamada). El mismo patron esta en `runtime/orchestrator.py:667` y `:688`
(`dirty_worktree_paths` / `dirty_tracked_worktree_paths`, consumidos por `unreported_dirty_paths`) y
en el espejo `examples/full_runtime_instance/runtime/orchestrator.py:142,163`. Afecta tambien a
nombres con `"` o `\`, y el `.strip()` se come espacios al principio y al final del nombre.
Probabilidad baja en este repo (los nombres son ASCII de facto), impacto alto si ocurre. Es
registrable aparte; no toco nada.

**R4 -- la poda estaba vencida en el ancla, y ya no lo esta.** `prune_state.py --check` daba exit 1
(`released_ratio 91.3 >= 90`) en `6dfdd4c7`, y la CI hace fallar la integracion con eso. Lo atribui
antes de reportarlo: ya estaba vencida en `38b46096`, es decir **antes** de TASK-0321, asi que no la
causa esta entrega. El Arquitecto la corrio en `53e380f6` y el gate esta en exit 0. Lo dejo anotado
solo por trazabilidad del recomputo.

## Respuesta directa a la pregunta del Arquitecto

**Si a las dos.** El emparejamiento de `Get-WorktreeDiskProof` es correcto en los 25 vectores,
incluidos los cuatro cruces que pediste (copia `C` via S5, origen y destino dentro y fuera, rutas con
espacios) y los tres de desalineo que anadi por mi cuenta. Y el barrido del AC5 confirma que no queda
ninguna cuarta lectura ciega del stream `-z` en el harness. Lo que si aparecio, fuera de ese
perimetro, es R3.

---
*Analista -- checker independiente. No implemento, no promuevo, no cierro.*
