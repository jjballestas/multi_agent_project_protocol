---
message_id: MSG-20260622-Operador-to-Arquitecto-GO-CIERRE-FASEA-Y-BC
task_id: TASK-0150
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "(1) CERRAR Fase A (TASK-0150) -> done: el Analista dio OK/CERRABLE 10/10 por comportamiento (server no-modelo-egress, raw fuera del #4, candidatas no-ledger, PII best-effort honesta, #4 byte-identica). (2) ARRANCAR Fase B (panel + gate humano de PII + re-screen candidate->intake) y Fase C (agente extractor), PLEGANDO las 2 recomendaciones del Analista como AC/prerequisito: (a) ampliar el guard AC40 a TODO src/** y marcar CUALQUIER red saliente (no solo proveedores nombrados) ANTES de Fase C (cuando enciende el agente = ventana real de modelo); (b) politica de purga/TTL del raw en os-tmp. (3) Atender el flake de timeout (1a corrida 41/42 luego 42/42 x3): hacer el test determinista/no sensible a timeout para que no parpadee en CI. La rama 'por archivo' del selector sigue GATEADA tras B/C; uso vivo OFF (requiere GO aparte mio cuando este lista)."
question: "Cierras Fase A (Analista OK) y arrancas B/C plegando las 2 recomendaciones del Analista como AC (guard AC40 a todo src/** + cualquier salida de red antes de Fase C; purga/TTL del raw), y de paso estabilizas el test del flake de timeout?"
one_line_summary: "GO: cerrar Fase A (TASK-0150, Analista OK/CERRABLE 10/10) y arrancar Fase B (panel+gate PII) y C (agente extractor) plegando como AC las 2 recos del Analista (ampliar guard AC40 a todo src/** + marcar cualquier red saliente antes de Fase C; purga/TTL del raw) + estabilizar el flake de timeout. Rama 'por archivo' gateada tras B/C; uso vivo OFF (GO aparte)."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0150-v2-faseA-veredicto.md
  - Area_comun/tasks/TASK-0150-codex-file-intake-v2-faseA.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
deadline_or_blocking_level: normal
---

# GO - cerrar Fase A + arrancar B/C plegando las recos del Analista

El Analista dio Fase A **OK/CERRABLE (10/10 por comportamiento)**. GO para:

1. **Cerrar Fase A** (TASK-0150) -> done.
2. **Arrancar Fase B** (panel de revision + **gate humano duro de PII** + re-screen candidate->intake) y
   **Fase C** (agente extractor), **plegando como AC** las 2 recomendaciones del Analista (prerequisito, NO
   opcionales):
   - **AC: ampliar el guard AC40 a TODO `src/**`** y marcar **CUALQUIER** red saliente (no solo los proveedores
     nombrados) **ANTES de Fase C** -- es cuando enciende el agente = la ventana real de modelo.
   - **AC: politica de purga/TTL del raw** en os-tmp.
3. **Estabilizar el flake de timeout** (1a corrida en frio 41/42, luego 42/42 x3): test determinista/no
   sensible a timeout, para que no parpadee en CI.

La rama "por carga de archivo" del selector sigue **gateada tras B/C**. El **uso vivo de la v2 sigue OFF** y
requiere un **GO aparte mio** cuando este lista (con su pasada de Analista al cierre de C, como siempre).
Canal ASCII.
