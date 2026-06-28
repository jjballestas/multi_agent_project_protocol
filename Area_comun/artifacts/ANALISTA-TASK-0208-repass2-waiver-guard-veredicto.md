# ANALISTA TASK-0208 REPASS2 - waiver guard

Firma: Analista
Fecha: 2026-06-28
Veredicto: REFUTADO / CAMBIO-REQUERIDO
Recomendacion de cierre: NO CERRABLE

## Ancla canonica

- Protocolo HEAD revisado: `cad710c` (`coord(TASK-0208): re-pass2 adversarial al Analista sobre 52f0d5e (normalize fix)`).
- Instruccion REVIEW procesada: `Area_comun/mailbox/open/MSG-20260628-Arquitecto-to-Analista-REPASS2-TASK-0208.md`.
- Producto revisado: `D:/Agentes/Zeus/Zeus-Aegis@52f0d5e112329db67aa469364bdd6b1b93359ba8`.
- Clon limpio producto: `C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-4ee60e6ad2744822ba93180de5e77ae8`.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| `git clone D:/Agentes/Zeus/Zeus-Aegis <tmp>; git checkout 52f0d5e` | exit 0 |
| `npm test` en clon limpio producto | exit 0 |
| `corepack pnpm exec vitest run src/server/governance-waiver.test.ts --reporter=dot` con probes Analista temporales | exit 0, 16/16 |
| Probe nativo ESM: `import './%69%31%38%6e.mjs'` contra archivo `i18n.mjs` | exit 0, resuelve a `i18n.mjs` |
| `python scripts/validate_collaboration_state.py` con secretos | exit 0 |
| `python scripts/validate_collaboration_state.py` en clon protocolo sin secretos `2d4802a` | exit 0 |
| `python runtime/protocol_replay.py --check-drift` | exit 0 |
| Drift por API | `has_drift=False`, `up_to_seq=2426` antes del claim de esta entrega |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| `git diff --exit-code -- protocol.config.json` | exit 0 |
| `Get-FileHash protocol.config.json -Algorithm SHA256` | `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Tabla vector por vector

| Vector | Resultado | Evidencia falsable |
| --- | --- | --- |
| Regresion original `../lib/I18N` | PASA | El test permanente `case-variant Windows import` produce violacion. |
| Regresion original `../lib/i18n?raw` | PASA | El test permanente `query-suffixed import` produce violacion. |
| Mezcla `../lib/I18N?raw` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Trailing slash `../lib/i18n/` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Double slash `../lib//i18n` | PASA | Probe temporal Analista devuelve 1 violacion por `path.posix.normalize`. |
| Dot segment `../lib/./i18n` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Index implicito `../lib/i18n/index` | PASA | Probe temporal Analista devuelve 1 violacion por prefijo `src/lib/i18n/`. |
| Alias `@/lib/i18n` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Absoluto `src/lib/i18n` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Dynamic import `import('../lib/I18N?raw')` | PASA | Probe temporal Analista devuelve 1 violacion. |
| CommonJS `require('../lib/I18N?raw')` | PASA | Probe temporal Analista devuelve 1 violacion. |
| Percent-encoded segment `../lib/%69%31%38%6e` | SLIPS | `collectGovernanceWaiverViolations` devuelve `[]`; guard no decodifica `%69%31%38%6e` antes de comparar con `src/lib/i18n`. |
| Percent-encoded explicit extension `../lib/%69%31%38%6e.ts` | SLIPS | `collectGovernanceWaiverViolations` devuelve `[]`; native ESM prueba que percent-encoded path segments can resolve to the decoded module name. |

## Hallazgo bloqueante

El fix de `52f0d5e` sostiene los dos slips previos, pero la familia de percent-encoding pedida por la
instruccion sigue abierta. El guard aplica `replace(/[?#].*$/, '')`, `path.posix.normalize` y `toLowerCase`,
pero nunca decodifica segmentos percent-encoded antes de resolver/comparar. Resultado falsable: un source de
panel con `import '../lib/%69%31%38%6e.ts'` no genera violacion aunque el segmento decodifica a `i18n.ts`.

La prueba nativa ESM fuera del producto confirma que el patron no es solo texto muerto:
`import './%69%31%38%6e.mjs'` carga el archivo `i18n.mjs` con exit 0. Bajo criterio adversarial y "default a no
cerrable si dudas", no doy cierre con esa familia sin control permanente o waiver explicito.

## Residuales

- No encontre nuevo escape en case+query, slash, dot-segment, index, alias, `src/`, dynamic import ni require.
- Percent-encoding debe resolverse con decodificacion controlada de specifier/path antes de comparar, o con una
prueba de resolucion del bundler que demuestre que la superficie no es importable en este producto.

## Cierre

REFUTADO. Devolver a Codex para hardening percent-encoding del waiver guard y regresion negativa permanente.
