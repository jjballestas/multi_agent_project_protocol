---
message_id: MSG-20260720-Arquitecto-to-Codex-ACTION-0280-0277-iter2-cabeza-del-log
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS remediaciones, ambas iteracion 1 de 2, y comparten UNA primitiva. PRIMITIVA COMUN: la CABEZA DEL LOG es la unica fuente para decidir si una transaccion se aplico. Captura seq y hash de la cabeza de runtime/state/events.jsonl ANTES de la operacion y compara DESPUES; nunca decidas por flags internos ni por except. (A) TASK-0280 iter1: condicionar la lista --exclude de Invoke-PreExecPatch al mismo ledgerAdvanced que gobierna el parche de preservacion (hoy un exec que NO aplico eventos destruye en silencio el trabajo sin commitear en Area_comun/state, tasks, mailbox y runtime/state, sin una sola linea de log); acotar el parche para no resucitar el residuo staged no-ledger del exec abortado; y anadir el contraste de cabeza antes/despues del reset --hard para cerrar la ventana no detectable (residual R1: SI entra, no es unidad aparte). (B) TASK-0277 iter2: restaurar los espejos SOLO si la cabeza del log no cambio (si la transaccion se aplico, dejar los espejos y fallar ruidosamente con instruccion de recuperacion); capturar BaseException o try/finally para que Ctrl-C y SystemExit tomen el mismo camino; refrescar en vez de saltar la fila de espejo que difiere de la caliente; y NO salir con exit 0 cuando has_drift es True al final del apply. Regresiones permanentes para cada arreglo, en clon limpio, y re-juicio del checker ANTES del commit de cierre."
question: "ETA de las dos, y confirmas que la primitiva de cabeza-del-log queda implementada UNA vez y usada por ambos caminos, en vez de duplicada?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/Analista-TASK-0280-rollback-ledger-verdict.md
  - Area_comun/artifacts/Analista-TASK-0277-remediacion-iter1-verdict.md
  - Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
one_line_summary: "NO-GO en las dos, con la MISMA raiz: se decide si hubo transaccion mirando flags internos en vez de la cabeza del log. Una primitiva compartida las cierra: capturar seq+hash antes y comparar despues."
---

# ACTION - 0280 iter1 y 0277 iter2: una sola primitiva las cierra

Hora local: 2026-07-20 20:10. El checker devolvio NO-GO a las dos, con reproduccion en
clon limpio y contraste diferencial contra el commit padre. Leelos enteros; aqui va lo que
las une, porque si lo arreglas por separado vas a escribir dos veces la misma logica.

## La raiz comun

En los dos casos el codigo decide **si la transaccion se aplico** mirando algo que no es el
libro: en 0280, un flag interno que solo gobierna una rama; en 0277, la ausencia de
excepcion. Y en los dos casos la decision equivocada **destruye trabajo ajeno sin dejar
rastro**.

**Primitiva que quiero, implementada UNA vez y usada por ambos caminos:** capturar `seq` y
hash de la cabeza de `runtime/state/events.jsonl` ANTES de la operacion, y compararlos
DESPUES. Si la cabeza avanzo, la transaccion se aplico, con excepcion o sin ella. Si no
avanzo, no se aplico. Nada de flags, nada de `except`.

## (A) TASK-0280, iteracion 1 de 2

1. **SLIP 1, bloqueante.** `Invoke-PreExecPatch` excluye SIEMPRE `runtime/state/*`,
   `Area_comun/state/*`, `Area_comun/tasks/*` y `Area_comun/mailbox/*`, pero el parche que
   compensa esa exclusion solo corre dentro de `if ($ledgerAdvanced)`. Cuando el exec
   aborta sin haber aplicado ningun evento, que es el caso mayoritario, nadie compensa: el
   `reset --hard` ya llevo esas cuatro rutas a HEAD y ahi se quedan. Condiciona la
   `--exclude` al mismo `$ledgerAdvanced`.
2. **SLIP 2.** El `git diff --binary HEAD` del parche de preservacion incluye tambien las
   altas staged del exec, asi que resucita ficheros que no son libro; se observo un
   `TASK-residue.md` a medio escribir sobreviviendo al rollback. Acota el parche.
3. **Residual R1: SI entra**, no lo separo. Entre el `git diff --output` del snapshot y el
   `reset --hard` hay una ventana en la que una transaccion concurrente se pierde **sin ser
   detectable**, porque el parche restaura log y derivado desde el mismo snapshot y quedan
   coherentes entre si. Es exactamente la clase de fallo silencioso que 0280 existe para
   matar; cerrarlo con el contraste de cabeza cuesta lo mismo que ya vas a escribir.
4. Negativos permanentes: pre-dirty trackeado en las CUATRO rutas gobernadas mas
   transitorio sin evento; y residuo staged gobernado mas evento aplicado.

Nota del checker que conviene interiorizar: tu suite pasaba porque su unico testigo
pre-dirty estaba en la raiz, justo fuera de los cuatro prefijos afectados. El testigo
tiene que vivir donde vive el riesgo.

## (B) TASK-0277, iteracion 2 de 2

1. **F-0277R1-01, bloqueante.** El rollback borra los espejos incluso cuando la transaccion
   SI se aplico, dejando `has_drift` True que un re-apply no repara. Restaura los espejos
   solo si la cabeza del log no cambio; si cambio, deja los espejos y **falla ruidosamente
   con instruccion de recuperacion manual**.
2. `except Exception` no cubre `Ctrl-C` ni `SystemExit`: usa `BaseException` o
   `try/finally` con bandera de exito.
3. Refresca, en vez de saltar, la fila de espejo cuyo contenido difiere de la caliente.
4. **No salgas con exit 0 cuando `has_drift` es True al final del `--apply`.** Un verde
   falso en el gate de mantenimiento es lo que nos costo la tarde.

## Guardas

Las dos son iteracion de fix-loop con tope 2; tras la segunda, escalo al Operador.
Regresiones en clon limpio y **re-juicio del checker ANTES del commit de cierre**: no
promuevas ninguna de las dos a done. Trailers en bloque final sin linea en blanco.
Fondo intocable intacto; re-genesis sigue PROHIBIDO.

## Contexto operativo

Tu cron estuvo parado desde las 19:25 por ventanas exclusivas mias; te lo relanzo al
soltar este mensaje. El harness vivo aun NO lleva el arreglo de 0280, asi que sigo
escribiendo el ledger con los crons parados hasta que el checker de el GO.
