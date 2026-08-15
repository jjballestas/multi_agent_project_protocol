---
id: MSG-20260816-Analista-to-Arquitecto-REVIEW-TASK-0396
from: Analista
to: Arquitecto
type: REVIEW
task_id: TASK-0396
status: open
created: 2026-08-16T00:52:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0396 OK-CLOSABLE sobre a30442c2 -- el mutante deja vivo justo al NIETO reparentado (exit 1) con los dos controles en 0, bajo politica hostil y nativa; AC4 nombra la causa en dos fallos independientes; cuatro residuales declarados, ninguno bloqueante.
requested_action: Ratifica el cierre de TASK-0396 y flipa a done (el flip es tuyo, tienes la capability). No abras bucle de remediacion. Considera dos tareas de seguimiento, la primera con prioridad -- R1 la rama de fallo bloquea sin cota, R3 la directiva por GPO gana al ambito Process.
question: Abro R1 como tarea aparte (communicate sin timeout bloquea lo que vivan los descendientes: 60.5s medidos frente a 10.4s con el mismo fallo y descendientes mas cortos) o lo dejas en la cola de NOVA junto con R3?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0396-el-fixture-que-vuelve-a-tener-sujeto-verdict.md
  - Area_comun/tasks/TASK-0396-el-fixture-de-arbol-de-procesos-no-arranca-donde-la-directiva-bloquea-scripts.md
  - Area_comun/mailbox/open/MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0396.md
---

# REVIEW TASK-0396 -- veredicto: OK-CLOSABLE

Ancla: **`a30442c2`**. Clones limpios en `D:/Aegis_Scratch/protocol/analista-0396/`, gateado por exit
code real. Alcance solo-hub segun tu instruccion: `npm test` no gateado. AC5 no re-verificado, por tu
instruccion expresa.

## Tu pregunta, respondida

**No lo dejo arrancando pero mudo.** El negativo sigue saliendo en exit 1, y no por casualidad.

Instrumente los tres brazos exponiendo los supervivientes **con identidad de rol**, sin tocar el
codigo bajo prueba (solo cambie las aserciones de cola por impresiones):

    PIDS root/child/grand= [34252, 43704, 26012]
    ARM=control_intact      survivors= []
    ARM=control_reparent    survivors= []
    ARM=mutant_no_sweep     survivors= [26012]      <-- pids[2] = el NIETO

El unico superviviente del mutante es el nieto reparentado, que es la propiedad exacta que el negativo
dice medir -- no un generico "algo quedo vivo". Identico bajo el host hostil y bajo la politica nativa
de esta maquina, asi que el arreglo no altero la topologia del arbol que se mide.

## El control que hace discriminante la medicion

Esta maquina permite scripts de forma nativa: sin simular el host hostil, cualquier A/B aqui seria
vacuo (el codigo viejo tambien saldria verde). Simule la directiva con `PSExecutionPolicyPreference`
-- ambito Process, reversible, sin tocar la maquina -- y verifique el instrumento antes de usarlo.

    clone_pre (a30442c2^), host hostil -> SecurityError / UnauthorizedAccess /
                                          "process tree did not start"   EXIT 1
    clone     (a30442c2),  host hostil -> RESULT=PASS                    EXIT 0

Mismo estimulo, dos commits, dos respuestas opuestas. AC1 y AC2 acreditados.

## AC4: probado con dos causas independientes

Una sola causa no prueba una propiedad de clase, asi que rompi el arranque por dos vias:

- **de politica** (raiz sin la politica acotada): `missing_pid_files=['root.pid','child.pid','grand.pid']`,
  `root_returncode=1`, y el `SecurityError`/`UnauthorizedAccess` literal dentro del `AssertionError`. Exit 1.
- **que no es de politica** (nieto apuntando a un `.ps1` inexistente, con raiz e intermedio vivos):
  `missing_pid_files=['grand.pid']` y la causa exacta en
  `descendant_stderr={'grand.stderr': "El argumento 'grand_absent.ps1' ... no existe"}`. Exit 1.

Credito al maker: el `-RedirectStandardError` **no es decoracion**. En el segundo caso la causa real
solo existe ahi; sin esa redireccion el diagnostico se quedaria en "falta grand.pid" sin decir por que.

## Frontera respetada

Una sola hunk en `run_mailbox_retry_cases.py`, dentro de `run_complete_tree_kill_case`. No toca el
estimulo de TASK-0343 (TASK-0395), ni la asercion de `:2122` (TASK-0401), ni el workflow, ni
configuracion del runner. No me tope con el rojo intermitente de 0401.

## Residuales declarados (ninguno retiene el cierre)

- **R1 (recomiendo seguimiento con prioridad).** La rama de fallo se bloquea lo que vivan los
  descendientes supervivientes. Control de variable unica: mismo fallo, descendientes de 60s -> 60.5s;
  descendientes de 3s -> 10.4s, contra un deadline de 10s. `terminate()` mata solo la raiz y los
  descendientes heredaron los handles de sus pipes, asi que `communicate()` sin `timeout=` espera a que
  mueran solos. Hoy acotado a 60s porque los scripts se autoterminan; **si un descendiente futuro no lo
  hiciera, bloquea sin cota, el job muere por timeout y el diagnostico que AC4 acaba de construir no se
  imprime nunca** -- vuelve la clase de fallo que 0396 vino a matar. Arreglo de una linea.
- **R2.** La vacuidad se desplazo, no se elimino: si el arbol se levanta y muere antes de la probe, los
  dos controles pasan vacuamente y lo unico que salva la corrida es `assert len(mutant_survivors) == 1`,
  cuyo mensaje es el literal `[]`. La mitad vinculante de AC4 se cumple (exit 1); la de nombrar la causa,
  no. Cae fuera de la letra de AC4 ("no llega a levantarse"), por eso no lo cuento como incumplimiento.
- **R3.** `-ExecutionPolicy Bypass` fija el ambito Process, y la precedencia es
  `MachinePolicy > UserPolicy > Process`: un adoptante con directiva por GPO -- el escenario de empresa,
  justo NOVA -- sigue sin levantar el arbol. **AC2 bendice explicitamente esta via**, asi que no hay
  desviacion del maker; y AC4 convierte el residual en fallo **con nombre** en vez de mudo. La via robusta
  para GPO es la otra que AC2 admitia: no materializar `.ps1` (`-EncodedCommand` o stdin).
- **R4 (no es defecto).** El fixture sigue siendo solo-Windows, pero el sujeto tambien lo es
  (`Stop-LeaseProcessTree` en un harness de Windows PowerShell, job `runs-on: [self-hosted, protocol-win]`).
  Sobre tu angulo de portabilidad: **el arreglo si viaja en el eje que importaba**, que era heterogeneidad
  de politica de host, no de SO -- con la cota de R3, y sin tocar configuracion alguna.

Nota metodologica que registro porque casi me cuesta un falso hallazgo: `-ExecutionPolicy` escribe
`PSExecutionPolicyPreference` en el entorno y **los descendientes la heredan**, asi que el `Bypass` de
la raiz ya cubre el arbol y los de `child.ps1`/`grand.ps1` son redundantes (inofensivos, dejan cada
nivel autosuficiente). Mi primer AC4-b quitaba solo el del nieto: salio verde porque **la perturbacion
era vacua**, no porque hubiera un escape. Lo rehice con una causa real.

## Puertas (clon limpio @ a30442c2)

    check_falsification_contracts.py --inventory   exit 0
    validate_collaboration_state.py                exit 0
    scan_encoding.py                               exit 0
    scan_domain_neutrality.py                      exit 0
    protocol_state_drift                           has_drift=False

Estado canonico verificado en verde antes de empezar; sin claims activos sobre ninguna ruta.

-- Analista, 2026-08-16 00:52 local (UTC+2)
