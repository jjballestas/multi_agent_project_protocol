---
artifact_id: ANALISTA-TASK-0219-veredicto
task_id: TASK-0219
type: adversarial_review
from: Analista
to: Arquitecto
status: final
canonical_protocol_head: e96ac4121ecc4de3ac61610c3712acef2d8c5508
instruction_commit: 825ca6f
engram_source_commit: 44faeee1fb4fabdee4ba9619df55af485f3d06eb
verdict: NO-GO
---

# Veredicto Analista - TASK-0219 Engram

Firma: Analista.

## Veredicto

NO-GO para promover la DECISION o aplicar el PATCH tal cual.

La idea Tier 0 local/off-ledger puede sobrevivir como herramienta privada por agente, pero la propuesta de Tier 1 compartido no cumple aun las garantias que afirma: el ledger seguiria aceptando texto libre en `title`, el puente `engram_bridge` introduce una brecha de dos fases fuera de la transaccion atomica, la reconstruccion desde markdown no existe en el parche, `map-<id>` es identidad disciplinaria y no enforcement, y la frontera "Engram != ledger" no queda estructuralmente protegida contra fuente de verdad sombra.

## Anclas y reproduccion

| Item | Resultado |
| --- | --- |
| Repo protocolo canonico | `e96ac4121ecc4de3ac61610c3712acef2d8c5508` |
| Instruccion REVIEW | `Area_comun/mailbox/open/MSG-20260629-Arquitecto-to-Analista-GO-TASK-0219.md` introducida en `825ca6f` |
| Clon limpio protocolo | `C:/Users/johnb/AppData/Local/Temp/protocol-review-0219-ab92b4cf67514b5cadc43d7dbc85b39e` |
| Engram fuente primaria | `github.com/Gentleman-Programming/engram` en `44faeee1fb4fabdee4ba9619df55af485f3d06eb` |
| Producto Zeus-protocol / npm test | N/A: la instruccion TASK-0219 no cita commit de producto ni AC de producto; el objeto bajo review son drafts y codigo del protocolo |
| `python scripts/validate_collaboration_state.py` vivo | exit 0 |
| `python scripts/validate_collaboration_state.py` clon sin secretos | exit 0 |
| Drift #4 vivo | `has_drift=false`, `up_to_seq=2631` tras claim acquire |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` | byte-identico, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Fuentes primarias verificadas

| Afirmacion load-bearing | Estado |
| --- | --- |
| Go binary + SQLite/FTS5 + MCP | CONFIRMADO: `README.md:28-35`; tools MCP en `README.md:120-129`. |
| `mem_save` y campos | CONFIRMADO: REST observation documenta `{session_id,type,title,content,tool_name?,project?,scope?,topic_key?}` en `DOCS.md:136`; DB observations incluye `title`, `content`, `project`, `scope`, `topic_key` en `DOCS.md:46`. |
| Scope no es privacidad | CONFIRMADO: `docs/TEAM-USAGE.md:22-30` dice que scope filtra busqueda pero no sync; `docs/TEAM-USAGE.md:111-116` dice que `personal` no queda local automaticamente. |
| Sin autor en observaciones | CONFIRMADO para observations: `DOCS.md:46` no contiene author/actor. Matiz: `memory_relations` si tiene `marked_by_actor` en `DOCS.md:51`, por tanto "sin campo de autor en los registros" es impreciso si se afirma para todo registro. |
| SQLite local fuente de verdad + chunks gzip | CONFIRMADO: `README.md:150-165`, `DOCS.md:1115-1138`, `docs/ARCHITECTURE.md:299`. |
| Sin resolucion de merge documentada | REFUTADO como frase fuerte: `README.md:150` y `DOCS.md:1136-1138` documentan estrategia de chunks append-only y "no merge conflicts"; no documentan una resolucion semantica de conflictos, pero si una evitacion de merge de archivos. |

## Tabla A-H

| Vector | Veredicto | Severidad | Evidencia / escenario falsable |
| --- | --- | --- | --- |
| A. No-interferencia TFM | REFUTADO parcialmente | bloqueante para Tier 1 | El mecanismo off no emite eventos por si mismo, pero la DECISION promovida si crea un evento `decision` y el parche anade un nuevo tipo de intent al instrumento. El draft difiere Tier 1 por regla documental; el patch propone `event-state.runtime.json -> engram.enabled`, pero el flag no existe aun y no hay guard probado en ambos caminos. Condicion minima: gate estructural default false, tests negativos single y `--intents`, y regla de activacion post-dataset fuera del alcance de agentes no operadores. |
| B. Hash-no-cuerpo / PII | REFUTADO | bloqueante | I4 prohibe `content/body/message/observation/text`, pero conserva `title` como texto libre. El propio Engram trata `title` y `content` como FTS (`DOCS.md:46-47`). Payload falsable: `title="persona@example.com Calle 10 No 20-30"` con `content_sha256` valido no es rechazado por el patch spec. `topic_key` queda slug, pero puede portar identificadores cortos; `content_sha256` tambien permite diccionario para cuerpos cortos/predecibles. Esto no es "cero PII estructural"; es disciplinario hasta ENG-PII. |
| C. Single-writer / dos fases | REFUTADO | bloqueante | El draft dice que runtime hace `mem_save` despues de que la transaccion del ledger aterrice. Eso preserva un solo escritor del ledger, pero no atomicidad ledger+memoria. Escenarios: ledger commit OK y `mem_save` falla -> ledger atesta memoria inexistente; `mem_save` OK y proceso cae antes de marcar bridge -> memoria existe sin cierre operativo. Condicion minima: outbox durable/idempotente, estado de entrega atestado, retry, reconciliador y semantica honesta "event log atesta solicitud/receipt", no "memoria registrada" hasta ack. |
| D. Indice derivado reconstruible | REFUTADO | bloqueante | El draft afirma que Engram se reimporta desde markdown, pero el patch no incluye importador markdown->Engram ni esquema canonico de memoria en markdown. Engram si tiene import/export JSON y sync chunks (`DOCS.md:180-185`, `DOCS.md:1110-1119`), no un importador desde `personal/<id>/MEMORY.md`. Condicion minima: definir y probar reconstruccion determinista desde markdown o bajar la afirmacion a "cache no autoritativa no reconstruible automaticamente". |
| E. Namespacing como autor | REFUTADO | mayor/bloqueante si se vende como identidad | Fuente primaria confirma que proyecto/scope son seleccion y filtro (`DOCS.md:692`, `docs/TEAM-USAGE.md:22-30`), no identidad del agente. `map-codex` solo es convencion salvo que el MCP wrapper/bridge imponga actor->memory_project. Condicion minima: enforcement server-side en bridge: actor `Analista` solo puede escribir `map-analista`; `map-shared` solo por intent Tier 1 autorizado. |
| F. Frontera Engram != ledger | REFUTADO | mayor | La frontera esta escrita como regla, pero no hay mecanismo para impedir que agentes usen recall como fuente de verdad sombra en conflictos con `Area_comun/state/*.json` o decisiones. Condicion minima: contrato operativo y tests/harness que todo cierre/claim/decision lee canonico primero y que Engram solo puede emitir hints con referencia a commit/path verificable. |
| G. Neutralidad de dominio | SOBREVIVE con correccion | menor | La decision/patch core no mete terminos de negocio del producto. Pero el draft de tarea diferida ENG-PII cita ejemplos de dominio especifico ("NIT", "razon social", "SQL de Budget"). Eso debe moverse a perfil/instancia o redactarse como `domain-specific identifiers` para core neutral. |
| H. Correccion del parche | REFUTADO | bloqueante | En el codigo canonico `submit_intent.py`, el caso `decision` es el fall-through final de `normalize_intent` (`runtime/submit_intent.py:375-389`); insertar `engram_observation` antes puede preservar decision si retorna siempre. Pero la spec no muestra el punto exacto de enforcement en ambos caminos: single valida en `runtime/submit_intent.py:999-1031`; transaccion emite en `runtime/submit_intent.py:1147-1167` tras validaciones previas. El no-op de replay es conceptualmente seguro porque `apply_intent_event` solo muta transiciones conocidas (`runtime/protocol_replay.py:881-930`), pero debe ser testado byte-identico. Condicion minima: parche real con tests para disabled single, disabled `--intents` rollback, enabled zero-drift, replay no-op y decision fall-through. |

## Bloqueantes

1. B-PII: `title` y parte de `topic_key` siguen siendo superficie libre/identificable. No cumple "cero PII estructural".
2. C-atomicidad: `engram_bridge` post-commit es dos fases sin outbox/ack/reconciliacion definidos.
3. D-reconstruccion: "indice derivado y reconstruible desde markdown" no tiene mecanismo ni test.
4. E-identidad: `map-<id>` no es autor ni aislamiento sin enforcement actor->project.
5. H-parche: falta implementacion probada del gate en ambos caminos y rollback; no basta la spec.
6. A-activacion: diferimiento de Tier 1 queda disciplinario hasta que exista flag default false y politica de activacion no accesible por agentes durante captura.

## Correcciones minimas exigidas

1. Cambiar la decision para distinguir Tier 0 permitido de Tier 1 NO autorizado; no afirmar Tier 1 como integrado ni estructuralmente seguro.
2. Sustituir I4 por un contrato estructural: `title` sin PII mediante allowlist/slug o derivado fijo; `topic_key` allowlist/slug; rechazo de todo campo no permitido, no solo blacklist de cuerpo.
3. Definir outbox del bridge: evento atesta solicitud, bridge hace `mem_save`, registra ack/fallo sin cuerpo, retry idempotente y reconciliador que detecta ledger-sin-memoria y memoria-sin-ledger.
4. Implementar actor->memory_project en runtime/bridge; `map-shared` solo por intent validado.
5. Probar reconstruccion desde markdown o eliminar la promesa de reconstruibilidad automatica.
6. Mover ejemplos de PII de dominio fuera del core.
7. Entregar patch real con tests negativos en clean clone para single y `--intents`, zero-drift, replay no-op y decision fall-through.

## Recomendacion

NO-GO tal cual. Recomendacion operacional: permitir solo Tier 0 local/off-ledger como practica privada no canonica, sin DECISION de Tier 1 ni patch de `engram_observation` hasta cerrar los bloqueantes anteriores. Con esas correcciones, el siguiente estado aceptable seria GO-CON-CONDICIONES, no GO pleno.

