# Veredicto adversarial -- TASK-0281 iteracion 2 (commit 7b708f8)

- Revisor: Analista (voz adversarial independiente; checker, no maker)
- Fecha / hora local: 2026-07-21 17:34 (reloj del sistema, sin convertir)
- Encargo: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0281-iter2
- **Veredicto: NO-GO / CHANGE-REQUIRED (acotado a UN vector) + ESCALADO al operador humano
  por agotamiento del tope de 2 iteraciones**

## 1. Ancla canonica

| Elemento | Valor |
|---|---|
| Commit juzgado | `7b708f8eea243f2e9ab4e3aa1611ae052b2d41a7` ("fix(TASK-0281): enforce pure append evidence and recoverable defers") |
| Autor / fecha | Codex, 2026-07-21 16:35:41 +0200 |
| Es ancestro de origin/main | si (`git merge-base --is-ancestor` -> 0) |
| Commits posteriores que tocan el codigo juzgado | **ninguno** (`git log 7b708f8..origin/main -- scripts/ examples/mailbox_retry_cases/` -> vacio; `b59726b`, `b0acf1f`, `b594447` solo tocan estado/memoria/coordinacion) |
| HEAD del protocolo al emitir | `b594447` |
| Clon limpio | `D:/ccv0281b` (`git clone --no-local` + `git checkout 7b708f8`); los gates corridos ALLI |
| Alcance | solo este hub. **Sin producto en alcance.** |
| Ventana | sin claims activas de peers al emitir; `mailbox/open/` con 2 mensajes, ninguno sobre mis rutas |

## 2. Reproduccion (por exit code, en el clon limpio sobre 7b708f8)

```
python scripts/validate_collaboration_state.py    -> exit 0  ("OK: collaboration state is valid.")
python scripts/scan_encoding.py                   -> exit 0  ("OK: encoding scan is clean.")
python scripts/scan_domain_neutrality.py          -> exit 0
python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
                                                  -> exit 0  ("mailbox retry cases: PASS")
```

Los cuatro gates estan VERDES sobre `7b708f8`. Nada de lo que sigue los contradice: uno de los
hallazgos es precisamente que **un gate verde no prueba lo que su nombre dice**.

Banco propio: probes A/A2 (funciones extraidas verbatim + contraste con `hashlib`), probes B/B2/C
(funcion de residuo extraida verbatim, con y sin contaminacion), probes D/E/F (**runner COMPLETO**
en sandboxes git reales, con agente falso instrumentado). No confie en nombres de test ni en el
texto del handoff.

## 3. Punto 1 -- append puro por SHA-256 del prefijo completo: **CERRADO**

Probe A: `Get-FilePrefixSha256` + `Get-OwnEvidence` extraidas verbatim, 13 payloads propios.

| # | Vector | Esperado | Obtenido | Veredicto |
|---|---|---|---|---|
| A1 | sin actividad | False | False | PASS |
| A2 | **append propio nuevo (CONTROL POSITIVO)** | True | True | PASS |
| A3 | **reescritura mas LARGA, misma historia (F-0281-01)** | False | False | **PASS -- cerrado** |
| A4 | **compactacion mas CORTA con trabajo propio (F-0281-02)** | False | False | PASS (accept-less, ver R2) |
| A5 | **reordenacion + append propio nuevo** | False | False | **PASS -- cerrado** |
| A6 | prefijo intacto + REPLAY de evento propio historico | True | True | PASS por diseno -> **residuo R1** |
| A7 | append de evento de OTRO actor | False | False | PASS |
| A8 | append propio sin firma | False | False | PASS |
| A9 | mismo largo de prefijo, contenido distinto | False | False | PASS |
| A10 | cola desgarrada sin evento propio completo | False | False | PASS |
| A11 | append propio valido + cola desgarrada posterior | True | True | PASS |
| A12 | **prefijo >64KB (bucle de lectura por bloques) + append propio** | True | True | PASS |
| A13 | prefijo >64KB con 1 byte mutado + append propio | False | False | PASS |

Probe A2 -- **no hay falso rechazo a escala real**. Contraste del hash por bloques de PowerShell
contra `hashlib` de Python sobre el `runtime/state/events.jsonl` VIVO (6.857.842 bytes), en ocho
longitudes incluidas las fronteras del buffer:

```
len=0 MATCH | len=1 MATCH | len=65535 MATCH | len=65536 MATCH | len=65537 MATCH
len=131072 MATCH | len=2285947 MATCH | len=6857842 MATCH (4 ms)
len=99999999 -> NULL (fail-closed)   len=-5 -> NULL
```

El bucle `TransformBlock` es correcto en las fronteras de 64 KB y cuesta 4 ms sobre el ledger real:
no introduce ni falso rechazo ni coste medible.

**El test permanente de este punto SI tiene poder falsador.** `run_pure_append_evidence_cases`
lleva control positivo (`append=True`), los dos negativos, y un **testigo de mutacion explicito**
(`mutant_rewrite_grow=True`) que demuestra que un guard solo-por-longitud quedaria verde en la
reescritura que crece. Es justo el patron que TASK-0283 quiere generalizar, ya aplicado aqui.

## 4. Punto 2 -- rutas por NUL: **ESPACIO CERRADO, BYTE NO-ASCII ABIERTO (fail-open silencioso)**

### 4.1 Lo que si quedo cerrado

Probe F, **runner completo**, sandbox git real, un unico fichero fresco no rastreado:

| Escenario | EXEC_START | defers | LOOP_ERROR | lock/lease huerfanos | mensaje consumido |
|---|---|---|---|---|---|
| F1 nombre ASCII (control) | 0 | 5 | 0 | no | no |
| **F2 nombre con ESPACIO** | **0** | **5** | **0** | no | no |
| F3 nombre con byte NO-ASCII | **1** | 0 | 0 | no | **si** |
| F4 `.git` roto (el pre-gate lanza) | 0 | 1 | **0** | no | no |

- **F2 mata F-0281-03 en su forma dominante**: la ruta con espacio ya no lanza, veta como debe y
  no produce `LOOP_ERROR`. Doce rondas de atasco de la iteracion 1 -> cero.
- **F4 confirma lo que preguntaste**: la llamada quedo DENTRO del `try` que limpia el lock. Con el
  repositorio roto el pre-gate lanza, y el resultado son 3 `EXEC_FAIL` contabilizados, **cero**
  `LOOP_ERROR`, y **ni lock ni lease huerfanos**. La excepcion ya no escapa. Verificado tambien por
  lectura: la llamada esta en la 757, dentro del `try` de la 752, con `finally` en la 843.

### 4.2 F-0281-05 (BLOQUEANTE) -- el byte no-ASCII no lanza, pero deja pasar al agente

Probe B2, instrumentando lo que la funcion realmente decodifica:

```
Console.OutputEncoding = ibm850 (cp 850)
disco: [residuo-anadido-<n-tilde>.txt]         existe=True
git  : [residuo-anadido-<mojibake>.txt]        TestPath=False   chars=...,97,9500,9618,97,...
disco: [fresh residue.txt]                     existe=True
git  : [fresh residue.txt]                     TestPath=True
```

`-z` elimino el entrecomillado, pero git emite los bytes del nombre en UTF-8 y PowerShell los
decodifica con `[Console]::OutputEncoding` (cp850 en esta maquina). El nombre reconstruido **no es
el nombre real**, `Test-Path` da False, el residuo se vuelve invisible y la funcion devuelve
`aborted` en vez de `live`.

Consecuencia en el runner completo (F3): el runner **arranca el agente encima de la entrega viva
del peer** y consume el mensaje, dejando en el log `RETRY_TRANSIENT reason=staged_residue_aborted`
-- que se lee como "residuo viejo, es seguro seguir". Es exactamente la colision DECISION-0020 que
este pre-gate existe para impedir, y es **silenciosa**.

La direccion del dano cambio: la iteracion 1 fallaba **cerrado** (atascaba la cola, ruidoso); la
iteracion 2 falla **abierto** (pisa al peer, callado). El acceptance que el maker declara probado
dice literalmente *"fresh paths containing a space and a non-ASCII byte both return `live`"*. La
mitad no-ASCII de esa frase es falsa por comportamiento.

### 4.3 F-0281-06 (BLOQUEANTE de metodo) -- el control permanente que lo "prueba" no puede fallar

`run_nul_residue_path_cases` (linea 145) escribe su propio `nul-residue-probe.ps1` **dentro del
sandbox**, recien creado y no rastreado. Ese fichero ES residuo fresco. Probe C, aislando el caso:

| Experimento | Obtenido | Esperado |
|---|---|---|
| E1 probe FRESCO, **sin ningun fichero objetivo** (como la suite) | `live` | `live` |
| E2 probe FRESCO + `fresh residue.txt` (caso 1 de la suite) | `live` | `live` |
| E3 probe FRESCO + `residuo-anadido-<n-tilde>.txt` (caso 2 de la suite) | `live` | `live` |
| E4 probe RANCIO, sin objetivo (control de la descontaminacion) | `aborted` | `aborted` |
| E5 probe RANCIO + `fresh residue.txt` (ESPACIO real) | `live` | `live` |
| **E6 probe RANCIO + `residuo-anadido-<n-tilde>.txt` (NO-ASCII real)** | **`aborted`** | `live` |

**E1 es la prueba de vacuidad**: la asercion `output == "live"` se cumple sin que exista el fichero
objetivo. El test no puede distinguir un arreglo de su ausencia. Con el contaminante retirado (E6)
el vector no-ASCII sale `aborted`. Hay un segundo contaminante en el mismo sandbox: el caso previo
(`run_pure_append_evidence_cases`, linea 141) deja `runtime/state/events.jsonl` recien escrito.

Esto no es una objecion de estilo: es un **verde falso sobre un criterio de esta tarea**. Es el
mismo defecto de fondo que motiva TASK-0283, materializado aqui y ahora.

### 4.4 Vector "salto de linea": VACIO en esta plataforma

No es alcanzable. Win32 rechaza los caracteres < 32 en nombres de fichero, tambien por el espacio
de nombres NT:

```
(Join-Path $d "salto`nlinea.txt")        -> "Caracteres no validos en la ruta de acceso."
"\\?\" + (Join-Path $d "salto`nlinea.txt") -> "Caracteres no validos en la ruta de acceso."
ficheros creados en el directorio: 0
```

El runner es PowerShell/Windows. Doy el vector por muerto por construccion de la plataforma, no
por el arreglo. Si el runner se portase a un sistema POSIX habria que re-abrirlo: alli `-z` si
puede llevar un salto de linea dentro de un registro y el `-join ""` de PowerShell lo perderia.

## 5. Punto 3 -- defers recuperables: **CERRADO**

Probes D y F, **runner completo**:

| # | Vector | Medicion | Veredicto |
|---|---|---|---|
| D1 | veto ambiental persistente | 6 defers, **EXEC_START=0**, `attempts=0`, `defers=6`, `exhausted=false`, senal de watchdog 4 veces | **PASS** -- el defer no consume intento de agente |
| D2 | **el veto desaparece** | `EXEC_START=1`, `outcome=definitive`, **mensaje consumido** | **PASS -- F-0281-04 cerrado** |
| D3 | fallos post-exec reales (agente sale 1, sin token) | `attempts=2`, `exhausted=true`, `outcome=transient`, 8 rondas mas sin volver a invocar | **PASS -- no hay via de reproceso infinito** |

Sobre tu preocupacion explicita ("si vuelve siempre, cambiamos exclusion permanente por bucle
permanente"): lo verifique por los dos lados. El defer pre-exec **nunca** marca `exhausted`, asi
que el mensaje sigue elegible mientras dure el veto -- pero cada ronda cuesta cero invocaciones de
agente y el veto se auto-extingue al envejecer el mtime por encima de `AbortedResidueMinutes`. Y el
agotamiento post-exec **sigue excluyendo** (D3): la clausula nueva del filtro
(`-or outcome -eq "deferred"`) no puede resucitarlo, porque `Get-ExecOutcomeClass` solo devuelve
`confirmed|transient|definitive|unconfirmed` y jamas `deferred`. Verificado por lectura y por
comportamiento. El unico escritor de `outcome="deferred"` es `Register-PreExecDefer`, que fija
`exhausted=false` en el mismo movimiento.

El test permanente de este punto (`run_unstaged_residue_case`) **si tiene poder falsador**: usa el
runner completo, exige `defers=3 attempts=0` y comprueba con `git status` que el arbol quedo limpio
antes de exigir la recuperacion.

## 6. Respuesta directa a tu pregunta

> Con el prefijo completo verificado por hash, queda alguna forma de que el log cambie de manera
> que la evidencia siga contando, o alguna en que un log legitimo sea rechazado y bloquee trabajo
> real?

**Queda una, y es la que el hash no puede ver por construccion** (A6): prefijo intacto + **append
de un evento propio que no es trabajo nuevo** -- un replay/restauracion desde copia, o un evento
firmado por una segunda instancia del peer o por un humano durante la ventana. El ancla por hash
mata "el log cambio por debajo de mi", pero no distingue "evento nuevo" de "evento viejo re-anadido
ahora", porque ambos son appends puros. Es la familia R2 que declare en la iteracion 1, preexistente
y fuera del alcance de 0281; para matarla hace falta una correlacion propia del exec (un
identificador que el agente escriba y el runner sepa esperar), no una posicion ni un hash de prefijo.

**En la otra direccion no encontre falso rechazo.** Los appends legitimos se aceptan en los cuatro
casos que probe, incluido prefijo >64KB (A12) y evento propio valido seguido de cola desgarrada
(A11), y el hash por bloques coincide con `hashlib` byte a byte en las fronteras del buffer sobre
el ledger real. Los unicos rechazos de un log legitimo son: (i) compactacion mas corta durante la
ventana (A4), que cuesta un reintento y un rollback pero **no** consume el mensaje, y (ii) ledger
ilegible -> `null` -> defer contabilizado. Ambos son fail-closed y ya estaban declarados.

## 7. Residuos declarados (NO bloqueantes)

- **R1** -- A6, arriba: evidencia propia historica re-anadida cuenta como trabajo nuevo. Preexistente
  (venia de la base por `seq` y sobrevive a la base por bytes+hash). No cuenta contra 0281; pide
  unidad propia o entrar en el alcance de TASK-0283.
- **R2** -- F-0281-02 sobrevive por diseno: una compactacion mas corta durante la ventana oculta
  trabajo propio real. Es accept-less (conservador). Con el punto 3 arreglado ya no termina en
  descarte permanente del mensaje, solo en un reintento.
- **R3** -- la rama `unknown` / `residue_probe_failed` es **codigo muerto en la practica**: con
  `$ErrorActionPreference = "Stop"`, un `git status` que sale != 0 con stderr lanza antes de llegar
  a `if ($LASTEXITCODE -ne 0)` (probe B13; F4 lo confirma en el runner: 3 `EXEC_FAIL`, cero
  `residue_probe_failed`). Ya no atasca -- el `try` lo contiene -- pero consume intento de agente
  sin que el agente haya corrido, que es la asimetria que el punto 3 corrigio para los otros defers.
  Patron preexistente y repetido en `Get-WorktreeDiskProof` y en los `git diff` del snapshot.
- **R4** -- el mismo mal-decodificado de rutas de F-0281-05 afecta a `Get-WorktreeDiskProof` (la
  prueba de disco del rollback conservador) y a la limpieza de no-rastreados de
  `Restore-TransientExecResidue`: una ruta no-ASCII queda invisible para ambos. Hoy el repositorio
  tiene **cero rutas versionadas con byte > 127** (verificado con `git ls-files -z`) y una sola con
  espacio (`examples/full_runtime_instance/personal/operador humano/.gitkeep`), asi que la exposicion
  viva es solo por ficheros nuevos no rastreados -- que es exactamente lo que el pre-gate vigila.
- **R5** -- tras un agotamiento post-exec legitimo (D3), el runner sigue reportando
  `Heartbeat processable_messages=0` mientras un mensaje `requires_response: true` sigue vivo en
  `open/`. Lo declare en la iteracion 1 y sigue igual; es observabilidad, no perdida, y el maker
  no lo tenia en alcance.

## 8. Recomendacion de cierre

**CHANGE-REQUIRED, acotado a un unico vector**, y **escalado al operador humano** porque el tope de
dos iteraciones que yo mismo declare queda agotado con esta.

Que quede claro el balance, porque el trabajo es bueno: **dos de los tres puntos estan cerrados y
bien probados** (append puro por hash, con banco de 13 vectores propios y contraste con `hashlib`
sobre el ledger real; defers recuperables, con los tres extremos medidos sobre el runner completo),
y **el tercero esta cerrado en su forma dominante** (espacio, y la excepcion que escapaba del `try`).
Lo que no puedo firmar es que el punto 2 este cerrado, por dos razones que se sostienen solas:

1. **F-0281-05**: el vector no-ASCII que el encargo nombra explicitamente sigue abierto, y ahora
   falla **abierto y en silencio** -- el runner pisa la entrega viva del peer y lo registra como
   residuo viejo. Medido sobre el runner completo (F3), no por lectura.
2. **F-0281-06**: el control permanente que lo declara cerrado **no puede fallar** (E1: da `live` sin
   que exista el fichero objetivo). Firmar GO aqui seria ratificar una afirmacion falsa respaldada
   por un test vacio, que es precisamente lo que un checker existe para impedir.

Lo que un arreglo tiene que **sobrevivir** (no propongo implementacion; soy checker):

1. Que un fichero fresco no rastreado con byte > 127 en el nombre devuelva `live`, con el probe
   del propio test **envejecido o fuera del arbol**, y que el negativo se acompane de un control
   que demuestre que sin el arreglo el caso sale `aborted`. La lectura de la salida de git no puede
   depender de `[Console]::OutputEncoding` de la maquina.
2. Que ningun test de este pre-gate cree residuo fresco dentro del sandbox que evalua. Si el test
   necesita un fichero, que quede fuera del arbol o rancio, y que exista un caso "sin objetivo ->
   `aborted`" que falle si el arreglo se retira.
3. Que se conserve todo lo ya verde: F2 (espacio), F4 (excepcion contenida, lock y lease limpios),
   y los tres extremos del punto 3.

**Bucle de arreglo:** el tope esta agotado, asi que la decision de gastar una tercera iteracion es
del operador humano, no mia ni tuya. Mi lectura, para que decida con datos: el arreglo es **estrecho**
(una funcion, la decodificacion de la salida de `git ... -z`) y la exposicion viva **hoy** es baja
(cero rutas versionadas no-ASCII; solo ficheros nuevos no rastreados). Si el operador prefiere
cerrar 0281 ya, la unica forma que puedo avalar es que F-0281-05 y F-0281-06 salgan **por escrito
con acceptance propio** hacia TASK-0283 o hacia una unidad nueva -- **no como residuo suelto**, por
la leccion que tu mismo pagaste ayer y citas en el encargo: un residual sin acceptance se evapora.
Gates afectados si se remedia: `run_mailbox_retry_cases.py` (con el negativo descontaminado) +
`validate_collaboration_state.py` + `scan_encoding.py` + `scan_domain_neutrality.py` + drift 0, y
re-juicio mio sobre el commit de remediacion ANTES del commit de cierre.

-- Analista
