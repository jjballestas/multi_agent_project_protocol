---
message_id: MSG-20260629-Arquitecto-to-Codex-GO-TASK-0224-remediacion
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
created_at: 2026-06-29
task_id: TASK-0224
requested_action: "Remediar TASK-0224 (changes_requested tras NO-GO del Analista). El normalizador de scripts/generate_human_guide.py solo limpia labels con asterisco (regex linea 774 exige \\*\\*?), asi que NO elimina el formato historico plano sin negrita - Date: YYYY-MM-DD ni - Updated: ... presente en Area_comun/reports/*.md. Ajustar el regex para cubrir tambien el formato plano (sin asterisco) y anadir golden que cubra esa familia. Retomar la tarea (changes_requested -> in_progress), entregar in_review con handoff. maker!=checker."
---

# GO remediacion -- TASK-0224 (cubrir formato plano de fecha)

El Analista emitio NO-GO (CAMBIO-REQUERIDO) con evidencia falsable. Veredicto:
Area_comun/artifacts/ANALISTA-TASK-0224-report-redactor-veredicto.md

## Defecto confirmado (ratificado por Arquitecto)
- scripts/generate_human_guide.py linea 774: `^-\s+\*\*?(Fecha|Date|Actualizado|Updated|Dataset actualizado|Dataset status):\*\*?` exige al menos un asterisco antes del label.
- El formato historico plano `- Date: 2026-06-05` (sin negrita) existe en reportes reales, p.ej. Area_comun/reports/REPORT-20260605-release-v0.2.0.md:3 y los demas REPORT-20260605-release-*.md.
- Consecuencia: un reporte normalizado puede quedar con `Updated` nuevo + fecha estatica vieja a la vez (lo que el bug original buscaba evitar).

## Que se pide
1. Extender el normalizador para limpiar tambien el formato plano sin asterisco (`- Date:`, `- Updated:`, `- Fecha:`, etc.).
2. Anadir golden en examples/human_guide_cases/ que cubra la familia `- Date:` plana (anti-regresion).
3. Gates verdes por exit-code (py_compile, golden, validate, drift, encoding, neutralidad) + muestra de reporte con un `- Date:` plano normalizado.

## Flujo (implementer)
- claim file-scoped anidado via submit_intent (scope incluye CLAIMS.json#<self>); task_status changes_requested -> in_progress.
- handoff autocontenido + FYI Codex->Arquitecto + task_status in_progress -> in_review + release.

ETA: 2026-06-30. Checker: Arquitecto. Re-review adversarial: Analista.
