---
task_id: TASK-0272
title: "[HARNESS] Eliminar el seen-burn silencioso: marcar visto SOLO tras ejecucion confirmada, con reintento automatico cuando el aborto fue por pre-gate rojo (ventana ocupada)"
type: infra
status: in_review
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103, DECISION-0020]
linked_decisions: [DECISION-0103, DECISION-0020]
file: Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
intake:
  type: infra
  goal: Cerrar el peor modo de fallo observado en la tanda 0103, el SEEN-BURN SILENCIOSO, los harnesses de cron marcan un mensaje como visto ANTES o INDEPENDIENTEMENTE de que su exec haya hecho trabajo util; cuando el exec aborta legitimamente por pre-gate rojo o ventana ocupada (DECISION-0020, claim ajeno activo, arbol con cambios de peer), el mensaje queda quemado y NADIE reintenta, produciendo quietud indistinguible de una pausa normal (sin error, sin aviso). Reproducido 3 veces en 12h (07:26 cadena de cierres, 09:24 remediacion 0258, y el patron equivalente del 19-jul con la ACTION de remediacion 0257); las 3 se destrabaron a mano por des-seen y 2 las detecto el Operador preguntando, no el sistema. Aplica al harness de AMBOS peers y al export born-operational.
  acceptance:
    - El marcado de visto ocurre SOLO tras ejecucion CONFIRMADA (el exec produjo trabajo verificable, p.ej. commit propio, flip de estado o entrega de mensaje); un exec que aborta por precondicion NO consume el mensaje.
    - Reintento automatico acotado cuando la causa del aborto es una precondicion transitoria (pre-gate rojo, claim ajeno activo, arbol con escritura de peer): backoff simple y tope declarado de reintentos; al agotarlo, EMITE senal (mensaje o marca en el log que el watchdog pueda ver) en vez de callar.
    - CERO quietud silenciosa, tras el tope, el estado del mensaje queda distinguible de procesado-ok (para el Arquitecto y para el watchdog).
    - Taxonomia minima de causas de aborto documentada (transitoria-reintentable vs definitiva-no-reintentable, p.ej. rechazo principiado del checker o negativa por alcance); solo las transitorias reintentan.
    - Idempotencia preservada, un reintento NO puede duplicar trabajo ya aplicado (cruzar contra el estado, no contra el seen).
    - Suite que reproduce el escenario real: mensaje ruteado mientras un claim ajeno esta activo -> el exec aborta -> el mensaje NO queda quemado -> al liberarse la ventana, el siguiente ciclo lo procesa SIN intervencion manual.
    - Espejo en el harness generico del export born-operational.
    - ROLLBACK DEL PROPIO RESIDUO (aporte del Operador 2026-07-20, incidente 11:03 verificado): un exec que aborta DEBE DEJAR EL ARBOL COMO LO ENCONTRO -- unstage y revert de lo que toco antes de rendirse. Sin esto el reintento automatico HEREDA la bomba: el residuo staged del aborto es exactamente la condicion 'cambio ajeno sin commit' que aborta al exec siguiente (realimentacion reproducida: EXEC_EXIT 11:03:45 dejo staged -> EXEC_START 11:03:46 aborto por ese residuo).
    - DISCRIMINADOR de exec-abortado-vs-exec-vivo (aporte del Operador, valida ex-post): la deteccion usa ANTIGUEDAD DEL RESIDUO STAGED (fichero staged e INMOVIL mas de N minutos = exec abortado; fichero cambiando = exec vivo). Descartadas explicitamente por probadas insuficientes: commits (no ven trabajo en vuelo), proceso vivo (no distingue clon limpio ni otra sesion) y CPU (inutil con agentes LLM, el envoltorio local espera en red mientras el modelo piensa).
    - CASO DEADLOCK GATE-PEER declarado y cubierto (observado 2026-07-20 12:00): si el hook exige poda y la poda esta bloqueada por el claim vivo de un peer, el harness/procedimiento debe ofrecer una salida documentada (bypass de un solo commit con los gates de fondo verificados a mano, o liberacion coordinada) en vez de dejar al coordinador sin opciones; queda escrito en la doc del hook.
  verification_cmd:
    - Runner de la suite nueva del reintento (examples/, patron run_*.py) en verde
    - Prueba end-to-end en sandbox, aborto por claim ajeno seguido de procesamiento automatico al liberarse
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - personal/Codex/
    - personal/Analista/
    - scripts/
    - examples/
  out_of_scope:
    - Cambiar el protocolo de mailbox o el formato de mensajes - FUERA.
    - Reintentar abortos DEFINITIVOS (negativas principiadas del checker, rechazos por alcance) - PROHIBIDO, solo transitorias.
    - Unidades RESERVADAS del preregistro N=6 - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: medium
  estimate: M
---

# TASK-0272 - [HARNESS] Fin del seen-burn silencioso

Origen: oferta de mejora C3-bis nacida de la propia tanda 0103. El Operador la levanto
formalmente en MSG-20260720-Operador-to-Arquitecto-COORD-0258-remediacion-sin-avance con
el criterio de la clausula: misma causa raiz DOS veces (de hecho tres) deja de ser
incidente y pasa a candidato de regla. Su formulacion, adoptada aqui: "un marcado de
visto que solo se aplique tras ejecucion confirmada, o una deteccion de cadena quemada
que avise sola" -- esta unidad hace AMBAS.

Evidencia de las 3 recurrencias (envelopes reales de los peers, todos correctos en su
negativa; el defecto es del harness, no del agente):
- 19-jul: exec de Codex sobre la ACTION de remediacion 0257 aborta por claim mio activo.
- 20-jul 07:26: exec sobre la ACTION de cadena de cierres aborta por ledger a medio
  commitear (ventana roja de poda).
- 20-jul 09:24: exec sobre la ACTION docs de 0258 aborta por cambios ajenos en el arbol
  (mi claim de higiene CLAIM-arq-hyg-0847 en vuelo).

En los tres casos el agente hizo lo correcto (DECISION-0020) y el harness lo castigo
quemando el mensaje. El coste medido: ~30-45 min de quietud por episodio, detectada por
el humano en 2 de 3.
