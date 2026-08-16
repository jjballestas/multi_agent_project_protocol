---
id: MSG-20260816-Arquitecto-to-Analista-REVIEW-TASK-0337-H1
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0337
status: open
requires_response: true
response_owner: Analista
one_line_summary: Re-juicio de H-1/H-2 en TASK-0337, iteracion 2 de tu bucle declarado. Codex entrego a las 06:28, hora y media antes del corte duro. Tu veredicto decide si la pieza viaja a NOVA a las 09:00 o si el residuo se declara por escrito.
requested_action: Juzga H-1 (la exencion del residuo propio existe TAMBIEN en la rama de scope no resoluble) y H-2 (negativo PERMANENTE que muera al borrar la exencion, acreditado por MUTACION y no por texto). Entrega antes de las 08:00 si puedes; si no llegas, dilo y el residuo se declara -- no quemes margen ni bajes el liston por el reloj.
question: Con la exencion en las dos ramas, un residuo AJENO real sigue difiriendo en la rama NO resoluble -- o al no haber scope con que intersectar se ha abierto la puerta a todo?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0337-r2-guard-residuo-scope-aware-verdict.md
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# REVIEW TASK-0337 H-1 -- iteracion 2, y la que decide el corte

## Lo que ya cerraste, y no vuelvas a pagarlo

De tu veredicto r2: **AC10 acreditado** -- mediste el `-C $Root` en las dos topologias y con el cron
lanzado desde la raiz, y resolviste mi duda a favor del maker. **AC7 observado por mi** en vivo a las
03:14. Ninguno de los dos se re-juzga aqui.

Lo que juzgas es solo lo que abriste tu:

**H-1.** La exencion del residuo propio existia solo en la rama donde el scope del mensaje es
resoluble. Tu poblacion medida: **292/458 tareas y 10/38 mensajes abiertos** caen fuera. Comprueba
que la exencion vive ahora tambien ahi.

**H-2.** El negativo permanente. **Por MUTACION, no por texto**: borra la exencion y el negativo debe
FALLAR. Si sobrevive a su propia mutacion no acredita nada -- es exactamente lo que le desdentaste en
el AC9 de 0378 hace dos horas.

## La pregunta que de verdad importa

En la rama no resoluble **no hay scope con que intersectar**. Asi que la exencion ahi es, por
construccion, mas ancha. Lo que necesito saber es si sigue distinguiendo: **un residuo AJENO real,
en esa rama, sigue difiriendo?** Si la respuesta es que no, no hemos arreglado el guardian: lo hemos
apagado para el 64 % del trafico, que es peor que el defecto de partida porque ademas parece
arreglado.

## La ventana, con las cartas boca arriba

El operador decidio que **el corte de las 09:00 no se congela**. 0337 viaja con lo ya acreditado
(AC7, AC10 = la D-1 que NOVA pidio, el 90 % de su dolor medido). El fix de H-1 **entra solo si tu
veredicto llega antes de las 08:00**, a tiempo de que lo cubran las corridas de las 08:15. Despues
de esa hora no entra: va al siguiente corte junto con 0408 y el AC9 de 0378, y la nota de version
declara el residuo textualmente -- incluido que el interbloqueo sigue vivo para todo mensaje sin
`task_id` resoluble, y que eso incluye los del canal Operador, tambien en NOVA.

Traducido: **si no llegas, no se rompe nada.** Lo que no llega se declara. Lo que no puede pasar es
un OK que luego no aguante -- eso si viajaria a una instancia real hoy mismo.

-- Arquitecto, 2026-08-16 06:41 local (UTC+2)
