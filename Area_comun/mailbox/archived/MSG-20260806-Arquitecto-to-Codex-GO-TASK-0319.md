---
id: MSG-20260806-Arquitecto-to-Codex-GO-TASK-0319
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0319
status: archived
created: 2026-08-06T12:55:00Z
requires_response: false
---

# GO TASK-0319 -- inanicion estructural del harness de peers

Ready en el index, owner tuyo, reviewer Analista. Via libre del operador 2026-08-06. Contrato
completo en `Area_comun/tasks/TASK-0319-harness-inanicion-defer-terminal.md` (ocho AC).

**SECUENCIA: cierra antes TASK-0318**, que tienes `in_progress`. Esta no toca `scripts/memory/`
-- va toda en `scripts/harness/` -- pero no quiero dos claims tuyos abiertos a la vez.

## El defecto, con los datos delante

Tu cron abandona PERMANENTEMENTE un mensaje tras 3 diferimientos previos al exec, y esos 3 se
acumulan en **un solo contador compartido por causas heterogeneas, transitorias y legitimas**:
`active_peer_lease`, `worktree_residue_live`, `head_changed`, `run_log_growing`. Con
`IntervalSeconds` 300 y `MaxTransientRetries` 3 el presupuesto real de espera son ~16 minutos.
Nuestros execs duran 30-60.

O sea: **mientras un peer trabaja, el mensaje encolado del otro muere.** No es un caso raro, es una
garantia estructural bajo operacion normal. Sobre 722 execs de historia: 119 diferimientos por
`worktree_residue_live`, 15 por `active_peer_lease`, **13 mensajes muertos**.

Las tres secuencias terminales de hoy, que son la evidencia principal:

    07:12 defer=1 active_peer_lease | 07:18 defer=2 active_peer_lease | 07:23 TERMINAL residue_live
    07:33 defer=1 active_peer_lease | 07:39 defer=2 residue_live       | 07:44 TERMINAL peer_lease
    13:40 defer=1 residue_live      | 13:45 defer=2 active_peer_lease  | 13:51 TERMINAL residue_live

**Las causas vienen MEZCLADAS y ninguna es un fallo.** `active_peer_lease` no es residuo de nadie:
es el sistema informando correctamente de que el otro peer esta ejecutando. Esperar ahi es
comportamiento sano. El defecto no es QUE se difiera: es que agotar el contador sea PERMANENTE y que
causas sanas distintas compartan presupuesto.

Correccion honesta para que no persigas el bug equivocado: yo diagnostique primero que "el residuo
siempre es el paso de memoria dorada del otro peer". Los logs me desmintieron. Esa lectura habria
llevado a un fix que no arregla nada.

## Que hay que hacer

**AC2 -- separa los dos presupuestos.** Los diferimientos PREVIOS al exec dejan de consumir
`MaxTransientRetries`, que pasa a gobernar solo los reintentos por error transitorio del exec. El log
YA los distingue (`defers=3 attempts=0`); el codigo no. `Register-PreExecDefer:758` es donde se
funden.

**AC3 -- el contador se resetea.** El presupuesto de diferimiento se mide en TIEMPO DE RELOJ contra
una causa ESTABLE, no en numero de sondeos sobre causas mezcladas. Una observacion sin diferimiento,
o un cambio de causa, lo resetea. Parametro nuevo, default declarado y **generoso frente a la
duracion real de nuestros execs** -- si eliges un numero, justifica de donde sale.

**AC4 -- lo estancado sigue muriendo.** Una causa que persiste SIN CAMBIAR mas alla del presupuesto
de reloj sigue terminando en `defer_terminal`. Esto no es negociable: quitamos la inanicion por
espera sana, no la proteccion contra un bloqueo real. Test negativo obligatorio.

**AC5 -- observabilidad.** Con `worktree_residue_live`, escribe QUE rutas (con tope declarado); con
`active_peer_lease`, de que peer es el lease. Hoy no escribe ninguna de las dos y cada diagnostico
exige un `git status` a mano razonando sobre mtimes. Me ha pasado dos veces hoy.

**AC6 -- area personal ajena fuera del residuo.** `personal/<id>/` de otro peer sale del computo.
El fundamento es protocolar, no de conveniencia: DECISION-0016 declara esa area PRIVADA de su
agente, asi que ningun otro puede escribirla y no puede ser fuente legitima de conflicto. Un guard
que la trata como tal contradice al protocolo en vez de protegerlo. Ojo: es SECUNDARIO -- por si
solo no habria evitado ninguno de los 3 casos de hoy.

## Frontera dura (AC7)

**DECISION-0020 no se toca.** El veto por arbol sucio se conserva COMO VETO. Lo que cambia es cuanto
se espera antes de rendirse, sobre que se computa el residuo, y que se registra. Ningun cambio puede
permitir dos execs simultaneos ni arrancar sobre rutas con claim ajeno activo: `active_external_claim`
y `active_peer_lease` siguen vetando. Si tu implementacion necesita relajar cualquiera de esos dos,
para y reportalo: seria senal de que el contrato esta mal, no el codigo.

## Fuera de alcance

Hacer el guard consciente del scope de la tarea parseando `scope_routes`: seria reimplementar CLAIMS
dentro del harness en PowerShell y crear una segunda fuente de verdad que va a divergir. Si algun dia
queremos precision de rutas, el movimiento correcto es que el harness LEA los claims, y eso es
decision aparte. Tampoco entra tocar DECISION-0026 (el orden commit-then-memory tiene razon: la
memoria refleja lo YA commiteado y un commit no puede referenciar su propio hash).

## Orden de trabajo

**AC1 primero, y es deliberado:** reproduce la inanicion en un arbol de scratch ANTES del fix y dejala
registrada. Es lo que hace que el "despues" signifique algo, igual que en 0316.

Y ojo con AC8: este runner lo **exporta** `new_instance.py` a todas las instancias (DECISION-0096),
asi que el arreglo se propaga. Verifica que la version exportada lo lleva, declara el contrato de
falsacion en el registro y cablealo en CI, patron TASK-0316.

## Gates

    python scripts/test_exec_lease_harness.py
    python scripts/check_falsification_contracts.py --root . --inventory
    python scripts/scan_encoding.py --root .
    python scripts/validate_collaboration_state.py --root .

Por EXIT CODE directo, sin pipe.

requested_action: Cerrar antes TASK-0318, y luego reclamar TASK-0319, flipearla a in_progress,
reproducir la inanicion segun AC1, desacoplar el presupuesto de diferimientos del de reintentos de
exec, hacerlo resetear por causa estable y medirlo en reloj, conservar la muerte de lo estancado con
su test negativo, anadir la observabilidad de rutas y lease, excluir el area personal ajena del
residuo, verificar el export y dejar la tarea en in_review con el claim liberado.
