---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-harness-spec0081
type: DECISION
task_id: PROMO-20260619-CARRIL-A
from: Operador
to: Arquitecto
status: answered
answered_by: MSG-20260619-Arquitecto-to-Operador-carril-A-GO-harness-ack
requires_response: true
response_owner: Arquitecto
one_line_summary: GO opcion 1. Promueve TASK-0117 a ready + GO y coordina a Codex para construir la infraestructura de SPEC-0081 (harness/goldens/smoke) SIN encender #4. Scope acotado; #4 sigue OFF.
requested_action: Promover TASK-0117 a ready y dar GO a Codex para construir el harness/goldens/smoke de SPEC-0081; NO encender #4; NO correr el piloto; mantener a Codex activo.
question: Confirmas TASK-0117 en ready + Codex coordinado, con #4 OFF y scope acotado (N y piloto)?
context_refs:
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
---

# GO opcion 1 - construir infraestructura de SPEC-0081 (sin encender #4)

Decision del operador: avanzar la instrumentacion. Promueve TASK-0117 a `ready` y da GO de ejecucion a
Codex para construir la INFRAESTRUCTURA de SPEC-0081, SIN encender #4.

## En alcance (Codex construye)
- Provisioning checks + smoke: event_auth.keys + signature_config.public_keys por agente + anchor remoto/
  proof; demostrar que append_event y el primer anclaje NO fallan tras provisioning (y fallan sin el) -- AC1.
- attestation_health_cases (manipulation-check AC2): >=99% sobre runs legitimos, denominador derivado del
  event log (independiente del firmante). Reporte que DECLARA "salud, no seguridad".
- 6 goldens negativos AC3 (seguridad, binaria): alteracion / borrado / insercion / reordenamiento / llave
  no registrada / atribucion cruzada; cada uno RECHAZADO con clase, golden reproducible por vector.
- Rollback ensayado AC5 (los 4 flags a false -> estado dormido byte-equivalente; replay == hot; drift 0).
- Si Codex es owner: prueba negativa de A3 (escritura al Core rechazada por el SO) -- DECISION-0041.

## Limites DUROS (build != enable)
- #4 SIGUE OFF: NO encender chain_enabled / agent_signatures_enabled / anchor_enabled / event_auth.enabled.
- NO correr el piloto ni pedir el GO de encendido todavia. El encendido de #4 es un GO POSTERIOR del
  operador, en su propia ventana, cuando la convergencia (DB + Carril B) este cerca.
- Scope ACOTADO (guardrail de la revision Analista): fijar N del manipulation-check (N>=20, valor concreto)
  y acotar el alcance del piloto en la SPEC; medicion propia, no un harness que se auto-justifique.
- TASK-0118 (DEF-PII) sigue diferida (antes de captura viva #2/#3 o publicacion); NO se arranca ahora.

## Crons
- Mantener a Codex ACTIVO mientras construye esto; no detener su cron ni el tuyo. El asistente
  (coordinando en nombre del operador) dara la senal "Codex puede parar" cuando el harness/goldens/smoke
  esten verdes, y "puedes detener tu cron" al cierre de fase.

## Reporte de vuelta
Cuando el harness + goldens + smoke esten verdes (AC1/AC2/AC3/AC5 cumplidos en construccion, #4 aun OFF),
reporta por mailbox para dejar el piloto servido al GO del operador. Drift 0 + gates verdes en cada commit.
Canal ASCII.
