---
message_id: MSG-20260619-Arquitecto-to-Codex-GO-T0-front-mvp
type: GO
task_id: TASK-0124
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: "T0 - KICKOFF del proyecto-front (primer handoff gobernado, atestado bajo #4). MVP single-operator (SPEC-0086/DECISION-0049). Codigo en D:\\Agentes\\Zeus\\Zeus-protocol (ya git-init); gobernanza en Area_comun (dataset). Secuencia: connector CI (floor, prereq) -> etapa 1 andamiaje (TASK-0124). Codex maker, Arquitecto checker."
requested_action: "T0 del proyecto-front. (1) Prereq floor: implementar el connector CI (deny-by-default, fixtures, off-by-default; DECISION-0048) ANTES del codigo que compila/testea -- el Arquitecto autora su SPEC como la siguiente pieza del floor; espera esa SPEC o coordina ETA. (2) Etapa 1 andamiaje (TASK-0124, SPEC-0086) en Zeus-protocol: stack web + CI verde (via connector CI) + lectura READ-ONLY del canonico del protocolo (objetos git/origin, NO working tree) + esqueleto navegacion. CODIGO solo en Zeus-protocol (repo separado, unidireccional, NO tocar el core). NINGUNA escritura directa al estado/ledger (etapa 3 = via submit_intent, sin bypass). Avanzar a in_review con claim file-scoped + submit_intent; yo reproduzco (checker). De a una etapa."
question: "Confirmas T0 (kickoff front MVP) y ETA? Implementas primero el connector CI (floor) y luego la etapa 1 andamiaje (TASK-0124)? Avisas en in_review por etapa para mi reproduccion."
context_refs:
  - Area_comun/decisions/DECISION-0049-proyecto-front-primario-t0-zeus.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0124-codex-front-mvp-etapa1-andamiaje.md
  - Area_comun/decisions/DECISION-0048-connectors-accion-tool-policy.md
deadline_or_blocking_level: normal
---

# T0 - KICKOFF proyecto-front MVP (single-operator)

**Este handoff ES T0** (primer handoff gobernado del proyecto-front, atestado en caliente bajo #4 = nace el
dataset publicable, PII-free). GO del operador (DECISION-0049). Proyecto PRIMARIO de tesis.

## Encuadre
- **Producto** (codigo) en `D:\Agentes\Zeus\Zeus-protocol` (ya git-init, commit 09be6b8); acoplamiento
  unidireccional; **el core neutral NO se toca**. **Gobernanza** (SPEC/tasks/handoffs) en `Area_comun`
  (atestada #4 = dataset). Single-operator (multi-tenant fuera de alcance). #4 epoca 1.14.0 (sin re-genesis;
  capacidades fuera del config pinned, DECISION-0047).
- **Principio rector:** el front OBSERVA por patron read-only sobre el CANONICO (no el working tree) y OPERA
  solo via `submit_intent` (escritor unico; sin bypass de gates/#4/drift). PII-free; canal ASCII.

## Secuencia (de a una pieza, maker=Codex/checker=Arquitecto)
1. **Floor pieza 2 - connector CI** (prereq de "el codigo que compila/testea"): deny-by-default, fixtures,
   off-by-default (DECISION-0048). Autoro su SPEC ahora-siguiente; implementalo antes del codigo del front.
2. **Etapa 1 - andamiaje (TASK-0124, SPEC-0086):** stack web en Zeus-protocol + CI verde + lectura read-only
   del canonico + esqueleto navegacion. Sin escrituras directas.
3. Luego etapa 2 (observar RF-1..RF-4) y etapa 3 (operar RF-5..RF-8 via submit_intent), una a la vez.

## DoD etapa 1
SPEC-0086 AC1/AC5/AC6/AC7/AC10; CI del producto verde; lectura read-only del canonico; gobernanza en
Area_comun valida (validate exit 0 con y SIN secretos, drift 0); sin tocar #4/core. Reporta a in_review por
etapa. Canal ASCII.
