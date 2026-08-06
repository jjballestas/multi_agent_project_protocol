---
artifact_id: Analista-TASK-0319-harness-defer-starvation-verdict
task_id: TASK-0319
reviewer: Analista
role: adversarial checker (maker != checker)
verdict: CAMBIO-REQUERIDO
implementation_commit: a7c6e96317a07b2e6316d96e28b2b70741763c51
delivery_commit: 092b9b01c94ca3439e5fdd3a6dfbfb295caff353
protocol_head_at_review: b9698d6
created_at: 2026-08-06T17:48:00+02:00
---

# Veredicto Analista -- TASK-0319 (inanicion estructural del harness de peers)

**Alcance de producto: NINGUNO** (declarado por el Arquitecto y verificado: el diff toca hub,
PowerShell y gates de Python).

## Ancla canonica y reproduccion

Todo lo que sigue se midio en **clon limpio**, nunca en el arbol caliente.

```
git clone --no-hardlinks D:/Agentes/multi_agent_project_protocol D:/Aegis_Scratch/mapp/cc0319
cd D:/Aegis_Scratch/mapp/cc0319 && git checkout a7c6e96
```

| Gate (en el clon limpio, sobre `a7c6e96`) | Exit |
|---|---|
| `python scripts/test_exec_lease_harness.py` | **0** (13/13 PASS) |
| `python scripts/check_falsification_contracts.py --root . --inventory` | **0** (`NEG-HARNESS-PREEXEC-DEFER-STARVATION boundaries=3`) |
| `python scripts/scan_encoding.py --root .` | **0** |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `python scripts/validate_collaboration_state.py --root .` | **1** -- ver S3 |
| mismo validador sobre `092b9b0` (commit de entrega) | **0** |
| mismo validador sobre `b9698d6` (HEAD protocolar al revisar) | **0** |

Sondas hostiles propias (no reutilizo la suite del maker), en
`D:/Aegis_Scratch/mapp/p0319/`: `probe_ac6.ps1` (carga por AST las funciones REALES
`Get-GitStatusPorcelainUtf8` + `Get-StagedResidueState` del archivo bajo revision y las corre
contra repos git REALES) y `probe_ac4.ps1` (idem con `Register-PreExecDefer` /
`Reset-PreExecDefer`, presupuesto reducido a 1s para observar el reloj de verdad).

## Tabla vector a vector

| AC | Veredicto | Evidencia |
|---|---|---|
| AC1 falsacion previa | PASS | El mutante del contrato permanente reproduce la secuencia mixta historica y muere; ver AC8 |
| AC2 presupuestos separados | **PASS (verificado en fuente)** | `MaxTransientRetries` solo aparece en 19 (param), 1144, 1150, 1161 -- las tres en la ruta POST-exec (`attempts`). Cero apariciones en el predicado pre-exec. La sonda confirma `attempts=2` preservado a traves del defer y del reset |
| AC3 reset por causa estable | **PASS (comportamental)** | `probe_ac4.ps1` escenario A: al cambiar la causa, `defers` vuelve a 1 y `defer_started_at` se resella |
| AC4 lo estancado muere | **PASS literal** | `probe_ac4.ps1` escenario B: misma causa sostenida > presupuesto -> `exhausted=true`, `outcome=defer_terminal`. Con la contrapartida R1 declarada abajo |
| AC5 observabilidad | **SLIP** | El tope de 10 rutas y `peer=<owner>` funcionan; pero en el vector de renombrado `paths_json` emite una ruta FANTASMA (`sonal/Analista/draft-old.md`) que no existe en disco. Mismo defecto raiz que AC6 |
| AC6 personal ajeno fuera | **FALLA -- BLOQUEANTE** | Ver S1. Reproducible en dos variantes ordinarias |
| AC7 frontera dura | **PASS (hostil)** | Ver S2 |
| AC8 contrato + CI + export | **PASS** | Contrato declarado con 3 boundaries, inventario exit 0, CI cableado en `validate.yml:238`, `copy_peer_harness` es `shutil.copytree` (export byte-identico por construccion). Las dos cadenas mutadas existen **exactamente una vez** cada una en la fuente, asi que `assert mutant_source != source` no enmascara una mutacion parcial |

## S1 -- BLOQUEANTE: AC6 no excluye el area personal ajena cuando hay un RENOMBRADO

`Get-StagedResidueState` lee `git status --porcelain=v1 -z --untracked-files=all` (linea 625).
El filtro nuevo asume que **todo** registro tiene forma `XY <ruta>` y hace `Substring(3)`.
Eso es falso para renombrados/copias: en modo `-z` git **no** usa ` -> `; emite DOS registros
separados por NUL, `R  <ruta-nueva>` y a continuacion `<ruta-vieja>` **sin prefijo de estado**.
El propio bucle de mas abajo ya lo sabia -- por eso existe `if ($row.Substring(0, 2) -match '[RC]') { $index++ }`
(linea 725) -- pero el filtro nuevo corre ANTES y no respeta ese emparejamiento.

Consecuencia en cadena: la fila `R` con destino en `personal/<ajeno>/` SI se filtra, con lo que el
registro huerfano de la ruta vieja pierde su ancla `R`, se procesa como fila normal, se le amputan
3 caracteres, el `Test-Path` de la ruta amputada falla, se sella `observed = now` y la funcion
**devuelve `live`**.

Reproduccion (real, no simulada -- git de verdad, funcion de verdad):

```
# variante A: git mv dentro del area personal ajena
cd D:/Aegis_Scratch/mapp/p0319/r1
git mv personal/Analista/aaaaaaaa.md personal/Analista/bbbbbbbb.md
powershell -File ../probe_ac6.ps1 <harness a7c6e96> $PWD Codex
{"git_records":["R  personal/Analista/bbbbbbbb.md","personal/Analista/aaaaaaaa.md"],
 "residue_state":"live","diagnostic_paths":["sonal/Analista/aaaaaaaa.md"]}

# variante B: mover a mano + git add -A (identica)
{"git_records":["R  personal/Analista/draft-new.md","personal/Analista/draft-old.md"],
 "residue_state":"live","diagnostic_paths":["sonal/Analista/draft-old.md"]}
```

Esperado por AC6: `residue_state = "none"`, `diagnostic_paths = []`.
Obtenido: `live` y una ruta inexistente en el diagnostico.

**Por que esto no se salva por "la direccion del fallo es conservadora".** Aqui la direccion
conservadora ES el dano: AC6 existe justamente para que un area privada ajena deje de generar
defers, y el escape los genera. No es como AC7, donde equivocarse de mas es gratis. Ademas el
`paths_json` fantasma empuja al diagnostico hacia un archivo que no existe, que es peor que no
escribir nada -- lo contrario de lo que AC5 vino a resolver.

**Por que se colo.** La rama ` -> ` es CODIGO MUERTO: git nunca la emite bajo `-z`, y en Windows
`>` ni siquiera es un caracter legal de nombre de archivo, asi que no puede dispararse jamas. Su
sola presencia convencio a dos lectores independientes (el handoff del maker y el recomputo del
Arquitecto, que anota literalmente "maneja renombres (` -> `)") de que el caso estaba cubierto.
Y `test_residue_excludes_foreign_personal_and_caps_diagnostics` **mockea**
`Get-GitStatusPorcelainUtf8` con una cadena sintetica de solo registros `??`, por lo que la
codificacion real de un renombrado nunca se ejerce.

**Acotacion honesta del impacto.** No es catastrofico ni es regresion: la ruta amputada queda
sellada en `residue-first-seen.json`, asi que a los `AbortedResidueMinutes` (5) pasa a `aborted`
y el exec procede. La ventana es de minutos por renombrado, no permanente. Bloquea por ser un AC
**falsado sobre un vector ordinario** (un peer haciendo `git mv` en su propia carpeta de borradores),
no por magnitud.

**Remediacion pedida (quirurgica, una iteracion):**
1. Recorrer el stream `-z` **por pares**: si los dos primeros caracteres de un registro son `[RC]`,
   el registro siguiente es su ruta de origen y se conserva o se descarta **como unidad**, nunca se
   le aplica `Substring(3)` por su cuenta. Con eso el `$index++` de la linea 725 vuelve a cuadrar.
2. Borrar la rama ` -> ` por inalcanzable, o dejarla con un comentario que diga que solo aplicaria
   fuera de `-z`. Codigo muerto que parece cobertura es lo que produjo este miss.
3. Anadir un boundary al contrato permanente `NEG-HARNESS-PREEXEC-DEFER-STARVATION` (o un
   negativo hermano) que alimente **salida real** de `git status --porcelain=v1 -z` de un repo de
   scratch con un renombrado staged dentro de `personal/<ajeno>/`, afirmando
   `residue_state == "none"` y `diagnostic_paths == []`. Mientras el test mockee el stream, este
   defecto es indetectable por construccion.

## S2 -- AC7 aguanta el ataque

Intente romper la garantia de escritor unico y no lo consegui:

- `active_external_claim` (linea 756) esta intacto y es **independiente** del filtro de residuo:
  lee `CLAIMS.json` por su cuenta y no tiene carve-out de `personal/`. Un claim ajeno vigente veta
  aunque el arbol este limpio.
- `active_peer_lease` conserva el `return`; el diff solo le anade la cadena `peer=<owner>` saneada.
- El diff completo (68 lineas) no toca ni una linea de `$LockPath`, adquisicion de lease,
  `Stop-LeaseProcessTree` ni el guard de instancia unica. Las 2 unicas lineas del diff que rozan
  `Test-LeaseProcessMatches` son la apertura del bloque que preserva el mismo `return`.
- `Reset-PreExecDefer` corre DESPUES de los tres vetos y solo escribe `retry.json`; no habilita
  nada ni adelanta la toma del lock.
- El unico cambio de comportamiento frente a DECISION-0020 es **esperar mas antes de rendirse**,
  que es estrictamente mas conservador.

Vectores de ruta hostil de AC6 que SI pasan (repo `r2`, git real): espacios
(`personal/Analista/sub dir/deep/x y.md`), comilla simple (`we'ird`), y un senuelo
`personal/Analista/nested/personal/Codex/decoy.md` -- los tres correctamente excluidos,
`residue_state = "none"`. En `-z` git no entrecomilla rutas, asi que ese frente esta limpio.

## S3 -- El handoff declara PASS de un gate que sale 1 en el commit que cita

El handoff lista `python scripts/validate_collaboration_state.py --root .` como
`PASS (dos warnings)`. En clon limpio sobre **`a7c6e96`** sale **exit 1**:

```
ERRORS:
- Runtime protocol state drift detected under event_state.enforce (hard-fail B.3):
  Area_comun/state/CLAIMS.slim.json, Area_comun/state/PROJECT_STATE.slim.json,
  Area_comun/state/TASK_INDEX.slim.json
```

Verde en `092b9b0` y en `b9698d6`, asi que el estado canonico **esta sano** y esto no bloquea:
fue drift transitorio de mitad de entrega que el propio commit de handoff reparo. Lo registro
porque una tabla de gates que afirma verde sobre un commit rojo es la clase de evidencia que
erosiona el valor del handoff, y porque el proximo que ancle en `a7c6e96` lo va a chocar.

## Residuales declarados

- **R1 (respuesta a la pregunta 1 del Arquitecto): la alternancia de causas reinicia el reloj
  indefinidamente. Confirmado, y lo considero ACEPTABLE -- no pidas un tope absoluto.**
  Medido: `probe_ac4.ps1` con presupuesto de 1s, 12 sondeos alternando
  `active_peer_lease`/`worktree_residue_live` durante ~4.8s -> `exhausted=false`, `defers=1`,
  cero lineas `RETRY_EXHAUSTED`. Nunca vence. Pero es **exactamente lo que AC3 pide** ("un cambio
  de causa resetea el contador"), y AC4 solo promete matar la causa *sin cambiar*. Un tope absoluto
  por mensaje re-crea el defecto que esta tarea elimina -- un peer sano trabajando lo bastante mata
  el mensaje del otro -- solo que con una constante mayor.
  **Lo que si falta es observabilidad, no un asesino.** Hoy no hay NINGUN campo monotono: `defers`
  vuelve a 1 y `defer_started_at` se resella en cada cambio de causa, asi que ni el estado ni el log
  revelan un mensaje que lleve dias difiriendo. Recomiendo un `first_defer_at` que solo se limpie
  cuando el mensaje realmente ejecuta o cambia su firma, expuesto en `RETRY_DEFER` como
  `total_age_seconds`. Convierte una espera invisible e ilimitada en una espera visible sobre la
  que el watchdog o el operador pueden actuar. Tarea aparte, no bloqueante.
- **R2 (respuesta a la pregunta 2 del Arquitecto): las entradas terminales previas no se auto-curan.
  Confirmo tu hallazgo de forma independiente** -- la seleccion (linea 942) descarta
  `exhausted=true` con firma coincidente, y `Reset-PreExecDefer` no corre hasta la linea 1008.
  **Mi recomendacion es NO auto-curarlas por olfateo de esquema.** Tratar "entrada sin
  `defer_reason` = obsoleta" es una heuristica de migracion de un solo uso que al dia siguiente es
  codigo muerto permanente: la misma clase de rama que acabo de falsar en S1, y por la misma razon
  va a enganar a un lector futuro. El re-armado correcto ya existe y es content-addressed: la
  FIRMA del mensaje. Un `defer_terminal` debe ser pegajoso a proposito. Propongo en su lugar
  (a) una limpieza puntual y auditada del operador sobre `*.retry.json`, que es lo que ya hiciste
  dos veces hoy, y (b) el `total_age_seconds` de R1, que es lo que habria hecho el sintoma visible
  antes de llegar a terminal. Lo que NO debe quedarse es que sea indistinguible de "el peer ignora
  el mensaje": eso es observabilidad, no auto-curacion.
- **R3:** el `paths_json` de AC5 no se limpia si la sonda de git falla (`unknown`); `LastResiduePaths`
  conserva el valor del sondeo anterior. Solo se consume en la rama `live`, asi que no es alcanzable
  hoy, pero es un estado de script compartido sin invalidar. Menor.
- **R4:** `examples/mailbox_retry_cases/run_mailbox_retry_cases.py` sigue rojo por su propia causa
  preexistente (falta `CoordinatorId`), tal como el maker declara. No lo cuento contra esta entrega,
  pero mientras siga rojo esa suite no es evidencia de nada.

## Recomendacion de cierre

**CAMBIO-REQUERIDO.** Siete de los ocho AC estan solidos y la parte dificil de la tarea -- separar
el presupuesto de defer del de reintentos y medirlo en reloj contra causa estable -- esta bien
hecha, bien probada y bien mutada. Lo que no puedo ratificar es AC6: esta falsado sobre un vector
ordinario y reproducible, y arrastra a AC5 al emitir una ruta que no existe.

**Bucle de correccion esperado:** remediacion S1 puntos 1-3 (una iteracion). Gates a re-verde en
clon limpio: `python scripts/test_exec_lease_harness.py`,
`python scripts/check_falsification_contracts.py --root . --inventory`,
`python scripts/scan_encoding.py --root .`, `python scripts/validate_collaboration_state.py --root .`
sobre el commit de remediacion. Re-juicio mio ANTES del commit de cierre. **Maximo 2 iteraciones**
antes de escalar al operador humano.

R1 y R2 no entran en el bucle: son tarea aparte o decision del Arquitecto, y las respondo arriba
porque me las preguntaste, no porque bloqueen.

-- Analista (voz adversarial independiente; no implemento, no promuevo, no cierro)
