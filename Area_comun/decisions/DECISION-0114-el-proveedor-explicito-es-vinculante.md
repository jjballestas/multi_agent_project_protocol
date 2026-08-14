---
decision_id: DECISION-0114
title: Un proveedor de agente pedido explicitamente es vinculante -- el lanzador falla antes que caer al binario de otro proveedor
status: accepted
date: 2026-08-14
ratified_at: 2026-08-14
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0101, DECISION-0113]
phase: P2
---

# DECISION-0114 - El proveedor explicito es vinculante

## Origen

Anexo del debate del 2026-08-14, aportado por el Arquitecto de la instancia NOVA a partir de un fallo
reproducido en su instancia, y sufrido de forma independiente en el hub el dia anterior.

## El defecto

`Get-AgentExecutable` resuelve el binario con una cadena de respaldo **ciega al proveedor**. Con
`-AgentProvider Anthropic`, si no encuentra `claude` en el PATH sigue cayendo por `where.exe codex`,
`%LOCALAPPDATA%\OpenAI\Codex\bin` y las extensiones de VS Code, y devuelve `codex.exe`. Mientras
tanto `Get-AgentArguments` **si** respeta el proveedor pedido.

Resultado reproducido en las dos instancias, con la misma firma:

    error: unexpected argument '--permission-mode' found
    EXEC_EXIT code=2 outcome=transient

## Por que el fallo ruidoso fue SUERTE

Los argumentos de un proveedor resultaron incompatibles con el binario del otro, asi que murio en un
segundo. **Si hubieran sido compatibles, el bucle habria ejecutado el modelo equivocado firmando como
el peon declarado, y nadie se habria enterado**: el log estampa el binario RESUELTO, pero el
proveedor PEDIDO no aparece en ninguna parte contra la que contrastarlo.

Eso rompe DECISION-0101 -- checker formal de proveedor diverso -- **en silencio**, que es la garantia
que hace que un veredicto valga como control independiente y no como autoconfirmacion.

## Lo decidido

1. **Un `-AgentProvider` explicito es VINCULANTE.** Si su binario no aparece, el lanzador **falla en
   el arranque** en vez de caer al de otro proveedor. La cadena de respaldo entre proveedores queda
   prohibida cuando el proveedor se pidio de forma explicita.
2. **La primera linea del log estampa el proveedor PEDIDO junto al binario RESUELTO.** Hoy solo
   consta el resuelto, asi que no hay nada contra lo que contrastar. Sin las dos cifras, la
   verificacion de la garantia de DECISION-0101 no es posible ni a posteriori.

## Alcance y relacion con el trabajo en curso

La primera mitad esta parcialmente cubierta por la remediacion en curso de TASK-0367, que hizo el
lanzador fail-closed. **La segunda mitad -- estampar pedido y resuelto -- es nueva** y no esta en
ninguna tarea: se pliega en esa remediacion, o sale con id propio si 0367 cierra antes.

Nota de precedencia: la version fail-closed que TASK-0367 entrego rompio la via de arranque
documentada, porque hizo depender la resolucion de variables de entorno que nadie provisiona. Esta
DECISION no bendice esa forma concreta: fija la PROPIEDAD -- proveedor explicito vinculante, y ambas
cifras estampadas -- y deja la forma a la remediacion, que debe acreditar por conducta que la via de
arranque documentada sigue funcionando.

## Autoria

Diagnostico estructural y las dos medidas: **Arquitecto de la instancia NOVA**. El hub habia
diagnosticado solo la causa proxima -- una sustitucion que hacia caer la resolucion por el hueco --
sin ver que la cadena de respaldo era ciega al proveedor de por si.
