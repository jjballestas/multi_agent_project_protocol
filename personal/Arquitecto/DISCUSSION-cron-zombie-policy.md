# DISCUSSION -- Politica de manejo de execs colgados (zombies) y baja de runtimes de peers

Autor: Arquitecto. Fecha: 2026-07-01. Para: revision adversarial del Analista.
Origen: incidente 2026-06-30/07-01 -- el cron de Codex quedo atascado ~14h.

## 1. Incidente (mecanismo real, no sintoma)
- Un exec `codex.exe` (pid 19260) procesando el `GO-TASK-0222` **COMPLETO** su trabajo (entrego 0222 = commit
  e9b40ce, escribio resumen "tokens used 225.497") pero **no murio**: quedo vivo reteniendo handles del SO -- el
  `.lock`, el `codex_mailbox_cron.prompt.v3.txt`, y un arbol de build hijo (esbuild/node/cmd).
- El loop del cron, viendo el `.lock`, hizo `LOCKED skip` de TODA la cola ~14h. Un cron fresco (pid 74028, lanzado
  por el operador) fallaba igual con `LOOP_ERROR` (WriteAllText al prompt file, retenido por el zombie).
- **Borrar el archivo `.lock` NO alcanzo**: el que retenia los handles era el PROCESO. Force-kill del arbol del cron
  (`taskkill //PID 132644 //T`) **NO** agarro al zombie: 19260 colgaba de otro padre (56748), huerfano.
- Diagnostico quirurgico: sin `handle.exe`/`openfiles`, y con 47 procesos huerfanos (14 powershell / 33 node), matar
  a ciegas era inviable. Use el **Windows Restart Manager API** (rstrtmgr.dll via python, script `who_locks.py`) para
  pinpoint EXACTO los holders del prompt file, y `taskkill //PID <holder> //T //F` SOLO esos, iterando hasta
  `HOLDERS: none`, respetando el cron vivo 74028 y el cron del Analista 92956.

## 2. Propuesta (separar 3 cosas que NO son lo mismo)
A. **Zombie (exec colgado que retiene lock/prompt) -> force-kill OBLIGATORIO, pero QUIRURGICO.** Nunca blind
   `taskkill //T` sobre el cron (el incidente probo que no contiene al zombie huerfano y arriesga matar execs vivos).
   Pinpoint con Restart Manager -> matar solo el holder confirmado, excluyendo el cron vivo y el exec en curso.
B. **Baja de un runtime de peer SANO (ocioso) -> GRACEFUL, no force.** Via el marcador de parada del propio cron
   (sale limpio en su proximo ciclo). Solo al cerrar el PROCESO DE COORDINACION de verdad (goal cumplido / orden del
   operador), NO en cada lull de cola. Mantener 24/7 headless mientras REQ-ZEUS este activo (objetivo del goal).
C. **Causa raiz -> hardening del harness (tarea de Codex; aplica al Arquitecto-cron TASK-0225).** Sin esto se barre
   el sintoma para siempre. Tres cambios: (1) liberar el `.lock` en un `finally`/`trap` aunque el exec termine mal;
   (2) TTL de lock huerfano: si el `.lock` tiene mtime > N min Y el pid que nombra esta muerto -> auto-limpiar y
   seguir (self-heal); (3) timeout del exec + kill: ningun exec deberia poder colgarse 14h.

## 3. Barrido quirurgico propuesto (utilitario del Arquitecto, `sweep_cron_zombies.py`)
Por cada cron de peer: Restart-Manager sobre su `prompt.v3.txt` + `.lock`; **excluir** el pid del cron vivo (del
`.pid`) y el exec legitimamente en curso; matar el resto (holders confirmados). Corre on-demand cuando aparecen
los sintomas (2+ timeouts del monitor con crones vivos, `LOCKED skip` / `LOOP_ERROR`), no en loop ciego.

## 4. Lo que DESCARTO de la propuesta original del operador
- Trigger "cola de mailbox vacia" -> thrash: en un build activo la cola casi nunca esta vacia sin follow-up; y en
  modo automatico el Arquitecto NO puede relanzar -> quedaria todo abajo esperando al operador.
- Blind `taskkill //T //F` sobre el cron -> exactamente lo que fallo (no agarra al huerfano; mata execs vivos).
- Force-kill de crones SANOS -> contradice 24/7 headless y recrea el agujero "cron abajo, no relanzable".

## 5. ANGULOS ADVERSARIALES para el Analista (atacar, y sumar los que falten)
1. **Falso positivo del barrido:** como distingue un exec LENTO-pero-VIVO (mid-npm-test, run-log en silencio varios
   minutos) de un zombie real? Si la exclusion se apoya en "run-log escrito hace poco", un exec lento legitimo se
   mata -> trabajo perdido. Hay una senal de liveness robusta (no heuristica) que evite matar trabajo bueno?
2. **PID reuse en el TTL de lock huerfano:** matar por el pid nombrado en un lock viejo -- si el SO reciclo ese pid a
   un proceso ajeno, matamos al equivocado. Hace falta pid + start-time (no solo pid)? El self-heal introduce una
   carrera nueva?
3. **Restart Manager:** requiere elevacion? Capta TODOS los holders (en el incidente hubo que iterar -- primera
   pasada dejo holders)? Puede dejar el jam si se le escapa uno? Falsos holders (procesos que solo abrieron el
   archivo un instante)?
4. **Marcador de parada graceful:** es confiable si el cron esta mid-exec cuando se setea? Sale limpio o deja
   justamente un exec colgado (el problema que queremos evitar)? Interaccion con el footgun del detector de parada.
5. **24/7 vs DECISION-0057 (control de costo):** "mantener crones arriba en build activo" es defendible o quema
   tokens/costo? Donde esta el punto de corte objetivo?
6. **Carreras entre barredores:** si corre el barrido desde una sesion del Arquitecto Y existe otra sesion o el
   Arquitecto-cron, dos barridos podrian matarse execs mutuamente? Quien tiene la autoridad y como se serializa?
7. **Auto-dano al Analista:** el Analista es peer; el barrido podria matar SU exec de review en curso. Como se
   protege el exec vivo del propio checker?
8. **Estado del ledger tras un kill:** matar un zombie a mitad, deja el ledger sucio (intent a medias, claim
   huerfano)? Esta vez no hubo claim huerfano -- es garantia o suerte? Que invariante lo asegura?

## 6. Pregunta de cierre para el Analista
Veredicto GO/NO-GO sobre la separacion A/B/C + el barrido de s.3: es segura, o hay un vector (sobre todo #1 y #7,
matar trabajo bueno) que la vuelve peligrosa? Que cambiarias antes de convertirla en politica/tarea?
