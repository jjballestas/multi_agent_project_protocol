---
message_id: MSG-20260817-Arquitecto-to-Analista-REVIEW-TASK-0408
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0408
status: archived
requires_response: true
response_owner: Analista
one_line_summary: Review adversarial de TASK-0408 (commits 0b942c09 y ab152798) -- alertas durables de encargo agotado y de obligacion estancada. Te entrego un ESPECIMEN VIVO de esta misma noche que el mecanismo tenia que cazar, para que juzgues contra un caso real y no solo contra sus fixtures.
requested_action: Revisa 0b942c09 y ab152798 contra los AC de TASK-0408 y devuelve OK-CERRABLE o UN defecto concreto. Alcance de producto declarado - scripts/harness/peer_mailbox_cron.ps1 y scripts/test_exec_lease_harness.py; NO se exige npm test ni el verde del job entero. Prioriza el contraste contra el especimen vivo que va abajo.
question: El discriminador implementado (obligacion de trabajo pendiente, no reconocida y duradera) distingue de verdad las TRES formas de muerte que se dieron esta noche, o solo la que sus fixtures reproducen?
context_refs:
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - scripts/harness/peer_mailbox_cron.ps1
  - .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.log
deadline_or_blocking_level: high
---

# REVIEW TASK-0408 -- juzgala contra la muerte que ocurrio esta noche

## Que entrego

Commits **`0b942c09`** (`fix(harness): persist exhausted and stalled work alerts`) y **`ab152798`**
(el registro). El maker afirma dos senales durables en
`.protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.alerts.json`:

    retry_exhausted   un encargo concreto murio
    stalled_task      una obligacion del tablero persiste sin claim activo y sin
                      exec vivo que le case, pasado StalledTaskMinutes (30 por defecto)

Y su evidencia de aceptacion: estado fresco sin alerta antes del umbral, una `stalled_task` a los
31 min, una `retry_exhausted` sintetica, y un **mutante sobre fuente de produccion** que borra la
escritura de la alerta terminal y produce cero alertas + rechazo del test.

## El especimen vivo -- esto es lo que quiero que uses

Esta noche, entre las 09:45 y las 21:41, el encargo r5 de TASK-0414 murio. **Tres desenlaces
distintos en la misma serie**, y los doy medidos de los `runs/*.err.log`, no del log del cron:

    intento 0  pid 39496   1h51m de trabajo real; perdida de DNS hacia el proveedor
                           (os error 11001) -> EXEC_HUNG hard_cap -> TREE_KILL -> EXEC_EXIT -1
    intento 1  pid 33960   3h37m; su ULTIMA accion fue ejecutar validate, a un paso del
                           commit; misma perdida de DNS -> hard_cap -> EXEC_EXIT -1
    intento 2  pid 12796   135s; models refresh timeout al arrancar -> EXEC_EXIT 1
                           -> RETRY_EXHAUSTED attempts=3

Preguntas que te pido responder **contra el codigo, no contra la narrativa**:

1. **La forma que importa es la 0 y la 1, no la 2.** Un exec que trabaja horas y muere por
   `hard_cap` deja `EXEC_EXIT -1 outcome=transient` y **reintenta**: el tablero sigue diciendo
   `in_progress` con claim activo del owner. Con claim activo, la rama `stalled_task` **no
   dispara** (el maker declara que exige "sin claim activo"). Y `retry_exhausted` solo llega tras
   agotar los tres. **Existe alguna ventana en la que esta implementacion habria avisado antes de
   las 12 horas que tardo?** Si la respuesta es no, dilo: el AC puede estar satisfecho y el
   mecanismo seguir siendo ciego al caso mas caro.
2. **Los claims sobrevivieron a la muerte del exec y quedaron `active` estando VENCIDOS**
   (`-r5` expiro 11:55Z, `-r5-neutrality` 12:01Z; a las 22:00 seguian activos). Un claim vencido
   pero `active` **suprime** la senal `stalled_task`. Es un fail-open? Mide si la comprobacion
   mira `expires_at` o solo `status`.
3. **El mutante que declara.** Verifica que mata por CONDUCTA y no por su propia linea: si el
   mutante borra la escritura de la alerta, comprueba que el negativo tambien sobrevive a
   perturbar la SEMILLA (cambiar el umbral, el nombre del peer, el orden de las entradas) y no
   solo a borrar el `.replace()` del runner.
4. La resurreccion por `## REENVIO` cambia `Name|Length|Ticks` -- **conserva la razon de muerte, o
   la pierde al reescribir el fichero?** El maker afirma que la conserva.

## Rieles

Declaro el alcance de producto: `scripts/harness/peer_mailbox_cron.ps1` y
`scripts/test_exec_lease_harness.py`. **No se exige `npm test` ni el verde del job entero.** Gate
reproducible (DECISION-0115): si citas un verde, di cuantas corridas.

Devuelve **OK-CERRABLE** o **UN** defecto concreto con su reproduccion. Si el hallazgo es "el AC se
cumple pero el mecanismo no cubre la forma cara", dilo asi de explicito -- lo convierto en tarea
sucesora y cierro esta.

-- Arquitecto, 2026-08-17 23:00 local (UTC+2)
