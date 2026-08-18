---
message_id: MSG-20260818-Arquitecto-to-Operador-RESP-veredicto-0410-y-el-198-retirado
from: Arquitecto
to: Operador
type: FYI
task_id: TASK-0410
status: open
requires_response: false
one_line_summary: Veredicto de 0410 CHANGE-REQUIRED por RES-3; confirmo r1 con RES-3 DENTRO y no a tarea propia. Y retiro un cardinal MIO - el "0 de 198" de mi GO no re-deriva contra ninguna poblacion del arbol.
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0410-paridad-gemelos-verdict.md
  - Area_comun/mailbox/archived/MSG-20260818-Arquitecto-to-Codex-GO-TASK-0410.md
  - Area_comun/mailbox/open/MSG-20260818-Arquitecto-to-Codex-ACTION-TASK-0410-r1.md
---

# Veredicto de TASK-0410, y un cardinal mio retirado

2026-08-18 18:36 local (UTC+2).

**Por que va a tu canal y no al del checker:** el checker me pregunto directamente y le debo la
respuesta, pero un mensaje mio a su buzon con un `task_id` valido le arranca un exec, y ahora mismo
tiene dos encargos reales en cola -- el re-juicio de 0397 r3, que acaba de morir por un
`API Error: 529 Overloaded` del proveedor y esta reintentando, y la review de 0408. Gastar uno de sus
brazos en leerme seria caro. La respuesta queda en el registro y la enlace desde los `context_refs`
del r1: el checker la leera cuando re-juzgue, que es cuando la necesita.

## El veredicto: seis de siete cortes PASAN

    AC1 divergencia por causa                       PASS
    AC2 borrado con el 2x2 de la posicion           PASS
    AC3 mutacion sobre produccion, mismo mensaje    PASS
    AC4 detector de coordenadas muertas como clase  PASS
    cardinal derivado -- vacuidad                   PASS, no vacuo
    E6 masters Markdown                             PASS en mecanismo
    RES-3 paridad por caja                          SLIPS -- BLOQUEANTE

El corte que mas me preocupaba **aguanto**: el cardinal derivado no es vacuo. El checker perturbo UNA
sola fuente y el test enrojece; con la paridad neutralizada el cardinal dispara solo (`88 != 89`), y
el control nulo sale verde. Las dos fuentes son independientes de verdad. Y el verde es discriminante:
el codigo viejo da exit 1.

## El bloqueante, y por que no lo aplazo

El maker reparo el EJEMPLO -- los globs con `-cmatch` -- y no la CLASE. La busqueda de exenciones
sigue con pertenencia insensible a caja en `ContainsKey` (:254) y `-contains` (:269), frente al
`.get()` e `in` sensibles del gemelo Python. Medido en clon limpio: **Python exit 1 nombrando el
fichero, PowerShell exit 0 en silencio**. PowerShell es el permisivo: **exime una fuga real**.

Y es alcanzable donde importa: el job que ejecuta el gemelo `.ps1` corre en
`[self-hosted, protocol-linux]`, un FS sensible a mayusculas donde `scripts/harness/` y
`scripts/Harness/` pueden coexistir. La suite entera da exit 0 con el escape vivo, porque la asercion
de paridad compara DECLARACIONES y no comportamiento.

**Confirmo r1 con RES-3 dentro**, y no a tarea propia, por tres razones:

1. El `out_of_scope` de la propia 0410 ya lo resolvio: un tercer dueno sobre los gemelos del escaner
   es la colision que costo dos intervenciones con reloj hoy.
2. Un escape alcanzable que exime una fuga real no se aplaza a una tarea futura.
3. 0410 **es** la tarea que gobierna la paridad de los gemelos. Cerrarla con los gemelos dando
   veredictos opuestos sobre la misma entrada seria cerrarla por su letra y no por su proposito.

Al maker le pido algo mas que el arreglo: **el censo del fichero completo** de operadores insensibles
a caja, con lo que arregla y lo que deja justificado. Esta clase ya reaparecio una vez por otra
coordenada despues de una remediacion.

## Lo que tengo que corregirme

Mi GO decia **"el escaner escanea 0 de 198 ficheros bajo claude-skills"**. El checker me pidio
re-derivarlo y no aguanta:

    scripts/instance_assets/claude-skills/    5 ficheros (todos .md)
    .md bajo scripts/ (todo)                  8
    ficheros bajo scripts/ (todo)           125
    ficheros bajo .claude/                   13

No hay lectura razonable de este arbol que de 198. **Lo retiro.** El numero re-derivable es el del
checker: 144 -> 152 ficheros admitidos por la seleccion del escaner, `.md` bajo `scripts/` 0/8 -> 8/8,
bajo `claude-skills` 0/5 -> 5/5.

No se me escapa donde ocurrio: publique un cardinal no re-derivable **en el GO de la tarea que existe
porque los cardinales no re-derivan**, y es la segunda vez hoy que un numero mio mueve el suelo de una
entrega -- la primera fue el censo de 0397, que tumbo su AC4. Va a la memoria como regla y no como
anecdota: **un cardinal en un GO se re-deriva antes de escribirlo, igual que uno en un handoff.** El
que rutea no esta exento de la regla que exige.

## Tres residuales, y donde los pongo

**RES-A, el enmascaramiento -- el hallazgo mas valioso del veredicto.** El control de coordenadas
muertas existe y dispara, pero vive rio abajo de la asercion de paridad **en el mismo metodo**: cualquier
divergencia de inventario lo enmascara entero. Eso explica por que tres coordenadas muertas
sobrevivieron "con el control declarandose sano". No es de 0410: es la clase "un control cuyo disparo
depende de que OTRO control pase primero".

**RES-B, el cardinal subsumido.** La linea del cardinal no puede ser jamas la asercion que falla --
mismo defecto estructural que RES-A. Va con ella.

**RES-C, mio:** los 10 `.md` bajo `.claude/skills/` siguen en 0/10, por estar fuera de `scripts/**`.
E6 se entrego como se especifico, asi que no ensancho 0410 por tercera vez.

Los registro como tareas propias en la proxima ventana de ledger, no en esta.

## Estado

Cola del maker: 1 (0410 r1). Cola del checker: 2 (0397 r3 reintentando tras el 529, 0408 r1).
`validate` 0. Fondo intocable verificado por el checker en clon limpio: `protocol.config.json` con
sha256[:8] `2E35F26E`, epoch `1.14.0`, cero lineas de diff.

**Poda VENCIDA** y sin correr: exige arbol quieto y no ha habido ventana sin exec de peon.
