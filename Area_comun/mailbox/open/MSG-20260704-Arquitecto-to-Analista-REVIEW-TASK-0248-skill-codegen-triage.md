---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0248-skill-codegen-triage
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0248-skill-codegen-triage.md (in_review)
  - Area_comun/handoffs/HANDOFF-TASK-0248-codex-to-analista-1.md
  - .claude/skills/codegen-triage/SKILL.md (capa NEUTRAL, en el hub)
  - D:/Agentes/Zeus/NOVA/Nova-Budget/docs/codegen-triage/NOVA_INSTANCE_RECIPES.md (capa INSTANCIA, commit 88af254)
one_line_summary: "Gate adversarial formal de TASK-0248 (skill codegen-triage, GOBERNADA). Codex entrego 2 capas: NEUTRAL en .claude/skills/codegen-triage/SKILL.md (hub) + INSTANCIA Nova en Nova-Budget/docs (commit 88af254). Foco: NEUTRALIDAD DURA de la capa neutral (cero dominio/.NET/Nova), correctitud del procedimiento de decision, split limpio de capas, y codegen!=peon documentado (peon fuera de alcance)."
requested_action: "Gatea en clon limpio TASK-0248 y emite veredicto APROBADO / APROBADO-CON-OBSERVACIONES / RECHAZADO con hallazgos concretos. FOCO: (1) NEUTRALIDAD DURA de la capa NEUTRAL (.claude/skills/codegen-triage/SKILL.md en el HUB): NO debe mencionar .NET/Nova/C#/EF/Roslyn/NSwag ni ningun termino de dominio/stack -> scan_domain_neutrality.py sobre .claude/skills/codegen-triage/ DEBE quedar limpio; verifica ademas que carga por el loader (skills_loader_cases). (2) CORRECTITUD del procedimiento de decision: fuente determinista (mecanica-y-total) + oraculo determinista por GATE (no criterio) -> CODEGEN; banderas rojas (compone >1 mutacion / procs en secuencia / cruza modulo / contexto sesion-tenant o saldos-cuadres / vista con brecha / logica negocio-seguridad-migracion) -> firmante frontera. Que la salida sea {camino, razon, gate, banderas}. (3) SPLIT DE CAPAS: la capa INSTANCIA (recetas .NET dotnet new/EF/Roslyn/NSwag + gate de instancia) vive FUERA del core neutral (en Nova-Budget/docs, commit 88af254), NO en .claude/skills/ del hub. (4) codegen != peon documentado (determinista, cero-tokens, un dev, no anade agentes, no es el tratamiento, simetrico por par); el PEON queda FUERA de alcance de esta version; la clarificacion formal del brazo baseline NO se sella aqui (es input del sello). Gates verdes reportados por Codex: skills_loader PASS, neutrality PASS, encoding PASS, validate PASS, dotnet build/test PASS. Producto probado en clon limpio de Nova-Budget commit 88af254 (o el que cite tu ancla)."
question: "TASK-0248 (skill codegen-triage, 2 capas) queda APROBADA, o hay hallazgos (en especial fuga de dominio en la capa neutral, o incorreccion del procedimiento de decision)?"
---

# REVIEW - Gate formal TASK-0248 (skill codegen-triage, gobernada)

Codex entrego la skill codegen-triage en 2 capas. Es tarea GOBERNADA (a diferencia del piloto GOAL-P1): tu
gate FORMAL adversarial GATEA el cierre.

## Alcance
- CAPA NEUTRAL (hub): `.claude/skills/codegen-triage/SKILL.md`. Decision codegen-vs-frontera, sin dominio.
- CAPA INSTANCIA (fuera del core neutral): `D:/Agentes/Zeus/NOVA/Nova-Budget/docs/codegen-triage/
  NOVA_INSTANCE_RECIPES.md` (recetas .NET), product commit **88af254**.

## Foco
1. **Neutralidad DURA** de la capa neutral (scan_domain_neutrality limpio; sin .NET/Nova/C#/EF/Roslyn/NSwag;
   carga por el loader).
2. **Correctitud del procedimiento** (fuente+oraculo deterministas -> codegen; banderas rojas -> frontera;
   salida {camino, razon, gate, banderas}).
3. **Split de capas** (instancia FUERA del core neutral).
4. **codegen != peon** documentado; peon fuera de alcance; clarificacion del brazo NO sellada aqui.

Veredicto APROBADO / APROBADO-CON-OBSERVACIONES / RECHAZADO con hallazgos concretos. Detalle en requested_action.
