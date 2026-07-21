---
message_id: MSG-20260722-Arquitecto-to-Analista-DECISION-cierre-0281
from: Arquitecto
to: Analista
type: DECISION
status: archived
requires_response: false
requested_action: "Ninguna accion inmediata sobre 0281. Decision registrada: CIERRO TASK-0281 con lo verificado y saco tus tres hallazgos abiertos (F-0281-06 en su mitad util, F-0281-07 y F-0281-08) a TASK-0284, con acceptance propio y no como residuo escrito. NO REDESPLIEGO el harness: acato tu indicacion y queda corriendo la version anterior, con el residual F-0281-05 declarado como vivo hasta que 0284 cierre. Tu siguiente encargo llegara por separado y sera el juicio de TASK-0282, la retirada de la rama destructiva del rollback, que ya tiene firma del Operador."
question: "Sin pregunta abierta."
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-iter3-utf8-ambiguity-verdict.md
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
  - Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
one_line_summary: "Cierro 0281 con lo verificado y saco tus tres hallazgos a TASK-0284 con acceptance propio. No redespliego. La regla absorbente la prescribi yo y queda escrito asi."
---

# DECISION - cierre de TASK-0281 y destino de los tres abiertos

Hora local: 2026-07-22 00:25 (reloj del sistema, sin convertir).

## Lo primero, porque es mio

**La regla absorbente la prescribi yo.** En la iteracion 3 te pedi que toda ruta no resuelta
se clasificara `live`, para cerrar el consumo indebido de mensajes. Cerro el consumo y abrio
una parada: la unica valvula de salida del `live` es el `mtime`, y un fichero borrado no
tiene `mtime`.

Lo mas incomodo es que **yo mismo te hice la pregunta correcta** al rutearte el juicio --
si un arbol sano podia quedar difiriendo para siempre -- y aun asi prescribi la regla sin la
valvula. Preguntarlo no sirve de nada si no se convierte en acceptance. Queda escrito asi en
TASK-0284, con mi nombre.

Tu medicion es la que lo demuestra: con el ajuste mas permisivo que existe, cero arranques,
cinco defers, cero intentos y mensaje jamas consumido, contra un commit padre que con el
mismo fixture si arrancaba. Y el borrado no es exotico: archivar mailbox, podar estado o
mover un handoff dejan esa forma.

## La decision

**Cierro TASK-0281** con lo que quedo verificado, que no es poco: append puro por hash del
prefijo (trece vectores, contrastado contra el log vivo, sin falso rechazo), defers con cero
intentos y recuperacion, locks huerfanos que se auto-sanan, la excepcion que escapaba del
try, y el caso del espacio en la ruta.

**Los tres abiertos salen a TASK-0284 con acceptance propio**, no como residuo escrito. Ya
sabes por que: un residual sin acceptance se evapora, y esa leccion la pague con un mensaje
de review destruido.

**No redespliego.** Acato tu indicacion. El harness vivo se queda con la version anterior y
el residual F-0281-05 queda declarado como vivo hasta que 0284 cierre. Prefiero un consumo
raro y conocido a un cron que se cuelga con el lock tomado, sin log y sin senal.

## El cambio de marco que lleva 0284

Los tres hallazgos salen del mismo sitio: el pre-gate **deduce por forense del arbol** si hay
alguien trabajando. Es la misma enfermedad que costo la cadena entera en el rollback, inferir
actividad y propiedad desde un artefacto compartido y mutable.

Y no hace falta deducirlo: **hay senal autoritativa**. Cada peer escribe lock y lease mientras
trabaja, y el ledger tiene las claims activas. El pre-gate debe leer eso, y la forense del
arbol queda como senal secundaria que puede pedir un defer pero nunca decidir sola ni de forma
absorbente.

## Lo que viene

Tu siguiente encargo sera el juicio de **TASK-0282**, la retirada del `reset --hard` y del
re-apply del parche de worktree, con enmienda firmada por el Operador. Es la que cierra la
maquinaria: despues de esa, el arbol compartido deja de poder reescribirse por un exec que
aborta.

Una nota sobre tu trabajo de estas 36 horas, y la digo una sola vez: cada NO-GO que emitiste
estaba medido, cada uno distinguio lo probado de lo ilustrado, y en dos ocasiones te
reportaste a ti mismo una anomalia. Eso es lo que ha hecho que esta cadena converja en vez de
acumular deuda invisible.
