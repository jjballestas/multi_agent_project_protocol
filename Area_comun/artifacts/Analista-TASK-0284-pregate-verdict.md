# Veredicto adversarial -- TASK-0284, el ultimo eslabon del pre-gate (commit 04ec9d1)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-22 02:21 +02:00 (reloj del sistema, sin convertir)
- Encargo: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0284-pregate
- **Veredicto: CHANGE-REQUIRED / NO-GO, y el bloqueo es SOLO de banco (el codigo es
  correcto). Los seis puntos del acceptance funcionan cuando los ejecuto con mis propios
  payloads de comportamiento. Pero DOS de los cinco negativos permanentes -- justo los dos
  de la lista de "prueba de bucle real" del acceptance (borrado que envejece; git con
  stderr grande sin cuelgue) -- MIDEN SU PROPIA SOMBRA: los mata solo un contrato de
  presencia-de-string, y ningun test de comportamiento los caza. Es la tercera aparicion
  del patron que esta unidad existe para cerrar.**

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado | `04ec9d1b3545c2619616fcf21b8284e256546ea9` ("fix(TASK-0284): bound conservative pre-gate defers") |
| HEAD del protocolo al emitir | `34c60b9` (== origin/main) |
| Es ancestro de origin/main | si (`git merge-base --is-ancestor 04ec9d1 origin/main` -> 0) |
| Commits posteriores sobre el codigo juzgado | ninguno (`git log 04ec9d1..origin/main -- scripts/harness/ examples/mailbox_retry_cases/` -> vacio) |
| Handoff | publicado como MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0284 (hoy en `mailbox/archived/`); el `context_ref` del encargo apunta a una ruta `handoffs/` que no existe -- residuo R3 |
| Clon limpio | `D:/ccv0284` (04ec9d1); mutantes en `D:/ccvA` |
| Alcance | solo este hub. **Sin producto en alcance.** |
| Ventana | `CLAIMS.json` sin claims activas (2 filas Codex del 3-jul en estado `blocked`, scope solo a su propia linea); `mailbox/open/` solo el encargo |

## 2. Reproduccion (por exit code, en clon limpio sobre 04ec9d1)

```
python scripts/validate_collaboration_state.py                 -> exit 0
python scripts/scan_encoding.py                                -> exit 0
python scripts/scan_domain_neutrality.py                       -> exit 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0  ("mailbox retry cases: PASS")
```

Los cuatro gates estan VERDES sobre `04ec9d1`. Drift 0 (validador limpio). Nada de lo que
sigue contradice los gates: mi hallazgo es sobre QUE prueba el banco, no sobre si pasa.

## 3. Lo que esta SOLIDO (verificado por comportamiento, con mis propios payloads)

Extraje las funciones VERBATIM del clon limpio y las corri en sandboxes git reales, con el
probe FUERA del arbol evaluado, sin confiar en nombres de test ni en el handoff.

### 3.1 F-0281-07 -- el borrado ENVEJECE (ya no es absorbente). CERRADO.

Sandboxes git reales, borrado real de un fichero rastreado, `AbortedResidueMinutes 0`:

| Caso | R1 | R2 | R3 | Veredicto |
|---|---|---|---|---|
| Borrado no indexado (` D governed.txt`) | live | aborted | aborted | **PASS -- envejece** |
| Borrado indexado (`git rm`, `D  governed.txt`) | live | aborted | aborted | **PASS -- envejece** |

Contraste con mi veredicto de 0281-iter3 sobre el mismo caso: alli daba `live/live` para
siempre (V6/V7/V12). Ahora sale de `live` con un `first-seen` persistido por ruta. La regla
"no-resuelve implica live" dejo de ser absorbente. Confirmado tambien que el estado
`residue-first-seen.json` vive en `.protocol-tmp/` (gitignore, linea 16), asi que NO se
auto-referencia en el status del repo vivo -- la rama "arbol limpio -> none + borra el
estado" funciona.

### 3.2 F-0281-08 -- git drena concurrente y no se cuelga. CERRADO (codigo).

Corri el bloque de drenaje EXACTO del commit contra un hijo que inunda stderr con 200 KB y
no escribe stdout (el escenario de mi seccion 6 de iter3):

```
NEW (async, bajo revision):  ok exit=0 stdout_len=0 stderr_len=204800 ms=191
SEQ (patron pre-fix, sin timeout): HUNG (timeout 124) = DEADLOCK
```

El drenaje asincrono con `WaitForExit(10000)` + `Task::WaitAll(...,10000)` termina en
191 ms y falla-cerrado (timeout -> ok=false -> "unknown" -> defer). El patron secuencial que
tenia iter3 se cuelga. El fix es real. El pre-gate ademas se movio ANTES del `Write-Utf8NoBom
-Path $LockPath`, asi que un probe lento/fallido difiere sin dejar lock huerfano.

### 3.3 Punto 5 y 6 -- la forense RETIENE sin lock/lease. CERRADO (codigo).

JSON gobernado truncado a mano (lo que deja un exec matado o una escritura del coordinador en
vuelo), mtime fresco, sin lock, `AbortedResidueMinutes 60`:

```
git status:  M Area_comun/state/CLAIMS.json
Get-StagedResidueState -> live   (RETIENE el arranque)
```

La forense de arbol-sucio es co-autoritativa y corre antes del lock; el coordinador escribe
sin lock/lease y aun asi la forense lo ve por el arbol. No encontre un camino en que la
ausencia de lock autorice un arranque sobre un arbol que otro dejo sucio o roto (FRESCO).

### 3.4 Claims solo refuerzan, con vejez dura. CERRADO (codigo).

`Get-AdditionalWorkSignal`, seis payloads:

| Caso | Senal | Veredicto |
|---|---|---|
| Claim externa fresca activa | active_external_claim | PASS |
| Claim externa VENCIDA (3-jul) | none | PASS (vencida jamas activa) |
| Claim propia activa | none (saltada) | PASS |
| Claim externa `released`, futura | none (saltada) | PASS |
| Dos filas rancias 3-jul + una fresca | active_external_claim | PASS |
| `expires_at` no parseable | none (saltada) | PASS |

La ausencia de claim NO autoriza arranque por si sola (la forense sigue mandando). Lectura de
CLAIMS fail-closed por deadline: un fichero torn -> reintento -> si sigue torn ->
`claims_unreadable` -> defer (verificado por lectura del cuerpo de `Read-JsonWithDeadline`).

### 3.5 Defer terminal que escapa (F-0281-04). CERRADO, y con test de comportamiento REAL.

`Register-PreExecDefer` fija `exhausted=$terminal` al llegar al tope y `Get-ProcessablePeerMessages`
ya no re-incluye el mensaje agotado; el outcome pasa a `defer_terminal` con senal de watchdog.
Lo caza `run_unstaged_residue_case` por comportamiento (ver seccion 4).

## 4. EL HALLAZGO -- dos negativos miden su propia sombra (bloqueante de banco)

El encargo pidio explicitamente: "cada negativo declara la mutacion que lo mata; corre esas
mutaciones y exige rojo. Un negativo que mide su propia sombra es lo que dejamos pasar dos
veces." Lo hice, en dos pasadas sobre clones limpios.

**Pasada A (banco tal cual se entrega).** Aplique las cinco mutaciones declaradas al fichero
real y corri la suite entera. Las CINCO salen rojas -- pero TODAS por la MISMA asercion:

```
AssertionError: TASK-0284 pre-gate contract is incomplete   (run_pregate_contract_mutants)
```

Esa funcion NO ejecuta nada: lee el `.ps1` como TEXTO y comprueba presencia de literales
(`ReadToEndAsync()` contado >=2, `"WaitForExit(10000)"`, `"$firstSeen.ContainsKey($relative)"`,
`"exhausted = $terminal"`, `"$expires -gt $now"`, y que el pre-gate aparezca antes del lock).
Es un detector-de-cambio de string, no una prueba de conducta.

**Pasada B (deshabilito SOLO ese contrato de string; dejo todos los tests de comportamiento).**
Vuelvo a aplicar cada mutacion. Esto revela que caza de verdad el banco:

| Mutacion declarada | Que rompe | Cazada por COMPORTAMIENTO? | Como |
|---|---|---|---|
| `terminal_defer_removed` (`exhausted=$terminal`->`$false`) | escape de defer (F-0281-04) | **SI** | `run_unstaged_residue_case` (exhausted=False) |
| `dirty_forensics_removed` (veto de arbol sucio) | retencion (pts 5/6) | **SI** | `run_unstaged_residue_case` (falta senal watchdog) |
| `sequential_pipe_drain` (F-0281-08) | deadlock de git | INCIDENTAL | `run_nul_residue_path_cases` cae a "unknown" por un choque de TIPO en `Task::WaitAll` (recibe un string), NO por reproducir un cuelgue |
| **`deleted_first_seen_removed`** (F-0281-07) | borrado absorbente | **NO -- PASA** | ningun test lo caza |
| **`claims_expiry_removed`** (`$expires -gt $now`->`$true`) | claim vencida leida activa | **NO -- PASA** | ningun test lo caza |

Las dos filas en negrita son el problema. `deleted_first_seen_removed` REINTRODUCE
EXACTAMENTE el bug F-0281-07 (borrado eternamente `live`) y la suite queda VERDE sin el
contrato de string. La razon es estructural: el unico test de vejez de comportamiento
(`run_nul_residue_path_cases`) usa un fichero NO RASTREADO con mtime viejo, que envejece por
la rama `Test-Path -> LastWriteTimeUtc`, NO por `first-seen`. Un BORRADO -- que es la forma
que no tiene mtime y la que estaba rota -- nunca se ejercita. Igual con la vejez de claims:
`$expires -gt $now -> $true` no cambia ningun test porque el sandbox no tiene una claim
externa que forzara la conducta.

Esto choca de frente con dos criterios del acceptance:

- Acceptance #8(i): "borrado que envejece Y SALE DEL DEFER" -- exigido "demostrado". Solo hay
  presencia-de-string. `verification_cmd`: "Prueba de bucle real: borrado en el arbol -> el
  pre-gate sale del defer al envejecer" -- AUSENTE.
- Acceptance #8(ii): "drenaje con stderr grande sin cuelgue ni lock huerfano". `verification_cmd`:
  "Prueba de bucle real: git con stderr grande -> el lector termina, no cuelga, y el lock no
  queda tomado" -- AUSENTE. El mutante de una linea que declara el maker se caza por un choque
  de tipo, no por un deadlock; el patron secuencial verdadero solo lo frena el string.

El handoff del maker afirma que el banco "also kills mutants that remove ... deleted-path
first-seen state ... claim expiry". Es cierto SOLO en el sentido presencia-de-string; leido
como comportamiento, sobre-declara la cobertura. Es la misma forma que deje pasar en iter2 e
iter3: la unidad se esta cerrando contra un control que no la mide, ahora por tercera vez, y
sobre el hallazgo mas importante (el borrado absorbente que abrio esta unidad).

## 5. Respuesta directa a tu pregunta

> Con la forense reteniendo el veto y el lease/claims solo reforzando, queda algun camino por
> el que un arranque ocurra sobre un arbol roto o sobre una escritura del coordinador en
> vuelo, o por el que un defer vuelva a ser absorbente?

**Con el CODIGO entregado: no lo encontre.** El arbol roto/sucio FRESCO retiene (3.3), la
escritura del coordinador en vuelo retiene, y los defers ya no son absorbentes: el borrado
envejece (3.1) y el defer va a terminal (3.5). La forense no se jubila y corre antes del lock.

**Pero la GARANTIA no esta protegida por un negativo falsable** para dos de esos caminos. Si
manana alguien revierte el `first-seen` del borrado o la vejez de claims dejando los strings en
su sitio, el borrado vuelve a ser absorbente (F-0281-07 renacido) y la suite queda VERDE. El
camino no esta abierto hoy; esta abierto para la REGRESION silenciosa de manana, que es
precisamente lo que esta unidad prometio cerrar.

## 6. Tabla de veredicto por vector del encargo

| Vector | Medicion | Veredicto |
|---|---|---|
| (1) Borrado envejece via first-seen | R1 live -> R2/R3 aborted (indexado y no) | **PASS (codigo)** |
| (2) Defers escapan a defer_terminal | exhausted=true, no re-encolado, watchdog | **PASS (codigo + test real)** |
| (3) git drena concurrente, timeout, fail-closed, sin lectura tras lock sin proteger | async 191ms / seq deadlock; pre-gate antes del lock | **PASS (codigo)** |
| (4) Decodificador mata mutante de codepage con caso RANCIO | `run_nul_residue_path_cases`: rancio -> aborted, codepage -> live | **PASS (test real)** |
| (5) Exec matado, arbol roto, sin lock -> forense RETIENE | JSON truncado fresco -> live | **PASS (codigo)** |
| (6) Coordinador sin lock/lease -> forense retiene | modificacion gobernada fresca -> live | **PASS (codigo)** |
| Negativo permanente: borrado que envejece (#8 i) | mutante `delfs` PASA sin el string-contract | **SLIP -- sombra, bloqueante de banco** |
| Negativo permanente: stderr grande sin cuelgue (#8 ii) | mutante `seq` cazado por tipo, no por deadlock; sin bucle real | **SLIP -- sombra, bloqueante de banco** |
| Negativo permanente: vejez de claims | mutante `claims` PASA sin el string-contract | **SLIP -- sombra (menor: claims solo refuerzan)** |
| Negativo permanente: veto de arbol sucio (pts 5/6) | mutante `forensics` cazado por comportamiento | PASS |
| Negativo permanente: defer terminal | mutante `term` cazado por comportamiento | PASS |

## 7. Residuos declarados (NO bloqueantes)

- **R1**: El mutante `sequential_pipe_drain` del banco (reemplaza un solo `ReadToEndAsync()`)
  se caza por un choque de tipo en `Task::WaitAll`, no por reproducir el deadlock. Un bucle
  real (mi seccion 3.2) es lo unico que prueba el cuelgue de verdad.
- **R2**: La persistencia de `first-seen` se trunca en la PRIMERA ruta `live` (solo se guardan
  las filas hasta ahi). Con varios residuos la vejez se SERIALIZA (cada ruta empieza su reloj
  tras la anterior), asi que el arbol puede quedar `live` bastante mas que `AbortedResidueMinutes`.
  Direccion segura (fail-closed, difiere de mas), no absorbente; lo dejo como residuo, no como
  bloqueo. Verificado que igualmente termina en `aborted`.
- **R3**: El `context_ref` del encargo apunta a `Area_comun/handoffs/HANDOFF-TASK-0284-...md`,
  que no existe; el handoff real se publico y archivo como MSG en el mailbox. Anomalia menor de
  traza (DECISION-0018), no afecta el codigo.
- **R4**: `Get-AdditionalWorkSignal` con `expires_at` malformado salta la claim (no la trata
  como activa). Aceptable porque las claims solo refuerzan; nunca autorizan un arranque.

## 8. Recomendacion de cierre y bucle de arreglo

**CHANGE-REQUIRED / NO-GO al cierre**, pero con una distincion que quiero explicita porque
pesa en tu decision de redespliegue: **el codigo esta correcto** -- hice yo las "pruebas de
bucle real" que al banco le faltan (borrado que envejece y sale del defer; git con stderr
grande que no se cuelga) y las DOS PASAN. Lo que falta es de BANCO, no de logica.

Arreglo que tiene que sobrevivir (no propongo implementacion; soy checker), TEST-ONLY:

1. Un negativo de BUCLE REAL para el borrado: arbol cuyo unico residuo sea un borrado
   (indexado y no indexado), con `AbortedResidueMinutes 0`, corriendo el runner completo, que
   termine en `EXEC_START=1` tras envejecer; y que FALLE (rojo) si se revierte el `first-seen`
   del borrado. Debe morir el mutante `deleted_first_seen_removed` por COMPORTAMIENTO, no por
   presencia de string.
2. Un negativo de BUCLE REAL para el drenaje: un `git status` (o hijo equivalente) que emita
   >64 KB a stderr y nada a stdout; el lector debe TERMINAR bajo un tope duro y NO dejar lock;
   el patron secuencial debe colgar (rojo). Debe morir por reproducir el cuelgue, no por tipo.
3. (Menor) Un negativo de comportamiento para la vejez de claims: una claim externa vencida en
   el sandbox del runner que NO difiera el arranque, y que FALLE si `$expires -gt $now` se
   neutraliza.

Puedo avalar mantener el contrato de presencia-de-string COMO EXTRA (evita reverts silenciosos
de fragmentos exactos), pero no como el UNICO guardian de los dos hallazgos cabecera.

**Gates afectados si se remedia**: `run_mailbox_retry_cases.py` (con los negativos 1-3 de
arriba) + `validate_collaboration_state.py` (exit 0) + `scan_encoding.py` (exit 0) +
`scan_domain_neutrality.py` (exit 0) + drift 0, y **re-juicio mio sobre el commit de
remediacion ANTES del commit de cierre**.

**Bucle de arreglo declarado**: remediacion test-only por Codex-maker; re-juicio por mi
(Analista-checker) sobre el commit de remediacion antes de cualquier flip a done; **maximo 1
iteracion** (el arreglo es de banco, acotado) antes de escalar al operador humano.

**Sobre el redespliegue y el defecto vivo**: entiendo que F-0281-07/08 estan vivos y que mi GO
habilitaba el redespliegue que los cierra. Como el codigo YA lo verifique correcto por
comportamiento, la decision de redesplegar el codigo correcto EN PARALELO con anadir los dos
negativos de bucle real es una llamada de coordinacion tuya y del operador -- no un bloqueo de
correctitud de mi parte. Lo que NO puedo avalar es marcar la unidad DONE con los dos hallazgos
cabecera protegidos solo por su propia sombra: seria cerrar por tercera vez contra un control
que no mide.

-- Analista
