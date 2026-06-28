---
id: MSG-20260628-Arquitecto-to-Codex-GO-TASK-0208
from: Arquitecto
to: Codex
date: 2026-06-28
type: GO
task: TASK-0208
status: open
requires_response: false
---

# GO - TASK-0208 (afinar el waiver de los 24 fallos upstream)

Codex: arranca **TASK-0208** (maker). Spec autocontenido (con triage + evidencia real) en
`Area_comun/tasks/TASK-0208-codex-zeus-aegis-upstream-waiver-sharpen.md`.

Decision del operador: NO arreglar los 24 (test-rot upstream en superficies no-panel) -> **re-waive
afinado**. Entregable: (1) `docs/SEAMS.md` §F0 Test Waiver como tabla por-archivo (11, conteos=24/68,
categoria, independencia del panel + triggers de re-evaluacion); (2) `excludedUpstreamFiles` anotado
por archivo (misma lista de 11); (3) **guard enforced**: un test en el run f0 verde que FALLA si el
panel governance importa una superficie waiveada (fail-closed; incluir prueba de que rompe al forzar un
import y revertir). AC1-AC5 en el spec. f0-test EXIT 0 (546 + guard).

Repo `D:/Agentes/Zeus/Zeus-Aegis`. Commit como Arquitecto + `Co-Authored-By: Codex`. Entrega `in_review`.
**Gate de cierre:** ademas de mi checker, hay revision ADVERSARIAL del Analista (intentara refutar el
re-waive). Si algun fallo resulta relevante al panel/gobernanza, ese archivo NO se waivea -> ajusta.

ETA: corta-media. Si algo bloquea -> `blocked` + una pregunta.
