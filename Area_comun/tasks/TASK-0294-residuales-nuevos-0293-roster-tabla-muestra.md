---
task_id: TASK-0294
title: "[0293/follow-up] Residuales nuevos de 0293: fila checker en la tabla de roles (RES-8) + muestra generada coherente (RES-9) + cobertura de neutralidad de examples (RES-10)"
type: infra
status: in_progress
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-24
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [TASK-0293, TASK-0256, DECISION-0099]
linked_decisions: [DECISION-0099]
file: Area_comun/tasks/TASK-0294-residuales-nuevos-0293-roster-tabla-muestra.md
intake:
  type: infra
  goal: "Cerrar los 3 residuales ACCIONABLES nuevos del veredicto de TASK-0293 (Analista-TASK-0293-roster-policy-polish-verdict). (a) RES-8 (referente indefinido + tabla sin checker): la tabla 'Suggested role model' de AGENTS.template.md solo trae 3 filas (architect, implementer, human owner) y NO una fila para el analyst/checker; por eso 'the roster' de la 1a oracion de 'Roster policy' no tiene referente titulado que enumere al checker (sujeto de la regla 3). Fix: anadir la fila del analyst/checker a la tabla (usando el placeholder del analista, el mismo que puebla la lista de participantes), lo que arregla a la vez el referente y la sub-captura. (b) RES-9 (muestra hibrida / falsa vigencia): examples/generated_minimal_instance/AGENTS.md fue editada A MANO para meter el bloque de politica pero sigue declarando 'Last updated: 2026-06-05' y le faltan 5 secciones que el template ya emite (Intake gate/DoR, Handoff envelope + fix-loop, Commit trailers, Audited exceptions, Governed plan approval); senala falsa vigencia. Fix: REGENERAR la muestra integra desde el template actual (fiel, con todas las secciones y la politica) O fecharla como snapshot CONGELADO con nota explicita; preferible regenerar. (c) RES-10 (texto gobernado en archivo exento del gate): examples/** es exempt_glob de scan_domain_neutrality, asi que el texto de politica en la muestra no se escanea. Fix/decision: o acotar la exencion para cubrir el bloque de politica de la muestra, O documentar que examples/** es exento por diseno (ilustrativo) y que el bloque de la muestra deriva del template YA escaneado (lo garantiza la regeneracion de RES-9); el maker elige y documenta. Neutralidad de dominio total; cero cambios de runtime/validador de comportamiento (RES-10 solo puede tocar el ALCANCE del scan, no su logica de deteccion)."
  acceptance:
    - "RES-8: la tabla 'Suggested role model' de AGENTS.template.md incluye una fila para el analyst/checker (rol de checker adversarial; no implementa ni ratifica su propio trabajo revisado). Una instancia generada por new_instance muestra la fila del checker en su tabla de roles (grep). test_attested_instancing y run_runtime_instantiation_cases y cualquier golden/pin afectados quedan verdes/actualizados."
    - "RES-9: examples/generated_minimal_instance/AGENTS.md queda COHERENTE: regenerada fiel al template actual (incluye la politica + las 5 secciones que faltaban + fecha real), O fechada explicitamente como snapshot congelado con nota; ya no senala falsa vigencia. validate y CI verdes."
    - "RES-10: cerrado con una decision trazada -- exencion acotada para cubrir el bloque de politica, O nota de by-design (examples ilustrativo, deriva del template escaneado). scan_domain_neutrality sigue verde y su intencion (falsable) intacta."
    - "Las 3 reglas de 0099 conservan su sentido; cero cambios de comportamiento de runtime/validadores; ninguna instancia VIVA tocada; neutralidad verde (falsable)."
  verification_cmd:
    - "generar instancia (los 3 tiers) con new_instance.py + grep de la fila del checker en la tabla de roles (evidencia RES-8)"
    - "diff de examples/generated_minimal_instance/AGENTS.md contra una generacion fresca = coherente (regenerada) o con nota de snapshot; grep de las 5 secciones + fecha (evidencia RES-9)"
    - "scan_domain_neutrality con la decision RES-10 aplicada -> 0 (y falsable); documentar el enfoque"
    - "python scripts/validate_collaboration_state.py -> 0 ; scan_encoding.py -> 0 ; protocol_replay.py --check-drift -> 0 ; test_attested_instancing.py -> 0 ; run_runtime_instantiation_cases.py -> 0"
  scope_routes:
    - AGENTS.template.md
    - examples/generated_minimal_instance/
    - scripts/scan_domain_neutrality.py
  out_of_scope:
    - "C1 (correccion de registro del checker: 'un humano no es un agente' era premisa falsa) -- FUERA: record-only, ya corregido en el veredicto; nada que implementar."
    - "RES-2 (re-materializar instancias VIVAS) -- FUERA: directiva aparte."
    - "RES-4 (enforcement mecanico de strong-capability) -- FUERA: DECISION aparte."
    - "RES-6 -- FUERA: record-only."
    - "Cambiar el sentido normativo de las 3 reglas, la LOGICA de deteccion del scan de neutralidad, runtime/config, instancias vivas, fondo intocable (2E35F26E epoch 1.14.0 N=500 N=6)."
  risk: low
  estimate: S
---

# TASK-0294 - Residuales nuevos de 0293 (tabla checker + muestra + neutralidad examples)

Origen: 3 residuales accionables del veredicto de TASK-0293. RES-8 (fila del analyst/checker en la
tabla de roles -> arregla el referente 'roster' y la sub-captura de la regla 3), RES-9 (muestra
generada coherente, no falsa-vigencia: regenerar o nota de snapshot), RES-10 (cobertura de neutralidad
del texto gobernado en examples: acotar exencion o documentar by-design). C1/RES-2/4/6 FUERA (record /
directiva / DECISION). ULTIMA capa de la cadena de residuales del espejo de roster. Sin runtime, sin
instancias vivas, neutralidad total.
