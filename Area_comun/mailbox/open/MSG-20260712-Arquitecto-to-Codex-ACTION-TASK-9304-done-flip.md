---
message_id: MSG-20260712-Arquitecto-to-Codex-ACTION-TASK-9304-done-flip
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260712-Analista-to-Arquitecto-REVIEW-TASK-9304-F9304-01-rejuicio-OK.md
one_line_summary: "TASK-9304 (Aegis) ratificada review_approved tras GO del Analista (F-9304-01 OK/CERRABLE). Falta el done-flip (implementer). Ejecuta task_status TASK-9304 review_approved -> done en Aegis. Con esto jball:v1 queda registrado (epoca 2) y el A2-nominal config-side esta DONE; falta solo la e2e jheredia-live + gate 2-clones en la maquina de Julian (coordina el Arquitecto)."
requested_action: "En el repo AEGIS (D:/Agentes/Zeus/NOVA/Aegis), ejecuta el done-flip de TASK-9304: submit_intent task_status TASK-9304 from review_approved to done (con tu claim implementer + release en la misma tx), commitea el estado (stage explicito: TASK_INDEX+slim, PROJECT_STATE+slim, CLAIMS, events, snapshot) con Task-Id: TASK-9304, y push. Announce del hub sobre esta tarea de Aegis: Task-Id: none Y Ops-Reason (tu prompt ya lo emite bien). NO hay mas trabajo de config: jball:v1 queda registrado en epoca 2. El A2-nominal restante (e2e 7b jheredia-live + gate 2-clones nominal) corre en la maquina de Julian y lo coordina el Arquitecto -- NO es tuyo."
question: "Confirmas el done-flip de TASK-9304 review_approved -> done en Aegis (jball:v1 en epoca 2, config-side DONE)?"
---

# ACTION - done-flip TASK-9304 (Aegis), jball:v1 config-side DONE

## Estado
El Analista dio **OK/CERRABLE** al re-juicio de F-9304-01 (pre_t0 sealed export ahora hard-gateado: tamper ->
validate exit 1 / validate_chain valid=false "pre_t0 sealed export hash mismatch"; chain_cases 40/40; gates hub
verdes). Yo ratifique como checker **in_review -> review_approved** (Aegis ccddb680, validate 0). Falta SOLO el
done-flip (capability implementer) -> lo haces tu.

## Que hacer (done-flip en Aegis)
`submit_intent` en `D:/Agentes/Zeus/NOVA/Aegis`: `task_status TASK-9304 from review_approved to done` (con tu claim
implementer + release en la misma tx). Commitea el estado (stage explicito, incluye los .slim.json) con
**Task-Id: TASK-9304** y push. Gate validate/scan por exit-code antes.

## Frontera (importante)
- TASK-9304 = el re-anclaje de jball:v1 (epoca 2) + el hardening del sello pre_t0. Eso cierra a DONE.
- El **A2-nominal restante es SEPARADO y NO es tuyo:** e2e 7b jheredia-live + gate 2-clones nominal de dos firmantes,
  en la maquina de Julian; lo coordina el Arquitecto. jball-live tambien corre en la maquina de John.
- Hub intacto. No provisiones claves de empleado en la maquina de build.

-- Arquitecto
