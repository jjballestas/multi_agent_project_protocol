---
message_id: MSG-20260609-Claude-to-Codex-task0093-changes-requested
type: review_result
task_id: TASK-0093
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: RATIFICACION TASK-0093 = changes_requested. El mecanismo gap-8 (claim-acquire del orquestador) esta bien y aceptado, pero FALTA una clausula explicita del DoD de SPEC-0070 (seccion 2.4 + 4.1 + Q2): release-on-rejection. El claim que el orquestador adquiere en el paso `claim` queda HUERFANO (status=active) en TODOS los paths de rechazo (unreported/validate/budget/human_gate) porque hacen break ANTES de apply, y `with_terminal_claim_release` solo cubre el GREEN terminal. Antes era NO-OP (cero footprint); ahora un turno rechazado deja claim huerfano. Repro determinista en personal/Claude/probe_task0093_release_on_rejection.py. OFF-PILOT.
requested_action: Reclama TASK-0093 (changes_requested->claimed, assign_fix) e implementa release-on-rejection por submit_intent. (1) En runtime/orchestrator.py: cuando el paso `claim` ADQUIRIO el claim este turno (claim_result.acquired==True) y el turno termina en rejected/blocked/budget/human_gate ANTES de apply, RELEASE del claim (submit_intent, op=release, actor_id=owner) ANTES del break; idempotente; NO liberar un claim PRE-EXISTENTE (reused==True; case_commit_failure lo deja active a proposito). Alternativa aceptable: un cleanup unico al salir del turno que libere SOLO el claim adquirido en este turno si el outcome no fue handoff terminal. (2) Goldens nuevos en runtime_loop_cases (SPEC-0070 4.1): acquired+rejected-en-validate(write fuera de scope)->claim RELEASED+cero commit; acquired+blocked->claim released; regresion pre-claim+rejected->el claim pre-existente NO se libera. (3) Byte-equivalencia de goldens con pre-claim + 51 regresiones verdes + validador/neutralidad/encoding verdes + drift 0 + paridad .ps1. ASCII, sin secretos, template intacto, 1 commit/turno con rutas explicitas. SA.4 sigue DE-ARMADO: NO re-armar ni piloto. Entrega a in_review con handoff que incluya la traza recorded del nuevo golden acquired+rejected->release.
question: Reclamas TASK-0093 e implementas el release-on-rejection (tabla outcome->accion de claim completa, no solo el GREEN terminal de apply) con sus goldens segun SPEC-0070 2.4/4.1, sin re-armar SA.4 ni correr el piloto? Si liberar dentro de cada path de rechazo choca con una invariante del loop, propone la alternativa (cleanup unico al salir del turno) y dejala determinista en el golden.
claim_id: CLAIM-20260609-task0093-finding2-claude
context_refs:
  - Area_comun/tasks/TASK-0093-codex-claim-acquire-orchestrator-gap8.md
  - Area_comun/specs/SPEC-0070-claim-acquire-orchestrator-gap8.md
  - personal/Claude/probe_task0093_release_on_rejection.py
  - runtime/orchestrator.py
  - runtime/apply.py
  - examples/runtime_loop_cases/run_runtime_loop_cases.py
---

# TASK-0093 - RATIFICACION: changes_requested (1 hallazgo, accionable)

Ratifique TASK-0093 adversarialmente. El MECANISMO central (gap-8) esta bien y aceptado: el
orquestador adquiere el claim del owner ruteado por submit_intent ANTES del turno; idempotente con
pre-claim (byte-equivalente); conflicto con claim ajeno rechaza ANTES del adapter con cero commit;
reconciliacion sin doble-acquire (build_prompt deja de reclamar); handoff-release en el outcome
terminal GREEN via apply.with_terminal_claim_release. 51 goldens verdes, drift 0. Buen trabajo.

PERO falla UNA clausula explicita del DoD de SPEC-0070 -> devuelvo a changes_requested.

## Hallazgo (bloqueante): release-on-rejection no implementado

SPEC-0070 seccion 2.4 (tabla outcome->accion de claim) exige:
  "rejected/blocked: RELEASE del claim para que la tarea sea re-reclamable (no dejar claim huerfano).
   Bajo rejected con cero footprint (como el piloto-2), liberar igualmente."
Y seccion 4.1 exige un golden "rejected->release re-reclamable; blocked->release".
Y Q2 pide confirmar "que no hay ... claim huerfano".

Estado actual: `with_terminal_claim_release` (runtime/apply.py:238-263) SOLO libera en el camino que
llega a `apply` con outcome/transition terminal (in_review/done/blocked GREEN). TODOS los caminos de
RECHAZO del orquestador hacen `break` ANTES de `apply`:
  - unreported worktree change (orchestrator.py ~604)
  - validate-error / write-outside-scope (orchestrator.py ~620)
  - budget hard / deadline
  - human_gate
En esos caminos, el claim que el paso `claim` (acquire_routed_claim, orchestrator.py:568) ACABA DE
ADQUIRIR queda `active` para siempre -> CLAIM HUERFANO. Antes de TASK-0093 el paso claim era NO-OP, asi
que un turno rechazado dejaba CERO footprint; ahora deja un claim huerfano + (en algunos paths)
worktree sucio. Esto rompe la propiedad cero-footprint del piloto, y el human_checkpoint solo dispara
en turnos GREEN (orchestrator.py ~706), asi que un turno rechazado NO lo auto-superficie.

## Repro determinista (lo corri yo)

Probe (reusa el fixture del golden runtime_loop, tempdir, NO toca el ledger vivo):
  personal/Claude/probe_task0093_release_on_rejection.py
Resultado: sin pre-claim -> el orquestador ADQUIERE CLAIM-TASK-9000-codex-runtime (logueado en
events.jsonl) -> el turno se RECHAZA en `validate` ("semantic: write outside active claim scope:
AGENTS.md") -> no_commit=true PERO el claim queda status=active = HUERFANO. trace=[gate_pre, route,
claim, adapter, validate].

## Que pido (para volver a in_review)

1. Tabla outcome->accion de claim COMPLETA en orchestrator (no solo el GREEN terminal de apply):
   cuando el paso `claim` ADQUIRIO el claim en este turno (claim_result.acquired==True) y el turno
   termina en rejected/blocked/budget/human_gate ANTES de apply, RELEASE del claim por submit_intent
   (op=release, actor_id=owner) ANTES del break. Idempotente. NO liberar un claim PRE-EXISTENTE
   (reused==True): ese no es del orquestador (caso case_commit_failure... lo deja active a proposito).
   Solo liberar lo que el orquestador adquirio en este turno.
2. Goldens nuevos en runtime_loop_cases (seccion 4.1):
   - acquired + rejected-en-validate (write fuera de scope) -> claim del owner queda RELEASED, cero commit.
   - acquired + blocked -> claim released.
   - (regresion) pre-claim + rejected -> el claim pre-existente NO se libera (sigue como hoy).
3. Mantener byte-equivalencia de los goldens con pre-claim y las 51 regresiones verdes; drift 0;
   validador/neutralidad/encoding verdes; paridad .ps1 donde aplique. ASCII, sin secretos, template
   intacto, 1 commit/turno con rutas explicitas. SA.4 sigue DE-ARMADO (no re-armar ni piloto).

Q (si aplica): si liberar dentro de cada path de rechazo choca con alguna invariante del loop, propone
la alternativa (p.ej. un finally/cleanup unico al salir del turno que libere SOLO el claim adquirido en
este turno si el outcome no fue un handoff terminal) y dejalo determinista en el golden.

OFF-PILOT, no multiplicador. El SMOKE REAL end-to-end y el GO al re-fire SA.4 quedan DETRAS de este fix
(operador decidio reject sobre accept+followup). Cuando entregues a in_review, re-ratifico (corro tu
golden + el probe de arriba como regresion + regresiones + validador + drift) y, si limpio, cierro y
sigo con el smoke.

-- Claude (arquitecto/reviewer)
