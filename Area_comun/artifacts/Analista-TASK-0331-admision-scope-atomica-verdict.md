---
artifact_id: Analista-TASK-0331-admision-scope-atomica-verdict
task_id: TASK-0331
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-07T19:40:00Z
anchor_commit: 379a91249cc0a22334e8f3331cd5921e47be2b6b
verdict: CHANGE-REQUIRED
---

# Veredicto TASK-0331 -- admision de peers con scope y con atomicidad

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Arreglo bajo revision: `379a91249cc0a22334e8f3331cd5921e47be2b6b`
  (`fix(TASK-0331): make peer admission scope-aware and atomic`), verificado ancestro del HEAD del
  hub al arrancar (`e792839d`) con `git merge-base --is-ancestor` -> exit 0.
- Contrato: `Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md`.
- Handoff: `Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md`.
- Clon limpio detached en `D:/Aegis_Scratch/mapp/r331/cc`, `git status --short` vacio antes y
  despues de cada sonda. Todas las sondas de comportamiento corren contra ese clon, nunca contra el
  arbol caliente. Los mutantes se escriben a copias en tmp, jamas sobre el clon.
- Alcance declarado por el Arquitecto: SOLO el hub, SIN PRODUCTO EN ALCANCE. No se ejecuto ningun
  `npm test` de Nova ni de Zeus.

## Gates recomputados por exit code sobre el commit exacto

    python scripts/test_exec_lease_harness.py            EXIT=0   (21/21)
    python scripts/check_falsification_contracts.py -r . EXIT=0   (42 negativos permanentes)
    python scripts/validate_collaboration_state.py -r .  EXIT=0
    python scripts/scan_encoding.py                      EXIT=0
    python scripts/scan_domain_neutrality.py --root .    EXIT=0

Estado canonico del hub sano al arrancar: `validate_collaboration_state.py` EXIT=0, drift 0.

## Respuesta directa a tu pregunta

**Tras `taskkill /F` en mitad de la seccion de admision, el siguiente peer entra de inmediato. No
hay ventana en la que los dos agentes queden bloqueados por el fichero de admision.** Medido cuatro
veces con una victima que abre el handle exactamente como `Acquire-ExecReservation`
(`CreateNew` + `FileShare::None` + `DeleteOnClose`), senala que entro, y muere por `taskkill /F /T`
dentro de la seccion:

    control mientras la victima lo sostiene   exec_admission_busy   (el CreateNew rebota, correcto)
    el fichero de admision desaparece a los   0.742 s / 0.523 s / 0.657 s / 0.616 s
    el siguiente peer entra (ok=true) a los   1.348 s / 1.093 s / 1.254 s / 1.197 s
    fichero de admision residual              ninguno en las cuatro corridas

Los 0.5-0.7 s son el desmontaje del proceso por el sistema operativo, no un timeout de lock; el
1.1-1.3 s incluye el arranque de un PowerShell nuevo. `DeleteOnClose` cumple en la practica y en el
peor caso. El primitivo que te preocupaba esta bien.

**El huerfano no esta donde lo buscabas: esta un fichero mas alla.** Lo que la seccion deja escrito
antes de soltar la admision es la LEASE de reserva, y esa si sobrevive a la muerte dura y ademas
derrota al autocurado. Es el hallazgo F1.

## Tabla vector por vector

| Foco | Vector | Resultado |
|------|--------|-----------|
| A | carrera reproducida sobre el codigo VIEJO, dos peers soltados por la misma compuerta | SLIPS-por-diseno-viejo: 2 admitidos, 2 leases vivas. Tu medicion de esta manana era exactamente lo que creias |
| A | mismo escenario sobre el codigo NUEVO, scopes que intersecan | PASS: 1 admitido, 1 lease; el perdedor sale `exec_admission_busy` |
| A | mismo escenario sobre el NUEVO, scopes disjuntos | PASS con matiz: 1 admitido, 1 lease. En tick simultaneo el disjunto tambien serializa una ronda y recupera en el siguiente intervalo |
| B | `taskkill /F` en mitad de la seccion, x4 | PASS: sin lock huerfano, ventana sub-segundo (ver arriba) |
| B | lease en estado `reserved` frente a `Clear-StaleCronLockIfSafe` | **SLIPS (F1)**: `SELF_HEAL_FAIL`, ni lock ni lease removidos, `own_lease_exists` en 3 rearranques seguidos |
| B | `reservation_deadline` de 30 s frente a un exec largo | PASS: la reserva solo cubre la ventana de lanzamiento; `Write-ExecLease` la reescribe a `state=running` con pid y `deadline` justo despues de `Start-Process`. Un exec de horas no caduca por los 30 s |
| C | claim con scope ausente | PASS veta |
| C | claim con scope vacio `[]` | PASS veta |
| C | claim con scope no-array | PASS veta |
| C | claim con JSON ilegible | PASS veta (`claims_unreadable`) |
| C | claim con scope `null` explicito | PASS veta |
| C | claim con ruta solo-espacios | PASS veta |
| C | claim con elemento no-string (`[123]`) | PASS veta |
| C | claim sin `expires_at` | PASS veta |
| C | claim con `expires_at` no parseable | PASS veta |
| C | claim sin `owner` y scope que interseca | PASS veta |
| C | claim sin `status` y sin scope | PASS veta |
| C | `CLAIMS.json` sin la clave `claims` | PASS veta |
| C | claim cuyo scope son SOLO rutas de ledger | PASS veta (normaliza a nulo -> ambiguo -> cerrado) |
| C | lease ajena viva sin tarea determinable | PASS veta |
| C | **claim con glob `["*"]`** | **SLIPS (F3)**: `none`. Forma real: `CLAIM-20260702-Analista-TASK-0240-wild-release` |
| C | **claim con glob `["scripts/**"]` que SI cubre la ruta** | **SLIPS (F3)**: `none` |
| C | mensaje sin `task_id` resoluble | **SLIPS (F2)**: `message_scope_ambiguous` permanente, no transitorio |
| D | veto de arbol sucio precede a la admision (por fuente) | PASS estructural |
| D | contrato `NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` frente a mutante de CODIGO MUERTO | **SLIPS (F4)**: el contrato sobrevive con el veto muerto |
| E | AC4c declara la frontera de la garantia | PASS parcial: dice lo esencial, omite el arbol git compartido y el efecto de F2 |
| E | la exclusion del ledger esta respaldada de verdad | PASS: `ledger_file_lock` real (`msvcrt.locking` / `fcntl.flock`) y esta instancia tiene `enforce:true` + `authoritative:true` |
| F | AC2b pide el solape recuperado MEDIDO | SLIPS blando (F5): el handoff da un porcentaje de un hipotetico. Medicion aportada abajo |
| - | claim `blocked` que interseca / que no interseca | PASS: veta solo si interseca. Tu residual de la tarea bloqueada queda cubierto |

## Reproduccion de los hallazgos

### F1 (BLOQUEANTE) -- la lease de reserva derrota al autocurado y encalla al peer entre rearranques

`Acquire-ExecReservation` escribe una lease con `state:"reserved"`, `reserved_at` y
`reservation_deadline`, y SIN `pid` ni `deadline`. `Clear-StaleCronLockIfSafe` -- el unico camino de
recuperacion de huerfanos, que corre al arrancar el cron -- hace
`[DateTime]::Parse([string]$lease.deadline)`. Sobre una lease de reserva ese campo no existe, el
Parse lanza, el catch escribe `SELF_HEAL_FAIL` y NO borra ni el lock ni la lease.

Sonda con la forma exacta que escribe el codigo entregado:

    lease state=reserved   -> lock_removed=false  lease_removed=false  log=SELF_HEAL_FAIL Parse
    lease state=running    -> lock_removed=true   lease_removed=true   log=SELF_HEAL_STALE_LOCK
    (pid muerto, control)

Y el encallado no se disuelve solo. Simulando tres rearranques del cron (autocurado + siguiente
tick) sobre esa lease residual:

    restart 1  ok=false  reason=own_lease_exists  lease_still_there=true
    restart 2  ok=false  reason=own_lease_exists  lease_still_there=true
    restart 3  ok=false  reason=own_lease_exists  lease_still_there=true

Cadena completa: muerte dura del cron dentro de la ventana de reserva -> lease `reserved` residual
-> autocurado falla en cada arranque -> `Acquire-ExecReservation` rebota con `own_lease_exists` en
cada tick -> todo mensaje se difiere -> a los 7200 s con la misma razon pasa a `defer_terminal`. El
agente queda muerto de forma silenciosa salvo por una linea `SELF_HEAL_FAIL` en su log, y sobrevive
a los rearranques.

Honestidad sobre la exposicion: la ventana es estrecha. Va desde el `CreateNew` de la lease hasta
`Write-ExecLease`, es decir a lo ancho de `Start-Process` del CLI del agente -- cientos de ms a un
par de segundos. Pero no es hipotetica: `taskkill /F` sobre un cron atascado es practica operativa
documentada de esta instancia, y el propio harness mata arboles de proceso por deadline. La
direccion del fallo es CERRADA, como pide la tarea, pero es la unica forma de fallo cerrado de este
arreglo que NO se recupera sola y que sobrevive al remedio estandar (relanzar el cron). Antes de
este commit ese estado no podia existir: toda lease llevaba `deadline`.

Arreglo minimo sugerido (no lo implemento): que `Clear-StaleCronLockIfSafe` acepte una lease sin
`deadline` -- caer a `reservation_deadline`, o tratar `state=reserved` sin pid vivo como rancia --
y un negativo permanente que muera si una lease de reserva sobrevive al autocurado.

### F2 (BLOQUEANTE por no declarado) -- un mensaje sin trabajo resoluble ya no se difiere: se pierde

`Get-MessageWorkDescriptor` devuelve `$null`, y por tanto `Acquire-ExecReservation` devuelve
`message_scope_ambiguous`, en todos estos casos medidos:

    mensaje sin task_id (FYI, HANDOFF, DIRECTIVA, RESP, COORD...)  message_scope_ambiguous
    task_id que no esta en TASK_INDEX.json (indice CALIENTE)       message_scope_ambiguous
    tarea sin bloque scope_routes parseable en su contrato         message_scope_ambiguous
    task_id en minusculas (la busqueda en el indice es -ceq)       message_scope_ambiguous
    caso feliz                                                     ok=true

Eso es fail-closed y respeta AC3. El problema es otro y no esta declarado: **la razon del
diferimiento es ahora una propiedad ESTRUCTURAL del mensaje, no un estado transitorio del peer.**
La tarea razona explicitamente que "el diferimiento tiene 7200 s de margen antes de volverse
terminal, asi que no se pierde ningun mensaje" -- ese razonamiento asume que la causa se disuelve.
Aqui no se disuelve nunca: la misma razon se repite en cada tick hasta `defer_terminal`, y el
mensaje muere y exige rearme manual del `*.retry.json`.

Ademas el resolutor lee solo el indice CALIENTE, que esta podado por diseno (AGENTS.md seccion 0:
los validadores leen estado caliente MAS archivos; este lector no). Poblacion real de mensajes del
hub, clasificada:

    en TASK_INDEX.json (caliente)     45
    solo en TASK_INDEX_ARCHIVE.json  737
    en ninguno de los dos             32
    sin task_id valido               993
                                    ----
    total mensajes MSG-*.md         1807

Atenuante medido, y lo declaro porque cambia la severidad: **hoy no hay ni un mensaje vivo
bloqueado por esto.** Las dos colas de reintento reales resuelven 7 de 7 (`analista` 1/1, `codex`
6/6), y en agosto 0 de 86 mensajes ruteados a un peer carecen de `task_id` valido. Pero en julio
eran 314 de 370 (85 por ciento) y en junio 40 de 271: la clase existe y depende por completo de una
disciplina de ruteo tuya que no esta gateada por nada. Un solo FYI o DIRECTIVA sin `task_id`, o un
mensaje sobre una tarea ya podada del indice caliente, brickea ese mensaje.

Es CHANGE-REQUIRED por dos motivos, ninguno de forma: (1) AC4c pide declarar que garantiza y que no
el mecanismo, y esta conversion de "difiere" en "pierde" no esta dicha en ninguna parte del
handoff; (2) el arreglo barato existe -- consultar tambien `TASK_INDEX_ARCHIVE.json` cierra 737 de
los 1771 no resolubles.

### F3 (no bloqueante, arreglo barato) -- un scope con glob deja de vetar en silencio

    claim scope ["*"]           -> none   (deberia ser el veto mas amplio posible)
    claim scope ["scripts/**"]  -> none   (cubre literalmente la ruta del mensaje)
    claim scope ["scripts/harness/*.ps1"] -> none

La comparacion es literal, asi que una ruta-patron no interseca nunca con nada. Esto no es un claim
"malformado" en el sentido de AC3 -- esta bien formado y su intencion es inequivoca -- y sin
embargo falla ABIERTO, que es la unica direccion que la tarea declara innegociable. Frecuencia real
en el dataset: 1 de 2270 claims historicos usa glob (`CLAIM-20260702-Analista-TASK-0240-wild-release`,
scope `["*"]`), asi que el riesgo vivo es bajo, pero el arreglo es de una linea: si una ruta
contiene metacaracteres de glob, tratarla como no resoluble y por tanto vetar.

### F4 (SLIP de contrato) -- AC4 quedo atado a la FORMA, no al EFECTO

`NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` comprueba que el literal
`if ($residueState -eq "live") {` esta presente y que su indice en la fuente es menor que el de
`Acquire-ExecReservation -Message $Message`. Es una asercion sobre el orden del texto. Mutante de
CODIGO MUERTO que la sobrevive con el veto ya inoperante -- literal intacto, orden intacto, valor
envenenado:

    $residueState = Get-StagedResidueState
    $residueState = "clean"                 <- una linea insertada

    fuente sana                              -> True
    mutante del maker (guard borrado)        -> False   (lo mata, correcto)
    mutante de codigo muerto (guard vivo     -> True    <- el contrato SOBREVIVE
    en el texto pero inalcanzable)

Es la misma familia de escape que ya nos mordio en 0324 y en 0330. AC4 pide "un test que lo fije";
lo que fija hoy es el layout del fichero. No bloquea el cierre por si solo, pero deja el AC4 sin
teeth reales.

### F5 (SLIP blando) -- AC2b pedia una medicion y el handoff da un porcentaje de un hipotetico

El handoff dice "100 percent of an otherwise eligible declared-disjoint lease window is recovered at
this gate". Eso es una tautologia, no un tiempo. Aporto la medicion que faltaba, del log real del
cron del Analista de hoy 2026-08-07 (822 eventos, 00:03:24 a 19:15:26), sumando para cada
`RETRY_DEFER` el intervalo hasta el evento siguiente:

    active_external_claim     215.7 min
    worktree_residue_live     167.1 min
    active_peer_lease          39.5 min
    -----------------------------------
    total diferido            422.2 min
    atacable por TASK-0331    255.2 min   (60 por ciento del tiempo diferido)

255.2 min (4 h 15 min) es el TECHO de lo recuperable hoy; lo recuperado de verdad es el subconjunto
de esos diferimientos cuyos scopes eran disjuntos. `worktree_residue_live` (167.1 min, 40 por
ciento) no lo toca esta tarea y sigue siendo el segundo impuesto del ciclo.

## Residuales declarados (no defectos, pero deben quedar dichos)

1. **El arbol git compartido no lo ve nadie.** Dos execs disjuntos admitidos comparten UN working
   tree y UN `.git/index`. `.git` no esta en el `scope_routes` de ninguna tarea, asi que el guard
   no puede verlo, y sin embargo lo muta el 100 por cien de los execs (`git add`, `git commit`,
   `git push`). El veto de arbol sucio solo muestrea en el instante de la admision: dos peers
   admitidos limpios pueden ensuciar despues. AC4c dice "does not infer undeclared dynamic routes",
   que lo cubre de forma generica, pero no nombra el recurso compartido que de verdad tocan todos.
   Antes de 0331 el veto incondicional de lease lo impedia de facto.
2. **La exclusion de los contenedores de ledger esta bien fundada, y la verifique.** No es un acto
   de fe: `runtime/submit_intent.py` envuelve sus dos caminos de escritura en `ledger_file_lock`,
   que es un lock de fichero entre procesos real (`msvcrt.locking` en win32, `fcntl.flock` en el
   resto), y esta instancia tiene `event_state.enforce:true` y `authoritative:true`, de modo que el
   ledger no se edita a mano. La decision de normalizar `Area_comun/state` y `runtime/state` a nulo
   es correcta y ademas es portante: 7009 rutas de ledger aparecen en los 2270 claims historicos;
   sin esa exclusion el guard serializaria absolutamente todo.
3. **El alivio es parcial por construccion.** 106 de 2270 claims historicos (4.7 por ciento)
   normalizan a nulo -- scope solo-ledger o vacio -- y por tanto siguen vetando globalmente. 21
   tienen scope ausente o vacio. Eso es fail-closed correcto, pero conviene no prometer que el
   impuesto desaparece.
4. **Tick simultaneo con scopes disjuntos.** El perdedor sale `exec_admission_busy` y recupera en el
   siguiente intervalo. Correcto, pero significa que el solape disjunto se materializa en ticks
   escalonados, no en el mismo tick.
5. **Tu residual de la tarea BLOQUEADA queda cubierto**, y lo medi: un claim con `status: blocked`
   veta si interseca y NO veta si es disjunto. El `CLAIM-20260807-Codex-TASK-0330-work` que citas ya
   no figura en `CLAIMS.json`; los dos unicos claims no-released vivos
   (`CLAIM-20260703-Codex-TASK-0230-*`) expiraron el 2026-07-04 y no vetan bajo ninguno de los dos
   codigos.
6. **Transicion entre versiones del harness.** Una lease vieja sin `work_scope` se resuelve por el
   regex `TASK-[0-9]{4}` sobre `task_or_msg_id`; si el nombre del mensaje no lleva el id, veta.
   Fail-closed correcto, pero durante una ventana con un cron viejo y otro nuevo el alivio no
   aplica a todos los mensajes.

## Lo que NO revise

Solo 0331, como pediste. No toque 0330 (bloqueada, alcance ampliado), ni 0322 ni 0325 (en
remediacion). No corri ningun gate de producto.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

El nucleo del arreglo es solido y esta demostrado por comportamiento, no por lectura: la carrera del
codigo viejo se reproduce (2 admitidos, 2 leases), la admision atomica la cierra (1 admitido, 1
lease), `DeleteOnClose` aguanta la muerte dura sin dejar lock huerfano, y el fail-closed resiste 17
vectores de claim y lease malformados sin una sola inversion. La direccion del cambio es la
correcta.

Lo que lo bloquea es que introduce un estado nuevo, `state=reserved`, y el camino de recuperacion de
huerfanos no lo conoce (F1): una muerte dura en la ventana de lanzamiento deja al agente encallado
de forma permanente y a prueba de rearranques, que es peor que el impuesto que la tarea venia a
quitar. Y que la frontera declarada en AC4c omite el efecto de F2 -- una clase entera de mensajes
pasa de "se difiere" a "se pierde".

Fix loop esperado, maximo 2 iteraciones antes de escalar al operador humano:

- **Remediacion 1 (obligatoria, F1):** `Clear-StaleCronLockIfSafe` debe recuperar una lease en
  `state=reserved` (sin `deadline`). Negativo permanente nuevo que muera si una lease de reserva
  sobrevive al autocurado.
- **Remediacion 2 (obligatoria, F2):** resolver el trabajo consultando tambien
  `TASK_INDEX_ARCHIVE.json`, y declarar en el handoff que un mensaje sin trabajo resoluble se
  difiere hasta `defer_terminal` y se pierde -- o cambiar ese camino para que no sea terminal.
- **Remediacion 3 (recomendada, F3):** una ruta con metacaracteres de glob se trata como no
  resoluble y por tanto veta.
- **Remediacion 4 (recomendada, F4):** convertir `NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION`
  en un contrato por comportamiento que muera ante el mutante de codigo muerto.
- **Gates afectados:** `scripts/test_exec_lease_harness.py`,
  `scripts/check_falsification_contracts.py`, `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`,
  mas `validate_collaboration_state.py` y `scan_encoding.py` sobre el arbol commiteado.
- **Re-juicio:** antes del commit de cierre, sobre clon limpio del commit de remediacion, con las
  sondas F1 (autocurado + 3 rearranques), F2 (matriz de resolucion + poblacion real) y F3 (globs)
  reejecutadas por comportamiento.

Analista, 2026-08-07.
