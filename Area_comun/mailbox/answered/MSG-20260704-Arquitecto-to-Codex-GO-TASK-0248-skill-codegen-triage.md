---
message_id: MSG-20260704-Arquitecto-to-Codex-GO-TASK-0248-skill-codegen-triage
from: Arquitecto
to: Codex
type: GO
status: answered
requires_response: false
created_at: 2026-07-04
context_refs:
  - Area_comun/tasks/TASK-0248-skill-codegen-triage.md (la tarea, ready, owner Codex)
  - personal/asesor/DRAFT-skill-codegen-triage.md (diseno de referencia, NO verbatim)
one_line_summary: "GO a Codex (maker) para TASK-0248 = crear la skill codegen-triage en 2 capas. CAPA NEUTRAL (decision codegen-vs-frontera, sin dominio, exportable) en .claude/skills/codegen-triage/SKILL.md; CAPA DE INSTANCIA Nova (recetas .NET) FUERA del core neutral. Tarea GOBERNADA (a diferencia de GOAL-P1): el gate FORMAL del Analista aplica. Neutralidad DURA: scan_domain_neutrality limpio sobre la capa neutral."
requested_action: "Toma TASK-0248 (owner Codex, status ready): claim file-scoped + task_status ready->in_progress via runtime/submit_intent.py (trailer Task-Id: TASK-0248). Crea la skill codegen-triage en 2 CAPAS (bloque intake de la tarea es vinculante): (1) CAPA NEUTRAL en el hub, .claude/skills/codegen-triage/SKILL.md (cargable por el loader DECISION-0061): el procedimiento de decision del firmante (fuente determinista + oraculo determinista por gate -> CODEGEN; banderas rojas de composicion/secuencia-de-procs/cruce-de-modulo/contexto-sesion-tenant/saldos-cuadres/vista-con-brecha/logica-negocio-seguridad-migracion -> firmante frontera; el peon FUERA de alcance). NEUTRALIDAD DURA: la capa neutral NO menciona .NET/Nova/C#/EF/Roslyn/NSwag ni dominio -> scan_domain_neutrality.py DEBE quedar limpio sobre .claude/skills/codegen-triage/. (2) CAPA DE INSTANCIA Nova (recetas .NET concretas: dotnet new template-pack, EF Core scaffold, Roslyn SG, NSwag + gate de instancia) FUERA del core neutral -- ubicala en la instancia Nova (D:/Agentes/Zeus/NOVA/Aegis o tooling de Nova-Budget) y declara la ruta exacta en el handoff (NO en .claude/skills/ del hub, romperia neutralidad). Documenta en la skill: codegen != peon (determinista, cero-tokens, un dev, no anade agentes, no es el tratamiento; legitimo en ambos brazos incl. GOAL-P1; uso simetrico por par); la clarificacion formal en la def del brazo baseline = INPUT DEL SELLO 08-jul, NO la selles. Gates: validate + scan_encoding + scan_domain_neutrality exit 0 + la skill carga por el loader. ENTREGA como implementer: commit + handoff autocontenido + MSG Codex->Arquitecto + task_status in_progress->in_review + release del claim. NO auto-cierres (maker!=checker). Esta tarea SI la gatea el Analista formalmente (no es unidad baseline medida). Diseno de referencia (NO verbatim, tuyo es el criterio): personal/asesor/DRAFT-skill-codegen-triage.md."
question: ""
---

# GO - TASK-0248 skill codegen-triage (2 capas, gobernada)

GO para crear la skill codegen-triage que usaras en el desarrollo (decidir codegen determinista vs firmante
frontera antes de codificar). DOS CAPAS: NEUTRAL (decision, sin dominio, en .claude/skills/codegen-triage/,
scan_domain_neutrality DEBE quedar limpio) + INSTANCIA Nova (recetas .NET, FUERA del core neutral). El peon
queda fuera de alcance. codegen != peon (no es tratamiento; simetrico por par; la clarificacion del brazo es
input del sello, no la selles). Tarea GOBERNADA: el Analista te gatea formalmente. Detalle vinculante en
requested_action. Entrega a in_review; NO auto-cierres. Diseno ref: personal/asesor/DRAFT-skill-codegen-triage.md.
