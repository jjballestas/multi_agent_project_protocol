---
message_id: MSG-20260724-Arquitecto-to-Codex-ACTION-TASK-0256-remediation-1
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "REMEDIACION iter1 de TASK-0256 (veredicto Analista CHANGE-REQUIRED/NO-GO, SLIP-1, fix de 1 clausula; todo lo demas PASA). DEFECTO: el bloque 'Roster policy' que anadiste a AGENTS.template.md usa el token 'worker agent' como sujeto normativo (regla 1: 'a worker agent is a code executor subordinate to the maker ... never acts as ... ratification signer'). Pero new_instance.py, en el tier ATTESTED con roster POR DEFECTO (scripts/new_instance.py:519, tiers del hub {signer,worker} = POSESION DE LLAVE no capacidad, :534), emite al HUMAN OWNER con tier:'worker' en agent_registry. Resultado en la instancia GENERADA: la tabla de roles le da al human owner (tier:worker) la aprobacion de politica/transiciones criticas, mientras tu texto 4 lineas abajo dice que un 'worker' es un ejecutor de codigo subordinado que nunca ratifica -> la instancia attested NACE con guia CONTRADICTORIA sobre quien ratifica. Es defecto de ESTE cambio (antes no habia definicion de 'worker' en la instancia). FIX MINIMO (elige UNA redaccion; solo texto de AGENTS.template.md; NO cambies las 3 reglas ni runtime/validador/config; NO toques instancias vivas): (A) acota el sujeto de la regla 1, p.ej. 'A worker agent (a weak-capability participant that executes code; this does not include the human owner, whose approval authority is defined in the role model above, regardless of the tier value its registry entry carries) is a code executor subordinate to the maker ...'; o (B) una linea introductoria antes de la lista: 'This policy governs agent participants that execute code; it does not alter the human owner's approval authority, nor does it redefine the signer/worker key-possession tiers of the registry.' Cualquiera cierra el SLIP. verification_cmd (re-correr en clon limpio): python scripts/validate_collaboration_state.py + scan_domain_neutrality.py + scan_encoding.py + python runtime/protocol_replay.py --check-drift --root . + python scripts/test_attested_instancing.py + python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py + generar una instancia ATTESTED por defecto con new_instance.py y grep de las 3 reglas + la clausula/linea nueva en su AGENTS (evidencia). Scope: AGENTS.template.md. FUERA: cambiar las 3 reglas, runtime/validador/config, instancias vivas, fondo intocable (2E35F26E epoch 1.14.0 N=500 N=6). Re-entrega TASK-0256 in_review + handoff con exit codes + release. Es la iteracion 1 (tope 2)."
question: "Confirmas que cierras SLIP-1 con SOLO texto en AGENTS.template.md (opcion A acotando la regla 1, u opcion B linea introductoria) para que 'worker agent' no capture al human owner tier:worker, sin cambiar las 3 reglas ni tocar runtime/instancias vivas, con evidencia de una instancia attested-default generada que muestra las 3 reglas + la aclaracion?"
created_at: 2026-07-24
context_refs:
  - Area_comun/artifacts/Analista-TASK-0256-roster-policy-born-operational-verdict.md
  - Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md
  - AGENTS.template.md
  - scripts/new_instance.py
one_line_summary: "Remediacion iter1 TASK-0256: 'worker agent' del texto colisiona con tier:worker del human owner en attested -> acotar el sujeto (o linea introductoria) en AGENTS.template.md, sin tocar las 3 reglas ni runtime; evidencia por instancia attested-default."
---

# ACTION - Remediacion iter1 TASK-0256 (SLIP-1: colision del token 'worker')

Hora local: 2026-07-24 03:35 (UTC+2). Veredicto Analista: CHANGE-REQUIRED, 1 defecto real, fix de 1
clausula; el resto (V1-V10) PASA. Artefacto: `Analista-TASK-0256-roster-policy-born-operational-verdict.md`.

## El defecto (SLIP-1, bloqueante)

Tu texto define 'worker agent' como ejecutor de codigo subordinado que nunca ratifica. Pero en el
tier ATTESTED con roster por defecto, `new_instance.py` escribe al HUMAN OWNER con `tier:'worker'`
(distincion de posesion-de-llave, no capacidad). La instancia generada nace con la tabla de roles
dando al human owner la aprobacion de politica Y tu texto diciendo que un 'worker' nunca ratifica ->
contradiccion normativa sobre quien ratifica. Lo introduce ESTE cambio.

## El fix (solo texto de AGENTS.template.md, 1 clausula)

Elige UNA: (A) acota el sujeto de la regla 1 para excluir explicitamente al human owner (cuya
autoridad esta en el role model, sea cual sea su `tier`); o (B) una linea introductoria antes de la
lista aclarando que la politica gobierna a los agentes que ejecutan codigo y NO redefine la autoridad
del human owner ni los tiers de posesion-de-llave `signer`/`worker`. NO cambies las 3 reglas.

## Entrega

TASK-0256 re-entregada a `in_review` + handoff con los verification_cmd y exit codes + EVIDENCIA:
instancia attested-default generada por new_instance que muestra las 3 reglas + la aclaracion, sin
colision. ASCII puro. Iteracion 1 (tope 2).
