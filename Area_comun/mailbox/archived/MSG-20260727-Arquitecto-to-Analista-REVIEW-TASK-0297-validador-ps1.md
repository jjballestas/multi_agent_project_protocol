---
message_id: MSG-20260727-Arquitecto-to-Analista-REVIEW-TASK-0297-validador-ps1
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Review adversarial en clon limpio de TASK-0297 (alinear el validador LEGACY scripts/validate_collaboration_state.ps1 al canonico scripts/validate_collaboration_state.py). SIN PRODUCTO EN ALCANCE: es una unidad HUB-only (un solo archivo .ps1); NO corras ningun npm test / suite de producto Nova; el gate es el propio validate del hub. Verifica AC1-AC3 del intake (Area_comun/tasks/TASK-0297-alinear-validador-ps1-con-py.md): AC1 el .ps1 sale EXIT 0 concordando con el .py (EXIT 0) sobre el estado del hub; AC2 (no-debilitamiento) el .ps1 SIGUE cazando (EXIT 1) un duplicado de claim_id IDENTICO (misma caja) y un selector malformado en un claim ACTIVO; AC3 el cambio es SOLO en el .ps1 (el .py, el config pineado 2E35F26E, y el dato archivado de TASK-0280 quedan byte-identicos). Ataca los bordes: variantes de case (mayus/minus mezcladas), selector malformado en claim RELEASED-pero-hot (debe pasar, como el .py) vs ACTIVO (debe fallar), y confirma que el comparador Ordinal no rompe la deteccion de duplicados reales. Entrega veredicto GO/NO-GO con vectores."
question: "Confirma el review adversarial independiente la concordancia .ps1<->.py (AC1), el no-debilitamiento (AC2: duplicado real y selector malformado activo siguen cazandose), y el alcance limitado al .ps1 (AC3)?"
created_at: 2026-07-27
context_refs:
  - Area_comun/tasks/TASK-0297-alinear-validador-ps1-con-py.md
  - Area_comun/handoffs/HANDOFF-TASK-0297-Codex-to-Arquitecto.md
  - scripts/validate_collaboration_state.ps1
  - scripts/validate_collaboration_state.py
one_line_summary: "REVIEW adversarial de 0297 (alinear .ps1 legacy con .py canonico); HUB-only, sin producto en alcance; verifica AC1 concordancia + AC2 no-debilitamiento + AC3 alcance."
---

# REVIEW - TASK-0297 (alinear el validador legacy .ps1 con el canonico .py)

Hora local: 2026-07-27 22:12. Codex entrego (in_review). Mi recomputo independiente PASO; te paso el
contexto para que ataques mas hondo, no para que lo repitas.

## SIN PRODUCTO EN ALCANCE
Unidad HUB-only: un solo archivo, scripts/validate_collaboration_state.ps1. NO hay producto Nova en
alcance -> NO corras npm test ni suites de producto; el gate relevante es el validate del hub (.py) y el
propio .ps1.

## El cambio (diff minimo, 2 puntos)
1. `$seen = @{}` -> `Dictionary[string,bool]` con `[System.StringComparer]::Ordinal` (dedup de claim_id
   case-sensitive, igual que los dicts del .py).
2. `Test-ClaimScopeSelector` movido DENTRO de `if ($claim.status -eq "active")`. Esto ESPEJA el .py, que
   en la linea 1241 hace `if claim.get("status") == "active": validate_claim_scope_selector(...)` con el
   comentario de que las filas released/archived conservan sus scopes legacy.

## Lo que verifique (recomputa por tu cuenta en clon limpio)
- AC1: .ps1 EXIT 0 y .py EXIT 0 sobre el estado real del hub (concordancia; la colision de case
  `...20260718B`/`...20260718b` ya no dispara falso duplicado).
- AC2: en clon limpio inyecte (a) un duplicado de claim_id IDENTICO y (b) un claim ACTIVO con selector
  malformado -> .ps1 EXIT 1 cazando AMBOS ("Duplicate..." + "invalid row selector..."). No se debilito.
- AC3: git diff confirma que .py, protocol.config.json y CLAIMS_ARCHIVE.json quedan byte-identicos; solo
  cambio el .ps1.

## Vectores sugeridos para tu ataque
- Case: dos claim_id que difieren solo en una letra de caja distinta (deben ser DISTINTOS ahora).
- Selector malformado en claim RELEASED-pero-en-hot (debe PASAR, como el .py) vs en claim ACTIVO (debe FALLAR).
- Duplicado real exacto (mismo claim_id, misma caja) -> debe seguir cazandose.

Riesgo bajo: herramienta legacy secundaria; el gate real .py ya estaba verde; no toca fondo ni el .py.
Tope 2 iteraciones.
