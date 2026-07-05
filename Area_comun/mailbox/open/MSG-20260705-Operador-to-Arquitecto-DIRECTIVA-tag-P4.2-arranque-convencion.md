---
message_id: MSG-20260705-Operador-to-Arquitecto-DIRECTIVA-tag-P4.2-arranque-convencion
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-05
context_refs:
  - MSG-20260705-Arquitecto-to-Operador-RESUMEN-ausente-3h-piso-minimo-cumplido (pediste confirmar el tag de P4.2)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.10 (regimen cuenta desde 30-jul; pre-30-jul aparte)
one_line_summary: "El Operador CONFIRMA: P4.2 (TASK-0254) tag_incidente_maquinaria = ARRANQUE, no regimen. Corrige la fila CLOSE seq 11. Razon: el tag es de FASE, no de calidad -- el sello s.10 reserva 'regimen' para el estado estable post-30-jul; P4.2 es pre-30-jul -> arranque, consistente con P4.1. Su corrida limpia (431k tokens, 0 reworks, 1 bloqueo) ya queda capturada en los TOKENS BAJOS, no en el tag. CONVENCION establecida para todas las unidades futuras: TODA unidad de la ventana baseline (pre-30-jul) = arranque; regimen SOLO desde 30-jul. Aplica a PAR-2 y siguientes. Resto del RESUMEN OK; piso minimo del 30-jul CUMPLIDO confirmado."
requested_action: "[DIRECTIVA] El Operador CONFIRMA tu pregunta del tag: P4.2 (TASK-0254) lleva tag_incidente_maquinaria = ARRANQUE, NO regimen. CORRIGE la fila CLOSE (seq 11) del journal de medicion. RAZON (para el registro): el tag_incidente_maquinaria es de FASE, no de calidad de corrida. El sello s.10 dice 'regimen cuenta desde 30-jul; instrumentacion pre-30-jul aparte' -> 'regimen' esta reservado para el estado estable post-30-jul. P4.2 se construyo pre-30-jul (ventana baseline) -> es arranque, igual que P4.1. Que corriera LIMPIO (431k tokens, 0 reworks, 1 solo bloqueo de permiso, GO adversarial en 1a pasada) NO lo hace 'regimen': esa limpieza ya queda reflejada honestamente en los TOKENS BAJOS y en notas_confound, no en el tag. Tagearlo regimen borraria la frontera arranque/regimen de la que depende Q1 (costo marginal regimen vs arranque separados). CONVENCION ESTABLECIDA (para no volver a preguntar): TODA unidad de la ventana baseline pre-30-jul = tag_incidente_maquinaria=arranque; regimen SOLO para unidades post-30-jul (Sprint 1 gobernado + Q4). Aplica a PAR-2 baseline surface y a cualquier unidad que cierre antes del 30-jul. NOTA util: el contraste arranque-caro (P4.1: 2M, 4 bloqueos, mock) vs arranque-limpio (P4.2: 431k, 1 bloqueo, sin mock) DENTRO del tag arranque es dato valioso -- muestra la maquinaria estabilizandose; se lee de los tokens, no del tag. RESTO DEL RESUMEN: OK y verificado. PISO MINIMO DEL 30-JUL (P1 + miembro baseline PAR-1) = CUMPLIDO, confirmado. SIGUIENTE en la cola: PAR-2 baseline surface (Annul_* con el pre-flight de BD ampliado -- recuerda SELECT sobre tablas base ademas de vistas, leccion P4.2/Budget_Adjustment). No requiere respuesta; solo corrige la fila y sigue."
question: ""
---

# DIRECTIVA - Tag P4.2 = arranque (confirmado) + convencion

El Operador **CONFIRMA**: P4.2 (`TASK-0254`) lleva `tag_incidente_maquinaria = arranque`, NO regimen.
**Corrige la fila CLOSE (seq 11).**

## Razon (para el registro)
El tag es de **FASE, no de calidad**. Sello s.10: `regimen` cuenta desde 30-jul; pre-30-jul aparte. P4.2 es
**pre-30-jul** -> arranque, igual que P4.1. Su corrida limpia (431k, 0 reworks, 1 bloqueo, GO en 1a pasada)
ya queda en los **tokens bajos** + notas_confound, no en el tag. Regimen borraria la frontera de Q1.

## Convencion establecida (para no repreguntar)
**TODA unidad de la ventana baseline pre-30-jul = `arranque`.** `regimen` SOLO para post-30-jul (Sprint 1 +
Q4). Aplica a PAR-2 y siguientes. El contraste P4.1-caro vs P4.2-limpio DENTRO de arranque es dato valioso
(maquinaria estabilizandose) -- se lee de los tokens, no del tag.

## Resto
RESUMEN OK y verificado. **Piso minimo del 30-jul CUMPLIDO**, confirmado. Siguiente: **PAR-2 baseline
surface** (Annul_*; recuerda el pre-flight ampliado -- SELECT sobre tablas base, no solo vistas). Solo
corrige la fila y sigue.
