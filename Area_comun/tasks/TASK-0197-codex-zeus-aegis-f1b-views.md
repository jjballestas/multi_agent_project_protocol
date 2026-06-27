---
task_id: TASK-0197
title: "Zeus-Aegis F1b - vistas Decisiones + Ledger/atestacion + Handoffs (read-only) + endpoints /api/governance/{decisions,handoffs,ledger} (SPEC-0107)"
type: integration
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0107
created_at: 2026-06-27
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-Aegis
project: Zeus-Aegis
linked_decisions: [DECISION-0064, DECISION-0050, DECISION-0040]
file: Area_comun/tasks/TASK-0197-codex-zeus-aegis-f1b-views.md
---

# TASK-0197 - Zeus-Aegis F1b (vistas Decisiones / Ledger / Handoffs)

> maker=Codex / checker=Arquitecto. Repo PRODUCTO Zeus-Aegis. Segundo increment de F1 (SPEC-0107). **SOLO LECTURA**
> (F2 gateado post-TFM). Mismas reglas que F1a: lectura CANONICA (git show, no working tree), salud derivada, sin
> ruta de escritura, PII redactada, core protocolo intacto, pin Hermes v2.3.0. Genera dataset elegible (seq>=2221).

## Alcance (F1b)

- Endpoints read-only `/api/governance/{decisions,handoffs,ledger}`:
  - `decisions` -> indice de Area_comun/decisions/ (id, titulo, status, fecha).
  - `handoffs` -> indice de Area_comun/handoffs/.
  - `ledger` -> ultimos N eventos atestados del event-log (con su event_auth/actor_auth method + actor; firma
    verificada == runtime, indicador DERIVADO de la verificacion real, NUNCA verde hardcodeado).
- Vistas en /governance: Decisiones, Ledger/atestacion (timeline), Handoffs. Reusar el design-system existente.
- Ledger: mostrar el method de firma por evento (hmac / ed25519 / not_enforced) y el actor; el chip "atestado" se
  DERIVA de validate_chain/agent_signatures reales (tri-estado, fail-safe no-verde). PII redactada (payload).

## DoD (= SPEC-0107 AC, vistas F1b)

- AC1 endpoints decisions/handoffs/ledger sirven datos read-only desde el CANONICO (git show), sin ruta de escritura.
- AC2 el indicador de atestacion del ledger es DERIVADO de la verificacion real (no hardcoded; fail-safe no-verde).
- AC3 las 3 vistas renderizan; PII redactada en payloads/textos libres.
- AC4 prueba negativa: sin superficie de escritura nueva (la denylist sigue cubriendo submit_intent/state).
- AC5 node --test verde; gate F0 (npm test) sigue exit 0.
- AC6 core protocolo intacto; handoff a Arquitecto (checker).

## Notas

- Tras cerrar F1b (checker verde) sigue F1c (migrar componentes de gobernanza de zeus-protocol, REUSE-INVENTORY).
- Commit como Arquitecto con Co-Authored-By Codex. Minimal narration. Bloqueo -> blocked + una pregunta.
- POLITICA: el Arquitecto actualiza Zeus-Aegis/pipeline.html tras cerrar este caso.
