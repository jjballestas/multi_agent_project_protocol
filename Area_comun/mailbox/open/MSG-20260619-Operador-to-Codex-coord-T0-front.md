---
message_id: MSG-20260619-Operador-to-Codex-coord-T0-front
type: FYI
task_id: TASK-0124
from: Operador
to: Codex
requires_response: false
status: open
one_line_summary: Respaldo el GO-T0 del Arquitecto (front MVP, TASK-0124). Heads-up de ruta: el diseno y los insumos viven en D:\Agentes\Zeus\Zeus-protocol\design (brief/diseno UI en design\interface). Para la etapa 1 (andamiaje) NO necesitas el diseno visual aun (se genera aparte con Claude Design). Lee el CANONICO, no el working tree. Escrituras solo por submit_intent. maker!=checker con el Arquitecto.
context_refs:
  - Area_comun/mailbox/open/MSG-20260619-Arquitecto-to-Codex-GO-T0-front-mvp.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
deadline_or_blocking_level: none
---

# Coordinacion operador - T0 front MVP

Codex: respaldo el **GO-T0** del Arquitecto. Arranca el front MVP (TASK-0124) con su secuencia (connector
CI floor -> etapa 1 andamiaje -> ...), de a una etapa, maker(tu)!=checker(Arquitecto). Solo agrego, como
operador, lo que no estaba o cambio:

## Ruta del diseno (corregida)
- **Insumos:** `D:\Agentes\Zeus\Zeus-protocol\design\front_requirements.html` (RF/RNF) +
  `front_pipeline.html` (etapas).
- **Diseno UI** (Claude Design): se depositara en `D:\Agentes\Zeus\Zeus-protocol\design\interface\`.
- **Aun NO esta generado** (lo corre el operador aparte). Para la **etapa 1 (andamiaje)** NO lo necesitas;
  procede con stack web + CI + lectura read-only + esqueleto. El diseno alimenta las **tareas de UI** (etapa
  posterior). El Arquitecto corrige las refs viejas de SPEC-0086 (`Zeus\design` -> `Zeus-protocol\design`).

## Recordatorios clave (no negociables)
- **Lee el CANONICO** (objetos git / origin/main), **NO el working tree** del mount: se re-trunca/cachea
  (anomalia conocida, RUNBOOK). Verifica contra el commit, no contra archivos volatiles.
- **Codigo SOLO en `Zeus-protocol`** (repo separado, acoplamiento unidireccional; **no toques el core
  neutral** ni `*.template.*`).
- **Ninguna escritura directa** al estado/ledger: todo write va por `submit_intent` (escritor unico, gates
  + #4 + drift). Sin bypass. Claims **file-scoped**.
- **PII-free** (este proyecto no maneja PII). **Canal ASCII**. **#4 intacto** (epoca 1.14.0, sin re-genesis).

Reporta a in_review por etapa al Arquitecto (el reproduce). Cualquier bloqueo real -> mailbox con pregunta
concreta. Gracias.
