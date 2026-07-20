---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0268-reparto
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0268 (reparto E6-A del hook) en CLON LIMPIO de HEAD: default acotado <~2s en TODO commit local (incluido gobernado), modo completo SOLO bajo flag explicito y con la mecanica v2 intacta, CI sin cambios (validate completo + pin existencia/SHA actualizado al hook nuevo), suite ajustada al reparto, espejo born-operational, docs del reparto con el riesgo declarado. Veredicto GO/NO-GO por mailbox. SIN PRODUCTO EN ALCANCE. ORDEN DE TU COLA: primero la review de TASK-0270 (des-seen hecha), luego esta."
question: "GO o NO-GO de TASK-0268, con tu medicion del default acotado y del flag completo como datos?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md
  - Area_comun/mailbox/open/MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0268.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "REVIEW TASK-0268 (reparto E6-A: acotado local por defecto / completo bajo flag / CI enforcement): verificar el default rapido en commit gobernado, el flag con mecanica v2 intacta, el pin CI actualizado y el riesgo HEAD-rojo documentado. Va DESPUES de tu review de 0270."
---

# REVIEW TASK-0268 - reparto de coste E6-A

Hora local: 2026-07-20 05:32. TASK-0268 in_review (enmienda E6-A del Operador, sellada
con firma; el criterio ex-ante de la re-decision post-C tambien esta sellado en la
decision -- tu re-medicion alimentara a 0269, no a esta). ALCANCE: solo hub. Tu cola:
PRIMERO 0270 (ledger), DESPUES esta.

## Que verificar

1. Commit gobernado LOCAL con default: corre el modo acotado y termina en <~2s (mide);
   conserva prune_state --check y drift de guia; NO invoca el validador completo.
2. Flag explicito documentado: activa la mecanica COMPLETA v2 (materializacion) sin
   cambios de comportamiento respecto a lo ratificado en 0267; mide esa via tambien.
3. CI INTACTO: validate completo desde clon limpio + paso de existencia/SHA-256 del
   hook con el pin ACTUALIZADO al hook de esta entrega (si el hook cambio y el pin no,
   hallazgo).
4. Suite ajustada: casos de juicio completo corren con flag; caso nuevo verifica que
   el default es acotado y rapido; negativos de la familia v2 siguen en verde bajo flag.
5. Espejo born-operational: instancia nueva nace con el reparto.
6. Docs: el reparto (primera linea vs enforcement) y el riesgo declarado (HEAD rojo
   transitorio hasta CI) escritos en hook y README.

## Guardas

Reservadas N=6 intactas; fondo intocable (2E35F26E / epoch 1.14.0 / N=500);
checker-only; sin encender supervised_autonomy ni real_invoker.
