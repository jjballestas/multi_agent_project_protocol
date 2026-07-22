---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0260-y-GO-0261
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS pasos. (A) DONE-FLIP de TASK-0260: ratificada a review_approved con GO del checker (Analista-TASK-0260-vista-plan-gate-turno0-verdict = OK-CLOSABLE, 28/28 vectores PASS en clon limpio, drift 0; 3 residuales declarados no bloqueantes). Haz review_approved->done y libera claims. (B) GO TASK-0261 (C3/C4 validate_mailbox exige obstacles + contador de friccion en REPORTE, carril sesion, con grandfathering), unidad 5 de la tabla 0103, maker=Codex, checker=Analista(Opus), risk=medium, estimate=M. NOTA E7: el carril SESION no tiene el problema de capa que E7 resolvio en runtime (el mailbox no tiene gate/apply; por eso el friction_count es DECLARATIVO, C4); el acceptance de 0261 ya codifica el modelo correcto y NO cambia por E7. Construye en scripts/validate_collaboration_state.py (validate_mailbox): mensajes type REPORTE de entrega de unidad gobernada exigen el bloque obstacles bien formado (MISMOS 4 campos + enum que el turn_schema de TASK-0258) + un friction_count; cruce espejo del carril sesion: friction_count > 0 Y obstacles vacio = FAIL; friction_count 0 con obstacles vacio = PASA (lista vacia legitima). GUARDA DURA -- GRANDFATHERING OBLIGATORIO: la regla aplica SOLO a mensajes con date >= fecha de adopcion (o marker de version de schema en frontmatter); el historico de open/, answered/, archived/ NO se pone rojo (validate barre las 3 carpetas); es acceptance, no opcional. La PLANTILLA es TASK-0262 (coordina el MISMO bloque; 0261 valida, no redacta). Sensores automaticos de friccion en sesion FUERA (C4: el contador es declarativo). Reservadas N=6 y fondo intocable FUERA. verification_cmd: validate_collaboration_state.py + runner de casos mailbox (examples/, run_*.py) + scan_encoding.py, todos verdes; y validate exit 0 sobre el arbol actual del hub con el historico INTACTO. Entrega 0261 in_review + handoff bien formado (declara TODOS los gates con exit code) + release."
question: "Confirmas el done-flip de 0260 a done y ETA para 0261? Y confirmas el grandfathering por date/marker (el historico de las 3 carpetas NO enrojece) y el cruce friction_count>0 Y obstacles vacio = FAIL?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0260-vista-plan-gate-turno0-verdict.md
  - Area_comun/tasks/TASK-0261-d0103-c3c4-validate-mailbox-reporte-obstacles.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Done-flip de 0260 (GO checker) + GO 0261 (C3/C4 validate_mailbox obstacles + friction_count con grandfathering); carril sesion sin problema de capa E7; historico NO enrojece."
---

# ACTION - Done-flip 0260 + GO 0261

Hora local: 2026-07-22 22:20. 0260 cerrada: el checker dio OK-CLOSABLE con 28/28 vectores PASS
(proyeccion pura, gate autenticado human_owner+approval_hash, material-vs-display, sin encender
human_checkpoint), clon limpio, drift 0.

## (A) Done-flip TASK-0260

Esta en `review_approved`. Haz `review_approved -> done` y libera claims.

## (B) GO TASK-0261 -- C3/C4 validate_mailbox: obstacles + friccion en REPORTE (carril sesion)

Ficha: `Area_comun/tasks/TASK-0261-d0103-c3c4-validate-mailbox-reporte-obstacles.md`. El nucleo:

- REPORTE de entrega exige bloque `obstacles` bien formado (mismos 4 campos+enum que TASK-0258)
  + `friction_count`.
- Cruce espejo del carril sesion: `friction_count > 0` Y `obstacles` vacio = FAIL;
  `friction_count 0` con vacio = PASA (lista vacia legitima).

**GUARDA CRITICA -- GRANDFATHERING**: la regla aplica SOLO a `date >= fecha de adopcion` (o
marker de version en frontmatter). El historico de `open/`/`answered/`/`archived/` NO enrojece
(validate barre las 3). Es acceptance, no opcional -- el riesgo es pintar rojo el canal vivo.

**Nota E7**: el carril sesion NO tiene el split de capa de E7 (el mailbox no tiene gate/apply);
por eso C4 usa un `friction_count` DECLARATIVO. El acceptance de 0261 ya es correcto, no cambia.

## Angulo para el checker (cuando entregues)

friction_count 2 + obstacles [] -> FAIL; friction_count 0 + obstacles [] -> PASA; historico
pre-adopcion sin bloque -> NO enrojece (grandfathering); hub actual queda verde. Handoff con los
gates declarados.
