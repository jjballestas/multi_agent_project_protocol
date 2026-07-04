---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-pre-sello
from: Operador
to: Arquitecto
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-arquitecto-sin-idle (cola previa; items 1/2/4 hechos, este REFRESCA)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (reloj duro <=08-jul)
  - NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md s.2.2/s.3 (pool Q4 enumerado + sorteo)
one_line_summary: "REFRESCO de la cola sin-idle (los items de build ya cerraron: GOAL-P1 done+medido+ratificado, skill 0248 done, SPECs P2 entregadas). Ola PRE-SELLO priorizada hacia el 08-jul: (1) COMPLETAR el prep/ensayo del sello (manifiesto de corpus + sha256 de TODOS los artefactos incl. el journal GOAL-P1 d2a13216 + dry-run de la atestacion consolidada + freeze schema v1.0 con los 3 hallazgos del piloto) = CAMINO CRITICO; (2) PREPARAR el resto de la familia de SPECs (P3.1-P3.5, P4.x, y los items del pool Q4) bajo TASK-0246, con las mismas restricciones (adversarial-separado, checker_formal=0, deuda front GOAL-P1, correlation+task_id); (3) ENUMERAR el pool Q4 NOMINALMENTE para el sello (incl. los Get_*_List verificados uno-a-uno contra el conector readonly). Trabaja en orden; el sello 08-jul es el reloj. Recordatorio: estimates S/M/L son del Operador (insumo del sorteo, pendiente)."
requested_action: "[DIRECTIVA] Los items de build ya cerraron (GOAL-P1 done+medido+ratificado sha256 d2a13216; skill codegen-triage 0248 done; SPECs P2-001..004 entregadas y verificadas). REFRESCO de tu cola sin-idle hacia el sello (trabaja EN ORDEN; el 08-jul es el reloj): (1) PRIMARIO / CAMINO CRITICO -- COMPLETA EL PREP/ENSAYO DEL SELLO: finaliza el manifiesto de corpus (lista + sha256 de TODOS los artefactos que se sellan: schema_medicion/defectos + medicion_ledger.py + el journal REAL de GOAL-P1 con su sha256 d2a13216c29b4572ce91a8d3569c3fbbd197be3ff27c372f43a1cf4d719ae2f5 + el SELLO draft + los NOVA_ESTUDIO_*), ensaya (dry-run) el intent CONSOLIDADO de atestacion del sello (el vehiculo `decision` per tu ensayo, GAP-5), y deja PRE-ARMADO el freeze del schema v1.0 con los 3 HALLAZGOS DEL PILOTO horneados (tokens_total_atribuibles como moneda baseline; captura en stderr; adversarial-separado habilita taggear tokens_adversarial_informal). NO selles: pre-arma para que el 08-jul sea un intent atomico limpio. (2) SECUNDARIO -- PREPARA EL RESTO DE LA FAMILIA DE SPECs bajo TASK-0246 (arq+docs, citas contra la BD readonly s9), para que Codex tenga backlog listo en Sprint 1: la familia P3 (P3.1 Initial Budget Draft primera_unidad + P3.2/P3.3/P3.4 Drafts + P3.5 Payment Draft frontera Treasury) y los mutadores P4.x (P4.1 pattern-setter + P4.4), con las MISMAS restricciones que horneaste en P2 (adversarial en SESION SEPARADA/contexto limpio, checker_formal=0 en baseline, deuda del harness de test del front de GOAL-P1 como bloqueante del front, correlation+task_id, no reimplementar reglas SQL en C#). Recordar: el DEV MEDIDO de estas unidades NO abre pre-sello (solo GOAL-P1 abrio); preparar SPECs es arq+docs, no arranque de dev. (3) TERCIARIO -- ENUMERA EL POOL Q4 NOMINALMENTE para el sello (Particion s.2.2): P4.4 Apply_Obligation_Adjustment, P3.2/P3.3/P3.4 (condicionadas a DEC cerrada), P2.3 UI, P6.3 OpenTelemetry, y los Get_*_List de BR-C3/DOC-11 enumerados UNO A UNO verificando que su vista EXISTE contra el conector readonly (fabrica de tareas S). Es contenido del sello. NOTA: los estimates S/M/L de las ~9-10 unidades son del OPERADOR (insumo del sorteo, aun pendientes); no los generes tu. Cualquier bloqueo -> senala por mailbox con una pregunta concreta, no quedes idle."
question: ""
---

# DIRECTIVA - Cola pre-sello (no idle hacia el 08-jul)

Los items de build cerraron (GOAL-P1 done+medido+ratificado; skill 0248 done; SPECs P2 entregadas).
Refresco tu cola sin-idle hacia el sello. Trabaja EN ORDEN; el 08-jul es el reloj.

1. **PRIMARIO / camino critico -- COMPLETA EL PREP DEL SELLO:** manifiesto de corpus (lista + sha256 de
   TODOS los artefactos, incl. el journal GOAL-P1 sha256 `d2a13216...ae2f5`) + dry-run del intent CONSOLIDADO
   de atestacion + freeze schema v1.0 PRE-ARMADO con los 3 hallazgos del piloto. NO selles; pre-arma.
2. **SECUNDARIO -- PREPARA EL RESTO DE SPECs** bajo TASK-0246: familia P3 (P3.1-P3.5) + mutadores P4.x, con
   las MISMAS restricciones que P2 (adversarial en sesion separada, checker_formal=0, deuda front, correlation).
   Dev medido NO abre pre-sello; esto es arq+docs.
3. **TERCIARIO -- ENUMERA EL POOL Q4 NOMINALMENTE** para el sello (P4.4, P3.2/3/4, P2.3, P6.3, Get_*_List
   uno-a-uno verificando vista existente contra el conector readonly).

NOTA: los estimates S/M/L son del OPERADOR (insumo del sorteo, pendientes); no los generes. Bloqueo -> mailbox, no idle.
