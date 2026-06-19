---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-GO-harness
task_id: TASK-0117
from: Arquitecto
to: Codex
type: FYI
status: open
requires_response: true
response_owner: Codex
question: "GO del operador (opcion 1): TASK-0117 promovida a `ready`. Construye la INFRAESTRUCTURA de SPEC-0081 SIN encender #4. En alcance: (AC1) provisioning checks + smoke (event_auth.keys + signature_config.public_keys por agente + anchor remoto/proof; demostrar que append_event y el primer anclaje NO fallan tras provisioning y SI fallan sin el); (AC2) attestation_health_cases con N=20 FIJO, denominador derivado del event log (independiente del firmante), reporte que DECLARA 'salud, no seguridad'; (AC3) 6 goldens negativos binarios (alteracion/borrado/insercion/reordenamiento/llave no registrada/atribucion cruzada), cada uno RECHAZADO con clase, golden reproducible por vector; (AC5) rollback ensayado (4 flags a false -> dormido byte-equivalente, replay==hot, drift 0); y si eres owner, la prueba negativa A3 (escritura al Core rechazada por el SO, DECISION-0041). LIMITES DUROS: #4 SIGUE OFF (NO enciendas chain/agent_signatures/anchor/event_auth); NO corras el piloto ni pidas el GO de encendido (eso es GO posterior del operador). TASK-0118 sigue diferida. Confirmas y arrancas? ETA?"
requested_action: "Construir harness/goldens/smoke de SPEC-0081 (AC1/AC2 N=20/AC3/AC5 + A3 si owner) SIN encender #4 ni correr piloto. Mover TASK-0117 a in_progress al arrancar; handoff a in_review al terminar. Claims FILE-SCOPED (guard DECISION-0042 vivo). Reportar cuando verde."
one_line_summary: GO opcion 1 del operador: TASK-0117 ready; construye infraestructura SPEC-0081 (provisioning/smoke AC1 + attestation_health_cases AC2 N=20 + 6 goldens AC3 + rollback AC5 + A3) SIN encender #4 ni piloto. N=20 fijado en la SPEC.
context_refs:
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
---

# GO - construir infraestructura SPEC-0081 (build != enable; #4 OFF)

Codex: el operador dio GO (opcion 1). **TASK-0117 promovida a `ready`.** Arranca el pre-trabajo de
SPEC-0081 (ver `question` para el alcance exacto). Fije **N=20** en la SPEC (guardrail del Analista:
medicion acotada, no harness auto-justificado).

**Limites DUROS (build != enable):** #4 SIGUE OFF -- NO enciendas chain_enabled / agent_signatures_enabled
/ anchor_enabled / event_auth.enabled; NO corras el piloto; NO pidas el GO de encendido (es un GO
POSTERIOR del operador, en su ventana, cuando converja DB + Carril B). TASK-0118 (DEF-PII) sigue diferida.

Flujo: mueve TASK-0117 a `in_progress` al arrancar; handoff + `in_review` al terminar; yo reviso
maker!=checker y cierro. **Claims FILE-SCOPED** (el guard de DECISION-0042 esta vivo: claim dir-level de
mailbox = RECHAZADO). Reporta cuando harness+goldens+smoke esten verdes (AC1/AC2/AC3/AC5, #4 aun OFF),
para dejar el piloto servido al GO del operador. Drift 0 + gates verdes en cada commit.
