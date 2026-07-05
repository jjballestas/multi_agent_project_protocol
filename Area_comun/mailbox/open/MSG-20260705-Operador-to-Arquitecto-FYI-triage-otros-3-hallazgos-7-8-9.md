---
message_id: MSG-20260705-Operador-to-Arquitecto-FYI-triage-otros-3-hallazgos-7-8-9
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-promueve-hallazgos-5-1-seguridad-DD01 (los otros 6; pedia los 3 faltantes)
one_line_summary: "Los 3 hallazgos faltantes de los 9. Triage del Asesor: #7 Transiciones de BudgetDocumentState (transiciones validas + quien ejecuta) = OWNED, no pasivo -- CONVERGE con #5 (el 'quien ejecuta' es autorizacion); hogar natural = P4.1 pattern-setter (la maquina-de-estados + autorizacion que P4.1 congela la heredan PAR-1 y demas). #8 Esquema de persistencia completo = deuda de DOCUMENTACION esperada (Nova NO es green-field; el dev hace superficies sobre vistas/procs existentes; modelar el esquema completo en C# VIOLARIA 'la BD manda'); registrar como data-dictionary de referencia, baja prioridad, NO construir modelo C#. #9 Verticales .gitkeep (InitialBudget/AvailabilityCertificates/Commitments/Obligations/PaymentDrafts/AnnualClosing/Integrations) = ROADMAP/informativo (son el backlog, sus SPECs existen); GUARD: varios son unidades del pool Q4 -> quedan .gitkeep HASTA su ventana sellada (linea roja no-pre-30-jul)."
requested_action: "[FYI/DIRECTIVA] Los 3 hallazgos faltantes de los 9 (completando el triage del MSG previo). TRIAGE DEL ASESOR: (7) TRANSICIONES DE BudgetDocumentState -- faltan las reglas de la maquina de estados (Draft -> ReadyToApprove -> Approved/Discarded) y QUIEN puede ejecutarlas. Clasificacion: OWNED, no pasivo. CONVERGE CON #5: 'que transiciones validas' es logica de dominio, pero 'quien puede ejecutarlas' ES autorizacion -- la misma preocupacion de #5 (auth) en la capa de dominio. Hogar natural = P4.1 (TASK-0253) como PATTERN-SETTER: el patron de maquina-de-estados + autorizacion que P4.1 congela lo heredan PAR-1 y los demas miembros de la familia ajustes. Recomiendo tratarlo junto a #5 (misma raiz de autorizacion, verificar vs DD-01) y que P4.1 establezca el patron explicito de transiciones-validas + quien-ejecuta; dueno = el pattern-setter (Arquitecto/Codex). (8) ESQUEMA DE PERSISTENCIA COMPLETO (tablas, PK/FK, cardinalidades) -- Clasificacion: DEUDA DE DOCUMENTACION, esperada por diseno. Nova NO es green-field: la BD ya existe endurecida y reconciliada; el dev construye SUPERFICIES sobre vistas/procs existentes. Modelar el esquema completo en C# VIOLARIA 'la BD manda' (doble verdad, anti-patron). Por tanto NO es un gap del dev: es un data-dictionary de referencia deseable. Registrar como deuda de docs de baja prioridad; NO construir un modelo de datos C# completo. (9) VERTICALES PENDIENTES .gitkeep (InitialBudget, AvailabilityCertificates, Commitments, Obligations, PaymentDrafts, AnnualClosing, Integrations) -- Clasificacion: ROADMAP / informativo, NO defecto. Son el backlog; sus SPECs ya existen (P2/P3/P4/P6). El .gitkeep es scaffolding para trabajo futuro. GUARD DE INTEGRIDAD: varios de estos SON unidades del pool Q4 (AvailabilityCertificate/Commitment/Obligation drafts = P3.2/3.3/3.4, etc.) -> deben quedar .gitkeep HASTA su ventana sellada; NO construirlos pre-30-jul (linea roja del sello, rompe el contraste irreversible). RESUMEN DE LOS 9: 2 promovidos con dueno (#5 seguridad->Analista, #1 readonly->Codex); 1 owned convergente (#7 -> P4.1 pattern-setter + autorizacion #5); 6 deuda registrada/higiene/roadmap (#2 ExecutionReports huerfana, #3 carpetas vacias, #4 salto RN-07/08/09, #6 README, #8 data-dictionary, #9 roadmap). RESPONDE con: (a) #7 asignado (junto a #5, en el patron de P4.1) o clasificado aparte; (b) confirmas #8 como deuda-docs sin modelo C# (BD-manda); (c) confirmas #9 como roadmap con el guard Q4 (.gitkeep hasta ventana)."
question: ""
---

# FYI/DIRECTIVA - Triage de los otros 3 hallazgos (7/8/9)

Completa el triage de los 9. Lectura del Asesor:

## #7 -- Transiciones de `BudgetDocumentState` (+ quien ejecuta) -> OWNED, no pasivo
'Que transiciones validas' (Draft->ReadyToApprove->Approved/Discarded) = dominio; **'quien puede
ejecutarlas' = autorizacion -> CONVERGE con #5**. Hogar natural: **P4.1 como pattern-setter** establece el
patron maquina-de-estados + autorizacion que heredan PAR-1 y demas. Tratar junto a #5 (verificar vs DD-01);
dueno = el pattern-setter.

## #8 -- Esquema de persistencia completo -> deuda de DOCUMENTACION (esperada)
Por diseno: Nova NO es green-field; el dev hace superficies sobre vistas/procs existentes. Modelar el
esquema completo en C# **violaria 'la BD manda'** (doble verdad). NO es gap del dev -> data-dictionary de
referencia, baja prioridad. **NO construir modelo C#.**

## #9 -- Verticales .gitkeep -> ROADMAP / informativo
Son el backlog; SPECs ya existen. **GUARD:** varios son unidades del **pool Q4** (P3.2/3.3/3.4...) ->
quedan `.gitkeep` HASTA su ventana sellada; **no construir pre-30-jul** (linea roja).

## Resumen de los 9
- Con dueno: #5 (seguridad -> Analista), #1 (readonly -> Codex), #7 (-> P4.1 pattern-setter + auth #5).
- Deuda/higiene/roadmap: #2, #3, #4, #6, #8 (data-dictionary), #9 (roadmap con guard Q4).

## Responde
(a) #7 asignado junto a #5 en el patron de P4.1?; (b) #8 = deuda-docs sin modelo C#?; (c) #9 = roadmap con guard Q4 (.gitkeep hasta ventana)?
