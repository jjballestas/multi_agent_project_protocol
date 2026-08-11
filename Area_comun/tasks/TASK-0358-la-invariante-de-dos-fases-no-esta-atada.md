---
id: TASK-0358
title: La invariante de dos fases no esta atada por ninguna puerta -- el bloque existe, nadie comprueba que nada corra antes
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0358-la-invariante-de-dos-fases-no-esta-atada.md
created: 2026-08-11
---

# TASK-0358 -- R0332-10: existe el bloque, no la garantia

Residual bloqueante declarado al cerrar TASK-0332
(`Analista-TASK-0332-remediacion-2-verdict.md`). **Era la unica razon por la que el checker no
firmaba aquel cierre.**

## El defecto

La invariante de dos fases -- la que impide que una exencion de fecha suprima PII no-telefonica en
otro item -- **es cierta del codigo, y ninguna puerta la ata**.

    :2302   comprueba que el BLOQUE existe una vez
            NO comprueba que nada corra antes

Cuatro mutantes del checker lo demuestran **dejando intactos** el texto del bloque, el conteo de
bucles y la ausencia de `break`/`continue`. Es decir: todo lo que la puerta mira sigue igual, y la
garantia ha desaparecido.

## Lo que tiene que sostener la remediacion

1. La puerta comprueba **el orden de ejecucion**, no la presencia del bloque. La pregunta correcta
   no es *"existe la fase 1"* sino *"puede algo correr antes de la fase 1"*.
2. Se falsa con los **cuatro mutantes del checker**, que hoy pasan en verde.
3. Y con el criterio general de esta instancia: sobrevive a cambio de coordenada, de orden y de
   formato, y se acredita matando un mutante de PRODUCCION.

## Lo que NO vale

Ensanchar la comprobacion de texto de `:2302` para tapar los cuatro mutantes. Cada ensanche
reintroduce la clase con otro traje; el defecto no es que el patron sea corto, es que **mira la
forma del bloque en vez del orden en que corre**.

Relacionado: TASK-0341 (el certificador ata la forma y no el efecto) -- misma familia.
