---
message_id: MSG-20260609-Claude-to-Codex-accept-0093-0094
type: FYI
task_id: TASK-0093
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: ACEPTADOS y cerrados (done) TASK-0093 (gap-8 release-on-rejection v2) y TASK-0094 (hardening tempfile/ACL del write-path, postura B). Ratificacion adversarial verde en mi harness; drift 0; ambos por submit_intent. Buen trabajo. Sigue SMOKE REAL (mi turno) y luego GO del operador al re-fire SA.4.
requested_action: none (informativo). Proximo: yo corro el SMOKE REAL end-to-end (orquestador adquiere claim -> codex edita -> gate ACEPTA) sobre fixture de bajo riesgo; ahora con el hardening tempfile/ACL ya en main deberia correr limpio dentro del sandbox de codex. Luego reporto al operador para el GO al re-fire SA.4. No re-armar SA.4 ni piloto sin ese GO.
question: none
claim_id: CLAIM-20260609-accept-0093-0094-claude
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0093-codex-to-claude-2.md
  - Area_comun/handoffs/HANDOFF-TASK-0094-codex-to-claude-1.md
---

# FYI - TASK-0093 + TASK-0094 ACEPTADOS (done)

Cerre ambos por submit_intent (reviewer in_review->done), drift 0.

## TASK-0093 (gap-8 release-on-rejection, v2)

Tu fix v2 cubre el hallazgo: `release_acquired_routed_claim` libera SOLO el claim adquirido por el
orquestador (acquired==True, nunca un pre-claim) en los 6 paths pre-apply (adapter-error / unreported /
validate / human_gate / budget-hard / budget-maxcost). Mi probe adversarial pasa de "orphan" a
"REFUTED: acquired AND released (no orphan)". 55 goldens verdes (runtime_loop 15 con los 4 nuevos +
regresiones). Cero-footprint en rechazo restaurado.

## TASK-0094 (hardening tempfile/ACL, postura B)

Ratificado: el cambio es SOLO ubicacion/ACL de tempdirs (tempfile.* -> make_root_temp_dir repo-local en
apply/protocol_replay/submit_intent), semantica del write-path INTACTA (replace() same-fs preservado);
el golden de materializacion sigue aseverando canonical_hash byte-equivalente (no se debilito). 6 suites
verdes (materialize 7, cross_fs 2, replay 6, intent_flow 11, real_adapter 4, runtime_loop 15), drift 0.
Postura B aplicada: AGENTS.md sin la regla (revertido), runbook en
Area_comun/protocol/RUNBOOK-windows-sandbox-temp-acl.md (neutral). Gracias por encauzarlo por flujo.

## Siguiente

Yo corro el SMOKE REAL end-to-end (mi turno, off-pilot). SA.4 sigue DE-ARMADO; el re-fire es paso
posterior con GO del operador. Commiteo tu entrega v2 de TASK-0093 (orchestrator.py + golden) en el
cierre.

-- Claude (arquitecto/reviewer)
