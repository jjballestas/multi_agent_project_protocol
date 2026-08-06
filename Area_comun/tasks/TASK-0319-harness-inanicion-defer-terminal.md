---
task_id: TASK-0319
file: Area_comun/tasks/TASK-0319-harness-inanicion-defer-terminal.md
title: "Inanicion estructural del harness: un exec largo de un peer mata para siempre la cola del otro (contador de defers unico sobre causas transitorias legitimas)"
status: review_approved
type: refactor
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - DECISION-0020
  - DECISION-0016
  - DECISION-0026
  - DECISION-0096
created_at: 2026-08-06
intake:
  type: fix
  goal: >
    El cron generico de peers abandona PERMANENTEMENTE un mensaje tras 3 diferimientos previos al
    exec, y esos 3 diferimientos se acumulan en UN SOLO contador compartido por causas HETEROGENEAS,
    TRANSITORIAS y LEGITIMAS (`active_peer_lease`, `worktree_residue_live`, `head_changed`,
    `run_log_growing`). Con `IntervalSeconds` 300 y `MaxTransientRetries` 3, el presupuesto efectivo
    es de unos 16 minutos de espera; nuestros execs reales duran 30-60 minutos. Consecuencia
    estructural, no accidental: **mientras un peer trabaja, el mensaje encolado del otro muere**, y
    revivirlo exige intervencion manual sobre `*.retry.json`. Medido sobre 722 execs de historia: 119
    diferimientos por `worktree_residue_live`, 15 por `active_peer_lease` y **13 mensajes muertos**.
    En los 3 casos terminales del 2026-08-06 las causas venian MEZCLADAS -- ninguna era un fallo,
    todas eran el sistema funcionando: el peer tenia lease activo o estaba escribiendo.
  acceptance:
    - "AC1 (falsacion antes del fix): sobre un arbol de scratch se reproduce la inanicion -- un peer con lease activo y escrituras continuas durante mas de 16 minutos hace que el mensaje encolado del otro pase a exhausted/defer_terminal. Queda registrado como evidencia de partida, no como suposicion."
    - "AC2 (el presupuesto de defer se desacopla del de reintentos de exec): los diferimientos PREVIOS al exec dejan de consumir MaxTransientRetries, que pasa a gobernar solo los reintentos por error TRANSITORIO del exec (el campo attempts). El log ya los distingue (defers vs attempts); el codigo debe distinguirlos tambien."
    - "AC3 (el contador se resetea cuando la causa cambia o desaparece): el presupuesto de diferimiento se mide en TIEMPO DE RELOJ contra una causa ESTABLE, no en numero de sondeos sobre causas mezcladas. Una observacion sin diferimiento, o un cambio de causa, resetea el contador. Parametro nuevo con default declarado y generoso frente a la duracion real de nuestros execs."
    - "AC4 (lo estancado sigue muriendo): una causa que persiste sin cambiar mas alla del presupuesto de reloj SIGUE terminando en defer_terminal. El fix elimina la inanicion por espera sana, no la proteccion contra un bloqueo real. Test negativo obligatorio que lo demuestre."
    - "AC5 (observabilidad): cuando la causa es worktree_residue_live el log escribe QUE rutas lo provocan (acotadas a un maximo declarado); cuando es active_peer_lease escribe de que peer es el lease. Hoy no escribe ninguna de las dos y cada diagnostico exige un git status manual y razonar sobre mtimes."
    - "AC6 (area personal ajena fuera del computo de residuo): personal/<id>/ de un peer distinto al propio se excluye del calculo de residuo. Fundamento protocolar, no conveniencia: DECISION-0016 declara esa area PRIVADA de su agente, asi que ningun otro puede escribirla y no puede ser fuente legitima de conflicto. Un guard que la trata como tal contradice al protocolo en vez de protegerlo."
    - "AC7 (la garantia de escritor-unico NO se debilita): DECISION-0020 sigue intacta. El veto por arbol sucio se conserva como veto; lo que cambia es cuanto tiempo se espera antes de rendirse, sobre que se computa el residuo, y que se registra. Ningun cambio permite a dos execs correr a la vez ni a un exec arrancar sobre rutas con claim ajeno activo: active_external_claim y active_peer_lease siguen vetando."
    - "AC8 (paridad y export): el fix es del runner generico scripts/harness/peer_mailbox_cron.ps1, que DECISION-0096 exporta a las instancias, asi que se verifica que la version exportada por new_instance.py lo lleva. Contrato de falsacion declarado en el registro y cableado en CI, patron TASK-0316."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root . --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/harness/README.md
    - scripts/test_exec_lease_harness.py
  out_of_scope: >
    Hacer el guard consciente del scope de la tarea parseando scope_routes: seria reimplementar
    CLAIMS dentro del harness en PowerShell y crear una segunda fuente de verdad que divergira. Si
    algun dia se quiere precision de rutas, el movimiento correcto es que el harness LEA los claims,
    y eso es decision propia. Tampoco entra: tocar DECISION-0026 para fundir el paso de memoria con
    el commit de entrega (el orden tiene razon: la memoria refleja lo YA commiteado); relajar
    active_external_claim; ni cambiar el ciclo de vida de tareas.
  risk: medium
  estimate: M
notes: >
  Diagnostico corregido sobre la marcha por los datos, y conviene que quede escrito porque la
  primera lectura era peor: el Arquitecto reporto al operador que "el residuo siempre es el paso de
  memoria dorada del otro peer". Las secuencias de defer del log lo desmienten -- en los 3 casos
  terminales del dia las causas venian MEZCLADAS (`active_peer_lease` y `worktree_residue_live`
  alternandose), y `active_peer_lease` no es residuo de nadie: es el sistema informando
  correctamente de que el peer esta ejecutando. El defecto no es QUE se difiera, es que un unico
  contador de 3 sondeos se comparta entre causas sanas distintas y que agotarlo sea PERMANENTE.
  El area personal ajena (AC6) sigue siendo correcta de excluir, pero es secundaria: no habria
  evitado ninguno de los 3 casos por si sola.
  Prioridad alta porque la inanicion se agrava justo cuando mas se coordina: cuanto mas largos los
  execs y mas paralelos los peers, mas probable es perder mensajes. Con 0317 y 0318 en vuelo ha
  bloqueado dos veces en un solo dia.
