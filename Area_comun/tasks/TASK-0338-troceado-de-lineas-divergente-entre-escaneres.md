---
id: TASK-0338
title: Los dos escaneres no comparten la definicion de LINEA a la que atan las coordenadas
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0338-troceado-de-lineas-divergente-entre-escaneres.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    SLIP-2 del veredicto r2 de TASK-0329. El escaner Python trocea con `str.splitlines()`, que
    rompe tambien en form feed, tabulador vertical, NEL y U+2028; el gemelo PowerShell trocea con
    `Get-Content`, que no rompe en ninguno de esos. Como las exenciones estan atadas a NUMEROS DE
    LINEA, una discrepancia de troceado se convierte en discrepancia de VEREDICTO. Es el UNICO
    camino encontrado en que el gemelo falla ABIERTO, y afecta sobre todo a instancias solo-Windows
    que corran unicamente el .ps1, que es lo que new_instance.py copia.
  acceptance:
    - "AC1 (falsacion previa): se reproduce la divergencia medida por el checker -- un unico form feed insertado en una linea de un fichero ya exento deja al Python en exit 1 y al gemelo en exit 0 -- y se confirma para las cuatro clases de caracter, declarando cual coincide y cual no."
    - "AC2 (definicion unica de linea): los dos escaneres pasan a compartir la MISMA semantica de troceado. Se declara cual se adopta y por que; si se adopta la mas estricta, se declara que ficheros del arbol real cambian de numeracion."
    - "AC3 (direccion del fallo): tras el cambio ninguna clase de caracter puede producir veredictos distintos entre los dos escaneres sobre el mismo arbol. Se verifica por comportamiento sobre las cinco clases, no por lectura del codigo."
    - "AC4 (contrato): negativo permanente que ejercite los dos escaneres sobre entradas con esos caracteres y exija veredicto identico, declarado en el registro y cableado en CI, verificado por MUTACION que caiga al revertir la unificacion."
    - "AC5 (la instancia solo-Windows): se declara explicitamente si una instancia que corra unicamente el .ps1 queda cubierta tras el arreglo, porque es el consumidor en el que el defecto falla ABIERTO."
    - "AC6 (sin regresion): gates del repo, suite de neutralidad y contratos de falsacion exit 0 en clon limpio, con los dos escaneres."
  verification_cmd:
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/test_scan_domain_neutrality.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/scan_domain_neutrality.py
    - scripts/scan_domain_neutrality.ps1
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El contrato de paridad de TASK-0329 (SLIP-1): se coordina, no se absorbe."
    - "El mecanismo de exencion por coordenada (SLIP-4, TASK-0339)."
    - "Codigo de producto."
  risk: medium
  estimate: M
---

# TASK-0338 -- el gemelo falla ABIERTO por el troceado de lineas

Medido por el checker en el re-juicio r2 de TASK-0329:

    fichero                     Python    PowerShell
    split_ff.py  (form feed)       3           2
    split_vt.py  (tab vertical)    3           2
    split_nel.py (NEL)             3           2
    split_ls.py  (U+2028)          3           2
    split_cr.py  (CR suelto)       3           3     <- aqui SI coinciden

Con un unico form feed dentro de la linea 10 de `scripts/prune_state.py`, sin tocar ningun escaner:

    python scripts/scan_domain_neutrality.py --root .   EXIT=1  (dos ocurrencias)
    powershell scripts/scan_domain_neutrality.ps1       EXIT=0

Python ve una linea mas a partir de ahi, las exenciones dejan de cubrir el contenido que
justificaban y grita. PowerShell no ve esa linea, sus coordenadas siguen encajando y calla.

## Por que se contrata aparte

El checker lo declaro residual y no bloqueante para 0329, con razon: la clase de caracter es exotica
en fuentes `.py` y `.ps1`, y en CI corren los dos gates, asi que el conjunto falla CERRADO por la
cara Python.

**Pero es el unico caso encontrado en que el gemelo falla ABIERTO**, y una instancia solo-Windows
que corra unicamente el `.ps1` -- exactamente lo que `new_instance.py` copia -- queda ciega ahi sin
que nada se lo diga. Ese consumidor es el que justifica la tarea, no el hub.
