---
id: TASK-0428
title: Dos mutantes de produccion sobreviven a la propiedad enfocada que deberia matarlos
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0428-dos-mutantes-de-produccion-sobreviven-a-la-propiedad-que-los-vigila.md
created: 2026-08-24
reviewer: Analista
intake:
  type: fix
  goal: >
    Residuo declarado por el checker en el veredicto r2 de TASK-0408 (ancla 6eb491f5), fuera del
    alcance de esa entrega y explicitamente no retenido por el. Sobre codigo que la r2 NO toco, dos
    mutantes de PRODUCCION sobreviven a la propiedad enfocada de la alerta de obligaciones
    estancadas, los dos con exit 0: el que borra la clausula de task_id, y el que infla el
    presupuesto. Una propiedad que no muere ante esas dos mutaciones no esta vigilando esas dos
    ramas: esta presente, no acreditada. Es la misma forma que RES-3 de TASK-0410 -- un arreglo sin
    negativo que muera al revertirlo -- y la que DECISION-0122 obliga a tratar como hallazgo aunque
    hoy no rompa nada.
  acceptance:
    - "AC1: el mutante que borra la clausula de task_id MUERE contra la propiedad enfocada. Se
      acredita mutando PRODUCCION, no el runner, y con el par: muere en el mutante y pasa en el
      arbol sano."
    - "AC2: el mutante que infla el presupuesto MUERE contra la propiedad enfocada, con el mismo
      par y la misma disciplina de mutar produccion."
    - "AC3: los negativos son PERMANENTES y quedan cableados donde el gate los corra, no en una
      comprobacion manual de una sola vez."
    - "AC4: la propiedad sigue verde sobre el arbol sano en DOS corridas, y no se cita ninguna
      puerta no reproducible; si alguna lo es, se declara y se excluye (DECISION-0115)."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/
  out_of_scope:
    - "NO se cambia la conducta de la alerta ni el criterio de supresion: TASK-0408 cerro eso y su
      veredicto lo acredita. Aqui solo se cierra la cobertura que faltaba."
    - "NO se toca el presupuesto de reintentos de la clase exit=-1: volvio a tres en la r2 de 0408
      y su re-presupuestacion, si alguna vez procede, es el AC5 de TASK-0424."
  risk: low
  estimate: S
---

# TASK-0428 -- la propiedad esta presente, no acreditada

El checker lo dejo dicho al aprobar la r2 de TASK-0408 y lo separo del cierre para no retenerlo:
sobre codigo que esa entrega no toco, **dos mutantes de produccion sobreviven con exit 0** a la
propiedad enfocada que deberia matarlos.

No es un defecto de conducta: hoy la alerta se comporta bien y su veredicto lo acredita por
comportamiento en clon limpio. Es un defecto de **cobertura**, y su coste es el de siempre -- si
alguien revierte manana cualquiera de esas dos ramas, nada enrojece.

Se registra por separado porque cerrar TASK-0408 con esto dentro habria sido cobrarle a una
remediacion una deuda que no genero, y dejarlo sin registrar habria sido perderlo.
