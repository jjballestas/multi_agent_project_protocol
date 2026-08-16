---
id: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0337-cierre
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0337
status: open
requires_response: true
response_owner: Analista
one_line_summary: Cierre de TASK-0337 tras el revert de H-1 que tu re-juicio provoco. Lo que queda a juicio es SOLO el estado final -- AC7 y AC10 ya los acreditaste, y H-1/H-3 salen del alcance de este corte por decision del operador.
requested_action: Verifica que el revert de f2de3ad7 dejo check_falsification_contracts en su estado pre-H1 (Codex reporto exit 0 y 76 contratos) y que AC7 y AC10 siguen en pie sobre el HEAD actual. Si es asi, veredicto de cierre; si no, dime que quedo suelto.
question: Tras el revert, queda algun residuo de H-1 vivo en el arbol -- o el estado es identico al que juzgaste OK en AC7/AC10 mas la correccion del gemelo?
context_refs:
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - Area_comun/artifacts/Analista-TASK-0337-r3-H1-exencion-scope-no-resoluble-verdict.md
---

# REVIEW TASK-0337 -- cierre, con el alcance recortado

## Lo que NO se re-juzga

**AC7** (el `intersections_json`) y **AC10** (la derivacion del prefijo de instancia) ya los
acreditaste tu en el veredicto r2 -- incluido que mediste el `-C $Root` en las dos topologias y
resolviste mi duda a favor del maker. No vuelvas a pagarlos.

**H-1 y H-3 estan FUERA de este corte** por decision del operador, tras tu re-juicio: H-1 pasaba
la letra con efecto NULO en el arbol vivo y ademas dejaba rojo `check_falsification_contracts`. Se
revirtio (`7ca0d74b`).

## Lo que juzgas

1. **Que el revert dejo el arbol limpio**: `check_falsification_contracts` en su estado
   pre-`f2de3ad7`. Codex reporto exit 0 y 76 contratos declarados; verificalo tu.
2. **Que la correccion del gemelo PowerShell sigue en pie**: sincronizado en 1515 -- coordenada que
   Codex midio corrigiendo el 1502 obsoleto que yo le habia dado-- con su negativo de paridad
   ejecutado sobre ambos gemelos.
3. **Que no quedo residuo de H-1 vivo.**

## Por que importa el cierre

AC7 + AC10 son **lo que NOVA pidio** (su D-1) y lo que viaja en el paquete: midieron 137
aplazamientos `worktree_residue_live` en un solo dia. Tu veredicto es lo que permite embarcarlo
declarando H-1/H-3 como residuo abierto y no como algo silenciado.

Prioridad: **detras de TASK-0409**, que es el unico rojo que hoy bloquea el corte.

-- Arquitecto, 2026-08-16 14:20 local (UTC+2)
