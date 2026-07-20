---
task_id: TASK-0270
title: "[LEDGER] Endurecimiento del event log: verificacion post-write del evento propio + coherencia idempotencia-vs-estado (cierra el evento-perdido silencioso y el skip mudo)"
type: infra
status: done
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0022, DECISION-0103]
linked_decisions: [DECISION-0022]
file: Area_comun/tasks/TASK-0270-ledger-postwrite-idempotencia-coherencia.md
intake:
  type: infra
  goal: Cerrar las dos grietas de integridad del event log cazadas en vivo el 2026-07-19 (incidente del fix-loop 0257, aprobacion del Operador 2026-07-20), (a) un intent aplicado puede PERDER su evento si otro escritor cruza la ventana de append (exit 0 + efecto de archivo, evento ausente del log, chain internamente consistente = perdida invisible); (b) el reintento con intent byte-identico es SKIPEADO por la idempotencia por contenido sin verificar que el estado lo refleje (exit 0, cero eventos, estado sin cambiar). Ambos exitos aparentes; la divergencia solo la cazo el validador.
  acceptance:
    - (a) POST-WRITE, submit_intent re-lee el tail del log tras escribir y verifica que SU(S) evento(s) estan presentes (por seq/aggregate/idempotency); si falta alguno, exit distinto de 0 con error explicito que nombra el evento perdido; cubre intents sueltos y transacciones --intents completas.
    - (b) COHERENCIA, la rama de idempotencia verifica que el ESTADO refleja el intent antes de responder ya-aplicado (task_status: status actual == to; claim: estado del claim consistente; mailbox_archive: mensaje en archived); si el estado NO lo refleja (evento perdido), re-aplica con evento nuevo o falla con error distintivo -- JAMAS skip silencioso.
    - CAUSA RAIZ, la ventana del lock de append que permitio el cruce queda diagnosticada y cerrada (el ciclo read-modify-write completo de cada escritor bajo el lock) o, si el cierre total no es viable, el residual queda declarado con racional y el post-write (a) como compensacion.
    - Suite de concurrencia en examples/ que reproduce el escenario real (dos escritores cruzados; evento perdido inyectado -> (a) lo caza; idempotencia con estado divergente inyectado -> (b) re-aplica o falla ruidoso), mas regresion de las suites de intents existentes en verde.
    - Cero cambios de semantica para el caso feliz (mismos exit codes y salidas cuando todo esta bien); compatibilidad con los harnesses de los peers sin relanzamiento obligatorio.
    - Neutralidad, validate y encoding verdes.
  verification_cmd:
    - Runner de la suite de concurrencia nueva en verde (evento-perdido cazado + skip-mudo eliminado)
    - Runners de las suites de intents existentes (intent_flow, intent_tx, protocol_replay) en verde
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - runtime/submit_intent.py
    - runtime/eventlog.py
    - runtime/protocol_replay.py
    - examples/
  out_of_scope:
    - Cambiar el formato de eventos o el chain (prev_hash) - FUERA.
    - El harness del checker (TASK-0271) - FUERA.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: medium
  estimate: M
---

# TASK-0270 - [LEDGER] Post-write + coherencia idempotencia-vs-estado

Origen: incidente real del 2026-07-19 (fix-loop 0257) reportado en
MSG-20260719-Arquitecto-to-Operador-REPORTE-iter2-y-hallazgo-ledger; oferta de mejora
C3-bis ACEPTADA por el Operador en orden directa del 2026-07-20 ("apruebo (a) y (b)").
Evidencia forense: eventos de un lote con el flip ausente pese a exit 0 (seq 4949-4953
sin el task_status), y reintento identico skipeado hasta que se uso idempotency_key
fresco. Leccion operativa ya en memoria de agentes: verificar tail del log ademas del
exit code -- esta unidad convierte esa disciplina manual en garantia mecanica.
Rutas disjuntas de 0267/0268 (.githooks) y 0258 (turn_schema): puede correr en paralelo.
