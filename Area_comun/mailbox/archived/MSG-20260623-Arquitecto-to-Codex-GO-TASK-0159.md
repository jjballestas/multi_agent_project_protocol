---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0159
task_id: TASK-0159
type: DIRECTIVE
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0159 (ready): Intake v3 fixes UX + fix '0 candidatas' (AC59-AC63, Zeus-protocol). (59) Execute submit_intent OCULTO en modo archivo, se habilita al APROBAR una tarjeta o en modo individual/typed. (60) selector 'Proyecto destino' como PRIMER elemento, antes del file input. (61) 'Extraer requisito' muestra estado 'procesando' + boton deshabilitado mientras el agente trabaja. (62) errores en ROJO; la nota de ingestion lista las extensiones REALES del config (hoy hardcodea '.md/.txt' en app.js ~1202). (63) FIX '0 candidatas': el codigo de tarjetas+refresh YA existe (2afc944); 'Sin candidatas' = extraccion devolvio 0 almacenadas -> verifica que el server vivo HONRE el runtime override (file-ingestion.runtime.json: extractor enabled, local-vlm, loopback) y NO el versionado (extractor OFF); que la extraccion local-vlm parsee+almacene candidatas de un .md multi-seccion; si 0 con causa real -> ERROR visible, no panel mudo. REPRO: server vivo + Ollama + subir historias_panel_operar_agentes.md -> N tarjetas. maker=Codex/checker=Arquitecto+Analista; #4 byte-id; off-by-default; NUNCA pilotar contra el log vivo (PROTOCOL_REPO_PATH a un clon desechable)."
requested_action: "Reclama TASK-0159 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. AC59: en modo carga-por-archivo NO muestres el boton 'Execute submit_intent' (envio individual); habilitalo solo al hacer click en una tarjeta candidata y aprobar ese requisito, o en el modo individual/typed explicito. AC60: renderiza el selector 'Proyecto destino' como PRIMER div de la seccion file, antes del selector de archivos. AC61: al disparar 'Extraer requisito' muestra un indicador visible de 'procesando' y deshabilita el boton hasta que la extraccion responde (el agente tarda). AC62: pinta los errores en ROJO/estado de error (extraccion fallida, archivo rechazado, 0 candidatas con causa); cambia la nota de ingestion (public/app.js ~1202) para listar las extensiones REALES y maxBytes del config cargado, no el literal '.md/.txt'. AC63: garantiza que tras una extraccion exitosa las candidatas aparezcan como TARJETAS visibles (el refresh ya existe -- verificalo end-to-end); DIAGNOSTICA el 'Sin candidatas' del archivo del operador: confirma que el server vivo lee file-ingestion.runtime.json (extractor enabled/local-vlm/loopback) y no el versionado; que runFileExtractionAgent/local-vlm parsea y ESCRIBE candidatas al store (tmpdir/zeus-protocol-file-candidates) para un .md con varias historias (carry AC53 parse robusto, AC51 troceado, AC52 loopback, AC43 gate PII, candidatas no-ledger); si la extraccion da 0 con causa (modelo vacio/timeout) reportalo como error visible (AC62). Documenta el REPRO: server vivo (runtime override + Ollama) + subir personal/operador/historias_panel_operar_agentes.md (o una copia) -> N tarjetas candidatas. Manten verdes: node --test clon limpio, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica (protocol.config.json sin tocar), off-by-default. NUNCA pilotar contra el canonico: si el repro necesita el write gobernado usa PROTOCOL_REPO_PATH apuntando a un clon desechable. Entrega in_review."
context_refs:
  - Area_comun/tasks/TASK-0159-codex-intake-v3-ux-fixes-cards-empty.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - personal/operador/historias_panel_operar_agentes.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/design/interface/components/intake/
deadline_or_blocking_level: normal
---

# GO - TASK-0159: Intake v3 fixes UX + fix "0 candidatas" (AC59-AC63)

Feedback de uso real del operador sobre la carga por archivo. Cinco cosas: (59) ocultar "Execute submit_intent" en
modo archivo (es para envio individual; se habilita al aprobar una tarjeta o en modo typed); (60) selector de
"Proyecto destino" como PRIMER div antes del file input; (61) indicador de "procesando" al extraer (el agente
tarda); (62) errores en ROJO + la nota de ingestion debe listar las extensiones REALES (hoy hardcodea ".md/.txt");
(63) FIX del "Sin candidatas" -- el codigo de tarjetas+refresh ya esta, el problema es que la extraccion devolvio 0
almacenadas: verifica que el server vivo lee el runtime override (extractor ON/local-vlm/loopback) y que la
extraccion parsea+almacena candidatas de un .md multi-seccion; si 0 con causa real, error visible, no panel mudo.

REPRO obligatorio: server vivo + Ollama + subir `historias_panel_operar_agentes.md` -> deben salir N tarjetas. Si
resultaba ser solo un server stale (sin reiniciar), igual implementa la UX (59-62) y deja AC63 con el repro que
prueba que con el codigo correcto SI salen tarjetas. NUNCA pilotar contra el log vivo (clon desechable). maker=Codex
/ checker=Arquitecto + Analista. #4 byte-identica; off-by-default.
