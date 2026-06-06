---
id: TASK-0038
owner: Claude
status: proposed
type: analysis
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0039]
relates_to: [TASK-0036]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015]
objective: Analizar y especificar la preparacion N-agent del protocolo para que no dependa de roles fijos architect/implementer ni de nombres Claude/Codex.
expected_output: Analisis de brechas, propuesta de registry de agentes/capacidades, y specs/tareas para migrar scaffolding, templates, router/runtime y validadores de forma aditiva.
question_to_resolve: Que contratos deben cambiar para soportar N agentes configurables manteniendo compatibilidad con instancias actuales?
closure_criterion: Queda una propuesta arquitectonica con tareas implementables y criterios de compatibilidad; no se ejecutan cambios incompatibles sin decision y aprobacion humana.
---

# TASK-0038 - N-agent readiness (PARAGUAS)

> Estado: PROPOSED (paraguas). Diseno CAPTURADO en
> [DECISION-0015](../decisions/DECISION-0015-n-agent-registry-y-capacidades.md) +
> [SPEC-0038](../specs/SPEC-0038-n-agent-registry.md) (modelo de equipo completo: registry por
> capacidades + review-by-not-author + QA gate). La descomposicion (sub-tareas a-g) vive en SPEC-0038 y
> NO esta registrada como tareas todavia. Implementacion **diferida y triple-gateada**: TASK-0039 (hecho)
> -> aprobacion humana de DECISION-0015 -> OK puntual del operador.

## Intencion
Dejar como trabajo futuro la preparacion real para N agentes. El protocolo no debe explicar el trabajo
como "que hace Claude / que hace Codex", sino como roles, capacidades y responsabilidades configuradas
en cada instancia.

## Brechas conocidas a estudiar
- `protocol.config.template.json` usa `agent_roles` fijo: `architect`, `implementer`, `human_owner`.
- `TASK_INDEX.template.json` limita la leyenda de owners a tres placeholders.
- `scripts/new_instance.py` acepta solo `--architect`, `--implementer`, `--human-owner`.
- `AGENTS.template.md` tiene tabla de roles fija.
- `runtime/turn_schema.json` enumera agentes concretos en `agent`.
- `runtime/router.py` hardcodea reviewer a `Claude` y human gate a `operador humano`.
- `runtime/apply.py` usa `Codex` como owner por defecto en claims adquiridos por runtime.
- Ejemplos y docs historicos pueden reforzar el modelo mental de dos agentes aunque el core file-based
  ya use owners como texto.

## Alcance futuro
- Reemplazar roles fijos por un registry de agentes/capacidades.
- Parametrizar reviewer, router y human gate.
- Eliminar enums Claude/Codex del runtime y derivarlos de configuracion/estado.
- Actualizar scaffolding y templates.
- Mantener compatibilidad aditiva con instancias existentes.

## No-alcance
- No activar autonomia multiagente por defecto.
- No romper instancias actuales sin decision + aprobacion humana.
- No acoplar el core a proveedores/modelos concretos.
