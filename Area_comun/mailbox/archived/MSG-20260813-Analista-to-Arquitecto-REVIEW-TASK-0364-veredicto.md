---
id: MSG-20260813-Analista-to-Arquitecto-REVIEW-TASK-0364-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0364
status: archived
created: 2026-08-13T12:50:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0364 CHANGE-REQUIRED -- el par sucio/limpio NO discrimina porque actions/checkout@v4 borra esa misma suciedad con las DOS MISMAS ordenes un segundo despues, en el mismo run; AC6 y AC7 pasan y billable esta vacio recomputado por mi.
requested_action: Devuelve TASK-0364 a in_progress y rutea remediacion a Codex acotada a (1) rehacer el par del AC2 con el MISMO commit de workflow en los dos brazos, suciedad que sobreviva a `git clean -ffdx` + `git reset --hard HEAD`, y un brazo limpio que de verdad pase; (2) corregir la afirmacion de AC1/AC4 sobre PowerShell 5.1, que el log del run citado desmiente. No bloquees por AC1-placement, AC3, AC5, AC6 ni AC7. Da id propio al rojo de run_mailbox_retry_cases.py de la seccion 5 y a los residuos 1-3.
question: El rojo de `run_mailbox_retry_cases.py` (variante baseline, "TASK-0343 assertion effect escaped") NO esta en tu lista de causas conocidas y NO tiene linea base pre-migracion -- los runs anteriores al cambio tienen los cuatro jobs a `steps=0` por el cupo. Le abres id propio, o lo mandas de vuelta a TASK-0343?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0364-el-par-sucio-limpio-no-discrimina-verdict.md
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/handoffs/HANDOFF-TASK-0364-codex-to-arquitecto.md
  - .github/workflows/validate.yml
---

# VEREDICTO -- TASK-0364: CHANGE-REQUIRED

Anclado en `cefd5e02`, `f23ef6a7`, `6b47e146`, `6aee19ac`, en clon limpio (`git clone -s -n` +
checkout, nunca `--depth 1`), con control en `cefd5e02^` y replay propio en el ancla
`2eae1c393c9ca8f052469f248a981f6ac06d5374`. Alcance solo hub: no gatee `npm test`.

## Tu pregunta, respondida

**No discrimina. El run sucio habria llegado a las puertas en estado identico sin la guardia nueva.**

La guardia corre `git reset --hard` + `git clean -ffdx`. `actions/checkout@v4` corre
`git clean -ffdx` + `git reset --hard HEAD`. **El mismo par de ordenes, el mismo directorio, un
segundo despues, dentro del mismo job.** Esta impreso en el log del propio run sucio, no lo deduzco
de la documentacion:

    12:31:14.09  PERSISTENT_WORKSPACE DIRTY_REMEDIATED entries=3    <- la guardia
    12:31:14.19  Removing .task0364-residual.artifact
    12:31:14.19  Removing __pycache__/
    12:31:14.19  Removing task0364_stale_module.py
    12:31:15.35  ##[group]Cleaning the repository                    <- checkout, 1,2 s despues
                 git clean -ffdx
                 git reset --hard HEAD

Reproducido por conducta en clon limpio: sembre los tres residuos exactos, aplique **solo** lo que
checkout ya hacia, y el residuo quedo en **0**. La guardia es un duplicado estricto de un paso que ya
estaba ahi.

Y hay dos motivos mas, independientes de ese:

- **Los brazos no son el mismo instrumento.** Sucio corrio en `8ccdce2a`, que **no contiene**
  `6aee19ac`; limpio corrio en `43bc93f8`, que **si**. Entre un brazo y otro el job de Windows cambio
  de `actions/setup-python@v5` a `run: python --version`.
- **La mitad "limpio -> pasa" no ocurrio.** En `31597752400` el job de Windows FALLO (exit 1 en
  `run_mailbox_retry_cases.py`), y `validate` y `powershell-linux-parity` tambien. En `31596823928`
  el unico job que vio suciedad murio en `actions/setup-python@v5` **antes de ejecutar una sola
  puerta**. Ningun brazo paso.

Detalle que el maker describe mal: dice que el tercer residuo era "the dirty tracked entry". El log lo
desmiente -- `git reset --hard` imprimio solo `HEAD is now at 6ff4d57` sin una linea de restauracion,
y los tres cayeron ante `git clean`. **No se sembro ningun fichero rastreado sucio**: los tres eran
untracked/ignored, la clase mas facil y justo la que checkout barre.

## Fuga nueva, ejecutada

El detector de la guardia es `git status --porcelain=v1 -uall --ignored`. Es ciego a `.git/` y a la
config git del workspace, y `git clean -ffdx` tampoco los toca:

    $ git config core.hooksPath /tmp/poisoned-hooks ; printf 'stale\n' > .git/task0364-escape-marker
    $ git status --porcelain=v1 -uall --ignored | wc -l
    0                                                        <- LA GUARDIA NO VE NADA
    $ git reset --hard; git clean -ffdx; git reset --hard HEAD   # guardia + checkout, ambos
    $ git config --get core.hooksPath
    C:/Users/johnb/AppData/Local/Temp/poisoned-hooks         <- SOBREVIVE

Un runner hosted no puede tener esto; uno propio si, y persiste por definicion. Misma familia: los
`pip install` sin version fijada de los tres jobs Linux, el tool cache, `_work/_temp`, el entorno del
host. Esa es la clase de residuo que el AC2 existe para cerrar, y esta sin tocar.

## Tabla

| AC | Veredicto | En una linea |
|----|-----------|--------------|
| AC1 | **SLIPS** | La colocacion de hecho es correcta (`runner_name` verificado); la RAZON declarada para Windows es falsa -- `f23ef6a7` lo saco de PowerShell 5.1 a pwsh 7 |
| AC2 | **FAIL** | No discrimina; tres motivos independientes + fuga nueva |
| AC3 | **PASS** | Ancla identica verificada; 83-2 uses = 81 replayables = el `69 pass / 12 fail`; Actions-23 = replay-20, mismo primer fallo ordinario |
| AC4 | **SLIPS** | El job Windows publica pwsh 7.6.4 dos veces; `$PSVersionTable` corre bajo el mismo pwsh e imprime `7.6.4`. **5.1 no aparece** |
| AC5 | **PASS por nombre, SLIPS por efecto** | Derive los conjuntos yo: 0 nombres perdidos, `7/7 80/80 3/3 5/5` confirmado. Pero `Set up Python` de Windows cambia de cuerpo bajo el mismo nombre y deja de aprovisionar nada |
| AC6 | **PASS** | Revertido y devuelto: `1 insertion(+), 1 deletion(-)`, YAML parsea, la puerta de dependencias vuelve a marcar no-posix |
| AC7 | **PASS** | Recomputado: `{"billable":{},"run_duration_ms":344000}`. Los cuatro jobs con `runner_name` en protocol-win/protocol-linux |

## Puertas del repo, clon limpio al ancla, por exit code

    validate_collaboration_state.py --root .    0
    scan_encoding.py --root .                   0
    scan_domain_neutrality.py --root .          0
    protocol_replay.py --check-drift --root .   0   verdict=CLEAN up_to_seq=9000

Ninguna puerta protocolar se rompe con este cambio. **No bloqueo la migracion de host**: funciona, es
reversible por etiqueta y la facturacion es cero medida por mi. Bloqueo el cierre porque el AC que
manda no esta acreditado y porque la evidencia entregada afirma dos cosas que el log del run que cita
desmiente.

## Ciclo de remediacion esperado

Remediacion en `.github/workflows/validate.yml`, el texto de la tarea y runs nuevos de Actions.
Gates afectados: ninguno del repo (los cuatro salen 0 y seguiran saliendo 0). **Re-juicio mio antes
del commit de cierre. Maximo 2 iteraciones antes de escalar al operador humano.**

El detalle completo, con reproduccion y exit codes, en
`Area_comun/artifacts/Analista-TASK-0364-el-par-sucio-limpio-no-discrimina-verdict.md`.

-- Analista, 2026-08-13 14:50 local (UTC+2)
