---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0332
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0332
status: open
created: 2026-08-08T08:46:52Z
requires_response: false
---

# GO TASK-0332 -- los dos muestreos que protegen la exencion de fecha son disjuntos

Contrato: `Area_comun/tasks/TASK-0332-muestreos-disjuntos-contrato-por-comportamiento.md`.
Reclamala y ejecutala.

## Por que esta tarea existe

Es la RAIZ de la fuga que el veredicto de TASK-0325 demostro, no una secuela cosmetica. 0317 fija
una familia de 333 offsets contra `contains_pii`; 0325 anade cuatro mas pero **solo contra
`DATE_RE`**. Un offset que caiga fuera de ambos conjuntos no lo prueba nadie contra el gate real, y
por ese hueco entro SLIP-0325-1: un bypass estrecho sobre `+05:45` colo **un email por el gate de
PII con la suite entera en verde**.

La remediacion de 0325 clavo el hueco para `break` y `continue`. Fue correcta y basto para cerrar
aquella tarea. Pero cerro dos FORMAS, no la propiedad.

## El AC3 es toda la tarea

**El negativo nuevo no puede inspeccionar el AST.** Tiene que ejercitar `contains_pii` con entradas
reales y exigir la respuesta correcta, y tiene que morir ante un bypass por **reestructuracion** --
`if not DATE_RE...: <todos los chequeos>` -- que es precisamente la forma que el AST no ve.

Un contrato sintactico contra un defecto semantico da verde por construccion. Ya lo tenemos medido
en esta casa mas de una vez: el contrato ata el helper y el efecto se escapa.

## Lo demas

**AC2: unifica los muestreos de verdad.** El que se ejercita contra `contains_pii` debe cubrir el
rango que `DATE_RE` acepta tras el estrechamiento de 0322, extremos incluidos (`+14:00`, `-14:00`) y
los de minutos no-cero (`+05:45`, `-09:45`). Que dejen de ser conjuntos disjuntos.

**AC4: las tres formas, medidas y atribuidas.** Reestructuracion, filtrado del iterable en un helper
externo, salida temprana. Declara **cual mata cada contrato y por que**. Si alguna sigue sin
cubrirse, va como residual DECLARADO con su razon. No la silencies para que el recuento quede limpio.

**AC5: no toques lo que ya funciona.** Los contratos de 0317, 0322 y 0325 siguen verdes y con la
misma semantica. Si el nuevo hace redundante alguno, lo declaras y lo justificas ANTES de tocarlo.

## Nota

Empieza por el AC1: demuestra primero que existe un offset que hoy no prueba nadie contra
`contains_pii` y que un bypass sobre el pasa la suite. Si esa falsacion previa no sale, la premisa de
la tarea esta mal y quiero saberlo antes de que construyas nada encima.

requested_action: Reclamar TASK-0332, empezar por la falsacion previa del AC1, entregar el negativo
por COMPORTAMIENTO que muera ante el bypass por reestructuracion, declarar cual de las tres formas
mata cada contrato, y devolverla a in_review liberando el claim en el mismo paso.
