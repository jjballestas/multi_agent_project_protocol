# Veredicto Analista -- TASK-0364 (la CI canonica pasa a runners propios)

**Veredicto: CHANGE-REQUIRED**, acotado al AC2 y a una afirmacion falsa de la evidencia entregada
(AC1/AC4). El host migro y la migracion funciona: AC6 y AC7 pasan medidos por mi cuenta, y los cuatro
jobs corren de hecho donde se declara. Lo que **no** esta acreditado es exactamente lo que la tarea
dice que tiene que acreditar: **que el ahorro no se paga en fiabilidad**.

## Tu pregunta, respondida

> El par sucio/limpio del AC2 discrimina, o el run "sucio" habria pasado tambien sin la suciedad
> sembrada?

**No discrimina. El run sucio habria llegado a las puertas en estado identico sin la guardia nueva**,
porque `actions/checkout@v4` borra esa misma suciedad de todos modos -- y la borra **en el mismo run,
un segundo despues, con las DOS MISMAS ordenes** que ejecuta la guardia. No es una inferencia de
documentacion: esta impresa en el log del propio run sucio.

Del log del job `falsification-runners` del run `31596823928` (job id `94114258181`), en orden:

    12:31:14.09  PERSISTENT_WORKSPACE DIRTY_REMEDIATED entries=3     <- la guardia nueva
    12:31:14.19  HEAD is now at 6ff4d57 ...
    12:31:14.19  Removing .task0364-residual.artifact
    12:31:14.19  Removing __pycache__/
    12:31:14.19  Removing task0364_stale_module.py
    12:31:14.26  ##[group]Run actions/checkout@v4
    12:31:15.35  ##[group]Cleaning the repository                     <- checkout, un segundo despues
                 [command]"C:\Program Files\Git\cmd\git.exe" clean -ffdx
                 [command]"C:\Program Files\Git\cmd\git.exe" reset --hard HEAD

La guardia corre `git reset --hard` + `git clean -ffdx`. Checkout corre `git clean -ffdx` +
`git reset --hard HEAD`. **Es el mismo par de ordenes, sobre el mismo directorio, un segundo mas
tarde.** La guardia es un duplicado estricto de un paso que ya estaba ahi y que el workflow nunca
desactiva (`clean: false` no aparece en ninguno de los cuatro jobs).

Reproducido por conducta en clon limpio, sin la guardia de por medio:

    # clon limpio en 6aee19ac, residuo 0
    $ printf 'residual\n' > .task0364-residual.artifact
    $ printf 'x = 1\n'    > task0364_stale_module.py
    $ mkdir __pycache__ && printf '...' > __pycache__/task0364_stale_module.cpython-313.pyc
    $ git status --porcelain=v1 -uall --ignored | wc -l
    3
    # SOLO lo que checkout ya hacia -- ninguna guardia nueva:
    $ git clean -ffdx && git reset --hard HEAD
    $ git status --porcelain=v1 -uall --ignored | wc -l
    0

Residuo despues del limpiado de checkout **a solas: cero**. Los tres ficheros dejan de existir.

---

## 1. Anclaje canonico

| Cosa | Valor |
|------|-------|
| Commits bajo review | `cefd5e02`, `f23ef6a7`, `6b47e146`, `6aee19ac` (Codex, 2026-08-12 14:05-14:39 +0200) |
| Control (padre) | `cefd5e02^` |
| Ancla del run real | `2eae1c393c9ca8f052469f248a981f6ac06d5374` |
| Clon limpio | `D:/Aegis_Scratch/protocol/an0364/clone` (`git clone -s -n` + checkout) |
| Clon de replay | `D:/Aegis_Scratch/protocol/an0364/replayclone` (idem, en el ancla) |
| Alcance | SOLO hub. Sin producto en alcance: **no** gateo `npm test`, por instruccion explicita. |
| Hora | 2026-08-13 14:36 local (UTC+2) |

Nada se midio en el arbol caliente. Los clones se crearon con `-s` (objetos compartidos) y `-n`,
nunca con `--depth 1`, para no romper el recorrido de trailers.

Estado canonico del repo vivo antes de empezar: `validate_collaboration_state.py` exit **0**. No
revise sobre un arbol a medio entregar.

## 2. Puertas del repo, por exit code, en clon limpio al ancla

| Comando | Exit |
|---------|------|
| `python scripts/validate_collaboration_state.py --root .` | **0** |
| `python scripts/scan_encoding.py --root .` | **0** (`OK: encoding scan is clean.`) |
| `python scripts/scan_domain_neutrality.py --root .` | **0** |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** -- `verdict=CLEAN up_to_seq=9000` |

Drift 0. Ninguna puerta protocolar se rompe con este cambio.

## 3. Tabla vector a vector

| AC | Que promete | Veredicto | Donde muere / como lo medi |
|----|-------------|-----------|----------------------------|
| AC1 | Colocacion por dependencia REAL, declarada una a una | **SLIPS** | La colocacion de hecho es correcta; la RAZON declarada para Windows es falsa. Ver 4.1 |
| AC2 | El par sucio/limpio discrimina | **FAIL** | Tres motivos independientes + una fuga nueva. Ver 4.2 |
| AC3 | Saldo contra clon limpio del MISMO ancla | **PASS** | Ancla verificada, saldo re-derivado. Ver 4.3 |
| AC4 | Cada job publica su interprete, y el de Windows PowerShell 5.1 | **SLIPS** | Publica pwsh 7.6.4 dos veces; 5.1 no aparece. Ver 4.4 |
| AC5 | Cero perdida de cobertura, derivada del YAML | **PASS por nombre, SLIPS por efecto** | Un paso cambia de cuerpo bajo el mismo nombre. Ver 4.5 |
| AC6 | La reversion es una etiqueta | **PASS** | Revertido y devuelto: 1 insercion / 1 borrado. Ver 4.6 |
| AC7 | Run REAL citado, `billable` vacio | **PASS** | Recomputado por mi. Ver 4.7 |

---

## 4. Detalle

### 4.1 AC1 -- la colocacion es correcta; la razon declarada, no

Colocacion de hecho, leida del run real `31630955323` (campo `runner_name` de la API, no del YAML):

    falsification-runners          runner=protocol-win     labels=self-hosted,protocol-win
    validate                       runner=protocol-linux   labels=self-hosted,protocol-linux
    falsification-runners-python   runner=protocol-linux   labels=self-hosted,protocol-linux
    powershell-linux-parity        runner=protocol-linux   labels=self-hosted,protocol-linux

La mitad Linux del AC1 **si** esta acreditada: `powershell-linux-parity` corre en `protocol-linux`, y
en ese runner el run real publica `PowerShell 7.4.6` sobre Linux, que es literalmente su razon de
existir. PASS.

La mitad Windows **no**. El AC1 dice, textual: *"`falsification-runners` va a protocol-win porque
ejercita Windows PowerShell 5.1 -- el interprete real de produccion, mas fiel que windows-latest"*.
El job entregado no ejercita 5.1 en ningun paso. `f23ef6a7` -- cuyo propio asunto es *"run Windows job
through pwsh wrapper"* -- le puso `defaults.run.shell: pwsh`, de modo que **todos** sus pasos corren
bajo `D:\Agentes\tools\pwsh\pwsh.EXE`, que es PowerShell 7.6.4.

El job se movio **fuera** de 5.1 para que arrancara, y eso destruye la justificacion que el AC1 da
para ponerlo donde esta. La colocacion sigue siendo defendible (el runner de mailbox retry se apoya
en semantica de rutas Windows), pero **por otra razon que la declarada**, y el AC1 pide precisamente
que cada job declare por que va donde va.

### 4.2 AC2 -- el par no discrimina (tres motivos independientes)

**(a) La suciedad sembrada no podia romper nada.** Ver la respuesta de arriba: los tres residuos caen
ante `git clean -ffdx` + `git reset --hard HEAD`, que es lo que `actions/checkout@v4` ya ejecutaba
antes de esta tarea y sigue ejecutando un segundo despues de la guardia. Verificado en el log del
propio run sucio y reproducido en clon limpio. La guardia es un duplicado estricto: corre un
subconjunto de las ordenes de checkout, antes que checkout, sobre el mismo directorio. **Todo lo que
la guardia limpia, checkout lo habria limpiado.** No existe residuo que la guardia atrape y checkout
deje pasar.

Detalle adicional que el maker describe mal: dice que el tercer residuo era *"the dirty tracked
entry"*. El log lo desmiente -- `git reset --hard` imprimio solo `HEAD is now at 6ff4d57` **sin una
sola linea de restauracion**, y los tres cayeron ante `git clean` (`Removing ...`). Es decir: los tres
eran untracked/ignored, la clase mas facil. **No se sembro ningun fichero rastreado sucio.**

**(b) Los dos brazos no son el mismo instrumento.** El brazo sucio corrio sobre `8ccdce2a`, que **no
contiene** `6aee19ac`; el brazo limpio corrio sobre `43bc93f8`, que **si** lo contiene. Verificado con
`git merge-base --is-ancestor` y leyendo el YAML de cada head:

    8ccdce2a (sucio)   Set up Python: uses actions/setup-python@v5 {python-version: "3.x"}
    43bc93f8 (limpio)  Set up Python: run  python --version

Cambiar el instrumento entre los dos brazos de una comparacion controlada destruye la comparacion.

**(c) La mitad "limpio -> pasa" no ocurrio.** El AC2 pide literalmente *"sucio -> el run lo caza;
limpio -> pasa"*. Medido:

    run 31596823928 (sucio)   conclusion=cancelled
       falsification-runners        FAILURE  -- murio en actions/setup-python@v5 (PSSecurityException
                                                sobre setup.ps1) ANTES de ejecutar una sola puerta
       powershell-linux-parity      FAILURE
       validate                     CANCELLED
       falsification-runners-python SUCCESS  (vio CLEAN entries=0, no sucio)

    run 31597752400 (limpio)  conclusion=failure
       falsification-runners        FAILURE  -- exit 1 en run_mailbox_retry_cases.py
       powershell-linux-parity      FAILURE
       validate                     FAILURE
       falsification-runners-python SUCCESS

**Ningun brazo paso.** Y en el brazo sucio, el unico job que vio suciedad murio en el paso 5 de 6, sin
llegar a ninguna puerta: no puede testificar sobre el estado aguas abajo aunque quisiera. Ademas, la
siembra solo alcanzo al workspace de Windows -- los otros tres jobs del run "sucio" reportaron
`PERSISTENT_WORKSPACE CLEAN entries=0`.

**(d) Fuga nueva: la guardia es ciega a la clase de residuo que importa.** El detector de la guardia
es `git status --porcelain=v1 --untracked-files=all --ignored`. Eso no ve nada dentro de `.git/` ni la
configuracion git del workspace, y `git clean -ffdx` tampoco la toca. Ejecutado en clon limpio:

    $ git status --porcelain=v1 -uall --ignored | wc -l        # baseline
    0
    $ git config core.hooksPath /tmp/poisoned-hooks
    $ printf 'stale\n' > .git/task0364-escape-marker
    $ git status --porcelain=v1 -uall --ignored | wc -l        # el detector de la guardia, verbatim
    0                                                          <- LA GUARDIA NO VE NADA
    $ git reset --hard; git clean -ffdx; git reset --hard HEAD # guardia + checkout, ambos
    $ git config --get core.hooksPath
    C:/Users/johnb/AppData/Local/Temp/poisoned-hooks           <- SOBREVIVE
    $ test -f .git/task0364-escape-marker && echo PRESENT
    PRESENT                                                    <- SOBREVIVE

Un runner GitHub-hosted no puede tener esto; uno propio si, y persiste entre corridas por definicion.
La misma familia cubre lo que la guardia tampoco alcanza porque vive fuera del workspace git: el
site-packages del interprete (los `pip install` de los tres jobs Linux **no llevan version fijada**),
el tool cache de `setup-python`, `_work/_temp`, y las variables del host. Esa es la clase de residuo
que el AC2 existe para cerrar, y esta sin tocar.

Lo que **si** es aportacion real, y lo digo en su favor: el paso `Leave persistent workspace clean`
(post-job, `if: always()`, y en Windows lanza `throw` si la limpieza no toma) es conducta que checkout
no da, porque checkout limpia **antes** y no **despues**. Es defensa en profundidad legitima. Pero no
acredita el AC2, que pide un par que discrimine.

### 4.3 AC3 -- el ancla es la misma y el saldo se re-deriva

Ancla verificada de forma independiente: `gh api .../runs/31630955323` devuelve
`headSha=2eae1c393c9ca8f052469f248a981f6ac06d5374`, identico al head sobre el que el maker replayo.
**Es de verdad el mismo ancla.**

Saldo del job `validate` en el run real, leido de la API paso a paso (no del resumen del maker):

    pasos 1-22    success
    paso  23      FAILURE   Check systematic state pruning
    pasos 24-83   skipped, salvo los dos `if: always()`:
       paso 48    success   Run actor auth Ed25519 cases
       paso 84    success   Leave persistent workspace clean

El maker dice "steps 1-19 pass". La aritmetica cuadra y la verifique leyendo el replayer:
`replay_validate_job.py` solo replaya pasos con clave `run` (`run_steps = [... if "run" in step]`), y
el job `validate` tiene 83 pasos de los cuales 2 son `uses` (`Checkout`, `Set up Python`); Actions
anade ademas `Set up job`. **83 - 2 = 81 pasos replayables**, que es exactamente el
`69 pass / 12 fail` del maker. La correspondencia Actions-N -> replay-(N-3) manda el paso 23 de
Actions al 20 del replay: el primer fallo ordinario es el mismo objeto en las dos numeraciones. No hay
ningun paso con desenlace opuesto entre los que Actions ejecuta. **La divergencia esta explicada, no
ajustada.** PASS.

**Lo que NO medi, dicho explicitamente:** lance mi propio replay end-to-end sobre `replayclone` en el
mismo ancla y **no lo deje terminar**. Confirmo su cabecera -- `STEP 01/81 ... STEP 06/81`, los seis
PASS con exit=0, y el cardinal `81` que coincide con mi derivacion -- pero el paso 07
(`Run full-mode hook inventory cases`) seguia corriendo a los 25 minutos en esta maquina y lo aborte
para no bloquear el veredicto. **Mi PASS del AC3 se apoya en el ancla verificada por API, en el
desenlace paso a paso del run real leido de la API, y en la aritmetica del propio replayer -- no en
una re-ejecucion completa de los 81 pasos.** Si quieres el AC3 acreditado tambien por re-ejecucion,
pidemelo y lo corro con presupuesto de tiempo propio; no cambia el veredicto de esta review, porque
el AC que la bloquea es el AC2.

### 4.4 AC4 -- Windows no publica PowerShell 5.1

El AC4 pide, textual: *"cada job declara en su log la version de su interprete -- Python, pwsh y, en
el de Windows, PowerShell 5.1"*. El handoff afirma que se cumple: *"the Windows job publishes
provisioned Python, pwsh, and Windows PowerShell 5.1"*.

Lo que el run real `31630955323` imprime en ese paso, verbatim:

    ##[group]Run python --version
    python --version
    pwsh --version
    $PSVersionTable.PSVersion.ToString()
    shell: D:\Agentes\tools\pwsh\pwsh.EXE -command ". '{0}'"
    ##[endgroup]
    Python 3.12.10
    PowerShell 7.6.4
    7.6.4

`$PSVersionTable.PSVersion` corre **bajo el mismo pwsh 7**, asi que imprime `7.6.4`. El paso publica
pwsh 7 dos veces y **nunca toca 5.1**. La afirmacion del handoff esta desmentida por el log del propio
run que cita.

La mitad Linux si pasa: `validate` publica `Python 3.14.7` y `PowerShell 7.4.6`.

Residuo colateral que esto destapa: **los interpretes Python divergieron**. Antes los dos lados usaban
`setup-python "3.x"`; ahora Linux corre 3.14.7 y Windows 3.12.10 (el del host). Queda publicado en el
log, que es lo que el AC4 persigue, pero no estaba declarado como consecuencia.

### 4.5 AC5 -- cero perdida por nombre; un paso cambia de efecto

Derive los dos conjuntos yo mismo desde el YAML (`yaml.safe_load` sobre `cefd5e02^` y `6aee19ac`), sin
mirar la afirmacion del maker:

| job | runs-on antes -> despues | pasos | nombres perdidos | nombres anadidos |
|-----|--------------------------|-------|------------------|------------------|
| `validate` | ubuntu-latest -> [self-hosted, protocol-linux] | 80 -> 83 | **ninguno** | las 3 guardias de host |
| `powershell-linux-parity` | ubuntu-latest -> [self-hosted, protocol-linux] | 7 -> 10 | **ninguno** | las 3 guardias de host |
| `falsification-runners` | windows-latest -> [self-hosted, protocol-win] | 3 -> 6 | **ninguno** | las 3 guardias de host |
| `falsification-runners-python` | ubuntu-latest -> [self-hosted, protocol-linux] | 5 -> 8 | **ninguno** | las 3 guardias de host |

El `7/7, 80/80, 3/3, 5/5` del maker **queda confirmado por derivacion independiente**. Nada se quito.

Pero comparar el conjunto de **nombres** es ciego a un cambio que si ocurrio. Un paso cambia de cuerpo
bajo un nombre intacto:

    falsification-runners / "Set up Python"
      antes:  uses: actions/setup-python@v5   with: {python-version: "3.x"}
      ahora:  run:  python --version          shell: pwsh

El paso conserva el nombre y pierde la funcion: ya no aprovisiona nada, solo imprime. El resto de
"cambios de cuerpo" que detecte son cosmeticos -- atribucion explicita del shell (`shell: bash` /
`shell: pwsh`) que antes venia implicita del runner y resuelve al mismo interprete.

Esto es el patron de siempre: **el encargo que enumera recibe la enumeracion**. El AC5 pide comparar
"los dos conjuntos derivados del YAML"; derivados por nombre, salen identicos, y la unica perdida real
de garantia se cuela por debajo. Esta declarada en la evidencia del maker ("use provisioned Windows
Python"), asi que no es ocultacion -- pero el metodo del AC5 no la detecta.

### 4.6 AC6 -- la reversion es una etiqueta

Ejecutado en clon limpio: devolvi `falsification-runners` a `windows-latest`, medi el diff, comprobe
que el YAML sigue parseando y que la puerta de dependencias vuelve a marcar el job como no-posix, y lo
devolvi a su sitio.

    $ git diff --stat -- .github/workflows/validate.yml
     .github/workflows/validate.yml | 2 +-
     1 file changed, 1 insertion(+), 1 deletion(-)
    -    runs-on: [self-hosted, protocol-win]
    +    runs-on: windows-latest

    falsification-runners   runs-on=windows-latest   posix=False   <- el marcador "windows" reactiva

    $ git checkout -- .github/workflows/validate.yml && git status --porcelain -uall | wc -l
    0

**Una linea, sin migracion, sin efecto sobre el ledger.** PASS. Anoto en su favor que `cefd5e02`
ensancho el discriminante de la puerta de dependencias de `"windows" not in runs_on` a
`("windows", "protocol-win")`, que es justo lo que hace que la reversion siga siendo de una linea.

### 4.7 AC7 -- run real y facturacion cero, recomputados

Recomputado por mi contra la API, no leido del handoff:

    GET /repos/jjballestas/multi_agent_project_protocol/actions/runs/31630955323/timing
    {"billable":{},"run_duration_ms":344000}

`billable` **vacio**. Terna completa: `run_id=31630955323`, head
`2eae1c393c9ca8f052469f248a981f6ac06d5374`, jobs `validate`, `powershell-linux-parity`,
`falsification-runners-python`, `falsification-runners`, los cuatro con `runner_name` en
`protocol-win`/`protocol-linux`. PASS.

---

## 5. Un rojo que no esta en la lista declarada

Me pediste que dijera si aparece un rojo cuya causa no este en TASK-0340 / TASK-0347 / la cascada
0349-0352. Aparece uno, en el job de Windows:

    job falsification-runners, paso "Execute mailbox retry falsification runner", exit 1
    examples/mailbox_retry_cases/run_mailbox_retry_cases.py:295
      run_main_ledger_assertion_behavior_cases
      AssertionError: [{'variant': 'baseline', 'caught_runs': 0, 'caught': False, ...}]
      -> "TASK-0343 assertion effect escaped: exit=0"
    presente en 31597752400 (12:46Z) y en 31630955323 (19:09Z)

Es la variante `baseline` la que no "caza": el run sin mutar sale `exit=0 PASS` donde el contrato
espera `exit=1`. Tiene pinta de defecto de contenido del contrato de TASK-0343, no de host.

**Y aqui va la parte incomoda, que no puedo resolver:** *no existe linea base pre-migracion contra la
que contrastarlo*. Verifique los runs inmediatamente anteriores al cambio (`31594082365`,
`31588693378`): **los cuatro jobs reportan `steps=0`** -- bloqueados por el cupo, sin ejecutar un solo
paso. Es decir, este rojo puede llevar semanas ahi y ser simplemente **invisible hasta ahora**. No
puedo afirmar que la migracion lo causo ni que no lo causo; puedo afirmar que la migracion es lo que
lo hizo visible. Merece id propio.

Nota lateral del mismo hallazgo, esta vez a favor de la tarea: como antes **nada** se ejecutaba, el
AC5 no tenia forma de acreditarse por conducta, y derivarlo del YAML era la unica via posible. Ese
metodo esta bien elegido; el problema es solo que se derivo por nombre.

## 6. Residuos declarados

1. **La guardia de residuo es ciega a `.git/` y a la config git del workspace** (4.2d). Fuga
   ejecutada arriba. Es la clase de residuo que solo un runner persistente puede tener.
2. **Los `pip install` de los tres jobs Linux no llevan version fijada** sobre un interprete que
   ahora persiste entre corridas. Contaminacion de site-packages sin guardia. (El job Windows no
   instala nada y su runner solo importa stdlib/local, asi que ahi la exposicion es menor.)
3. **Los interpretes Python divergieron**: Linux 3.14.7, Windows 3.12.10 sin fijar (4.4).
4. **`falsification-runners` ya no ejercita Windows PowerShell 5.1** pese a que AC1 y AC4 lo declaran
   (4.1, 4.4). O se corrige la declaracion, o se ejercita 5.1 de verdad.
5. **El rojo de `run_mailbox_retry_cases.py`** (seccion 5), sin linea base pre-migracion.

## 7. Recomendacion de cierre

**CHANGE-REQUIRED.**

No bloqueo la migracion de host: funciona, es reversible por etiqueta, y la facturacion es cero
medida por mi. Bloqueo el cierre porque el AC2 -- el AC que manda, segun tu propia instruccion -- no
esta acreditado, y porque la evidencia entregada afirma dos cosas (AC1 y AC4 sobre PowerShell 5.1)
que el log del run citado desmiente.

Remediacion minima que aceptaria:

- **AC2.** Un par de verdad, con las tres condiciones a la vez: (i) **el mismo commit de workflow en
  los dos brazos**; (ii) suciedad que **sobreviva a `git clean -ffdx` + `git reset --hard HEAD`** --
  o sea, residuo en `.git/`, en la config git, en site-packages o en el entorno del host, no ficheros
  untracked en el arbol; (iii) el brazo limpio **pasando** el job que se usa como testigo, o
  eligiendo como testigo un job que si pase (`falsification-runners-python` lleva SUCCESS en los tres
  runs citados y sirve). Si el brazo sucio no puede romperse cuando se le quita la guardia, el AC2
  sigue sin acreditar nada, por mucho que las corridas existan.
- **AC1/AC4.** O se corrige el texto (el job va a `protocol-win` por la semantica Windows del runner
  de mailbox retry, no por 5.1), o se anade un paso que ejecute algo bajo
  `powershell.exe` 5.1 de verdad y publique su version. Cualquiera de las dos me vale; la mezcla
  actual, no.
- **AC5.** Basta con declarar el cambio de `Set up Python` en Windows como consecuencia asumida. No
  pido revertirlo.

**Gates afectados por la remediacion:** ninguno del repo (validate, scan_encoding, neutralidad y drift
salen 0 al ancla y seguiran saliendo 0). La remediacion vive en `.github/workflows/validate.yml`, en
el texto de la tarea y en runs nuevos de Actions.

**Re-juicio:** vuelvo a juzgar antes del commit de cierre. **Maximo 2 iteraciones** antes de escalar
al operador humano.

---

*Analista, 2026-08-13 14:36 local (UTC+2). Medido en clon limpio con `git clone -s -n`; ninguna
afirmacion de este veredicto se apoya en el arbol caliente ni en el resumen del maker.*
