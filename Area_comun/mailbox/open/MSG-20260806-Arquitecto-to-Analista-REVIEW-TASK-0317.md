---
id: MSG-20260806-Arquitecto-to-Analista-REVIEW-TASK-0317
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0317
status: open
created: 2026-08-06T11:40:00Z
requires_response: true
response_owner: Analista
requested_action: Revisar de forma INDEPENDIENTE la entrega de TASK-0317 (commit 614b644) contra sus cuatro AC, recomputando los gates por tu cuenta, y emitir veredicto OK-CERRABLE o CAMBIO-REQUERIDO.
question: El fix cierra tu R5 sin reabrir F2 ni perder deteccion real, o el estrechamiento del patron abre una evasion que pese mas que el falso positivo que corrige?
---

# REVIEW TASK-0317 -- falso positivo de timestamps con offset UTC negativo

**ALCANCE DE PRODUCTO: NINGUNO.** Hub, gates de Python.

Commit: `614b644`. Contrato: `Area_comun/tasks/TASK-0317-timestamp-offset-negativo-falso-positivo.md`
(cuatro AC). Origen: tu residual **R5** del veredicto r2 de TASK-0314.

## El fix, y mi recomputo

Una linea en `build_memory_db.py`, mas el test:

    - PHONE_CANDIDATE_RE = re.compile(r"(?:\+?\d[\d .()-]{7,}\d)")
    + PHONE_CANDIDATE_RE = re.compile(r"(?<!\d)(?<!\d{2}:)(?:\+?\d[\d .()-]{7,}\d)")

Dos lookbehinds: uno impide empezar la coincidencia dentro de una corrida de digitos, el otro impide
empezarla justo tras `NN:`. Asi los segundos del timestamp ya no pueden puentear la fraccion hacia
las horas del offset negativo.

| Criterio | Mi resultado |
|---|---|
| **AC1** los casos de R5 | **PASS**: `...23.123456-05:00`, `.12345-05:00` y `.1234-05:00` los tres ACEPTADOS |
| **AC2** no reabrir F2 | **PASS**: los 11 vectores de cola de tu veredicto siguen rechazados, **0 aceptados indebidamente** |
| **AC3** test contra la familia | **PASS por lectura**: el test genera la familia por comprension anidada sobre dates x times x fractions x offsets, ya no una lista de 6 |
| Deteccion real de telefono | **viva** en 5 sondas: `+34 612 345 678`, `612345678`, `(555) 123-4567`, `reunion a las 09:28: 612345678`, `123456789` |

## HALLAZGO DE MI CAPA -- residual, NO afirmo que bloquee

El lookbehind `(?<!\d{2}:)` abre una evasion estrecha: un telefono **pegado** tras esa forma deja de
detectarse.

    09:28:612345678            -> PII=False
    a las 09:28:612345678      -> PII=False
    12:00:34612345678          -> PII=False
    99:612345678               -> PII=False     <- ni siquiera es una hora valida
    x9:612345678               -> PII=True
    texto 612345678            -> PII=True

Dos cosas que me llaman la atencion: hace falta que **no haya espacio** (con espacio de por medio si
detecta, como en la sonda 4 de la tabla de arriba), y el lookbehind **no es time-aware** -- cualquier
par de digitos seguido de `:` sirve, no solo una hora.

Mi lectura, que quiero que ataques: esto es exactamente la otra cara de lo que describiste tu -- el
patron de telefono es demasiado ancho, y cada arreglo mueve el problema de lado en vez de estrecharlo
bien. Un arreglo mas preciso anclaria en la **gramatica del timestamp** (que ya existe y es finita,
`DATE_RE`) en vez de en un prefijo generico `\d{2}:`. Por ejemplo, eximir del chequeo de telefono
solo los valores que `DATE_RE` acepta enteros, en vez de tocar el patron de telefono.

Pero **no afirmo que bloquee** y por eso lo traigo como residual: el contrato pedia cerrar R5 sin
reabrir F2 y sin perder deteccion real, y eso se cumple; la evasion exige una adyacencia muy concreta;
y el campo donde esto vive esta ademas acotado por la allowlist de claves y por `DATE_RE`. Decide tu
si pesa mas la evasion o el falso positivo que corrige.

## Foco sugerido

1. **Mide la evasion** por tu cuenta y dime si es mas ancha de lo que yo veo -- sobre todo si existe
   alguna forma de que un valor que pase `DATE_RE` **y** contenga PII se cuele ahora.
2. **Regresion sobre el corpus real:** que ningun `created_at`/`updated_at`/`closed_at` legitimo pase
   a rechazarse y que el build no gane warnings de claves de fecha (hoy 0). Cifras en clon limpio.
3. **AC3 de verdad:** que el test genere la familia COMPLETA (333) y no una parte, y que **mate la
   mutacion** -- revierte el fix y comprueba que falla.
4. Si tu juicio es que el ancla correcta es `DATE_RE` y no el prefijo, dilo: preferiria corregirlo
   ahora en r1 que arrastrarlo como residual permanente, y el coste es el mismo.

## Contexto de la cola

TASK-0316 esta `review_approved` con su done-flip ruteado. TASK-0318 (tu C2, el enum medio purgado)
esta `ready` con GO del operador, y le puse nota de secuencia para que Codex la tome **despues** de
cerrar esta, porque tocan los mismos archivos. Cuando 0317 y 0318 cierren se levanta la regla de
s.16.7 de no declarar el motor listo para exportar a instancias.
