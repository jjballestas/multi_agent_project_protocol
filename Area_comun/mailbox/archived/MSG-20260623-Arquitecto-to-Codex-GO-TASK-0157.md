---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0157
task_id: TASK-0157
type: DIRECTIVE
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0157 (ready): Intake v3 en Zeus-protocol. (A) modo carga-por-archivo abre SECCION dedicada (selector + boton Extraer requisito como primer elemento visible, SIN scroll, SIN pedir Titulo/Narrativa/Intencion antes); boton -> ruta gobernada del Extractor -> candidatas como TARJETAS -> click puebla [Titulo,Narrativa,Intencion]. (B) auto-commit-push ergonomico: el server PREFIERE el override runtime gitignored (*.runtime.json) cuando existe (cae al versionado off-by-default si no) -> Execute submit_intent llega al canonico sin push manual; versionado sigue enabled:false. AC55-AC58, carry AC16/17/43/51-54. #4 byte-identica. maker=Codex/checker=Arquitecto+Analista. Cierra tambien TASK-EXTRACT-DC0E283672 (done; spawned este task)."
requested_action: "Reclama TASK-0157 (ready), implementa en D:/Agentes/Zeus/Zeus-protocol y entrega in_review. AC55: en el Intake, elegir 'carga por archivo' abre una SECCION dedicada cuyo PRIMER elemento visible es el selector de archivo + boton 'Extraer requisito' (sin scroll para alcanzarlo); NO renderices ni exijas Titulo/Narrativa/Intencion de aceptacion ANTES de cargar el archivo. AC56: el boton 'Extraer requisito' manda el archivo a la ruta gobernada del Extractor (/api/protocol/intake-extractions/run, off-by-default, loopback, carry AC51-54) y al volver renderiza las candidatas como TARJETAS (una por candidata, pendientes de aprobacion). AC57: click en una tarjeta puebla las secciones [Titulo, Narrativa, Intencion de aceptacion] con los valores de esa candidata, pendiente de aprobacion humana + submit_intent (no entra al ledger antes; gate PII AC43 intacto). AC58: cambia la RESOLUCION de config en el server para PREFERIR el override runtime gitignored (commit-push.runtime.json / file-ingestion.runtime.json) cuando exista, cayendo al config versionado off-by-default cuando no; con override activo, 'Execute submit_intent' dispara commit+push del output gobernado a origin (visible al checker sin push manual); el config VERSIONADO permanece enabled:false (invariante off-by-default para clones/CI); el push solo propaga el output de submit_intent (carry AC17 no-bypass; no es segundo escritor); manten isLoopbackHost estricto. Behavior-tests deterministas por AC (DOM/render AC55-57; git mockeado AC58). Manten verdes: node --test clon limpio, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica (core/config/genesis/registry/keys sin tocar). NO enciendas nada vivo por tu cuenta (la activacion la hace el operador via el override runtime). Cierra TASK-EXTRACT-DC0E283672 ready->done (lo spawneo este task; tienes implementer)."
context_refs:
  - Area_comun/tasks/TASK-0157-codex-intake-v3-file-mode-cards-autopush.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/task-extract-dc0e283672-file-intake.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/public/index.html
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/intake/
deadline_or_blocking_level: normal
---

# GO - TASK-0157: Intake v3 (file-mode seccion + tarjetas candidatas + auto-push ergonomico)

Feedback de uso real del operador, capturado por el propio Intake gobernado (TASK-EXTRACT-DC0E283672). Dos frentes:

**A. UX de carga por archivo (AC55-AC57).** Hoy el cargador queda abajo (hay que hacer scroll) y se piden los
campos antes. Cambialo: elegir "carga por archivo" abre una SECCION propia (selector + boton "Extraer requisito"
arriba, sin scroll); el boton manda al Extractor y muestra las candidatas como TARJETAS; al hacer click en una
tarjeta se pueblan [Titulo, Narrativa, Intencion de aceptacion]. NO pidas esos campos antes de la carga (vienen en
el archivo o los pone el modelo). Reutiliza lo ya construido: rutas intake-extractions/intake-candidates,
buildFileRequirementPayload, buildCandidateApprovalPayload, diseno en design/interface/components/intake/.

**B. Auto-push ergonomico (AC58).** El operador tuvo que hacer push manual para que yo (checker) viera el requisito.
El codigo de auto-commit-push ya existe (commitAndPushSubmitIntentOutputs) y commit-push.runtime.json ya esta
enabled:true; falta que el server LO LEA: cambia la resolucion de path para preferir el *.runtime.json gitignored
cuando exista (default versionado sigue enabled:false). Asi "Execute submit_intent" llega a origin sin paso manual.
No conviertas el push en un segundo escritor: solo propaga el output que ya escribio submit_intent (carry AC17).

OFF-by-default e #4 byte-identica: sin override runtime presente, el comportamiento vivo queda apagado y el core/
config/genesis/registry/keys NO se tocan. Entrega in_review con node --test verde en clon limpio + validate con/sin
secretos exit 0; yo reproduzco desde clon limpio (.protocol-tmp/zc) y el Analista hace la pasada (egress/PII) antes
de cerrar. Cierra de paso TASK-EXTRACT-DC0E283672 (done).
