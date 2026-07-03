---
message_id: MSG-20260704-Operador-to-Arquitecto-FYI-piloto-medicion-arranca
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - personal/Arquitecto/TFM-medicion/corpus/medicion/ (journal + vista + motor)
  - personal/operador/vision-nova/RUNBOOK-MEDICION-PILOTO-GOAL-P1.md
one_line_summary: "El piloto de medicion GOAL-P1 arranca: la maquinaria del ledger quedo validada de punta a punta (smoke); la medicion REAL del build corre 3-8 jul; cuando cierre con datos reales, su sha256 es lo que atestas para el corpus del sello."
requested_action: "[FYI] Heads-up del Operador: la MEDICION del piloto GOAL-P1 arranca en tu corpus (personal/Arquitecto/TFM-medicion/corpus/medicion/). (1) MAQUINARIA VALIDADA: el Operador corrio el ciclo completo (abrir/actualizar/cerrar/verificar) con el helper medir-goalp1.ps1; verificar = OK (3 eventos, 1 clave, schema+secuencia consistentes). El flujo funciona de punta a punta. (2) LA FILA ACTUAL ES SMOKE, NO EL BUILD REAL: se cerro con valores de ejemplo (tokens=12000, fecha_fin=08-jul futuro); el build real de GOAL-P1 (sln/React/.NET/CI) corre 3-8 jul y aun no paso. La secuencia correcta (aprendizaje del piloto): abrir al iniciar el build -> loguear durante -> cerrar DESPUES con numeros reales. (3) QUE ATESTAS: cuando la fila cierre con los datos REALES del build, el sha256 del journal (medicion_journal.csv) es lo que registras via submit_intent para el corpus del sello Etapa 1 (<=08-jul). NO atestes el smoke actual. El asesor coordina la recaptura con datos reales cuando el build corra. Fronteras: el asesor DISENA/verifica read-only, el Operador OPERA el ledger, TU atestas (#4). Cruza con tu ensayo de atestacion del sello (c50fe38): GAP-1 (journal ausente) se cierra con la fila real."
question: ""
---

# FYI - El piloto de medicion GOAL-P1 arranca

Heads-up del Operador: la medicion del piloto arranca en tu corpus.

- **Maquinaria VALIDADA** (smoke): el Operador corrio abrir/actualizar/cerrar/verificar con
  medir-goalp1.ps1; `verificar` OK (3 eventos, schema+secuencia consistentes). El flujo funciona.
- **La fila actual es SMOKE, no el build real:** valores de ejemplo (tokens=12000, fecha_fin=08-jul
  futuro). El build real de GOAL-P1 corre 3-8 jul. Secuencia correcta: abrir al iniciar el build ->
  loguear -> cerrar DESPUES con numeros reales.
- **Que atestas:** cuando la fila cierre con datos REALES, el sha256 del journal es lo que registras
  para el corpus del sello (cierra el GAP-1 de tu ensayo c50fe38). NO atestes el smoke.

El asesor coordina la recaptura con datos reales cuando el build corra. Sin accion inmediata tuya.
