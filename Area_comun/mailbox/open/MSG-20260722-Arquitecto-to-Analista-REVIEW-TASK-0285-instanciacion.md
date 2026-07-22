---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0285-instanciacion
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0285, la ULTIMA de la cola de higiene, sobre el commit 3b66b6b (entrega 23e4179). El runner de instanciacion completa nacia ROJO por dos causas preexistentes que tu mismo confirmaste ajenas a 0279 (fallan igual en el padre 6197e10): el export no arrastraba ledger_head, y la asercion de coordination-default chocaba con el config runtime-tier. Verificar POR COMPORTAMIENTO, con la disciplina de mutantes de 0283: (1) el runner de instanciacion completa pasa a VERDE sobre una instancia recien exportada; (2) ledger_head se arrastra al export -- el prune_state generado lo encuentra; (3) la asercion de tier distingue la instancia bajo prueba y no da rojo con runtime-tier legitima; (4) NEGATIVO PERMANENTE con mutacion demostrada: quitar ledger_head del export vuelve a poner el runner rojo, y un tier mal declarado tambien. Emitir GO o NO-GO con artifact. Si sale GO, cierra la maquinaria COMPLETA y abrimos el nucleo 0103. SIN PRODUCTO EN ALCANCE."
question: "El runner de instanciacion pasa a verde sobre una instancia recien exportada, y quitar ledger_head del export lo vuelve a poner rojo (el negativo tiene dientes)?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0285-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md
one_line_summary: "Juicio de 0285, ultima de higiene: el runner de instanciacion deja de nacer rojo. Con su GO, la maquinaria queda completa."
---

# REVIEW - TASK-0285, el humo del export deja de nacer rojo

Hora local: 2026-07-22 18:20 (reloj del sistema, sin convertir).

Esta es la que tu mismo destapaste: al juzgar 0279, el maker declaro que el runner de
instanciacion ya estaba rojo por dos causas ajenas, y tu lo confirmaste independiente en el
padre. Lo saque a unidad propia porque un gate de humo que nace rojo no distingue un fallo
real de su propio ruido. Ahora se arregla.

## Que verificar

1. **Verde sobre instancia recien exportada.** El runner completo pasa; ese es el criterio
   central -- que un rojo futuro vuelva a ser senal.
2. **`ledger_head` arrastrado**: el `prune_state` generado lo encuentra.
3. **Asercion de tier**: distingue el tier, no da rojo con runtime-tier legitima.
4. **Negativo con dientes**: quitar `ledger_head` del export vuelve a poner el runner rojo;
   tier mal declarado tambien. Aplica tu escrutinio de mutantes.

## Contexto

Es la ultima de la cola de higiene. Con tu GO, las cinco centrales (0279, 0274, 0283, 0276,
0275) mas esta quedan cerradas, la maquinaria esta completa, y abrimos el nucleo 0103 -- las
ocho unidades que el Operador firmo y que son el objetivo real de la tanda. Gracias por las
horas; cada NO-GO tuyo cerro un hueco que ningun test del maker veia.
