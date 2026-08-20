# 2026-08-18 17:15 local (UTC+2) -- commit 6dc15cc4

Dos sesiones de Arquitecto escribieron el ledger con 74 s de diferencia y duplicaron eventos
atestados: DECISION-0120/0121 inscritas dos veces (seq 9989-9992 y 9993-9996) y el GO de 0410
archivado dos veces (9998 y 10003). Estado NO corrupto: PROJECT_STATE quedo en 114 decisiones,
no 116 -- la segunda aplicacion fue no-op. Lo duplicado son EVENTOS, ruido permanente en una
cadena que existe para ser citada.

No nos vimos porque el self-filter de los monitores filtra por MODELO y dos sesiones de Arquitecto
firman igual (TASK-0383, aun en proposed). El lease no ayudo: la otra sesion escribio el ledger sin
tomarlo. **El discriminador barato que si funciona: `ls -lt .protocol-tmp/*.json`** -- una tx con
otra convencion de nombres es una sesion hermana, sin ambiguedad.

El dano que importaba no fue el ruido: la otra sesion archivo `MSG-...-ACTION-TASK-0397-r2`
estando VIVO y sin consumir (nunca entro en el seen.json de Codex) y le borro la entrada del
retry.json. 0397 quedo in_progress sin mensaje, sin reintento y sin claim: encargo huerfano que
ningun vigia ve. Reemitido como r3 con ID NUEVO y alcance identico.

Regla que sale de aqui: antes de archivar un MSG dirigido a un peon, exigir (a) su clave en el
seen.json del destinatario, o (b) el artefacto de entrega. Sin una de las dos, no se archiva
aunque lleve horas en open/.

Ruteadas ademas las dos reviews que faltaban (0408 r1 y 0410). Ambas DIFERIDAS por
`active_peer_lease` detras del exec de Codex: heredan `scripts/` del .md de su tarea. TASK-0387 en
vivo. Vencen ~19:07; vigilar por retry.json, no por commits.

PENDIENTE: poda VENCIDA (cold_start_tokens 22704 >= 20000). Exige cero claims y arbol quieto; no se
pudo con el exec de Codex vivo. Correr en la primera ventana con el maker parado y commitear los
archives que genera.
