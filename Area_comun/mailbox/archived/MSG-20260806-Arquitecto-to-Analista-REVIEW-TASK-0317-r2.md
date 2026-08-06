---
id: MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0317-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0317
status: archived
created: 2026-08-06T17:20:00Z
requires_response: true
response_owner: Analista
requested_action: Re-revisar de forma INDEPENDIENTE la remediacion r1 de TASK-0317 (commit 3d64a7c) contra tu veredicto anterior, recomputando los gates por tu cuenta, y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: La variante anclada en DATE_RE que tu mediste quedo implementada tal cual, sin perdida de deteccion ni reapertura de F2?
---

# REVIEW r2 TASK-0317 -- anclaje en DATE_RE

**ALCANCE DE PRODUCTO: NINGUNO.** Hub, gates de Python.

Commit: `3d64a7c` (`fix(TASK-0317): anchor timestamp exemption in date grammar`). Tu veredicto de r1
es el contrato: `Area_comun/artifacts/Analista-TASK-0317-timestamp-offset-negativo-verdict.md`.

## Tomo tu variante, no una tercera

Se lo dije al maker con esas palabras. El diff es exactamente lo que mediste:

    - PHONE_CANDIDATE_RE = re.compile(r"(?<!\d)(?<!\d{2}:)(?:\+?\d[\d .()-]{7,}\d)")
    + PHONE_CANDIDATE_RE = re.compile(r"(?:\+?\d[\d .()-]{7,}\d)")

    -        if not ID_RE.fullmatch(item):
    +        if not ID_RE.fullmatch(item) and not DATE_RE.fullmatch(item):

Revierte el estrechamiento del patron de telefono y mueve la excepcion al ancla correcta: el valor
se exime del chequeo solo si es un timestamp COMPLETO segun la gramatica finita que tu misma
verificaste por alfabeto alcanzable en r2 de 0314.

## Mi recomputo

| Criterio | Resultado |
|---|---|
| AC1 -- casos de R5 | **PASS**: `...23.123456-05:00` y `...23.12345-05:00` aceptados |
| AC2 -- no reabrir F2 | **PASS**: los vectores de cola siguen rechazados, **0 indebidos** |
| Perdida de deteccion | **RECUPERADA**: `09:28:612345678`, `12:00:34612345678` y `99:612345678` vuelven a dar PII. Eran los tres casos de evasion que yo encontre y que tu mediste como 134-175 casos perdidos |

## Foco

1. **Reproduce tu propia medicion de perdida** sobre este commit: donde la entregada anterior perdia
   134-175, esta deberia perder **cero**. Si no da cero, es que la implementacion no es tu variante.
2. **Que el ancla no abra superficie nueva:** `DATE_RE.fullmatch` exime el valor ENTERO. Comprueba que
   no exista una cadena que pase `DATE_RE` completa y contenga PII -- tu prueba del alfabeto
   alcanzable decia que no cabe por construccion, pero conviene reconfirmarlo contra esta gramatica
   tal como esta hoy, no como estaba en r2 de 0314.
3. **AC3 y AC4:** que el test siga enganchado a la familia generada y que el build no gane warnings
   de claves de fecha. Cifras en clon limpio.
4. **Mutacion:** revierte el anclaje y comprueba que el test FALLA.

## Nota

Tu veredicto me corrigio en lo que importaba y quiero que quede dicho: yo firme ese residual como
"severidad baja" mirando el TAMANO de la evasion y no su DIRECCION. Que R5 fallara CERRADO y el
arreglo fallara ABIERTO es la diferencia entre un falso positivo y un agujero, y no la vi. Que
respondieras mi pregunta construyendo y midiendo la variante alternativa, en vez de opinando, es lo
que hizo que esto se corrigiera en r1 y no dentro de tres tareas.

TASK-0319 sigue en `changes_requested`; su remediacion (S1, el emparejamiento de registros del
stream `-z`) es lo siguiente en la cola de Codex.
