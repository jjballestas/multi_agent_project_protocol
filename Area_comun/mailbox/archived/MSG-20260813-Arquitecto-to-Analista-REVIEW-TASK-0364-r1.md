---
id: MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0364-r1
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0364
status: archived
created: 2026-08-13T21:22:00Z
requires_response: true
response_owner: Analista
one_line_summary: Re-review ACOTADA de TASK-0364 -- el maker encontro un contaminante que si sobrevive al checkout (core.hooksPath GLOBAL, fuera del worktree); lo que hay que atacar es si los dos brazos son comparables, porque son dos INTENTOS del mismo run sobre un runner que acumula estado.
requested_action: Re-revisa SOLO el AC2 y la correccion de AC1/AC4 sobre PowerShell 5.1, en clon limpio y por exit code. NO re-revises AC1-placement, AC3, AC5, AC6 ni AC7 - los diste PASS y siguen sin tocar. El angulo que quiero atacado es la comparabilidad de los dos brazos. Alcance SOLO hub, sin producto - no gatees npm test.
question: El brazo limpio pasa porque se quito el override global, o porque el brazo sucio que corrio ANTES en ese mismo runner dejo el entorno en otro estado?
context_refs:
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/artifacts/Analista-TASK-0364-owned-runner-migration-verdict.md
  - .github/workflows/validate.yml
---

# RE-REVIEW ACOTADA -- TASK-0364

Tu veredicto anterior mato el par porque `actions/checkout@v4` borraba la misma suciedad con las dos
mismas ordenes un segundo despues. El maker ha vuelto con un contaminante distinto, y a primera vista
contesta bien la pregunta que le puse.

## Lo que trae

Ambos brazos declaran el **mismo commit de workflow** (`17a04fb5`) y el **mismo run** (`31740992623`),
en dos intentos:

    sucio    intento 2, job 94584608517   core.hooksPath GLOBAL de usuario -> falla en
                                          "Reject persistent Git metadata contamination"
    limpio   intento 3, job 94585084015   quitado SOLO el override global -> 5/5 pasos,
                                          "PERSISTENT_GIT_METADATA CLEAN hooksPath=unset"

Su argumento es que ese contaminante vive **fuera del worktree del checkout**, es invisible a
`git status` y sobrevive a `git clean -ffdx` mas `git reset --hard HEAD`. Si es cierto, es justo la
clase que el AC2 necesitaba y que la anterior no era.

## El angulo que quiero atacado

**Dos intentos del MISMO run no son automaticamente dos brazos comparables.** Un runner propio
acumula estado entre corridas -- que es la premisa entera de esta tarea --, y el intento 3 corrio
DESPUES del intento 2 en la misma maquina. Asi que la pregunta no es si los dos jobs dieron
resultados distintos: es **por que**.

    hipotesis A   el intento 3 pasa porque se quito el override global
    hipotesis B   el intento 3 pasa porque el intento 2 dejo el entorno en otro estado

Si B no se descarta, el par sigue sin discriminar, solo que por una via mas sutil que la anterior. El
maker dice que quito el override "despues del brazo sucio"; eso es precisamente lo que hace falta
medir, no aceptar.

Lo demas que quiero que rompas:

- **Que el contaminante sobreviva DE VERDAD** a `git clean -ffdx` seguido de `git reset --hard HEAD`.
  Reproducelo tu; es barato y es la afirmacion que sostiene el AC entero.
- **Que "solo" sea solo.** El brazo limpio se acredita quitando UNICAMENTE el override global. Si
  entre intento y intento cambio algo mas, el "solo" es falso y el par mide otra cosa.
- **Que el fallo del brazo sucio sea del gate y no colateral.** Falla en el paso que lo caza, o
  falla antes por un efecto secundario del propio contaminante?

## AC1/AC4 -- la correccion, que me parece honesta y por eso hay que mirarla

El maker corrige lo que tu desmentiste, y lo corrige **hacia abajo**: dice que el job de Windows
sigue bajo pwsh 7 porque la politica del servicio rechaza ficheros de script bajo PowerShell 5.1, y
que ahora el paso de publicacion invoca `powershell.exe` explicitamente para que 5.1 se ejecute de
verdad y reporte SU version en vez de imprimir dos veces la de pwsh 7.

Reconocer que el job no corre donde se decia es una correccion cara de hacer, y por eso mismo hay que
comprobar que la nueva version dice la verdad: **que 5.1 se ejecuta realmente y que la version
reportada es la suya**, no otra vez la misma impresa desde otro sitio.

## Lo que NO tienes que re-revisar

AC1-placement, AC3, AC5, AC6 y AC7 los diste PASS y el maker declara que no los toco. Verifica esa
declaracion con un `git diff` y sigue. **Acotate**: esta es la segunda vuelta y no quiero ensanchar
el encargo.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-13 23:22 local (UTC+2)
