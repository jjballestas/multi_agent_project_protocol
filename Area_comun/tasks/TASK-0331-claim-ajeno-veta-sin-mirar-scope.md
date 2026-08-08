---
task_id: TASK-0331
file: Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md
title: "Exclusion mutua total entre agentes: un claim ajeno vivo veta sin mirar scope Y una lease de exec ajena veta sin condicion alguna, asi que maker y checker no pueden trabajar nunca a la vez"
status: in_review
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0319
  - TASK-0321
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    `Get-AdditionalWorkSignal` en `peer_mailbox_cron.ps1` recorre `CLAIMS.json` y devuelve
    `active_external_claim` en cuanto encuentra UN claim vivo de otro owner. No compara `scope`, ni
    `task_id`, ni ruta alguna. Consecuencia: mientras Codex sostiene un claim sobre TASK-0322, el
    Analista no puede ejecutar NINGUN mensaje -- ni siquiera la review de TASK-0324, otra tarea, sin
    una sola ruta en comun.
    Eso serializa por completo al maker y al checker. El ciclo de dos capas existe precisamente para
    que el checker revise la tarea N mientras el maker construye la N+1; con este guard se alternan
    en vez de solaparse, y como los claims del maker duran lo que dura una implementacion (30-70 min
    medidos esta noche), el checker pasa ese tiempo parado.
    El propio DECISION-0020 formula la regla CON alcance -- "el peer no tiene claim activo sobre las
    rutas" -- asi que el guard es MAS ESTRICTO que la politica que implementa. No hay que cambiar la
    politica: hay que implementarla como esta escrita.
    Medido en los logs: 12 diferimientos por esta causa en el cron del Analista frente a 1 en el de
    Codex. La asimetria es la esperada -- el que revisa es el que paga el peaje.
    **Y hay un SEGUNDO veto, mas absoluto todavia.** La misma funcion recorre las leases de exec y
    devuelve `active_peer_lease` si CUALQUIER lease ajena tiene proceso vivo, sin mirar tarea, ruta
    ni nada. Medido en vivo 2026-08-07: liberado el claim de 0322, el Analista paso de
    `active_external_claim` a `active_peer_lease detail=peer=Codex` y siguio bloqueado. Con este
    veto, el checker no puede ejecutar mientras el maker ejecute -- y como el maker suele tener cola,
    la exclusion es practicamente permanente. El ciclo de dos capas queda estrictamente secuencial.
    El veto de lease es el que de verdad manda: el de claim ni siquiera llega a notarse cuando hay
    un exec vivo.
    **Y el veto NO es un lock: es un check-then-act sin atomicidad.** Medido 2026-08-07: los dos
    peers emitieron `EXEC_START` en el MISMO SEGUNDO (08:59:34, pids 76572 y 55112) con dos
    `exec-lease.json` vivas a la vez. Ambos leyeron "no hay lease ajena", ambos escribieron la suya,
    ambos arrancaron. No hay lock, ni compare-and-swap, ni orden. De modo que el guard es
    ESTRICTO DE MAS cuando los peers llegan escalonados y NO GARANTIZA NADA cuando llegan juntos:
    paga el coste completo de la exclusion mutua sin entregar la garantia. Si alguna parte del
    sistema se apoya en esa exclusion para la seguridad del ledger (la anti-colision de
    DECISION-0020), la garantia es ilusoria.
  acceptance:
    - "AC1 (falsacion previa): se reproduce que un claim ajeno SIN interseccion de rutas con el trabajo del mensaje produce active_external_claim, y se declara con la traza que lo demuestra (residua ya excusada y defer por el claim solo)."
    - "AC2 (el guard pasa a mirar el scope): un claim ajeno vivo veta solo si su scope interseca las rutas que el mensaje va a tocar. La comparacion es por ruta, con el mismo criterio de normalizacion que ya usa el resto del harness."
    - "AC2b (la lease ajena deja de ser veto incondicional): una lease de exec ajena viva veta solo si el trabajo que ampara interseca el del mensaje. Si no se puede determinar que ampara -- lease sin tarea declarada, ilegible o ambigua -- SIGUE VETANDO (mismo criterio fail-closed del AC3). Se declara por medicion cuanto tiempo de solape recupera el ciclo."
    - "AC3 (fail-closed en toda duda, INNEGOCIABLE): un claim sin scope, con scope vacio, ilegible o no parseable SIGUE VETANDO. Un claim malformado no puede convertirse en permiso. Test negativo por cada una de esas cuatro formas."
    - "AC4 (la asimetria deliberada se conserva): la ausencia de claims NUNCA es permiso para saltarse el veto de arbol sucio -- es lo que dice el comentario de la funcion y debe seguir siendo cierto. Test que lo fije."
    - "AC4b (la carrera de arranque simultaneo, INDEPENDIENTE del scope): dos peers que sondean en el mismo tick no deben poder arrancar los dos. Se reproduce primero la carrera (dos EXEC_START en el mismo segundo con dos leases vivas) y luego se cierra con una adquisicion ATOMICA de la lease -- creacion exclusiva del fichero, o el primitivo equivalente del sistema -- no con una relectura. Un guard que solo LEE nunca excluye."
    - "AC4c (declarar el alcance real de la garantia): el handoff declara EXPLICITAMENTE que garantiza el mecanismo tras el arreglo y que no. Si tras 0331 dos peers pueden seguir escribiendo el ledger a la vez por diseno, se dice; si no pueden, se demuestra. Lo que no puede quedar es la ambiguedad actual, donde el guard aparenta una exclusion que no da."
    - "AC5 (contrato): negativo permanente que caiga si el guard deja pasar con un claim ajeno que SI interseca, y otro que caiga si veta con uno que no interseca; ambos verificados por MUTACION y cableados en CI."
    - "AC6 (sin regresion): suite del harness y gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/test_scan_domain_neutrality.py"
    - "powershell scripts/scan_domain_neutrality.ps1 -Root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca el veto de arbol sucio ni la clasificacion live/aborted de residuas, que funcionan
    bien. No se toca DECISION-0020 -- esta tarea acerca la implementacion a la politica, no la
    politica a la implementacion. No se tocan las leases de exec.
  risk: high
  estimate: M
---

# TASK-0331 -- el guard serializa a los dos agentes

## Lo medido (2026-08-07)

    07:13:41  RETRY_TRANSIENT reason=staged_residue_aborted age_minutes=5     <- residua excusada
    07:13:41  RETRY_DEFER     reason=active_external_claim                    <- y aun asi difiere

La segunda linea sale inmediatamente despues de la primera: con el arbol ya excusado, lo unico que
bloqueaba era el claim de Codex sobre TASK-0322, una tarea distinta de la que el mensaje pedia
revisar. Evidencia por comportamiento, no por lectura del codigo.

    defers por claim ajeno, cron del Analista    12
    defers por claim ajeno, cron de Codex         1

## Por que esto no es una urgencia pero si un impuesto

Falla CERRADO: bloquea trabajo, no lo corrompe, y el diferimiento tiene 7200 s de margen antes de
volverse terminal. Ese margen protege causas transitorias; no protege una ambiguedad estructural,
que llega a terminal y exige rearme manual. Por la regla de direccion del fallo que gobierna este
hilo, eso lo situa por debajo de los residuales que fallan abiertos, pero no autoriza afirmar que
ningun mensaje se pierde.

Pero se cobra el solape entero entre maker y checker, que es la premisa de rendimiento del ciclo de
dos capas. Y explica algo que yo venia leyendo mal: al Analista ocioso mientras Codex trabaja lo
interpretaba como "no hay nada que revisar", y en parte era este veto.

## La linea que NO se puede cruzar

El comentario de la funcion dice que la ausencia de claims "nunca se usa como permiso para saltarse
el veto de arbol sucio". Esa asimetria es deliberada y correcta: el guard puede ser mas estricto que
las senales, nunca mas laxo. El AC3 la extiende a lo que toca esta tarea -- un claim ilegible,
vacio o sin scope sigue vetando. Convertir un claim malformado en permiso seria cambiar un guard
que falla cerrado por uno que falla abierto, exactamente el defecto que estamos corrigiendo en el
resto del arbol esta noche.

## Riesgo declarado (high)

Es un guard de anti-colision: relajarlo mal reintroduce escrituras concurrentes del ledger, que
es el fallo que DECISION-0020 existe para evitar. Por eso AC3 es innegociable y el criterio ante
cualquier ambiguedad es VETAR. La direccion del fallo hoy es CERRADA (bloquea, no corrompe), asi
que el arreglo no debe convertirla en abierta a cambio de rendimiento: si el checker no logra un
criterio de interseccion que le convenza, es preferible dejar el veto como esta y declararlo.

## Remediacion 1 (2026-08-08)

- `Clear-StaleCronLockIfSafe` selecciona `reservation_deadline` para una lease en
  `state=reserved`; una reserva sin `deadline` y sin proceso vivo ya se elimina junto con el lock.
  `NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` mata el mutante que vuelve a leer el deadline de running.
- La resolucion de trabajo consulta `TASK_INDEX.json` y `TASK_INDEX_ARCHIVE.json` como una sola
  poblacion. `NEG-HARNESS-ARCHIVED-TASK-WORK-RESOLUTION` mata el mutante que consulta dos veces el
  indice caliente y deja de resolver una tarea archivada.
- Una ruta declarada con `*`, `?`, `[` o `]` no se interpreta como literal ni como glob: el scope
  queda ambiguo y veta. `NEG-HARNESS-GLOB-SCOPE-FAILS-CLOSED` mata el mutante que elimina ese veto.
- `NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` ahora ejecuta el camino real: con residuo live
  no llama a admision; un mutante que mantiene el texto del guard pero vuelve limpio el estado si
  alcanza la admision y muere.

Frontera explicita: un mensaje sin `task_id` valido, sin tarea en ninguno de los dos indices, sin
fichero de tarea o sin `scope_routes` resoluble conserva `message_scope_ambiguous`. Esa causa no se
disuelve por tiempo: tras el presupuesto de defer llega a `defer_terminal` y el mensaje no se
ejecuta hasta rearme manual. El arreglo evita esa perdida para tareas podadas al archivo, no para
mensajes estructuralmente irresolubles.

Medicion honesta del solape: el log observado por el checker da un techo atacable de 255,2 minutos
(4 h 15 min, 60 por ciento de 422,2 minutos diferidos). No demuestra que todo ese techo se recupere:
solo el subconjunto con scopes declarados y disjuntos puede solaparse. El arbol Git y `.git/index`
siguen siendo recursos compartidos no declarados en `scope_routes`; el veto de arbol sucio es una
sonda previa y no una exclusion de vida completa. Las escrituras del ledger siguen serializadas por
el lock real de `submit_intent` en esta instancia authoritative.

Remediacion 2: el autocurado ya no depende de que exista el lock ni intenta parsear un deadline
cuando ningun proceso posee la lease. La publicacion crea el lock antes que la lease y la limpieza
borra la lease antes que el lock. El negativo permanente ejecuta tres rearranques sobre los cuatro
estados exigidos: `reserved` sin lock, lease truncada con lock, lease vacia con lock y `reserved`
sin `reservation_deadline`; todos convergen en el primer rearranque y permanecen limpios. La
garantia de resolucion de tareas archivadas queda limitada a contratos con `scope_routes`: la
medicion del checker recupero 228 de 1.033 mensajes y encontro 272 de 365 contratos archivados sin
esa declaracion.

Remediacion 3: las publicaciones de lease running y cada latido reemplazan el JSON mediante un
fichero temporal en el mismo directorio, de modo que un lector ve la version completa anterior o
la completa nueva. El autocurado reintenta una lectura ilegible tres veces y despues solo elimina
la lease si una identidad de proceso parseable demuestra que el dueno no vive. Si el dueno vive o
la liveness sigue siendo desconocida, conserva lease y lock y emite
`SELF_HEAL_UNREADABLE_LEASE` con `liveness=live|unknown action=preserve`; una huerfana demostrada
emite `SELF_HEAL_ORPHAN_LEASE liveness=dead action=remove`. El lock publica identidad PID+start de
su supervisor durante la reserva y del proceso hijo desde su arranque; ademas, una segunda instancia
sale por el guard de PID antes de intentar autocurado. El negativo permanente usa procesos reales:
preserva leases truncada, vacia y sin deadline de un dueno vivo, y mata el mutante que vuelve a leer
`deadline` en vez de `reservation_deadline`. Frontera: una lease ilegible sin evidencia parseable de
dueno se conserva deliberadamente; falla cerrado y requiere intervencion en vez de arriesgar borrar
un exec vivo.

## Remediacion 4 - tabla normativa de estados

Regla de oro: ante duda real, ni borrar ni dejar pasar. El autocurado preserva la lease y publica
`SELF_HEAL_MANUAL_RECOVERY_REQUIRED`; si no habia lock, crea un marcador de recuperacion atomico.
El guard del peer trata la lease como ocupada. `dead` significa muerte demostrada por una identidad
PID + start-time; ausencia de identidad o fallo al leer start-time es `unknown`, nunca `dead`.

La columna `dueno` enumera el estado fisico pedido para completar el producto cartesiano. La accion
se gobierna por el resultado trivaluado de la mejor evidencia util entre lease y lock. Con lease
ilegible/0 bytes/sin identidad y lock ausente, ese resultado necesariamente es `unknown`, aunque el
estado fisico sea live o dead. Esas filas convergen deliberadamente en la misma accion segura: no
se borra por conjetura y queda bloqueado con senal explicita para intervencion.

Convenciones de respuesta del guard: `scope` significa `active_peer_lease` solo si el scope legible
interseca (trabajo legible y disjunto puede solaparse); `busy` significa veto fail-closed
`peer_lease_unreadable`; `none` significa que no veta. Para `dead`, la respuesta anterior al
autocurado solo puede ser `none` si la lease legible trae identidad util; las otras formas quedan
`busy` hasta que el autocurado respaldado por el lock las retire. Despues de retirar, siempre `none`.

| lease | dueno | lock | autocurado | guard antes -> despues | porque |
|---|---|---|---|---|---|
| legible | live | presente | preservar | scope -> scope | La identidad util prueba vida; solo el scope decide solape. |
| legible | live | ausente | preservar | scope -> scope | La lease basta para probar vida. |
| legible | dead | presente | retirar lease+lock | none -> none | La identidad util prueba muerte. |
| legible | dead | ausente | retirar lease | none -> none | La lease basta para probar muerte. |
| legible | unknown | presente | preservar | busy -> busy | No hay certificado de muerte. |
| legible | unknown | ausente | preservar+marcador | busy -> busy | El marcador evita arranque propio y el guard veta. |
| ilegible | live | presente | preservar | busy -> busy | El lock prueba vida; la lease no permite scope seguro. |
| ilegible | live | ausente | preservar+marcador | busy -> busy | Sin evidencia observable se clasifica unknown y no se arriesga. |
| ilegible | dead | presente | retirar lease+lock | busy -> none | Solo el lock puede probar muerte. |
| ilegible | dead | ausente | preservar+marcador | busy -> busy | Muerte real sin evidencia observable no autoriza borrar. |
| ilegible | unknown | presente | preservar | busy -> busy | Lock no util y lease no legible: duda real. |
| ilegible | unknown | ausente | preservar+marcador | busy -> busy | Duda real sin lock: se hace visible y bloqueante. |
| 0 bytes | live | presente | preservar | busy -> busy | Vacio es ilegible, no ausencia de lease. |
| 0 bytes | live | ausente | preservar+marcador | busy -> busy | Vacio sin evidencia sigue siendo ocupacion dudosa. |
| 0 bytes | dead | presente | retirar lease+lock | busy -> none | El lock prueba muerte aunque la lease este vacia. |
| 0 bytes | dead | ausente | preservar+marcador | busy -> busy | No existe prueba observable de muerte. |
| 0 bytes | unknown | presente | preservar | busy -> busy | El lock no resuelve la duda. |
| 0 bytes | unknown | ausente | preservar+marcador | busy -> busy | Cierra el fallo abierto de vacio/espacios. |
| sin identidad | live | presente | preservar | busy -> busy | El lock prueba vida; la lease no puede probar scope+owner completo. |
| sin identidad | live | ausente | preservar+marcador | busy -> busy | Sin identidad observable no se asume vida ni muerte. |
| sin identidad | dead | presente | retirar lease+lock | busy -> none | El lock prueba muerte. |
| sin identidad | dead | ausente | preservar+marcador | busy -> busy | Sin prueba observable no se borra. |
| sin identidad | unknown | presente | preservar | busy -> busy | Ninguna evidencia util resuelve el owner. |
| sin identidad | unknown | ausente | preservar+marcador | busy -> busy | El marcador evita el estado absorbente mudo. |

Refinamiento temporal: una lease `running` viva y pre-deadline se preserva. Si expira, se intenta
detener el arbol y solo se retira tras observar `dead`. Una reserva viva pre-deadline se preserva;
si vence con supervisor aun vivo se preserva y exige recuperacion manual. Un deadline ilegible no
convierte `live` en `dead`.

Contrato permanente: `NEG-HARNESS-LEASE-OWNER-LOCK-STATE-TABLE` recorre las 24 celdas y comprueba
preservacion/retirada, marcador, senal y respuesta del guard antes/despues. Sus mutantes cambian
por separado `unknown -> dead`, omiten evidencia del lock, convierten `unknown` en permiso y
suprimen la creacion del marcador;
cualquier movimiento desde una accion declarada rompe al menos una frontera de la tabla.

## Remediacion 5 - veredicto por rama y orden por efecto

El contrato trivaluado ya no depende del numero de literales `return "unknown"`. La sonda ejecuta
la `Get-LeaseProcessState` real y fuerza por separado el `catch` de `Get-Process`, el `catch` de
`StartTime` y un PID vivo con una hora de arranque desplazada. Los tres mutantes del checker
preservan los literales originales como codigo muerto, pero M1 y M2 devuelven `dead` donde la
produccion devuelve `unknown`, y M3 devuelve `live` donde la produccion devuelve `dead`; cada rama
queda sujeta por comportamiento.

El contrato TASK-0284 resuelve el escritor de evidencia por su efecto observable: usa `$LockPath`,
`$MessageName` y `process_start_time_utc`, encuentra su llamada desde `Invoke-PeerForMessage` y exige
que ocurra despues de `Get-StagedResidueState`. El mutante mueve esa llamada por encima de la sonda,
sin borrarla ni depender del nombre del helper, y el contrato lo mata.

Al alcanzar por primera vez el cuerpo completo del runner, la prueba expuso que Windows PowerShell
rechaza `File.Replace(..., $null)` cuando el lock ya existe. La sustitucion atomica ahora usa una
ruta de backup unica y limpia backup y temporal en `finally`; el runner completo ejerce la
sustitucion y pasa. Los tres lectores de CI que faltaban quedan incluidos en `verification_cmd`.
