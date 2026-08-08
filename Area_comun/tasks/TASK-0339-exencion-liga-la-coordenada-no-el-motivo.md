---
id: TASK-0339
title: La exencion de identidad liga (linea, termino) y no el motivo que la justifica
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0339-exencion-liga-la-coordenada-no-el-motivo.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    SLIP-4 del veredicto r2 de TASK-0329. La exencion declara ruta, linea y termino mas un campo
    de motivo en prosa, pero el contrato solo comprueba que en esa coordenada OCURRA el termino;
    nunca que la ocurrencia sea la que el motivo describe. Una linea exenta es por tanto un
    contenedor ciego PERMANENTE para ese termino, diga lo que diga la linea manana. Superficie
    residual medida por el checker: 91 pares (linea, termino).
  acceptance:
    - "AC1 (falsacion previa): se reproduce lo medido por el checker -- reescribir el contenido de una linea ya exenta por una fuga de identidad real deja los dos escaneres, la suite y el inventario de contratos en exit 0."
    - "AC2 (ligar el motivo, no la coordenada): la exencion pasa a quedar atada a la propiedad que la justifica, de forma que un cambio de contenido que deje de satisfacerla la invalide. Se declara la forma elegida y por que sobrevive a cambios de coordenada, de orden y de formato."
    - "AC3 (superficie declarada): se mide y declara la superficie ciega ANTES y DESPUES, en pares (linea, termino), con el mismo criterio con que el checker midio 91."
    - "AC4 (direccion del fallo): el mecanismo nuevo no puede volver ruidoso el gate sobre las nueve referencias legitimas a la CLI de terceros; si alguna deja de estar excusada, se declara. Un gate ruidoso acaba desactivado, y eso es peor que uno ancho."
    - "AC5 (contrato): negativo permanente que muera cuando el contenido de una coordenada exenta cambia a una fuga real, declarado en el registro y cableado en CI, verificado por MUTACION."
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
    - "El troceado de lineas divergente (SLIP-2, TASK-0338)."
    - "Codigo de producto."
  risk: medium
  estimate: M
---

# TASK-0339 -- una linea exenta es un contenedor ciego permanente

Repro medida por el checker sobre HEAD, reescribiendo la linea 1397 -- ya exenta -- del propio
fichero del que trata TASK-0329, por la clase de fuga que TASK-0316 corrigio:

    antes:  comentario que menciona la CLI del proveedor de terceros
    ahora:  una asignacion de identidad por defecto real

    python scripts/scan_domain_neutrality.py --root .    EXIT=0
    powershell scripts/scan_domain_neutrality.ps1        EXIT=0
    python scripts/test_scan_domain_neutrality.py        EXIT=0
    python scripts/check_falsification_contracts.py      EXIT=0

Los cuatro verdes sobre una fuga viva. El canario del recuento de exenciones declaradas no lo ve
porque el numero no cambia; el uno-a-uno no lo ve porque la ocurrencia existe.

## Lo que esta tarea NO es

**No es un reproche a TASK-0329.** Su AC2 admitia literalmente "el token concreto (o la linea
concreta)", y la entrega eligio la linea, que estaba dentro de lo pedido. Y la mejora fue enorme y
esta medida: **de 8289 lineas ciegas a 91 pares ciegos, una reduccion del 98,9 por ciento de la
superficie ciega.** Esta tarea recorta el 1,1 por ciento que queda, que es distinto de deshacer
nada.

## Por que aun asi importa

Porque la superficie que queda es exactamente donde alguien puede plantar una fuga **mas tarde** sin
que ningun gate se entere, y porque el re-pinneo manual de coordenadas -- que ya ocurrio una vez en
menos de 24 horas -- pasa por esas mismas lineas. La ventana no se abre al re-pinnear: esta abierta
todo el rato, y el re-pinneo solo es la ocasion mas visible.
