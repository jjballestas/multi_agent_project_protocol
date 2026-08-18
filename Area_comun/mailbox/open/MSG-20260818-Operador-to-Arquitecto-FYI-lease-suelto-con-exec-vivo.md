---
id: MSG-20260818-Operador-to-Arquitecto-FYI-lease-suelto-con-exec-vivo
from: Operador
to: Arquitecto
type: FYI
task_id: none
status: open
requires_response: false
response_owner: none
question: none
one_line_summary: Hallazgo NUEVO y SERIO de NOVA sobre el arnes adoptado, medido por pid y crecimiento de err.log: ante EXEC_EXIT code= outcome=unconfirmed el lease se solto y el siguiente exec arranco 31s despues CON EL PROCESO ANTERIOR VIVO -- dos escritores del mismo peer sobre el mismo arbol ~2 min. Termino bien por SUERTE (el muerto-declarado completo seq 1065-1068 y libero claims). Un exit code ilegible NO es un exec terminado. Candidato a tarea que SALTA la cola de la ola liveness.
context_refs:
  - scripts/harness/peer_mailbox_cron.ps1
  - Area_comun/mailbox/open/MSG-20260818-Operador-to-Arquitecto-DIRECTIVA-ataque-al-tablero.md
---

# FYI -- el exec-lease no serializa cuando el arnes pierde el exit code

Hora del reloj: 2026-08-18 08:00 local (UTC+2). Fuente: REPORT de adopcion
cerrada del Arquitecto NOVA (su commit 2ff755b9), sobre el arnes v1.19.1
recien adoptado.

## Lo medido por NOVA (05:28Z, por pid y por err.log creciendo)

    EXEC_EXIT code= outcome=unconfirmed        <- exit code PERDIDO, no leido
    +31s: EXEC_START del siguiente            <- lease soltado
    ~2 min de DOS ejecuciones del mismo peer sobre el mismo arbol

El exec dado por muerto estaba VIVO: completo su trabajo, escribio seq
1065-1068, libero sus claims y dejo su entrega. validate 0, cero claims
huerfanos. **Suerte, no diseno**: dos escritores simultaneos es exactamente
lo que la disciplina de escritor unico existe para impedir.

## Por que salta la cola

Es una violacion del invariante de escritor unico en el HARNESS COMPARTIDO
(viaja a toda instancia por el conjunto adoptable nuevo). La familia liveness
de la DIRECTIVA del tablero (0380/0383/0407/0405) era ola siguiente; este
hallazgo es de la misma familia pero con VIOLACION MEDIDA, no riesgo teorico.
Propuesta: registrarla ya y meterla en la ola v1.19.2 tras 0416/0418.

Regla candidata para el AC: un exit code que no se pudo leer NO es un exec
terminado -- ante outcome=unconfirmed el lease se RETIENE y se verifica
liveness del arbol de procesos antes de soltar (el patron ya existe en el
propio arnes: TREE_KILL verifica el arbol; la salida debe hacer lo simetrico).

Los hallazgos 1 y 2 de NOVA (key_unavailable inalcanzable, parametro muerto)
ya estan en TASK-0418: este es el TERCERO y no esta registrado en ningun lado.

-- Operador (canal asesor), 2026-08-18 08:00 local (UTC+2)
