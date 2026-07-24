---
task_id: TASK-0293
title: "[DECISION-0099/0256][follow-up] Pulido de los residuales accionables del espejo de roster (polish/RES-5, RES-3, RES-7, RES-1) en AGENTS.template + muestra generada"
type: infra
status: ready
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-24
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0256, DECISION-0099, DECISION-0096]
linked_decisions: [DECISION-0099]
file: Area_comun/tasks/TASK-0293-pulido-residuales-roster-policy-0256.md
intake:
  type: infra
  goal: "Cerrar los residuales ACCIONABLES declarados por el checker en TASK-0256 (veredictos Analista-TASK-0256-*-verdict), todos de TEXTO/DOC, sin cambios de runtime ni de las reglas de fondo. (a) POLISH+RES-5 (sub-captura de alcance): la 1a oracion del bloque 'Roster policy' acota a 'agent participants that execute code', lo que un lector literalista podria usar para argumentar que un checker que solo lee cae fuera de alcance; reformular a un alcance que EXCLUYA al human owner (un humano no es un agente) SIN estrechar a la ejecucion de codigo (p.ej. la sugerencia del checker: 'This policy governs the agent participants of the roster.'). (b) RES-7 (referencia colgante): la 2a oracion referencia 'the registry's signer/worker key-possession tiers', pero los tiers coordination/runtime generan protocol.config.json SIN agent_registry; suavizar la redaccion para que no cuelgue donde no hay registry (p.ej. '...where the registry defines them', o equivalente que la deje como exencion inocua). (c) RES-3 (falta la razon de la regla 3): anadir una clausula breve con el POR QUE de la regla 3 (un checker incapaz de refutar convierte el gate en rubber-stamp), para que la razon viaje al adoptante. (d) RES-1 (muestra desincronizada): examples/generated_minimal_instance/AGENTS.md no contiene la politica (grep -c 'Roster policy' -> 0); dejarlo COHERENTE -- regenerar la muestra para que refleje el template actual, O anadir una nota de que es un snapshot congelado en una version dada; en cualquier caso los gates/CI siguen verdes. Neutralidad de dominio total en todo el texto."
  acceptance:
    - "POLISH/RES-5: el bloque 'Roster policy' del AGENTS.template ya no acota el alcance a 'that execute code'; el nuevo alcance excluye al human owner y NO deja fuera al checker (que puede no ejecutar codigo). Una instancia attested-default generada por new_instance sigue mostrando las 3 reglas + el alcance corregido (grep)."
    - "RES-7: la referencia a los tiers signer/worker del registry ya NO cuelga en instancias coordination/runtime (sin agent_registry); redaccion como exencion condicional. Verificar generando los 3 tiers."
    - "RES-3: la regla 3 (o una clausula adyacente) incluye la razon (checker debil -> rubber-stamp), texto neutral."
    - "RES-1: examples/generated_minimal_instance/AGENTS.md queda coherente (contiene la politica regenerada, O una nota de snapshot congelado); validate y CI verdes."
    - "Las 3 reglas conservan su sentido normativo de DECISION-0099; cero cambios de runtime/validador/config; ninguna instancia VIVA tocada; neutralidad verde (gate falsable)."
  verification_cmd:
    - "generar instancia attested-default con new_instance.py + grep de las 3 reglas + el alcance corregido (evidencia)"
    - "generar coordination y runtime + confirmar que la referencia al registry no cuelga (evidencia)"
    - "grep -c 'Roster policy' examples/generated_minimal_instance/AGENTS.md coherente con la decision (regenerar o nota)"
    - "python scripts/validate_collaboration_state.py -> 0 ; scan_domain_neutrality.py -> 0 ; scan_encoding.py -> 0 ; protocol_replay.py --check-drift -> 0 ; test_attested_instancing.py -> 0 ; run_runtime_instantiation_cases.py -> 0"
  scope_routes:
    - AGENTS.template.md
    - examples/generated_minimal_instance/
  out_of_scope:
    - "RES-2 (upgrade_instance.py propaga el template, no re-materializa el AGENTS.md vivo de instancias existentes) -- FUERA: coincide con el out_of_scope de 0256; re-materializar instancias vivas seria una directiva aparte."
    - "RES-4 (enforcement mecanico de 'strong-capability' / validador de roster) -- FUERA: DECISION-0099 lo contempla como DECISION separada (cambio de frontera), no un pulido de texto; requiere DECISION del Operador."
    - "RES-6 (correccion de registro del propio checker) -- FUERA: ya quedo corregido en el veredicto; nada que implementar."
    - "Cambiar el sentido normativo de las 3 reglas de 0099, runtime/validador/config, instancias vivas, fondo intocable (2E35F26E epoch 1.14.0 N=500 N=6)."
  risk: low
  estimate: S
---

# TASK-0293 - Pulido de residuales accionables del espejo de roster (0256)

Origen: residuales declarados por el checker en TASK-0256 (verdicts
`Analista-TASK-0256-roster-policy-born-operational-verdict.md` y
`Analista-TASK-0256-roster-policy-remediation1-verdict.md`). Accionables (texto/doc): POLISH+RES-5
(alcance sin 'that execute code'), RES-7 (referencia colgante al registry en coordination/runtime),
RES-3 (razon de la regla 3), RES-1 (muestra generada desincronizada). RES-2/RES-4/RES-6 FUERA (por
diseno / DECISION aparte / record-only). Sin runtime, sin instancias vivas, neutralidad total.
