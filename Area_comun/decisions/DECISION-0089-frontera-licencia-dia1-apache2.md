---
decision_id: DECISION-0089
title: "Frontera abierto/cerrado y licencia decidida el DIA 1: spec/core neutral bajo Apache-2.0; el complemento escaso (motor de evidencia atestada + estudio medido) se protege; NUNCA retrofit de licencia sobre lo publicado"
status: accepted
date: 2026-07-04
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0087, DECISION-0088, DECISION-0050, DECISION-0002, GOAL-VISION-NOVA-001]
phase: P2
scope: governance
carril: B
approval_ref: "Aprobada por el Operador (John Ballestas) 2026-07-04 (aprobacion interactiva 'aprobadas' de los drafts 0089/0090). Origen: R-EXT-08 de F1.6 (personal/Arquitecto/APRENDIZAJES-EXTERNOS-extraccion-reglas.md), redactada como DRAFT-DECISION-0089 tras la DIRECTIVA cola-trabajo-ventana-muerta (item 3). Frontera de licencia = BOUNDARY -> aprobacion humana registrada (AGENTS.md s.4)."
---

# DECISION-0089 - Frontera de licencia decidida el dia 1 (Apache-2.0; no retrofit)

> Carril B (post-sello) pero de ENTRADA: debe respetarse ANTES de publicar CUALQUIER artefacto de Aegis
> (gatea la publicacion habilitada por DECISION-0087). No bloquea el Carril A ni el sello Etapa 1. La
> EJECUCION (aplicar cabeceras de licencia, preparar el paquete publicable, i18n) es trabajo posterior.

## Contexto

DECISION-0087 marco la metodologia como 'Aegis' y difirio la ejecucion de publicacion (i18n del core
neutral + spec de referencia) a Carril B. Publicar cualquier artefacto sin fijar antes la frontera
abierto/cerrado y la licencia es un error caro e IRREVERSIBLE: cambiar la licencia despues de publicar
quema la confianza (precedente HashiCorp/BUSL 2023). R-EXT-08 (F1.6) extrajo la regla de los precedentes
de captura de valor: quien capturo valor poseia un COMPLEMENTO ESCASO, nunca la spec en si
(Sigstore -> Chainguard ~3.5B USD; Git -> GitHub; semver capturo CERO valor directo).

## Decision

1. **El complemento escaso -- lo que se PROTEGE -- es el MOTOR DE EVIDENCIA ATESTADA + el estudio medido.**
   No la spec. Concretamente: la cadena #4 atestada operada como servicio/dataset, el corpus sellado
   (N=500 y sucesores), el estudio con pre-registro y su evidencia falsable reproducible. Ese es el activo
   durable (R-EXT-10) y el que puede capturar valor comercial.

2. **La spec / core neutral se publica bajo licencia PERMISIVA (Apache-2.0).** El protocolo domain-neutral
   (task lifecycle, claims, mailbox, handoffs, decisiones, reportes, validador, el contrato AGENTS.md y los
   `*.template.*`) es reputacion e interoperabilidad, no el foso. Apache-2.0 (con clausula de patentes)
   maximiza adopcion y citabilidad sin regalar el complemento escaso. La eleccion de Apache-2.0 sobre MIT
   se justifica por la clausula de patentes (relevante en atestacion/seguridad).

3. **Superficie publicable acotada (no todo el repo).** Se publica: el core neutral + `*.template.*` +
   README + el spec de referencia (mapping Plan/Generation/Approval de R-EXT-01, controles SOC2/ISO/NIST de
   R-EXT-06). NO se publica: el dogfooding en espanol, las areas personales, el corpus sellado, el motor de
   evidencia operado, ni el codigo de producto de dominio (Nova-X, Zeus-Aegis). Esos son repos/capas
   separados con su propia licencia (posiblemente cerrada/comercial).

4. **NUNCA retrofit de licencia sobre lo ya publicado.** Una vez un artefacto sale bajo Apache-2.0, esa
   version queda bajo Apache-2.0 para siempre. Cambios de modelo de negocio se hacen en artefactos NUEVOS
   (el motor/servicio), jamas re-licenciando lo publicado. Esta clausula es la que preserva la confianza.

5. **Gate de publicacion.** Ningun artefacto de Aegis se publica hasta que esta DECISION este registrada
   (lo esta). El primer release publico referencia este decision_id.

## Alcance y limites

- Es DIRECCION, no ejecucion. La ejecucion (cabeceras de licencia, paquete publicable, i18n) es trabajo de
  Carril B posterior, gateado por el sello.
- No toca el N=500 sellado, el epoch pineado, ni la cadena #4 (ortogonal; solo fija como se licencia lo que
  se publique de la superficie neutral).
- Interactua con DECISION-0087 (marca) y DECISION-0088 (asiento): 'Aegis' publicable + Apache-2.0 son la
  misma linea de salida.

## Consecuencias

- (+) Frontera clara antes de publicar; cero riesgo de retrofit-de-confianza.
- (+) Adopcion/citabilidad maxima de la spec; el valor se captura en el complemento escaso.
- (-) Renuncia explicita a monetizar la spec en si (correcto: semver capturo CERO; la spec es reputacion).
- Riesgo residual a acotar en la EJECUCION de Carril B: definir con precision la linea "core neutral
  publicable" vs "motor operado" para que un fork no reconstruya el complemento escaso solo con lo publicado.
