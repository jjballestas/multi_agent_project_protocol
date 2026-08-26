---
id: TASK-0410
title: La paridad de inventario de identidad diverge entre gemelos y su censo no cuadra -- 92 contra 91, con tres coordenadas muertas
status: done
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
created: 2026-08-16
reviewer: Analista
intake:
  type: infra
  goal: >
    Aislado por el checker al cerrar TASK-0337 y declarado por el HEREDADO, no atribuible a esa
    entrega: el contrato `NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY` esta ROJO en
    `scripts/test_scan_domain_neutrality.py`, cableado en CI en `.github/workflows/validate.yml:522`.
    Dos sintomas medidos que probablemente son el mismo defecto: UNA divergencia de inventario entre
    el gemelo Python y el gemelo PowerShell, y TRES coordenadas MUERTAS en `runtime/context.py` --
    exenciones que apuntan a lineas que ya no contienen lo que decian vigilar. El censo sale 92
    frente a 91. Es la QUINTA aparicion en 24h del mismo patron -- controles anclados a una
    coordenada que el sistema cambia por diseno -- despues de las 353 fronteras por texto literal
    (0397), las 164 exenciones por numero de linea (0388), el pin del gancho (0378) y el ID de tarea
    clavado en un test (0409). Aqui el ancla no solo diverge: apunta a vacio, y el control sigue
    declarandose sano.
  acceptance:
    - "AC1 (cerrar la divergencia por su causa, no por su numero): igualar el censo a 92==92 subiendo
      un contador NO acredita. Hay que decir CUAL es la divergencia de inventario, POR QUE existe, y
      si el gemelo que declara de menos esta siendo mas permisivo o mas estricto -- eso decide si el
      arreglo es anadir la exencion o quitarla. Se declara antes de tocar."
    - "AC2 (las tres coordenadas muertas): identificar las tres exenciones de `runtime/context.py`
      que apuntan a lineas que ya no contienen su objeto, y decidir por cada una si el objeto se
      movio (se re-ancla) o si desaparecio (se borra la exencion). Una exencion muerta es peor que
      ninguna: exime algo que ya no existe y podria estar tapando una violacion nueva en esa linea."
    - "AC3 (el negativo, por MUTACION): con la paridad restituida, mover el objeto vigilado debe
      hacer FALLAR a los DOS gemelos con el mismo mensaje. Si solo falla uno, la paridad no esta
      acreditada -- que es exactamente lo que ya paso con el gemelo de 0337."
    - "AC4 (detectar coordenadas muertas, no solo arreglar estas tres): un control que marque las
      exenciones cuyo objeto ya no esta en la linea declarada. Sin el, la clase se repara hoy y
      vuelve manana con otras coordenadas."
  verification_cmd:
    - "python scripts/test_scan_domain_neutrality.py"
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/test_scan_domain_neutrality.py
    - scripts/scan_domain_neutrality.py
    - scripts/scan_domain_neutrality.ps1
  out_of_scope:
    - "AMPLIACION 2026-08-18 11:55 local (Arquitecto) -- no es exclusion, es un caso que ENTRA:
      RES-3 del veredicto de TASK-0394 r2. La lista negra esta espejada en CONTENIDO pero NO en
      COMPORTAMIENTO: `ContainsKey` de una hashtable de PowerShell es INSENSIBLE a mayusculas y la
      pertenencia a un `set` de Python no lo es. Reproducido por el Arquitecto:
      `Secrets/leak.py` -> Python exit 1 nombrando el fichero, PowerShell exit 0. Los dos gemelos
      dan veredictos OPUESTOS sobre la misma entrada, que es exactamente la paridad que esta tarea
      gobierna -- por eso entra aqui y no en tarea propia: crear un tercer dueno sobre
      scan/upgrade_instance.{py,ps1} es la colision que costo dos intervenciones con reloj el
      18-ago. Se resuelve aqui, no en tarea aparte."
    - "Las otras cuatro variantes del patron de coordenada fragil (0397 fronteras literales, 0388
      exenciones por linea, 0378 pin literal, 0409 ID de tarea clavado): cada una tiene su via."
    - "Igualar el censo tocando el numero esperado sin explicar la divergencia: descartado
      explicitamente -- repara la corrida y deja la clase intacta."
    - "El rediseno de como se declaran las fronteras de los controles: es la DECISION que estas cinco
      tareas juntas justifican, y va aparte."
  risk: low
  estimate: S
---

# TASK-0410 -- el inventario de identidad que diverge y ademas apunta a vacio

## Origen

Lo aislo el checker al dar OK-CLOSABLE a TASK-0337, y lo declaro **heredado y no atribuible** a esa
entrega. Condicion de publicacion S-1 del paquete para instancias.

## Lo medido

    NEG-NEUTRALITY-IDENTITY-INVENTORY-PARITY   ROJO
      runner   scripts/test_scan_domain_neutrality.py
      cableado .github/workflows/validate.yml:522
      censo    92 frente a 91
      causas   1 divergencia de inventario entre gemelos
               3 coordenadas MUERTAS en runtime/context.py

## Lo que hace a este caso distinto de los otros cuatro

En 0397, 0388, 0378 y 0409 el ancla **divergia**: apuntaba a otro sitio. Aqui hay tres anclas que
apuntan **a vacio** -- exenciones cuyo objeto ya no esta en la linea declarada -- y el control
sigue declarandose sano. Una exencion muerta no es inocua: **exime algo que ya no existe, y puede
estar tapando una violacion nueva en esa misma linea**.

Por eso el AC4 pide el detector y no solo el arreglo: sin el, la clase se repara hoy y vuelve
manana con otras tres coordenadas.
