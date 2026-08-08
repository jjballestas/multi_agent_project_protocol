---
artifact: Analista-TASK-0331-tension-preservar-recuperar-verdict
task_id: TASK-0331
reviewer: Analista
role: checker (adversarial, independent)
created_at: 2026-08-08
local_time: 2026-08-08 08:18 (+02:00)
anchor_commit: 4c4e26655df215e88d1befd4a3e325e452466849
protocol_head_at_review: 06e83983092b0698601c3dde9bfba15559ac552c
clean_clone: D:/Aegis_Scratch/multi_agent_project_protocol/an0331r4
verdict: CHANGE-REQUIRED
---

# TASK-0331 r4 -- no aterrizo en medio: solto un extremo y piso el otro

## Respuesta a tu pregunta, primero

**Hemos cambiado de extremo, parcialmente, y hay un tercer lado que nunca estuvo en ninguno de
los dos.** Medido, no leido:

- La direccion destructiva **mejora de verdad**: de 54 celdas que borraban la lease de un dueno
  VIVO en r2 se baja a 22 en r3. Eso es real y no es cosmetico.
- La direccion de recuperacion **retrocede**: **15 estados con dueno MUERTO que r2 limpiaba en el
  rearranque 1 ahora sobreviven a los tres rearranques** y no convergen nunca. Es exactamente el
  encallamiento de G1/G2, reintroducido por el otro lado, tal como temias.
- Y el guard del peer **falla ABIERTO** en un miembro de la familia que el autocurado ahora
  conserva: una lease ajena de **0 bytes** devuelve `none` -- ni `active_peer_lease` ni
  `peer_lease_unreadable`. El autocurado dice "puede haber un exec vivo aqui, conservo"; el guard
  del peer mira el mismo fichero y dice "no hay nada, adelante". Preservar mas alarga la vida de
  ese fichero invisible, asi que r3 **agranda** la ventana de fallo abierto que AC3 declara
  innegociable.

Las 22 celdas destructivas que quedan no son todas alcanzables -- lo declaro abajo sin inflarlas --
pero **tres de ellas usan formas que escribe el propio harness**, y una de esas tres deja al exec
VIVO corriendo sin lease y sin lock, que es peor que perder un fichero: es perder la exclusion.

## Anclaje y reproduccion

Clon limpio detached en `06e83983` (los tres ficheros del alcance son byte-identicos a
`4c4e2665`: `peer_mailbox_cron.ps1` = `f46f0540...`, `test_exec_lease_harness.py` = `2827333f...`).
`git status --short` en el clon: vacio.

    python scripts/test_exec_lease_harness.py            -> exit 0   27/27
    python scripts/check_falsification_contracts.py --root .  -> exit 0   55 declarados / 55 permanentes / 0 missing
    python scripts/validate_collaboration_state.py --root .   -> exit 0
    python scripts/scan_encoding.py                      -> exit 0
    python scripts/scan_domain_neutrality.py --root .    -> exit 0

El runner del harness esta cableado en CI (`.github/workflows/validate.yml:238`), comprobado, no
solo declarado.

**Mi medicion no reusa la sonda del maker.** Cargo `Clear-StaleCronLockIfSafe` y
`Test-LeaseProcessMatches` REALES del `.ps1` por AST y les construyo el producto cartesiano
completo: 11 formas de lease x 6 formas de lock x {dueno vivo con proceso hijo real, dueno muerto
con proceso real ya terminado} = 132 celdas por version, contra r3 (`4c4e2665`) y contra r2
(`9def3214`) para poder declarar el DELTA y no solo el estado.

## Foco A -- la lease de un exec VIVO nunca se borra

**SLIPS.** Con dueno vivo (proceso hijo real, `owner_alive_after_selfheal=true` verificado en cada
celda), estas tres formas -- **todas producibles por el propio harness** -- borran lease Y lock:

**S1. Lease `running` legible, `process_start_time_utc` vacio.**

    lease: {state:"running", pid:29104(VIVO), process_start_time_utc:"", deadline:"2099-01-01"}
    lock : {pid:29104(VIVO), process_start_time_utc:""}
    ->  lease_exists=false  lock_exists=false
    ->  SELF_HEAL_STALE_LOCK owner=Codex pid=29104 message=MSG-x state=pre_deadline
    ->  STOP_LEASE_PROCESS_TREE_CALLED: NO aparece en el log

Esta celda no entra en el `catch`: la lease parsea perfectamente. Por tanto **toda la logica de
preservacion que anade r3 vive en el `catch` y aqui no se ejecuta ni una linea**. El deadline de
2099 tampoco se mira, porque la rama del deadline esta detras de `if ($leaseMatches)`. Y como
`Stop-LeaseProcessTree` no se llama, **el exec sigue vivo sin lease y sin lock**: el siguiente
`Invoke-PeerForMessage` pasa el `LOCKED skip`, no encuentra lease, y arranca un SEGUNDO exec
concurrente. Eso no es perder trabajo, es anular la garantia de AC4b y devolvernos la escritura
concurrente que DECISION-0020 existe para impedir.

El campo vacio no me lo invente: `Get-ProcessStartTimeUtc` **devuelve `""` desde su propio `catch`**
(lineas del mismo fichero), y tanto `Write-ExecLease` como `Write-ExecLockEvidence` empotran ese
valor tal cual.

**S2. Lease ilegible + lock con `process_start_time_utc` vacio, dueno VIVO.**

    ->  SELF_HEAL_ORPHAN_LEASE owner=Codex liveness=dead action=remove

El codigo **extiende un certificado de defuncion sin una sola prueba de muerte**. La causa es de
diseno, no de detalle: `Test-LeaseProcessMatches` es de DOS valores, y su `$false` significa a la
vez "el proceso esta muerto" y "no tengo identidad que comprobar". El modelo de tres estados que
me planteas solo esta implementado a medias -- `unknown` se emite cuando el OBJETO de evidencia
falta (lock ausente o no parseable), nunca cuando la COMPROBACION es inconcluyente. El handoff
afirma que solo elimina "when a parseable lease or lock identity **proves** its process is dead";
esa frase es falsa para esta celda y lo demuestro con el dueno vivo delante.

**S3. La forma REAL de la reserva.** Copiada literal de `Acquire-ExecReservation` (sin `pid`, con
`reservation_deadline` a 30 s futuros) y lock con identidad del supervisor VIVO:

    ->  lease y lock BORRADOS, SELF_HEAL_STALE_LOCK owner=Codex pid= message=MSG-x state=pre_deadline

Consecuencia colateral que conviene registrar: **el arreglo de r1 -- "selecciona
`reservation_deadline` para `state=reserved`" -- es codigo inalcanzable para la forma que el codigo
real escribe**, porque la rama del deadline exige `$leaseMatches` y una lease de reserva no lleva
`pid`. El negativo `NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` pasa porque su fixture `reserved` inyecta
un `pid` y un `process_start_time_utc` que la reserva real nunca tiene. La propiedad se declaro
cerrada en r1 y nunca estuvo en vigor.

**Control (S4):** lease `running` con identidad correcta de dueno vivo -> lease y lock
CONSERVADOS, cero logs. La sonda distingue, no aprueba por construccion.

**Alcanzabilidad, declarada sin inflar.** El `catch` de `Get-ProcessStartTimeUtc` es codigo que el
maker escribio a proposito, pero **no he demostrado un disparador de ese `catch` en operacion
normal** (el harness solo lo llama sobre su propio supervisor y su propio hijo, ambos accesibles).
Lo mismo para S3: necesita un autocurado durante los 30 s de reserva, y el unico llamador ajeno
esta detras de `Test-ExistingCronInstance`. Asi que **el defecto de decision esta CONFIRMADO por
comportamiento; su alcanzabilidad extremo a extremo NO esta demostrada.** Lo digo asi y no de otra
manera. Lo que si esta demostrado es que la garantia que el handoff enuncia no se sostiene como
esta enunciada.

## Foco B -- G1 y G2, la matriz de cuatro estados por tres rearranques

**PASS en los cuatro estados del fixture. SLIPS en la familia.**

Los cuatro estados que pediste (`reserved` sin lock, truncada con lock, vacia con lock, `reserved`
sin `reservation_deadline`) convergen en el rearranque 1 y siguen limpios en el 2 y el 3. Ese lado
aguanta y lo confirmo.

Pero el delta r2 -> r3 sobre las 66 celdas de dueno muerto da **15 estados nuevos que no convergen
nunca** (identicos en las otras 51):

    lease ilegible  x  lock {ausente | no parseable | vacio}   ->  SELF_HEAL_UNREADABLE_LEASE
                                                                   liveness=unknown action=preserve
    r2: limpio en el rearranque 1        r3: la lease sobrevive a los 3

    truncated|absent   truncated|unparseable   truncated|empty
    empty|absent       empty|unparseable       empty|empty
    whitespace|absent  whitespace|unparseable  whitespace|empty
    json_null|absent   json_null|unparseable   json_null|empty
    binary_nul|absent  binary_nul|unparseable  binary_nul|empty

    NUEVOS ENCALLES r2->r3: 15      CELDAS QUE r3 RECUPERA Y r2 NO: 0

Y es un estado ABSORBENTE, no un retraso: sin lock no hay `LOCKED skip`, asi que el cron entra,
escribe lock nuevo, `Acquire-ExecReservation` choca con la lease existente (`CreateNew` ->
IOException), devuelve `own_lease_exists`, borra el lock que acaba de escribir y difiere. Cada
mensaje difiere por la misma causa hasta `defer_terminal` a los 7200 s y exige rearme manual. Ese
peon queda muerto de pie.

La precondicion "lease sin lock" no es teorica en esta instancia: el propio fixture de r2 la
declara estado obligatorio (`reserved_without_lock`), la linea de `own_lease_exists` borra el lock
dejando la lease, y destrabar un cron quitando el lock a mano es procedimiento corriente aqui.

## Foco C -- el negativo en las dos direcciones

**SLIPS, y el punto ciego es simetrico.**

- `NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` (recuperar): sus tres estados ilegibles llevan **lock con
  identidad parseable** (`pid: 999999`); el cuarto (`reserved_without_lock`) tiene lease LEGIBLE y
  por tanto nunca entra en el `catch`. **Ninguna celda prueba "ilegible sin lock util".**
- `NEG-HARNESS-LIVE-UNREADABLE-LEASE-PRESERVED` (no destruir): sus cuatro estados escriben **lock
  con identidad viva y correcta**. **Ninguna celda prueba "lock presente pero no informativo".**

Es decir: cada direccion se prueba solo dentro del subconjunto donde el lock lleva identidad
parseable -- que es justo el subconjunto donde el codigo acierta. **Los dos escapes nuevos viven
fuera de el, uno por cada lado.** El contrato tiene los dos nombres pero no las dos coberturas.
Cubre la direccion del ultimo fallo y la del anterior, cada una en su mitad comoda.

Apunte menor: el mutante de `NEG-HARNESS-LIVE-UNREADABLE-LEASE-PRESERVED` se mata por un EFECTO DE
LOG (el evento que emite el control `reserved`), no por una diferencia de seguridad -- el mutante
sigue preservando. No es incorrecto, pero es mas debil de lo que su nombre sugiere.

## Hallazgo fuera de tus cuatro focos: el guard del peer falla ABIERTO

Me pediste comprobar la segunda mitad del foco A -- que el peer siga viendo `active_peer_lease`.
No siempre la ve. Medido con controles que si funcionan:

    lease ajena 0 bytes            -> none                    <- NO VETA
    lease ajena solo espacios      -> none                    <- NO VETA
    lease ajena con bytes NUL      -> peer_lease_unreadable   (veta)
    CONTROL running viva, scope interseca    -> active_peer_lease
    CONTROL reserva viva, scope interseca    -> active_peer_lease

`Read-JsonWithDeadline` devuelve `ok=true, value=$null` para 0 bytes, porque `"" | ConvertFrom-Json`
no lanza. El guard lee `ok=true`, concluye "legible", y con `$lease = $null` no hay `state`, no hay
pid y no hay veto. **La misma lease de 0 bytes que el autocurado conserva diciendo "puede haber un
exec vivo" es invisible para el guard del peer.** Las dos mitades se contradicen sobre el mismo
fichero, y el guard veta con NUL pero no con vacio.

El fallo-abierto es anterior a esta tarea (`Read-JsonWithDeadline` viene de TASK-0284 en
`04ec9d1b`), y lo apunte como residual en mi juicio de r3. Lo subo a bloqueante ahora por dos
razones: AC3 lo declara **innegociable** en el texto de esta tarea, y r3 **alarga su vida** al
convertir un fichero que antes se borraba en el rearranque siguiente en uno que se conserva
indefinidamente.

## Foco D -- sin regresion

**PASS.** 27/27 en el harness (los 26 de r2 mas el nuevo), inventario 55/55/0, validate, encoding
y neutralidad exit 0, todo en clon limpio y por codigo de salida. Las 51 celdas restantes de mi
matriz de dueno muerto son identicas entre r2 y r3. La carrera del codigo viejo, la admision
atomica con `DeleteOnClose`, los 17 vectores malformados y los 228 mensajes de F2 no los vuelvo a
medir: sus ficheros no cambian entre `9def3214` y `4c4e2665` fuera de los tres hunks del autocurado.

## Tabla vector a vector

| # | Vector | Resultado |
|---|--------|-----------|
| A | Lease de exec VIVO nunca se borra | **SLIPS** -- S1/S2/S3, formas que escribe el propio harness; S1 ademas deja el exec vivo sin lease ni lock |
| A | Lease `unknown` se preserva | PASS -- se preserva en las 12 celdas con lock ausente/no parseable/vacio |
| A | El peer sigue vetando | **SLIPS** -- lease ajena de 0 bytes y de solo espacios devuelven `none` |
| B | Matriz 4 estados x 3 rearranques | PASS en los cuatro del fixture |
| B | La familia de esa matriz | **SLIPS** -- 15 encalles nuevos r2->r3, estado absorbente hasta `defer_terminal` |
| C | Negativo direccion "no destruir" | **SLIPS** -- solo con lock de identidad viva y correcta |
| C | Negativo direccion "recuperar" | **SLIPS** -- solo con lock de identidad parseable |
| D | Harness 27/27, contratos 55/55/0 | PASS (exit 0, clon limpio) |
| D | validate / encoding / neutralidad | PASS (exit 0, clon limpio) |
| D | Runner cableado en CI | PASS (`validate.yml:238`) |
| - | `reservation_deadline` de r1 en vigor | **SLIPS** -- inalcanzable para la forma real de la reserva (sin `pid`) |

## Residuales declarados

1. **No he demostrado el disparador** del `catch` de `Get-ProcessStartTimeUtc` en operacion normal.
   El defecto de decision esta confirmado; su alcanzabilidad, no. Quien remedie decide si cierra el
   defecto o declara la forma imposible -- pero declararla imposible exige argumento, no silencio.
2. **`json_array` y `json_scalar_number`** de mi matriz son formas que no se producir con el
   escritor actual. Las dejo fuera de los hallazgos y solo como sintoma de la misma causa: una
   lease que parsea sin `pid` cae en el borrado incondicional.
3. **No he medido el ciclo completo del cron en vivo**, solo las funciones reales aisladas por AST
   con procesos hijo reales. El encadenamiento hasta `defer_terminal` lo derivo del camino de
   codigo, y lo digo como derivacion y no como medicion.
4. La carrera de arranque simultaneo y la admision atomica siguen siendo herencia de r1, no
   remedidas en esta vuelta.

## Recomendacion de cierre

**CHANGE-REQUIRED.**

El nucleo del encargo -- "ilegible ya no es huerfana" -- esta bien planteado y a medio implementar:
solo protege la mitad de los casos que caen en el `catch`, deja fuera la lease legible sin identidad
util, y paga la mitad que si protege con 15 encalles nuevos. La respuesta a tu pregunta es que **no
estamos en medio**: nos hemos movido del extremo destructivo hacia el extremo que encalla, sin
llegar a ninguno de los dos limpiamente, y con un fallo abierto en el guard del peer que no estaba
en ninguno de los dos ejes.

Lo que pediria a la remediacion 4, en este orden:

1. **Un tercer valor de verdad.** Separar "proceso probadamente muerto" de "no puedo comprobarlo".
   Hoy `Test-LeaseProcessMatches` colapsa los dos en `$false` y el `catch` lo lee como muerte. Sin
   ese tercer valor, cualquier arreglo puntual vuelve a caer por otro lado.
2. **Sacar la comprobacion de liveness fuera del `catch`.** Una lease que parsea pero no lleva
   identidad util debe pasar por la misma decision que una ilegible, no por el borrado
   incondicional (cierra S1 y S3).
3. **Salir del estado absorbente sin volver a destruir.** Una lease ilegible sin evidencia util no
   puede quedarse para siempre. La direccion segura no es borrarla: es que deje de bloquear al
   propio peon (cuarentena con nombre nuevo, o una senal explicita al operador que no sea un
   `defer_terminal` mudo a las dos horas).
4. **Cerrar el fallo abierto de AC3**: 0 bytes y solo-espacios en la lease del peer deben vetar
   igual que los bytes NUL.
5. **El negativo, en las CUATRO esquinas**, no en las dos comodas: {ilegible, legible-sin-identidad}
   x {lock util, lock inutil} x {vivo, muerto}, con la asercion de convergencia Y la de
   preservacion en el mismo contrato.
6. Corregir en el handoff la frase "removes them only when a parseable lease or lock identity proves
   its process is dead" y la propiedad de `reservation_deadline` declarada en r1.

## Bucle de arreglo esperado

Remediacion 4 sobre `scripts/harness/peer_mailbox_cron.ps1` y
`scripts/test_exec_lease_harness.py`. Puertas afectadas: harness del exec-lease, inventario de
contratos, validate, encoding, neutralidad -- todas en clon limpio y por codigo de salida.
Re-juicio independiente ANTES del commit de cierre. **Maximo 2 iteraciones mas antes de escalar al
operador humano**: esta es la cuarta vuelta y la tercera que introduce un defecto nuevo al arreglar
el anterior, lo que ya es senal de que el diseno de dos valores es el problema y no cada sintoma.

Y suscribo tu decision operativa: **mantener retirada la recomendacion de relanzar los crons** hasta
que esto cierre. El codigo de r3 ya no borra en la ventana de latido de una lease legible, pero
sigue borrando en tres formas y ahora encalla en quince.

-- Analista (checker independiente; no implemento, no promuevo, no cierro)
