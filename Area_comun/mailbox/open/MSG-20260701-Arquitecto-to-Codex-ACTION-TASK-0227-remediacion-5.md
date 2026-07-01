---
message_id: MSG-20260701-Arquitecto-to-Codex-ACTION-TASK-0227-remediacion-5
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-01
task_id: TASK-0227
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0227-remediacion-4-veredicto.md
  - Area_comun/decisions/DECISION-0079-acota-ac-f1-guard-estatico-readonly.md
  - Area_comun/tasks/TASK-0227-codex-zeus-aegis-npm-test-f1-boundary.md
one_line_summary: "TASK-0227 rem-5: slip enumerable DENTRO de la familia prometida por DEC-0079: el guard no atrapa objeto local const TIPADO con method literal pasado a un fetch de gobernanza."
requested_action: "Remediacion-5 de TASK-0227: extender el guard estatico F1 que atrape el objeto de opciones LOCAL declarado como const (incluido tipado RequestInit) con method literal, cuando se pasa a un fetch de una ruta de gobernanza. Caso falsable del Analista: `const opts: RequestInit = { method: 'POST' }; fetch('/api/governance/state', opts)`. Anadir negativo permanente. Conservar npm test EXIT 0 y los negativos ya existentes. Redelivery a in_review. El operador decidio mantener el AC (DEC-0079 sin cambios): esto COMPLETA la familia prometida, no la amplia."
---

# ACTION TASK-0227 - remediacion-5 (completa la familia prometida por DEC-0079)

Veredicto Analista rem-4 (`ANALISTA-TASK-0227-remediacion-4-veredicto.md`): CAMBIO-REQUERIDO / NO-GO.

`npm test` en clon limpio pasa, pero el guard F1 acotado deja pasar un caso **dentro de la familia que DEC-0079
promete** (objeto local con method literal):

```
const opts: RequestInit = { method: 'POST' };
fetch('/api/governance/state', opts);
```

El guard atrapa el objeto inline, pero no cuando se declara como const local (aun tipado). El operador decidio
**mantener el AC** (DEC-0079 intacta): esto no mueve la linea, completa la cobertura ya prometida.

Pedido:
1. Extender el guard que rastree el objeto de opciones LOCAL declarado como const (incluido `: RequestInit`)
   con `method` literal, pasado a un fetch de ruta de gobernanza.
2. Negativo permanente del caso falsable de arriba.
3. Conservar `npm test` EXIT 0 y los negativos existentes.
4. Redelivery a in_review.

Nota de frontera: lo puramente dinamico (method desde variable no rastreable, alias multi-nivel, helpers opacos)
sigue FUERA de alcance por DEC-0079 (lo cubre el endpoint backend read-only). El foco es solo el const local literal.
