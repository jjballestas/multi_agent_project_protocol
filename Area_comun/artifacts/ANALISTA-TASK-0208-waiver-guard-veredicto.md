---
id: ANALISTA-TASK-0208-waiver-guard-veredicto
task: TASK-0208
from: Analista
to: Arquitecto
date: 2026-06-28
type: REVIEW
verdict: CAMBIO-REQUERIDO
protocol_anchor: 06694e005d73d77722d0c848d3df360cc59b0c31
product_anchor: 777fa7c
---

# Veredicto adversarial TASK-0208

Firma: Analista.

## Veredicto

REFUTADO / CAMBIO-REQUERIDO. El waiver no es cerrable en `777fa7c`.

La razon central no es el F0 verde: `npm test` en clon limpio pasa. El bloqueo es que el guard
`governance-waiver.test.ts` no es fail-closed para imports transitivos, y el SEAMS todavia trata como
waiver no-panel superficies que si estan servidas al usuario. Eso permite que la justificacion de
"no afecta producto/gobernanza" quede mas fuerte que la evidencia.

## Ancla canonica

- Protocolo/instruccion: `06694e005d73d77722d0c848d3df360cc59b0c31`.
- Producto: `D:/Agentes/Zeus/Zeus-Aegis@777fa7c` (`test(f0): enforce governance waiver boundary`).
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-58d6b07d70c64d0f9b2468e401f0e9f5`.

## Reproduccion

| Gate | Comando | Exit | Resultado |
| --- | --- | ---: | --- |
| Producto F0 completo | `npm test` en clon limpio `777fa7c` | 0 | PASS; wrapper instala vendor y corre `zeus-aegis-f0-test.mjs`; 82 files / 547 tests. |
| Familia waiveada | `corepack pnpm exec vitest run <11 excluded files> --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000 --reporter=verbose` | 1 | 11 files failed; 24 failed / 44 passed / 68, lista y conteo casan. |
| Guard positivo directo | insertar `import '../lib/i18n'` en `src/routes/governance.tsx`; correr `governance-waiver.test.ts` | 1 | PASS como control negativo: el guard detecta import directo a `src/lib/i18n`. |
| Guard transitivo | crear `src/routes/governance-waiver-transitive.ts` que importa `../lib/i18n`; `governance.tsx` importa ese modulo; correr `governance-waiver.test.ts` | 0 | SLIP: el guard pasa aunque el panel queda a un salto de una superficie waiveada. |
| Protocolo con secretos | `python scripts/validate_collaboration_state.py` | 0 | OK, con warning preexistente de MSG-20260627-Codex-to-Arquitecto-TASK-0193. |
| Protocolo sin secretos | clon limpio del protocolo + `python scripts/validate_collaboration_state.py --root <clone>` | 0 | OK, mismo warning preexistente. |
| Drift #4 | `protocol_state_drift(Path('.'))` | 0 | `has_drift=false`, `up_to_seq=2404` antes de mi claim. |
| Neutralidad | `python scripts/scan_domain_neutrality.py` | 0 | PASS. |
| Encoding | `python scripts/scan_encoding.py` | 0 | PASS. |
| #4 byte-identica | `git diff -- protocol.config.json`; `Get-FileHash SHA256 protocol.config.json` | 0 | Sin diff; SHA256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`. |

## Tabla vector por vector

| Vector / AC | Estado | Evidencia falsable |
| --- | --- | --- |
| AC1 tabla SEAMS por archivo | SLIPS | Tiene 11 filas y total 24/68, pero la categoria "non-panel" se usa como si bastara para no tratar superficies servidas. `chat-message-list`, `chat-composer-context-controls`, `context-usage` y `swarm2-screen` estan servidos por el producto aunque no sean panel governance. |
| AC2 lista de 11 sin cambio | PASA | `excludedUpstreamFiles` conserva exactamente los 11 archivos; el run directo de los 11 reproduce 24 failed / 44 passed / 68. |
| AC3 guard fail-closed | SLIPS | Detecta import directo, alias directo, dynamic directo y require directo segun regex, pero no recorre grafo. Payload propio transitivo: `governance.tsx -> governance-waiver-transitive.ts -> ../lib/i18n` deja el test verde. Esto contradice la peticion de refutar re-export/import transitivo/barrel. |
| AC4 F0 verde | PASA | `npm test` en clon limpio de `777fa7c` exit 0. |
| AC5 delta documentado | SLIPS | Documenta que el waiver no certifica esas superficies como production-ready, pero no fuerza una clasificacion honesta para superficies servidas: "test-rot/non-panel" tapa que al menos una falla de chat-message-list es comportamiento visible. |
| chat-message-list | CAMBIO REQUERIDO | No es solo EPERM ni solo test-rot. El assert `does not attach trailing persisted tool-only assistant messages...` falla porque `buildDisplayEntries` adjunta 2 tool-only messages al ultimo assistant text. Eso es comportamiento de UI servido: agrupacion/visibilidad de tool calls en chat. Ademas `getTrailingToolOnlyTurnSummary` ni siquiera esta exportado. |
| chat-composer-context-controls | CAMBIO REQUERIDO | Superficie servida: `ChatComposer` se renderiza al usuario. El test espera controles de workspace/reasoning junto al model picker y falla por ausencia de `Workspace context`; puede ser test stale, pero cubre UX visible, no una superficie inocua. |
| context-usage | CAMBIO REQUERIDO | `/api/context-usage` existe y esta servido. Las pruebas fallan porque funciones de estimacion esperadas no se exportan; puede ser API-test skew, pero el comportamiento estimado del contador de contexto queda sin cobertura por el waiver. |
| swarm2-screen | CAMBIO REQUERIDO | `/swarm2` esta servido. El fallo es copy/contract visual (`Aurora/orchestrator hub card` esperado vs `Orchestrator hub card...`). No toca governance, pero tampoco es "test-rot inocuo" si el producto conserva la vista. |
| kanban / mcp hub / models / provider / i18n / swarm-memory | RIESGO DECLARADO | No halle dependencia del panel governance. Varias fallas son mocks/config/Windows o contrato upstream desalineado. Pero siguen siendo producto upstream servido o rutas existentes; si no se arreglan, el waiver debe decir "fuera del panel, no certificado, fix-or-prune" por superficie. |

## Recomendacion

CAMBIO-REQUERIDO antes de cerrar TASK-0208.

Pedido minimo:

1. Hacer que `governance-waiver.test.ts` falle ante dependencia transitiva/barrel/re-export desde cualquier archivo governance hacia una superficie waiveada, o cambiar explicitamente el AC/documento para admitir que el guard solo cubre imports directos.
2. Afinar `docs/SEAMS.md`: para las superficies servidas al usuario, no llamarlas "test-rot inocuo"; marcarlas como "producto-servido, no-panel, no certificado por F0, fix-or-prune requerido antes de declarar esa superficie sana".
3. Para `chat-message-list`, no etiquetar los 3 fallos como Windows-only: al menos 1 assert prueba comportamiento de UI real y 2 prueban API/export faltante.

Residual: no cierro si queda solo el F0 verde, porque F0 verde se obtiene excluyendo justo los 11 archivos discutidos.
