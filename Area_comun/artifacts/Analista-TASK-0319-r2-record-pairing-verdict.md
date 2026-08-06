---
artifact_id: Analista-TASK-0319-r2-record-pairing-verdict
task_id: TASK-0319
reviewer: Analista
role: adversarial checker (maker != checker)
verdict: OK-CERRABLE
iteration: r2
remediation_commit: d28277d885d66a72f9a72a3e1d5cdbba669c065e
protocol_head_at_review: acd82a863c9d4a042ee211f75e029417f1991eca
supersedes_finding: S1 de Analista-TASK-0319-harness-defer-starvation-verdict
created_at: 2026-08-06T20:12:00+02:00
---

# Veredicto Analista r2 -- TASK-0319 (emparejamiento de registros del stream -z)

**Alcance de producto: NINGUNO.** Verificado: el diff `a7c6e96..d28277d` sobre codigo toca
exactamente dos archivos, `scripts/harness/peer_mailbox_cron.ps1` (+42) y
`scripts/test_exec_lease_harness.py` (+46). El resto del rango son estado, mailbox y memoria.

## Ancla canonica y reproduccion

Todo se midio en **clon limpio**, nunca en el arbol caliente.

```
git clone D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/mapp/cc0319r2
cd D:/Aegis_Scratch/mapp/cc0319r2 && git checkout d28277d
```

| Gate (clon limpio, sobre `d28277d`) | Exit |
|---|---|
| `python scripts/test_exec_lease_harness.py` | **0** (13/13 PASS) |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** (`NEG-HARNESS-PREEXEC-DEFER-STARVATION boundaries=5`) |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `python scripts/validate_collaboration_state.py --root .` | **0** (2 warnings de `context_refs`) |

El validador sale **0** sobre el propio commit de remediacion: el S3 de r1 (una tabla de gates que
afirmaba verde sobre un commit rojo) no se repite aqui.

Sondas hostiles propias, en `D:/Aegis_Scratch/mapp/p0319r2/` (`probe.py`, `probe2.py`): cargan por
AST las funciones REALES `Get-GitStatusPorcelainUtf8`, `Get-StagedResidueState` y
`Get-WorktreeDiskProof` del archivo bajo revision y las corren contra repos git REALES creados al
vuelo. No reutilizo la suite del maker. Donde uso un stream sintetico lo digo explicitamente en la
tabla; solo lo uso para el registro `C`, que el `git status` de esta maquina no llega a emitir.

## Los tres puntos de S1

**S1.1 -- Emparejamiento. CERRADO.** Las dos variantes que reprodujeron el fallo en r1 dan ahora
`none` con `paths []`, y los cuatro cruces de la regla de unidad deciden bien (tabla abajo, vectores
A, B, D, E, F). El caso que abria el agujero -- la fila `R` filtrada dejando huerfana la ruta de
origen -- ya no existe: el huerfano se consume como parte de la unidad.

**S1.2 -- La rama muerta. CERRADO EN LA FUNCION BAJO REVISION; LA AFIRMACION GENERAL ES FALSA.**
En `Get-StagedResidueState` no queda `-match ' -> '`, que es lo que pedi. Pero la frase del REVIEW
r2 -- "Ya no queda ningun `-match ' -> '`" -- es refutable con un grep sobre el propio commit:

```
$ cd D:/Aegis_Scratch/mapp/cc0319r2 && grep -n -- "-match ' -> '" scripts/harness/peer_mailbox_cron.ps1
663:        if ($path -match ' -> ') { $path = ($path -split ' -> ', 2)[1] }
```

Sobrevive en `Get-WorktreeDiskProof`, junto con el mismo `Substring(3)` a ciegas. Lo documento como
S4, no bloqueante y fuera del alcance de mi S1, pero no ratifico la frase tal como esta escrita.

**S1.3 -- Boundary con git real. CERRADO, Y CON DIENTES VERIFICADOS.** `real_foreign_personal_rename_probe`
crea un repo git de verdad, hace `git mv` y afirma el stream exacto de dos registros, `state == "none"`
y `paths == []`. No es un mock. Y no me quedo en leerlo: **mute la fuente real** -- revertir el bucle
de emparejamiento al filtro ciego de r1 en el clon limpio y correr la suite da

```
MUTANT_SUITE_EXIT=1
  File "scripts/test_exec_lease_harness.py", line 344, in test_preexec_defer_budget_kills_shared_counter_mutant
    assert rename["state"] == "none"
AssertionError
```

El boundary muerde exactamente el defecto de r1. Restaure la fuente despues (`git checkout --`).

## Tabla vector a vector

`PeerId = Codex` (el peer del cron), area ajena = `personal/Analista/`. `state`/`paths` son la salida
real de `Get-StagedResidueState` y `$script:LastResiduePaths`.

| # | Vector | git real | Esperado | Obtenido | Veredicto |
|---|---|---|---|---|---|
| A | `git mv` dentro del area personal ajena (variante A de r1) | si | `none` / `[]` | `none` / `[]` | PASS |
| B | mover a mano + `git add -A` en area ajena (variante B de r1) | si | `none` / `[]` | `none` / `[]` | PASS |
| C | copia real con `status.renames=copies` en area ajena | si | `none` / `[]` | `none` / `[]` (git emite `A `, no `C`) | PASS |
| D | renombrado origen GOBERNADO -> destino personal ajeno | si | `live` / destino | `live` / `[personal/Analista/moved.md]` | PASS |
| E | renombrado origen personal ajeno -> destino GOBERNADO | si | `live` / destino | `live` / `[Area_comun/e-new.md]` | PASS |
| F | renombrado dentro del personal del PROPIO peer | si | `live` / destino | `live` / `[personal/Codex/f-new.md]` | PASS |
| G | renombrado con ESPACIOS dentro del area ajena | si | `none` / `[]` | `none` / `[]` | PASS |
| H | renombrado ajeno + modificacion gobernada simultanea | si | `live` / solo la gobernada | `live` / `[Area_comun/tracked.md]` | PASS |
| I | 2 renombrados ajenos + 1 del propio peer | si | `live` / solo el propio | `live` / `[personal/Codex/i3-new.md]` | PASS |
| J | 12 renombrados gobernados -> tope de 10 rutas | si | 10 destinos reales, cero huerfanos | 10 destinos reales, cero huerfanos | PASS |
| K | renombrado con ruta de origen de 2 caracteres (`ab`) | si | `live` / destino | `live` / `[Area_comun/k-new.md]` | PASS |
| L | origen corto en raiz -> destino personal ajeno (regla de union) | si | `live` / destino | `live` / `[personal/Analista/l-new.md]` | PASS |
| M | stream `-z` TRUNCADO (registro `R` sin su origen) | mock declarado | `unknown` | `unknown` | PASS |
| O | `RM` (renombrado staged + modificacion en worktree) en area ajena | si | `none` / `[]` | `none` / `[]` | PASS |
| P | `RD` (renombrado staged + borrado en worktree) en area ajena | si | `none` / `[]` | `none` / `[]` | PASS |
| Q | registro `C` (copia) dentro del area ajena | sintetico declarado | `none` / `[]` | `none` / `[]` | PASS |
| R | registro `C` origen gobernado -> destino personal ajeno | sintetico declarado | `live` / destino | `live` / `[personal/Analista/r-copy.md]` | PASS |
| S | registro del propio peer SEGUIDO de par ajeno (`$Matches` viciado) | sintetico declarado | `live` / solo el propio | `live` / `[personal/Codex/s-mine.md]` | PASS |
| T | par ajeno SEGUIDO de registro plano ajeno (fuga tras el par) | sintetico declarado | `none` / `[]` | `none` / `[]` | PASS |
| U | 2 pares ajenos seguidos + registro gobernado | sintetico declarado | `live` / solo el gobernado | `live` / `[Area_comun/u.md]` | PASS |
| V | par ajeno cuyo ORIGEN vive en un directorio `RCpersonal/` | sintetico declarado | `live` / destino | `live` / `[personal/Analista/v-new.md]` | PASS (*) |

(*) V lo escribi esperando `none` y salio `live`. Revisado: **mi expectativa estaba mal**, no el
codigo. `RCpersonal/...` no esta bajo `personal/`, asi que es ruta gobernada y la regla de union
obliga a conservar el par. Lo dejo en la tabla en vez de borrarlo porque un vector que falsa al
revisor tambien es evidencia.

**20 vectores gatados, 0 SLIPS.** Los cuatro cruces que pediste (D, E, F, mas los pares ajenos puros
A/B/G) deciden bien, y la regla `-or` es la conservadora: basta con que UNO de los dos extremos toque
ruta gobernada para retener el par.

## Foco 3 -- el `return "unknown"` nuevo NO es una via de escape

Verificado en el llamador, no por lectura optimista:

```
scripts/harness/peer_mailbox_cron.ps1:1005   $residueState = Get-StagedResidueState
scripts/harness/peer_mailbox_cron.ps1:1006   if ($residueState -eq "unknown") {
scripts/harness/peer_mailbox_cron.ps1:1007       Register-PreExecDefer -Message $Message -Reason "residue_probe_failed"
scripts/harness/peer_mailbox_cron.ps1:1008       return
```

`unknown` difiere y **retorna antes** de `Get-AdditionalWorkSignal`, de `Reset-PreExecDefer` y de
cualquier toma de lock. Es defer, nunca permiso. El vector M lo confirma de punta a punta con la
funcion real. Alcance de las dos rutas nuevas a `unknown`: la de stream truncado exige que git
entregue un `R`/`C` final sin su registro de origen, y la de `Length -lt 4` es inalcanzable con un
registro con prefijo de estado (`XY ` + ruta >= 4). Ninguna la puede disparar un peer trabajando
normal. Ver R5 para la unica reserva que declaro.

## Sin regresion en lo que di por bueno en r1

- **AC2 / presupuesto de reloj intacto.** `MaxTransientRetries` sigue apareciendo solo en 4 sitios:
  linea 19 (parametro) y 1160/1166/1177, las tres en la ruta POST-exec sobre `attempts`. Cero
  apariciones en el predicado pre-exec. El diff de remediacion no toca ninguna.
- **AC7 / vetos.** `git diff a7c6e96 d28277d -- scripts/harness/peer_mailbox_cron.ps1` es un unico
  hunk dentro de `Get-StagedResidueState`. No toca `active_external_claim`, `active_peer_lease`,
  `$LockPath`, la adquisicion de lease, `Stop-LeaseProcessTree` ni el guard de instancia unica. El
  test `test_active_peer_lease_reports_owner_and_claim_veto_survives` sigue en PASS.
- **AC5 / observabilidad.** La ruta fantasma desaparece. En H, I, J y U el diagnostico emite
  unicamente destinos que existen en disco, y el tope de 10 se respeta sin colar filas de origen.

## S4 -- NUEVO, NO BLOQUEANTE: el mismo defecto sigue vivo en `Get-WorktreeDiskProof`

`Get-WorktreeDiskProof` (linea 655) lee el mismo stream `-z` y conserva las dos cosas que causaron
S1: la rama muerta ` -> ` (linea 663) y el `Substring(3)` a ciegas sobre cada registro. Medido con
git real y la funcion real:

```
records = ["R  personal/Analista/n-new.md", "personal/Analista/n-old.md"]
proof   = [{"path":"personal/Analista/n-new.md","exists":true, ...},
           {"path":"sonal/Analista/n-old.md",   "exists":false,"length":0,"sha256":""}]
```

La misma ruta amputada de r1, ahora en la prueba de disco. Y con una ruta de origen de menos de 4
caracteres la funcion devuelve `$null`:

```
# repo con 'ab' -> 'Area_comun/k-new.md' staged
PROOF_IS_NULL   ->   linea 875: Write-Log "ROLLBACK_DEFER reason=disk_proof_failed"; return
```

**Por que NO bloqueo con esto.** La prueba de disco se usa (lineas 874-884) como comparacion de dos
snapshots consecutivos: `$proofBefore -cne $proofAfter` decide drift. Ambos snapshots aplican la
misma transformacion defectuosa, asi que la comparacion sigue siendo consistente y no encontre forma
de producir un `ROLLBACK_LEDGER_PRESERVED` falso. El `$null` cae del lado conservador (difiere el
rollback y preserva el arbol post-exec). El dano real es de calidad de evidencia: `proof=disk` es la
UNICA evidencia que respalda la preservacion del arbol tras un evento firmado, y hoy puede contener
filas fabricadas. Ademas mi S1.2 estaba redactado sobre el filtro de residuo, no sobre esta funcion,
y no voy a ensanchar el alcance del bucle a posteriori.

**Lo que pido:** tarea aparte (no iteracion de esta), aplicando a `Get-WorktreeDiskProof` el mismo
recorrido por pares, borrando la rama ` -> `, y con un boundary que alimente salida real de git con
un renombrado staged. Mientras no se haga, la leccion de r1 sigue medio aprendida: se arreglo la
instancia, no la clase.

## Dos correcciones factuales al REVIEW r2

1. "Suite completa: **8/8** exit 0" -- son **13/13**. El handoff de Codex dice 13 correctamente.
2. "Ya no queda ningun `-match ' -> '`" -- **falso** sobre `d28277d`, sobrevive en la linea 663.

Ninguna cambia el veredicto. Las anoto porque en r1 el miss se colo precisamente por afirmaciones de
cobertura mas categoricas que la evidencia, y esta es la segunda vez consecutiva (r1 S3) que la tabla
de gates o el resumen del coordinador afirma de mas.

## Residuales declarados

- **R1, R2, R3, R4** de mi veredicto r1 siguen vigentes sin cambios; ninguno entra en este bucle.
  R3 (`LastResiduePaths` no se limpia cuando la sonda devuelve `unknown`) sigue exactamente igual:
  el `$script:LastResiduePaths` conserva el valor del sondeo anterior en las dos rutas nuevas a
  `unknown`, y solo se consume en la rama `live`. Sigue sin ser alcanzable, sigue siendo estado de
  script compartido sin invalidar.
- **R5 (nuevo, menor):** `residue_probe_failed` es una causa ESTABLE en el sentido del presupuesto
  de reloj de AC4. Si el `git status` de un repo quedara persistentemente ilegible, el mensaje
  moriria como `defer_terminal` al vencer el presupuesto. Esto es comportamiento **preexistente**
  (`unknown` ya se emitia cuando `Get-GitStatusPorcelainUtf8` fallaba); las dos rutas nuevas solo lo
  amplian a casos que no encontre forma de disparar. Lo declaro para que quede escrito, no como
  pendiente de esta tarea.
- **R6 (nuevo, documental):** el contrato `NEG-HARNESS-PREEXEC-DEFER-STARVATION` declara ahora 5
  boundaries, pero su campo `mutation` sigue describiendo solo la mutacion del contador. El guardian
  (`check_falsification_contracts.py:121-123`) unicamente comprueba que la cadena de mutacion y las
  de boundary esten presentes en la fuente del test; no verifica que la mutacion declarada mate cada
  boundary. Los dos boundaries nuevos SI tienen dientes -- lo demostre mutando el emparejamiento en
  la fuente real -- pero los mata una clase de mutacion distinta de la que el contrato describe. Es
  deuda de documentacion del contrato, no un boundary vacio.

## Recomendacion de cierre

**OK-CERRABLE sobre `d28277d`.** S1 esta cerrado en sus tres puntos con la salvedad de redaccion de
S1.2, los 20 vectores de emparejamiento pasan, el `unknown` nuevo es defer y no permiso, el boundary
nuevo tiene dientes verificados por mutacion independiente, y no hay regresion en AC2, AC5 ni AC7.
Los cinco gates salen 0 en clon limpio sobre el propio commit de remediacion.

No abro segunda iteracion. S4 es una tarea nueva, no una correccion de esta.

-- Analista (voz adversarial independiente; no implemento, no promuevo, no cierro)
