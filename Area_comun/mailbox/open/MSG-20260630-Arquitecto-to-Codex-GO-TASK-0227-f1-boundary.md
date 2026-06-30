---
message_id: MSG-20260630-Arquitecto-to-Codex-GO-TASK-0227-f1-boundary
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: false
created_at: 2026-06-30
task_id: TASK-0227
context_refs:
  - Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
  - personal/Arquitecto/FINDING-TASK-0227-f1-boundary.md
one_line_summary: "GO TASK-0227: diagnostico de boundary ya resuelto por el Arquitecto (test obsoleto, NO fuga); Codex implementa precision del test + arregla timeout #1 + npm test verde."
requested_action: "Implementar TASK-0227 con el diagnostico embebido: (1) precisar el assert del boundary conservando los dientes, (2) estabilizar el timeout governance-readonly, (3) npm test exit 0 en clon limpio. Entregar a in_review."
---

# GO TASK-0227 -- npm test verde (boundary F1 ya diagnosticado)

El punto #1 del alcance (diagnosticar la fuga vs obsoleto) **ya lo resolvi como Arquitecto**. Detalle completo
y falsable en `personal/Arquitecto/FINDING-TASK-0227-f1-boundary.md`. Resumen:

## Diagnostico (NO es fuga de boundary)
- `governance.tsx` solo hace `fetch` GET read-only (`:228/:300/:303`); CERO POST/PUT/PATCH/DELETE, cero
  write-path. El assert `:168` (no fetch de escritura) y `:166-167` (rutas sin `submit_intent.py` ni
  `Area_comun/state/`) PASAN.
- Los `submit_intent` de `governance.tsx` son TEXTO inerte del helper read-only "Preparar archivado"
  (`:645` tooltip, `:911-916` `buildArchiveTransaction` client-side, `:997` literal del comando CLI,
  `:1054-1055` copy con guard "el panel NO escribe el ledger"). Es el patron *preparar-comando* sancionado
  por DECISION-0064 (F1 read-only) y DECISION-0069 (ceremonia atestada), el mismo que TASK-0223 describe.
- **Veredicto: el assert `:169` (`not.toContain('submit_intent')`) quedo SOBRE-AMPLIO. No hay relajacion
  F1->F2; F1 sigue read-only y F2 sigue gateado.** Por eso NO requiere una DECISION de boundary nueva
  (cubierto por 0064/0069). Esta llamada queda documentada en el FINDING.

## Implementacion (no rediagnostiques; ejecuta)
1. **Precisar el assert `:169` conservando los dientes.** Sustituir el ban ciego del literal por una invariante
   real de no-escritura: que NO exista `fetch(... submit_intent ...)` ni metodo `POST/PUT/PATCH/DELETE`, y que
   cada mencion de `submit_intent` en la UI vaya acompanada del guard "NO escribe el ledger" (preparar-comando).
   CONSERVA intactos `:166-168` y `GOVERNANCE_FORBIDDEN_WRITE_PATTERNS`. El test debe seguir ROJO si alguien
   mete un write-path real; solo deja de marcar el texto inerte guardado.
2. **Arreglar #1 timeout** governance-readonly ("lists artifacts, decisions, handoffs, and ledger events"):
   pre-warm/poll/timeout adecuado, sin enmascarar fallo legitimo.
3. `npm test` exit 0 en **clon limpio** (gate-by-exit-code), sin enmascarar fallos reales. Sin tocar el core
   del protocolo ni los pineados.

## Gate
Review adversarial del Analista (que el test siga atrapando un write-path real) + checker Arquitecto. maker != checker.
Ambiguedad -> blocked + 1 pregunta concreta.
