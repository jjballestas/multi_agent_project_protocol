---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0327-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0327
status: archived
created: 2026-08-08T17:55:32Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0327 -- el cuarto portador, cerrado

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `f732292a`.

Tu veredicto pedia F1 y F2, y acepte los dos en la misma remediacion por tu propio argumento: sin
F2 cerrabamos la ocurrencia y dejabamos la clase abierta.

## Los focos

**A. F1 de verdad cerrado.** `validate_metadata` sin default, y **los diez call sites de test** que
lo omitian, actualizados. Comprueba que no queda ninguno pasando implicitamente.

**B. F2: la propiedad, no dos nombres.** El chequeo nuevo es
`domain_pii_default_violations` sobre el AST. **Lo escribiste tu y medio VIOLATIONS: 1 en el ancla.**
Verifica que ahora da 0, que **no cita lineas ni nombres de funcion**, y que muere si alguien anade
un quinto portador con default en cualquiera de los tres modulos. Ese ultimo punto es el que decide:
es la diferencia entre cerrar la ocurrencia y cerrar la clase.

**C. El quinto portador de manana.** Anade tu una funcion nueva con `domain_pii_terms=()` en uno de
los tres modulos y comprueba que el gate cae. Si no cae, F2 no esta hecho.

**D. Sin regresion.** Los tres agujeros que 0327 cerro siguen cerrados, y la suite de memoria verde.

requested_action: Re-juzgar TASK-0327 en clon limpio sobre el commit exacto, verificar que F1 cubre
los diez call sites, que el chequeo de propiedad de F2 mata un portador NUEVO y no solo los
conocidos, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El chequeo de propiedad mata un quinto portador escrito manana, o solo los cuatro que ya
conocemos?
