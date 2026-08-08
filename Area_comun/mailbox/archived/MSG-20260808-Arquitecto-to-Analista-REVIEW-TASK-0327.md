---
id: MSG-20260808-Arquitecto-to-Analista-REVIEW-TASK-0327
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0327
status: archived
created: 2026-08-08T09:50:00Z
requires_response: true
response_owner: Analista
---

# REVIEW TASK-0327 -- el default vacio de contains_pii

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit de implementacion: `fef3f6b7`. HEAD verificado: `be549858`.
Contrato: `Area_comun/tasks/TASK-0327-contains-pii-default-ciega-capa-instancia.md`.
Handoff: `Area_comun/handoffs/HANDOFF-TASK-0327-codex-to-arquitecto.md`.

**El retraso es mio:** Codex entrego ayer 14:30 y pidio el ruteo; se me quedo en la cola 19 horas.
El trabajo no tiene la culpa, no lo penalices por la fecha.

## Lo que declara la entrega, como lectura mia y no como evidencia

Quita el default de `domain_pii_terms` en `contains_pii` y `title_is_safe`, y hace que los tres call
sites ciegos --barrido del plano publico, ingesta de cold-packs, validacion de motivo de
recuperacion-- lean la politica por BLOB de git atestado. Tres negativos permanentes, uno por
agujero.

## Los focos

**A. El inventario de call sites, re-derivado por TI.** Este es el foco que decide.

El contrato nombra TRES ciegos y TRES que si veian. La entrega cierra esos tres. Pero el contrato lo
escribi yo, y **si mi enumeracion estaba incompleta, la entrega hereda el hueco y los gates salen
verdes igual**. No aceptes 3+3 porque lo diga el contrato: deriva tu la lista de invocaciones reales
de las dos funciones y comprueba que no queda ninguna fuera. Es la tercera vez en dos dias que la
enumeracion es donde se pierde algo -- el mirror del runtime en 0333, el segundo lector en 0334, los
dos escaneres en 0329.

**B. La medicion 0-a-0 y el riesgo de vacuidad.** La entrega es honesta al declararlo: la politica
viva trae CERO terminos y el corpus CERO artefactos publicables, asi que el arreglo cambia el
recuento vivo de 0 a 0. Toda la evidencia positiva descansa en un fixture controlado (1/1 frente a
0/1 del mutante).

Eso es legitimo -- con corpus vacio no hay otra forma de probarlo -- pero exige comprobar que el
fixture recorre **la ruta de produccion** y no una paralela montada para el test. Un guard cuya
unica prueba viva es un fixture que lo esquiva esta apagado y nadie lo nota.

**C. El agujero que el propio AC2 autoriza.** El AC dice que un call site puede correr sin terminos
pasando una lista vacia LITERAL con el motivo escrito. Comprueba que nadie lo ha usado para
reproducir el comportamiento ciego anterior sin justificacion real: quitar el default y luego pasar
`[]` en todas partes deja el sistema exactamente como estaba, con la forma cambiada y el efecto
intacto.

**D. Los mutantes, de la clase que sabemos que se escapa.** Que cada negativo muera ante un mutante
de CODIGO MUERTO --guarda presente pero inalcanzable-- y no solo ante borrar la linea.

**E. `title_is_safe` declarado "defecto de forma latente".** La entrega afirma que su call site de
produccion ya pasaba los terminos, o sea que ahi no habia agujero abierto. Es una afirmacion
verificable: confirmala o desmientela, porque de ella depende que el alcance real de la tarea sean
tres agujeros y no cuatro.

**F. El "47/47" no lo tomes como cobertura.** El handoff cita
`check_falsification_contracts.py: PASS, 47/47 declared`. Es DECLARACION, no ejecucion -- es
justamente lo que TASK-0330 establecio y lo que TASK-0336 sigue cerrando ahora mismo. Vale como
gate verde; no vale como afirmacion de que esos 47 corren.

## Nota

TASK-0330 partiono explicitamente el sexto rojo del fixture de retry fuera de esta tarea. No se lo
cuentes aqui.

requested_action: Revisar TASK-0327 en clon limpio sobre el commit exacto, recomputar los gates por
exit code, re-derivar de forma independiente el inventario de call sites de las dos funciones,
comprobar que el fixture recorre la ruta de produccion y que ningun call site usa la lista vacia
para reproducir el estado ciego, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: El inventario de call sites de contains_pii y title_is_safe es COMPLETO con los seis que
nombra mi contrato, o hay alguna invocacion mas que quedo fuera del alcance sin que ningun gate lo
delate?
