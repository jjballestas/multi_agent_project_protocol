---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0263
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0263 (C3-bis mecanismo de OFERTA de mejora, ambos carriles), impl commit f97e0e1. SIN PRODUCTO EN ALCANCE. Modulo runtime/improvement_offers.py + doc Area_comun/protocol/IMPROVEMENT_OFFERS.md + registro Area_comun/protocol/improvement_offer_registry.json + suite examples/improvement_offer_cases/. Verifica: (1) INVARIANTE DURO -- CERO AUTO-APLICACION (el punto que mas importa): busca CUALQUIER ruta de codigo por la que un obstacle se convierta en un cambio de skill/regla/protocolo, o cree tasks/decisions, o emita intents al ledger, SIN paso humano. El handoff afirma que el modulo no puede editar skills/reglas ni submit intents; PRUEBALO leyendo los imports/llamadas (no debe importar submit_intent/ledger_ops ni escribir en skills/ ni en decisions/ ni tocar el harness); la unica salida debe ser una oferta (texto) + el registro. Si encuentras UNA ruta de auto-aplicacion, es NO-GO. (2) CRITERIO DETERMINISTA de mismo root_cause: NFKC+casefold+trim+collapse+igualdad exacta; confirma que es REPRODUCIBLE (mismos inputs -> misma clave) y que NO sobre-fusiona (root_causes distintos -> claves distintas) ni sub-fusiona (mismo root con diferencias triviales de formato/unicode/espacios -> misma clave). Ataca con casos unicode/espacios. (3) ANTI-BUCLE: una oferta RECHAZADA o PARQUEADA NO se re-oferta salvo evidencia nueva declarada + --new-evidence explicito; una ACEPTADA nunca recurre; el registro se consulta ANTES de ofrecer. Construye: ofrecer -> rechazar -> re-evaluar sin evidencia nueva -> NO re-oferta; con evidencia nueva + flag -> re-oferta. (4) AMBOS CARRILES: run-logs del runtime (JSON/JSONL) Y mensajes REPORTE del mailbox alimentan el MISMO evaluador. (5) Los 5 casos de acceptance: recurrence_risk high -> oferta; root_cause x2 -> oferta; rechazada -> no re-oferta; aceptada -> marcada; sin candidatos -> nada. (6) La oferta incluye el BORRADOR del cambio concreto (texto de skill/regla) + CITA los obstacles que la motivan. Gates: runner de la suite + validate + scan_encoding + neutralidad, exit 0. Veredicto GO/NO-GO con el vector exacto por punto."
question: "Existe ALGUNA ruta de auto-aplicacion (obstacle -> cambio de skill/regla o intent al ledger sin humano)? Es el criterio de root determinista y reproducible sin sobre/sub-fusion? Y el anti-bucle impide re-ofertar una rechazada salvo evidencia nueva declarada?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0263-d0103-c3bis-oferta-de-mejora.md
  - Area_comun/handoffs/HANDOFF-TASK-0263-codex-to-arquitecto.md
  - runtime/improvement_offers.py
  - Area_comun/protocol/IMPROVEMENT_OFFERS.md
one_line_summary: "Review 0263 (C3-bis oferta de mejora): CERO auto-aplicacion (invariante duro) + criterio root determinista sin sobre/sub-fusion + anti-bucle rechazada/parqueada + ambos carriles + borrador citado. Sin producto en alcance."
---

# REVIEW - TASK-0263, C3-bis mecanismo de oferta de mejora

Hora local: 2026-07-23 01:10. Impl f97e0e1. **Sin producto en alcance**.

## Que probar (el (1) es el que decide)

1. **CERO auto-aplicacion (invariante duro).** Ninguna ruta obstacle -> cambio de
   skill/regla/protocolo, ni crear tasks/decisions, ni submit intents. Leelo en el codigo
   (imports + llamadas): no submit_intent/ledger_ops, no escribir skills/decisions, no tocar el
   harness. Salida = oferta (texto) + registro. Una sola ruta de auto-aplicacion -> NO-GO.
2. **Criterio determinista.** NFKC+casefold+trim+collapse+exacto: reproducible; sin sobre-fusion
   (distintos -> distintas) ni sub-fusion (mismo con formato/unicode/espacios triviales ->
   misma). Ataca unicode/espacios.
3. **Anti-bucle.** rechazada/parqueada no vuelve salvo evidencia nueva + --new-evidence;
   aceptada nunca recurre; registro consultado ANTES. Construye ofrecer->rechazar->re-evaluar.
4. **Ambos carriles.** run-logs (JSON/JSONL) Y REPORTE alimentan el mismo evaluador.
5. **5 casos** de acceptance.
6. **Oferta** con el borrador concreto + cita de obstacles.

## Guardas

El corazon de C3-bis es 'ofrece, no crea': si hay cualquier grieta por la que el mecanismo
aplique un cambio sin humano, es NO-GO aunque todo lo demas pase. Veredicto con el vector exacto.
