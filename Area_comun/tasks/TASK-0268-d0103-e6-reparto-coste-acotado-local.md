---
task_id: TASK-0268
title: "[DECISION-0103][E6-A] Reparto de coste del hook: modo acotado por defecto en local (todo commit), completo solo bajo flag explicito; CI como enforcement completo"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: high
created_at: 2026-07-20
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0103]
linked_decisions: [DECISION-0103]
file: Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md
intake:
  type: infra
  goal: Implementar la parte A de la enmienda E6 de DECISION-0103 (decision del Operador 2026-07-20 tras evaluacion de coste, serie v2 51.5-53.3s por commit gobernado), en LOCAL el hook corre el modo ACOTADO por defecto (~0.4s) para TODO commit incluido el gobernado, y el modo COMPLETO (materializacion + validate, entregado por TASK-0267) queda disponible solo bajo flag explicito (variable de entorno o config git documentada, pensada para pre-push voluntario); el CI conserva la validacion completa desde clon limpio + el paso de existencia/SHA del hook. El CI es el enforcement duro; el hook es la primera linea rapida.
  acceptance:
    - Commit gobernado en local corre el modo acotado por defecto y termina en menos de ~2s (medido y declarado en el handoff); el acotado conserva los chequeos baratos existentes (prune_state --check, drift de guia) y anade lo minimo de forma barato si ya existe (sin llamar al validador completo).
    - El modo COMPLETO se activa SOLO con flag explicito documentado (p.ej. HOOK_FULL=1 o git config hook.full true) y entonces ejecuta la materializacion v2 de TASK-0267 sin cambios de mecanica.
    - CERO cambios al paso de CI (validate completo + existencia/SHA del hook siguen tal cual); el reparto queda documentado en el propio hook y en README_INSTANCIACION (primera linea vs enforcement duro, y el riesgo declarado de HEAD rojo transitorio con su mitigacion de gates pre-push).
    - Los negativos permanentes de la suite se ajustan al reparto, los casos de juicio completo corren con el flag activado; se anade un caso que verifica que el default es acotado y rapido.
    - Espejo en el export born-operational (instancia nueva nace con el reparto E6) y compatibilidad con lo que TASK-0266 propaga.
    - Neutralidad, validate y encoding verdes.
  verification_cmd:
    - Medicion en el handoff, commit gobernado con default acotado (<~2s) y con flag completo (cifra v2)
    - Suite del hook (scripts/test_precommit_hook.py) en verde con el reparto
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - .githooks/pre-commit
    - scripts/test_precommit_hook.py
    - scripts/new_instance.py
    - README_INSTANCIACION.md
  out_of_scope:
    - La optimizacion de la materializacion (TASK-0269, parte C) - FUERA.
    - Cambiar el paso de CI o el validador - FUERA.
    - Unidades RESERVADAS del preregistro N=6 (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c) - FUERA.
    - protocol.config.json pineado (epoch 1.14.0, genesis 2E35F26E) y dataset N=500 - FUERA (fondo intocable).
    - Encender supervised_autonomy o real_invoker - FUERA.
  risk: low
  estimate: S
---

# TASK-0268 - [E6-A] Acotado por defecto en local, completo bajo flag

Origen: enmienda E6 de DECISION-0103 (orden directa del Operador 2026-07-20, "GO A"),
tras la evaluacion de coste pedida en su RESP de O1. SECUENCIA: arranca tras el
veredicto y ratificacion de TASK-0267 (comparte .githooks/pre-commit y depende de su
mecanica de materializacion para el modo bajo flag); su GO lo emite el Arquitecto en
esa ratificacion. TASK-0269 (parte C) va despues.
