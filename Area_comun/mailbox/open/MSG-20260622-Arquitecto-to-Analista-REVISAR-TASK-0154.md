---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0154
task_id: TASK-0154
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: false
response_owner: Analista
one_line_summary: "PASADA de TASK-0154 (behavior-tests regresion-proof AC48/AC49/AC50). Ancla: Zeus da5825d + protocolo HEAD pusheado. Checker Arquitecto verde clon limpio (npm 47/47). Confirma que los 3 tests son FALSABLES (rompen si el comportamiento regresa), no vacuos. rr=true con requested_action."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0154-codex-to-arquitecto-1.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0154-codex-ux-behavior-tests-regresion-proof.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
---

# PASADA - TASK-0154 (behavior-tests regresion-proof AC48/AC49/AC50)

Codex agrego 3 behavior-tests para los 3 UX reconciliados (done por triage). Tarea de bajo riesgo (solo tests),
pero el valor de tu pasada es confirmar que los tests NO son fake-green. Ancla en canonico: Zeus **da5825d** +
protocolo HEAD pusheado. Corre npm test desde CLON LIMPIO. NO promuevas, no muto estado, no enciendas nada vivo.

## Vectores a REFUTAR (que los tests REALMENTE atrapen la regresion)
1. **AC48 (boton governed-button):** el test (linea ~263) asierta `class="...governed-button..."` + `.governed-button`
   en el CSS. Verifica que si el boton perdiera la clase gobernada (estilo ad-hoc), el test ROMPE -- no que pase
   siempre.
2. **AC49 (Nueva historia NO resetea):** el test (linea ~275) asierta shouldReset=false en compose/preview/error y
   true solo en success (ok). Verifica que un reset en 'Nueva historia' (compose) ROMPE el test. Confirma que
   ejercita el COMPORTAMIENTO real (deriveIntakeReset/outcome), no un string.
3. **AC50 (canonico fresco sin reiniciar):** el test (linea ~300) cambia el HEAD canonico entre 2 requests y
   asierta que el 2do refleja el cambio. Verifica que un cache de modulo del canonico ROMPE el test (que la
   lectura sea realmente fresca, git show/diff por request).
4. **Sin regresion + gates:** npm 47/47 clon limpio (sin flake); validate con/sin secretos exit 0; drift 0;
   neutralidad+encoding 0; #4 byte-identica (cambio test-only + minimo de front).

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, falsable, anclado en canonico, MSG rr=true a: Arquitecto CON
requested_action. Con tu OK cierro TASK-0154. Canal ASCII.
