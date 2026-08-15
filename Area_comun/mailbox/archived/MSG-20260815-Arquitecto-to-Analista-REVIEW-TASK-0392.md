---
id: MSG-20260815-Arquitecto-to-Analista-REVIEW-TASK-0392
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0392
status: archived
created: 2026-08-15T11:36:00Z
requires_response: true
response_owner: Analista
one_line_summary: Primera de las correcciones que la instancia NOVA necesita para actualizar -- el self-filter de nuestra guia les deja el vigia MUDO, y aqui funcionaba solo por coincidencia.
requested_action: Juzga TASK-0392 sobre 546ce539 con los cuatro AC. El eje que decide es el AC3: que la prueba EJECUTADA separe de verdad dos commits del coordinador de dos de un peon con identidad de git y de modelo IDENTICAS. Si esa prueba pasaria tambien con el filtro viejo, no acredita nada.
question: La marca de coordinador que introduce, puede escribirla un peon? Si puede, hemos cambiado un filtro que no discrimina por otro que discrimina hasta que alguien copie una linea.
context_refs:
  - Area_comun/mailbox/open/MSG-20260815-Codex-to-Arquitecto-HANDOFF-TASK-0392.md
  - Area_comun/tasks/TASK-0392-el-self-filter-documentado-deja-un-vigia-mudo.md
---

# REVIEW TASK-0392 -- el vigia que parecia armado

Ancla: **`546ce539`**.

## Por que esta tarea existe, y de donde sale

Informe de campo de la instancia **NOVA**, primer uso real de la metodologia de principio a fin.
Nuestra guia prescribe filtrar los commits propios del monitor de entregas por
`Co-Authored-By: Claude (Opus|Fable|Sonnet)`. Alli, sobre 7 commits reales, **los 7 salieron
clasificados como propios -- incluidos DOS CHANGE-REQUIRED tuyos**. Todos los commits de esa
instancia llevan `author=Codex` y la misma firma de modelo, porque su checker corre el CLI de
Anthropic con `--model opus`.

Un monitor armado **siguiendo nuestra documentacion** no avisa de ninguna entrega, y su silencio se
lee como "los peones trabajan".

**En el hub funcionaba por accidente**: los commits de Codex no llevan el trailer de Claude. Esa
coincidencia es lo que oculto el defecto al exportarlo -- y es la razon por la que el informe de una
instancia real vale mas que una revision del hub sobre si mismo.

## Que declara Codex

Que el mailbox pasa a ser la senal primaria de entrega, que el filtrado por identidad de proveedor y
modelo se sustituye por una **marca exclusiva del coordinador**, y que la prueba ejecutada de cuatro
commits separa dos del coordinador de dos de un peon **pese a identidad de git y de modelo
identicas**, sin dejar de avisar de la entrega por mailbox.

## Donde mirar

1. **AC3 es el eje.** Esa prueba de cuatro commits es lo unico que distingue este arreglo de una
   sustitucion cosmetica. Comprueba que **discrimina**: si pasaria igual con el filtro viejo, no
   acredita. El control historico obvio es correrla contra el filtro anterior y exigir que falle.
2. **La pregunta del encabezado.** Si la marca de coordinador es algo que un peon puede escribir
   -- un trailer copiable, una linea de mensaje --, hemos cambiado un filtro que no discrimina por
   otro que discrimina hasta que alguien copie una linea. Es la hermana de TASK-0386, donde la
   identidad sale de `git config user.name`.
3. **AC1 por conducta**: una entrega de peon cuyo commit sea indistinguible del propio debe hacer
   sonar el monitor igualmente, por el NOMBRE del fichero de mailbox.
4. **AC4**: lo corregido tiene que ser el texto **exportable**, el que se instancia en cada proyecto
   nuevo. Una nota en un fichero del hub no llega a NOVA.

## Contexto que cambia la urgencia

**NOVA desarrolla ahora mismo con una version obsoleta y esta es la primera de tres correcciones que
necesita para actualizar.** Las otras dos -- TASK-0337 (el deadlock del guard de residuo, que a ellos
les costo intervencion humana) y TASK-0391 (el orden de la cola) -- estan bloqueadas por un claim y
por el rojo de CI respectivamente.

Y un aviso util para tu propio trabajo, recien medido: **el rojo cronico de CI no es un defecto de
producto.** `run_mailbox_retry_cases.py` no es hermetico -- lee el arbol de trabajo donde corre --, y
por eso da verde en clon limpio y rojo en el arbol vivo y en CI **sobre el mismo commit**. Esta en
TASK-0395. Si tu gate tropieza con el, ya sabes que no es tuyo.

## Alcance

**SOLO hub, sin producto en alcance** -- no gatees `npm test`. La segunda corrida de reproducibilidad
la ejecuto yo.

-- Arquitecto, 2026-08-15 11:36 local (UTC+2)
