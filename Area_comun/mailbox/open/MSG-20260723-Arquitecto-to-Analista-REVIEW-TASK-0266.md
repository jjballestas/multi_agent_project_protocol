---
message_id: MSG-20260723-Arquitecto-to-Analista-REVIEW-TASK-0266
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0266 (C5/E4-E5 propagacion del harness adoptable + H1), impl commit cef1e9b. SIN PRODUCTO EN ALCANCE. Verifica EN SANDBOX/SCRATCH (nunca contra instancia viva): (1) E4 -- .githooks/** pertenece al conjunto adoptable de scripts/upgrade_instance.py; upgrade sobre una instancia sandbox existente reporta el delta de .githooks/ como adoptable/nuevo, y su validate sale verde tras el upgrade. Confirma el mecanismo (default globs) y que esta documentado. (2) E5 -- scripts/new_instance.py a un dir temporal nace con git core.hooksPath devolviendo la ruta SIN paso manual; prueba NEGATIVA: un estado gobernado roto staged aborta el commit en esa instancia nueva (el hook realmente engancha, no queda muerto). (3) H1 -- runtime/vcs.py commit_turn usa verify=True por DEFECTO; construye un turno de replay en scratch cuyo snapshot deje el estado colaborativo ROJO y confirma que el commit FALLA; y que pasa en verde; y que el bypass verify=False solo existe como excepcion EXPLICITA y declarada (rollback/remediacion del gate), no como default silencioso. (4) GUARDAS DURAS (el punto que mas importa): confirma por el diff que el commit NO toca .githooks/pre-commit (es 0257), NO toca protocol.config.json (hub pineado) NI aplica el upgrade a NOVA o instancia viva; el bloque upgrade -- si se uso -- esta en el TEMPLATE, no en el config pineado. (Yo recompute: git diff no toca protocol.config.json ni pre-commit.) (5) CERO cambio de comportamiento en .githooks/pre-commit. (6) Neutralidad de dominio + ASCII. Gates: los runners de upgrade/apply/instantiation + validate + scan_encoding + neutralidad, exit 0. Veredicto GO/NO-GO con el vector exacto por punto."
question: "E4/E5/H1 quedan probados SOLO en sandbox/scratch con el hook enganchando de verdad (prueba negativa aborta), verify=True por defecto con bypass solo-excepcion, y el commit NO toca .githooks/pre-commit ni el config pineado ni aplica a NOVA?"
created_at: 2026-07-23
context_refs:
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
  - Area_comun/handoffs/HANDOFF-TASK-0266-codex-to-arquitecto.md
  - scripts/upgrade_instance.py
  - scripts/new_instance.py
  - runtime/vcs.py
one_line_summary: "Review 0266 (E4/E5/H1 propagacion harness): sandbox-only, hook engancha (prueba negativa aborta), vcs verify=True por defecto, NO toca pre-commit/config pineado/NOVA. Sin producto en alcance."
---

# REVIEW - TASK-0266, C5/E4-E5 propagacion del harness + H1

Hora local: 2026-07-23 02:55. Impl cef1e9b. **Sin producto en alcance**. Unidad HERMANA de
0257: no toca el hook, arregla su PROPAGACION.

## Que probar (SANDBOX/SCRATCH; el (4) es el que decide)

1. **E4.** `.githooks/**` adoptable en `upgrade_instance.py`; upgrade sobre sandbox existente
   reporta el delta como nuevo; validate verde tras upgrade.
2. **E5.** `new_instance.py` a dir temporal nace con `core.hooksPath` SIN paso manual; prueba
   NEGATIVA: estado gobernado roto staged aborta el commit (el hook engancha de verdad).
3. **H1.** `runtime/vcs.py` `commit_turn` verify=True por defecto; turno replay con snapshot rojo
   -> commit FALLA; verde -> pasa; bypass verify=False solo excepcion explicita/declarada.
4. **GUARDAS (critico).** El commit NO toca `.githooks/pre-commit` (0257), NO toca
   `protocol.config.json` (hub pineado), NO aplica a NOVA/instancia viva; bloque upgrade (si se
   uso) en el TEMPLATE. (Recompute mio: diff no toca config pineado ni pre-commit.)
5. **Cero cambio** de comportamiento en `.githooks/pre-commit`.
6. **Neutralidad + ASCII**.

## Guardas

El nucleo del riesgo es (4)+(2): que el hook enganche de verdad (no quede muerto como el error que
motivo C5) y que nada toque el hub pineado ni NOVA. Veredicto con el vector exacto.
