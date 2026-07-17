---
task_id: TASK-0256
title: "Espejo de DECISION-0099 (politica roster peon/maker/checker) en el export born-operational (DECISION-0096)"
type: feature
status: proposed
owner: Codex
phase: P2
priority: normal
created_at: 2026-07-17
reviewer: Analista
project: multi_agent_project_protocol
relates_to: [DECISION-0099, DECISION-0096]
linked_decisions: [DECISION-0099, DECISION-0096]
file: Area_comun/tasks/TASK-0256-espejo-decision-0099-export-born-operational.md
intake:
  type: feature
  goal: Cablear el espejo de DECISION-0099 (politica de roster sellada 2026-07-17, version corregida; peon = ejecutor subordinado al maker, maker fuerte gobierna y especifica, checker siempre fuerte) en el export born-operational de DECISION-0096, para que toda instancia NUEVA nazca con la politica anotada en su contrato de roster (AGENTS.template de instancia o seccion de roster que new_instance materializa). Mantener neutralidad de dominio total en el texto exportado.
  acceptance:
    - El template que new_instance materializa incluye la politica de roster de 0099 (3 reglas, texto neutral) en la seccion de roles/roster del AGENTS de la instancia.
    - Una instancia recien creada con new_instance en un directorio temporal muestra la politica en su AGENTS (verificacion por grep en la instancia generada).
    - Cero cambios de comportamiento en runtime/validadores; solo contenido del template.
    - Neutralidad: sin terminos de dominio/negocio (scan de neutralidad verde).
    - Instancias vivas NO se tocan (la politica les aplica por el hub; su AGENTS se actualiza en su propio ciclo).
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_domain_neutrality.py
    - python scripts/scan_encoding.py
  scope_routes:
    - AGENTS.template.md
    - scripts/new_instance.py
  out_of_scope:
    - Editar AGENTS de instancias vivas (Nova-Payroll/NOVA) - FUERA.
    - Cambiar reglas de 0099 o el flujo de capabilities - FUERA.
    - Enforcement mecanico de la politica (validador de roster) - FUERA (si se quiere, DECISION aparte).
  risk: low
  estimate: S
---

# TASK-0256 - Espejo DECISION-0099 en el export born-operational

Origen: FIRMA + correccion del operador (commits 585b7ab + dca50ec) y sello de DECISION-0099
(36c000f, tx 4713-4715). Tarea de mantenimiento NO bloqueante ordenada como parte del sello:
las instancias futuras deben nacer con la politica de roster en su contrato. Promocion a ready
cuando el operador abra la cola del hub (crons del hub apagados hoy salvo build-open).
