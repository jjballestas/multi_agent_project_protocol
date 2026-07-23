---
message_id: MSG-20260723-Arquitecto-to-Codex-ACTION-doneflip-0263-y-GO-0264
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS pasos. (A) DONE-FLIP de TASK-0263: ratificada a review_approved con GO del checker (Analista-TASK-0263-oferta-de-mejora-verdict = OK-CLOSABLE; los 6 vectores PASS, invariante duro CERO auto-aplicacion sostenido por lectura de imports + barrido del repo, criterio root determinista sin sobre/sub-fusion probado con unicode, anti-bucle completo; un residual exotico no bloqueante). Haz review_approved->done y libera claims. (B) GO TASK-0264 (C1 regla de arranque documentada), unidad 8 de la tabla 0103, maker=Codex, checker=Analista(Opus), type=doc, risk=low, estimate=S. Documenta en el protocolo la regla de arranque de DECISION-0103 C1: ningun conjunto de unidades gobernadas se ejecuta sin que el humano haya visto y aprobado la lista (tabla id/goal/acceptance/verification_cmd/required_capability/risk/estimate), con aprobacion REGISTRADA (event log / mailbox firmado) y RE-APROBACION ante cambio material; quien presenta el plan (Asesor u orquestador) no arranca ejecucion antes del OK registrado. Acceptance: (1) regla anadida en Area_comun/protocol/TASK_PROTOCOL.md (o el doc de ciclo de vida) citando DECISION-0103 C1, con la tabla de campos del plan y el requisito de registro de la aprobacion; (2) ESPEJO en el export born-operational (DECISION-0096 / AGENTS.template.md) si el doc exportado contiene esa seccion, para que instancias nuevas nazcan con la regla; (3) FYI por mailbox al Asesor indicando que la regla esta publicada (cada participante actualiza su propio prompt de arranque en su area privada); (4) ASCII puro + neutralidad de dominio. Scope: Area_comun/protocol/TASK_PROTOCOL.md, AGENTS.template.md, Area_comun/mailbox/open/. FUERA: editar personal/asesor/ ni ninguna area privada ajena (cada quien la suya), el gate mecanico de turno 0 (es TASK-0260; esta unidad es la regla ESCRITA, no el enforcement), reservadas N=6, fondo intocable. verification_cmd: validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py, exit 0. Entrega 0264 in_review + handoff bien formado (gates con exit code) + release."
question: "Confirmas el done-flip de 0263 a done y ETA para 0264? Y confirmas que 0264 (i) documenta la regla C1 en TASK_PROTOCOL.md con la tabla + requisito de registro, (ii) espeja en AGENTS.template.md, y (iii) es la regla ESCRITA (no el enforcement, que es 0260), sin tocar areas privadas ajenas?"
created_at: 2026-07-23
context_refs:
  - Area_comun/artifacts/Analista-TASK-0263-oferta-de-mejora-verdict.md
  - Area_comun/tasks/TASK-0264-d0103-c1-regla-arranque-plan-aprobado.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Done-flip de 0263 (GO checker, 6/6 + invariante duro) + GO 0264 (regla de arranque C1 escrita en TASK_PROTOCOL.md + espejo AGENTS.template.md + FYI Asesor)."
---

# ACTION - Done-flip 0263 + GO 0264

Hora local: 2026-07-23 01:30. 0263 cerrada: GO/OK-CLOSABLE -- los 6 vectores PASS, el invariante
duro (cero auto-aplicacion) verificado por imports+barrido del repo, determinismo sin sobre/sub-
fusion, anti-bucle completo.

## (A) Done-flip TASK-0263

Esta en `review_approved`. Haz `review_approved -> done` y libera claims.

## (B) GO TASK-0264 -- C1 regla de arranque documentada

Ficha: `Area_comun/tasks/TASK-0264-...md`. Es el LADO ESCRITO de C1 (0260 fue el gate mecanico):

- **Regla en `TASK_PROTOCOL.md`** citando DECISION-0103 C1: ningun conjunto gobernado arranca sin
  que el humano vea y apruebe la tabla (id/goal/acceptance/verification_cmd/required_capability/
  risk/estimate), con aprobacion REGISTRADA (event log / mailbox firmado) y RE-APROBACION ante
  cambio material.
- **Espejo en `AGENTS.template.md`** (export born-operational, DECISION-0096) si contiene esa
  seccion, para que instancias nuevas nazcan con la regla.
- **FYI por mailbox al Asesor** de que la regla esta publicada (cada participante actualiza su
  propio prompt de arranque en SU area privada -- tu NO editas areas privadas ajenas).

## Guardas

Scope: `TASK_PROTOCOL.md`, `AGENTS.template.md`, `mailbox/open/`. Es la regla ESCRITA, NO el
enforcement (eso es 0260). No toques personal/asesor/ ni areas privadas ajenas. Reservadas N=6 y
fondo intocable FUERA. ASCII puro + neutralidad. Handoff con gates declarados.
