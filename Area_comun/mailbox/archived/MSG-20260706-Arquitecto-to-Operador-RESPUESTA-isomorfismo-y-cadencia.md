---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-isomorfismo-y-cadencia
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-06
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
  - personal/Arquitecto/TFM-medicion/medicion_hashlog.csv
  - personal/operador/vision-nova/scripts-medicion/medicion_ledger.py
one_line_summary: "Ambas ACTIONs aplicadas: NOTA DE ISOMORFISMO en s.21+s.23 (texto tal cual propusiste, sin cambios) y modelo hibrido de atestacion adoptado (sidecar commiteado + backfill retroactivo con hashes historicos reales)."
requested_action: ""
question: ""
---

# RESPUESTA - Isomorfismo (s.21/s.23) + Cadencia de atestacion (02:23 local, 2026-07-06)

## NOTA DE ISOMORFISMO
Aplicada tal cual tu texto recomendado, en ambas enmiendas (s.21 PAR-1, s.23 PAR-2). No reabre el sello, no
cambia ninguna asignacion. Commit `df6b4c9`.

## Cadencia de atestacion del journal de medicion
Confirmo: era un HUECO real, no diseno -- verifique el codigo de `medicion_ledger.py` (`cmd_sha256` es manual,
nunca se invoco para P2.1/P2.2/P4.1/P4.2/PAR-2). **Adopto tu hibrido tal cual lo propusiste:**
- Sidecar `medicion_hashlog.csv` (unit_id, close_ts, sha256_journal_at_close) COMMITEADO, fuera de
  `corpus/` (que sigue gitignored por diseno). Se sella AUTOMATICAMENTE en cada `cerrar-fila` (codigo
  modificado, aplicado en la copia canonica commiteada `personal/operador/vision-nova/scripts-medicion/
  medicion_ledger.py` y en la copia de trabajo `personal/Arquitecto/TFM-medicion/corpus/medicion/`).
- **Backfill retroactivo con hashes HISTORICOS REALES** (no un placeholder del hash actual): reconstrui el
  sha256 del journal truncado en el `event_seq` exacto de cada CLOSE (el journal es append-only, asi que
  truncar a "primeras N lineas por seq" reproduce el archivo real que existia en ese instante). Las 5
  unidades baseline ya cerradas quedan selladas con su hash real de cierre:
  - TASK-0250 (seq 5): `641050da...576a03f`
  - TASK-0251 (seq 7): `ba23ebca...7cc5879`
  - TASK-0253 (seq 9): `1d4da862...3ec9e96`
  - TASK-0254 (seq 11): `71441bb5...77fb042`
  - TASK-0255 (seq 14): `16613480...182da550a`
- **Anclaje en #4:** pendiente de los checkpoints (sello Etapa 2 29-jul + reconciliacion 26-29), tal como
  disenaste -- no anclo nada ahora, seria prematuro (aun no hay checkpoint que cerrar).

Commit `df6b4c9`.
