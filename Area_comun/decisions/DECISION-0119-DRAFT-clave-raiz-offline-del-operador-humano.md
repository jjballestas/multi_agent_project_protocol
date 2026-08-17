---
decision_id: DECISION-0119
title: Clave raiz offline del operador humano -- generacion, custodia y entrega fuera de banda
status: draft
date: 2026-08-17
author: Arquitecto
approved_by: PENDIENTE -- operador humano EN PERSONA
supersedes: []
superseded_by: []
related:
  - TASK-0414
  - TASK-0386
  - DECISION-0117
---

# DECISION-0119 (BORRADOR) -- la raiz que ningun agente de esta maquina puede autorizar

## Estado

**BORRADOR. NO aplicar.** Requiere firma del **operador humano en persona**, con ceremonia fuera de
banda. **Sin reloj**: nada de lo que hay en curso depende de esta decision, por diseno.

## Por que existe: lo que TASK-0414 demostro en cuatro rondas

Cuatro intentos de anclar la identidad de una clave, y el checker rompio los tres primeros **por la
misma razon estructural**, no por tres descuidos:

    r1  el discriminador era signature.keyid       -> lo escribe el forjador
    r2  el ancla existia pero no estaba atada      -> se la acuna el mismo
    r3  el ancla vive en un registro versionado    -> lo escribe cualquiera con un trailer,
                                                      y quedo en la unica familia de rutas que
                                                      el gate de claims de producto NO mira

**Las tres veces se intento anclar la identidad en algo que el propio actor controla.** No hay una
cuarta variante ingeniosa: **o hay raiz externa, o la propiedad no se sostiene**.

## La regla de diseno que esta decision consagra

**Una raiz de confianza generada o autorizada por cualquier agente de esta maquina nace
comprometida** -- y eso **incluye al canal delegado del operador**. Su proposito es precisamente
estar fuera del alcance de todos los que operamos aqui.

Por eso esta decision **no puede aprobarla el canal Operador**, aunque tenga autoridad delegada para
casi todo lo demas. Que el canal se declare incompetente para esto **es** la propiedad que la hace
creible.

## Lo que se propone al humano

1. **Generacion FUERA de esta maquina.** Ningun agente participa, ni observa, ni almacena.
2. **Custodia fisica del operador.** La privada no toca esta maquina en ningun momento.
3. **Entrega al replay del fingerprint / clave publica por un canal que el operador disene** --
   deliberadamente no se propone aqui: proponerlo seria volver a meter a un agente en el diseno de
   su propia raiz.
4. **Uso:** firmar el genesis del registro de claves y delegar las altas posteriores.

## Lo que NO bloquea (y por que se puede esperar sin coste)

TASK-0414 se resuelve **hoy** con **ancla-por-cadena**: el registro se fija con un evento
`registry.anchor` encadenado por `prev_hash` sobre el **genesis pineado del ledger #4**, que es la
unica raiz **preexistente, externa al registro y ya atestada** disponible. Alterar el registro sin su
ancla rompe CLEAN; retirar el ancla rompe la cadena.

**El residual que esa via NO cubre** -- un insider que ademas appendee un ancla plausible -- queda
declarado con dueno **aqui**: es ambiental de la maquina compartida y **su cura es esta decision**,
no otro mecanismo. Perseguirlo con codigo seria intentar cerrar con ingenieria lo que solo cierra la
custodia.

## Nota de metodo, para quien lea esto despues

El fondo intocable --config pineado, re-genesis prohibida-- se trato durante toda la jornada como una
restriccion. Resulto ser **el activo**: era el unico punto de confianza que no dependia de ningun
agente. La restriccion que mas incomoda es la que hizo posible el arreglo.
