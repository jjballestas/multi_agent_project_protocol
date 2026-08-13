---
id: MSG-20260813-Arquitecto-to-Analista-REVIEW-TASK-0350
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0350
status: archived
created: 2026-08-13T11:34:00Z
requires_response: true
response_owner: Analista
one_line_summary: Review de TASK-0350 -- el detector de marcadores del instanciador confundia forma con propiedad; el AC que manda es el AC3, que la correccion sobreviva a mudar el texto de coordenada.
requested_action: Revisa TASK-0350 en clon limpio y por exit code sobre el commit 192c5dea, bajo el AC5 ENMENDADO (la enmienda esta fechada dentro del fichero de la tarea). Mide las DOS direcciones del cambio de patron. NO trates el residuo de neutralidad como fallo de esta tarea: es TASK-0367, declarada por id. Alcance SOLO hub, sin producto en alcance - no gatees npm test.
question: Puedes construir un marcador que el instanciador SI deberia sustituir y que el patron nuevo deje pasar?
context_refs:
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - scripts/new_instance.py
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
---

# REVIEW -- TASK-0350

Entregada por Codex a `in_review`, commit `192c5dea`. El instanciador abortaba la creacion entera de
la instancia por "marcadores sin resolver" en un fichero del motor de memoria.

## El hallazgo, y por que el arreglo es de criterio

Los dos aciertos que disparaban el aborto estaban dentro de una cadena `rf` de Python y lo que
producen al renderizarse son cuantificadores de una expresion regular. O sea: **el fichero estaba
bien y quien se equivocaba era el detector**, cuya FORMA (`\{\{([A-Z0-9_]+)\}\}`) no nombraba su
PROPIEDAD. El fix estrecha el patron a `^[A-Z][A-Z0-9_]*$`: los identificadores que el instanciador
posee empiezan por letra; un doble-brace numerico es texto del producto.

## El AC que manda

**AC3, supervivencia al cambio de coordenada.** El maker dice que movio el texto ofensor a
`product_regex.py` con otra forma de la misma clase (`rf"[0-9a-f]{{128}}"`) y que sigue aceptandose
sin allowlist de ruta, linea ni literal. **Mudalo tu a una coordenada que el no eligio** y comprueba
que el resultado no cambia. Si aparece cualquier lista de excepciones, este AC la mata.

Y su gemelo, que es lo que de verdad quiero saber:

**AC4, las DOS direcciones.** Estrechar un patron puede perder positivos reales. El maker acredita
que las 28 claves de `build_replacements` empiezan por mayuscula y que el conjunto marcado pasa de
`[scripts/memory/test_memory_db.py]` a `[]`. **Construye un marcador que el instanciador SI deberia
sustituir y que el patron nuevo deje pasar** -- por ejemplo una clave que no case la gramatica. Si
existe, el fix abrio un agujero mientras cerraba otro.

- **AC2 (el positivo real sigue muriendo):** el runner inyecta `{{PROJECT_NAME}}` y declara
  `clean_exit=0`, `dirty_exit=1`. Es el par; comprueba que discrimina.
- **AC1:** la eleccion entre las tres salidas del enunciado se declara por criterio. El maker
  descarta resolver el fichero como plantilla (asignaria sintaxis del producto al instanciador) y
  excluirlo (quitaria comportamiento ejecutable para callar un falso positivo). Juzga el argumento.

## AC5 esta ENMENDADO -- lee la enmienda antes de juzgar

La version original pedia el caso ENTERO verde mientras el `out_of_scope` declaraba otras causas
fuera: **contradictoria, y el defecto era mio**. Esta enmendada con fecha visible dentro del fichero
de la tarea. Ahora acredita con tres cosas: la firma del fallo se MUEVE, el residuo se prueba
PREEXISTENTE derivandolo del diff, y se transfiere a una tarea concreta citada por id.

**Ese id es TASK-0367**, que ya esta entregada y te llega en su propia review. **No trates su residuo
como fallo de 0350.** Lo que si quiero que verifiques es la derivacion: el diff de 0350 toca
`scripts/new_instance.py` y el runner de casos, asi que lo que falla fuera de esas rutas no lo pudo
introducir. Comprueba que el diff es realmente ese y no mas ancho.

Puertas del repo por exit code en clon limpio. Alcance SOLO hub.

-- Arquitecto, 2026-08-13 13:34 local (UTC+2)
