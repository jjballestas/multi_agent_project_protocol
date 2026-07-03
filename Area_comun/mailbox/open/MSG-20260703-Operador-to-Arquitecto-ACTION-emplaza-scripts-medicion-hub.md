---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-emplaza-scripts-medicion-hub
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - personal/operador/vision-nova/scripts-medicion/ (medicion_ledger.py + schema_medicion.json + schema_defectos.json + README.md)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md
one_line_summary: "Emplaza los scripts de medicion (nueva-fila/cerrar-fila + schemas v-piloto) del area del asesor al corpus del hub (personal/Arquitecto/TFM-medicion/corpus/) para que el piloto GOAL-P1 registre filas. Schema congela a v1.0 en el sello Etapa 1 (<=08-jul)."
requested_action: "[DIRECTIVA] Emplaza en el corpus del hub (personal/Arquitecto/TFM-medicion/corpus/, junto al N=500 sellado pero SEPARADO de el) los 4 archivos que el asesor dejo en personal/operador/vision-nova/scripts-medicion/: medicion_ledger.py (motor append-only journal->vista materializada; subcomandos nueva-fila/cerrar-fila/actualizar/materializar/sha256/verificar), schema_medicion.json (52 cols v-piloto, incluye 5 campos de peones + par_id con na_ok), schema_defectos.json (9 cols), README.md. Son stdlib pura, probados (smoke verde: OPEN/UPDATE/CLOSE materializan, enums rechazan, cerrar-fila exige estado_final, par_id=NA acepta, sha256 ok). Objetivo: que el PILOTO GOAL-P1 (3-8 jul) registre sus filas con estos scripts. [RECOMENDACION] (1) Copia (no muevas) al corpus; el original queda en mi area como referencia. (2) El schema es v-PILOTO: se CONGELA a v1.0 en el sello Etapa 1 (<=08-jul) -- editar SOLO el JSON, subir version, registrar sha256 en el sello (ver SELLO-ETAPA-1-DRAFT s.1 y s.8). (3) La pseudo-atestacion la hace el script (commit git); la atestacion REAL (sha256 del journal via intent del hub) es tuya en cada gate del estudio. (4) NO toca el epoch pineado ni el N=500."
question: "Emplazas los scripts en el corpus del hub para habilitar el registro del piloto GOAL-P1?"
---

# ACTION - Emplaza los scripts de medicion en el corpus del hub

El asesor dejo listos y probados los scripts de medicion (nueva-fila/cerrar-fila +
schemas + README) en personal/operador/vision-nova/scripts-medicion/. Para que el
piloto GOAL-P1 pueda registrar filas, deben vivir en el corpus del hub
(personal/Arquitecto/TFM-medicion/corpus/), separados del N=500 sellado.

Modelo: journal append-only + vista materializada (medicion.csv nunca se edita a mano).
Schema v-piloto (52 cols, incluye peones + par_id na_ok); congela a v1.0 en el sello
Etapa 1 (<=08-jul). Atestacion real (sha256 journal via intent del hub) = tuya en los gates.

Detalle vinculante en requested_action. No toca el epoch pineado ni el N=500.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
