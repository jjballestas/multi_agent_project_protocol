# Veredicto adversarial -- TASK-0281 iteracion 3 (commit 8c70dbb)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-22 00:09 (reloj del sistema, sin convertir)
- Encargo: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0281-iter3
- **Veredicto: NO-GO / CHANGE-REQUIRED. La remediacion cierra el vector que pedi y
  introduce DOS regresiones nuevas, ambas del lado de la PARADA. NO REDESPLEGAR el
  harness con este codigo. Escalado al operador humano: el tope de 2 iteraciones ya
  estaba agotado en iter2 y esta es la tercera.**

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado | `8c70dbbceb9e453cfa51aefee1debd831502872a` ("fix(TASK-0281): decode git residue paths as UTF-8") |
| Autor / fecha | Codex, 2026-07-21 23:22:14 +0200 |
| Es ancestro de origin/main | si (`git merge-base --is-ancestor` -> 0) |
| Commits posteriores sobre el codigo juzgado | **ninguno** (`git log 8c70dbb..origin/main -- scripts/harness/ examples/mailbox_retry_cases/` -> vacio) |
| HEAD del protocolo al emitir | `fa98595` |
| Commit padre (contraste de regresion) | `7b708f8` |
| Clones limpios | `D:/ccv0281c` (8c70dbb), `D:/ccv0281p` (7b708f8), `D:/ccv0281m` y `D:/ccv0281f` (mutantes) |
| Alcance | solo este hub. **Sin producto en alcance.** |
| Ventana | `CLAIMS.json` sin claims activas al emitir; `mailbox/open/` con un solo mensaje, el encargo |

## 2. Reproduccion (por exit code, en clon limpio sobre 8c70dbb)

```
python scripts/validate_collaboration_state.py            -> exit 0  ("OK: collaboration state is valid.")
python scripts/scan_encoding.py                           -> exit 0  ("OK: encoding scan is clean.")
python scripts/scan_domain_neutrality.py                  -> exit 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py -> exit 0  ("mailbox retry cases: PASS")
```

Los cuatro gates estan VERDES sobre `8c70dbb`. Nada de lo que sigue los contradice: dos de los
tres hallazgos son estados que **ningun gate de esta suite ejercita**.

Banco propio, sin confiar en nombres de test ni en el texto del handoff:

- **P0**: `Get-GitStatusPorcelainUtf8` + `Get-StagedResidueState` extraidas verbatim del clon
  limpio, ejecutadas en sandboxes git reales, con el probe **fuera** del arbol evaluado.
- **P1**: regresion SOLO del decodificador (UTF8 estricto -> cp850), fail-safe intacto.
- **P2**: regresion SOLO del fail-safe (`no resuelve -> live` sustituido por `continue`),
  decodificador intacto.
- **Runner COMPLETO** en sandbox git real con agente falso, replicando el fixture de
  `run_unstaged_residue_case`, y el MISMO experimento contra el commit padre `7b708f8`.
- Mutantes aplicados al fichero real del runner en clones separados, corriendo la suite entera.

## 3. Lo que SI quedo cerrado (y esta bien hecho)

### 3.1 F-0281-05, mitad de decodificacion: **CERRADO, y esta vez de forma falsable**

| # | Vector | Esperado | Obtenido | Veredicto |
|---|---|---|---|---|
| V1 | no rastreado fresco, ASCII (control positivo) | `live` | `live` | PASS |
| V2 | no rastreado fresco con **ESPACIO** | `live` | `live` | PASS (conservado) |
| V3 | no rastreado fresco con **byte NO-ASCII** | `live` | `live` | PASS |
| **V5** | **no rastreado RANCIO con byte NO-ASCII** | `aborted` | `aborted` | **PASS -- prueba no vacua** |
| V4 | no rastreado RANCIO, ASCII (control negativo) | `aborted` | `aborted` | PASS |
| V15 | rastreado modificado, rancio | `aborted` | `aborted` | PASS |
| V14 | directorio no rastreado rancio (`--untracked-files=all`) | `aborted` | `aborted` | PASS |
| V8 | **renombrado en index** (dos campos NUL, `$index++`) | `aborted` | `aborted` | PASS |

**V5 es la prueba que la suite no tiene**: un fichero no-ASCII **rancio** solo puede salir
`aborted` si la ruta se resolvio de verdad. Con la regresion del decodificador (P1) ese mismo
arbol da `live` (V5b). Es decir: el decodificador funciona, y yo puedo demostrarlo. La suite
permanente no (seccion 5).

### 3.2 F-0281-06, mitad de contaminacion: **CERRADO**

El probe ya no se escribe dentro del sandbox (`tempfile.mkdtemp`), asi que el test dejo de medir
su propia sombra. La vacuidad por auto-contaminacion que documente en E1/E6 de la iteracion 2
esta muerta. Lo que queda abierto es otra cosa, y es la seccion 5.

### 3.3 Lo verde anterior se conserva

Espacio (V2), renombrado (V8), y el comportamiento del defer recuperable siguen intactos; en el
runner completo, arbol limpio -> `EXEC_START=1` (C0) y residuo no rastreado con `AbortedResidueMinutes 0`
-> clasificado `aborted` y ejecuta (C1).

## 4. F-0281-07 (BLOQUEANTE, REGRESION NUEVA) -- un BORRADO deja el pre-gate en `live` PARA SIEMPRE

La regla nueva es `if (-not (Test-Path -LiteralPath $full)) { return "live" }`. Una ruta
**borrada** es, por definicion, una ruta que git reporta y que no existe en disco. Y una ruta que
no existe **no tiene mtime**, asi que **nunca puede envejecer**. El unico camino de salida del
`live` es el envejecimiento. No hay salida.

Funcion extraida (P0), sandboxes git reales:

| # | Vector | Esperado | Obtenido | Veredicto |
|---|---|---|---|---|
| V6 | borrado no indexado de un fichero rastreado | debe poder envejecer | `live` | **SLIP** |
| V7 | borrado indexado (`git rm`) | debe poder envejecer | `live` | **SLIP** |
| V12 | el mismo borrado, sondeado dos veces (t0 y t+2s) | `aborted` en algun momento | `live` / `live` | **SLIP** |
| V13 | borrado + hermano no rastreado RANCIO (arbol solo rancio) | `aborted` | `live` | **SLIP** |

Runner COMPLETO, fixture equivalente al de `run_unstaged_residue_case`, con
**`-AbortedResidueMinutes 0`** (el ajuste MAS permisivo que existe: hace rancio todo residuo al
instante):

| Escenario | EXEC_START | RETRY_DEFER | reason | attempts | defers | exhausted | mensaje consumido |
|---|---|---|---|---|---|---|---|
| C0 arbol limpio (control positivo) | **1** | 0 | -- | -- | -- | -- | si |
| C1 no rastreado, aging=0 (control) | **1** | 0 | `staged_residue_aborted` | -- | -- | -- | si |
| **V-DEL borrado no indexado** | **0** | 5 | `worktree_residue_live` | **0** | 5 | **false** | **no** |
| **V-DEL2 borrado indexado (`git rm`)** | **0** | 5 | `worktree_residue_live` | **0** | 5 | **false** | **no** |

```
2026-07-22T00:02:26 RETRY_EXHAUSTED defers=3 attempts=0 signal=watchdog outcome=deferred reason=worktree_residue_live message=MSG-retry.md
2026-07-22T00:02:27 RETRY_EXHAUSTED defers=4 attempts=0 signal=watchdog outcome=deferred reason=worktree_residue_live message=MSG-retry.md
```

**Contraste contra el commit padre `7b708f8`, mismo script, mismo fixture:**

| Escenario | 7b708f8 | 8c70dbb |
|---|---|---|
| V-DEL borrado no indexado | `EXEC_START=1`, `staged_residue_aborted`, mensaje consumido | `EXEC_START=0`, defer infinito |
| V-DEL2 borrado indexado | `EXEC_START=1`, `staged_residue_aborted`, mensaje consumido | `EXEC_START=0`, defer infinito |

La regresion es **de esta iteracion**, no preexistente.

Por que importa y no es un caso de laboratorio: un borrado es una forma **ordinaria** de residuo
de un exec abortado. El propio fixture de la suite lo produce (el agente falso mueve
`MSG-gov.md` de `open/` a `archived/`, que en git es un borrado mas un anadido). Archivar
mailbox, podar estado, mover un handoff o renombrar a mano dejan exactamente esa forma. Si el
exec muere a mitad, el `D` se queda. A partir de ahi el runner **no vuelve a ejecutar nunca**:
`attempts=0`, `exhausted=false`, el mensaje sigue elegible, cada ronda cuesta cero invocaciones
y no avanza. La cola queda parada hasta que un humano restaure el fichero.

Es **literalmente** el reves que me pediste vigilar: cambiamos el consumo indebido de la
iteracion 2 por **una parada**. Es ruidosa (el watchdog dispara cada ronda), no silenciosa, y ese
es el unico consuelo.

## 5. F-0281-06 (SIGUE ABIERTO en su mitad util) -- el control permanente no puede falsar el decodificador

Aplique cada mitad del arreglo por separado al fichero REAL del runner, en clones limpios
separados, y corri la **suite entera**:

| Mutante aplicado al runner real | Suite `run_mailbox_retry_cases.py` | Deberia |
|---|---|---|
| P2: solo el fail-safe revertido (`no resuelve -> continue`) | **exit 1** (`fail-safe unresolved-path rule did not contain the decoding mutant`) | rojo -- **OK** |
| **P1: TODO el decodificador UTF-8 revertido a cp850** | **exit 0, PASS** | rojo -- **SLIP** |

Se puede **borrar entero el arreglo que da titulo al commit** y la suite sigue verde. La razon es
estructural: la asercion no-ASCII de `run_nul_residue_path_cases` es
`assert output == "live"` sobre un fichero **fresco**, y `live` es tambien lo que devuelve el
fail-safe cuando la ruta no resuelve. Los dos mundos dan la misma respuesta, asi que la asercion
no los distingue. El mutante combinado que el maker anadio prueba que la **conjuncion** es
necesaria; no prueba que el decodificador sea correcto.

Y no es academico: con el decodificador roto y el fail-safe puesto, un residuo no-ASCII **rancio**
sale `live` (V5b medido) y ya no envejece nunca. O sea, la regresion que ningun test detecta
desemboca en **la misma parada permanente** de la seccion 4.

Lo que falta es una sola linea de banco: el caso **rancio** (V5). Con un fichero no-ASCII
envejecido, `aborted` solo es alcanzable si la ruta se resolvio; el fail-safe no puede fingirlo.

## 6. F-0281-08 (BLOQUEANTE, REGRESION NUEVA) -- `Get-GitStatusPorcelainUtf8` se bloquea si git escribe a stderr

```powershell
$raw = $process.StandardOutput.ReadToEnd()
$null = $process.StandardError.ReadToEnd()
$process.WaitForExit()
```

Las dos tuberias se drenan **en secuencia**. Si git llena el buffer de stderr antes de cerrar
stdout, git se bloquea escribiendo stderr, nunca cierra stdout, y `ReadToEnd()` sobre stdout no
retorna jamas. No hay timeout ni en la lectura ni en `WaitForExit()`.

Medido, sandbox git real con 120 directorios demasiado largos (git avisa uno por directorio):

```
stderr_bytes=32664  stdout_bytes=0  git_exit=0
lector de 8c70dbb  -> HUNG (>60 s)  = DEADLOCK
lector de 7b708f8  -> COMPLETED [none]
```

**El mismo arbol**: el lector del padre termina; el nuevo se cuelga. Regresion de esta iteracion.

Donde cae el bloqueo: `Get-StagedResidueState` se llama en la linea 786, **dentro** del `try` que
en la 785 acaba de escribir `$LockPath`. Un cuelgue ahi deja el runner colgado **con el lock
tomado**, sin linea de log, sin defer, sin senal de watchdog propia. Es la familia de atasco de
cron que ya nos costo tiempo, ahora reintroducida por el pre-gate que existe para evitar danos.

Cualquier `git status` que produzca mas stderr que el buffer de la tuberia lo dispara: avisos de
ruta demasiado larga, directorios ilegibles, permisos denegados en masa. No hace falta que git
falle: en mi medicion git salio con **exit 0**.

## 7. Respuesta directa a tu pregunta

> Con la ambiguedad clasificada como live, queda algun camino por el que un residuo real siga
> leyendose como abortado, o alguno por el que un arbol sano quede difiriendo para siempre?

**Difiriendo para siempre: SI, y es el hallazgo principal.** Cualquier borrado en el arbol
(seccion 4) fija `live` de forma permanente, con `AbortedResidueMinutes` en cero incluido, porque
la unica valvula de escape del `live` es el mtime y una ruta borrada no tiene mtime. Medido sobre
el runner completo, y ausente en el commit padre. La misma parada llega por la puerta de atras si
el decodificador regresa (seccion 5), y ningun gate lo notaria.

**Residuo real leido como abortado: no por el camino que arreglaste.** El no-ASCII fresco da
`live` (V3) y el rancio da `aborted` (V5), que es la conducta correcta. Queda un camino distinto,
preexistente y NO introducido por ti: una ruta **demasiado larga** que git no llega a enumerar. En
mi medicion git emite `warning: ... Filename too long`, sale con **exit 0** y no reporta nada, asi
que `Get-StagedResidueState` devuelve `none` y el runner arranca sobre un residuo que existe en
disco. El lector nuevo ademas **descarta stderr**, asi que el aviso no queda ni en el log. El
padre se comporta igual, por eso es residuo (R6) y no bloqueante.

En corto: la ambiguedad ya cae del lado seguro, pero el lado seguro se volvio **absorbente**. Una
puerta que solo se abre con el tiempo, aplicada a estados que no envejecen, es una puerta cerrada.

## 8. Tabla de veredicto por vector

| Vector del encargo | Medicion | Veredicto |
|---|---|---|
| Decodificacion: byte no-ASCII | V3 `live` fresco, V5 `aborted` rancio | **PASS** |
| Decodificacion: mezcla de codificaciones | V10 nombre con sustituto no emparejado -> `live`, sin lanzar | PASS (no observe excepcion; ver R7) |
| Decodificacion: ruta larga | V9 git no la enumera -> `none` | SLIP preexistente -> **R6** |
| Ambiguedad: ruta que desaparece entre enumeracion y comprobacion | `live` por construccion | PASS en direccion, **SLIP en permanencia** si el borrado persiste (F-0281-07) |
| Ambiguedad: enlace roto | no reproducible sin privilegio en esta maquina | NO PROBADO; cae en la familia de F-0281-07 si es permanente |
| Ambiguedad: permiso denegado | mismo camino `Test-Path` falso | NO PROBADO; misma familia |
| Ambiguedad: BORRADO (no estaba en el encargo) | V6/V7/V12/V13 + runner completo | **SLIP -- F-0281-07, bloqueante** |
| Arbol sano difiriendo para siempre | V-DEL / V-DEL2, `EXEC_START=0`, `exhausted=false` | **SLIP -- confirmado** |
| Probe fuera de su sandbox | `tempfile.mkdtemp` | **PASS** |
| Poder falsador real del probe | suite verde con el decodificador entero revertido | **SLIP -- F-0281-06 abierto** |
| Conservacion de lo verde anterior | V2, V8, V14, V15, C0, C1 | **PASS** |

## 9. Residuos declarados (NO bloqueantes)

- **R1 a R5**: siguen tal cual los declare en la iteracion 2 (evidencia propia historica
  re-anadida; compactacion mas corta accept-less; rama `unknown` practicamente muerta;
  `Get-WorktreeDiskProof` y la limpieza de no rastreados; `processable_messages=0` tras
  agotamiento legitimo). R4 mejora: `Get-WorktreeDiskProof` comparte ahora el lector UTF-8, asi
  que la mitad de mal-decodificado de R4 queda cubierta.
- **R6 (nuevo)** -- ruta demasiado larga sin `core.longpaths`: git avisa por stderr, sale 0 y no
  la enumera; el pre-gate devuelve `none` y arranca. El lector nuevo descarta stderr, asi que ni
  siquiera queda rastro. Preexistente (el padre igual), pero ahora es el unico camino conocido de
  "residuo real que no se ve".
- **R7 (nuevo)** -- `UTF8Encoding($false, $true)` lanza ante bytes invalidos; el `catch` devuelve
  `ok=false` y el pre-gate `unknown` -> `residue_probe_failed`, que es un defer con
  `exhausted=false`. Si la causa fuese permanente, seria la misma parada de F-0281-07 por otra
  puerta. No consegui provocar la excepcion (V10 no lanzo), asi que lo declaro plausible y no
  medido.

## 10. Recomendacion de cierre

**NO-GO / CHANGE-REQUIRED**, y **NO REDESPLEGAR** el harness con `8c70dbb`. El handoff dice que
los harnesses vivos de Codex y Analista no se redesplegaron: bien, eso mantiene F-0281-07 y
F-0281-08 fuera de produccion. Redesplegar ahora cambiaria un fail-open acotado por un cuelgue con
lock tomado y una cola que se para ante cualquier borrado.

Que quede claro el balance, porque el trabajo tiene merito: **el vector que pedi esta cerrado de
verdad** -- el decodificador funciona y lo demuestro con el caso rancio que la suite no tiene -- y
**la contaminacion del probe esta muerta**. El problema es que la regla de ambiguedad se escribio
como absorbente y el arreglo se cubrio con un control que no lo prueba.

Lo que un arreglo tiene que **sobrevivir** (no propongo implementacion; soy checker):

1. Un borrado en el arbol (indexado y no indexado) debe poder salir de `live` sin intervencion
   humana. Con un negativo que falle si la regla vuelve a ser absorbente: arbol cuyo unico residuo
   sea un borrado, con `AbortedResidueMinutes 0`, tiene que terminar en `EXEC_START=1`.
2. La lectura de `git status` no puede bloquearse cuando git escribe a stderr. Reproducible con el
   sandbox de rutas largas de la seccion 6 (32 KB de stderr, stdout vacio, git exit 0), con un
   tope de tiempo duro para que un fallo sea rojo y no un cuelgue.
3. El control permanente debe volverse rojo cuando **solo** se revierte el decodificador. El caso
   rancio no-ASCII (V5) basta.
4. Conservar todo lo verde: V2 espacio, V3/V5 no-ASCII fresco y rancio, V8 renombrado, V14, V15,
   C0 y C1, mas F2 y F4 de la iteracion 2.

**Bucle de arreglo.** El tope de dos iteraciones se agoto en la iteracion 2; esta es la tercera y
la abrio el operador. **Vuelvo a escalar**, ahora con un dato nuevo que deberia pesar en su
decision: dos iteraciones seguidas de este pre-gate han introducido un fallo nuevo cada una
(iter2 fail-open silencioso, iter3 dos paradas), y la suite quedo verde en las dos. Eso ya no es
un vector suelto: es que **la unidad se esta cerrando contra un control que no la mide**. Mi
lectura para el operador: el arreglo tecnico sigue siendo estrecho (una regla de tres lineas y un
drenaje de dos tuberias), pero el metodo de cierre necesita el negativo antes que el positivo. Si
el operador prefiere no gastar una cuarta iteracion, la unica forma que puedo avalar es que
F-0281-06, F-0281-07 y F-0281-08 salgan **por escrito con acceptance propio** hacia TASK-0283 o
una unidad nueva, con el harness **sin redesplegar** hasta entonces -- nunca como residuo suelto.

Gates afectados si se remedia: `run_mailbox_retry_cases.py` (con los tres negativos de arriba) +
`validate_collaboration_state.py` + `scan_encoding.py` + `scan_domain_neutrality.py` + drift 0, y
**re-juicio mio sobre el commit de remediacion ANTES del commit de cierre**.

-- Analista
