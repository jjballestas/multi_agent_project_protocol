---
id: TASK-0424
title: El arnes carga al presupuesto del encargo los fallos del PROVEEDOR, y descarta la prueba que los distingue
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0424-el-arnes-carga-al-encargo-los-fallos-del-proveedor.md
created: 2026-08-21
reviewer: Analista
intake:
  type: fix
  goal: >
    Get-ExecOutcomeClass (scripts/harness/peer_mailbox_cron.ps1:1441) clasifica CUALQUIER salida
    distinta de cero como "transient" sin mirar la causa, y el llamador (:1707-1710) suma un intento
    al encargo por cada una. Un exec que muere en 3-4 segundos porque el PROVEEDOR rechazo la
    peticion -- "You've hit your usage limit", cuota agotada, corte de red -- consume vidas de una
    tarea que no ha ejecutado ni una linea. Reportado por la instancia NOVA (2026-08-21T21:30Z):
    su maker llego a attempts 2 de 3 sin haber empezado, y la causa solo estaba en
    runs/<ts>-<msg>.err.log, no en el log del cron, asi que desde fuera el cuadro es identico al de
    una tarea que falla. El agravante esta en el propio codigo: la salida de error SI se captura y
    SI se pasa a la funcion como $InvokerDiagnostics (:1693-1695), y el cuerpo de la funcion NUNCA
    la usa. La prueba que discrimina esta en la mano en el punto exacto de la decision y se tira.
  acceptance:
    - "AC1: un exec que termina por fallo declarado del proveedor (patron reconocible en la salida
      de diagnostico del invocador) NO incrementa attempts del encargo y NO lo acerca al agotamiento.
      Acreditar con el par: mismo encargo, dos execs con fallo de proveedor -> attempts sigue en su
      valor previo; dos execs con fallo real de la tarea -> attempts sube dos."
    - "AC2: NO se consume el mensaje. Un fallo de proveedor deja el encargo REINTENTABLE; jamas lo
      marca seen ni lo da por entregado. La guarda existente -- que la salida de diagnostico nunca
      determine el CONSUMO de un mensaje (comentario en :1437-1438) -- se conserva intacta y se
      acredita con su negativo: un diagnostico que dijera 'hecho' no consume nada."
    - "AC3: el reconocimiento es por lista EXPLICITA y auditable de senales de proveedor, no por
      heuristica abierta. Un mensaje de error desconocido cae del lado seguro: cuenta como intento
      de la tarea, como hoy. Acreditar el caso desconocido."
    - "AC4: la distincion queda VISIBLE donde se mira. El log del cron emite una linea propia que
      nombra el fallo de proveedor; hoy la unica huella vive en runs/*.err.log y por eso el defecto
      fue invisible durante toda una noche."
    - "AC5: decidir y MEDIR aqui el presupuesto de la clase exit=-1. Test-ExecRetryExhausted
      (:1303) hace terminal en el primer intento todo exec con exit=-1 y outcome transient, que es
      TODO exec que mata el arnes (TREE_KILL por deadline, TREE_KILL post-entrega y el kill de la
      linea 801). Ese cambio entro en TASK-0408 fuera de su alcance y se revierte alli; su sitio es
      esta tarea, con el colateral declarado: un exec que SI escribio en el ledger y murio por el
      techo antes de imprimir su OUTCOME pierde los dos intentos que tenia para aterrizar lo que
      dejo a medias."
    - "AC6: cuando un encargo SI se agota, su salida de la cola deja de ser invisible. Hoy
      RETRY_EXHAUSTED lo saca del reintento y el fichero SIGUE en Area_comun/mailbox/open/ con el
      mismo aspecto que uno pendiente: la instancia NOVA tuvo un GO dos dias asi antes de que
      alguien lo notara, y tuvo que reponer el contador a mano para reanudar sin arriesgar la cola.
      Acreditar que un encargo agotado es distinguible de uno pendiente leyendo solo lo que el
      arnes deja escrito, sin abrir runs/*.err.log."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/
  out_of_scope:
    - "NO se toca la frontera de consumo: la salida de diagnostico sigue sin poder marcar un mensaje
      como entregado. Distinguir un fallo de proveedor es NO cobrarle el intento, no darlo por hecho."
    - "NO se toca el contador de defers ni el defer_terminal: son otra averia (TASK-0387) y van por
      su via."
  risk: medium
  estimate: M
---

# TASK-0424 -- el arnes carga al encargo los fallos del proveedor

## Lo que hace hoy, linea a linea

    :1693  $invokerDiagnostics = Get-Content $stderrPath      <- la prueba se captura
    :1695  Get-ExecOutcomeClass ... -InvokerDiagnostics $invokerDiagnostics   <- y se pasa
    :1436  param(... [string]$InvokerDiagnostics = "" ...)    <- y se recibe
    :1441  if ($ExitCode -ne 0) { return "transient" }        <- y no se mira jamas
    :1707  $attempt = $previous + 1                           <- el encargo paga

`$InvokerDiagnostics` no aparece ni una vez en el cuerpo de la funcion. No es que falte informacion
para distinguir un fallo de proveedor de un fallo de tarea: **la informacion esta en el parametro y
se descarta**.

## Por que es caro y por que no se ve

Tres execs de proveedor caido bastan para agotar un encargo que nunca empezo, y `RETRY_EXHAUSTED`
lo declara muerto con la misma cara que un trabajo intentado tres veces. La unica huella de la causa
vive en `runs/<ts>-<msg>.err.log`, que nadie abre salvo que ya sospeche. Es la misma familia que el
defecto que mordio aqui la noche del 18 al 19: **el presupuesto de reintentos de una tarea se gasta
en fallos que no son de la tarea**.

## La frontera que NO hay que romper al arreglarlo

El comentario de `:1437-1438` esta ahi por un motivo: la salida del invocador **nunca** puede
decidir que un mensaje quedo consumido, o cualquier epilogo ruidoso daria por entregado un encargo
sin hacer. El arreglo correcto es asimetrico y hay que escribirlo asi: un fallo de proveedor
**exime del cobro del intento**, y no habilita ninguna via nueva para consumir el mensaje. AC2
existe para que esa asimetria se acredite y no se pierda en la implementacion.

## Nota anadida el 2026-08-22 -- la consecuencia que lo vuelve caro

El informe completo de NOVA cierra el circulo: el coste no acaba en el intento gastado. Cuando el
tercer intento se quema, `RETRY_EXHAUSTED` saca el mensaje de la cola **en silencio** y el fichero
se queda en `open/` **aparentando pendiente**. Su GO-28-9432 estuvo dos dias en ese estado. Es la
misma forma que nos mordio a nosotros con la review de TASK-0410, y la razon por la que aqui hubo
que armar un vigia que lee el `retry.json`: porque una muerte por agotamiento **no emite commit ni
evento**, y desde el buzon un encargo muerto y uno pendiente son identicos.
