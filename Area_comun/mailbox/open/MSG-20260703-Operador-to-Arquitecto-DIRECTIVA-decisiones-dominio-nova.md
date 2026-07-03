---
message_id: MSG-20260703-Operador-to-Arquitecto-DIRECTIVA-decisiones-dominio-nova
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md (tracker, DD-01/02/03 RESUELTAS)
  - Area_comun/specs/nova/SPEC-NOVA-P3-001..005
one_line_summary: "El Operador resolvio las 3 decisiones de dominio del tracker (DD-01 autorizacion / DD-02 objeto min 20 / DD-03 SECOP 'N/A'); hornealas en las SPECs cuando convenga (sin prisa; cabe con la remediacion THROW o en la ventana muerta)."
requested_action: "[DIRECTIVA] Resolucion del Operador de las 3 decisiones de dominio (tracker personal/operador/vision-nova/DECISIONES-DOMINIO-PENDIENTES-nova.md). Hornealas en las SPECs gobernadas; no urge (cabe junto a la remediacion THROW en curso o en la ventana muerta hasta 17-jul). (1) DD-01 AUTORIZACION -- aplica a las 5 SPECs de aprobacion P3-001..005 (el supuesto recurre en P3-004/005, no solo 001/002/003): ACEPTADO el supuesto temporal (usuario autenticado con rol presupuesto captura/aprueba/emite) para Sprint 1; BR-C4 (policy por operacion) CONFIRMADA post-Sprint-1. Cambia el texto de 'SUPUESTO TEMPORAL declarado' a 'CONFIRMADO por el Operador: aceptado para Sprint 1; policy por operacion via BR-C4 post-Sprint-1'. (2) DD-02 OBJETO DEL RP (P3-003): SE NORMA el minimo en 20 caracteres (cambia el legacy de 15). Reemplaza 'objeto (min. 15 chars -- decidir si norma, B-04)' por 'objeto (min. 20 chars, norma del Operador)' en el alcance p.3 y la restriccion 6d; ajusta la validacion de aplicacion (400 ProblemDetails si <20). (3) DD-03 REFERENCIA SECOP VACIA (P3-003): default documentado = marca 'N/A' declarada; jamas el centinela '0' legacy. Reemplaza 'valor por defecto documentado (no el 0 magico legacy)' por \"default 'N/A' declarada (decision del Operador); jamas el '0' legacy\". NOTA DE GATE: DD-02 toca un criterio de aceptacion falsable (min 20 chars); no requiere re-gate por si sola, pero si editas los criterios, que la version resultante viaje en el proximo gate del lote (o el re-audit THROW en curso) para dejar el cambio atestado."
question: ""
---

# DIRECTIVA - Resolucion de las 3 decisiones de dominio NOVA (DD-01/02/03)

El Operador resolvio las 3 decisiones de dominio del tracker. Hornealas en las SPECs cuando convenga
(sin prisa; caben con la remediacion THROW o en la ventana muerta hasta 17-jul):

- **DD-01 (autorizacion, las 5 SPECs P3-001..005):** ACEPTADO el supuesto temporal para Sprint 1;
  BR-C4 (policy por operacion) CONFIRMADA post-Sprint-1. El supuesto pasa de 'declarado' a
  'confirmado por el Operador'.
- **DD-02 (P3-003, objeto del RP):** SE NORMA el minimo en **20 caracteres** (cambia el legacy de 15).
  Ajusta el alcance p.3, la restriccion 6d y la validacion de aplicacion.
- **DD-03 (P3-003, SECOP vacio):** default = marca **'N/A' declarada**; jamas el '0' legacy.

Detalle vinculante en requested_action. DD-02 toca un criterio falsable: que el cambio viaje en el
proximo gate del lote para quedar atestado.
