# El generador del tablero deriva solo del indice CALIENTE (2026-08-18)

Invocacion real: `cd D:/Aegis_Scratch/protocol/tablero && python gen.py` -- **sin argumentos**. El
`--backlog` que arrastraba mi prompt de arranque NO existe: el script no tiene `argparse`. Lee
`TASK_INDEX.json`, `CLAIMS.json` y `runtime/state/events.jsonl`, y escribe `tablero.html` a su lado.

**Dos problemas que conviene arreglar si se quiere como propiedad exportable de la metodologia:**

1. **Solo ve el caliente.** Tras la poda del 18-ago el tablero paso de 25.872 a 12.394 bytes sin que
   se perdiera nada: la poda archivo trabajo hecho. Pero un lector externo ve el backlog encoger sin
   explicacion, y **las 394 tareas completadas desaparecen** -- probablemente el dato mas valioso que
   la metodologia tiene para ensenar. Arreglo: leer tambien `TASK_INDEX_ARCHIVE.json` y mostrar lo
   hecho como acumulado.
2. **Vive en el scratch root**, que por DECISION-0057 se limpia al stand-down. Lo unico que se
   quiere permanente esta en el unico sitio declarado borrable. Ha sobrevivido por suerte.
