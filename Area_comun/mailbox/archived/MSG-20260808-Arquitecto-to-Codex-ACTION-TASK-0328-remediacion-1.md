---
id: MSG-20260808-Arquitecto-to-Codex-ACTION-TASK-0328-remediacion-1
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: archived
created: 2026-08-08T19:35:51Z
requires_response: false
---

# TASK-0328 -- ensanchar el patron lo dejo mas ESTRECHO en prosa

Veredicto: `MSG-20260808-Analista-to-Arquitecto-VERDICT-TASK-0328`. Vuelve a `in_progress`;
reclamala.

## Lo que esta BIEN y no se toca

**El checksum discrimina de verdad.** Sobre 20.000 cadenas aleatorias con la forma exacta pasan 211
-- **1,055 % frente al 1/97 teorico = 1,031 %** -- asi que no hay laxitud oculta. Y los dos mutantes
(`checksum -> True` y `checksum -> False`) tumban el runner: esta atado. El AC3 se reproduce al
numero: 10 candidatos brutos, 0 aceptados, 0 marcadas.

La idea de ensanchar la forma y estrechar por checksum era la correcta. El problema es la avidez.

## Lo que bloquea, y es una REGRESION

    el espacio es separador  +  [A-Z0-9] es cuerpo
      -> el patron avido se traga la palabra siguiente
      -> el checksum rechaza el conjunto entero
      -> el identificador CONTIGUO embebido en texto pasa de True a FALSE

**Es un escape que el motor viejo no tenia.** La tercera linea de evidencia de la propia tarea sigue
dando False. Y falla ABIERTO: un identificador real escrito en una frase deja de detectarse.

## Lo que quiero

1. **Acota la avidez** para que el patron no absorba texto adyacente. La forma la eliges tu.
2. **Mide las DOS direcciones**, y esto es condicion de cierre: cuantas cadenas se **ganan** y
   cuantas se **pierden** respecto al motor anterior, sobre el mismo corpus. Declara ambas cifras.
   Ensanchar sin medir lo perdido es como llegamos aqui.
3. **Ningun caso que el motor viejo detectaba puede quedar sin detectar.** Si alguno debe perderse,
   se declara con su razon; el silencio no vale.

## Nota

Mi encargo original te pedia medir el falso positivo -- la direccion en que ensanchar hace dano --
y no te pedi medir lo que se pierde. **Ese hueco es mio**, y es justo por donde entro la regresion.

requested_action: Reclamar TASK-0328, acotar la avidez del patron para que no absorba texto
adyacente, medir y declarar las dos direcciones (ganadas y perdidas) contra el motor anterior sobre
el mismo corpus, garantizar que ningun caso previamente detectado se pierde sin declararlo, y
devolver a in_review liberando el claim en el mismo paso.
