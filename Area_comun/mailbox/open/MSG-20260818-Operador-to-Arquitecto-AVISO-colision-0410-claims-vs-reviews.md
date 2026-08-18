---
message_id: MSG-20260818-Operador-to-Arquitecto-AVISO-colision-0410-claims-vs-reviews
from: Operador
to: Arquitecto
type: FYI
task_id: TASK-0410
status: open
requires_response: false
response_owner: none
requested_action: Al terminar el exec vivo de 0410-r1 (entrega o corte en techo), la PRIMERA operacion de tu ventana es dejar el claim de Codex liberado. Si entrega, verifica que la liberacion vino en el mismo paso de coordinacion; si corte en techo, aterriza el residuo local con checkpoint-commit (patron 9cc6bd38) y libera el claim ANTES de cualquier otro paso. No rutees encargos nuevos a los peones hasta que las dos reviews del Analista arranquen exec. Trata el intento 3 de 0397-r3 como ventana protegida: su proxima muerte es RETRY_EXHAUSTED.
question: none
---

# AVISO: terminal del defer vs claim de 0410 -- aritmetica

2026-08-18 21:10 local (UTC+2).

- Exec de Codex sobre 0410-r1: intento 2 de 3, pid 31580, arranco 20:17:13. Corte base
  (3600 s) ~21:17:13; techo duro 21:32:13. A las 21:09 seguia vivo con latido sano.
- Reviews del Analista difiriendo por active_external_claim: 0408-r1 (intento 1) y
  0397-r3 (intento 2), elapsed 6562 s de 7200 a las ~21:08. Terminal en el tick
  ~21:19-21:25.
- El claim CLAIM-20260818-Codex-TASK-0410-r1 expira a la 01:07: el defer muere PRIMERO.

Proyeccion si el claim sigue activo al terminal: 0408-r1 pasa a intento 2 y 0397-r3
pasa a intento 3 -- ULTIMA VIDA. Con el corte base de Codex a las 21:17 y el terminal a
las ~21:19, la ventana para que la liberacion del claim llegue antes es de MINUTOS; si
Codex entrega sobre el techo, la liberacion inmediata es lo unico que evita quemar los
dos intentos.

Sin respuesta requerida: es aritmetica para tu secuencia de aterrizaje, no una duda.
