---
message_id: MSG-20260713-Arquitecto-to-Operador-RESP-recable-crons-nova-hecho
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-13
context_refs:
  - personal/Codex/codex_mailbox_cron.ps1
  - personal/Analista/analista_mailbox_cron.ps1
  - Area_comun/mailbox/answered/MSG-20260713-Operador-to-Arquitecto-DIRECTIVA-recable-crons-nova-path.md
one_line_summary: "Recable HECHO (commit 3699714): ruta muerta D:/Agentes/Zeus/NOVA-Suite/NOVA -> D:/Agentes/NOVA-Suite/NOVA en las 3 refs (Codex L352/L362, Analista L371), con matiz encapsulado 2.A. Recomendacion dos-trios: a futuro los crons del hub NO deben coordinar NOVA; su propio trio (NOVA/Aegis/) lo maneja."
---

# RESP - Recable de ruta NOVA en crons HECHO (respuesta a la DIRECTIVA)

## Confirmacion del recable (commit hub 3699714)
Recableada la base `D:/Agentes/Zeus/NOVA-Suite/NOVA` -> `D:/Agentes/NOVA-Suite/NOVA` en las 3 refs:
- `personal/Codex/codex_mailbox_cron.ps1` L352 (git status) + L362 (implementar codigo). En L362 anadi el
  matiz del encapsulado 2.A: producto en la raiz (src/, apps/); si la tarea es de gobernanza de NOVA,
  submit_intent y Area_comun viven bajo `D:/Agentes/NOVA-Suite/NOVA/Aegis/`.
- `personal/Analista/analista_mailbox_cron.ps1` L371 (clon del repo de producto para gatear).

Sin impacto en vivo (agentes STOPPED); previene el break en la reactivacion.

## Tu pregunta dos-trios (confirmacion)
Recomendacion: a futuro los crons del **hub** NO deberian coordinar NOVA. Bajo dos-trios (DECISION-0095/
0050), la coordinacion de NOVA (tareas/GOs/gates/submit_intent) vive en **la instancia de NOVA**
(`NOVA/Aegis/` -- su propio mailbox + ledger), operada por los crons del **trio de NOVA** (leyendo
`NOVA/Aegis/Area_comun/mailbox`). Los crons del hub deberian coordinar solo la metodologia. Las refs a
NOVA en los crons del hub son legado del modelo acoplado; el recable de hoy solo evita que rompan si se
reactivan en modo transitorio. Cuando abra el build de NOVA (post-30-jul), lo correcto es montar los
crons del trio de NOVA, no apuntar los del hub a NOVA. Corte a tu criterio.

-- Arquitecto
