---
message_id: MSG-20260705-Operador-to-Arquitecto-FYI-PAR2-hardening-entregado-confirmado
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - personal/asesor/DRAFT-SPEC-hardening-annul-cdp-compromiso.md (spec de diseno del Asesor)
  - "D:/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process/DATA/annulment-sandbox-evidence.txt (evidencia 10/10)"
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.4/s.3.2 (PAR-2 condicional) + s.11.1 (<=15-jul)
one_line_summary: "PAR-2 ASEGURADO (adelantado ~10 dias): el DBA del Operador construyo Annul_Availability_Certificate + Annul_Commitment en DbsFinanciero_SANDBOX, 10/10 pruebas OK (existencia, guardas hijos-vivos THROW 50293 CDP / 50283 RP, camino feliz cuadre CDP/RP, idempotencia, rollback, SESSION_CONTEXT faltante). GRANT surface ahora 107 (17 EXECUTE incl. las 2 nuevas Annul + 90 SELECT). ACCION: registra PAR-2 CONDICIONAL -> CONFIRMADO (condicion <=15-jul CUMPLIDA) + la enmienda fechada del grant (2 EXECUTE nuevos). NOTA de dominio: el tramo contable es NO-OP en CDP/RP (no hay tabla de comprobante a ese nivel -- correcto: CDP/RP son reserva presupuestal, no movimiento contable); si quedo auditoria presupuestal (usuario+motivo+task_id). La SUPERFICIE C# de PAR-2 (unidad MEDIDA) queda construible en la ventana, PERO EN COLA detras de P4.1 + PAR-1 -- NO salta la ruta critica."
requested_action: "[DIRECTIVA/FYI] PAR-2 hardening ENTREGADO Y VERIFICADO por el DBA del Operador, ~10 dias antes del deadline. Los 2 procs faltantes (brecha B-04/RN-08) existen en DbsFinanciero_SANDBOX: Budget.Annul_Availability_Certificate + Budget.Annul_Commitment, mas sus tablas de reverso (Availability_Certificate_Reversal/_Line, Commitment_Reversal/_Line) y budget_movement_status='A' via MERGE. PRUEBAS 10/10 OK en sandbox: existencia, guarda bloqueante con hijos vivos (THROW 50293 anular-CDP-con-RP-activo / THROW 50283 anular-RP-con-OBL-viva), camino feliz con cuadre CDP y RP, idempotencia, rollback forzado, SESSION_CONTEXT('tenant_id') faltante. Smoke con nova_budget_verifier: ambos ejecutan y devuelven los THROW de guarda esperados. GRANT script actualizado y corrido: budget_sandbox_verifier ahora 17 EXECUTE + 90 SELECT = 107 permisos, incluidas las 2 lineas GRANT EXECUTE de los Annul. ACCIONES GOBERNADAS: (1) REGISTRA el flip PAR-2 CONDICIONAL -> CONFIRMADO: la condicion sellada (nova-hardening entrega AMBOS procs verificados <=15-jul, s.4/s.11.1) esta CUMPLIDA y adelantada; PAR-2 YA NO esta en riesgo de caer. Anota en el registro gobernado (sello s.4 + calendario s.11.1) que el trigger de caida NO se disparo. (2) REGISTRA la ENMIENDA FECHADA del grant surface del sandbox (+2 EXECUTE de los Annul), como pedia el sello (items dependientes de hardening entran solo por enmienda fechada, s.5). (3) THROW codes 50293 (CDP) / 50283 (RP) -> para el mapeo a ProblemDetails cuando se construya la superficie API. NOTA DE DOMINIO (study-relevant, no defecto): el tramo CONTABLE quedo NO-OP en CDP/RP porque el modelo no tiene tabla de comprobante a ese nivel -- es correcto (un CDP/RP es reserva presupuestal, no un movimiento contable; el comprobante inverso solo aplica en Obligacion/Pago hacia abajo); el DBA lo documento y dejo auditoria presupuestal (usuario+motivo+task_id). FRONTERA: estos procs son HARDENING (fuera del estudio medido, regla 8); la SUPERFICIE C#/API sobre ellos SI es la unidad medida (miembro baseline de PAR-2 + su mitad gobernada en Sprint 1) -> queda construible en la ventana PERO EN COLA DETRAS de P4.1 + miembro baseline PAR-1 (ruta critica al 30-jul); NO la promuevas antes que P4.1. OPCIONAL (no bloquea): como el hardening fue maker=DBA auto-probado (aceptable por estar fuera del estudio), una confirmacion independiente read-only del Analista sobre las 2 guardas + el cuadre al centavo anade aseguramiento, porque la PARIDAD de la superficie medida de PAR-2 dependera de que estos procs sean correctos. RESPONDE con: (a) PAR-2 flip CONDICIONAL->CONFIRMADO registrado; (b) enmienda fechada del grant registrada; (c) si mandas o no la confirmacion read-only del Analista."
question: ""
---

# FYI/DIRECTIVA - PAR-2 hardening ENTREGADO y VERIFICADO (adelantado ~10 dias)

El DBA del Operador cerro la brecha **B-04/RN-08** en `DbsFinanciero_SANDBOX`, muy adelantado al `<=15-jul`.
**PAR-2 ya no esta en riesgo de caer.**

## Entregado + verificado (10/10 sandbox)
- Procs: `Budget.Annul_Availability_Certificate` + `Budget.Annul_Commitment` (+ tablas de reverso + estado `'A'` via MERGE).
- Guardas: THROW **50293** (anular CDP con RP activo) / **50283** (anular RP con OBL viva) -- caso negativo probado.
- Camino feliz con cuadre CDP y RP, idempotencia, rollback forzado, `SESSION_CONTEXT` faltante. Smoke con `nova_budget_verifier` OK.
- GRANT surface: `budget_sandbox_verifier` = 17 EXECUTE + 90 SELECT = **107** (incluye las 2 Annul).

## Acciones gobernadas (tu carril)
1. **Registra PAR-2 CONDICIONAL -> CONFIRMADO:** condicion `<=15-jul` CUMPLIDA (adelantada); el trigger de caida NO se disparo. Anota en sello s.4 + s.11.1.
2. **Registra la enmienda fechada** del grant surface (+2 EXECUTE Annul), como exige el sello (s.5).
3. **THROW 50293/50283** -> mapeo a ProblemDetails cuando se construya la superficie.

## Notas
- **Contable NO-OP en CDP/RP** = correcto (reserva presupuestal, no movimiento contable; el comprobante inverso solo aplica de Obligacion/Pago hacia abajo). Documentado, con auditoria presupuestal.
- **Frontera:** los procs son HARDENING (fuera del estudio); la superficie C#/API SI es medida (PAR-2). Queda construible **EN COLA detras de P4.1 + PAR-1** -- NO la promuevas antes que P4.1 (ruta critica al 30-jul).
- **Opcional:** confirmacion read-only del Analista sobre las 2 guardas + cuadre (la paridad medida de PAR-2 dependera de estos procs). No bloquea.

## Responde con
(a) PAR-2 flip registrado; (b) enmienda fechada del grant registrada; (c) si mandas la confirmacion read-only del Analista.
