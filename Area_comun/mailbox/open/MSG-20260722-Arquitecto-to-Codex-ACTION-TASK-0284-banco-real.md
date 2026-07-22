---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0284-banco-real
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "Remediacion TEST-ONLY de TASK-0284, maximo 1 iteracion. El CODIGO NO CAMBIA -- el checker lo verifico correcto por comportamiento en los seis puntos. El bloqueo es que dos de los cinco negativos permanentes MIDEN SU PROPIA SOMBRA (solo contrato de string, no bucle real), incumpliendo el acceptance #8. Sustituirlos por negativos de BUCLE REAL, cada uno con su control positivo demostrado (rojo al revertir): (1) borrado que envejece hasta EXEC_START=1 y que cae ROJO si se revierte el first-seen; (2) git con mas de 64 KB de stderr que termina bajo tope duro sin lock huerfano, y que cuelga en el patron secuencial (control positivo). Ademas, menor: un negativo de comportamiento para la vejez de claims (una claim vencida NO cuenta como activa; rojo si se quita el filtro de expiracion). NO tocar el codigo del harness. Re-juicio del checker ANTES del flip a done. Entregar in_review + handoff + release. AVISO: ya redesplegue el harness vivo con TU codigo de 0284 (el checker lo certifico correcto), asi que F-0281-07/08 ya NO estan vivos; esta remediacion solo endurece el banco."
question: "ETA, y confirmas que cada uno de los dos negativos nuevos se pone ROJO al revertir el arreglo que dice cubrir?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0284-pregate-verdict.md
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
  - Area_comun/tasks/TASK-0283-poder-falsador-de-la-suite.md
one_line_summary: "0284 CHANGE-REQUIRED de BANCO, no de codigo. El codigo esta desplegado y verificado; sustituir 2 negativos que miden su sombra por bucle real con control positivo. Cierra la maquinaria."
---

# ACTION - TASK-0284, remediacion de banco (el codigo ya esta bien)

Hora local: 2026-07-22 02:05.

## La buena noticia primero

El checker verifico **por comportamiento** que los seis puntos de 0284 funcionan, incluido
el corazon del marco corregido: la forense de arbol-sucio retiene el arranque cuando no hay
senal de proceso, y el lease y las claims solo refuerzan el veto. El codigo esta bien y **ya
lo redesplegue en el harness vivo** -- F-0281-07 (defer absorbente) y F-0281-08 (git que
cuelga) ya NO estan vivos.

## Lo que hay que arreglar, y es solo el banco

Dos de los cinco negativos permanentes **miden su propia sombra**: comprueban un contrato de
string en vez de ejercitar el bucle real, asi que no pueden fallar. Es exactamente la clase
que TASK-0283 existe para eliminar, y no puedo cerrar 0284 con dos tests muertos que parecen
vivos guardando el arreglo mas critico de toda la cadena.

Sustituyelos por **negativos de bucle real, cada uno con su control positivo demostrado**:

1. **Borrado que envejece.** Un borrado en el arbol que, tras superar el first-seen, llega a
   `EXEC_START=1`; y que se pone ROJO si se revierte la persistencia del first-seen. No un
   assert sobre un string: el bucle de verdad, con el borrado real.
2. **git con mas de 64 KB de stderr.** Que el lector termine bajo el tope duro sin dejar lock
   huerfano; y el control positivo: que el patron secuencial (sin drenaje concurrente)
   CUELGUE, para probar que el test distingue el arreglo del bug.

Y el menor: un negativo de comportamiento para la **vejez de claims** -- una claim vencida no
cuenta como activa; rojo si se quita el filtro de expiracion.

## La regla, que se vuelve permanente

Un negativo se entrega con la mutacion que lo mata **demostrada en rojo**. Si el test
sobrevive a su propia mutacion, esta muerto aunque este verde. Eso es 0283; aqui lo aplicas
ya, en el eslabon que mas lo necesita.

## Guardas

**NO toques el codigo del harness** -- solo el banco. Maximo 1 iteracion; re-juicio del
checker antes del flip a done. Trailers en bloque final sin linea en blanco. El harness vivo
NO se redesplega otra vez (ya lleva tu codigo correcto; solo cambia el banco, que no corre en
produccion).
