---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-doneflip-0262-y-GO-0263
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS pasos. (A) DONE-FLIP de TASK-0262: ratificada a review_approved con GO del checker (Analista-TASK-0262-remediation-iter1-verdict = OK-CLOSABLE; agent_id->agent confirmado 0 residual, no-regresion PASS en los 5 vectores, cross-check con validate_mailbox verde). Haz review_approved->done y libera claims. (B) GO TASK-0263 (C3-bis mecanismo de OFERTA de mejora, ambos carriles), unidad 7 de la tabla 0103, maker=Codex, checker=Analista(Opus), type=feature, risk=medium, estimate=L. Implementa la clausula 3-bis de DECISION-0103: (1) DETECCION de obstacles candidatos sobre AMBOS carriles (run-logs del runtime + mensajes REPORTE del mailbox): recurrence_risk 'high', O el MISMO root_cause en dos o mas entregas. El criterio de 'mismo root_cause' debe ser DETERMINISTA y DOCUMENTADO (match exacto o clave normalizada explicita), NUNCA heuristica opaca. (2) OFERTA al humano con el BORRADOR DEL CAMBIO CONCRETO ya redactado (texto de la skill/regla propuesta, no un consejo generico) que CITA los obstacles que la motivan. (3) REGISTRO DURABLE de ofertas y respuestas en ruta gobernada (define la ruta en el diseno, p.ej. JSON en Area_comun/), CONSULTADO antes de ofrecer: una propuesta RECHAZADA o PARQUEADA no se re-oferta salvo evidencia nueva declarada (anti-bucle). (4) CERO auto-aplicacion: el output es una oferta en el reporte/mailbox; el cambio real va por el flujo normal (DECISION + tarea) SOLO si el humano acepta. Ningun agente modifica protocolo ni skill por su cuenta -- es el invariante duro de la clausula. Acceptance/suite: recurrence_risk high -> oferta; root_cause repetido x2 -> oferta; rechazada -> NO se re-oferta; aceptada -> marcada; sin candidatos -> no ofrece nada. Scope: scripts/, runtime/, examples/, Area_comun/protocol/. FUERA: crear/modificar skills o reglas automaticamente (PROHIBIDO por la clausula), los bloques obstacles en si (deps 0258/0259/0261), reservadas N=6, fondo intocable, encender supervised_autonomy/real_invoker. verification_cmd: runner de la suite nueva (examples/, run_*.py) + validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py, exit 0. Entrega 0263 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas el done-flip de 0262 a done y ETA para 0263? Y confirmas (i) el criterio DETERMINISTA y documentado de mismo root_cause, (ii) el registro durable consultado antes de ofrecer (anti-bucle rechazada/parqueada), y (iii) CERO ruta de auto-aplicacion (ofrece, no crea)?"
created_at: 2026-07-23
context_refs:
  - Area_comun/artifacts/Analista-TASK-0262-remediation-iter1-verdict.md
  - Area_comun/tasks/TASK-0263-d0103-c3bis-oferta-de-mejora.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Done-flip de 0262 (GO checker) + GO 0263 (C3-bis oferta de mejora: deteccion determinista + borrador redactado + registro durable anti-bucle + CERO auto-aplicacion)."
---

# ACTION - Done-flip 0262 + GO 0263

Hora local: 2026-07-23 00:55. 0262 cerrada: GO/OK-CLOSABLE (agent_id->agent, 0 residual,
no-regresion PASS, los 3 ejemplos siguen pasando validate_mailbox de 0261).

## (A) Done-flip TASK-0262

Esta en `review_approved`. Haz `review_approved -> done` y libera claims.

## (B) GO TASK-0263 -- C3-bis mecanismo de OFERTA de mejora (ambos carriles)

Ficha: `Area_comun/tasks/TASK-0263-...md`. Es la unidad que CIERRA EL BUCLE DE APRENDIZAJE:
los obstacles no valen por estar, valen por producir cambios. El nucleo:

1. **Deteccion** sobre run-logs (runtime) + REPORTE (mailbox): `recurrence_risk: high` O el
   MISMO `root_cause` en >=2 entregas. Criterio de igualdad **DETERMINISTA y DOCUMENTADO**
   (match exacto o clave normalizada explicita), nunca heuristica opaca.
2. **Oferta** con el **borrador del cambio concreto** ya redactado (la skill/regla propuesta,
   no un consejo) que CITA los obstacles que la motivan.
3. **Registro durable** de ofertas+respuestas en ruta gobernada, CONSULTADO antes de ofrecer:
   rechazada/parqueada NO se re-oferta salvo evidencia nueva declarada (anti-bucle).
4. **CERO auto-aplicacion** -- el invariante duro: ofrece, NO crea. El cambio real va por
   DECISION + tarea solo si el humano acepta.

## Angulo para el checker (cuando entregues)

El invariante critico es (4): que NO exista ninguna ruta por la que un obstacle se convierta en
un cambio de protocolo/skill sin paso humano. Y (3): que una oferta rechazada no vuelva en bucle.
Y (1): que el criterio de mismo root_cause sea reproducible, no opaco. Suite con los 5 casos.

## Guardas

Scope: `scripts/`, `runtime/`, `examples/`, `Area_comun/protocol/`. PROHIBIDO auto-crear
skills/reglas. Reservadas N=6 y fondo intocable FUERA. No encender supervised_autonomy.
Handoff con gates declarados. ASCII.
