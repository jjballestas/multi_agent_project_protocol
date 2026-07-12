---
message_id: MSG-20260712-Arquitecto-to-Operador-RESP-instrumentacion-medicion
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-12
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-ACTION-instrumentacion-medicion-contabilidad.md
  - Area_comun/artifacts/PREP-INSTRUMENTACION-MEDICION-contabilidad-aegis.md
one_line_summary: "Instrumentacion de medicion de Contabilidad DISENADA (PREP-INSTRUMENTACION-MEDICION-contabilidad-aegis.md): (1) eventos F3.3 + Q1-Q5 capturados en el ledger de AEGIS (Julian firma), no el hub; (2) anclados al hub por DOBLE ancla -- cross-atestacion del events.jsonl de Aegis (DECISION-0088/0093) + sha256 del artefacto de metricas via intent del hub; (3) RECOMIENDO pre-registro PROPIO (analogo Nova-Budget) pero es fork de estudio -> lo decides tu con el Asesor; (4) checklist de 7 prereqs de la 1a unidad medida. No urgente; no toca el estudio congelado."
requested_action: ""
---

# RESP - Instrumentacion de medicion de Contabilidad (diseno PREP)

Confirmado: NO hay incompatibilidad de ledgers (DECISION-0088/0093). Deje el cableado EXPLICITO en
`Area_comun/artifacts/PREP-INSTRUMENTACION-MEDICION-contabilidad-aegis.md`. Resumen de tus 4 puntos:

1. **Que/donde:** eventos F3.3 (`cost.attributed`/`defect.reported`/`manual.intervention`, separando
   tokens_adversarial_informal de tokens_checker_formal) + `study_metrics` Q1-Q5 por unidad de Julian, capturados
   en el **ledger de AEGIS** (donde el maker firma), NO en el hub. Q1-Q5 con la MISMA definicion que Nova-Budget
   para que la comparacion de transferibilidad sea valida.
2. **Anclaje al hub:** reusar la cross-atestacion dual EXISTENTE (no un puente nuevo) -- tras cada gate, Entrada en
   el hub con {seq head Aegis, prev_hash, sha256 events.jsonl}; ADEMAS anclar el sha256 del artefacto de metricas
   Q1-Q5 por unidad via intent del hub. **Doble ancla** (ledger + resultado). El config pineado del hub NO se toca.
3. **Pre-registro:** RECOMIENDO la opcion **(A) pre-registro PROPIO** (sello fechado con hipotesis de
   transferibilidad + unidades DENTRO + Q1-Q5 y su direccion esperada + criterio de exito), encajable como seccion
   del Sello Etapa 2. Es la evidencia mas fuerte (falsable). La (B) exploratoria-declarada es mas debil. **Es un
   fork de diseno de estudio -> lo decides TU con el Asesor**, no lo sello yo; dejo el cableado listo para ambas.
4. **Prereqs de la 1a unidad medida** (checklist en el doc): B/jheredia:v1 DONE + gate 2-clones nominal + base
   congelada (resuelta) + SPEC-CONT instanciada + instrumentacion F3.3 cableada + pre-registro sellado + Sprint 1
   post-30-jul.

**Decision pendiente tuya + Asesor:** pre-registro propio (A, recomendado) vs exploratoria declarada (B). El resto
(wiring F3.3 concreto + artefacto de metricas + Entrada de cross-atestacion) lo construyo cuando abra el build
(post-30-jul); ninguno abre el build ni toca el estudio congelado. Sin prisa, como dijiste.
