---
artifact_id: Analista-TASK-0331-remediacion-2-verdict
task_id: TASK-0331
reviewer: Analista
role: adversarial checker (maker != checker)
created_at: 2026-08-08T04:35:00Z
anchor_commit: 9def32142513ebe81d1a7f81684838dc4456ac5a
supersedes: Analista-TASK-0331-remediacion-1-verdict
verdict: CHANGE-REQUIRED
iteration: 3 (el Arquitecto retiro el limite de 2 en el encargo r3)
---

# Re-juicio TASK-0331 -- remediacion 2

Voz del Analista. Yo no implemento, no promuevo, no cierro. Este veredicto gatea el cierre.

## Anclaje canonico

- Commit bajo revision: `9def32142513ebe81d1a7f81684838dc4456ac5a`
  (`fix(TASK-0331): recover orphan exec leases`). Ancestro de `origin/main` y de HEAD
  (`git merge-base --is-ancestor` -> EXIT 0 en ambos).
- Padre: `ddcdc497be5e7596cd064d45ba2f09b661cb8531`. Lo uso como control para separar
  "defecto heredado" de "direccion creada por este commit".
- Clon limpio detached en `D:/Aegis_Scratch/mapp/r331c/cc` sobre el commit exacto;
  `git status --short` vacio antes y despues de todas las sondas. Los mutantes se aplican
  sobre copias en `D:/Aegis_Scratch/mapp/r331c/mut/<mutante>`, jamas sobre el clon de
  referencia (DECISION-0104: todo bajo el scratch root declarado).
- Alcance declarado por el Arquitecto: SOLO el hub. **SIN PRODUCTO EN ALCANCE.** No corri
  ningun gate de producto.
- Veredicto previo que este supersede:
  `Area_comun/artifacts/Analista-TASK-0331-remediacion-1-verdict.md`.

## Gates recomputados por exit code sobre el clon limpio

    python scripts/test_exec_lease_harness.py                 EXIT=0   (26 PASS)
    python scripts/check_falsification_contracts.py --root .  EXIT=0   (53 negativos / 53 declarados / 0 missing)
    python scripts/validate_collaboration_state.py --root .   EXIT=0
    python scripts/scan_encoding.py                           EXIT=0
    python scripts/scan_domain_neutrality.py --root .         EXIT=0

Estado canonico del hub sano al arrancar: `validate_collaboration_state.py` EXIT=0.

## Respuesta directa a tu pregunta

**Si a la primera mitad y NO a la segunda.**

Los cuatro estados de tu matriz se recuperan en el rearranque 1 y se sostienen en el 2 y en el
3 -- y dos estados vecinos mas que tambien medi. Pero **el negativo nuevo no fija tus cuatro**:
fija cuatro estados distintos (cambia tu fila base `reserved` + lock con proceso muerto por
`reserved` sin `reservation_deadline`), y sobre todo **los cuatro casos del negativo apagan por
stub la unica rama donde vive el peligro**: `function Test-LeaseProcessMatches { return $false }`.
Con el dueno siempre declarado muerto, la rama `if ($leaseMatches)` no se ejecuta nunca en la
corrida sana. Consecuencia medida: el arreglo de la remediacion 1 (leer `reservation_deadline`
para `state=reserved`) **perdio sus dientes**, y la direccion nueva que abre este commit --
borrar la lease de un exec VIVO -- es invisible al gate.

## Matriz de estados x tres rearranques (funciones REALES del `.ps1`, dueno muerto)

Sonda `probes/p1_matrix.py`: carga por AST `Clear-StaleCronLockIfSafe`, `Test-LeaseProcessMatches`
y `Stop-LeaseProcessTree` reales (no stubs), pid inexistente, tres ciclos de autocurado por caso.

| Estado inicial | r1 | r2 | r3 | log emitido |
|---|---|---|---|---|
| `reserved` + lock, proceso muerto (tu fila base) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=pre_deadline` |
| `reserved` **sin lock** (G1) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=pre_deadline` |
| lease truncada + lock (G2) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=unreadable_lease` |
| lease 0 bytes + lock (G2) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=pre_deadline` |
| `reserved` sin `reservation_deadline` + lock (G3) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=pre_deadline` |
| lease truncada **sin lock** | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=unreadable_lease` |
| `running` + lock, pid muerto (control) | RECUPERADO | RECUPERADO | RECUPERADO | `SELF_HEAL_STALE_LOCK state=pre_deadline` |

**G1, G2 y G3 cerrados y convergentes.** Ni un solo `LOCKED skip` mudo, ni un solo
`SELF_HEAL_FAIL`. Las siete filas que en r1 tenian cuatro encalladas permanentes estan verdes.

## Tabla vector por vector

| Foco | Vector | Resultado |
|------|--------|-----------|
| G1 | `reserved` sin lock x3 rearranques | **PASS** |
| G2 | lease truncada / 0 bytes + lock x3 | **PASS** |
| G3 | `reserved` sin `reservation_deadline` + lock x3 | **PASS** |
| G4 | frase de alcance del archivo en el handoff vs mis cifras medidas | **PASS** |
| Nuevo | lease ILEGIBLE de un exec **VIVO** (V3/V4/V5) | **SLIPS (G6, bloqueante)** |
| Nuevo | el peer deja de vetar tras el autocurado, con el exec vivo | **SLIPS (G6)** |
| Dientes | mutante que revierte la lectura de `reservation_deadline` (arreglo de r1) | **SLIPS (G7, bloqueante)** -- gate VERDE |
| Dientes | mutante `catch` sin limpieza | **PASS** -- gate RED |
| Dientes | mutante que vuelve a exigir lock | **PASS** -- gate RED |
| Dientes | mutante que revierte el orden lock/reserva | **SLIPS (G8, no bloqueante)** -- gate VERDE |
| Dientes | mutante que revierte el orden del `finally` | **SLIPS (G8)** -- gate VERDE |
| Regresion | funciones de scope/archivo/reserva vs mi ancla de r1 `714221b6` | **PASS** -- byte identicas |
| Regresion | admision atomica, `DeleteOnClose`, carrera vieja, veto de arbol sucio | **PASS** -- 26/26 |
| Regresion | 22 vectores de claim malformado y de frontera | **PASS** por identidad de funcion |
| Carry | scope MIXTO con glob (G5 de r1) | sin cambio, sigue fallando ABIERTO |

## G6 (BLOQUEANTE) -- el autocurado borra la lease de un exec VIVO, y nadie la repone

Este es el estado vecino nuevo que pediste que te dijera.

El arreglo trata "lease ilegible" como sinonimo de "lease huerfana". No lo es: la ventana en la
que la lease es ilegible es **exactamente la ventana del latido de un exec que esta vivo**.

### Medicion 1 -- la ventana existe y es de un exec vivo

`Write-Utf8NoBom` es `[System.IO.File]::WriteAllText` (`:128`), que trunca antes de escribir, y
`Update-ExecLeaseHeartbeat` lo llama **una vez por segundo durante todo el exec**
(`:1354`, `while (-not $process.WaitForExit(1000))`). Sonda `probes/p5_window.py`, un escritor
real en bucle y un job lector externo muestreando `Length`:

    tamanos observados por el lector externo:  0  y  1092

### Medicion 2 -- con el codigo nuevo, esa lease se borra aunque el dueno viva

Sonda `probes/p2_live_owner.py`: proceso hijo REAL, lease escrita con su `pid` y su `StartTime`
real en formato "o", funciones reales (incluida `Test-LeaseProcessMatches` de verdad).

| Caso (dueno VIVO) | 9def3214 (nuevo) | ddcdc497 (padre) |
|---|---|---|
| lease valida, `deadline` futuro | conservada | conservada |
| lease valida `reserved`, deadline futuro | conservada | conservada |
| lease **truncada** | **BORRADA** (lease+lock) | conservada (`SELF_HEAL_FAIL`) |
| lease **0 bytes** | **BORRADA** (lease+lock) | conservada (`SELF_HEAL_FAIL`) |
| `reserved` sin `reservation_deadline` | **BORRADA** (lease+lock) | conservada (`SELF_HEAL_FAIL`) |

En las tres filas nuevas el proceso seguia vivo despues (`proc_vivo_despues=True`): el autocurado
no mata al dueno, solo le quita su lease y su lock.

### Medicion 3 -- nada la repone, y el log miente

`Update-ExecLeaseHeartbeat` (`:195`) empieza con `if (-not (Test-Path $LeasePath)) { return }`.
Sonda `p5_window.py` con la lease ya borrada: `lease_recreada=false`, **y ni una linea de log**.
El exec vivo sigue el resto de su vida sin lease y sin lock, en silencio.

Y la linea que si se emite dice lo contrario de lo que paso:

    SELF_HEAL_STALE_LOCK owner=Codex pid= message= state=pre_deadline

Se anuncia una recuperacion de algo rancio cuando lo que se hizo fue desarmar la exclusion mutua
de un exec en curso. `pid=` y `message=` vacios son la unica pista, y no hay ningun estado que
los distinga.

### Medicion 4 -- la consecuencia, por comportamiento

Sonda `probes/p6_cadena.py`, con `Get-AdditionalWorkSignal` real sobre un fixture con
`scope_routes: src/target`, la lease de Codex solapando ese scope y su exec vivo:

    paso 1  el peer (Analista) pregunta            -> active_peer_lease
    paso 2  lease a 0 bytes (ventana del latido);
            una SEGUNDA instancia del cron de Codex corre Clear-StaleCronLockIfSafe
            -> lease BORRADA, lock BORRADO, exec de Codex VIVO
    paso 3  el peer vuelve a preguntar             -> none

`Get-AdditionalWorkSignal` (`:985`) enumera **ficheros** `*.exec-lease.json`. Sin fichero no hay
lease, y sin lease no hay veto.

**Honestidad sobre lo heredado:** en el paso 3 el codigo padre tambien devuelve `none` con una
lease de 0 bytes -- `Read-JsonWithDeadline` sobre un fichero vacio devuelve `ok=true, value=null`,
asi que el fallo-abierto momentaneo ya existia y **corrijo aqui mi residual 2 de r1**, donde dije
que ese caso caia en `peer_lease_unreadable` fail-closed. No es cierto. La diferencia que
introduce este commit no es el fallo-abierto: es su **duracion**. Con el padre los dos artefactos
sobreviven, el escritor termina su `WriteAllText` en microsegundos y el veto vuelve. Con
9def3214 los artefactos **desaparecen y no vuelven nunca**: el fallo-abierto pasa de una ventana
de microsegundos a todo lo que le quede de vida al exec.

### Medicion 5 -- alcanzabilidad del disparo

`p5_window.py` sobre el fuente del clon:

    llamadas a Clear-StaleCronLockIfSafe:  linea 1267 (por mensaje) y linea 1470 (arranque)
    guard de instancia unica Test-ExistingCronInstance:  linea 1471

El autocurado de arranque corre **una linea ANTES** del guard de instancia unica. Es decir: una
segunda instancia del cron del mismo peer, lanzada mientras la primera esta a mitad de exec --
relanzar tras un fix del harness, destrabar un jam, un barrido de zombies: practica operativa
documentada de esta instancia -- ejecuta el borrado y **solo despues** descubre que sobra y sale
con `INSTANCE_ALREADY_RUNNING`. El dano ya esta hecho.

No vendo esto como frecuente: exige que ese arranque caiga en la ventana del `WriteAllText`. Lo
vendo por lo que es: **una direccion de fallo ABIERTO, creada por este commit, en la unica
direccion que la tarea declara innegociable**, y que convierte un solape de microsegundos en uno
que dura el exec entero. Es tambien la promocion a defecto de mi residual 2 de r1 (el latido no
es atomico): lo que era ruido evitable ahora es portante.

### Arreglo minimo (no lo implemento)

Cualquiera de los dos cierra la direccion sin reabrir G2:

1. **Escritura atomica de la lease** (temp + `Move`/`Replace`) en `Write-Utf8NoBom` para la lease
   y en `Acquire-ExecReservation`. Con eso "lease ilegible" pasa a implicar de verdad un dueno
   muerto, y el autocurado actual queda correcto tal cual esta.
2. **Reintento acotado antes de declarar huerfana:** releer la lease N veces con una pausa mayor
   que la duracion de un `WriteAllText` antes de tratarla como rancia. Un escritor vivo cierra su
   ventana en milisegundos; una lease huerfana truncada sigue truncada para siempre, asi que G2
   se mantiene cerrado.

Y en los dos casos un negativo **por comportamiento con un proceso VIVO real**, no con
`Test-LeaseProcessMatches` stubeado.

## G7 (BLOQUEANTE, barato) -- el arreglo de la remediacion 1 se quedo sin negativo

`NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` cambio de mutante: antes revertia
`[string]$lease.reservation_deadline` a `[string]$lease.deadline` (la linea que arreglo r1);
ahora muta la rama del dueno vivo, el `catch` y la exigencia de lock. Corri mis propios cinco
mutantes sobre copias del clon con el gate COMPLETO (`probes/p4_mutants.py`):

    M1  revierte la lectura de reservation_deadline (arreglo de r1)   EXIT=0  GATE VERDE  <- SOBREVIVE
    M2  catch sin limpieza (fail-only)                               EXIT=1  GATE RED
    M3  vuelve a exigir lock antes de mirar la lease propia          EXIT=1  GATE RED
    M4  revierte el orden lock/reserva en Invoke-PeerForMessage      EXIT=0  GATE VERDE
    M5  revierte el orden de borrado del finally                     EXIT=0  GATE VERDE

M1 sobrevive por la misma causa que G6: los cuatro casos de la sonda declaran
`function Test-LeaseProcessMatches { param($Lease) return $false }`, asi que el `if ($leaseMatches)`
-- que es donde vive ahora la lectura del deadline -- **no se ejecuta jamas** en la corrida sana.
El negativo prueba la rama del dueno muerto por cuatro caminos distintos y deja la del dueno vivo
sin una sola asercion.

Y M1 no es cosmetico: con el mutante aplicado, un `reserved` de dueno **vivo** lee
`$lease.deadline` (ausente), `[DateTime]::Parse("")` lanza, y el `catch` nuevo borra lease y lock
de un exec en curso. O sea, el mutante empeora exactamente en la direccion de G6 y el gate no se
entera.

**Ojo con el arreglo facil:** volver a meter tu fila base (`reserved` + lock, proceso muerto) NO
devuelve los dientes -- con el dueno muerto el deadline tampoco se lee. Lo que hace falta es un
caso de dueno **VIVO**: `reserved` pre-deadline debe conservarse, `reserved`/`running` pasado de
deadline debe limpiarse. Ese mismo caso es el que cierra G6.

## G8 (NO bloqueante) -- el reordenamiento lock/lease no tiene negativo

M4 y M5 dejan el gate verde. El handoff acredita a ese reordenamiento haber eliminado
"the reachable own-lease-without-lock window". La afirmacion es cierta por lectura -- la lease ya
no puede existir sin lock en el arranque, y en el `finally` se borra antes que el lock -- pero
hoy **nada la sostiene**: si alguien revierte las dos lineas, ningun contrato se entera. No
bloquea porque G1 lo cierra el autocurado por si solo (la fila `reserved` sin lock se recupera),
asi que el orden es cinturon sobre tirantes. Queda declarado.

## G4 -- la afirmacion del handoff: PASS

La frase nueva dice exactamente lo que yo medi, con mis cifras:

    "The archive lookup resolves only archived tasks whose contracts declare scope_routes: the
     checker measured 228 of 1,033 archived-task messages recovered, while 272 of 365 archived
     task contracts lacked scope_routes. A message whose hot or archived task lacks that
     declaration remains terminally deferred until manual rearm."

228/1033 y 272/365 son mis numeros de r1, medidos sobre los 2272 `MSG-*.md` reales. La frase
falsa ("removes archived tasks from that class") desaparecio. Afirma el alcance y declara el
residuo. **Cerrado.**

Lo que el handoff **no** declara es la frontera nueva que abre G6: que una lease ilegible se
trata como huerfana sin comprobar que el dueno este muerto. Eso es justo lo que pediste en tu
punto G4 ("si el arreglo amplia el espacio recuperable, que lo declare con su frontera nueva").

## Sin regresion en lo ya probado

Verificado por identidad de funcion contra mi ancla de r1 `714221b6` (md5 del cuerpo extraido):

    ConvertTo-ComparableScope   IGUAL      Get-MessageWorkDescriptor  IGUAL
    Get-TaskRowById             IGUAL      Get-AdditionalWorkSignal   IGUAL
    Acquire-ExecReservation     IGUAL      ConvertTo-ComparableRoute  IGUAL
    Test-ScopeIntersection      IGUAL      Get-LeaseWorkScope         IGUAL

El diff de `9def3214` contra su padre toca **tres hunks y nada mas**:
`Clear-StaleCronLockIfSafe` y las dos reordenaciones de `Invoke-PeerForMessage`. Por tanto los 22
vectores de claim malformado y de frontera, la matriz de resolucion de los 228 mensajes y la
familia de globs dan el mismo resultado que en r1 por construccion, no por suposicion. La carrera
del codigo viejo, la admision atomica, `DeleteOnClose` bajo muerte dura y el veto de arbol sucio
los cubre el gate del harness: 26/26 PASS sobre el commit exacto.

## Residuales declarados (no defectos nuevos)

1. **G5 de r1 sigue abierto y sin declarar.** `ConvertTo-ComparableScope` es byte-identica, asi
   que un scope MIXTO (`["src/**", "ruta/concreta.md"]`) sigue dando `none` y fallando ABIERTO.
   Era mi "remediacion 3 (recomendada)"; no se hizo y el handoff no la menciona ni como residuo.
   Riesgo vivo hoy: 0 claims mixtos en el corpus. Lo dejo como residuo, no como bloqueo.
2. **El arbol git compartido** sigue siendo un recurso no declarado. Sin cambio.
3. **Tarea presente en indice caliente Y en archivo** -> irresoluble. Sin cambio, 0 duplicados hoy.
4. **El latido no es atomico.** En r1 era ruido evitable; con G6 pasa a ser portante (ver arreglo
   minimo 1).

## Lo que NO revise

Solo 0331. No toque 0329, 0334, 0335 ni 0336 aunque comparten fichero. Ningun gate de producto,
como declaraste.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

Lo que pediste como criterio esta cumplido: tus cuatro estados (y dos vecinos mas) se recuperan en
el primer rearranque y **se sostienen** en el segundo y el tercero, sin `LOCKED skip` mudo y sin
`SELF_HEAL_FAIL`; el handoff dice lo medido y solo lo medido sobre el archivo; y nada de lo ya
probado se movio. Esta iteracion cierra de verdad el modo de fallo "encallado a prueba de
rearranques".

Lo que lo bloquea es lo que pediste que te dijera: **al cerrar G1 y G2 aparecio un estado vecino
nuevo, y este si es fallo ABIERTO**. El autocurado equipara "ilegible" con "huerfana" sin
comprobar liveness, y la ventana en la que una lease es ilegible es precisamente la del latido de
un exec vivo. Medido: lease y lock de un proceso vivo BORRADOS, nunca repuestos, sin log que lo
distinga, y el peer pasando de `active_peer_lease` a `none` con el exec en curso. Y el negativo no
puede verlo porque apaga por stub la rama del dueno vivo -- la misma razon por la que el arreglo
de la remediacion 1 se quedo sin dientes (M1 verde).

No es un no al diseno. Es "el autocurado necesita saber que el dueno esta muerto antes de borrar,
y el negativo necesita un proceso vivo de verdad".

**Sobre tu oferta de particionar:** G6 y G7 los cierra el mismo cambio (escritura atomica o
reintento acotado + un caso de dueno vivo en el negativo), asi que no lo veo como "arreglar todo
el ciclo de vida de las leases": es acotado. Si prefieres particionar G6 a una tarea propia y
cerrar 0331 con G1/G2/G3/G4, **G7 sigue siendo bloqueante aqui**: es dentro de 0331 donde el
contrato perdio los dientes sobre el arreglo de 0331. Esa decision es tuya, no mia.

Fix loop esperado -- **maximo 2 iteraciones mas; si no cierra, escalo al operador humano**:

- **Remediacion 1 (obligatoria, G6):** el autocurado no debe borrar una lease propia cuya
  ilegibilidad no distinga a un dueno muerto de un dueno vivo a mitad de latido. Direccion A
  (preferida): escritura atomica de la lease (temp + `Move`/`Replace`) en el latido y en la
  reserva. Direccion B: reintento acotado de lectura antes de declararla rancia. En ambas,
  mantener las siete filas de la matriz recuperandose y convergiendo a tres rearranques.
- **Remediacion 2 (obligatoria, G7):** el negativo debe ejercitar la rama del dueno VIVO con un
  proceso real (`Test-LeaseProcessMatches` de verdad, no stub): `reserved` pre-deadline con dueno
  vivo se conserva; `reserved`/`running` pasado de deadline se limpia; y el mutante que revierte
  `reservation_deadline` a `deadline` debe dejar el gate ROJO.
- **Remediacion 3 (recomendada, G8):** un negativo que muera si se revierte el orden de
  publicacion lock/lease.
- **Declaracion (obligatoria):** el handoff debe declarar la frontera nueva del autocurado (que
  trata como huerfana toda lease propia que no pueda leer) o, si se adopta la direccion A,
  declarar que la escritura atomica hace esa equivalencia legitima.
- **Gates afectados:** `scripts/harness/peer_mailbox_cron.ps1`,
  `scripts/test_exec_lease_harness.py`, `Area_comun/protocol/FALSIFICATION_CONTRACTS.json`,
  `Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md`, mas
  `validate_collaboration_state.py`, `scan_encoding.py` y `scan_domain_neutrality.py` sobre el
  arbol commiteado.
- **Re-juicio:** sobre clon limpio del commit siguiente, con la matriz de siete estados x tres
  rearranques reejecutada, la sonda de dueno vivo (lease valida, truncada, 0 bytes y sin
  `reservation_deadline`), la cadena peer `active_peer_lease` -> autocurado -> peer, y los cinco
  mutantes M1-M5.

Analista, 2026-08-08 06:35 (hora local del sistema, UTC+2).
