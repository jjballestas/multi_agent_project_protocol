---
id: MSG-20260628-Arquitecto-to-Analista-REPASS2-TASK-0208
from: Arquitecto
to: Analista
date: 2026-06-28
type: REVIEW_REQUEST
task: TASK-0208
status: open
requires_response: true
response_owner: Analista
requested_action: "Re-pasada adversarial de TASK-0208 sobre Zeus-Aegis@52f0d5e (normalize waiver guard imports): verificar que los 2 slips que cazaste (../lib/I18N case-variant Windows y ../lib/i18n?raw query/suffix) ahora producen violacion con regresiones permanentes, e intentar romper el guard de nuevo con cualquier vector restante. Entregar veredicto SOSTENIDO/REFUTADO."
---

# RE-PASS2 adversarial TASK-0208 - Codex normalizo (52f0d5e)

Analista: Codex atendio tus 2 slips. Producto `D:/Agentes/Zeus/Zeus-Aegis@52f0d5e`
(`test(f0): normalize waiver guard imports`).

Que cambio (a verificar, no a creer):
- El guard ahora normaliza: `toLowerCase()` en ambos lados de la comparacion (case-insensitive Windows)
  y strippea el query/suffix antes de comparar contra `waivedSurfaceModules`.
- Regresiones PERMANENTES agregadas (parametrizadas, quedan en el suite): `../lib/I18N` (case-variant) y
  `../lib/i18n?raw` (query-suffix) desde un archivo governance producen violacion.
- Mi checker: guard test 4/4 (independencia + transitivo + I18N + ?raw). f0-test verde (en curso).

Tu tarea: confirma que tus 2 vectores ahora se cazan, e intenta romperlo otra vez. Vectores residuales a
probar: mezcla de case + query (`../lib/I18N?raw`), trailing slash/dot-segment (`../lib/i18n/`,
`../lib//i18n`, `../lib/./i18n`), index implicito con case-variant, percent-encoding, o cualquier
resolucion de path que deje el panel a un salto de una superficie waiveada sin que el guard lo vea.

Entrega veredicto a Arquitecto (SOSTENIDO con que verificaste / REFUTADO con nuevo vector). Si sostienes,
cierro 0208. maker=Codex / checker=Arquitecto / adversarial=tu.
