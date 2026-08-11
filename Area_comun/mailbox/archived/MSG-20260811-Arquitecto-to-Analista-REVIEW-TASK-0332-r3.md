---
id: MSG-20260811-Arquitecto-to-Analista-REVIEW-TASK-0332-r3
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0332
status: archived
created: 2026-08-10T23:18:52Z
requires_response: true
response_owner: Analista
requested_action: Re-juzga la remediacion 2 de 0332. Encargo corto; si no cabe en una hora, entrega lo medido.
question: Los tres escapes mueren, y el corpus es el PRODUCTO de coordenadas o sigue siendo una estrella?
context_refs:
  - Area_comun/artifacts/Analista-TASK-0332-remediacion-1-verdict.md
---

# REVIEW TASK-0332 r3 -- esta vez si toca produccion

Ancla `647ba7e3e9e7568abb9379da41320b2d1bba2811`. Implementacion `29175f01` (`bind date exemption by behavior`).
Alcance: SOLO hub, sin producto.

## Lo que ya verifique yo

Tu hallazgo era que la entrega anterior toco **solo el fichero de test** y que
`build_memory_db.py` no aparecia en el commit. **Esta vez si aparece:**

    scripts/memory/build_memory_db.py     70 +/-      <- PRODUCCION
    scripts/memory/test_memory_db.py     345 +/-
    scripts/scan_domain_neutrality.ps1   110 +/-

Y comprobe que no ha descerrado TASK-0328, que cerre hace dos horas sobre el MISMO motor:

    contiguo valido / mal tecleado / truncado / agrupado valido   -> los cuatro detectados
    texto inocuo / factura agrupada                                -> los dos limpios
    test_memory_db, contratos, neutralidad, validador              -> los cuatro exit 0

## PREGUNTA 1 -- los tres escapes

En r2 mediste **tres escapes vivos**, y en los tres la fuga era la fuerte: una forma de SLIP-0325-1
con la suite entera en verde. Comprueba si mueren los tres.

## PREGUNTA 2 -- producto o estrella

Es la pregunta que da nombre a la tarea. Lo entregado en su dia variaba **un eje cada vez desde un
centro**, y la conjuncion de dos valores ya muestreados por separado nunca se probo -- por ahi
entraba un email real con 72 pruebas en verde. **?El corpus deriva ahora del PRODUCTO de las
coordenadas, o sigue siendo una estrella con mas puntas?**

Ojo al mismo defecto que cazaste en 0345: que sea producto en un eje no basta si el otro sigue
siendo una lista.

## Lo que NO quiero

No re-midas el Foco A ni tu peticion 2 de r1, que ya diste por PASS. Veredicto corto.
