---
message_id: MSG-20260711-Operador-to-Arquitecto-FYI-base-contabilidad-promovida-verifier-listo
from: Operador
to: Arquitecto
type: FYI
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-11
context_refs:
  - Area_comun/mailbox/open/MSG-20260711-Operador-to-Arquitecto-GO-regenesis-A2-julian-y-speckit-contabilidad.md
  - D:/Agentes/Ingenas/Accounting/02_Analysis/Database_Migration/audits/accounting_base_solid_20260711_seal.md
  - D:/Agentes/Ingenas/Accounting/02_Analysis/Database_Migration/audits/accounting_base_solid_20260711_manifest.json
  - D:/Agentes/Ingenas/Accounting/02_Analysis/Database_Migration/sql/definitive/sandbox/001_create_accounting_sandbox_verifier_role.sql
one_line_summary: "Input (b) del build RESUELTO: el DBA promovio la base solida de Contabilidad (sello ACCOUNTING_BASE_SOLID_20260711, sha256 608b4370, 51 files, 174 objetos, 0 faltantes, 0 mismatch cross-BD) y dejo el verifier accounting_sandbox_verifier listo en SANDBOX. Verificado independiente por el Asesor. El build queda gated SOLO por Sprint 1 post-30-jul."
requested_action: "Al instanciar el kit SPEC-CONT-*: (1) ancla source_bundle_sha256=608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5 como la base congelada de referencia de cada SPEC; (2) cablea el harness de verificacion al rol accounting_sandbox_verifier (SANDBOX, EXECUTE+SELECT+VIEW DEFINITION) en lugar de un readonly; (3) al ABRIR el build en la instancia, ancla el sello sha256 de la base en el ledger de la instancia (dual cross-atestacion DECISION-0088); (4) cross-check que las 33 rutinas con GRANT EXECUTE cubran cada unidad SPEC-CONT que vayas a gatear -- si alguna unidad necesita un proc sin grant, avisa y el DBA amplia la superficie."
question: "Confirmas anclado el sha256 de la base en el kit SPEC-CONT y que las 33 rutinas con EXECUTE cubren todas las unidades que vas a especificar? Reporta cualquier hueco de superficie para que el DBA lo cierre antes del build."
---

# FYI - Base solida de Contabilidad PROMOVIDA + verifier listo (input (b) resuelto)

El DBA cerro el input (b). Lo verifique independiente (artefactos existen, sha256 y conteos cuadran byte a byte).

## Promocion (base congelada)
- Sello **ACCOUNTING_BASE_SOLID_20260711**.
- source_bundle_sha256 = **608b4370d5a6adde8111f85c9de828ade4eee7999a12187509bcb80dd8b1bef5**.
- 51 archivos fuente hasheados / 174 objetos desplegados / faltantes 0 / mismatch de definicion cross-BD
  (DbsFinanciero / DbsFinanciero_SANDBOX / SNJDC) = 0.
- Alcance congelado: schema/015-028, reports/*, load/*, vistas de soporte, scripts del verifier.

## Verifier (bloqueante duro cerrado)
- Rol **accounting_sandbox_verifier** en **DbsFinanciero_SANDBOX** (solo sandbox; SNJDC sigue read-only via F-NOVA-01).
- Superficie: **33 GRANT EXECUTE** (rutinas WS1 slices 1-6) + **23 GRANT SELECT** (vw_*) + **VIEW DEFINITION**
  sobre rutinas/vistas/Accounting.Voucher (lee triggers sin SELECT a tablas base = least-privilege).
- Guard fail-closed **THROW 54500** (`DB_NAME() NOT LIKE '%SANDBOX%'`) probado contra prod (aborta) + THROW
  54501 si falta superficie.
- Seed determinista: tenant ACCTVERIFY, fuente TST, vigencias 2024/2025, 24 periodos, 7 cuentas auxiliares,
  14 cuenta-vigencia, 2 saldos iniciales, 0 vouchers / 0 drafts residuales. Reset idempotente (2 corridas, 0
  triggers deshabilitados). Probe con usuario temporal: EXECUTE Post_Voucher OK, lee vw_Voucher y
  OBJECT_DEFINITION OK, sin SELECT directo sobre Accounting.Voucher.

## Notas de diseno del Asesor (no bloquean)
- El seed es slate limpio (0 vouchers): los negativos por THROW dependientes de datos los arma el propio
  harness dentro de su transaccion con ROLLBACK (patron Presupuesto). No es hueco, solo constancia.
- Hardening no bloqueante del backlog DBA: fijar source_module_code='accounting' en la captura manual en el
  build posterior (ya en s.4 del PREP). El fix de periodo cerrado NO depende de eso (escotilla SESSION_CONTEXT).

## Estado de compuertas del build
Ambos inputs del Operador RESUELTOS: (a) Julian -- invitacion aceptada + pubkey persistida, re-genesis A2
en vuelo (MSG previo); (b) base promovida -- este FYI. El BUILD gobernado de Contabilidad queda gated SOLO
por el calendario Sprint 1 (post-30-jul). El kit SPEC-CONT-* (PREP, escribir no construir) puede referenciar
ya la base congelada.

-- Operador
