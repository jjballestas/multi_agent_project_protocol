---
id: TASK-0372
title: El gate de identidad solo ve los nombres que la propia instancia declara, y una instancia adoptada nace con ochenta apariciones del equipo autor que su puerta no mira
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0372-el-gate-de-identidad-solo-ve-los-nombres-que-la-propia-instancia-declara.md
created: 2026-08-13
intake:
  type: fix
  goal: >
    Bloqueante B1 del veredicto formal de TASK-0367, sacado a tarea propia por decision del
    Arquitecto. El escaner de identidad **deriva sus terminos prohibidos de la configuracion de la
    instancia que escanea**, asi que solo caza una identidad heredada cuando coincide con un nombre
    que la instancia nueva se puso a si misma. El checker lo midio: enveneno `runtime/context.py` del
    hub con una identidad, genero una instancia nueva, y **su propio escaner salio exit 0 con la
    identidad presente en el arbol**. Con nombres de adoptante real la instancia generada nace con
    **80 apariciones** (tier coordination) y **98** (tier runtime) de identidades del equipo autor, y
    su puerta no ve ninguna. Entre ellas hay defectos vivos, no solo texto: `runtime/apply.py:440`
    con `transition.get("owner", "Codex")` y `scripts/prune_state.py:272` con
    `state["updated_by"] = "Codex"`. La consecuencia es que la garantia que TASK-0367 perseguia --
    que una instancia generada no herede la identidad de quien escribio el protocolo -- **no se
    cumple hoy**, y lo que es peor, el instrumento que deberia detectarlo dice que si.
  acceptance:
    - "AC1 (el instrumento deja de ser ciego por construccion): el escaner de identidad detecta una
      identidad AJENA a la instancia escaneada, no solo las que su propia config declara. Se acredita
      por conducta con el experimento del checker: envenenar el nucleo del hub con una identidad,
      generar una instancia, y exigir que su gate salga distinto de cero. Hoy sale 0."
    - "AC2 (la cobertura de rutas se DERIVA, no se presume): se declara que rutas barre el escaner y
      por que. El checker reporta ceguera a rutas no-`.py`; el criterio de que entra al barrido tiene
      que salir de la propiedad `esto viaja en la instancia generada`, no de una extension."
    - "AC3 (la poblacion real se mide y se reporta): se cuenta cuantas apariciones de identidad del
      equipo autor quedan en una instancia generada de cada tier, antes y despues, con el conteo
      derivado de una corrida y no afirmado. El checker midio 80 y 98 como linea de partida; si tu
      medicion da otra cifra, se declara la diferencia y su causa."
    - "AC4 (los defectos vivos se corrigen, no solo el texto): `runtime/apply.py:440` y
      `scripts/prune_state.py:272` no son prosa: son valores por defecto que la instancia adoptada
      ejecutaria. Se corrigen por el mismo criterio de TASK-0367 -- valor generico o valor derivado de
      la config -- y se declara cual se eligio para cada uno."
    - "AC5 (el negativo discrimina en las DOS direcciones): tras el cambio, una identidad ajena
      inyectada pone rojo el gate Y el estado sano sigue verde. Un instrumento que se ponga rojo
      tambien sin veneno no acredita nada; y el conteo de AC3 no puede bajar porque el escaner deje
      de mirar."
  verification_cmd:
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_domain_neutrality.py
    - runtime/apply.py
    - scripts/prune_state.py
    - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
  out_of_scope:
    - "La resolucion del ejecutable del agente por proveedor y la contradiccion del README del
      scaffold: son B2 de la remediacion de TASK-0367, no esta."
    - "La interferencia del caso nuevo de 0367 con el sandbox compartido de la suite de retry: es B3
      de la misma remediacion."
    - "Los cuatro sitios que TASK-0367 ya corrigio: el checker confirma que siguen intactos y
      neutrales. No se re-abren."
  risk: medium
  estimate: M
---

# TASK-0372 -- la puerta que solo ve lo que ya sabe

## Como se midio

Veredicto formal de TASK-0367, bloqueante B1. El experimento es limpio y no admite lectura amable:

    envenenar runtime/context.py del HUB con una identidad
    generar una instancia nueva
    correr SU escaner  ->  exit 0, con la identidad presente en su arbol

El escaner deriva los terminos prohibidos de la config de la instancia que mira. Una instancia
adoptada por otro equipo se llama a si misma con otros nombres, asi que las identidades del equipo
AUTOR le resultan invisibles: no estan en su lista porque su lista habla de ella misma.

## Por que esto es mas grande que TASK-0367

0367 corrigio cuatro sitios y su negativo permanente parecia sostenerlo. Pero ese negativo solo
prueba lo que la instancia ya sabe nombrar. Con nombres de adoptante real quedan **80 y 98**
apariciones segun el tier -- y dos de ellas no son texto:

    runtime/apply.py:440        transition.get("owner", "Codex")
    scripts/prune_state.py:272  state["updated_by"] = "Codex"

Eso son valores por defecto que la instancia adoptada **ejecuta**. Atribuiria acciones a un actor que
no existe en su registro.

## Por que sale a tarea propia y no se cuela en la remediacion

El checker pregunto si preferia ensanchar el negativo permanente dentro de 0367 o narrar la
limitacion y sacar la brecha aparte. Sale aparte, y la razon es de frontera: **ensanchar un encargo
desde su review es la misma clase de defecto que el encargo persigue**, y el propio checker se nego a
hacerlo en TASK-0350 por ese motivo exacto. No puedo aceptar esa frontera cuando cierra una tarea y
rechazarla cuando cuesta abrir otra.

Lo que si se corrige dentro de 0367 es la NARRACION de su AC3: que declare lo que caza -- una
identidad que la instancia declara -- y lo que no.
