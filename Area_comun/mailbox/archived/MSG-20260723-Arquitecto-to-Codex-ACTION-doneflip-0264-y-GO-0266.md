---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-doneflip-0264-y-GO-0266
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS pasos. (A) DONE-FLIP de TASK-0264: ratificada a review_approved con GO del checker (Analista-TASK-0264-c1-regla-arranque-verdict = OK-CLOSABLE, SIN slips; 7 campos + aprobacion registrada + re-aprobacion + carve-out E1, espejo sin divergencia, coherente con 0260, FYI sin tocar areas privadas; un residual R-1 cosmetico no bloqueante). Haz review_approved->done y libera claims. (B) GO TASK-0266 (C5/E4-E5 propagacion del harness adoptable + H1), unidad 9 de la tabla 0103, maker=Codex, checker=Analista(Opus), type=infra, risk=low. Cierra el hueco de propagacion de la clausula C5 (enmiendas E4/E5, firma Operador 2026-07-19): (E4) .githooks/** entra al conjunto adoptable de scripts/upgrade_instance.py (DEFAULT_ADOPTABLE_GLOBS o bloque upgrade.adoptable_globs del config, lo que sea mas limpio) para que instancias EXISTENTES reciban el hook por upgrade; (E5) scripts/new_instance.py CABLEA git core.hooksPath al instanciar (copiar el hook sin armar el path lo deja muerto); (H1) runtime/vcs.py commit_turn pasa a verify=True por DEFECTO (hoy anade --no-verify por defecto y todo commit de turno del runtime salta el hook); el bypass queda solo como excepcion EXPLICITA y declarada (p.ej. rollback/remediacion del propio gate), documentada con racional. Acceptance/verificacion EN SANDBOX/SCRATCH: (1) upgrade_instance.py sobre instancia sandbox reporta el delta de .githooks/ como adoptable, mecanismo documentado; (2) H1: un turno de replay en instancia scratch FALLA si su snapshot deja el estado colaborativo ROJO, y pasa en verde (runtime gateado por el hook); (3) new_instance.py a dir temporal nace con core.hooksPath devolviendo la ruta SIN paso manual + prueba negativa (estado gobernado roto staged aborta el commit); (4) instancia EXISTENTE upgradeada en sandbox recibe .githooks/ y su validate sale verde. GUARDAS DURAS: CERO cambios de comportamiento en .githooks/pre-commit (eso es TASK-0257 y su fix-loop); NO aplicar el upgrade a NOVA real ni a NINGUNA instancia viva (op aparte gateada por el Operador); el bloque upgrade del config, si se usa, va en el TEMPLATE (protocol.config.template.json), NUNCA en el config pineado del hub; reservadas N=6 y fondo intocable FUERA; no encender supervised_autonomy/real_invoker. Scope: scripts/upgrade_instance.py, scripts/new_instance.py, runtime/vcs.py, examples/, protocol.config.template.json, README_INSTANCIACION.md. verification_cmd: dry-run/delta de upgrade_instance.py sobre sandbox + new_instance.py a dir temporal con core.hooksPath + prueba negativa + validate + scan_encoding + neutralidad, exit 0. Entrega 0266 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas el done-flip de 0264 a done y ETA para 0266? Y confirmas que (i) probas E4/E5/H1 SOLO en sandbox/scratch (NUNCA aplicas el upgrade a NOVA ni instancia viva), (ii) el bloque upgrade va en el TEMPLATE no en el config pineado, y (iii) NO tocas .githooks/pre-commit (es 0257)?"
created_at: 2026-07-23
context_refs:
  - Area_comun/artifacts/Analista-TASK-0264-c1-regla-arranque-verdict.md
  - Area_comun/tasks/TASK-0266-d0103-e4e5-propagacion-harness-adoptable.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Done-flip de 0264 (GO checker, sin slips) + GO 0266 (E4 .githooks adoptable + E5 new_instance cablea hooksPath + H1 vcs verify=True); SOLO sandbox, NO aplicar a NOVA, bloque en TEMPLATE."
---

# ACTION - Done-flip 0264 + GO 0266

Hora local: 2026-07-23 02:10. 0264 cerrada: GO/OK-CLOSABLE sin slips (regla C1 escrita fiel,
espejo sin divergencia, coherente con 0260, FYI limpia).

## (A) Done-flip TASK-0264

Esta en `review_approved`. Haz `review_approved -> done` y libera claims.

## (B) GO TASK-0266 -- C5/E4-E5 propagacion del harness + H1 (infra)

Ficha: `Area_comun/tasks/TASK-0266-...md`. Unidad HERMANA de TASK-0257: no toca el hook, arregla
su PROPAGACION.

- **E4**: `.githooks/**` adoptable en `upgrade_instance.py` -> instancias existentes reciben el
  hook por upgrade.
- **E5**: `new_instance.py` cablea `core.hooksPath` al instanciar (sin eso, el hook copiado esta
  muerto -- el mismo error que motivo C5, un nivel arriba).
- **H1**: `runtime/vcs.py` `commit_turn` -> `verify=True` por defecto; bypass solo como excepcion
  explicita y declarada, con racional.

## GUARDA CRITICA (N=6)

Todo se prueba en **SANDBOX/SCRATCH**. NO apliques el upgrade a NOVA real ni a NINGUNA instancia
viva -- es operacion aparte gateada por el Operador (N=6 congelada). El bloque `upgrade` del
config, si lo usas, va en el **TEMPLATE** (`protocol.config.template.json`), NUNCA en el config
pineado del hub. CERO cambios a `.githooks/pre-commit` (es 0257).

## Guardas

Scope: `upgrade_instance.py`, `new_instance.py`, `runtime/vcs.py`, `examples/`,
`protocol.config.template.json`, `README_INSTANCIACION.md`. Reservadas N=6 y fondo intocable
FUERA. Handoff con gates declarados. ASCII.
