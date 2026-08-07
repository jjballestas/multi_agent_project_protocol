# Veredicto Analista -- TASK-0323: lectores de git status --porcelain sin -z

**Revisor:** Analista (voz adversarial independiente, checker-only)
**Fecha:** 2026-08-07 04:36 (hora local del sistema, UTC+2)
**Instruccion:** `Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0323.md`
**Contrato:** `Area_comun/tasks/TASK-0323-porcelain-sin-z-lectores.md` (cinco AC)
**Origen:** residual R3 de mi veredicto de TASK-0321.
**Alcance de producto:** NINGUNO. Hub, gates de Python y PowerShell.

## Recomendacion de cierre

**OK-CERRABLE.** Los cinco AC pasan. Ningun SLIP bloqueante. Cinco residuales declarados abajo,
todos con reproduccion; el mas sustantivo (R4) es un hallazgo NUEVO fuera del alcance de esta
tarea y su direccion tambien es ABIERTA, por lo que pido tarea propia.

Respuesta directa a tu pregunta: **si, el inventario del AC3 esta completo.** Barri por vias
distintas a las tuyas y a las suyas y no queda ningun lector que decodifique rutas sin `-z` en
todo el repo. Detalle abajo.

## Anclaje canonico

| Cosa | Valor |
|------|-------|
| Commit del arreglo | `0ee452ed` (`fix(TASK-0323): parse porcelain paths losslessly`) |
| Commit de entrega | `3df488fa` (`coord(TASK-0323): deliver porcelain reader fix`) |
| Base inmediata (para regresion) | `ee9c0dde` (`coord(TASK-0317): deliver remediation iteration 4`) |
| HEAD del hub al revisar | `c5644adc` |
| Handoff | `Area_comun/handoffs/HANDOFF-TASK-0323-codex-to-arquitecto.md` |
| Clon limpio | `D:/Aegis_Scratch/protocol/an0323` (detached en `0ee452ed`, `git status` vacio) |
| Clon de base | `D:/Aegis_Scratch/protocol/base` (detached en `ee9c0dde` y `8e07aa14`) |

Todo lo que sigue se midio en esos clones, nunca en el arbol caliente. Gate por exit code.

## Gates recomputados por mi cuenta (clon limpio, `0ee452ed`)

| Gate | Exit | Nota |
|------|------|------|
| `python scripts/test_exec_lease_harness.py` | 0 | 15/15 PASS, incluido `test_zombie_sweeper_parses_real_git_quoted_rename_paths` |
| `python scripts/check_falsification_contracts.py --root . --inventory` | 0 | `NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS` DECLARED, boundaries=7 |
| `python scripts/validate_collaboration_state.py --root .` | 0 | solo warnings de `context_refs` |
| `python scripts/scan_encoding.py --root .` | 0 | |
| `python scripts/scan_domain_neutrality.py --root .` | 0 | |
| drift (`protocol_state_drift`) | 0 | `has_drift=false`, `up_to_seq=7299`, `entries=[]` |
| `git diff --check` | 0 | |
| `git status --porcelain=v1 -z` | vacio | 0 bytes |

## Tabla vector por vector

| # | Vector exigido | Resultado | Evidencia |
|---|----------------|-----------|-----------|
| AC1-a | Renombrado: el lector viejo fabrica ruta, el nuevo devuelve la exacta | PASS | ver "Falsacion AC1" |
| AC1-b | Ruta entrecomillada/escapada por git: idem | PASS | ver "Falsacion AC1" |
| AC2 | Se elige `-z` y se recorre por pares, con justificacion | PASS | ver "AC2" |
| AC3 | Inventario COMPLETO de lectores de git status | PASS | ver "Inventario propio" |
| AC4 | Negativo permanente con salida REAL de git + cableado en CI | PASS (con residual R1) | ver "AC4" |
| AC5 | Suite y gates verdes por exit code en clon limpio, sin regresion | PASS | tabla de gates + "Regresion" |
| Foco 4 | El barredor ya NO falla ABIERTO | PASS (con residual R4) | ver "Direccion del fallo" |

## Falsacion AC1 -- por comportamiento, contra git real

Repo real en scratch: `git mv "old name.txt" "new name.txt"`, un modificado en `sub dir/`, y un
no-rastreado `nandu con espacio.txt` (con no-ASCII). Salida real de git sin `-z`:

```
R  "old name.txt" -> "new name.txt"
 M "sub dir/plain.txt"
?? "\303\261and\303\272 con espacio.txt"
```

Extraje `parse_porcelain_v1_z` de los TRES ficheros (barredor, runtime vivo, espejo de
`examples/full_runtime_instance`) y los alimente con la salida `-z` real del mismo repo:

```
LECTOR VIEJO : ['"/303/261and/303/272 con espacio.txt"', '"new name.txt"', '"sub dir/plain.txt"']
BARREDOR     : ['nandu con espacio.txt', 'new name.txt', 'old name.txt', 'sub dir/plain.txt']
RUNTIME      : idem
ESPEJO       : idem
VERDAD       : idem

existe en disco, lector viejo : 3 de 3 -> False
existe en disco, lector nuevo : 3 de 3 -> True
```

El lector viejo falla en los DOS vectores a la vez, y de forma peor de lo anotado en el intake:
el `.replace("\\", "/")` convierte el escape en C `\303\261` en `/303/261`, o sea fabrica
segmentos de ruta enteros. Los tres lectores nuevos coinciden exactamente con la verdad.

## AC2 -- eleccion justificada

Se eligio `-z` (no desentrecomillado manual) y se declara en el handoff. Es la eleccion correcta:
elimina la ambiguedad en el productor en vez de reimplementar `unquote_c_style` en tres sitios.
El recorrido por pares (`R`/`C` consume el registro siguiente) es **consistente con la convencion
que ya fijaron TASK-0319 y TASK-0321** en `Get-WorktreeDiskProof`, que tambien anade la ruta
origen al conjunto. Verifique que el espejo de `examples/full_runtime_instance` es **identico
byte a byte** al del runtime vivo (`diff` de la funcion: sin diferencias), asi que no hay deriva
entre instancia viva y plantilla enviada.

## Inventario propio del AC3

No use tus dos globs ni la tabla del maker. Barri por: `git.\{0,3\}status` sobre todo el arbol,
`"status"` como argumento en `.py`, `Arguments`/`git` en `.ps1`/`.psm1`, y `.js`/`.mjs`/`.ts`
(cero resultados). Clasificacion mia:

**Decodifican rutas (tienen que usar `-z`) -- 5 sitios, los 5 con `-z`:**

| Lector | Modo | Veredicto |
|---|---|---|
| `scripts/sweep_cron_zombies.py:dirty_paths` | `--porcelain=v1 -z` | OK |
| `runtime/orchestrator.py:dirty_worktree_paths` | `--porcelain=v1 -z` | OK |
| `runtime/orchestrator.py:dirty_tracked_worktree_paths` | `--porcelain=v1 -z --untracked-files=no` | OK |
| `examples/full_runtime_instance/runtime/orchestrator.py` (los dos espejos) | idem | OK, parser identico |
| `scripts/harness/peer_mailbox_cron.ps1:Get-GitStatusPorcelainUtf8` (y sus consumidores `Get-WorktreeDiskProof`, `Get-StagedResidueState`) | `--porcelain=v1 -z --untracked-files=all` | OK (0319/0321) |

**NO decodifican rutas (sin `-z` es correcto) -- inspeccionados uno a uno:**

- `examples/mailbox_retry_cases/run_mailbox_retry_cases.py:761` -- compara `== ""`, vacuidad.
- `examples/mailbox_retry_cases/run_mailbox_retry_cases.py:1367` -- acotado con `-- predirty.txt`,
  asserta `startswith(" M ")`, es decir letras de estado, no ruta.
- `examples/runtime_apply_cases/run_runtime_apply_cases.py:141` (`git_status_for_path`) --
  `--short -- <path>`, compara `== ""`. **Este no aparece nominalmente en la tabla del handoff**,
  pero cae dentro de su clausula "runtime apply ... compare emptiness"; no es un hueco.
- `scripts/memory/test_memory_db.py` (704, 707, 1247, 1249, 1356, 1358, 1559, 1562) -- compara
  `before == after` como blob completo.
- `connectors/git_readonly/connector.py:15,49` -- lista blanca de verbos, no ejecuta ni decodifica.
- `scripts/test_exec_lease_harness.py` -- la llamada legacy deliberada del negativo AC4, como control.

**Conclusion: cero lectores de ruta sin `-z` en el repo.** El AC3 cumplio su proposito de evitar
una cuarta ronda por esta clase.

## AC4 -- el negativo contra git real

`NEG-CRON-ZOMBIE-SWEEPER-PORCELAIN-Z-PATHS` esta declarado con 7 boundaries, colocado junto a
`test_zombie_sweeper_parses_real_git_quoted_rename_paths`, y cableado en CI por dos vias:
`.github/workflows/validate.yml:238` corre la suite del harness y `:47` corre el inventario.
El fixture crea un repo git de verdad con `git mv` y un no-rastreado con espacio y `e` acentuada,
verifica que la salida legacy contiene literalmente `" -> "` y comillas, y exige que los tres
parsers devuelvan las tres rutas exactas. Cumple el AC al pie de la letra.

Ademas mata la mutacion declarada (quitar `-z`): lo reproduje y el mutante levanta
`ValueError("missing source path in git status --porcelain=v1 -z pair")`. Ver residual R1 sobre
el alcance real de esa muerte.

## Direccion del fallo -- tu foco 4, medido de punta a punta

No me quedo en el parser: reconstrui la DECISION completa (`dirty_claimed_route`) con el lector
viejo sacado de `0ee452ed^` y con el nuevo, sobre repos git reales con un `CLAIMS.json` que da a
Codex un claim activo **acotado a fichero**, que es como manda el protocolo para el mailbox.

**Caso A -- ruta que git entrecomilla (claim file-scoped):**

```
git legacy         : ?? "Area_comun/mailbox/open/MSG-nota cafe\303\251.md"
claim scope        : Area_comun/mailbox/open/MSG-nota cafee.md
VIEJO dirty        : ['"Area_comun/mailbox/open/MSG-nota cafe/303/251.md"']
VIEJO route dirty  : False  -> MATA TRABAJO VIVO (FALLA ABIERTO)
NUEVO dirty        : ['Area_comun/mailbox/open/MSG-nota cafee.md']
NUEVO route dirty  : True   -> SKIP (FALLA CERRADO)
```

**Caso B -- renombrado, ASCII puro, sin entrecomillado de por medio (claim sobre la ruta origen):**

```
git legacy         : R  Area_comun/mailbox/open/MSG-orig.md -> Area_comun/mailbox/open/MSG-renamed.md
claim scope        : Area_comun/mailbox/open/MSG-orig.md
VIEJO dirty        : ['.../MSG-renamed.md']
VIEJO route dirty  : False  -> MATA TRABAJO VIVO (FALLA ABIERTO)
NUEVO dirty        : ['.../MSG-orig.md', '.../MSG-renamed.md']
NUEVO route dirty  : True   -> SKIP (FALLA CERRADO)
```

El fallo ABIERTO era real y esta cerrado en los dos vectores, no solo en el primero. El caso B es
el mas instructivo: no necesita ni no-ASCII ni espacios, basta un `git mv` normal, y el barredor
viejo habria matado al peer a mitad de un renombrado dentro de su propia ruta reclamada.

Un endurecimiento adicional que el maker no destaca y que verifique: `dirty_paths` ya no ignora
el codigo de salida de git. Antes, si `git status` fallaba (repo corrupto, git ausente), stdout
venia vacio, el conjunto sucio salia vacio y el barredor **procedia a matar**. Ahora levanta
`RuntimeError` que sube sin capturar hasta `main()` dentro del `global_lock`, cuyo `finally`
libera el lock: el barredor aborta sin matar nada. Es otro fallo abierto cerrado, de propina.

## Regresion (AC5) -- medida contra la base, no asumida

El handoff declara que `examples/runtime_loop_cases/run_runtime_loop_cases.py` esta rojo pero que
ya lo estaba. **Lo verifique yo**, porque `runtime/orchestrator.py` es justo uno de los ficheros
tocados y no acepto esa afirmacion de palabra:

| Commit | Exit | Casos fallando |
|---|---|---|
| `0ee452ed` (el arreglo) | 1 | 9 |
| `ee9c0dde` (base inmediata) | 1 | 9 |
| `8e07aa14` (TASK-0321, ya ratificada verde) | 1 | 9 |

Conjuntos **identicos** (`case_once_commits_one_turn`,
`case_claim_step_acquires_missing_owner_claim`,
`case_preclaimed_turn_does_not_emit_orchestrator_acquire`,
`case_claim_step_rejects_conflicting_other_claim`,
`case_acquired_claim_released_after_blocked_terminal`, `case_sequence_max_iter_cuts`,
`case_runtime_commit_bypasses_prune_hook_and_auto_prunes`,
`case_manual_commit_still_uses_prune_hook`,
`case_commit_failure_discards_half_applied_turn_and_blocks`).
Diferencia entre arreglo y base: cero en los dos sentidos. **TASK-0323 no introduce regresion.**

Observacion aparte, no imputable a esta tarea: ese runner ESTA cableado en CI
(`.github/workflows/validate.yml:208`) y esta rojo en local sobre Windows desde al menos
`8e07aa14`, una tarea ya cerrada en verde. No he medido si CI sobre Linux tambien lo esta, asi
que no afirmo "CI roja"; lo senalo como anomalia DECISION-0018 para que decidas si merece tarea.

## Residuales declarados (ninguno bloqueante)

**R1 -- la muerte del mutante del AC4 depende de la FORMA del fixture, no solo de la mutacion.**
El handoff dice "malformed input fails closed" y la tabla dice "malformed input fails closed".
Es mas ancho de lo que el codigo garantiza. Sin `-z`, `raw.split(b"\0")` devuelve UN registro
gigante con todas las lineas pegadas; la guarda `record[2:3] != b" "` lo deja pasar porque el
byte 2 de la primera linea SI es un espacio. Solo salta la excepcion si esa primera linea es un
`R`/`C`, porque entonces falta el registro origen. Medido, mismo mutante, dos formas de arbol:

```
V1 con renombrado : ValueError(missing source path ...)   -> mutante MUERTO
V2 SIN renombrado : RETURNED ['"otro archivo.md"\n?? "unt cafe/303/251.md"\n']  -> mutante VIVO
```

En V2 el parser inventa una ruta unica de varias lineas, en silencio. **No bloqueo** porque el
fixture del negativo siempre construye un renombrado, la mutacion declarada muere de forma
determinista y el codigo de produccion pasa `-z` siempre, luego no es un escape vivo. Arreglo
barato si lo quieres cerrar: rechazar cualquier registro que contenga `\n`, una linea, cierra la
clase entera y hace la muerte independiente del fixture.

**R2 -- superficie de excepcion nueva y no declarada en el runtime.**
`dirty_worktree_paths` y `dirty_tracked_worktree_paths` nunca levantaban: devolvian `[]` ante
cualquier fallo de git. Ahora pueden propagar `ValueError` desde el parser. Sus llamadores
(`auto_prune_if_due` en la linea 770 y el bucle principal en la 884) no la capturan, asi que
abortaria la corrida. La direccion es CERRADA (aborta en vez de seguir con rutas fabricadas) y es
inalcanzable mientras `-z` este fijo, por eso no bloqueo, pero es un cambio de contrato que el
handoff no menciona.

**R3 -- cambio semantico no anunciado: ahora las rutas ORIGEN cuentan como sucias.**
Antes solo entraba el destino del renombrado. Es justo lo que cierra el caso B y coincide con la
convencion de `Get-WorktreeDiskProof`, o sea es correcto; pero `unreported_dirty_paths` pasa a
exigir que el informe declare TAMBIEN la ruta origen. Una entrega que renombre un fichero y
reporte solo el destino puede quedar bloqueada donde antes pasaba. Merece una linea en el runbook.

**R4 -- HALLAZGO NUEVO, direccion ABIERTA, fuera del alcance de TASK-0323.**
`sweep_cron_zombies.dirty_paths` **no** pasa `--untracked-files=all` (el helper de PowerShell si).
Cuando el directorio entero esta sin rastrear, git colapsa la salida al directorio, y un claim
acotado a FICHERO dentro de el no casa nunca. Medido, mismo caso A pero con el directorio sin
rastrear:

```
git legacy        : ?? Area_comun/mailbox/
claim scope       : Area_comun/mailbox/open/MSG-nota cafee.md
VIEJO route dirty : False   NUEVO route dirty : False   -> los DOS matan trabajo vivo
```

No es un defecto de decodificacion de porcelain y TASK-0323 no lo empeora ni lo mejora, pero la
direccion vuelve a ser ABIERTA y el barredor mata procesos. **Pido tarea propia**, con el mismo
criterio que aplicasteis para registrar 0323 en vez de anotarlo como residual.

**R5 -- cosmetico.** `.replace("\\", "/")` corromperia una ruta POSIX con barra invertida
legitima. Inalcanzable en Windows; el espejo de `examples/full_runtime_instance` si se envia a
otras plataformas. Preexistente, sin cambio en esta tarea.

## Reproduccion

```bash
git clone --no-checkout --shared . D:/Aegis_Scratch/protocol/an0323
cd D:/Aegis_Scratch/protocol/an0323 && git checkout 0ee452ed
python scripts/test_exec_lease_harness.py                                  # exit 0, 15/15
python scripts/check_falsification_contracts.py --root . --inventory       # exit 0
python scripts/validate_collaboration_state.py --root .                    # exit 0
python scripts/scan_encoding.py --root .                                   # exit 0
python scripts/scan_domain_neutrality.py --root .                          # exit 0
git diff --check && git status --porcelain=v1 -z                           # exit 0, vacio
# regresion: mismo runner en 0ee452ed / ee9c0dde / 8e07aa14 -> exit 1, 9 casos identicos
```

Los tres guiones de falsacion propios (parsers contra git real, decision de punta a punta en los
casos A y B, y la sonda de robustez del mutante) se corrieron desde
`D:/Aegis_Scratch/protocol/gt/`, fuera del arbol atestado, y quedan descritos arriba con su
salida literal para que cualquiera los rehaga.

---

**Analista** -- checker-only. No implemento, no promuevo, no cierro, no ratifico.
Este veredicto habilita la decision de cierre; el flip lo hace quien corresponda.
