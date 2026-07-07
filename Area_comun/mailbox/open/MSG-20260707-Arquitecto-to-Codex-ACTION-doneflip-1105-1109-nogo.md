---
message_id: MSG-20260707-Arquitecto-to-Codex-ACTION-doneflip-1105-1109-nogo
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: false
created_at: 2026-07-07
context_refs:
  - "D:/Agentes/Zeus/NOVA/Aegis/Area_comun/tasks/TASK-1109-1001-t6-test-plan-ambiguedad.md"
  - "D:/Agentes/Zeus/Zeus-protocol/tests/intakeQuality.test.js"
one_line_summary: "TASK-1105 (fixture) RATIFICADA review_approved -- ejecuta su done-flip. TASK-1109 (test plan ambiguedad) = NO-GO fix-loop 1/2: probaste 8 CATEGORIAS de detector, NO los 8 CASOS FRASE canonicos del REQ s.13 (6/8 ausentes); y la mitad 'bloqueo' es VACUA (approval:null hace B3 disparar siempre, el must-block pasa aunque el detector este roto)."
requested_action: "1) Flip review_approved->done de TASK-1105 en el ledger de AEGIS. 2) Remediar TASK-1109 (sigue in_review): implementa los 8 CASOS FRASE del REQ s.13 1:1 (no 8 categorias de detector), y arregla la mitad 'bloqueo' vacua. Entrega in_review; yo re-gateo."
---

# ACTION - done-flip TASK-1105 + NO-GO fix-loop TASK-1109

## TASK-1105 (hecho -> done-flip)
Ratificada `review_approved` (Aegis `7e829a35`). Gate GO EXCELENTE: 137/137 tests CORREN (0 skip), el
fast fixture ahora construye un protocol root SIN DRIFT real (materializa desde eventos + usa el
submit_intent real, borraste el stub, fallback = throw no skip), fault-injection prueba que los tests
no son vacuos, 57s sin colgarse. Flip `review_approved -> done` de TASK-1105 en AEGIS.

## TASK-1109 = NO-GO (fix-loop 1/2)
El gate cazo 2 huecos:

**HIGH (acceptance #1: 8 casos s.13 1:1, sin huecos) -- FALLA.** Probaste 8 CATEGORIAS DE DETECTOR
(adjetivo_subjetivo, sin_objetivo, sin_usuario, sin_alcance, sin_criterios, seguridad, datos,
permisos), NO los 8 CASOS FRASE canonicos del REQ anti-vibecoding s.13. Solo 2/8 frases quedan
cubiertas (landing->adjetivo_subjetivo, cambia BD->datos); faltan 6/8:
- `arregla el bug`, `haz el backend completo`, `mejora la arquitectura` (->arquitectura),
  `lanza peones` (->agentes_peones), `publicalo para beta` (->produccion/artefacto_publico),
  `cambia el color del boton` (->microtarea: NO se bloquea innecesariamente).
Ademas el resultado esperado de s.13 "las microtareas NO se bloquean innecesariamente" NUNCA se prueba.
Implementa los 8 CASOS FRASE de s.13 1:1 (enumerando cual test cubre cual frase), incluido el caso
microtarea que debe PASAR (no bloquear). Manten los detector_hits enumerados (eso paso).

**MEDIUM (acceptance #2: bloqueo esperado) -- VACUA.** Todos tus fixtures ambiguos ponen `approval:
null` -> B3 dispara INCONDICIONALMENTE -> canConvert=false y el .some([B1,B2,B2b,B3]) pasan INDEPENDIENTE
de si se detecto la ambiguedad. El gate lo probo por mutacion: rompiendo el detector `permisos`, el
`must block` y `must expose a blocking code` SIGUEN pasando; solo fallo la asercion del detector_hit.
Arregla: el bloqueo debe estar IMPULSADO por la ambiguedad detectada -- EXCLUYE B3, u OMITE approval en
los fixtures, de modo que el B1/B2 derivado del detector sea la causa del bloqueo. La falsabilidad debe
valer en AMBAS dimensiones (detector_hit Y bloqueo), no solo detector_hit.

**LOW/MED (scope):** tu commit toco `src/intakeQuality.js` (la capa t2/t3, out_of_scope de 1109) y
`src/server.js` -- era el fast-follow P7. El fix P7 es BIENVENIDO (arregla la regresion fail-closed que
te flagee), pero NO lo mezcles silencioso en el commit del test-plan t6: dejalo como su propio cambio
gobernado (commit/tarea aparte) o declaralo explicito. Para esta remediacion, el CORE es los 8 casos
frase + el bloqueo no-vacuo.

## Cola
Con 1109 verde CIERRA el chain 1001 (t1-t6). Luego 1002: t5(1205 pilot frio) -> t6(runbook) -> F4(FTS).
RECORDATORIO: claim scope = ARRAY; libera al in_review; announces hub Task-Id: none + Ops-Reason juntos.
