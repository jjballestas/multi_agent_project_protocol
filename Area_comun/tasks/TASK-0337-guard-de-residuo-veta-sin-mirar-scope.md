---
id: TASK-0337
title: El guard de residuo veta sin mirar scope -- gemelo de TASK-0331
status: review_approved
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    El guard pre-exec de residuo decide sobre la suciedad del arbol COMPLETO, no sobre si las rutas
    sucias intersectan lo que el mensaje diferido necesita. Es el mismo defecto de ceguera de scope
    que TASK-0331 corrige en la admision de claims, en un guard hermano del mismo fichero.
    Inventariar TODOS los vetos pre-exec, declarar para cada uno sobre que liga hoy y sobre que
    deberia ligar, y corregir los que vetan por una propiedad global cuando la decision es por-par.
  acceptance:
    - "Inventario COMPLETO de los vetos pre-exec del harness, uno por uno, con lo que liga cada uno hoy y si su alcance es correcto; el inventario se entrega aunque solo uno resulte defectuoso."
    - "Medido: un mensaje cuyo trabajo NO intersecta las rutas sucias deja de ser diferido, y un mensaje cuyo trabajo SI las intersecta sigue siendolo."
    - "Declarado explicitamente que garantiza el guard tras el cambio, incluida la frontera que deja de cubrir si la hay."
    - "Negativo permanente nuevo que MUERA ante el mutante de codigo muerto, no solo ante la ausencia del fichero."
    - "Sin regresion en lo ya probado del harness, en particular la admision atomica y el ciclo de vida de leases de TASK-0331."
    - "AC6 (ANADIDO 2026-08-15 por la enmienda, y es el que mas pesa): el DEADLOCK CIRCULAR muere,
      REPRODUCIDO. Se construye el caso exacto que midio NOVA -- el peon termina su exec dejando su
      propia `personal/<Peer>/MEMORY.md` sin commitear -- y se comprueba por conducta que su siguiente
      mensaje ARRANCA en vez de diferirse contra el reloj de 7200 s. Se acredita con el par: el caso
      del deadlock arranca, y un residuo AJENO de verdad sigue difiriendo. Un arreglo que abra la
      puerta a todo residuo no es arreglo."
    - "AC7 (el fallo deja de ser mudo): cuando el guard difiera, el log dice QUE ruta sucia intersecta
      QUE ruta del mensaje. Hoy emite `RETRY_DEFER reason=worktree_residue_live` sin distinguir un
      solape real de un residuo del propio peon, y por eso costo intervencion humana detectarlo."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El ciclo de vida de leases de TASK-0331: si el arreglo lo toca, se declara y se coordina, no se absorbe."
    - "Cualquier cambio en el umbral de poda o en el driver de peso de mailbox (RES-11)."
    - "Codigo de producto."
  amendment_20260815: >
    ENMIENDA 2026-08-15 (Arquitecto), con la medicion de campo de la instancia NOVA -- primer uso
    real de la metodologia de principio a fin. El defecto es PEOR de lo que esta tarea enunciaba: no
    solo veta sin mirar scope, sino que puede producir un **DEADLOCK CIRCULAR SIN SALIDA POR DISENO**.
    Mecanismo medido alli: el ciclo del peon termina con ultimo commit -> el harness escribe
    `personal/<Peer>/MEMORY.md` -> el exec muere, dejando esa memoria SIN COMMITEAR. El guard la ve
    como residuo (`Get-StagedResidueState` cuenta el area personal del PROPIO peon:
    `$candidateIsRelevant = ... -or $Matches[1] -ieq $PeerId`). Y como un peon solo commitea DENTRO
    de un exec, y no puede arrancar uno por ese residuo, no hay salida: en NOVA seis GO encolados
    murieron en `RETRY_DEFER reason=worktree_residue_live` con
    `paths_json=["Aegis/personal/Codex/MEMORY.md"]` -- su PROPIO fichero -- y hubo que romperlo con
    intervencion humana. Confirmado tambien en el hub: el 2026-08-15 la remediacion r2 de TASK-0378
    difirio con `personal/Codex/MEMORY-*` en su `paths_json`. Lo grave es el SILENCIO: peones vivos,
    heartbeats latiendo, ledger verde, validate y encoding en 0, y la cola muriendose sola contra un
    reloj de 7200 s; la unica senal esta en el log del cron, que nadie mira cuando todo lo demas dice
    que va bien. Arreglos por orden de calidad, tal como los formula NOVA: (1) que el ciclo del peon
    TERMINE con el arbol limpio -- commitear su memoria DENTRO del exec, antes de soltar el lock --,
    que elimina la causa; (2) que el guard ignore `personal/<peer>/**` DEL PROPIO peon que va a
    ejecutar; (3) minimo aceptable: que el deadlock sea DETECTABLE -- si el unico residuo pertenece al
    peon que va a ejecutar, no diferir, o emitir una linea distinta que lo nombre. El AC de esta tarea
    se amplia: debe acreditarse que el caso del deadlock circular MUERE, reproducido.
  risk: medium
  estimate: M
---

# TASK-0337 -- el guard de residuo veta sin mirar scope

## El hecho medido

Hoy 2026-08-08, con Codex ejecutando la remediacion 4 de TASK-0331, el cron del Analista difirio
`MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0329-r2`:

    09:24:15 RETRY_DEFER defer=1 reason=worktree_residue_live
             paths=["Area_comun/state/*.json", "Area_comun/tasks/TASK-0331-*.md",
                    "runtime/state/events.jsonl", "runtime/state/snapshot.json",
                    "personal/Analista/drafts/DRAFT-MSG-0258-rejuicio-GO.md"]

**El mensaje diferido es de TASK-0329. Ninguna de las rutas sucias pertenece a TASK-0329.**

## El defecto

`Get-StagedResidueState` (`scripts/harness/peer_mailbox_cron.ps1:775`) toma el `git status`
porcelain del repositorio entero. El unico filtro que aplica es por area personal ajena
(`^personal/<otro>/`). Despues devuelve un veredicto GLOBAL -- `none` / `live` / `aborted` --
y el llamador (`:1274`) difiere el mensaje sea cual sea su trabajo.

No existe comparacion alguna entre las rutas sucias y las rutas que el mensaje necesita.

## Por que es el gemelo de TASK-0331

TASK-0331 se titula *claim ajeno veta sin mirar scope*. Es literalmente el mismo defecto en el
guard de al lado, en el mismo fichero: **una decision que es por-par (este mensaje contra estas
rutas) tomada sobre una propiedad global (el arbol esta sucio)**. Cerrar la admision de claims no
cerro la familia. Esto es lo que hace el hallazgo interesante y no un bug suelto.

## Lo que NO doy por sentado

No prescribo el arreglo, y hay una tension real que el inventario debe resolver antes de tocar nada:

- Un revisor que **clona limpio desde HEAD** es indiferente al arbol sucio: para el, el veto sobra
  casi siempre.
- Un agente que trabaja **en el arbol vivo** si necesita el veto.

Asi que "hacerlo scope-aware" puede ser correcto para un consumidor e incorrecto para otro. Quiero
el inventario y la propuesta razonada ANTES del parche, y quiero declarado a que consumidor sirve
cada veto.

## Direccion e impacto, sin inflarlo

**No corrompe y falla CERRADO**: bloquea de mas, nunca de menos. El presupuesto real es de 7200 s
por razon, y la razon al cambiar reinicia el reloj, asi que un exec normal de 20-40 min no lo agota.
El dano aparece cuando un peer deja trabajo sin commitear durante horas -- **paso tres veces en la
jornada del 7 al 8 de agosto**, cada una por una tarea que un peer dejo `blocked` con residuo, y las
tres las desbloquee yo a mano commiteando su trabajo. Ese es el coste que justifica la tarea, no el
diferimiento de hoy, que se resolvera solo.

## Secuenciacion -- importa

**No se rutea hasta que TASK-0331 cierre.** Comparte fichero con ella y Codex lo tiene modificado
ahora mismo. Contratarla ya es para que no se pierda; ejecutarla en paralelo es fabricar un conflicto.

## REFUERZO DE EVIDENCIA -- 2026-08-16 (Arquitecto)

El AC6 de esta tarea se escribio sobre el caso que midio NOVA. **Se ha reproducido DOS VECES en el
hub el 2026-08-15**, y las dos las rompio el Arquitecto commiteando a mano la memoria del peon:

    ~19:35  GO de TASK-0396 -> RETRY_DEFER reason=worktree_residue_live
            paths_json incluye personal/Codex/MEMORY-*.md (7 ficheros) -- suyos
    ~00:30  el mismo patron tras la entrega de TASK-0396

Y una TERCERA forma que el AC6 no nombra y conviene que el arreglo cubra: **el residuo de un peon
difiere al OTRO**. El 2026-08-16, la review de TASK-0396 al Analista estuvo **30 minutos** sin
consumirse, difiriendo primero por `active_external_claim` (los claims de Codex sobre 0397) y luego
por `worktree_residue_live` (el arbol sucio de Codex). Quien genera el residuo no es quien paga el
bloqueo, que es la razon por la que el incentivo no lo corrige solo.

Dato que acota el arreglo: **pedirselo al peon en el texto del encargo FUNCIONA** -- se hizo en el GO
de TASK-0397 y esa vez commiteo su memoria dentro del exec. Pero eso es disciplina por mensaje, no
propiedad del sistema: se cae en cuanto un encargo no lo diga.

**NO se abre tarea aparte para esto** (se evaluo TASK-0406 y se descarto por duplicar AC6/AC7). Lo que
SI sale aparte es el ancla del regex, que es un defecto distinto: **TASK-0405**.

## Inventario implementado de vetos pre-exec (Codex, 2026-08-16)

| Veto | Liga antes del cambio | Liga tras el cambio | Alcance |
|---|---|---|---|
| `residue_probe_failed` | Lectura global del worktree | Igual | Correcto: no hay prueba fiable para decidir. |
| `worktree_residue_live` | Cualquier residuo relevante del repositorio | Solo cada par ruta sucia-ruta del mensaje; `personal/<Peer>/**` propio no veta | Corregido: la decision es por-par. |
| `message_scope_ambiguous` | Mensaje sin scope resoluble | Igual, dentro de la reserva | Correcto: falla cerrado si no puede construirse el par. |
| `claims_unreadable` / `active_external_claim` | Ledger global ilegible; claim externo global o intersectante | Igual | Correcto: ilegibilidad falla cerrada; claim resoluble liga por interseccion. |
| `peer_lease_unreadable` / `active_peer_lease` | Lease global ilegible; lease vivo global o intersectante | Igual | Correcto: ilegibilidad falla cerrada; lease resoluble liga por interseccion. |
| `exec_admission_busy` / `own_lease_exists` | Reserva atomica global o lease propio existente | Igual | Correcto: protegen exclusion mutua, no rutas de trabajo. |
| `ledger_unreadable_before_exec` / `ledger_prefix_snapshot_failed` | Baseline global de evidencia | Igual | Correcto: sin baseline no se puede atribuir evidencia al exec. |
| `index_snapshot_failed` / `untracked_snapshot_failed` | Snapshot global de rollback | Igual | Correcto: sin snapshot no hay rollback no destructivo demostrable. |

Garantia tras el cambio: un mensaje con scope resoluble solo es diferido por residuo vivo si al menos
una ruta sucia no propia intersecta una ruta material de su scope. El detalle registra el par exacto
como `dirty_path` y `message_route`. La memoria privada del mismo peer no participa y por ello no puede
cerrar circularmente la entrada a su siguiente exec. Una ruta ajena que si intersecta conserva el veto.
La frontera deliberada permanece cerrada: si el scope del mensaje no es resoluble, el flujo no usa la
ausencia de interseccion como permiso; y un fallo de lectura del worktree conserva el veto global.

La exencion deriva el prefijo que Git usa para la raiz de la instancia. El contrato permanente ejecuta
el mismo par en dos layouts: instancia en la raiz del repositorio (prefijo vacio) e instancia anidada
(prefijo no vacio). En ambos, la memoria propia arranca y el residuo ajeno que intersecta sigue
difiriendo con el par exacto en el diagnostico.

## Correccion de paridad del gemelo PowerShell (Codex, 2026-08-16)

El inventario efectivo de Python ubica la identidad vigilada de
`scripts/harness/peer_mailbox_cron.ps1` en la linea 1515. El valor 1502 citado en el ACTION era una
coordenada intermedia anterior al revert posterior; el escaneo del arbol vivo demostro que 1515 es
la coordenada actual. El gemelo PowerShell se sincroniza de 1474 a 1515.

Censo medido desde los dos inventarios efectivos, despues del arreglo puntual:

- Python: 82 exenciones indexadas por numero de linea.
- PowerShell: 82 exenciones indexadas por numero de linea.
- Divergencias restantes: 1. En `scripts/harness/peer_mailbox_cron.ps1:553`, Python declara los
  digests `_EXEMPT_TERM_1` y `_EXEMPT_TERM_6`, mientras PowerShell declara solo el primero.

Negativo de paridad: insertar una linea antes de la ocurrencia vigilada la movio temporalmente de
1515 a 1516. Ambos gemelos salieron 1 y emitieron exactamente
`scripts/harness/peer_mailbox_cron.ps1:1516: Codex`. El fichero vigilado se restauro byte a byte
despues de la prueba; la unica implementacion persistente de esta correccion es la coordenada del
inventario PowerShell.
