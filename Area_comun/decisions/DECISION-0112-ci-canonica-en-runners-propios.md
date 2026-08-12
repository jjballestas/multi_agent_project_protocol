---
decision_id: DECISION-0112
title: La CI canonica corre en runners propios, y el repositorio sigue privado porque publicarlo prohibiria ese arreglo
status: accepted
date: 2026-08-12
ratified_at: 2026-08-12
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0010, DECISION-0098, DECISION-0104, DECISION-0110]
phase: P2
---

# DECISION-0112 - La CI canonica en runners propios

## Origen

Debate entre el operador humano y el Arquitecto en la sesion del 2026-08-12, tras el reinicio de la
maquina. El operador pregunto si convenia hacer publico el repositorio; el dolor real que empujaba esa
pregunta era la factura de Actions. Aprobada por el operador el 2026-08-12.

## Contexto medido

    plan real                     GitHub Free -- 2.000 minutos de Actions/mes
    Copilot Pro (10 $/mes)        aporta CERO minutos de Actions
    cadencia                      39 y 56 runs/dia (10 y 11 de agosto); 3.208 runs historicos
    commits en 7 dias             795, de los cuales 211 (27%) son commits de memoria
    coste por run                 ~13 minutos facturables -- 4 jobs, cada uno redondeado al minuto
                                  entero, y el de Windows a doble tarifa
    necesidad                     ~18.000 min/mes  =  NUEVE veces el cupo

Ninguna dieta de triggers cierra un factor nueve: aun eliminando el 100% de los commits de memoria y
el 45% de corridas superadas por la guarda de concurrencia, quedarian ~7.000 min/mes.

El sintoma que se venia leyendo como "CI rota" era doble. La anotacion de GitHub -- *"the job was not
started because recent account payments have failed or your spending limit needs to be increased"* --
enuncia DOS causas distintas con una sola frase. No hay problema de cobro: la causa activa es el
limite de gasto en 0 $ tras agotar el cupo incluido.

## Las dos salidas descartadas, y por que

**Subir el limite de gasto.** ~130-150 $/mes al ritmo actual, y al alza: `validate` abortaba en el paso
28 de 77, asi que cuando la cascada cierre y recorra los 77 cada run durara mas. Descartada por el
operador.

**Hacer publico el repositorio.** Daria minutos ilimitados, pero DECISION-0010 fija visibilidad privada
y licencia propietaria, y la exposicion es irreversible: forks, caches y archivos sobreviven a una
re-privatizacion posterior. Y ademas **se muerde la cola**: los runners self-hosted en un repositorio
publico son un agujero de seguridad conocido -- un PR de un tercero ejecuta codigo en la maquina del
operador, que es donde viven las llaves privadas de firma. Publicar prohibiria el unico arreglo
gratuito. Descartada.

## La medicion que sostiene la decision

Run `31581821440`, con job de **control en la misma corrida**, que es lo que la hace discriminante:

    control  ubuntu-latest (GitHub-hosted)   BLOQUEADO   0/0 pasos   12 s
    probe    self-hosted Linux               SUCCESS     8/8 pasos   16 s
    probe    self-hosted Windows             SUCCESS     8/8 pasos   75 s
    timing.billable  ->  UBUNTU total_ms=0 (el control). Los self-hosted NO aparecen en el desglose.

Los pasos no eran simbolicos: checkout, interprete y el gate real `scan_encoding`. El runner de Linux
ejecuta ademas el gemelo PowerShell sobre Linux; el de Windows acredita PowerShell 5.1.

**El bloqueo por facturacion no alcanza a los runners propios, y sus minutos no se facturan.**

## Decision

1. **La CI canonica de esta instancia corre en runners propios.** `falsification-runners` en
   `[self-hosted, protocol-win]`; `validate`, `powershell-linux-parity` y `falsification-runners-python`
   en `[self-hosted, protocol-linux]`.
2. **El repositorio sigue PRIVADO** (DECISION-0010 intacta), y ahora ademas por una razon tecnica: los
   runners propios exigen que lo sea.
3. **Un run en runner propio SATISFACE los criterios que exigen "un run real de GitHub Actions"**
   (AC6 de TASK-0340, AC7 de TASK-0347): es un run autentico, orquestado por GitHub, con
   `run_id` / `job` / `head_sha` citables. Lo unico que cambia es donde ocurre el computo.
4. **El estado acumulado entre corridas es el riesgo, y se vigila por conducta, no por declaracion.**
   Un runner GitHub-hosted nace limpio en cada corrida; uno propio no. Es la misma clase de falso verde
   que esta instancia lleva semanas cazando. La mitigacion es un criterio de aceptacion falsable, no una
   promesa: se ensucia el arbol de trabajo a proposito y el run debe detectarlo o eliminarlo, acreditado
   con el par sucio/limpio -- un run que pase en ambos casos no acredita nada.
5. **Reversion**: una etiqueta por job en `runs-on`. Sin migracion de datos, sin efecto sobre el ledger.

## Fuera del alcance de esta decision

- La dieta de triggers (`branches: [main]`, `paths-ignore: personal/**`). El `paths-ignore` tiene su
  propia contrapartida -- pierde granularidad de biseccion, la misma que el AC2 de TASK-0354 ya acepto
  para la cancelacion -- y se declara en decision propia, no se cuela en esta.
- La persistencia de los runners como servicio del sistema, que es operativa y no protocolar.
- La visibilidad del repositorio y su licencia, que siguen fijadas por DECISION-0010.

## Consecuencias

- TASK-0340 y TASK-0347 salen de `blocked`: lo que estaba bloqueado era su cierre, no su trabajo.
- TASK-0342 puede cerrar.
- Detras entran 0349, 0350, 0351 y 0352, los cinco rojos de causa ajena que TASK-0347 dejo fuera.
- El coste de CI de esta instancia pasa a 0 $/mes.
