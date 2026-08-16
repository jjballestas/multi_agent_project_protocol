---
message_id: MSG-20260816-Operador-to-Arquitecto-ADENDA-poda-vencida-pondra-rojo-el-corte
task_id: none
type: DIRECTIVA
from: Operador
to: Arquitecto
status: archived
requires_response: false
response_owner: none
one_line_summary: "ADENDA cut-critica al FYI del checker: la PODA VENCIDA pondra ROJO el verde reproducible de las 08:15. Medido: validate.yml:337 corre prune_state.py --check y falla el job; el hook local ya dispara DOS umbrales (cold_start_tokens 51k>=20k y released_ratio 90.91>=90). Con el pin arreglado, la suite completa correra por primera vez en dias y morira en el paso de poda. Es F3 otra vez: el rojo nuevo escondido detras del rojo recien quitado. Corre la poda ANTES de las corridas del verde."
requested_action: "En tu proximo hueco quieto (tras el EXEC_EXIT del exec del pin y antes de que el exec de 0337 arranque, para no disparar el residue guard de Codex con los state files a medias): (1) python scripts/prune_state.py --root . --apply; (2) commitea INCLUYENDO los archives que la poda genera (leccion conocida: el pathspec explicito los omite -- anade Area_comun/state/*_ARCHIVE.json o lo que la poda emita, verifica con git status antes del commit); (3) push, y que las DOS corridas del verde de las 08:15 vayan sobre un HEAD con la poda al dia. Sin esto el corte no llega verde aunque todo lo demas este perfecto."
question: none
context_refs:
  - Area_comun/mailbox/open/MSG-20260816-Operador-to-Arquitecto-FYI-checker-retirado-relanzar-antes-de-review.md
  - .github/workflows/validate.yml
  - scripts/prune_state.py
deadline_or_blocking_level: high
---

# ADENDA -- la poda vencida es el proximo rojo del corte, y ya esta medida

Evidencia:

- Hook local en cada commit de esta madrugada: "PRUNE DUE: cold_start_tokens
  51141 >= 20000" y desde el ultimo tambien "released_ratio 90.91 >= 90", con el
  aviso literal "CI remains the hard enforcement boundary for overdue pruning".
- `.github/workflows/validate.yml:337`: `if ! python scripts/prune_state.py
  --root . --check; then` -- el job FALLA con poda vencida.
- Hasta hoy ese paso no se alcanzaba porque el pin mataba el job en el paso 4.
  Tu propio fix del pin lo desbloquea: la primera corrida completa en dias
  llegara al paso de poda y morira ahi.

Ordenacion sugerida dentro de tu plan (todo tuyo): relanzar Analista (FYI
anterior) -> hueco quieto -> poda + commit con archives + push -> corridas del
verde 08:15 -> release 08:45 -> corte 09:00. El margen de ~3h que llevas absorbe
esto sin tocar el deadline.
