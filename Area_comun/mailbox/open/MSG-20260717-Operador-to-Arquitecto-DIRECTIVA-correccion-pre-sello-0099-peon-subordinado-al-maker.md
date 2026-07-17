---
message_id: MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-correccion-pre-sello-0099-peon-subordinado-al-maker
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-FIRMA-decision-0099-politica-roster.md
one_line_summary: "CORRECCION PRE-SELLO de DECISION-0099 (aun draft-pendiente-firma). El operador PRECISA la jerarquia: el peon NO es el maker; es un ejecutor de codigo SUBORDINADO al maker. El MAKER (modelo fuerte) gobierna a los peones, les asigna sub-tareas con especificacion DETALLADA y responde ante el checker. Ajusta la regla 1 (y la 2) a esa jerarquia ANTES de sellar; la firma del operador aplica a la version corregida."
requested_action: "[DIRECTIVA] NO selles el draft actual. Ajusta DECISION-0099 a la jerarquia precisada (abajo) y sella la version CORREGIDA con submit_intent decision. La firma del operador (MSG-FIRMA-0099) aplica a la version corregida, no al texto con 'como maker'."
question: "Confirmas la redaccion corregida (regla 1 = peon subordinado al maker; el maker gobierna+especifica) y sellas esa version?"
---

# DIRECTIVA - Correccion pre-sello de DECISION-0099: el peon es SUBORDINADO al maker

## Precision del operador (2026-07-17)
"Los peones solo hacen codigo, GOBERNADOS POR EL MAKER, quien les asignara las tareas
especificandoles detalladamente lo que deben hacer."

Es una **jerarquia**, no una equivalencia. El draft dice "peon = maker-only / se asigna COMO maker",
lo que confunde al peon con el maker. Corrige asi:

## Redaccion corregida (reemplaza la regla 1; ajusta la 2)
1. **Peon = ejecutor de codigo SUBORDINADO al maker.** El peon (modelo debil, p.ej. local 3B-8B)
   SOLO escribe codigo, bajo la direccion de un maker. NO es un maker autonomo, NO ocupa rol de
   checker, orquestador, ni firmante de ratificacion.
2. **El MAKER (modelo fuerte) gobierna a los peones.** El maker asigna a cada peon sub-tareas de
   codigo con **especificacion DETALLADA y sin ambiguedad** (DoR completo, contrato, acceptance
   verificable, verification_cmd, scope, out_of_scope), y **responde por el resultado ante el
   checker**. Una tarea abierta/subespecificada NO se rutea a un peon: el maker la refina primero.
3. **El checker permanece en modelo fuerte** (sin cambios): revision adversarial nunca degradada a
   modelo debil; maker!=checker por CAPACIDAD ademas de por llave.

## Alcance (sin cambios)
Capa HUB (metodologia), aplica a toda instancia; espejo en el export born-operational (0096). El
trio actual de Nova-Payroll ya cumple. Guardrails intactos (fondo 2E35F26E/1.14.0/N=500, firewall
anti-HARKing, DECISION-0081, PII de nomina fuera del store).

## Firma
La firma del operador (MSG-FIRMA-0099) SE MANTIENE, aplicada a esta version CORREGIDA. Sella la
corregida con submit_intent decision (patron 0091): status -> active, approved_by: operador.

-- Operador (via Asesor). Firma relevada: el operador aprobo la politica en chat; el Asesor solo
   transmite la precision, no firma por el.
