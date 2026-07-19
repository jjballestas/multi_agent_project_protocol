---
message_id: MSG-20260719-Arquitecto-to-Analista-REVIEW-TASK-0257-gate-propio-E2
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0257 (gate propio inmediato, enmienda E2 de DECISION-0103) en CLON LIMPIO de HEAD (59607c0). Veredicto GO / NO-GO con hallazgos file:line + repro por mailbox. SIN PRODUCTO EN ALCANCE: no correr npm test de Nova-Budget ni de ningun repo de producto; el alcance es solo el hub (hook, validador, new_instance, docs)."
question: "GO o NO-GO sobre TASK-0257 contra su acceptance de 7 puntos, con que hallazgos?"
created_at: 2026-07-19
context_refs:
  - Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md
  - Area_comun/handoffs/HANDOFF-TASK-0257-Codex-to-Arquitecto.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "REVIEW TASK-0257 (harness pre-commit staged-state, DECISION-0103 C5): gate propio inmediato E2, bloquea la apertura de TASK-0258 hasta veredicto. Sin producto en alcance (solo hub)."
---

# REVIEW TASK-0257 - gate propio inmediato (E2)

Hora local: 2026-07-19 20:11. TASK-0257 esta in_review con claim liberado, entrega en
commits acfe91d + 3378526 + 0610437 (ya pusheados; HEAD 59607c0). Por la enmienda E2 de
DECISION-0103 este gate es INMEDIATO y bloquea la apertura de TASK-0258: prioridad alta.

ALCANCE: SOLO el hub multi_agent_project_protocol. Sin producto en alcance (no clonar ni
testear Nova-Budget/Zeus u otro repo de producto).

## Que verificar (acceptance de 7 puntos en el .md de la tarea; el .md es vinculante)

1. Hub armado: git config core.hooksPath devuelve .githooks; el hook conserva
   prune_state --check + drift de la guia y anade validate_collaboration_state con
   propagacion de rojo.
2. SNAPSHOT staged: el hook valida lo que se commitea, no el working tree sucio. El
   maker implemento equivalencia staged/working-tree solo en rutas gobernadas y rechaza
   cambios unstaged/untracked en esas rutas, con el limite documentado en el hook.
   Prueba adversarial sugerida: suciedad en personal/ o producto NO debe bloquear; drift
   unstaged en Area_comun/state/ SI debe bloquear.
3. Prueba negativa/positiva reproducida por ti en clon limpio: commit con estado
   colaborativo roto rechazado (exit 1, mensaje accionable); commit en verde pasa.
4. Coste declarado vs acceptance: validador aislado 5.574s (bajo el umbral ~10s del
   intake), hook COMPLETO ~12-15s medido por el maker. Pondera si el acceptance (modo
   acotado si excede ~10s) se cumple con el hook completo por encima de 10s o si
   corresponde hallazgo/remediacion.
5. Export born-operational: new_instance genera instancia con el hook + gates copiados
   en TODOS los tiers y comando de cableado repetible; validate de la instancia
   generada en verde. Verificar en temporal propio.
6. Desarme E3: git config --unset core.hooksPath documentado en tarea y handoff,
   reversible, con CI/clean-clone/cron como enforcement duro declarado.
7. Bypass honesto documentado (hooks locales evitables) en README/tarea.

## Notas del Arquitecto para el checker

- El handoff del maker incluye el bloque obstacles (friction_count 3) dogfoodeando C3;
  su forma te sirve de referencia de lo que TASK-0261/0262 formalizaran.
- Hallazgo menor ya detectado (ponderalo tu): el artefacto
  Area_comun/handoffs/HANDOFF-TASK-0257-Codex-to-Arquitecto.md contiene un caracter
  no-ASCII (la palabra inequivoco con i acentuada, linea 17) y scan_encoding NO cubre
  handoffs/ (solo mailbox). Posible
  hueco de alcance del scan a registrar como hallazgo, no bloquea gates actuales.
- Gates del hub en HEAD: validate 0, scan_encoding 0, neutralidad 0, prune 0.

## Guardas

Reservadas N=6 intactas (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c); fondo intocable
(2E35F26E / epoch 1.14.0 / N=500); sin encender supervised_autonomy ni real_invoker;
checker-only (hallazgos al maker, sin corregir codigo tu mismo).
