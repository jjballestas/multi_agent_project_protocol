---
id: TASK-0388
title: Las exenciones del gate de neutralidad estan ancladas a un NUMERO DE LINEA -- editar un test obliga a editar el gate, y un numero mal deja el gate ciego sin enrojecer nada
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0388-las-exenciones-del-gate-estan-ancladas-a-una-coordenada.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Hallazgo del Arquitecto al revisar la remediacion r1 de TASK-0373. `scripts/scan_domain_neutrality.ps1`
    mantiene su tabla `IdentityLiteralExemptions` indexada por **NUMERO DE LINEA** del fichero
    vigilado: `Lines = @{ 204 = @("<sha>"); 237 = @("<sha>") ... }`. Codex anadio 75 lineas a
    `scripts/memory/test_memory_db.py` para remediar F2 y **tuvo que renumerar las exenciones del
    gate** -- 54 lineas cambiadas en un fichero que estaba FUERA de los `scope_routes` de 0373.
    Tres consecuencias, en orden creciente de gravedad: (1) cambiar un test obliga a editar un GATE,
    acoplando por posicion el control y lo controlado; (2) la exencion queda anclada a una COORDENADA
    y no a la propiedad que pretende eximir, que es la familia de defectos que este repo lleva
    catalogando (contratos atados a la forma y no al efecto); (3) **un numero mal renumerado exime la
    linea EQUIVOCADA**, dejando el gate ciego en un punto arbitrario del fichero **sin que nada
    enrojezca** -- el gate pasa igual, porque pasar es justamente lo que hace cuando no mira. Un
    control cuya cobertura se desplaza en silencio al editar otro fichero no es un control: es una
    coincidencia mantenida a mano.
  acceptance:
    - "AC1 (la exencion se ancla al CONTENIDO, no a la posicion): la tabla identifica lo eximido por
      una propiedad estable del propio texto -- su hash, ya presente en la tabla, o un marcador
      explicito en el fichero vigilado -- de modo que insertar o borrar lineas ANTES de una exencion
      no la invalide ni la desplace. Se acredita insertando N lineas al principio del fichero
      vigilado y comprobando por exit code que el gate sigue eximiendo lo mismo y NO eximiendo lo
      demas."
    - "AC2 (prueba de que RECHAZA, no de que pasa): con el anclaje nuevo, una identidad introducida
      en una linea NO eximida pone el gate en exit 1, y la salida nombra fichero y linea. Ejecutado,
      con su salida y su exit code. Un gate que nunca ha dicho que no en esta configuracion no esta
      demostrado."
    - "AC3 (el desplazamiento silencioso muere): se reproduce el defecto -- desplazar el contenido de
      forma que una exencion por numero cubra otra linea -- y se comprueba que con el anclaje nuevo
      ese caso YA NO puede ocurrir, o que si ocurre el gate lo DICE. Es el nucleo del hallazgo."
    - "AC4 (editar un test deja de editar el gate): tras el cambio, anadir lineas a
      `scripts/memory/test_memory_db.py` no requiere tocar `scan_domain_neutrality.ps1`. Se acredita
      con el par: antes exigia renumerar, ahora no."
    - "AC5 (el camino feliz no se rompe): las exenciones legitimas vigentes siguen eximiendo tras la
      migracion, una por una. Medido, no afirmado -- la migracion no puede perder cobertura NI
      ensancharla."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
  scope_routes:
    - scripts/scan_domain_neutrality.ps1
  out_of_scope:
    - "El equivalente en Python del escaner de neutralidad, si existe otra ruta con la misma tabla:
      se declara si aparece, pero esta tarea cierra el vector de `scan_domain_neutrality.ps1`."
    - "TASK-0372 (el escaner solo ve los nombres que la instancia declara): es el hermano -- aquel
      es QUE mira, este es DONDE mira. No se mezclan en una entrega."
    - "Revisar si las exenciones vigentes estan JUSTIFICADAS. Esta tarea preserva la cobertura tal
      como esta; auditar su contenido es otra tarea."
  risk: medium
  estimate: S
---

# TASK-0388 -- la exencion anclada a una coordenada

## Lo observado

En `4a9b6a12` (remediacion r1 de TASK-0373):

    scripts/scan_domain_neutrality.ps1 | 108 ++++++++++-------------
    1 file changed, 54 insertions(+), 54 deletions(-)

    -            204 = @("1a05b53aa...", "fcfd3ebc...")
    +            205 = @("1a05b53aa...", "fcfd3ebc...")
    -            237 = @("57de4cf...")
    +            238 = @("57de4cf...")

El fichero **no estaba en los `scope_routes` de 0373**. Se toco porque no habia alternativa: anadir
tests desplaza las lineas que el gate tiene apuntadas.

## Por que no es cosmetico

El gate seguira dando exit 0 tanto si la renumeracion es correcta como si no. **Su verde no
distingue** entre "estoy eximiendo lo que debo" y "estoy eximiendo otra cosa". La unica senal
posible seria un falso positivo ruidoso, y solo si la linea equivocada resulta contener una
identidad; en el caso normal, el gate simplemente deja de vigilar un trozo y nadie se entera.

Nota: la tabla YA lleva el hash del contenido eximido junto al numero. La informacion para anclar por
contenido esta ahi; lo que falta es usarla como clave en vez de como acompanante.
