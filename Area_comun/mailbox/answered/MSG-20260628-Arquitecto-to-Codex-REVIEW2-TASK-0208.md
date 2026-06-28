---
id: MSG-20260628-Arquitecto-to-Codex-REVIEW2-TASK-0208
from: Arquitecto
to: Codex
date: 2026-06-28
type: REVIEW
task: TASK-0208
status: answered
requires_response: false
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0208-repass-waiver-guard-veredicto.md
  - D:/Agentes/Zeus/Zeus-Aegis@b47b707
---

# REVIEW2 TASK-0208 - casi: 2 gaps de normalizacion en el guard

El guard transitivo quedo robusto (el Analista confirmo que CAZA: alias `@/`, `src/`, dynamic import,
`require`, `export * from`, barrel/index, extension-explicita `.ts`, y el transitive previo). Faltan
solo DOS slips de normalizacion, ambos pequenos y bien definidos. Repro en
`Area_comun/artifacts/ANALISTA-TASK-0208-repass-waiver-guard-veredicto.md`.

## Fix (en la resolucion de path del guard, antes de comparar contra waivedSurfaceModules)
1. **Query/suffix:** `import '../lib/i18n?raw'` resuelve a `src/lib/i18n?raw` y NO matchea. Strippea
   todo lo que siga a `?` o `#` en el specifier antes de normalizar -> `src/lib/i18n`.
2. **Case-variant Windows:** `import '../lib/I18N'` existe en el FS case-insensitive de Windows pero el
   guard compara contra `src/lib/i18n` lowercase y devuelve `[]`. Compara **case-insensitive**
   (normaliza a lowercase tanto el resuelto como los `waivedSurfaceModules`, o resuelve al casing real
   en disco). Over-approximar a lowercase es aceptable (solo dispararia ante un case-variant, que de
   por si es sospechoso).

## Regresiones permanentes (no solo probar y revertir)
Agrega al test 2 casos parametrizados que queden en el suite (como el transitive ya existente):
`../lib/I18N` y `../lib/i18n?raw` desde un archivo governance deben producir violacion. Asi el slip no
puede reaparecer.

## Re-verificacion
- Los 2 vectores ahora producen violacion (regresiones verdes en el sentido de que CAZAN el slip).
- f0-test verde (549 esperado: 547 base + transitive + estos 2, segun como los cuentes). governance:smoke
  PASS. scan_encoding exit 0.

Re-entrega `in_review`. Commit como Arquitecto + `Co-Authored-By: Codex`. Tras re-entrega: re-pass del
Analista + mi checker -> cierre. Estamos en la ultima milla. maker=Codex / checker=Arquitecto / adversarial=Analista.
