---
id: TASK-0045
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0043]
relates_to: [TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0001]
execution_pipeline: [runtime/router.py select por capacidad requerida + carga (load_score con pesos en config) + exclusion de autor en review/QA + max_active_claims + desempate stable_hash y lexicografico SOLO como ultimo recurso; required_capability opcional en la tarea; routing_decision.explanation (candidatos+filtrados+score); fairness ratio sobre asignaciones ELEGIBLES con anti-starvation; golden examples/runtime_router_cases ampliado]
acceptance_criteria: [review y QA nunca asignan al autor (I1/I2) incluso si el autor tiene esa capacidad; sin revisor/QA elegible => escalate/blocked con razon+candidatos (A9 sin escalado oculto, nunca self-review); routing determinista (mismo estado/routing_epoch => misma asignacion); fairness: 100 tareas entre 3 agentes identicos sin sesgo por nombre y sin starvation (un elegible con cero tras muestra minima => fallo); pesos en config (no hardcode); routing_decision.explanation presente; fallback N=2 byte-equivalente (review->Claude, human gate->operador humano) sin editar fixtures; sin red]
test_plan: [runtime_router_cases ampliado: review/QA != autor; autor-unico => escalate; 3 agentes identicos -> fairness dentro de umbral + anti-starvation; replay mismo estado => misma asignacion; 5 casos actuales intactos]
closure_criteria: [router por capacidad+carga determinista + exclusion de autor + fairness gate + explanation + pesos en config; golden verdes; fallback N=2 sin regresion; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0045 - N-agente Fase 3: router balanceado + fairness gate

Estado operativo: DONE. ACEPTADA por Claude con ratificacion adversarial (2026-06-06): suite 52/52
(router 10/10) + validador/encoding/neutralidad py+ps1 verdes; A9 (review/QA != autor, escalate sin
self-review), A4 (fairness 100/3 sin sesgo por nombre + anti-starvation + ponderado), determinismo y
fallback N=2 verificados. Ver `Area_comun/handoffs/HANDOFF-TASK-0045-codex-to-claude-1.md`.

> `implementation` -> SDD; implementar contra **SPEC-0038 (congelada)** Fase 3 (sec.13) + addenda
> A4 (fairness) y A9 (sin escalado oculto / exclusion multi-capacidad). Aditivo, config-gated,
> **fallback N=2 intacto**.

## Alcance (Fase 3)
- `runtime/router.py` (sec.6): `select_agent`/`select_review`/`select_ready_task` por **capacidad
  requerida** + **carga** (`load_score` con pesos en config `routing_weights`, no constantes) + **exclusion
  de autor** en review/QA (I1/I2, A9) + `max_active_claims` + desempate `stable_hash(task+transition+agent+
  routing_epoch)` y **lexicografico SOLO como ultimo recurso**.
- `required_capability` **opcional** en la tarea (si ausente, usa `owner` como hoy).
- **A9 sin escalado oculto:** si no hay revisor/QA elegible distinto del autor => `escalate`/`blocked` con
  razon + conjunto de candidatos; **nunca self-review** silencioso.
- **A4 fairness gate (CI):** metrica sobre asignaciones **elegibles** en ventana; agentes identicos =>
  distribucion casi uniforme; con peso => observado vs esperado; **fallo por starvation** si un elegible
  recibe cero tras muestra minima; guarda contra denominador cero.
- `routing_decision.explanation` con candidatos, filtrados con razon y tupla de score.

## No-alcance (fases posteriores)
- NO maquina de estados Review/QA con defect logs/contadores (Fase 4). NO tool-policy/guardrails (Fase 5).
- NO romper N=2: sin registry, review sigue a Claude y el human gate a "operador humano" (byte-equivalente).

## Tests
- `examples/runtime_router_cases/` ampliado: review/QA != autor (incl. autor con capacidad reviewer);
  autor-unico => escalate; **fairness** 100 tareas / 3 agentes identicos sin sesgo + anti-starvation;
  replay con mismo estado => misma asignacion; 5 casos actuales intactos. Sin red.

## Dogfood
Liveness + handoff-release. ASCII-only en mailbox/state. Tu area personal es `personal/Codex/`. Te ratifico
adversarialmente con foco en: review/QA != autor (multi-capacidad), no-escalado-oculto, fairness sin sesgo
por nombre y determinismo. Si un punto exige decision, `blocked` + 1 pregunta.
