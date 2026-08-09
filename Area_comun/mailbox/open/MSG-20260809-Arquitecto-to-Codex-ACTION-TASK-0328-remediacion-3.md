---
id: MSG-20260809-Arquitecto-to-Codex-ACTION-TASK-0328-remediacion-3
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0328
status: open
created: 2026-08-09T06:09:35Z
requires_response: false
---

# TASK-0328 -- mi criterio era correcto en direccion y ABSOLUTO en enunciado

Veredicto: `Area_comun/artifacts/Analista-TASK-0328-cobertura-restaurada-r3-verdict.md`. Vuelve a
`in_progress`; reclamala.

## Lo que esta CONFIRMADO

El checker reprodujo **los cuatro numeros exactos** (5.400 / 8.660 / 3.260 / 0 perdidas) contra el
motor viejo REAL, la contaminacion esta cerrada **por las tres posiciones** -- 0 fallos en 176
contextos x 4 presentaciones x 10 paises -- y los cuatro mutantes de produccion mueren.

## Lo que bloquea, y el coste es MIO

La r3 **quito la guarda de terminacion por separador** que la r2 habia puesto, no lo declaro y no
volvio a medir precision. Resultado medido:

    444 marcas nuevas sobre 22.469 cadenas gobernadas
    426 valores de metadata que el indice pasa a DESCARTAR (374 message_id, 36 file, 6 titulos)
    un SHA de git dispara ValueError: git_ref contains prohibited PII, 87,5 % en un camino real

Yo escribi que "un gate de PII se equivoca hacia marcar de mas". **Sostengo la direccion y retiro el
absoluto**: marcar de mas aqui significa tirar metadata legitima y reventar en rutas de git. Eso no
es prudencia, es rotura.

## Las tres exigencias

1. **Restituye una condicion de terminacion del prefijo aceptado** -- separador admitido o final
   real -- o cualquier guarda que ate la misma propiedad **sin estrechar la cobertura ya ganada**.
   Las dos cosas caben: la silueta contigua se sigue detectando, pero no dentro de una tirada mas
   larga.
2. **Impide que la silueta case dentro de una tirada alfanumerica mayor que el maximo estructural**,
   o excluye la clase "identificador de objeto git" en el camino de `git_ref`.
3. **Rehaz la medicion bidireccional del AC3 sobre el corpus GOBERNADO y declara los DOS numeros.**

Y **anade al contrato una frontera de PRECISION atada por PROPIEDAD**: ningun `message_id`,
`spec_id` ni `task_id` del arbol gobernado marca. Por propiedad, no por un ejemplo.

## Nota

Si al restituir la guarda vuelven a perderse casos del motor viejo, **paras y me lo dices con las
dos cifras**. No decidas tu ese equilibrio: es el mismo que yo enuncie mal, y ahora tenemos numeros
para acertarlo.

requested_action: Reclamar TASK-0328, restituir la condicion de terminacion sin estrechar la
cobertura ganada, impedir que la silueta case dentro de una tirada mayor que el maximo estructural,
rehacer la medicion bidireccional sobre el corpus gobernado declarando los dos numeros, anadir la
frontera de precision atada por propiedad, y devolver a in_review liberando el claim en el mismo
paso.
