---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0267-hook-v2
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0267 (hook v2 por materializacion del indice) en CLON LIMPIO de HEAD (7c98fd4), contra su acceptance ampliado post-O1. Veredicto GO / NO-GO por mailbox. SIN PRODUCTO EN ALCANCE (solo hub). El COSTE medido (51.5-53.3s) NO es criterio de NO-GO unilateral: esa decision la reservo el Operador; reporta tu propia medicion y pondera solo la CORRECCION."
question: "GO o NO-GO de TASK-0267 en correccion, y cual es tu medicion independiente del coste?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0267-d0103-h2-hook-snapshot-checkout-temporal.md
  - Area_comun/handoffs/HANDOFF-TASK-0267-Codex-to-Arquitecto.md
  - Area_comun/artifacts/ANALISTA-TASK-0257-gate-propio-E2-rejuicio-final-iter2-veredicto.md
one_line_summary: "REVIEW TASK-0267 (hook v2, materializacion del indice): verificar que mata el mutex H2 + toda la familia selector (incl. tu rename R100) + arnes de negativos real + CI existencia/hash + limite C1 declarado. Coste 51.5-53.3s medido: reportar, no vetar (decision reservada del Operador). Este veredicto destraba el cierre de 0257 y la apertura de 0258."
---

# REVIEW TASK-0267 - hook v2 por materializacion del indice

Hora local: 2026-07-20 01:57. TASK-0267 in_review con claims liberados (nucleo b583090,
cierre completado en 7c98fd4; nota: el exec del maker salio sin su commit final y el
Arquitecto completo el snapshot consistente -- verificalo como parte del clon limpio).
ALCANCE: solo hub.

## Que verificar (acceptance ampliado post-O1 en el .md; vinculante)

1. NUCLEO: el hook materializa el INDICE en temporal y corre alli el validador; la
   exigencia de arbol limpio DESAPARECE. Prueba de concurrencia: unstaged AJENO en
   Area_comun/ + commit propio limpio = PASA; estado staged roto = FALLA; mutacion
   unstaged del validador = veredicto NO cambia.
2. TU FAMILIA DE ESCAPES: el rename R100 de scripts/validate_collaboration_state.py
   hacia fuera (tu repro exacto del veredicto final de 0257) ahora FALLA; negativo
   permanente presente. Borrados de validador/runtime/estado siguen cubiertos.
3. ARNES REAL: los negativos invocan el flujo de git commit real (no sh del hook); tu
   hallazgo del falso-pasa (archivo-inexistente confundido con rechazo) esta cerrado.
4. C2: paso de CI en .github/workflows/validate.yml verifica existencia + SHA-256 de
   .githooks/pre-commit y el hash pineado corresponde al hook v2 de ESTA entrega.
5. LIMITE C1 declarado en handoff y doc: el borrado del propio hook en local NO esta
   cubierto (residual estructural de 0257); solo CI/diffs lo detectan.
6. Limpieza robusta del temporal (sin residuos, incluso en fallo) + espejo
   born-operational + regresion de los vectores PASA de 0257 (arming, export, desarme).
7. COSTE: el maker midio 53.251s frio / 51.487s caliente. REPORTA tu medicion
   independiente (frio/caliente) como dato; NO es criterio de NO-GO por si solo -- el
   Operador reservo la decision del reparto acotado/completo y decidira con tu cifra.

Si GO: ratifico, y el cierre de 0257 (con residuales declarados) + apertura de 0258
siguen en cadena. Si NO-GO en correccion: hallazgos con file:line + repro; el fix-loop
de esta unidad tiene su tope estandar de 2 iteraciones.

Pendiente tuyo aparte (sin urgencia, no bloquea esta review): la confirmacion de la
correccion de tu plantilla de trailers (REQUEST del 19-jul sigue abierta).

## Guardas

Reservadas N=6 intactas; fondo intocable (2E35F26E / epoch 1.14.0 / N=500);
checker-only; sin encender supervised_autonomy ni real_invoker.
