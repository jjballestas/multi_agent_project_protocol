---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promocion
type: DECISION
task_id: COORD-20260619-CARRIL-A-REVERIFY
from: Operador
to: Arquitecto
status: answered
answered_by: MSG-20260619-Arquitecto-to-Operador-carril-A-promocion-done
requires_response: true
response_owner: Arquitecto
one_line_summary: GO APROBADO. Promueve DECISION-0039/0040/0041 + SPEC-0081 por submit_intent (SemVer MINOR + CHANGELOG). El GO es SOLO de promocion al ledger; NO enciende #4.
requested_action: Promover los 4 drafts por submit_intent como decisiones/SPEC; registrar la tarea diferida DEF-PII con fecha; NO encender flags de #4.
question: Confirmas la promocion limpia (drift 0, gates verdes, SemVer MINOR + CHANGELOG) y que #4 sigue OFF tras promover?
context_refs:
  - Area_comun/mailbox/answered/MSG-20260619-Codex-to-Operador-carril-A-reverify-verdict.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0039-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0081-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0040-gate-dataset.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md
---

# GO APROBADO - promocion Carril A

Arquitecto: GO del operador para PROMOVER Carril A. Base: convergencia de las tres revisiones
(Analista honestidad/metodologia + cruce read-only del asistente + re-verificacion de Codex), todas
aprobables; Codex sin objeciones restantes de codigo-invariante.

## Alcance del GO (leelo: es acotado)

- ESTE GO autoriza UNICAMENTE promover al ledger por submit_intent:
  DECISION-0039, DECISION-0040, DECISION-0041 y SPEC-0081 (intents decision + spec).
- ESTE GO NO enciende #4. Los flags (chain_enabled / agent_signatures_enabled / anchor_enabled /
  event_auth.enabled) siguen en false tras promover. Off-by-default intacto en template y config vivo.
- El encendido de #4 es un GO POSTERIOR y separado, tras el piloto: provisioning (event_auth.keys +
  signature_config.public_keys + anchor remoto/proof) + goldens verdes + manipulation-check (AC2) +
  prueba negativa (AC3, 6 vectores) + rollback ensayado. En su PROPIA ventana de riesgo, sin SA.4 /
  authoritative-teeth / subagents / Capa C.

## Condiciones de promocion

1. SemVer MINOR + CHANGELOG por el cambio visible.
2. Drift 0 y gates verdes (validate_collaboration_state, scan_encoding, scan_domain_neutrality) tras promover.
3. Neutralidad de dominio: Carril A queda documental/gateado; cero reglas fiscales en core o *.template.*.
4. Registrar la tarea diferida DEF-PII (detector de PII real / exporter del plano publicable) en TASK_INDEX,
   con FECHA atada al hito "antes del primer franqueo de #2/#3 contra Core vivo o cualquier publicacion".
   NO se construye ahora (regla 3.4).

## Restriccion de orden DURA (recordatorio)

#4 debe estar ON antes del primer handoff real del modulo-app (la cripto encadenada NO es retrofiteable).
Eso ocurre en el GO posterior de encendido, no en este.

## Opcional en la misma pasada

Puedes reconciliar la anomalia PROJECT_STATE.agents.architect = "Claude" -> "Arquitecto" por el escritor
unico, si no anade riesgo a la promocion.

Reporta de vuelta cuando la promocion este hecha (ids finales de DECISION/SPEC, version, CHANGELOG, drift 0).
Canal ASCII.
