# Veredicto Analista -- TASK-0408

**Veredicto: CHANGE-REQUIRED (un defecto concreto).**

El mecanismo cierra la mitad `in_review` del AC3 -- la del especimen original D-8 (TASK-0378).
La mitad `in_progress`, que el AC3 nombra PRIMERO, queda estructuralmente inerte: el predicado
"sin claim activo" se implementa mirando solo `status` e ignorando `expires_at`, y el arnes nunca
libera un claim. El unico acto que puede desbloquear la alerta es la liberacion manual del claim,
es decir, el acto de quien YA se dio cuenta. El control no puede ser lo que avisa.

No es un juicio de letra-contra-proposito: **el mismo fichero, 160 lineas mas arriba, ya define
"claim activo" incluyendo la caducidad**. El control nuevo usa una definicion mas debil, y la
diferencia abre en la direccion insegura.

## Ancla canonica

    commits bajo revision   0b942c09 (fix/harness) + ab152798 (registro)
    protocol HEAD al juzgar 1ee31cdf
    clon limpio             git clone -s + git checkout 0b942c09
                            D:/Aegis_Scratch/protocol/an0408/cc
    especimen replayado     estado canonico en dbb9294f (2026-08-17T22:40:08+02:00)
    hora del veredicto      2026-08-18 02:10 local (UTC+2)

## Puertas de protocolo -- clon limpio en 0b942c09

    python scripts/validate_collaboration_state.py --root .   exit 0   OK: collaboration state is valid
    python scripts/scan_encoding.py --root .                  exit 0   OK: encoding scan is clean
    python scripts/scan_domain_neutrality.py --root .         exit 0
    python runtime/protocol_replay.py --check-drift --root .  exit 0   PROTOCOL_STATE_DRIFT verdict=CLEAN up_to_seq=9777

Test declarado por el maker, DOS corridas (DECISION-0115):

    test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant   run 1 PASS   run 2 PASS

Las puertas estan verdes. El defecto no lo ve ninguna de ellas -- que es, otra vez, la forma del
propio TASK-0408.

## Reproduccion del defecto sobre el especimen VIVO

Materializo el estado canonico tal cual quedo commiteado en `dbb9294f`, sin editarlo:

    TASK_INDEX.json   TASK-0414  status=in_progress  owner=Codex  reviewer=Analista
    CLAIMS.json       CLAIM-20260817-Codex-TASK-0414-r5             status=active  expires_at=2026-08-17T11:55:04Z
                      CLAIM-20260817-Codex-TASK-0414-r5-neutrality  status=active  expires_at=2026-08-17T12:01:00Z

A las 20:40Z esos dos claims llevaban **8h45m vencidos** y seguian `active`. Cargo por AST las
funciones de PRODUCCION del clon limpio (Get-Field, Write-Utf8NoBom, Write-AtomicUtf8NoBom,
Write-CoordinationAlert, Test-StalledTaskObligations), envejezco el fichero de tarea 10h -- muy
por encima del umbral de 30 min -- y corro el control con PeerId=Codex:

    A  estado TAL CUAL en dbb9294f                          alert_count = 0   alerts = []
    B  MISMO estado, unica delta: los dos claims vencidos
       reetiquetados status=released                        alert_count = 1   alerts = [stalled_task:TASK-0414]

Una sola variable cambia entre A y B: si se honra `expires_at`. El resto -- indice, tarea, umbral,
peer, reloj -- es identico. En A el tablero afirma durante toda la noche que TASK-0414 se trabaja,
y el mecanismo nuevo guarda silencio.

Matriz sintetica independiente (semilla propia: otro id de tarea, otro peer, otros claims), misma
fuente de produccion:

    caso                                                        alertas
    fresco 5 min, sin claims                                        0    <- AC4 negativo: correcto
    viejo 31 min, sin claims                                        1    <- AC3/AC4 positivo: correcto
    viejo 600 min, claim status=active VENCIDO hace 10h             0    <- DEFECTO
    viejo 600 min, MISMO claim con status=released                  1    <- control: solo cambia status
    viejo 600 min, claim active de OTRO participante                0    <- residual R2
    in_review 600 min, PeerId=reviewer, sin claims                  1    <- la mitad que SI cubre

## La contradiccion interna, en el mismo fichero

`scripts/harness/peer_mailbox_cron.ps1`, `Get-AdditionalWorkSignal` (lineas 1149-1153):

    $now = [DateTime]::UtcNow
    foreach ($claim in @($claimsResult.value.claims)) {
        if ([string]$claim.owner -eq $PeerId -or [string]$claim.status -eq "released") { continue }
        try { $expires = [DateTime]::Parse([string]$claim.expires_at).ToUniversalTime() } catch { ... }
        if ($expires -le $now) { continue }        # <-- un claim vencido NO es un claim

`Test-StalledTaskObligations` (linea 1315), 160 lineas mas abajo:

    $activeClaim = @($claims.claims | Where-Object {
        [string]$_.task_id -eq [string]$task.id -and [string]$_.status -eq "active" }).Count -gt 0
                                                   # <-- un claim vencido SI es un claim

`expires_at` es campo declarado del contrato de claim (`Area_comun/protocol/COMMUNICATION_PROTOCOL.md`)
y esta poblado en los 19 claims del ledger. No es un campo opcional que el maker pudiera no ver.

Y el arnes **no libera claims**: no hay ninguna ruta de escritura a `CLAIMS.json` en el fichero. Un
exec muerto deja su claim `active` para siempre. Por eso el efecto no es "el aviso llega tarde":
es que para toda obligacion `in_progress` el aviso solo puede llegar despues de que alguien ya
haya actuado.

## Tabla vector por vector

    AC / pregunta                                          resultado
    AC1  el verde sobre un tablero que miente               PASS  validate exit 0 sobre el estado A
    AC2  RETRY_EXHAUSTED deja rastro durable                PASS  alerts.json legible sin abrir el log del cron
    AC3  in_progress/in_review sin claim > N min            SLIPS in_review PASS; in_progress inerte (defecto)
    AC4  negativo en las dos direcciones                    PASS  fresco 0 / viejo 1, con semilla propia
    AC5  resurreccion por REENVIO documentada               PASS  medido, ver Q4
    Q1   ventana de aviso antes de las 12h                  NO -- y peor que lo sospechado (ver abajo)
    Q2   claim vencido pero active: fail-open?              SI -- confirmado, A/B sobre estado real
    Q3   el mutante mata por CONDUCTA                       PASS  sobrevive a perturbar la semilla
    Q4   REENVIO conserva la razon de muerte                PASS  medido

### Q1 -- la respuesta es mas dura que la pregunta

Preguntas si existe alguna ventana en la que esta implementacion habria avisado antes de las 12h.
**No existe ninguna ventana, ni a las 12h ni nunca.** Tu hipotesis era que el claim activo tapaba
la senal hasta que expirase; medido, la expiracion no la destapa, porque el control no la mira.
En el replay A el silencio es total en t+10h y lo seguiria siendo en t+40h. La senal solo aparece
cuando alguien libera el claim -- y eso ya es el desenlace, no el aviso.

Las formas 0 y 1 (hard_cap tras 1h51m y 3h37m de trabajo real) son ademas invisibles por un segundo
motivo independiente: `EXEC_EXIT -1 outcome=transient` no agota reintentos, asi que `retry_exhausted`
tampoco escribe nada. La forma 2 (`RETRY_EXHAUSTED attempts=3`) es la unica que el mecanismo caza, y
es la barata: 135s de exec perdidos.

### Q3 -- el mutante, verificado contra la semilla

Perturbo la semilla del negativo y vuelvo a matar: peer `Analista` en vez de `Codex`, umbral 7 en
vez de 30, otro nombre de mensaje, otro `task_id`, otro orden de entradas.

    m1  borra la LLAMADA a la alerta terminal (source.replace, 1 vez)
        sano 1 alerta / mutante 0 alertas   -> muere con semilla perturbada: NO es seed-bound
    m2  neutraliza el umbral: if ($ageMinutes -ge $StalledTaskMinutes) -> if ($true)
        el fresco pasa de 0 a 1 alertas     -> lo mata la asercion sana fresh_stalled_count == 0
    m3  neutraliza el ESCRITOR (el efecto, no el punto de llamada): Write-AtomicUtf8NoBom -> $null
        todas las alertas caen a 0          -> lo matan ambas mitades

El negativo es honesto: mata por conducta y no por su propia linea. **Residual del test, y es la
razon por la que el defecto sobrevivio a un mutante verde:** la sonda embebida fija
CLAIMS.json = {"claims": []}, de modo que la rama de supresion por claim -- la linea exacta que
lleva el defecto -- no la ejercita ninguna asercion. El mutante no podia verlo.

### Q4 -- la resurreccion conserva la razon

    exhausted en retry.json, firma intacta           -> processable = 0
    tras anadir el bloque "## REENVIO" al fichero    -> processable = 1
    entrada en alerts.json tras la resurreccion      -> sobrevive, detail = "outcome=transient attempts=3"

Conserva la razon, como afirma el maker. Confirmado.

## Residuales declarados (NO bloqueantes)

- **R1 -- el reloj es la mtime del fichero de tarea.** `$ageMinutes` se mide contra
  `LastWriteTimeUtc` del `.md`, no contra el inicio de la obligacion. Medido: tarea con 600 min de
  atasco, un `Add-Content` cualquiera sobre el fichero -> las alertas caen de 1 a 0. Cualquiera que
  anote la tarea (el maker adjuntando evidencia, el coordinador dejando una nota) silencia el
  control otros 30 min; en un clon fresco toda tarea tiene 0 minutos de edad.
- **R2 -- el claim que suprime no tiene que ser el del obligado.** `$activeClaim` casa por `task_id`
  sin mirar `owner`: el claim del reviewer silencia el atasco del owner y viceversa (medido: 0).
- **R3 -- las alertas no se cierran nunca.** No hay ruta que borre ni resuelva una entrada, y
  `acknowledged` se reescribe `false` en cada toque. `alerts.json` es append-only: pasadas unas
  semanas es exactamente la superficie que el AC4 advierte que "se aprende a ignorar en una tarde".
- **R4 -- la comprobacion solo corre entre execs.** El bucle es de un solo hilo: durante un exec de
  3h37m nadie evalua obligaciones. Es coherente con el diseno, pero acota el mejor tiempo de aviso
  posible al final del exec en curso.

## Arreglo minimo esperado

En `Test-StalledTaskObligations`, que un claim suprima solo mientras siga vigente, reutilizando el
predicado que el propio fichero ya aplica en `Get-AdditionalWorkSignal`: `status -eq "active"` **y**
`expires_at > now`.

Una advertencia sobre la copia: en `Get-AdditionalWorkSignal` un `expires_at` ilegible devuelve
`active_external_claim`, porque alli lo conservador es **bloquear**. Aqui lo conservador es lo
contrario -- **avisar**. Copiar el predicado tal cual invierte la direccion de seguridad. El maker
debe elegir y declarar que hace con un `expires_at` ausente o no parseable.

Y el negativo tiene que crecer con el arreglo: la sonda debe ejercitar la rama de claim con al
menos tres poblaciones -- sin claims, claim vigente, claim vencido -- o el mutante volvera a salir
verde sobre el mismo hueco.

## Bucle de correccion esperado

    remediacion        peer_mailbox_cron.ps1: predicado de vigencia en Test-StalledTaskObligations
                       test_exec_lease_harness.py: la sonda cubre las tres poblaciones de claim
    puertas afectadas  validate exit 0, scan_encoding exit 0, drift CLEAN,
                       test_retry_exhaustion_alert_and_stalled_task_threshold_kill_mutant
    re-juicio          mio, ANTES del commit de cierre, con el A/B sobre dbb9294f reproducido
    maximo             2 iteraciones; a la tercera escala al operador humano

## Recomendacion de cierre

**CHANGE-REQUIRED.** Un defecto, concreto y reproducible. Los residuales R1-R4 los declaro para que
decidas si van a tarea sucesora; no los cuento como bloqueantes.

Si prefieres cerrar 0408 por la mitad que SI cumple y abrir sucesora, es una decision legitima de
coordinacion -- pero entonces que quede escrito que la mitad `in_progress` del AC3 no esta cubierta,
porque hoy el registro dice que si lo esta.

-- Analista, 2026-08-18 02:10 local (UTC+2)
