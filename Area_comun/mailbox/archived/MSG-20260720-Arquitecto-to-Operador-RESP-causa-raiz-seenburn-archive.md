---
message_id: MSG-20260720-Arquitecto-to-Operador-RESP-causa-raiz-seenburn-archive
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: false
created_at: 2026-07-20
context_refs:
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-codex-dos-encargos-sin-recoger.md
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
one_line_summary: "RESP (11:05 local): 4a recurrencia CONFIRMADA y CAUSA RAIZ ENCONTRADA -- no era el cron: mis podas archivaban tareas y Area_comun/state/TASK_INDEX_ARCHIVE.json quedaba SIN COMMITEAR en mis ciclos; esa era la unica 'escritura ajena' que el pre-gate de Codex veia, y por la que se nego 4 veces. Commiteado (617efc2), arbol gobernado 100pct limpio, ambos mensajes des-seen. Regla propia adoptada: los *_ARCHIVE.json entran SIEMPRE en el pathspec post-poda."
---

# RESP - causa raiz del seen-burn: era mia, y era el ARCHIVE

Hora local: 2026-07-20 11:05. Tenias razon otra vez, y esta vez la investigacion
llego al fondo en vez de solo destrabar.

## Lo que encontre (envelope de Codex, no interpretacion mia)

Su exec de las 10:21 sobre el GO de 0272 SI corrio (50 segundos) y se nego con este
diagnostico literal: *"Pre-gate de ventana segura FAIL: git status --short muestra
cambios ajenos en ledger, task TASK-0272, eventos y snapshot"*. Fui a mirar QUE cambio
ajeno veia, esperando encontrar residuo de un peer.

Era mio: **`Area_comun/state/TASK_INDEX_ARCHIVE.json` llevaba horas modificado sin
commitear.** Cada `prune_state --apply` que corri archivaba tareas cerradas (0257 la
ultima) y escribia ese fichero -- pero el pathspec de mis commits de estado incluia solo
los 3 hot + slims + events + snapshot. El ARCHIVE nunca entraba. Resultado: un fichero
gobernado permanentemente sucio en el arbol compartido, que hacia fallar el pre-gate de
Codex UNA Y OTRA VEZ.

**Las 4 negativas de Codex fueron correctas las 4 veces.** El harness quemaba el mensaje
(defecto real, TASK-0272 lo arregla), pero la piedra que disparaba el aborto la ponia yo,
y era la MISMA piedra desde la primera vez. Por eso reaparecia cada vez que "limpiaba la
ventana": limpiaba todo menos el ARCHIVE.

## Aplicado ya

1. `617efc2`: ARCHIVE commiteado. **Arbol gobernado 100% limpio** (primera vez en horas).
2. Des-seen de los DOS mensajes (ACTION docs 0258 + GO 0272). Su proximo ciclo los toma
   con la ventana realmente limpia.
3. **Regla propia adoptada** (la cuarta del dia, y la que faltaba): todo commit posterior
   a `prune_state --apply` stagea TAMBIEN `Area_comun/state/*_ARCHIVE.json`; mi pathspec
   de estado pasa a ser el conjunto COMPLETO que la poda puede tocar.

## Sobre la circularidad que nombraste

Tenias razon en que el fallo bloqueaba su propia reparacion, pero por una via distinta a
la sospechada: no era el harness impidiendo construir 0272, era mi residuo. 0272 sigue
siendo necesaria (el harness no debe quemar mensajes de execs que no hicieron trabajo),
pero ahora sabemos que sin mi residuo no se habria disparado ninguna de las 4 veces.
Ambas cosas se arreglan: la mia ya, la del harness cuando 0272 aterrice.

## Nota honesta sobre la deteccion

Los 4 episodios los cazaste tu mirando CPU y edad de mensajes. Mis watchdogs vigilan
execs colgados y crons muertos, pero NINGUNO vigila "mensaje a peer sin recoger tras N
minutos" -- que es justo el sintoma. Lo anado como watchdog de sesion ahora mismo, sin
esperar a 0272 (que es el arreglo estructural). Si quieres que ademas quede como regla
exportable, dilo y lo registro.

## Estado

DONE: 0257, 0267, 0268, 0270, 0271. E6 resuelta (E6-A permanente). En cola de Codex con
ventana limpia: docs 0258 -> 0272. Pendiente tuyo: GO build-open N=6.
