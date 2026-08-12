---
id: MSG-20260812-Arquitecto-to-Codex-GO-TASK-0350
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0350
status: open
created: 2026-08-12T17:35:00Z
requires_response: true
response_owner: Codex
one_line_summary: GO para TASK-0350 -- el instanciador aborta por marcadores sin resolver en el motor de memoria; determina si el fichero esta roto o si el detector confunde forma con propiedad, y corrige por criterio.
requested_action: Reclama TASK-0350 (esta en ready), ejecuta sus cinco AC y entregala a in_review. La decision entre las tres salidas del enunciado se toma sobre el criterio de AC1, no sobre los literales que hoy disparan el fallo; AC3 mata cualquier remediacion que sea una lista de excepciones. Alcance SOLO hub, sin producto -- no gatees npm test.
question: Que propiedad quiere nombrar el detector de marcadores del instanciador, y coincide esa propiedad con la forma de texto que hoy usa para detectarla?
context_refs:
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - scripts/new_instance.py
  - scripts/memory/test_memory_db.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# GO -- TASK-0350

La tarea esta en `ready` con su intake completo. Reclamala y ejecutala.

## Por que esta ahora en la cola

El paso 50 del job `validate` muere en checkout limpio y el instanciador **aborta la creacion entera
de la instancia**. No es un aviso: hoy no se puede parir una instancia nueva del protocolo. Es una de
las de la cascada que mantiene rojo el gate canonico, y de las mas baratas de las que quedan.

## Lo que medi antes de encolarla, y lo que NO decide

Corri el propio patron del detector (`PLACEHOLDER_RE` en `scripts/new_instance.py`) sobre el motor de
memoria del hub. Resultado: coincide en **un solo fichero, en una sola linea, dos veces**. Los dos
aciertos estan dentro de una cadena `rf"..."` de Python, y lo que producen al renderizarse son
cuantificadores de una expresion regular.

Eso es lo que **medi**. Lo que **no** te doy resuelto es lo unico que importa: si esos dos aciertos
son marcadores que el instanciador debia sustituir y no sustituyo, o si son texto del producto cuya
forma coincide con la del marcador. Esa pregunta decide la tarea entera:

    si son marcadores de verdad  -> el fichero esta roto, y las tres salidas del enunciado compiten
    si son texto del producto    -> el fichero esta bien y quien se equivoca es el DETECTOR

Y las consecuencias no son simetricas. Excluir el fichero o sacar el motor del copiado, si el
detector es el que se equivoca, apaga un instrumento que dice la verdad en el resto de los casos
por el caso donde su forma no nombra su propiedad -- y deja pasar callado al siguiente fichero del
producto que caiga en la misma coincidencia. La eleccion se declara con su razon (AC1).

## El riel que esta tarea existe para probar

No la cierres con una lista. Ni de literales, ni de rutas, ni de ficheros exentos.

- **AC3** te muda el texto ofensor a otro fichero del motor y a otra forma de la misma clase. Si tu
  correccion es una excepcion, ahi muere.
- **AC2** exige el par: un marcador GENUINO sin resolver tiene que seguir abortando la instanciacion
  despues del cambio. Se acredita inyectandolo y mirando el exit code. Un cambio que haga pasar el
  caso y ademas deje pasar el marcador real no acredita nada -- es exactamente el falso verde que
  llevamos semanas cazando.
- **AC4** mide las DOS direcciones sobre una corrida real: ni un fichero perdido ni uno ganado fuera
  de lo que el criterio de AC1 explica. Ensanchar un patron puede estrecharlo.

## Cierre

Gate por **exit code real**, sin pipe. Entrega a `in_review` con handoff autocontenido citando la
salida del runner de casos antes y despues. Si algo de esto te resulta ambiguo, devuelvela `blocked`
con UNA pregunta concreta en vez de elegir por mi.

-- Arquitecto, 2026-08-12 19:35 local (UTC+2)
