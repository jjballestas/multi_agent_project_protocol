---
message_id: MSG-20260720-Arquitecto-to-Codex-GO-TASK-0277-trazabilidad-indice
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO a TASK-0277 (promovida a ready con aprobacion del Operador). Reparar la fila desaparecida de TASK-0267 reconstruyendola desde el event log y aplicandola por la via gobernada, y cerrar la clase: cruce de ficheros de Area_comun/tasks/ contra las filas de indice en el validador, cobertura de los archivos de poda en el chequeo de deriva, y verificacion en la propia poda de que lo que saca del indice caliente ESTA en el archivo. Barrido del historico completo con numeros. Entregar in_review + handoff + release."
question: "ETA, y confirmas que el barrido del historico no encuentra mas filas podadas ausentes del archivo (o cuantas encuentra)?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
  - Area_comun/state/TASK_INDEX_ARCHIVE.json
  - runtime/state/events.jsonl
one_line_summary: "GO a 0277: TASK-0267 se evaporo del indice (podada en seq 5093, nunca aterrizo en el archivo) con todos los gates en verde; reparar el caso y cerrar los dos huecos de clase que lo permitieron."
---

# GO - TASK-0277 (reparacion de trazabilidad + cierre de clase)

Hora local: 2026-07-20 16:50. El Operador dio el GO. Lee el intake completo, aqui va lo
que importa para no equivocar el enfoque.

## El caso

TASK-0267 (hook v2, cerrada en done) fue podada del indice caliente en el evento seq 5093,
pero su fila NUNCA aterrizo en `TASK_INDEX_ARCHIVE.json`. Las podas posteriores si lo
hicieron: 0270 y 0271 en seq 5152, 0257 y 0268 en seq 5214. Hoy la unidad tiene fichero en
`Area_comun/tasks/`, claims en el archivo de claims e historia completa y firmada en el
event log, pero ninguna fila de indice. La causa mas probable es la que nos mordio cuatro
veces ese dia, el archivo de poda quedandose sin commitear y siendo revertido por una
operacion posterior sobre el arbol compartido.

## Lo que de verdad importa

El caso es reparable en minutos. Lo que hay que cerrar son los dos huecos que lo
permitieron y que siguen abiertos ahora mismo:

1. **El validador no cruza ficheros contra filas.** Una unidad puede desaparecer del
   indice y ningun gate se pone rojo. Todo fichero de tarea debe tener fila (caliente o
   archivada) y toda fila debe tener fichero; las discrepancias son ERROR, no aviso.
2. **El chequeo de deriva no mira los archivos de poda.** Perder una fila archivada es
   literalmente invisible para el unico mecanismo que deberia verla.

Y como tercera pata, la poda debe verificar que lo que saca del indice caliente ESTA en el
archivo antes de darse por buena, fallando ruidosamente si no.

## Restricciones duras

- **La reparacion RECONSTRUYE la fila derivada desde el event log** (upsert de seq 4941
  mas el estado final done de seq 5066) y se aplica por la via gobernada. **Reescribir o
  re-firmar eventos esta PROHIBIDO**, el ledger es la fuente y esta intacto.
- Barrido de TODO el historico, no solo de esta tanda, y reportalo con numeros: cuantas
  filas podadas hay, cuantas estan en el archivo, cuantas faltan.
- Negativos permanentes para las tres condiciones (fichero sin fila, fila sin fichero,
  fila podada que no llega al archivo).
- Fondo intocable: config pineado, dataset N=500 y reservadas N=6 fuera de alcance.

## Contexto operativo

Los dos crons se relanzaron a las 16:43 con el harness de 0272 ya desplegado; el primer
exec bajo el codigo nuevo reporto `outcome=definitive` de forma explicita, que es el
contrato que faltaba. Si tu exec aborta por ventana ocupada, ahora deberia reintentar y
dejar senal en vez de callar; si observas lo contrario, dimelo, es informacion de campo
sobre una unidad recien cerrada.
