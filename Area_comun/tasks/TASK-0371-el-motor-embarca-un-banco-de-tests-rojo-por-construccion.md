---
id: TASK-0371
title: Cada instancia generada embarca un banco de 72 tests que esta rojo por construccion el dia que nace
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0371-el-motor-embarca-un-banco-de-tests-rojo-por-construccion.md
created: 2026-08-13
intake:
  type: fix
  goal: >
    Observacion nueva del veredicto formal de TASK-0350, senalada por DECISION-0018 y explicitamente
    declarada como NO perteneciente a esa tarea. El motor de memoria viaja en el instanciador y es
    ejecutable en la instancia generada -- eso es cierto y esta medido --, pero su banco de 72 tests
    NO esta verde en una instancia recien nacida: 3 errores en seco y 70/72 tras darle un commit
    inicial. El checker persiguio las tres hasta su traza y ninguna es del motor: una es
    `git rev-parse HEAD` sobre un repo todavia sin commit (desaparece al commitear, lo que cierra el
    diagnostico), otra pide `scripts/new_instance.py`, que una instancia no embarca por diseno, y la
    tercera es un `assertGreater(len(object_ids), 100)` que recibe 1 porque el corpus ES la historia
    git y una instancia recien parida no tiene historia. Las tres son suposiciones del banco sobre el
    entorno del HUB que no valen en una instancia. El efecto practico es que un equipo que instancia
    el protocolo hereda una suite roja el primer dia, sin manera de distinguir "el motor esta mal" de
    "estos tests no aplican todavia aqui".
  acceptance:
    - "AC1 (la clase se nombra, no se enumera): se declara que propiedad comparten los casos que no
      valen en una instancia recien nacida -- suponen historia git, suponen ficheros que la instancia
      no embarca, o suponen un corpus por encima de un tamano. Las tres observadas son el sintoma; el
      criterio es lo que decide que se hace con cada una y con las que aparezcan."
    - "AC2 (cada caso va a su destino declarado): para cada caso de la clase se elige UNA salida y se
      dice por que -- que se salte declarando su precondicion, que se adapte para valer en los dos
      entornos, o que no viaje al instanciador. Dejar la suite roja y documentarlo NO acredita: el
      objetivo es que el primer dia sea distinguible de una averia."
    - "AC3 (medido en una instancia REAL recien parida): la suite se corre en una instancia generada
      de cero, antes y despues, con exit code y el saldo de casos. El estado 'antes' incluye los dos
      escenarios que el checker separo: en seco y tras el commit inicial, porque dan resultados
      distintos y confundirlos oculta la causa."
    - "AC4 (no se debilita en el hub): los mismos casos siguen ejerciendo lo que ejercian cuando
      corren en el hub, donde las suposiciones SI valen. Se acredita con el saldo del hub antes y
      despues: un caso que en el hub deje de probar lo que probaba es una perdida de cobertura
      disfrazada de portabilidad."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/memory/test_memory_db.py
    - scripts/new_instance.py
  out_of_scope:
    - "El comportamiento del motor de memoria: no esta en cuestion. Lo que falla son las suposiciones
      de sus TESTS sobre el entorno, no el motor."
    - "La invariante clave-a-gramatica sin guardia: es TASK-0370."
    - "Los dos bloqueantes de la review formal de la SPEC (TASK-0368 y TASK-0369): otra cosa."
  risk: low
  estimate: M
---

# TASK-0371 -- la suite que nace roja

## Por que nadie lo habia visto

Lo dice el propio checker, y es la parte que mas me interesa:

> Hasta este commit la generacion abortaba, asi que nadie habia podido observar que el motor embarca
> en cada instancia un banco de 72 tests **rojo por construccion en una instancia recien nacida**.
> 0350 no lo introdujo: 0350 es lo que lo hizo visible.

Es el mismo patron que ya nos dio TASK-0367: **una puerta que aborta pronto oculta lo que hay
detras**. Cada vez que se mata una causa temprana hay que presupuestar que aflore la siguiente, y
tratarla como hallazgo nuevo, no como regresion.

## Lo que esta realmente en juego

No es la estetica de un rojo. Un equipo que instancia el protocolo corre la suite el primer dia y ve
tres fallos. Sin nada que los distinga, tiene que elegir entre dos lecturas incompatibles -- "el
motor que me acaban de dar esta roto" o "estos tests no aplican aqui todavia" -- y la unica manera de
resolverlo es leer las trazas una a una, que es justo lo que el checker tuvo que hacer.

Una instancia nace operativa o no nace. Una suite que nace roja por construccion gasta la confianza
del primer dia, que es la mas cara.
