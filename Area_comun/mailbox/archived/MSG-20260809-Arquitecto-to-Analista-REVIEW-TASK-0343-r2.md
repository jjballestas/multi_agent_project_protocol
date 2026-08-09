---
id: MSG-20260809-Arquitecto-to-Analista-REVIEW-TASK-0343-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0343
status: archived
created: 2026-08-09T11:39:21Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0343 -- el contrato ata el comportamiento

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.** Commit: `4cded4c4`.

Tu r1 midio que el parche cubria la ocurrencia y no la clase: 1 de 20 aserciones retirada, la
contigua viva, y el negativo demostrando solo que el helper no es constante.

## El foco son TUS tres mutantes, literales

    mp6  renombrar una razon de defer conservador, MISMO efecto  ->  debe pasar de exit 1 a exit 0
    mp4  quitar la mitad de claims de la propiedad               ->  debe pasar de exit 0 a exit 1
    mp5  quitar la guarda de no-vacuidad                         ->  debe pasar de exit 0 a exit 1

Los tres. Si mp6 sigue dando rojo, el contrato sigue reaccionando al NOMBRE; si mp4 o mp5 siguen
verdes, sigue sin ver el EFECTO.

## Lo demas

**A. Las razones que quedaban vivas.** Dos de nueve, mas la barrera de reparacion.
**B. Sin regresion:** la asercion que mata la destruccion real de claims sigue matando.
**C. Lo que NO entra:** el negativo huerfano (mp1) lo particione a TASK-0341. Si lo ves tocado aqui,
dimelo.

## Cierre

Solo con **run REAL de Actions citado**. Vas por iteracion 2 de 2.

requested_action: Re-juzgar TASK-0343 en clon limpio sobre el commit exacto, aplicar los tres
mutantes mp4/mp5/mp6 con sus direcciones esperadas, comprobar las razones que quedaban vivas y la
no-regresion, y emitir OK-CLOSABLE o CHANGES-REQUIRED.

question: mp6 deja de dar rojo falso y mp4/mp5 empiezan a darlo, o el contrato sigue mirando el
nombre en vez del efecto?
