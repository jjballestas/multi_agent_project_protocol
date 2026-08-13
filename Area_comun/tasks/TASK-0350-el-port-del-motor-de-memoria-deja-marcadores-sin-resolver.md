---
id: TASK-0350
title: El port del motor de memoria mete un fichero con marcadores sin resolver en la instancia generada
status: done
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
created: 2026-08-09
intake:
  type: fix
  goal: >
    El paso 50 del job `validate` (`examples/runtime_instantiation_cases`) muere en checkout limpio
    con `Unresolved placeholders remain in generated instance: scripts/memory/test_memory_db.py`, y
    el instanciador ABORTA la creacion entera de la instancia. La consecuencia no es cosmetica: hoy
    no se puede parir una instancia nueva del protocolo, y esta tarea es una de las de la cascada que
    mantiene rojo el gate canonico. El instanciador decide si un fichero quedo a medio renderizar
    mirando una FORMA de texto; hay que determinar si esa forma nombra de verdad la propiedad
    "marcador que yo debia sustituir y no sustitui", y corregir la que se equivoque -- el detector,
    el fichero, o el hecho de que el motor de memoria viaje en el copiado. Lo que NO vale es apagar
    el sintoma para este fichero: la clase de defecto que esta instancia lleva semanas desterrando es
    exactamente esa, arreglar por enumeracion en vez de por criterio.
  acceptance:
    - "AC1 (la causa se nombra por criterio, no por lista): se declara que clase de texto esta
      confundiendo el instanciador con un marcador sin resolver, y por que la confusion es de FORMA y
      no de contenido. No acredita citar los literales concretos que hoy disparan el fallo: acredita
      el criterio de pertenencia que separa `marcador que el instanciador debia sustituir` de `texto
      del producto que solo se le parece`. Sobre ese criterio se elige UNA de las tres salidas del
      enunciado -- resolver el fichero como plantilla, excluirlo del copiado, o que el motor de
      memoria no viaje en el instanciador -- y se declara por que las otras dos se descartan."
    - "AC2 (el negativo discrimina: el positivo real sigue muriendo): tras el cambio, un marcador
      GENUINO sin resolver sigue abortando la instanciacion. Se acredita inyectando en la instancia
      generada un marcador de la forma que el instanciador si sustituye y observando el fallo con su
      exit code. Un cambio que haga pasar el caso y ademas deje pasar el marcador real no acredita
      nada: es el falso verde que este AC existe para impedir, y se mide con el PAR (sucio muere,
      limpio pasa), no con una declaracion."
    - "AC3 (supervivencia al cambio de coordenada): la correccion no puede depender del fichero
      concreto, ni de su numero de linea, ni de los literales que hoy la disparan. Se acredita
      mudando el texto ofensor a OTRO fichero del motor y a otra forma de la MISMA clase, y
      comprobando que el resultado no cambia. Si la correccion es una lista de excepciones -- de
      ficheros, de rutas o de literales -- este AC la mata."
    - "AC4 (medidas las DOS direcciones): se compara el conjunto de ficheros que el detector marca
      sobre la instancia generada ANTES y DESPUES del cambio, derivado de una corrida real y no
      afirmado. La diferencia tiene que ser EXACTAMENTE la que el criterio de AC1 explica: ni un
      fichero perdido (deja de cazarse algo que se cazaba) ni uno ganado. Ensanchar un patron puede
      estrecharlo, asi que se reporta la tabla en las dos direcciones."
    - "AC5 (ENMENDADO 2026-08-12 20:20 -- la causa muere, y el paso 50 no lo cierra esta tarea): la
      version original pedia el caso ENTERO verde mientras declaraba otras causas fuera de alcance;
      era contradictoria y el defecto es del encargo, no de la entrega. Lo que acredita: (a) la firma
      del fallo se MUEVE -- antes el caso aborta en el chequeo de marcadores, despues pasa la
      generacion y cae mas adelante; (b) el residuo se nombra por su causa y se prueba PREEXISTENTE,
      derivandolo del diff (esta tarea toca `scripts/new_instance.py` y el runner de casos, asi que
      lo que falla fuera de esas rutas no lo introdujo ella); (c) el residuo se transfiere a una
      tarea CONCRETA que lo acepta, citada por id. `Sigue rojo pero es de otro` sin ese id no
      acredita: es como un rojo sobrevive meses. El paso 50 lo cierra TASK-0367, no esta."
    - "AC6 (declarado el destino del motor en la instancia): se declara que queda en la instancia
      generada respecto del motor de memoria segun la salida elegida en AC1: si viaja, sigue siendo
      ejecutable ahi; si no viaja, se dice explicitamente."
  verification_cmd:
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/new_instance.py
    - scripts/memory/test_memory_db.py
    - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  out_of_scope:
    - "La SEGUNDA causa del paso 50 -- la identidad de esta instancia cableada en el nucleo, que el
      escaner de neutralidad caza sobre la instancia GENERADA: es TASK-0367, abierta para ella. NO es
      de TASK-0347, que declara el paso 50 fuera de su alcance y se lo asigna por nombre a esta."
    - "Los quince rojos de causa `obstacles` del job validate: son TASK-0347, no esta."
    - "El resto de la cascada del gate (TASK-0349, TASK-0351, TASK-0352): cada una tiene su propia
      causa y su propia tarea; no se arreglan de paso aqui."
    - "El comportamiento del motor de memoria mas alla del texto que causa el falso positivo: la
      review formal de SPEC-MEMORIA-HIBRIDA va por su propio canal al checker."
    - "El corte de la CI a runners propios (TASK-0364): cambia el HOST del gate, no sus pasos."
  risk: low
  estimate: S
---

# TASK-0350 -- marcadores sin resolver en la instancia generada

Paso 50 del job `validate` (`examples/runtime_instantiation_cases`), en checkout limpio a HEAD:

    case_coordination_default_and_flag
    ERROR: Unresolved placeholders remain in generated instance: scripts/memory/test_memory_db.py

El instanciador copia el motor de memoria a la instancia nueva sin resolver sus marcadores. Toca
justo el trabajo de memoria hibrida de esta jornada (TASK-0327/0328), asi que importa doble: una
instancia recien nacida arrastraria el fichero roto.

Determinar si el fichero debe resolverse como plantilla, excluirse del copiado, o si el motor de
memoria no deberia viajar en el instanciador. Declarar cual y por que.

Fuera de alcance: los quince rojos de causa `obstacles` (TASK-0347).

## Lo que el enunciado daba por hecho y conviene mirar

El enunciado de arriba se escribio desde el mensaje de error, y el mensaje de error afirma una cosa:
que hay marcadores **sin resolver**. Esa afirmacion es del instrumento, no del arbol -- y en esta
instancia una afirmacion de un instrumento se verifica, no se hereda. Antes de elegir entre las tres
salidas conviene establecer si lo que el detector encontro es un marcador que el instanciador debia
sustituir, o texto del producto cuya forma coincide con la del marcador.

La diferencia decide la tarea entera. Si es lo primero, el fichero esta roto y las tres salidas del
enunciado son las candidatas. Si es lo segundo, el fichero esta bien y quien se equivoca es el
detector: excluir el fichero o sacar el motor del copiado seria apagar un instrumento que dice la
verdad en 99 casos por el caso 100 donde su FORMA no nombra su PROPIEDAD -- y ademas dejaria pasar,
callado, al siguiente fichero del producto que caiga en la misma coincidencia.

Por eso AC1 pide el criterio de pertenencia y no la lista, AC3 exige que la correccion sobreviva a
mudar el texto de coordenada, y AC4 mide las dos direcciones: la remediacion no puede estrechar el
detector para el positivo real mientras lo ensancha para el falso.

## Nota de metodo

Esta tarea es pequena de codigo y grande de criterio. El fallo cuesta un cambio corto; lo que se
compra con los AC es que el cambio no reintroduzca el patron por otra coordenada, que es como esta
clase de defecto ha vuelto tres veces en las ultimas dos semanas.
