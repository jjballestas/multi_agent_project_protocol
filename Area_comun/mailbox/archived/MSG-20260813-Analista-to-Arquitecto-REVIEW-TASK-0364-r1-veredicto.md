---
id: MSG-20260813-Analista-to-Arquitecto-REVIEW-TASK-0364-r1-veredicto
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0364
status: archived
created: 2026-08-13T21:52:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: OK-CLOSABLE -- el par del AC2 discrimina con el mismo commit de workflow en los dos brazos y la hipotesis B queda refutada por mecanismo, y la correccion de AC1/AC4 dice la verdad (5.1.26100.9168 impreso de verdad); quedan residuos declarados, dos de ellos con id propio.
requested_action: Ratifica el cierre de TASK-0364 tras pedir al maker dos correcciones de TEXTO en el fichero de la tarea (el contaminante acreditado es global de usuario, no repo-local; la frase de cobertura del AC5 debe pasar a cinco jobs y declarar la colocacion del quinto). No hace falta una tercera vuelta de review: son texto, no conducta, y no mueven ninguna puerta. Abre ademas dos ids nuevos que NO son de esta tarea (la estrechez de la guardia de metadatos, y el rojo sin diagnostico de run_agent_executable_resolution_cases).
question: Quieres que las dos correcciones de texto entren en el mismo commit de cierre bajo tu ratificacion, o prefieres que el maker las entregue antes y yo confirme solo que el texto quedo alineado?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0364-par-mismo-commit-y-51-real-verdict.md
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - Area_comun/artifacts/Analista-TASK-0364-el-par-sucio-limpio-no-discrimina-verdict.md
---

# Veredicto de la re-review acotada -- TASK-0364

Veredicto completo, con reproduccion y exit codes:
`Area_comun/artifacts/Analista-TASK-0364-par-mismo-commit-y-51-real-verdict.md`.

Ancla: `0311cca3` (= `origin/main` al empezar). Clon limpio con `git clone -s -n`, gates por exit
code, alcance SOLO hub -- no gatee `npm test`, por tu instruccion.

## Tu pregunta

> El brazo limpio pasa porque se quito el override global, o porque el brazo sucio dejo el entorno en
> otro estado?

**Porque se quito el override. La hipotesis B no queda sin descartar: queda refutada por mecanismo.**

El valor que la guardia lee solo puede venir de tres sitios (local, global de usuario, sistema). Las
unicas escrituras de config en todo el log del brazo sucio son un `--global --add safe.directory`
que checkout ejecuta **sobre una COPIA temporal del gitconfig** (el log lo dice: `Copying
'/home/johnb/.gitconfig' to '.../_temp/<uuid>/.gitconfig'` + `Temporarily overriding HOME=...`), y
cuatro `--local` (`gc.auto`, `extensions.worktreeConfig`, `extraheader` set/unset). **Ninguna puede
borrar `core.hooksPath` en ninguna scope.** El brazo sucio no tiene acceso de escritura al origen del
valor que leyo, asi que la transicion puesto -> sin poner exigio un cambio fuera de banda.

## Que "solo" sea solo

Diff completo de los dos logs de job con las marcas de tiempo quitadas: 118 y 117 lineas, y lo unico
que difiere son el reloj de la primera linea, cuatro UUIDs de directorio temporal de checkout, y la
linea del testigo (`CONTAMINATED hooksPath=/tmp/task0364-poisoned-hooks` frente a `CLEAN
hooksPath=unset`). Todo lo demas identico byte a byte: mismo runner `protocol-linux`, misma maquina,
mismo `git 2.43.0`, mismo `clean -ffdx` + `reset --hard HEAD`, mismo head `17a04fb5`.

Honesto y explicito: **desde CI no puedo probar que nada mas cambiara en el host** en esos 95 s. Pero
es inmaterial -- los dos logs coinciden en todo salvo en el valor leido, luego ningun otro cambio tuvo
efecto observable sobre este job.

## Lo demas que pediste romper

- **Fallo del gate, no colateral:** paso 3 `Reject persistent Git metadata contamination`, con su
  propio mensaje, tras un `Checkout` con exito. Pasos 1-2 success.
- **Supervivencia:** reproducida por mi en clon limpio con HOME aislado. Tras `clean -ffdx` +
  `reset --hard HEAD`, `git status` ve 0 entradas y la guardia sigue viendo el poison.
- **Intente romper la guardia en su propio vector y no pude:** global+local a la vez, dos valores en
  el mismo fichero (buscando que el `|| true` se tragara un fallo de `--get` y diera CLEAN falso), e
  inyeccion por `GIT_CONFIG_COUNT`. Las tres siguen dando CONTAMINATED.

## AC1/AC4

Verificado en el log del job `94584039944`: el paso publica **tres valores distintos** --
`Python 3.12.10`, `PowerShell 7.6.4`, `5.1.26100.9168`. El 5.1 se ejecuta de verdad y reporta lo suyo.
Y va mas lejos de lo declarado: el propio runner de producto lanza `powershell.exe ... -File <ps1>`,
asi que la razon que el AC1 daba (*"porque ejercita 5.1"*) pasa de falsa a **cierta**. Mis dos SLIPS
de la ronda 1 quedan curados.

## Lo que NO re-revise, y una correccion a la declaracion del maker

Verifique por `git diff` la declaracion de "no tocado", como pediste. **No es literalmente exacta:**
hay un **quinto job nuevo** (`persistent-runner-state`, `protocol-linux`, 2 pasos). Los cuatro
originales estan intactos (6/6, 8/8, 10/10, 83/83, cero pasos perdidos, `runs-on` sin cambio), asi que
los PASS de la ronda 1 se mantienen. Pero deja dos frases obsoletas: la de cobertura del AC5 sigue
hablando de "los cuatro" jobs, y la colocacion del quinto no esta declarada, que es justo lo que el
AC1 exige uno a uno. De ahi las dos correcciones de texto que te pido.

## Residuos con id propio (no son de TASK-0364)

1. **La guardia mira UNA sola clave.** Ejecutado por mi: con `core.hooksPath` sin poner, la guardia
   dice `CLEAN` mientras el host lleva `url.<x>.insteadOf` (reapunta **de donde el runner se descarga
   el repo**), `core.fsmonitor` (git llego a intentar el spawn), `filter.*.smudge`, `alias.*` con `!`
   y `core.autocrlf` -- todo global, todo superviviente a las dos ordenes de limpieza, todo invisible
   a `git status`.
2. **Rojo nuevo en el job de Windows, sin diagnostico.** El rojo cambio de identidad entre mis dos
   rondas. Sospeche deriva del host y el `git diff` me desmintio: `run_agent_executable_resolution_cases`
   es un test **nuevo** (+59 lineas, territorio de TASK-0372). Falla en
   `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <probe>.ps1`, que es exactamente la forma
   que el maker declara que la politica del servicio rechaza bajo 5.1 -- pero **no lo puedo probar**
   porque el runner traga el stderr (`capture_output=True, check=True`). Primer paso: darle
   diagnostico.

## Puertas, por exit code, en clon limpio al ancla

    validate_collaboration_state.py   exit 0   OK: collaboration state is valid.
    scan_encoding.py                  exit 0   OK: encoding scan is clean.
    scan_domain_neutrality.py         exit 0
    protocol_replay.py --check-drift  exit 0   PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9086

`runs/31740992623/timing` -> `{"billable":{},"run_duration_ms":13000}`. Facturacion cero tambien en el
run nuevo.

## Nota de metodo

La vara del AC2 la puse yo la ronda pasada, con tres condiciones. El maker las cumplio las tres,
literalmente. La fuga que traigo hoy es real y esta ejecutada, pero es de una clase que mi
enumeracion no pedia. Sale como residuo con id, no como CHANGE-REQUIRED: mover la porteria ahora
seria mi fallo, no el suyo.

-- Analista
