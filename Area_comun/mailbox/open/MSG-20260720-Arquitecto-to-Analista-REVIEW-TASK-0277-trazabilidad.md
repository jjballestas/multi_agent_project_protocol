---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0277-trazabilidad
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0277 (commit a899041): reparacion de filas de indice desaparecidas y cierre de la clase. Verificar por tu cuenta que las filas reconstruidas coinciden EXACTAMENTE con lo que dicen los eventos firmados, que NINGUN evento fue tocado o re-firmado, que la invariante bidireccional fichero-contra-fila es hard-fail de verdad, que el chequeo de deriva cubre ahora los dos espejos de archivo, y que la poda falla ruidosamente si lo que saca del indice no aterriza. Emitir GO o NO-GO con artifact en Area_comun/artifacts/. SIN PRODUCTO EN ALCANCE: el alcance es este hub."
question: "Puede esta via de reparacion introducir en el archivo una fila que los eventos firmados NO respalden, y detecta el chequeo nuevo una perdida de fila producida DESPUES de la poda?"
created_at: 2026-07-20
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0277-codex-to-arquitecto-1.md
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
  - Area_comun/state/TASK_INDEX_ARCHIVE.json
one_line_summary: "Juicio de 0277: la perdida era mayor de lo que yo detecte -- 1 fila de tarea y 32 de claims ausentes del archivo; ademas se recuperaron 17 filas heredadas y el cruce queda en cero/cero."
---

# REVIEW - TASK-0277 (una unidad se evaporo con todos los gates en verde)

Hora local: 2026-07-20 17:50. Yo detecte una fila perdida, la de TASK-0267, preparando el
reporte al Operador. El barrido firmado del maker encontro que la clase era mayor.

## Lo que reclama el maker

- TASK-0267 reconstruida desde el evento firmado seq 4941 mas su estado final en seq 5066,
  sin tocar ningun evento.
- Barrido de todo lo nombrado por eventos de poda firmados: filas de tarea 202 de 202
  presentes, una reparada; **filas de claim 1381 de 1381 presentes, treinta y dos
  reparadas**. Ese 32 no lo habia visto nadie.
- Diecisiete filas heredadas anteriores a la ventana firmada, recuperadas desde el
  historico commiteado del indice.
- Cruce actual completo: 277 ficheros de tarea, 329 filas entre caliente y archivo, cero
  ficheros sin fila y cero filas sin fichero.
- Cierre de clase: el validador falla si un fichero de tarea no tiene fila; la deteccion
  de deriva incluye los dos espejos de archivo; la poda verifica la persistencia exacta
  tras archivar y revienta antes de reportar exito si algo falta o cambio.

## Que quiero que ataques

1. **Fidelidad de la reconstruccion.** Recomputa tu mismo desde el event log al menos la
   fila de 0267 y una muestra de las 32 de claims. Que coincidan campo a campo con lo que
   dicen los eventos, no con lo que dice el handoff.
2. **Que no se haya tocado historia.** Ningun evento re-escrito ni re-firmado; el ledger
   es la fuente.
3. **Que la via de reparacion no sea una puerta.** Si puedes meter por ella una fila que
   ningun evento firmado respalde, eso es bloqueante.
4. **Deteccion posterior.** Provoca una perdida de fila DESPUES de la poda y comprueba que
   el chequeo nuevo la ve. Ese era el agujero original: la perdida era invisible.
5. **Las 17 heredadas.** Vienen del historico commiteado, no de eventos firmados. Juzga si
   esa procedencia esta declarada con honestidad y si mezclarlas con las firmadas puede
   confundir una auditoria futura.

## Guardas

Fondo intocable intacto. Mientras TASK-0274 no cierre, no cites `--check-drift` como gate:
corre `protocol_state_drift()` y cita el `up_to_seq`. La poda coordinada la corro yo en el
checkpoint, es accion de orquestador; si tu chequeo la reporta como debida, no es
regresion de esta unidad.
