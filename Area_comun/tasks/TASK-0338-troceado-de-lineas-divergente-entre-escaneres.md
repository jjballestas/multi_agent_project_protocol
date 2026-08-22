---
id: TASK-0338
title: Los dos escaneres no comparten la definicion de LINEA a la que atan las coordenadas
status: ready
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

## Segunda medicion independiente -- 2026-08-22, veredicto r1 de TASK-0410

Este defecto se ha medido **dos veces, con catorce dias de diferencia, por el mismo checker y en dos
tareas distintas**, mientras esta tarea seguia en `proposed`. La primera fue el re-juicio r2 de
TASK-0329 (8-ago), que la origino. La segunda es el veredicto r1 de TASK-0410 (22-ago), y aporta
evidencia nueva que vale la pena tener aqui:

**La sonda ya no es sintetica: es sobre el fichero REAL del inventario.**
`scripts/harness/peer_mailbox_cron.ps1`, exento en la linea 555, con **un** U+000C insertado antes
de la identidad:

    numeracion:  PY splitlines -> 556      PS Get-Content -> 555

    python scan_domain_neutrality.py --root probeLF
      scripts/harness/peer_mailbox_cron.ps1:556: Codex        PY_EXIT=1
    pwsh -File scan_domain_neutrality.ps1 -Root probeLF
                                                              PS_EXIT=0

**Misma entrada, veredictos OPUESTOS, y PowerShell es el permisivo:** exime en silencio una fuga de
identidad REAL. Cinco separadores lo reproducen (VT, FF, FS, NEL, LS) y la suite completa sale
exit 0 con el escape vivo. Coordenadas exactas del arbol de hoy:

    scan_domain_neutrality.py:267    text.splitlines()
    scan_domain_neutrality.ps1:329   Get-Content -Encoding UTF8

**Por que no se absorbio en TASK-0410 y vive aqui:** la r1 de 0410 cerro los dos ejes que le tocaban
-- la clave de RUTA y el DIGEST -- y su censo cuadra 88 == 88. El eje de la COORDENADA es heredado y
no atribuible a esa remediacion. El cierre de TASK-0410 nombra este residuo y apunta aqui.
