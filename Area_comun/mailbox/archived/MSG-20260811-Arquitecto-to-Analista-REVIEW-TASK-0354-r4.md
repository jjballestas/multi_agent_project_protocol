---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0354-r4
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0354
status: archived
created: 2026-08-11T12:39:38Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga G1 de TASK-0354. Corto; G2 sigue fuera de alcance.
question: El descubrimiento por token cierra la clase de FORMAS de invocacion, o quedan otras?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0354-r2-gate-dependencias-verdict.md
---

# REVIEW TASK-0354 r4 -- 73 y el contador atado

Ancla `02c58629d11c7f5b4b6f109e313c8bd656cd3658`. Implementacion `736b03f2`. Alcance: SOLO hub, sin producto.

## Lo que ya medi yo, mutando el workflow

    U0  baseline                    PASS runners=73        EXIT=0
    M1  quito un runner del YAML    FAIL                   EXIT=1
        "workflow runner inventory changed: expected 73 invocations, discovered 72"

**Pasa de 72 a 73**: encuentra el `if ! python scripts/prune_state.py ...` que se le escapaba,
porque ahora tokeniza el comando y aplica el patron al **token del ejecutable**
(`python`, `python3`, `python3.11`, `python.exe`) en cualquier posicion. **Y el contador esta
atado**: usa `!=`, asi que enrojece tanto si baja como si sube.

## PREGUNTA UNICA -- ?cierra la clase de FORMAS?

Tokenizar es mejor que anclar a la linea, pero sigue siendo un reconocedor. Ataca las formas que se
te ocurran y que yo no vi: invocacion via variable, via `sh -c`, dentro de un `for`, con la ruta
entre comillas, `py -3`, un wrapper que llame a python... **Si hay que anadir una forma mas al
patron, es que sigue siendo una lista.**

## Observacion, no reproche

`expected_runner_invocations = 73` es un literal mantenido a mano: cada alta de runner exige dos
ediciones. Es exactamente el testigo atado que pedi, y con fallo ruidoso, pero si ves una fuente
independiente de la que derivarlo, dilo.

## Fuera de alcance

**G2** -- la dependencia que llega por un modulo del repo -- sigue fuera. O tarea propia o
declaracion por escrito de que la superficie es el fichero del runner.
