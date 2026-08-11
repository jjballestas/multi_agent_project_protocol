---
id: TASK-0354
title: El workflow no cancela corridas superadas y paga el multiplicador de Windows por dos runners que no lo necesitan
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
created: 2026-08-10
intake:
  type: infra
  goal: >
    Autorizado por el operador el 2026-08-10. El repo es PRIVADO, asi que cada minuto de Actions se
    factura, y el workflow se dispara con `on: push` sin filtro y sin guarda de concurrencia. Medido
    sobre 400 corridas (06 al 10 de agosto): el **45%** fue superado por otra corrida en menos de 5
    minutos y el 30% en menos de 3 -- con tres agentes empujando a rafagas, casi la mitad del gasto
    es en corridas que nacian obsoletas. Ademas `falsification-runners` corre en `windows-latest`
    (multiplicador x2) y de sus TRES runners solo uno tiene dependencia real de host:
    `run_mailbox_retry_cases.py` extrae funciones de `scripts/harness/peer_mailbox_cron.ps1`, las
    muta y las ejecuta con `powershell.exe` -- Windows PowerShell 5.1, el mismo interprete bajo el
    que corren los crons en produccion. Los otros dos son Python puro (`subprocess` solo invoca
    `git`). Dos cambios en el mismo fichero gobernado, una sola tarea.
  acceptance:
    - "AC1 (guarda de concurrencia): el workflow cancela la corrida anterior de la misma referencia cuando llega una nueva. Se acredita por COMPORTAMIENTO -- dos pushes seguidos y la primera corrida en estado `cancelled` -- no por la presencia del bloque en el YAML. Si Actions sigue bloqueada por facturacion cuando se entregue, se declara como residual y se acredita al desbloquear."
    - "AC2 (el residual de la cancelacion, declarado): con cancelacion activa, los commits intermedios de una rafaga NO quedan validados individualmente. Se declara por escrito que el modelo de puerta de esta instancia valida el ARBOL en HEAD y no cada commit, y que la contrapartida es que bisecar una regresion futura pierde granularidad. No se oculta como detalle de implementacion."
    - "AC3 (colocacion por dependencia REAL, derivada): cada runner del workflow se coloca en el host que su dependencia exige, y la dependencia se DERIVA del runner -- que interprete invoca, que binario necesita -- no de donde estaba antes. Se declara runner por runner por que va donde va."
    - "AC4 (cero perdida de cobertura): despues del cambio, el conjunto de runners ejecutados por el workflow es el MISMO que antes. Se acredita comparando los dos conjuntos derivados del YAML, no afirmando que no se quito nada."
    - "AC5 (la dependencia dura sigue siendo dura): `run_mailbox_retry_cases.py` hoy NO tiene guarda de disponibilidad de `powershell.exe`: en un host sin el revienta con FileNotFoundError en vez de saltarse el caso. Eso es correcto y debe seguir asi. Se falsa que no se ha introducido ningun `skip`, `which` ni try/except que convierta la ausencia del interprete en verde."
    - "AC6 (sin regresion): el replicador local del job no empeora; se declara el saldo antes y despues, con la lista de fallos derivada del propio run."
  verification_cmd:
    - "python scripts/replay_validate_job.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - .github/workflows/validate.yml
  out_of_scope:
    - "Excluir `personal/**` de los disparadores: ahorraria otro tercio, pero `scan_encoding.py` y `scan_domain_neutrality.py` recorren el repo ENTERO y si escanean `personal/`. Excluirlo quita cobertura real. La decision previa -- si `personal/` debe estar gateado -- es de protocolo y no se toma aqui."
    - "La cascada de TASK-0353 y TASK-0347."
    - "Desbloquear la facturacion de Actions: decision del operador, y su instruccion es no desbloquear hasta cerrar la cascada en local."
  risk: medium
  estimate: S
---

# TASK-0354 -- lo que se paga sin comprar informacion

## Lo medido

    corridas analizadas            400   (2026-08-06 -> 2026-08-10)
    superadas por otra en < 3 min  122   (30%)
    superadas por otra en < 5 min  179   (45%)
    corridas/dia                   43 / 106 / 153 / 94

    coste por push (3 jobs):
        validate                 ubuntu    3m52s   x1
        powershell-linux-parity  ubuntu    0m51s   x1
        falsification-runners    windows   2m26s   x2   <- la mitad de la factura

Nota: esos 3m52s son de un `validate` que **aborto en el paso 28 de 77**. Cuando la cascada cierre y
el job recorra los 77, durara mas. El coste por corrida va a SUBIR.

## La pregunta que el operador pidio investigar, contestada

**?La cobertura de `falsification-runners` ya esta en `powershell-linux-parity`?** No. Son conjuntos
disjuntos y con proposito opuesto:

    powershell-linux-parity  ->  scan_encoding.ps1, scan_domain_neutrality.ps1,
                                 run_neutrality_scan_cases.ps1        [pwsh 7 sobre Linux]
                                 proposito: PORTABILIDAD del escaner

    falsification-runners    ->  run_mailbox_retry_cases.py           [powershell.exe 5.1]
                                 objetivo: scripts/harness/peer_mailbox_cron.ps1
                                 proposito: FIDELIDAD al host de produccion
                                 run_runtime_turn_obstacle_cases.py   [python + git]
                                 run_post_gate_obstacle_cases.py      [python puro]

El primero ejercita el interprete bajo el que corren los crons de verdad. Ese runner **debe** quedarse
en Windows. Los otros dos pagan el x2 sin ninguna razon de host.

## Lo que NO se acepta como cumplimiento

- Un bloque `concurrency` en el YAML **sin una corrida cancelada que lo demuestre** (AC1).
- Colocar los runners "donde parece razonable": la colocacion se **deriva** de lo que cada runner
  invoca, y se declara uno a uno (AC3).
- Convertir la dependencia dura de `powershell.exe` en un `skip` para que el runner "pase" en Linux.
  Eso seria un gate que aprueba por no ejecutar (AC5).

## Remediacion de dependencias y residuales de cierre

La dependencia de paquetes se verifica desde el propio workflow. El job `validate` deriva los
runners Python de los comandos `run`, analiza sus imports de nivel superior, excluye stdlib y
modulos locales del repositorio, resuelve modulo -> distribucion con los metadatos instalados y
compara el resultado con los `python -m pip install` declarados por cada job. Un modulo externo sin
proveedor conocido o sin distribucion declarada deja el workflow en rojo. En particular, `yaml`
se resuelve a `pyyaml`; quitar `pyyaml` del job `falsification-runners-python` debe matar esta puerta.

La granularidad elegida sigue siendo `github.workflow` + `github.ref`. Por eso una corrida `push`
y una corrida `pull_request` del mismo commit usan referencias distintas y no se cancelan entre si.
Se acepta esa duplicacion para conservar ambos triggers; la guarda elimina solo corridas superadas
del mismo workflow y la misma referencia.

La puerta estatica de contratos acredita cableado, no ejecucion de cada corrida: una corrida
cancelada puede no ejecutar sus runners. La corrida superviviente sobre el HEAD es la que conserva
la cobertura. AC1 sigue pendiente hasta que Actions permita dos pushes rapidos y la primera corrida
se observe en estado `cancelled`; la presencia del YAML no lo acredita. La cancelacion tambien
reduce la granularidad de validacion y de una futura biseccion para commits intermedios de una rafaga.

Para AC6, el replicador sin `--job` solo cubre `validate` y es ciego a los jobs movidos. La
remediacion mide por separado `falsification-runners` y `falsification-runners-python`, y deriva sus
fallos de cada salida. La comparacion de saldo historico se hace en clones limpios de las anclas
`a583e189^` y `a583e189`, nunca desde el arbol vivo.

## Remediacion G1 autorizada el 2026-08-11

El criterio de pertenencia no enumera formas de invocacion. La poblacion se deriva de todos los
ficheros `.py` del repositorio que aparecen nombrados en cada bloque `run`, con separadores de ruta
normalizados. Para cada bloque, el conjunto descubierto por el analizador de invocaciones debe
contener esa poblacion. Una omision produce `FAIL`, nombra la ruta concreta que falta y no puede
repararse bajando un cardinal literal.

El tokenizador conserva la semantica de host del job: usa reglas POSIX salvo cuando `runs-on`
declara Windows. Esta diferencia evita interpretar `\` como escape en comandos del job Windows.
Una forma script descubierta cuyo token no resuelva a un fichero del repositorio queda en postura
fail-closed. La cobertura no alcanza tokens compuestos que no presentan una ruta `.py` al analizador:
`$BASE` compuesto, `find -exec` y `bash -c` sobreviven y quedan declarados como residual.

G2 queda explicitamente fuera de esta vuelta: la superficie de la puerta termina en el fichero
del runner descubierto. No calcula clausura transitiva de imports locales ni certifica procesos
hijo. Cerrar esa clase requiere otro mecanismo y otra tarea; no se presenta como cubierto aqui.
