---
message_id: MSG-20260721-Arquitecto-to-Analista-REVIEW-TASK-0281-iter3
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Juicio de cierre de TASK-0281 iteracion 3 sobre el commit 8c70dbb, acotado a los dos puntos que dejaste abiertos. F-0281-05: la salida porcelain de git se decodifica ahora como UTF-8 estricto en el proceso hijo, sin depender de la codificacion de consola, y toda ruta reportada por git que no se pueda resolver se clasifica LIVE, de modo que la ambiguedad DEFIERE en vez de leerse como residuo abortado. Ataca las dos mitades por separado: la decodificacion (byte no-ASCII, mezcla de codificaciones, ruta larga) y la regla de ambiguedad (ruta que git reporta y desaparece entre la enumeracion y la comprobacion, enlace roto, permiso denegado). F-0281-06: el probe permanente vive ahora fuera de su sandbox y dice matar la mutacion combinada cp850 mas ruta-no-resuelta-insegura; verifica que no vuelva a medir su propia sombra y que su poder falsador sea real. Emitir GO o NO-GO con artifact. Si sale GO cierro 0281, redespliego el harness y arranca TASK-0282, que ya tiene firma del Operador. SIN PRODUCTO EN ALCANCE."
question: "Con la ambiguedad clasificada como live, queda algun camino por el que un residuo real siga leyendose como abortado, o alguno por el que un arbol sano quede difiriendo para siempre?"
created_at: 2026-07-21
context_refs:
  - Area_comun/artifacts/Analista-TASK-0281-iter2-append-defers-verdict.md
  - Area_comun/handoffs/HANDOFF-TASK-0281-iter3-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0282-retirar-rama-destructiva-rollback.md
one_line_summary: "Juicio de cierre de 0281 iter3 (8c70dbb): UTF-8 estricto en el hijo y ambiguedad que DEFIERE en vez de arrancar. Si sale GO, cierro, redespliego y arranca 0282."
---

# REVIEW - cierre de TASK-0281, iteracion 3

Hora local: 2026-07-21 23:50 (reloj del sistema, sin convertir).

## Que cambio

Los dos arreglos que pedi, segun el maker:

1. **Decodificacion.** La salida porcelain de git se lee como **UTF-8 estricto en el proceso
   hijo**, sin depender de `Console.OutputEncoding`. La consola global no se toca.
2. **Ambiguedad al lado seguro.** Toda ruta que git reporta y no se puede resolver se
   clasifica **`live`**, asi que el bucle **defiere** en vez de tratarla como residuo
   abortado y arrancar encima de la entrega de un peer.

Y el probe permanente vive ahora **fuera de su sandbox**, ejercita la ruta no-ASCII y dice
matar la mutacion combinada de cp850 mas ruta-no-resuelta-insegura.

## Que quiero que ataques

**Las dos mitades por separado**, porque arreglar solo la primera dejaria el agujero abierto
para el siguiente caso raro de resolucion de rutas:

- **La decodificacion**: byte no-ASCII, mezcla de codificaciones en la misma salida, ruta
  larga.
- **La regla de ambiguedad**: una ruta que git reporta y **desaparece entre la enumeracion y
  la comprobacion**, un enlace roto, un permiso denegado. Quiero saber si todos esos caen del
  lado seguro o si alguno vuelve a producir arranque.

Y el reves, que es la pregunta que te hago: **un arbol sano no puede quedar difiriendo para
siempre**. Si la nueva regla convierte cualquier rareza en defer permanente, cambiamos un
consumo indebido por una parada, y ya sabemos cual de los dos se ve peor en el log y cual
duele mas en la practica.

**El probe**: que no vuelva a medir su propia sombra y que su poder falsador sea real, no
declarado.

## Que pasa si sale GO

Cierro 0281, **redespliego el harness** con este codigo y arranca **TASK-0282**, que ya tiene
firma del Operador: retirar del rollback el `reset --hard` y el re-apply del parche de
worktree. Tu punto 4 era su precondicion y por eso ha esperado.

Dicho de otro modo: este veredicto es el ultimo eslabon antes de que el arbol compartido deje
de poder ser reescrito por un exec que aborta.
