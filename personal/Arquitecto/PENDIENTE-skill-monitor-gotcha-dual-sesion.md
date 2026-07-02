# PENDIENTE: gotcha dual-sesion para .claude/skills/arquitecto-monitor-coordina/SKILL.md

El harness (clasificador de permisos, guard de auto-modificacion de skills) BLOQUEO la edicion
autonoma de la skill. Texto listo para insertar en la seccion "## 4. Gotchas aprendidos",
antes del bullet "**Arbol compartido:**" (aplicar en sesion interactiva con aprobacion del
operador, o que el operador lo pegue):

- **DUAL-SESION ARQUITECTO (leccion 2026-07-03, directiva Operador resolucion-dual-sesion):** dos sesiones
  interactivas del Arquitecto pueden quedar vivas a la vez (la vieja con monitores armados sigue reaccionando
  cuando el operador ya arranco la nueva). Son INVISIBLES entre si: ambas firman actor_id Arquitecto y sus
  commits llevan Co-Authored-By: Claude, asi que el SELF-FILTER de ambos monitores descarta los commits de la
  otra -> colision silenciosa (higiene/promociones/GOs duplicados). GUARD OBLIGATORIO: al arrancar, verificar
  `personal/Arquitecto/.session-lease` (si hay lease FRESCO <30min de otro session_id -> NO coordinar, consultar
  al Operador); escribir/refrescar el lease propio en cada turno como parte del auto-poll; borrarlo al cerrar.
  Mitigacion si la dualidad ya ocurrio: particion de carriles via CLAIMS del ledger (unico mutex efectivo entre
  sesiones con la misma firma) + FYI al Operador para que ordene el stand-down de una (discriminador por
  session_start_ts). NO re-emitir GOs/higiene que la otra ya emitio: verificar CLAIMS.json + git log ANTES de
  cada escritura compartida.
