---
decision_id: DECISION-0078
title: "Pre-registro de medicion A/B/C de peones: contrato de asignacion, coste completo del firmante y sandbox aislado"
status: proposed
date: 2026-07-01
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [REQ-ZEUS-001, DECISION-0070, DECISION-0074, DECISION-0077, TASK-0231]
scope: product-research
phase: P2
---

# DECISION-0078 - Medicion A/B/C de peones con contrato de asignacion

## Contexto

DECISION-0074 acepta el backend hibrido con firmantes frontera y peones keyless fuera del ledger. Tambien exige
medir antes de adoptar peones en produccion: A control, B peon -> gate -> firmante, C peon -> gate ->
critico asesor -> firmante, en `D:/Agentes/Zeus/piloto-peones/`.

Esta decision propuesta pre-registra la medicion secundaria posterior al corpus principal del TFM. No cambia el
baseline N=500 ni sus hipotesis principales. Sirve como medicion complementaria de eficiencia: si la delegacion a
peones reduce el coste del firmante sin degradar calidad, gates ni trazabilidad.

## Decision propuesta

Antes de ejecutar el experimento A/B/C, toda tarea enviada a un peon debe cumplir un **contrato de asignacion
cerrado y verificable**. El coste de producir ese contrato cuenta como coste del firmante.

La adopcion de peones solo puede considerarse si la medicion muestra ahorro en el coste total del firmante y no
introduce degradacion de calidad, seguridad, PII, gates, ciclos de revision ni estabilidad operativa.

## Contrato de asignacion a peon

Un peon solo puede recibir una tarea si la orden incluye, como minimo:

1. Objetivo concreto.
2. Rutas permitidas y rutas prohibidas.
3. Entrada exacta y salida esperada.
4. Patron o pasos permitidos.
5. Restricciones duras: no ledger, no `submit_intent`, no commits, no secretos, no PII, no decisiones, no cambios de
   protocolo y no reglas de negocio.
6. Verificacion objetiva: comandos, tests, golden, lint, build, diff esperado o fixture reproducible.
7. Criterio de aceptacion.
8. Regla de bloqueo: si falta contexto, devolver `BLOCKED` con una pregunta concreta; no inventar alcance.
9. Provenance minima del borrador: peon/modelo, prompt id, timestamp, rutas tocadas y resultado de gates locales.

## Elegibilidad de tareas

Son elegibles para peon solo tareas acotadas, repetitivas y gate-verificables: scaffolding de tests, transformaciones
mecanicas con variacion menor, fixtures, runbooks iniciales, reemplazos de texto/i18n y borradores donde el gate
objetivo decide la correccion.

No son elegibles: arquitectura, seguridad, reglas de negocio, cambios del protocolo core, ledger, decisiones,
PII/datos reales, integracion novel o cualquier tarea cuya correccion dependa principalmente de criterio senior.

Si la salida es funcion mecanica de la entrada, se usa codegen/script antes que LLM.

## Diseno de medicion

- Ruta sandbox: `D:/Agentes/Zeus/piloto-peones/`.
- Repo medido principal: no se toca.
- Muestra: 10-20 tareas homogeneas reales-sin-PII, pre-listadas antes de ejecutar.
- Brazos:
  - A: firmante solo.
  - B: peon produce borrador -> gate -> firmante revisa/integra/firma.
  - C: peon produce borrador -> gate -> critico asesor no firmante -> firmante revisa/integra/firma.
- Stop rule: cerrar al completar la muestra pre-listada o declarar aborto si se incumple PII, ledger, sandbox o gate
  operativo.

## Metricas

La metrica primaria es el coste total del firmante:

```text
tokens_firmante_total =
  tokens_prompt_delegacion
+ tokens_revision
+ tokens_integracion
+ tokens_rework
```

Tambien se registran:

- tokens del peon de entrada/salida;
- tokens del critico asesor, si aplica;
- tiempo de pared;
- fallos de gate;
- ciclos de correccion;
- tareas descartadas;
- calidad final: aceptada, corregida, rechazada;
- incidentes de PII, ledger o estabilidad operativa.

La comparacion que decide no es "tokens totales baratos", sino ahorro del firmante frente al control A.

## Regla de adopcion

Peones pueden pasar de experimento a uso acotado solo si:

- `tokens_firmante_total` de B o C baja de forma material frente a A;
- los gates finales no empeoran;
- los ciclos de correccion no suben de forma material;
- no hay incidentes de PII, secretos, ledger o commits no autorizados;
- el resultado es reproducible en al menos dos tandas o una tanda con muestra suficiente y homogenea;
- Analista emite GO adversarial y Arquitecto ratifica.

Un resultado negativo tambien es valido: bloquea adopcion productiva y documenta donde los peones no ahorran.

## Relacion con TFM

Esta medicion es secundaria y separada del TFM principal. Puede reportarse como complemento post-N=500 o anexo de
optimizacion de coste, pero no modifica el corpus principal, el baseline canonico ni H1-H3.

## Requisitos previos operativos

El experimento puede prepararse en paralelo en sandbox, pero cualquier concurrencia real de peones o firmantes debe
respetar el resultado de TASK-0235 o ejecutarse de forma manual, serializada y con limites duros, para no multiplicar
riesgos de locks/zombies.

## Estado

Propuesta pendiente de ratificacion. No autoriza ejecucion hasta que el operador/Arquitecto la acepten y el gate
Analista valide el diseno de medicion.
