---
message_id: MSG-20260714-Operador-to-Arquitecto-FIRMA-s29-hardening-par2-fuera
from: Operador
to: Arquitecto
type: RESP
status: answered
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (enmienda s.29 DRAFT)
  - Area_comun/mailbox/open/MSG-20260714-Arquitecto-to-Operador-RESP-confirmacion-hardening-par2-servida.md
one_line_summary: "FIRMA del operador: (1) apruebo la enmienda s.29 (checkpoint hardening-15-jul CERRADO EN PLAZO, con la clase de evidencia declarada honesta); (2) decision PAR-2 = FUERA del pool Q4 (entregado, fuera del contraste). n=10 intacto. NO se ordena re-verificacion gobernada ni enmienda de pool ni cableado de Annul_Commitment."
requested_action: "(1) Sella la enmienda s.29 (checkpoint hardening-15-jul cumplido en plazo con la evidencia declarada). (2) Registra PAR-2 = FUERA del pool: entregado, fuera del contraste; n=10 sin cambio; RP/OBL-annul se cablean DESPUES fuera del estudio cuando convenga al producto. NO ordenes re-verificacion gobernada del hardening, NO enmienda de pool, NO cables Annul_Commitment. El numero citable sigue siendo 30 hasta reconciliar la anomalia 36-vs-30 (queda como DECISION-0018 para el Arquitecto de NOVA)."
question: "Confirmas sellado de s.29 + PAR-2 registrado FUERA?"
---

# FIRMA - Enmienda s.29 (hardening 15-jul) + PAR-2 FUERA del pool

FIRMO. Dos decisiones:

## 1. Enmienda s.29 - APROBADA
Apruebo la enmienda s.29 tal como esta redactada: el checkpoint **hardening-15-jul queda CERRADO EN
PLAZO** (procs Budget.Annul_* entregados adelantado el 14-jul), con la **clase de evidencia declarada
honestamente**:
- El guard Assert_Permission sobre los 3 Annul_* tiene verificacion INDEPENDIENTE FIRMADA (TASK-9392).
- La entrega PAR-2 como tal NO alcanza el estandar maker!=checker (a2333dc = solo-docs; TASK-0254 no
  gobernada). Se registra tal cual, sin sobrevender.
- Numero citable = **30** (no 36) hasta reconciliar la inconsistencia; la anomalia queda senalada al
  Arquitecto de NOVA (DECISION-0018).

## 2. PAR-2 = FUERA del pool Q4
Decido **FUERA**. Motivo: n=10 ya esta confirmado SIN PAR-2, no es ruta critica, y no incorporo una
unidad al pool bajo presion de tiempo (semana del sello) con evidencia hoy delgada. Efecto:
- Se registra "entregado, fuera del contraste"; el estudio sigue con **n=10 intacto**.
- **NO** se ordena la re-verificacion gobernada del hardening (patron TASK-9392).
- **NO** enmienda de pool; **NO** se cabla Annul_Commitment ahora (regla 8: el dev nunca crea el proc).
- RP/OBL-annul se pueden cablear DESPUES, fuera del estudio, cuando convenga al producto.

## Frontera
No toca el fondo pineado (hub 2E35F26E / epoch 1.14.0 / dataset N=500). La ruta critica sigue siendo la
reconciliacion 26-29-jul.
