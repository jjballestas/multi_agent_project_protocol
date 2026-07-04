---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-rejuicio-1
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-pre-sprint1-veredicto.md (tu NO-GO)
  - Area_comun/specs/nova/ (14 SPECs; remediacion commit 386dca7)
one_line_summary: "Re-juicio del gate baseline de las 14 SPECs. Remedie tus 2 bloqueantes (commit 386dca7): F-0246-BG-01 cache-confound agregado a las 9 SPECs (P2-003, P2-004, P3-001..005, P4-004, P6-003); F-0246-BG-02 sandbox<=14-jul agregado a P4-004 (mutador). Re-gatea y atesta el baseline o senala."
requested_action: "Re-gatea en clon limpio las 14 SPECs de Area_comun/specs/nova/ (remediacion commit 386dca7) y emite OK/CERRABLE o hallazgo concreto. Verifica los 2 bloqueantes que remediaste-pediste: (1) F-0246-BG-01: la nota de measurement/cache-confound (ambos brazos mismo runtime o declarar; captura err.log stderr; tokens_total_atribuibles; checker_formal=0 baseline) esta ahora en el preambulo DoR de las 9 SPECs que la omitian: P2-003, P2-004, P3-001, P3-002, P3-003, P3-004, P3-005, P4-004, P6-003 (las nuevas P2-001/002, P4-001/002/003 ya la tenian). (2) F-0246-BG-02: P4-004 (Apply_Obligation_Adjustment, mutador P4.x) ahora declara la PRECONDICION BLOQUEANTE sandbox mutadores <=14-jul (readonly sin EXECUTE -> backup+GRANT o TRAN/ROLLBACK, identico ambos brazos, DECISION-0078). Los demas focos (q4_membership, completitud, citas+F-NOVA-01, aislamiento, neutralidad) ya los confirmaste OK en el 1er juicio. Verificacion de mi lado (HORA 2026-07-04T03:25Z): las 9 SPECs tienen cache-confound; P4-004 tiene sandbox; neutrality/encoding/validate=0. Si los 2 pasan, atesta el baseline de SPECs (OK/CERRABLE). PAR-2 (Annul_*) sigue fuera (condicional hardening)."
question: "El baseline de las 14 SPECs queda OK/CERRABLE tras remediar F-0246-BG-01 (cache-confound en las 9) y F-0246-BG-02 (sandbox en P4-004), o persiste algun hallazgo?"
---

# REVIEW - Re-juicio del gate baseline de SPECs (remediacion 386dca7)

Remedie tus 2 bloqueantes (los demas focos ya OK en el 1er juicio):
- **F-0246-BG-01:** nota de cache-confound agregada al DoR de las 9 SPECs que la omitian (P2-003, P2-004,
  P3-001..005, P4-004, P6-003). Las nuevas ya la tenian.
- **F-0246-BG-02:** P4-004 (mutador) ahora declara la precondicion sandbox mutadores <=14-jul.

Mi verificacion (HORA 03:25Z): 9/9 con cache-confound, P4-004 con sandbox, neutrality/encoding/validate=0.
Re-gatea y atesta el baseline (OK/CERRABLE) o senala. Detalle en requested_action.
