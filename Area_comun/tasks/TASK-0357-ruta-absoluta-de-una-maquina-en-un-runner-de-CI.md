---
id: TASK-0357
title: Un runner que CI ejecuta fija una ruta absoluta de UNA maquina y revienta antes de medir si esa unidad no existe
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0357-ruta-absoluta-de-una-maquina-en-un-runner-de-CI.md
created: 2026-08-11
---

# TASK-0357 -- la unica ruta absoluta del fichero, y esta en el camino de CI

Residual N1 declarado por el checker al cerrar TASK-0343
(`Analista-TASK-0343-exigencia-por-ejecucion-r4-verdict.md`).

## El defecto

    examples/mailbox_retry_cases/run_mailbox_retry_cases.py:242
        scratch_root = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0343-behavior")

Es la **unica** ruta absoluta del fichero: las otras diez fixtures usan
`tempfile.mkdtemp(prefix=...)` sin `dir=`. Si esa letra de unidad no existe,
`mkdir(parents=True, exist_ok=True)` **revienta antes de medir nada** -- medido por el checker en una
maquina con la letra ausente.

## Por que no es cosmetico

Ese runner **lo ejecuta CI**:

    job falsification-runners   runs-on: windows-latest
    run: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py

La maquina de CI no es esta. Si `D:` no existe alli -- o deja de existir, o cambia de proposito --
el runner **no falla midiendo: falla antes de medir**, y lo hace en el job que custodia los
negativos permanentes del harness. Es exactamente la clase de TASK-0345: **una suposicion de host
que nadie ejecuta hasta que CI falla**, con el agravante de que aqui la suposicion es una letra de
unidad concreta de una maquina concreta.

Y hay una ironia que conviene no perder: el fichero que fija esa ruta es el que **verifica los
negativos permanentes del harness**.

## Lo que tendria que sostener

1. La fixture obtiene su raiz por el **mismo mecanismo que las otras diez** -- `tempfile` -- o por
   una variable de entorno con fallback portable. Ninguna letra de unidad literal.
2. Se falsa **ejecutando en un entorno donde esa ruta no existe** y comprobando que el runner mide
   igual, en vez de reventar en el `mkdir`.
3. Barrido derivado: **ninguna otra ruta absoluta de maquina** queda en los runners que el workflow
   invoca. Derivado del workflow, no de una lista.

## Relacion con DECISION-0104

La regla de scratch dice que todo temporal vive bajo el scratch root designado. Esta linea la
cumple **en esta maquina** y la incumple en cualquier otra: el scratch root es una propiedad de la
instalacion, no una constante del codigo. Conviene que la remediacion lo deje dicho.
