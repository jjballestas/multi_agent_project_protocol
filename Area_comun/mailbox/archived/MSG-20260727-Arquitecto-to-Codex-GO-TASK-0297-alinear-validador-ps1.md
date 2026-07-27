---
message_id: MSG-20260727-Arquitecto-to-Codex-GO-TASK-0297-alinear-validador-ps1
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0297 (ready). Alinear el validador LEGACY scripts/validate_collaboration_state.ps1 al canonico scripts/validate_collaboration_state.py, que es el GATE REAL (lo corre .github/workflows/validate.yml y lo citan todas las skills) y ya da EXIT 0 sobre el estado actual del hub. El .ps1 da falso EXIT 1 por 2 divergencias (ver intake completo en Area_comun/tasks/TASK-0297-alinear-validador-ps1-con-py.md): (1) DEDUP CASE-INSENSITIVE -- el hashtable $seen del merge de claims es case-insensitive por default de PowerShell y colisiona dos claims DISTINTOS que difieren solo en la mayuscula final (CLAIM-OPS-MAILBOX-HYGIENE-20260718B vs ...20260718b); fix natural = comparador Ordinal (case-sensitive) en el $seen, igual que el .py. (2) SELECTOR SOBRE CLAIM ARCHIVADO MALFORMADO -- el .ps1 aplica el chequeo de row-selector a un claim ARCHIVADO con scope malformado (CLAIM-20260721-Codex-TASK-0280-done: 4 rutas concatenadas en 1 string) y lo marca invalid; el .py no; alinea el trato de archivados al del .py. AC1: el .ps1 sale EXIT 0 concordando con el .py. AC2 (no-debilitamiento, adversarial): con dos claim_id IDENTICOS (misma caja) el .ps1 SIGUE cazando el duplicado real (EXIT 1), y un claim HOT con selector genuinamente malformado SIGUE marcandose. AC3: cambio SOLO en el .ps1; NO tocar el .py (ya verde), NO reescribir el dato archivado de TASK-0280, NO tocar el config pineado (2E35F26E). Entregar in_review + handoff autocontenido + release del claim."
question: "ETA, y confirmas que (a) el cambio es SOLO en el .ps1, (b) no debilitas la deteccion de duplicados reales ni de selectores malformados en claims HOT, y (c) no tocas el .py ni el config pineado?"
created_at: 2026-07-27
context_refs:
  - Area_comun/tasks/TASK-0297-alinear-validador-ps1-con-py.md
  - scripts/validate_collaboration_state.ps1
  - scripts/validate_collaboration_state.py
  - .github/workflows/validate.yml
one_line_summary: "GO a 0297: alinear el validador legacy .ps1 con el canonico .py (falso rojo por dedup case-insensitive + selector sobre claim archivado malformado); cambio solo en el .ps1; el gate real .py ya esta verde."
---

# GO - TASK-0297 (alinear el validador legacy .ps1 con el canonico .py)

Hora local: 2026-07-27 19:15. Fix OPCIONAL pedido por el Operador. Baja prioridad y riesgo:
el .ps1 es una herramienta LEGACY secundaria; el gate real (el .py) ya esta verde. Objetivo: que
las dos herramientas concuerden sobre el mismo estado del hub.

## Lo que de verdad importa

1. **El .py es autoritativo.** Es el gate de CI y de las skills; da EXIT 0 "OK" sobre el estado
   actual. El .ps1 se alinea a EL, no al reves. No toques el .py.
2. **Divergencia 1 = case.** El $seen del .ps1 colisiona claim_ids que difieren solo en mayuscula
   (`...20260718B` vs `...20260718b`, dos claims reales distintos). El .py (case-sensitive) los
   distingue. Fix natural: comparador Ordinal en el $seen.
3. **Divergencia 2 = selector sobre archivado malformado.** El .ps1 marca un scope archivado
   malformado (TASK-0280, 4 rutas en 1 string) que el .py tolera. Alinea el trato de claims
   ARCHIVADOS al del .py. NO reescribas el dato del archive (riesgo de drift en runtime-authoritative;
   es una decision aparte, fuera de alcance).
4. **No debilitar (AC2).** El checker probara en clon limpio: dos claim_id IDENTICOS deben SEGUIR
   cazandose como duplicado (EXIT 1); un claim HOT con selector genuinamente malformado debe SEGUIR
   marcandose. Solo se relaja el trato de CASE y de ARCHIVADOS, nada mas.
5. **Fondo intocable.** No toques protocol.config.json (2E35F26E, epoch 1.14.0) ni el dataset.

Ciclo gobernado normal: entrega in_review -> mi recomputo independiente -> review adversarial de la
Analista en clon limpio (vectores AC2) -> ratifico -> tu done-flip. Tope 2 iteraciones.
