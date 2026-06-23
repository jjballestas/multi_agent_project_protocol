---
handoff_id: HANDOFF-TASK-0159-codex-to-arquitecto-1
task_id: TASK-0159
from: Codex
to: Arquitecto
status: ready_for_review
product_commit: bc8346d
created_at: 2026-06-23T12:00:00Z
---

# TASK-0159 - entrega Codex

Implementacion en `D:/Agentes/Zeus/Zeus-protocol`:

- Commit producto: `bc8346d fix(intake): surface file extraction candidates`.
- AC59: en modo archivo se oculta el boton directo `EXECUTE SUBMIT_INTENT`; la ejecucion queda en `Aprobar` candidata o modo digitado.
- AC60: `Proyecto destino` es el primer control de la seccion de archivo.
- AC61: `Extraer requisito` muestra `Procesando extraccion...` y deshabilita el boton hasta respuesta.
- AC62: errores locales, escritura, extraccion fallida y 0 candidatas se muestran en rojo; la nota de ingestion usa `allowedExtensions` y `maxBytes` del config cargado.
- AC63: el server honra `file-ingestion.runtime.json` con `endpoint`/`model` local-vlm a nivel de `extractor`, escribe candidatas al store y registra `completed-empty` con razon explicita cuando el extractor devuelve 0.

Evidencia:

- `node --check public/app.js src/server.js tests/staticContract.test.js` OK.
- `git diff --check` OK.
- `npm test` PASS 52/52.
- clean clone `npm test` PASS 52/52.
- smoke local puerto 4190 OK: `/healthz` y `/api/protocol/actions` confirmaron runtime override gitignored ON, `provider=local-vlm`, loopback `127.0.0.1:11434`, extensiones reales `.md/.txt/.html/.pdf/.png/.jpg/.jpeg`.
- Protocolo: encoding OK, neutrality OK, `validate_collaboration_state.py --root .` OK, drift false `up_to_seq=1302` antes de cierre; `--with-secrets` no existe en el validador actual.

REPRO para checker:

1. Usar un clon desechable del protocolo en `PROTOCOL_REPO_PATH`; no usar el canonico vivo.
2. En Zeus-protocol, mantener `file-ingestion.runtime.json` gitignored con extractor enabled/local-vlm/loopback y Ollama en `127.0.0.1:11434`.
3. Arrancar el server producto y subir `personal/operador/historias_panel_operar_agentes.md` desde modo Archivo.
4. Esperado: nota de ingestion con extensiones reales del runtime, estado de procesamiento visible, y N tarjetas candidatas visibles. Si el modelo responde vacio/timeout, el panel queda en error rojo con causa, no en silencio.

No se modifico `protocol.config.json`; extractor sigue OFF-by-default en el config versionado.
