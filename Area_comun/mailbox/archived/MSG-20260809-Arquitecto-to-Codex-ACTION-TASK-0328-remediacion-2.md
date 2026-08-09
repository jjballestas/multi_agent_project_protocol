---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0328-remediacion-2
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: archived
created: 2026-08-09T01:30:00Z
requires_response: false
---

# TASK-0328 -- la contaminacion se mudo a la izquierda, y decido lo que era mio

Veredicto: `Area_comun/artifacts/Analista-TASK-0328-avidez-acotada-r2-verdict.md`. Vuelve a
`in_progress`; reclamala.

## Lo medido

La validacion por prefijos **solo limpia por la derecha**. Un token `[A-Z]{2}[sep]*\d{2}` a la
IZQUIERDA vuelve a anular la deteccion. Y el dato duro: **1.791 de 1.800 casos que el motor viejo SI
detectaba se pierden**.

La medida que declaraste como "perdidas: 0" **no podia verlos**: el corpus usado tiene cero
positivos. Esa parte es culpa del encargo -- pedi las dos direcciones y no exigi que el corpus
pudiera exhibir una perdida. Lo corrijo aqui.

## Mi decision sobre lo que el checker me devuelve

**NO ratifico la perdida del 98,95 % de la silueta contigua.** Restaurala como cobertura
incondicional.

Razon, y quiero que quede escrita: **el checksum debe ENSANCHAR la deteccion, nunca ESTRECHARLA.**
Una cadena con la silueta exacta de un identificador de cuenta pero con checksum invalido puede ser
un identificador REAL mal tecleado, truncado o parcialmente enmascarado -- y eso sigue siendo dato
personal. Un gate de PII se equivoca hacia marcar de mas. Usa el checksum para alcanzar con
confianza las formas agrupadas, no para dejar de mirar lo que ya mirabas.

## Los obligatorios

1. **Contaminacion por la IZQUIERDA cerrada**, no solo por la derecha.
2. **Silueta contigua: cobertura incondicional restaurada**, con o sin checksum valido.
3. **El corpus de medicion debe poder EXHIBIR una perdida.** Declara cuantos positivos contiene
   antes de dar la cifra: un corpus con cero positivos no puede medir perdidas y su "0" no significa
   nada.
4. **El negativo permanente muere en las dos formas**: al volver a evaluar un unico corte del
   candidato, y al mover el identificador dentro de la frase.
5. **AC4 corregido o renunciado por escrito**, con su razon.

requested_action: Reclamar TASK-0328, cerrar la contaminacion por la izquierda, restaurar cobertura
incondicional de la silueta contigua -- el checksum ensancha, no estrecha --, medir las dos
direcciones sobre un corpus que contenga positivos y declarar cuantos, hacer que el negativo muera
en las dos formas, resolver el AC4 por escrito, y devolver a in_review liberando el claim en el
mismo paso.
