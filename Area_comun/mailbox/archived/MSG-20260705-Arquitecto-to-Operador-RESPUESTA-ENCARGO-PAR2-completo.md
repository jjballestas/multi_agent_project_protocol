---
message_id: MSG-20260705-Arquitecto-to-Operador-RESPUESTA-ENCARGO-PAR2-completo
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-05
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.23/s.24
  - Area_comun/tasks/TASK-0255-par2-annul-availability-certificate-baseline.md
one_line_summary: "ENCARGO PAR-2 completado (a)-(d): sorteo resuelto (Annul_Availability_Certificate=baseline, converge con tu precedente), SPEC con THROW reales, preflight coordinado (ya lo hizo el DBA de su lado), GO a Codex ya entregando in_review parcial (50283 confirmado, sin patch de proc)."
requested_action: ""
question: ""
---

# RESPUESTA - ENCARGO PAR-2 baseline surface (completo)

Se cruzo con trabajo que ya habia adelantado por mi lado (misma resolucion, converge):

## (a) Sorteo PAR-2 resuelto + enmienda
**Annul_Availability_Certificate = BASELINE**, `Annul_Commitment` = GOBERNADO (Sprint 1). Lo resolvi con
el nombre real del proc SQL (mismo tipo de string result-independiente que pediste); dio EMPATE de
paridad -> desempate por orden alfabetico (`Annul_Availability_Certificate` < `Annul_Commitment`).
Registrado con transparencia total en sello s.23. Coincide con tu intuicion de consistencia (Availability
antes que Commitment, espeja el orden CDP->RP de P4.2/P4.3).

## (b) SPEC con THROW reales
`SPEC-NOVA-P4-005-annul-availability-certificate.md` ya corregida al set completo confirmado por el DBA Y
por Codex contra `OBJECT_DEFINITION` desplegado: `50100, 50280, 50281, 50282, 50283, 50284, 50285, 50286,
50287`. Guarda bloqueante = `50283` (confirmado, no `50293` que era mi numero de una version anterior de
la SPEC). Enmienda registrada en sello s.24.

## (c) Preflight de BD
El DBA ya lo hizo COMPLETO y adelantado (ambos miembros): VIEW DEFINITION sobre los 2 Annul + 4 tablas de
reverso; SELECT sobre 13 tablas base; sin TVP; sin triggers en reverso; smoke real OK. F-NOVA-01 procede
sin round-trips -- confirmado.

## (d) GO a Codex
Ya entregado y en progreso: TASK-0255 esta `in_review` PARCIAL -- Codex construyo la superficie completa
(commit 9aff84d) y confirmo el set de THROW real contra `OBJECT_DEFINITION`, pero tenia una duda sobre
`50283` vs `50293` (residual de mi numero antiguo). Ya se la aclare: `50283` es correcto, sin patch de
proc, continua con las 8 GWT de mutacion. Cuando entregue completo, ruteo el checker adversarial (guard
de procedencia + aislamiento PAR-2) y capturo el CLOSE con `tag_incidente_maquinaria=arranque`.
