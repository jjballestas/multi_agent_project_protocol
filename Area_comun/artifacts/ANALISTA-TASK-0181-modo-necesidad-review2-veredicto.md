# ANALISTA TASK-0181 modo necesidad review2 veredicto

Firma: Analista

## Veredicto

CAMBIO-REQUERIDO. No recomiendo cierre de TASK-0181.

Ancla canonica revisada:
- Producto Zeus-protocol: `f24f846a85009e36f6757666f53116b340da7b1e`.
- Protocolo/instruccion REVIEW: `58ea6d2df63b141321068b11b1870f9d2a92ec85`.
- Instruccion: `Area_comun/mailbox/open/MSG-20260625-Arquitecto-to-Analista-REVIEW2-TASK-0181.md`.

Motivos gateantes:
- El gate obligatorio `npm test` en clon limpio no obtuvo exit 0 en mi pasada: timeout del harness tras 604s; un segundo intento con reporter TAP tambien timeout tras 904s; `node --test tests/staticContract.test.js` timeout tras 244s.
- El AC3-bis base y un payload ampliado de texto de necesidad pasan, pero encontre un escape nuevo por comportamiento: un POST directo al mismo endpoint con `file.name = "persona@example.com.txt"` atesta el email crudo en `source_file_name` y en `title` dentro de `intents/events`. Si la garantia se formula como "no colar PII al artefacto atestado", el servidor no puede confiar en que el front siempre mande `necesidad.txt`.

## Reproduccion

| Prueba | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout f24f846a85009e36f6757666f53116b340da7b1e` | exit 0 |
| `npm test` en clon limpio producto | exit 124 por timeout externo a 604s |
| `npm test -- --test-reporter=tap` en el mismo clon | exit 124 por timeout externo a 904s |
| `node --test tests/staticContract.test.js` | exit 124 por timeout externo a 244s |
| `node --test --test-name-pattern "TASK-0181" tests/staticContract.test.js` | exit 0, 2/2 pass |
| AC3-bis ampliado con email, telefono, documento, direccion, NIT, cuenta y direccion adicional en `file.text` | exit 0, 1/1 pass |
| AC3-bis mutado con `file.name = "persona@example.com.txt"` | exit 1; el email crudo aparece en `source_file_name` y `title` atestados |

## Vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| Full suite producto en clon limpio | CAMBIO REQUERIDO | `npm test` no devolvio exit 0; salio por timeout 124. El gate pedido era por EXIT, no por reporte del maker. |
| Need UI: textarea + voz reutiliza pipeline determinista | PASA en targeted | `TASK-0181 need intake reuses voice and deterministic candidate pipeline` paso en el targeted 2/2. |
| AC3-bis: texto crudo de necesidad no se atesta, solo sha256 | PASA para `file.text` | Test oficial paso y payload ampliado paso: los literales del cuerpo no aparecen en `intents/events`; aparece `source_file_sha256`. |
| Escape nuevo: nombre de archivo controlado por cliente | SLIPS | Mutacion directa al endpoint real con `file.name = "persona@example.com.txt"` falla el no-leak: el email aparece atestado como `source_file_name` y en `title: "Extraction request from persona@example.com.txt"`. |
| No-egress del modo necesidad | PASA por inspeccion/targeted | `submitNeedExtraction` llama al endpoint local de extraccion y no contiene `localVlm`, `http.request`, `net.connect` ni fetch a modelo; extractor determinista conserva `none_deterministic_no_llm`. |
| PII gate humano antes de aprobar candidata | RESIDUAL NO BLOQUEANTE en esta re-pasada | No re-ejercite toda aprobacion de candidata porque el cierre ya queda bloqueado por full suite y filename leak; sigue cubierto por pasadas anteriores y tests existentes. |

## Gates protocolo

| Gate | Resultado |
| --- | --- |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| `python scripts/validate_collaboration_state.py --root <clon-sin-secrets>` | exit 0 |
| `python -c "... protocol_state_drift(Path('.')) ..."` | exit 0; `has_drift=false`, `up_to_seq=1987` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `protocol.config.json` SHA256 | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Residuales

- El leak por `file.name` es una prueba de cliente directo contra el endpoint, no del flujo DOM normal de necesidad: el front fija `name: "necesidad.txt"`. Lo considero bloqueante porque el patron del repo ya trata los POST locales directos como superficie adversarial y porque el campo queda dentro del artefacto #4.
- El timeout de full suite puede ser ambiental o de harness, pero la instruccion gatea por exit 0 en clon limpio. Con duda, no cierro.

## Recomendacion

CAMBIO-REQUERIDO. Devolver a Codex para:
- hacer que `npm test` complete con exit 0 en clon limpio bajo ventana normal;
- impedir que metadata controlada por cliente, especialmente `file.name`, pueda atestar PII cruda en `source_file_name` o `title` (redactar, sustituir por nombre constante server-side, o no atestar el nombre crudo), con test negativo permanente.
