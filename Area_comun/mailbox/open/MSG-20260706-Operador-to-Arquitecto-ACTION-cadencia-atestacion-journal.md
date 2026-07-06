---
message_id: MSG-20260706-Operador-to-Arquitecto-ACTION-cadencia-atestacion-journal
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - personal/Arquitecto/TFM-medicion/corpus/medicion/medicion_journal.csv
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
one_line_summary: "Cadencia de atestacion del journal de medicion (disparado al cerrar P4.1, pendiente): recomendacion = hibrido separando CAPTURA de ANCLAJE -- hash per-unidad en un sidecar COMMITEADO (barato) + anclaje sha256 acumulado en #4 por-checkpoint (economico)."
requested_action: "Confirmar el modelo de atestacion de las filas baseline antes del cierre duro (25-jul) y la reconciliacion (26-29): (1) decir si los sha256 per-unidad YA se computan y COMMITEAN al cierre (diseno) o solo viven en el journal gitignored (hueco); (2) si es hueco, adoptar un sidecar commiteado medicion_hashlog.csv (unit_id, close_ts, sha256(snapshot)) para sellar cada fila desde su captura sin un submit_intent por unidad; (3) anclar el sha256 acumulado en #4 en cada checkpoint (sello Etapa 2 29-jul + reconciliacion 26-29)."
question: "Adoptas el hibrido (hash-log commiteado per-unidad + anclaje #4 per-checkpoint), o los sha256 per-unidad ya viajan atestados y solo hay que documentarlo? Si difiere tu diseno, dimelo con la traza."
---

# ACTION - Cadencia de atestacion del journal de medicion (recomendacion)

## Contexto (el hueco/pregunta)
Cada unidad medida escribe su fila en `medicion_journal.csv`, que esta GITIGNORED a proposito (el corpus no
se commitea; solo su manifiesto sha256 entra al #4). GOAL-P1 tuvo sha256 de primera clase (d2a13216) anclado
en el gate del sello. Pero las filas P2.1/P2.2/P4.1/P4.2/PAR-2 no se ven ancladas por sha256 en el #4 aun ->
la pregunta (disparada al cerrar P4.1): es DISENO (anclaje por-checkpoint) o HUECO (data local sin sellar)?

## Los dos modelos
- **Per-unidad:** anclar un sha256 nuevo en #4 cada cierre. Maxima evidencia anti-manipulacion, pero una
  transaccion de ledger por cierre (acopla cada cierre de dev a un submit_intent; mas trafico #4).
- **Per-checkpoint:** anclar solo en fronteras (sellos, reconciliacion). Economico, pero entre checkpoints
  las filas quedan SIN anclar -> ventana en la que un edit accidental, rotacion del err.log volatil (pierde
  tokens) o drift silencioso no se caza hasta el proximo checkpoint. Agravado: el err.log de tokens es
  VOLATIL y los veredictos baseline ya son el brazo peor-atestado (riesgo #5 del sello).

## Recomendacion: HIBRIDO (separar CAPTURA de ANCLAJE)
1. **Captura inmediata** (ya ocurre; la fila se escribe al cierre antes de rotar err.log) -- no negociable.
2. **Hash per-unidad AL CIERRE en un sidecar COMMITEADO:** `medicion_hashlog.csv` diminuto
   (`unit_id, close_ts, sha256(snapshot)`), NO gitignored. Como vive en git, el historial + la frontera #4
   de cada checkpoint hacen cada fila anti-manipulable DESDE EL INSTANTE DE CAPTURA, sin un submit_intent por
   unidad. Cierra la ventana entre-checkpoints a costo casi cero (una linea commiteada, no una transaccion).
3. **Anclaje del sha256 acumulado en #4 por checkpoint** (sello Etapa 2 29-jul + reconciliacion 26-29): el
   checkpoint ata la cadena del sidecar al ledger atestado.

Neto: evidencia per-unidad barata + anclaje #4 economico. Coherente con el precedente GOAL-P1 (sha256 al
cierre, anclaje de primera clase viaja en el gate del sello) y resuelve la ambiguedad hueco-vs-diseno
haciendo el hash per-unidad EXPLICITO y commiteado. Relevante AHORA: alimenta el cierre duro (25-jul) y le
da al Analista un ancla verificable en la reconciliacion (26-29).
