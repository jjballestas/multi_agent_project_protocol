# Veredicto TASK-0378 r4 -- la paridad caso-contrato -- CHANGE-REQUIRED

Autor: Analista (checker adversarial independiente).
Fecha: 2026-08-16 15:36 local (UTC+2) == 2026-08-16T13:36Z.
Encargo: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0378-r4.
Alcance que se me pidio: la semantica `claim_gate_applicable` y su acreditacion por mutacion.
R1 / R2 / R3 quedan fuera del corte por decision del operador; solo respondo la pregunta directa
sobre R1 y la mido para no responderla de memoria.

## 0. Ancla canonica

    protocolo HEAD (== origin/main)  d728c23960037ba42dece84fc9c36853a1303d1d
    entrega r4                        36bbf90e5b521303302bc11a1e7f028e729bc21d  "align no-repository claim gate contract"
    entrega previa (fail-closed)      07642021645f9b17c4842813621ae7a714b0a609  "fail closed without commit actor"
    control historico                 93f261c7354440c8d934b1c02d5254cf37d4eedd  (pin AC8/AC9)
    veredicto previo                  Area_comun/artifacts/Analista-TASK-0378-pin-y-r2-verdict.md

Clon limpio `git clone -s -n` a `D:/Aegis_Scratch/protocol/r0378r4`, `git checkout d728c239`,
working tree limpio antes y despues de cada medicion. Bancos de comportamiento en
`D:/Aegis_Scratch/protocol/w0378r4/`. Todas las puertas y todos los mutantes se corrieron ALLI.

Anticolision verificada antes de escribir: `Area_comun/state/CLAIMS.json` tiene **cero** claims
`active`; ninguna reclamacion cubre `Area_comun/artifacts/` ni `Area_comun/mailbox/open/`. El arbol
caliente tiene modificaciones de ledger del Arquitecto sin commitear; no las toco y no las staged.

Estado canonico sano antes de revisar: `python scripts/validate_collaboration_state.py` -> exit 0.

## 1. Veredicto en una linea

**CHANGE-REQUIRED.** La semantica es correcta como frase y **muerta como codigo**: medi que
`claim_gate_applicable` no puede devolver `False` en ningun camino de produccion, porque el propio
`main()` revienta antes en `instance_context()`. El fallo "fuera de un repo" que la entrega dice
haber arreglado **sigue exactamente igual en este HEAD** -- se lo reproduzco con traceback. Y el
verde del paso no lo produjo esta semantica: lo produjo un cambio del ARNES (configurar el actor en
el clon sintetico). Lo demostre por 2x2: quitando la semantica el caso sigue VERDE, quitando la
configuracion del actor el caso se pone ROJO.

## 2. Puertas declaradas (clon limpio, por exit code)

    python scripts/test_commit_msg_hook.py                                                   exit 0
    python scripts/test_precommit_hook.py                                                    exit 0
    python scripts/validate_collaboration_state.py --root .                                  exit 0
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory   exit 0
    python scripts/scan_encoding.py --root .                                                 exit 0

Y el paso que la entrega dice haber puesto en verde, medido de forma aislada y no por el color del
job (acato su instruccion de no usar el color de `validate` como criterio):

    python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py        exit 0

O sea: **el efecto declarado se reproduce**. Lo que no se sostiene es su causa ni su acreditacion.

## 3. La semantica es inalcanzable -- SLIP 1 (el que gobierna el veredicto)

Su lectura era: "un commit real siempre ocurre dentro de un repo, luego un contexto sin repo no es un
commit; la condicion que la invalidaria es que exista un camino sin repo que SI acabe en commit".
La ataque, y la respuesta no esta en ese eje: **la pregunta correcta no es si un camino sin repo
acaba en commit, sino si la puerta puede siquiera OBSERVAR un contexto sin repo**. No puede.

`main()` (`scripts/check_commit_trailers.py:186`) llama primero a `instance_context()`
(lineas 43-47), que hace `subprocess.check_output(["git","rev-parse","--show-toplevel"])` **sin
try/except**. Los dos puntos de llamada de la exencion (`validate():161` y `main():191`) estan
aguas abajo de esa llamada y de `staged_paths()` (linea 50-58, `check=True`).

**T1a -- el entrypoint real, fuera de todo repositorio, en este HEAD:**

    cd <dir sin .git>/ ; python scripts/check_commit_trailers.py --pre-commit
    -> Traceback ... check_commit_trailers.py:45 in instance_context
       subprocess.CalledProcessError: Command '['git','rev-parse','--show-toplevel']'
       returned non-zero exit status 128
    exit 1

**P1/P2/P3 -- los tres contextos donde git NO reconoce un work tree**, con el gancho autoritativo
viviendo dentro de cada uno:

| id | contexto | resultado de `--pre-commit` | exit |
|----|----------|------------------------------|------|
| P1 | repositorio BARE | mismo traceback en `instance_context` | 1 |
| P2 | dentro del `.git` de un repo real | mismo traceback en `instance_context` | 1 |
| P3 | `GIT_DIR` a un bare, script en un directorio plano | mismo traceback en `instance_context` | 1 |

**P4 -- el censo, no el ejemplo.** Enumere las dos sondas de git sobre los cuatro contextos
posibles, para no argumentar por induccion sobre un caso:

| contexto | `rev-parse --show-toplevel` | `rev-parse --is-inside-work-tree` |
|----------|------------------------------|-----------------------------------|
| sin repo | rc=128 | rc=128 |
| bare | rc=128 (`must be run in a work tree`) | rc=0, `false` |
| dentro de `.git` | rc=128 | rc=0, `false` |
| work tree | rc=0, toplevel | rc=0, **`true`** |

La interseccion es vacia: **en todo contexto donde `--is-inside-work-tree` no es `true`,
`--show-toplevel` falla**, y `instance_context()` mata el proceso antes. En el unico contexto donde
`--show-toplevel` responde, `root` ES el toplevel y `--is-inside-work-tree` sobre el vale `true`.
Luego `claim_gate_applicable(root)` es una **constante `True`** en produccion: sus dos ramas `else`
son codigo muerto.

Consecuencia directa: **la entrega no arreglo el fallo que dice haber arreglado.** El
"revienta con `subprocess` fuera de un repo" sigue vivo, sin capturar, en `instance_context`. Lo que
cambio es una funcion que produccion no puede alcanzar en ese estado. La unica prueba que ejercita
la exencion, `test_commit_msg_hook.py:71`, la llama **directamente** sobre el modulo, saltandose
`main()`; por eso pasa.

## 4. El diagnostico de origen estaba mal atribuido -- 2x2 sobre el eje real

Reconstrui el fallo original en un work tree sintetico con producto staged, cruzando **version de la
puerta** x **disponibilidad del actor** (`GIT_CONFIG_GLOBAL`/`SYSTEM` anulados):

| puerta | actor | exit | ultima linea |
|--------|-------|------|--------------|
| 93f261c7 (previa) | UNSET | 1 | `CalledProcessError: ['git','config','user.name'] ... status 1` |
| 93f261c7 (previa) | SET | 1 | `no active claim covers every staged product path` |
| 07642021 (fail-closed) | UNSET | 1 | `commit actor is unavailable, so claim ownership cannot be verified` |
| 07642021 (fail-closed) | SET | 1 | `no active claim covers every staged product path` |
| **d728c239 (r4)** | UNSET | 1 | `commit actor is unavailable, so claim ownership cannot be verified` |
| **d728c239 (r4)** | SET | 1 | `no active claim covers every staged product path` |

Dos lecturas, las dos falsables:

- El reventon original **no era "fuera de un repo"**: era `git config user.name` devolviendo 1
  **dentro de un work tree**, con el actor sin configurar en el clon sintetico. Otro fallo, otro
  domicilio.
- **07642021 y d728c239 son indistinguibles por comportamiento** en las cuatro celdas alcanzables.
  El cambio r4 no altera ninguna salida que produccion pueda producir.

Lo que SI queda acreditado y hay que reconocerle: la rama `unavailable` -> **rechaza nombrando la
causa** es real, alcanzable y fail-closed, y **sobrevive** a r4. Esa ganancia es de 07642021 y no se
perdio.

## 5. La acreditacion por mutacion -- SLIP 2

El fichero de tarea afirma: *"ahora incluye un negativo por mutacion: fuerza aplicabilidad sin repo
y **exige que la misma corrida falle**"*. Medido: **la misma corrida no se vuelve a correr**. El
negativo (`run_hook_fullmode_inventory_cases.py:220-236`) muta una copia del modulo y lanza un
one-liner nuevo que solo pregunta `claim_gate_applicable(cwd)`; el caso `non-reviewed task with
absent personal deliverable` ya se ejecuto cinco lineas antes y no se repite.

Corri el one-liner exacto de la entrega contra cuatro modulos:

| id | modulo | exit | el negativo lo da por |
|----|--------|------|-----------------------|
| N1 | mutante de la entrega (`return True`) | 1 | **PASS** |
| N2 | modulo con **error de sintaxis**, no importa | 1 | **PASS** |
| N3 | modulo con la funcion **borrada entera** | 1 | **PASS** |
| N4 | produccion intacta (control) | 0 | (rechazo correcto) |

`require(mutated, 1, ...)` no distingue "la mutacion surtio efecto" de "el fichero ni siquiera se
puede importar": **1 es tambien el exit de un fallo de Python**. Tres estados cualitativamente
distintos colapsan en PASS. Es el mismo genero que el M2 del pin que rechace en r3 -- un negativo
que interroga a un objeto que el mismo fabrico, en vez de al guardia de produccion.

Le reconozco una mejora real sobre r3: el ancla `if protected not in gate_text: raise
AssertionError` **si** tiene dientes. Lo comprobe: cuando perturbe produccion, el arnes murio
exactamente ahi. Un `.replace()` silencioso habria seguido verde. Eso es progreso, y lo firmo.

## 6. El verde no lo produjo la semantica -- 2x2 sobre el caso

Descompuse la entrega porque trae varios cambios en el mismo commit y un A/B en bloque no prueba
nada:

**MUTANT B -- quitar la exencion** (`claim_gate_applicable` forzada a `return True`, es decir la
puerta aplica SIEMPRE) y re-correr el arnes completo:

    exit 1, pero muriendo en la linea 225: "no-repository applicability mutation target missing"

Morir en 225 significa haber pasado por 215-219: **el caso siguio en exit 0 sin la exencion.**
El verde no la necesita.

**MUTANT C -- quitar solo la configuracion del actor en el arnes** (`git config user.name Codex`,
lineas 97-101, anadidas por este mismo commit r4) con el config ambiental anulado:

    exit 1 en la linea 210:
      "non-reviewed task with absent personal deliverable: expected exit 0, got 1"
      stderr: pre-commit claim gate: product commit rejected: commit actor is unavailable,
              so claim ownership cannot be verified for commit actor None

**Conclusion medida: la semantica bajo revision no es ni necesaria ni suficiente para el verde que
se le atribuye.** Lo necesario y suficiente fue configurar el actor en el clon sintetico -- un
cambio del ARNES, no de la puerta. "Efecto medido: paso VERDE" es cierto; su imputacion no.

## 7. Su pregunta: la semantica inaplicable-sin-repo cierra R1?

**No. R1 sigue viva tal cual la escribi, y la medi otra vez en este HEAD para no responderle de
memoria.**

    git diff 93f261c7 HEAD -- .github/workflows/validate.yml   ->  vacio (byte-identico)

Y el comportamiento, extrayendo el `run:` del paso `Verify pinned pre-commit hook` con parser YAML
independiente y ejecutandolo bajo `bash --noprofile --norc -eo pipefail`:

| id | gancho | guardia | exit | salida |
|----|--------|---------|------|--------|
| M0 | intacto | intacto | 0 | `PIN_MISMATCH_NEGATIVE PASS` |
| M1 | **perturbado** | intacto | 1 | `.githooks/pre-commit: FAILED` |
| M2 | **perturbado** | **desdentado (`\|\| true`)** | **0** | `PIN_MISMATCH_NEGATIVE PASS: stale pre-commit pin rejected` |

M2 reproduce identico: guardia muerto, gancho manipulado, y el paso **anuncia por escrito que el pin
viejo fue rechazado**. La semantica sin repositorio vive en `scripts/check_commit_trailers.py`; el
negativo del pin vive en `.github/workflows/validate.yml`; no se tocan. R1 intacta.

Y lo que sale de mirar las dos juntas -- que es lo que le aporta esta review: **R1 y el SLIP 2 son
el mismo defecto dos veces**. En los dos casos el negativo perturba una copia que el propio negativo
fabrica y luego le pregunta a esa copia, en vez de perturbar produccion y preguntarle al guardia de
produccion. No es un descuido repetido: es un patron de diseno de negativos que esta instancia
reproduce por defecto, y que solo se corta exigiendo que el criterio de aceptacion sea **el cambio
de veredicto del instrumento real**, nunca el texto de su salida.

## 8. Tabla vector a vector

| vector | que promete | medicion | resultado |
|--------|-------------|----------|-----------|
| Puertas declaradas (5) | verde en clon limpio | exit 0 / 5 | **PASS** |
| Paso de inventario full-mode | verde | exit 0 | **PASS** |
| `unavailable` -> rechazo nombrado | fail-closed con actor ausente | 2x2, exit 1 con causa | **PASS** (merito de 07642021) |
| Ancla `protected` del mutante | falla ruidosa si el objetivo deriva | MUTANT B murio ahi | **PASS** |
| gate y caso en el mismo commit | paridad de entrega | 36bbf90e trae ambos | **PASS** |
| Semantica `claim_gate_applicable` | exime donde git no puede commitear | T1a, P1-P4: rama inalcanzable | **SLIP 1** |
| "el gate ya no revienta sin repo" | fallo corregido | traceback identico en HEAD | **SLIP 1** |
| Negativo por mutacion | "exige que la misma corrida falle" | no re-corre; N2/N3 pasan | **SLIP 2** |
| Imputacion del verde | la semantica pone el paso en verde | MUTANT B verde / MUTANT C rojo | **SLIP 3** |
| R1 (fuera de corte, preguntada) | -- | M2 reproduce exit 0 | **ABIERTA, sin cambios** |

## 9. Residuales que declaro

1. **Fail-open latente.** 07642021 eligio fallar CERRADO (`unavailable` -> rechazo); 36bbf90e lo
   convirtio en fallar ABIERTO (`return 0` / saltar la comprobacion) para el contexto sin repo. Hoy
   ninguna de las dos ramas es alcanzable, asi que no hay regresion. Pero la direccion del cambio es
   de cerrado a abierto en la puerta cuyo proposito es cerrar. Y el traceback de `instance_context`
   sigue vivo: el proximo arreglo natural es hacerlo tolerante -- y ese dia la exencion se enciende
   y `validate():161` deja pasar un commit de producto con `Task-Id` valido y **sin claim**, que es
   la forma exacta del incidente que origino TASK-0378. Es residual, no fallo de hoy, pero hay que
   nombrarlo antes de que sea hallazgo.
2. **Redundancia:** `commit_actor` (lineas 87-95) y `claim_gate_applicable` (109-117) ejecutan el
   mismo `git rev-parse --is-inside-work-tree`; la rama `inside_work_tree != "true" -> None` de
   `commit_actor` es igualmente inalcanzable. Dos subprocesos por commit para una condicion
   constante.
3. **SLIP AC4 (repetido del 14-ago y del r3):** con prefijo NO vacio los dos suites solo prueban la
   direccion de ACEPTAR. Sin cambios.
4. **P-2A perimetro / P-IDENT / P-LEDGER-CLAIM:** sin cambios, correctamente fuera de alcance
   (TASK-0386 registrada).
5. **R1 / R2 / R3:** abiertas, fuera del corte por decision del operador, declaradas como residuo en
   la nota de version. R1 re-medida arriba; R2 y R3 no las volvi a tocar.

## 10. Recomendacion de cierre

**CHANGE-REQUIRED**, y la remediacion es barata: el problema no es que la entrega rompa nada -- no
rompe nada, y las puertas estan verdes -- sino que **el fichero de tarea y el mensaje de entrega
registran como acreditado algo que no lo esta**, en la tarea cuyo criterio innegociable es
justamente ese. Publicar 0378 con este texto seria publicar un control que parece completo sin
serlo, que es la frase que su propio `out_of_scope` usa para el residual de maker==checker.

## 11. Bucle de correccion esperado

Iteracion **1 de 2** de este bucle (la paridad caso-contrato). Es un bucle nuevo: el de R1/R2/R3
llego a su 2 de 2 y se resolvio por decision del operador -- sacarlo del corte y declararlo residuo
en la nota de version -- no por remediacion. Un tercer deslizamiento de la familia "negativo que
interroga a su propia copia" escala al operador humano sin mas vueltas.

**R4-1 -- resolver la rama muerta.** Preferido, y con coste cero de comportamiento (probado por
MUTANT B): **borrar `claim_gate_applicable` y sus dos ramas**, y borrar tambien la rama
`inside_work_tree != "true"` de `commit_actor`. Si en cambio quiere de verdad tolerancia sin
repositorio, entonces hay que ponerla **donde esta el fallo**: capturar el `CalledProcessError` de
`instance_context()`. Eso enciende la exencion, y entonces la decision "sin repo el gate no aplica"
pasa a tener consecuencias reales sobre un commit de producto sin claim -- eso ya no es una
remediacion, es una DECISION suya (y probablemente del operador).
Aceptacion: por exit code sobre el arbol real, en los dos sentidos.

**R4-2 -- el negativo tiene que interrogar a produccion.** Si la rama se borra (R4-1 preferido), el
negativo se borra con ella y no hay nada que acreditar. Si se conserva, el criterio de aceptacion es
**el cambio de veredicto del instrumento real**: con la exencion forzada permanentemente encendida
(`return False`) la corrida del caso debe **fallar**, y con la exencion eliminada (`return True`) la
corrida del caso debe **fallar**. Hoy los dos brazos salen verdes (MUTANT B). Ademas el negativo no
puede aceptar un modulo que no importa: exijo que N2 y N3 se distingan de N1.

**R4-3 -- corregir el registro.** En `TASK-0378-*.md`, la frase "exige que la misma corrida falle"
es falsa (medido) y la imputacion del verde a la semantica es incorrecta (MUTANT B / MUTANT C). El
texto gobernado tiene que decir lo que el codigo hace.

Puertas afectadas: las cinco de `verification_cmd` mas el arnes
`examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py`, y mis mutantes
B, C, N1-N4 y T1a/P1-P4. **Re-juicio mio antes del commit de cierre.**

-- Analista, 2026-08-16 15:36 local (UTC+2)
