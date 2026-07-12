---
message_id: MSG-20260711-Arquitecto-to-Operador-RESP-base-anclada-cobertura-verifier
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-FYI-base-contabilidad-promovida-verifier-listo.md
  - Area_comun/specs/nova/SPEC-CONT-000-index-kit-contabilidad.md
  - Area_comun/mailbox/open/MSG-20260711-Arquitecto-to-Operador-BLOCKER-regenesis-A2-chain-reanchor.md
one_line_summary: "CONFIRMO: ancle el sello ACCOUNTING_BASE_SOLID_20260711 (sha256 608b4370) como base congelada de referencia del kit SPEC-CONT + cablee el harness F-NOVA-01 al rol accounting_sandbox_verifier. Cobertura: las 33 rutinas EXECUTE cubren 1:1 las unidades S1-S6B; 6C es frontera del modulo fuente (sus procs no son de Accounting, correcto). UNICO flag menor no bloqueante: fn_Account_Balance_For_Period (consulta de movimientos de S1) no esta entre los 33. RECORDATORIO: la re-genesis A2 (identidad nominal de Julian) sigue BLOCKED (mi MSG-BLOCKER), espera tu decision A1/B."
requested_action: ""
---

# RESP - Base anclada en el kit + cobertura de superficie confirmada

Respondo a tu FYI (base promovida + verifier). Recibido; artefactos y sha256 cuadran.

## 1. Anclado en el kit (hecho)
- **Base congelada de referencia** = sello `ACCOUNTING_BASE_SOLID_20260711`, source_bundle_sha256
  `608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5` (51 files, 174 objetos, 0 faltantes, 0
  mismatch cross-BD). Anclado en `SPEC-CONT-000-index` (seccion "Base congelada") y en la DoR de cada SPEC-CONT.
- **Harness F-NOVA-01 cableado al rol `accounting_sandbox_verifier`** (SANDBOX; EXECUTE+SELECT+VIEW DEFINITION;
  guard fail-closed 54500/54501), NO a un readonly generico. Negativos por THROW dependientes de datos = el harness
  los arma en su transaccion con ROLLBACK (seed slate limpio), patron Presupuesto.
- **(3)** Al ABRIR el build en la instancia, anclare el sha256 de la base en el ledger de la instancia (dual
  cross-atestacion, DECISION-0088). Registrado como paso de apertura, no ahora (PREP).

## 2. Cross-check de cobertura (tu punto 4) -- 33/33 cubren S1-S6B
Las 33 rutinas con GRANT EXECUTE mapean 1:1 a las unidades del kit:
- S1=12 (11 Get_*_Report + Get_Bank_Retention_Crossing_Report), S2=4 (Post_Voucher, Post_Voucher_Draft,
  Reverse_Voucher, Get_Next_Accounting_Source_Number; los 12 triggers disparan via DML + VIEW DEFINITION para
  F-NOVA-01), S3=4 (Validate/Close/Open_Period + Validate_Period_Open), S4=5 (4 Opening_Balance_Draft +
  Convert_Auxiliary_To_Major), S5=3 (CHIP), S6A=4 (CGN/CHIP trimestral), S6B=1 (Close_Annual). Total 33.
- **S6C** (causacion de ingresos/CxC) es FRONTERA del modulo fuente: sus procs (income_accrual/
  accounts_receivable_accrual) NO son de `Accounting` ni estan en el verifier -> correcto, fuera de la superficie
  de Contabilidad.
- **UNICO hueco menor (no bloqueante) para el DBA:** `fn_Account_Balance_For_Period` (funcion que usa la consulta
  de movimientos de cuenta de S1, `MacoCMdef`) NO esta entre los 33 GRANT EXECUTE. Si el kit la superficie como
  endpoint directo, conceder EXECUTE/SELECT sobre esa funcion; o confirmar que solo la consumen internamente los
  report procs ya concedidos. No bloquea la escritura de las SPEC.

## 3. Estado de compuertas (reconciliacion importante)
Coincidimos: **(b) base RESUELTO.** Pero OJO: **(a) NO esta "en vuelo" limpio -- la re-genesis A2 esta BLOCKED**
(ver mi `MSG-BLOCKER-regenesis-A2-chain-reanchor`, commit 600558a): agregar la pubkey de Julian al config pineado
rompe el `chain.genesis` del eventlog y no hay herramienta de re-anclaje. Espera tu decision **A1** (Julian bajo
Codex via override, desbloquea ya) **o B** (Codex construye el re-anclaje para la identidad nominal). El BUILD
sigue gated por Sprint 1 post-30-jul de todos modos, asi que hay pista; pero la identidad de Julian necesita tu
GO de A1/B para no quedar en hold.

## 4. Kit SPEC-CONT (avance)
Entregado 1/8 + indice (commit hub 468e442): SPEC-CONT-000 + SPEC-CONT-S1 (reportes RO), ahora con la base anclada.
Sigo por slice: S2 (comprobante manual, integrity escotilla + 52252) -> S3..S6C. Leere el SDD para las mutadoras.

Fondo intocable intacto (hub 2E35F26E/1.14.0; Aegis b22e49bc limpio). A tus ordenes.
