---
task_id: TASK-0280
title: "[HARNESS][CRITICO] El rollback del exec revierte el LEDGER: transacciones ya aplicadas desaparecen y el agente reporta trabajo que no existe"
type: fix
status: review_approved
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0272, TASK-0277, TASK-0278, DECISION-0022, DECISION-0103]
linked_decisions: [DECISION-0022, DECISION-0103]
file: Area_comun/tasks/TASK-0280-rollback-no-puede-revertir-el-ledger.md
intake:
  type: fix
  goal: "Observado en campo el 2026-07-20 a las 18:33. Un exec aplico correctamente el done-flip de TASK-0278 por el runtime (eventos 5402 a 5404 segun su propio reporte), despues aborto por una condicion no relacionada, y el rollback de TASK-0272 restauro el worktree pre-exec, borrando de paso runtime/state/events.jsonl. Resultado: el agente entrego un informe afirmando que la unidad quedaba cerrada mientras el ledger vivo sigue en 5401 y TASK-0278 sigue en review_approved. El ledger es append-only y es la fuente de verdad; un rollback de worktree no puede tratarlo como un fichero mas. La consecuencia no es solo perder trabajo: es producir un reporte ATESTADO que afirma algo que el ledger no respalda, que es exactamente la clase de fallo que esta metodologia existe para impedir."
  acceptance:
    - "El rollback del exec NO restaura runtime/state/events.jsonl ni el resto del estado del ledger a su version pre-exec; el log firmado es append-only y queda fuera del alcance de la restauracion."
    - "Si el exec aplico eventos y despues aborta, el harness lo DECLARA en su senal (los eventos aplicados quedan y se reportan), en vez de dejar al agente afirmando trabajo que ya no existe."
    - "Ningun camino del rollback puede dejar el ledger y el estado derivado en desacuerdo: si tras el rollback el estado derivado ya no corresponde al log, el harness lo detecta y lo senala en vez de continuar en silencio."
    - "Negativo permanente: exec que aplica una transaccion de ledger y despues aborta por precondicion; el evento sobrevive, el reporte lo refleja y el mensaje sigue siendo reintentable sin duplicar el trabajo ya aplicado."
    - "ENMENDADA (firmada por el Operador 2026-07-21 00:25, sustituye a la original de esta linea) Negativo permanente del caso inverso: un exec que NO aplico ningun evento revierte su propio residuo, pero ante cualquier ambiguedad -- evento que nombra ficheros, linea ilegible en cualquier posicion, transaccion que crea o borra -- NO revierte: deja el residuo, lo declara en el log y lo deja recuperable."
    - "ANADIDA (firmada por el Operador 2026-07-21 00:25) El harness no puede emitir ROLLBACK_LEDGER_PRESERVED sin verificar contra disco que lo preservado existe; un exito no verificado es un fallo."
    - "Espejo en el harness generico del export born-operational."
  verification_cmd:
    - "Runner de la suite del reintento (examples/, patron run_*.py) en verde con los negativos nuevos"
    - "Sandbox E2E: transaccion aplicada mas aborto posterior, el evento permanece en el log"
    - "python scripts/validate_collaboration_state.py"
    - "python scripts/scan_encoding.py"
    - "python scripts/scan_domain_neutrality.py"
  scope_routes:
    - scripts/
    - examples/
    - personal/Codex/
    - personal/Analista/
  out_of_scope:
    - "Reescribir o re-firmar eventos existentes - PROHIBIDO."
    - "Cambiar el modelo de transacciones del runtime (submit_intent ya es atomico con rollback propio) - FUERA, el defecto es del rollback de worktree del harness."
    - "Re-genesis o cualquier toque al config pineado - PROHIBIDO (epoch 1.14.0, genesis 2E35F26E, dataset N=500)."
    - "Unidades RESERVADAS del preregistro N=6 - FUERA."
  risk: high
  estimate: S
---

# TASK-0280 - Un rollback no puede borrar el libro

Secuencia real del 2026-07-20:

1. 18:33, el exec de Codex aplica el done-flip ratificado de TASK-0278 por la via
   gobernada. Sus eventos existen mientras el exec vive.
2. El mismo exec intenta despues reproducir el `prune_state --apply` que le pedi, choca
   con el fallo de TASK-0277 y decide abortar.
3. El rollback de TASK-0272 restaura el worktree al estado pre-exec. `events.jsonl` es un
   fichero del worktree, asi que vuelve atras con todo lo demas.
4. Su informe dice, de buena fe, que TASK-0278 quedo cerrada citando los seq 5402 a 5404.
   El ledger vivo termina en 5401 y la unidad sigue en `review_approved`.

Nadie mintio y sin embargo el reporte era falso. Esa es la gravedad: no es perdida de
trabajo, es **atestacion sin respaldo**, producida por el propio mecanismo de seguridad.

Remediacion iteracion 1: una unica primitiva compartida captura `seq` y SHA-256 de la
cabeza del event log. El rollback solo excluye rutas gobernadas cuando esa cabeza avanzo,
preserva cambios trackeados sin resucitar altas staged, y contrasta otra vez la cabeza
antes del reset y despues de restaurar.

Remediacion iteracion 2: las rutas preservadas se derivan de los eventos aplicados en la
ventana, no del tipo de cambio que informa git. Esto conserva tambien movimientos
firmados de mailbox (baja en `open/` y alta en `archived/`). La primitiva de cabeza tolera
una ultima linea desgarrada y el harness emite `ROLLBACK_DEFER reason=ledger_torn_tail`
sin mutar la cola. Ambos casos tienen negativos permanentes en el sandbox de reintentos.

Relacion con lo demas: el rollback de TASK-0272 sigue siendo correcto para lo que se
diseno, deshacer el residuo staged de un exec abortado. El error es de alcance, no de
concepto. El ledger firmado no es residuo: es la unica cosa del arbol que no se puede
deshacer restaurando un fichero.

## ENMIENDA FIRMADA -- iteracion 3 con acceptance cambiado (2026-07-21 00:25)

El tope de dos iteraciones se agoto con NO-GO. El patron del fallo, y no el caso concreto,
es lo que se escalo: tres versiones cerrando los casos que el veredicto anterior ENUMERO y
abriendo los adyacentes que nadie enumero -- rutas, luego tipo de cambio, luego nombre de
evento. Una cuarta ronda del mismo enfoque compraba el siguiente caso adyacente, no la
garantia.

**El Operador firma el cambio de enfoque a ROLLBACK CONSERVADOR POR DEFECTO.** Ante
cualquier ambiguedad el rollback no revierte: deja el residuo, lo declara y lo deja
recuperable. El principio que lo sostiene: **perder trabajo es peor que dejar basura**, y el
20-jul hubo evidencia de los dos danos -- la basura siempre fue reparable, la perdida no.

Que cambia respecto a la aprobacion original, para que quede explicito:

- **Acceptance**: la linea del caso inverso prometia rollback COMPLETO del worktree cuando
  el exec no aplico eventos, tal y como lo dejo TASK-0272. Bajo esta enmienda esa promesa se
  invierte para el caso ambiguo. Se anade ademas la prohibicion de emitir PRESERVED sin
  verificar contra disco.
- **scope_routes**: sin cambios.
- **risk**: sigue high; lo que sube es el RESIDUO ACEPTADO, que es decision de politica.
- **Coste conocido y aceptado**: el arbol puede quedar sucio en rutas gobernadas, que es la
  precondicion que DECISION-0020 pide evitar. Queda acotado porque el aborto ya reintenta y
  senala (TASK-0272 y TASK-0278, desplegadas), y quedara recuperable cuando cierre TASK-0275
  (cuarentena en vez de borrado).

Unidad padre de la iteracion: esta misma, TASK-0280. Tope reiniciado por cambio de enfoque
firmado, no por indulgencia con el enfoque anterior.

## Reparacion F-0280R4-02 -- poder falsador del negativo (2026-07-21)

El brazo ambiguo de `events.jsonl` captura ahora el contenido inmediatamente despues
de que el rollback emite su decision y antes de que el reparador habilite la siguiente
vuelta. La barrera distingue preservacion real de destruccion seguida de reparacion.

Control positivo ejecutado sobre un mutante que vacia `events.jsonl` en la rama
`ledger_unreadable_after_exec`: la suite sale 1 en la nueva asercion, con
`after_rollback=['']` frente al fixture ambiguo completo. Sobre el runner reparado la
misma suite sale 0. No se anadio ningun guard de `torn_tail` y no se redesplego el
harness vivo.
