---
task_id: TASK-0248
title: "[VISION-NOVA] Skill codegen-triage para Codex (2 capas: NEUTRAL decision codegen-vs-frontera exportable + recetas de INSTANCIA Nova). Gobernada: owner Codex-maker / checker Analista."
type: feature
status: ready
owner: Codex
phase: P2
priority: high
created_at: 2026-07-04
reviewer: Analista
checker: Analista
project: multi_agent_project_protocol
relates_to: [GOAL-VISION-NOVA-001, NOVA-GOAL-001, DECISION-0061, DECISION-0078, DECISION-0088]
linked_decisions: [DECISION-0061, DECISION-0078, DECISION-0002]
linked_reqs: []
file: Area_comun/tasks/TASK-0248-skill-codegen-triage.md
intake:
  type: feature
  goal: Crear la skill codegen-triage que usa Codex durante el desarrollo para clasificar el CAMINO DE GENERACION de una tarea (codegen determinista vs firmante frontera) ANTES de codificar, para no gastar criterio/tokens en trabajo que una fuente determinista + un gate resuelven. En DOS CAPAS por neutralidad (CLAUDE.md regla 1): (a) capa NEUTRAL en el core exportable (sin dominio, sin .NET/Nova) = la skill de decision; (b) capa de INSTANCIA Nova (recetas .NET concretas) FUERA del core neutral. Diseno de referencia (NO verbatim): personal/asesor/DRAFT-skill-codegen-triage.md.
  target_user: Codex (maker) durante el build de GOAL-P1/P2 y siguientes; exportable a cualquier instancia Aegis.
  acceptance:
    - CAPA NEUTRAL: skill .claude/skills/codegen-triage/SKILL.md (cargable por el loader DECISION-0061). Procedimiento de decision del FIRMANTE responsable: (1) fuente determinista (salida mecanica y TOTAL de una fuente: 'por cada X emite N archivos rellenando huecos'); (2) oraculo determinista (correctitud comprobable por GATE automatico build+test+arch-test+paridad+lint, NO por criterio) -- requisito DURO; si 1 y 2 -> CODEGEN; (3) BANDERAS ROJAS -> firmante frontera (compone >1 mutacion / llama procs en secuencia / cruza frontera de modulo / toca contexto de sesion-tenant o saldos-cuadres / depende de vista con brecha / logica de negocio-seguridad-migracion). Salida = {camino: codegen|frontera, razon, gate que la verifica, banderas detectadas}. El peon queda FUERA de alcance (capa aparte, DECISION-0078).
    - NEUTRALIDAD DURA: la capa neutral NO menciona .NET, Nova, C#, EF, Roslyn, NSwag ni ningun termino de dominio/stack. scan_domain_neutrality.py DEBE quedar limpio sobre .claude/skills/codegen-triage/.
    - CAPA DE INSTANCIA (fuera del core neutral, en la instancia Nova / tooling del producto, NO en .claude/skills/ del hub): recetas concretas (dotnet new template-pack, EF Core scaffold, Roslyn SG, NSwag/openapi-generator) + GATE de instancia (dotnet build+test+arch-tests+paridad EXEC-vs-endpoint+dotnet format+scan ASCII+guard 'sin logica de negocio/sin deps nuevas'). Ubicacion propuesta: la instancia Nova (D:/Agentes/Zeus/NOVA/Aegis o tooling de Nova-Budget); el maker propone la ruta exacta en el handoff.
    - RESTRICCION DE ESTUDIO documentada en la skill: codegen != peon (determinista, cero-tokens, un dev, NO anade agentes, NO es el tratamiento; legitimo en AMBOS brazos incluido GOAL-P1; uso SIMETRICO por par). La CLARIFICACION formal en la definicion del brazo baseline es INPUT DEL SELLO (08-jul), NO se sella en esta tarea.
    - Gate = APROBADO del Analista (checker adversarial formal; esta tarea SI es gobernada, no es unidad baseline medida) + validate + scan_encoding + scan_domain_neutrality exit 0 + la skill carga por el loader.
  verification_cmd:
    - python scripts/validate_collaboration_state.py
    - python scripts/scan_encoding.py
    - python scripts/scan_domain_neutrality.py
  scope_routes:
    - .claude/skills/codegen-triage/
    - Area_comun/tasks/TASK-0248-skill-codegen-triage.md
    - Area_comun/handoffs/
  out_of_scope:
    - NO incluir el peon (asistencia autorizada LLM) en esta version: la skill decide codegen-vs-frontera; el peon es capa aparte (DECISION-0078).
    - NO meter recetas .NET/Nova en la capa NEUTRAL (romperia neutralidad; van en la instancia).
    - NO sellar la clarificacion codegen!=peon en la definicion del brazo (es input del sello 08-jul, lo confirma el Operador al sellar).
    - NO tocar el core pineado (epoch 1.14.0) ni el N=500.
  tech_constraints:
    - Skill markdown cargable por el loader de skills (DECISION-0061). Capa neutral domain-agnostic; recetas de instancia separadas.
  assets_inputs:
    - Diseno de referencia (no verbatim): personal/asesor/DRAFT-skill-codegen-triage.md.
    - Runbook operativo de referencia (personal/ungobernado): D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/TEMP_Guia_Modelos_Peones_y_Medicion.md s.1/s.5.
  risks_list:
    - Riesgo de fuga de dominio en la capa neutral (scan_domain_neutrality es el gate duro).
  priority: high
  risk: low
  estimate: M
---

# TASK-0248 - Skill codegen-triage para Codex (2 capas)

Crea la skill codegen-triage: capa NEUTRAL (decision codegen-vs-frontera, exportable, sin dominio, en
.claude/skills/codegen-triage/) + capa de INSTANCIA Nova (recetas .NET, fuera del core neutral). La usa Codex
para decidir cuando delegar a generacion determinista (con gate verde) vs hacerlo como firmante frontera. NO
incluye el peon. codegen != peon (determinista, cero-tokens, no es tratamiento; simetrico por par; la
clarificacion formal en la def del brazo es input del sello, no se sella aqui). Gobernada: Codex-maker /
Analista-checker (gate formal aplica). Diseno ref: personal/asesor/DRAFT-skill-codegen-triage.md.
