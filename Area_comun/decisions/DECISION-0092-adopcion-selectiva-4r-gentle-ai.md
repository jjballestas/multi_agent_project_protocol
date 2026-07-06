---
decision_id: DECISION-0092
title: "Adopcion SELECTIVA de patrones 4R (gentle-ai/gentle-pi): vocabulario de lentes + contrato de salida + carve-outs + principio de disjuncion-del-maker registrados AHORA (presentacion, no cambia el gate); disparo automatico de lentes y judgment-day dual-juez DIFERIDOS a Sprint 1 (cambio del brazo gobernado); catalogo web/frontend y framing advisory RECHAZADOS"
status: accepted
date: 2026-07-06
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0038, DECISION-0002, DECISION-0090, DECISION-0091, GOAL-VISION-NOVA-001]
phase: P2
scope: process-presentation
carril: A
approval_ref: "Aprobada por el Operador (John Ballestas) 2026-07-06, cerrando el debate registrado en personal/asesor/DRAFT-revision-4r-decisiones-v1.md (Fase A/B/C + resoluciones ronda 2-4). Fuente material: personal/operador/Revision/ (framework gentle-ai/gentle-pi de Alan Buscaglia, licencia MIT; skill judgment-day, licencia Apache-2.0)."
---

# DECISION-0092 - Adopcion selectiva del framework 4R (gentle-ai)

> Fuente completa con evidencia archivo:linea: `personal/asesor/DRAFT-revision-4r-decisiones-v1.md` (Fases
> A/B/C + resoluciones R1-R4 del debate operador-asesor). Esta DECISION resume el REPARTO vinculante; el
> draft queda como memoria de trabajo, no como fuente de verdad normativa (esta DECISION lo es).

## Contexto

El framework 4R (gentle-ai/gentle-pi, Alan Buscaglia, MIT) y la skill judgment-day (Apache-2.0) describen
lentes de revision read-only (Risk/Readability/Reliability/Resilience), un contrato de salida uniforme, y
un patron de doble-juez ciego para revision adversarial. La metodologia de este hub YA implementa versiones
ATESTADAS y con GATE DURO de varios de estos patrones (checker formal atestado, maker!=checker, evidencia
obligatoria via F-NOVA-01, pre-registro del estudio, ledger #4 con `submit_intent`). El ejercicio no es
"adoptar por primera vez" la mayoria de los patrones, sino: (a) formalizar con nombre lo que ya se hace
implicito, (b) tomar prestada ESTRUCTURA que aun no esta formalizada (contrato de salida, disparo
automatico de lentes), y (c) declarar explicitamente que se RECHAZA (el catalogo web/frontend, el framing
"recomendacion organica, no gate duro").

**Linea roja que gobierna todo el reparto:** cualquier item que CAMBIE EL COMPORTAMIENTO del gate (es decir,
altere el brazo GOBERNADO / el tratamiento medido del estudio pre-registrado) se DIFIERE a Sprint 1
(post-30-jul), respetando la ventana sellada (DECISION-0091). Lo que es puramente documentacion/presentacion
sobre hallazgos y checkers YA existentes se adopta ahora.

## Decision

### A. ADOPTAR AHORA (documentacion/presentacion; NO cambia el comportamiento del gate; NO toca lo medido)

1. **Vocabulario de lentes R1-R4** como ETIQUETA sobre los checkers que ya se emiten (R1 Risk / R2
   Readability / R3 Reliability / R4 Resilience). No es un checker nuevo; es nombrar lo que ya corre
   (F-NOVA-01 guard de procedencia = R1; handoffs autocontenidos/DECISION-0038 = R2; gates dotnet/arch-tests
   + GWT versionados = R3; watchdogs/lease/rollback de `submit_intent`/SLA del sello = R4).
2. **Contrato de salida uniforme** para reportes de checker/revision: cabecera (`reviewer_role`,
   `provider_family`, `maker_family`, `lenses_run`, `verdict`) + por-hallazgo (`id #N` continuando la
   numeracion de hallazgos ya en uso, `lens`, `severity` BLOCKER|CRITICAL|WARNING|SUGGESTION, `blocking`,
   `files:line`, `evidence`, `why`, `corrective_criterion`, `attestation`) + cadena limpia canonica
   (`R{n}: No findings.` / `REVIEW CLEAN -- no findings across [R1,R2,R3,R4].`). El mapeo de severidad a
   nuestro eje bloqueante/quality-data queda fijado en la tabla del Anexo A del draft fuente. Los campos
   `corrective_criterion` y `attestation` son EXTENSION PROPIA (el 4R original no los tiene) y se conservan
   como diferencial.
3. **Carve-outs "do not flag" auditables por lente** (gate-scope explicito): cada checker/lente declara que
   NO marca deliberadamente (p.ej. R1 no marca terminos de dominio dentro de `profiles/`; R3 no marca
   `tokens=NA` sellado por degradacion de err.log ya declarada; R4 no marca latencia conocida de harnesses
   pesados; R2 no marca un helper local claro y autoexplicativo). Vuelve auditable el punto ciego del gate en
   vez de dejarlo implicito.
4. **Principio de disjuncion-del-maker** (familia-juez != familia-maker) REGISTRADO como diseno sellable,
   NO operado todavia. Regla dura: un juez de la MISMA familia de modelo que el maker esta PROHIBIDO
   mientras esa relacion maker/checker este vigente (hoy: maker=Codex/OpenAI, checker=Claude/Anthropic ya
   cumple disjuncion-del-maker con 1 solo juez cross-family). Jerarquia registrada para configuraciones
   futuras (de menor a mayor independencia): (a) 1 checker cross-family = ya vigente hoy; (b) dual 2xClaude
   (maker-disjunto, juez-juez correlacionado, sin infra nueva) = suficiente para un piloto dual-blind; (c)
   dual Claude+Gemini (maker-disjunto Y juez-diverso) = maxima independencia, grado-publicacion; (d)
   Claude+OpenAI = PROHIBIDO mientras Codex sea maker. **No se introduce un segundo modelo frontera a mitad
   del experimento** (contaminaria lo medido); la infra multi-proveedor queda diferida (ver seccion B.3).
5. **Convergencia declarada (no adopcion duplicada):** la categoria "require-evidence" del 4R (evidencia
   obligatoria por hallazgo) ya esta implementada como F-NOVA-01 (guard de procedencia SQL/THROW real). Se
   CITA como validacion independiente convergente, NO se re-implementa como lente nueva.
6. **Neutralidad de dominio (DECISION-0002):** el vocabulario de lentes/eventos y la regla "componente
   compartido por >=2 verticales -> dispara R2" son NEUTRALES y van al nucleo del protocolo si se
   formalizan; los globs especificos de una instancia (nombre de proc mutador, nombre de BD, endpoints de
   auth) son de PROFILE de esa instancia, nunca del core. Ningun termino de dominio (Nova, presupuesto,
   Budget, etc.) entra a los archivos genericos del protocolo.

### B. DIFERIR a Sprint 1 / post-30-jul (cambia el COMPORTAMIENTO del gate = cambia el brazo gobernado)

7. **Computo de `lenses_required`** (derivado deterministicamente de las senales del diff: toca-proc-mutador
   -> R1; toca-componente-compartido-por->=2-verticales -> R2; cambia-comportamiento-observable -> R3;
   toca-runtime/error-mapping/retry/rollback/observabilidad -> R4) mas el **gate de cobertura**
   (`lenses_run` DEBE cubrir `lenses_required`; si no cubre, el gate falla por cobertura incompleta, no por
   hallazgo). Este es el mecanismo que vuelve NO-decorativas a R2/R4 (el hallazgo #10, acople de switch
   compartido entre superficies, es precisamente una senal R2 que hoy no tiene disparador automatico y se
   cazo por una pasada transversal, no por diseno).
8. **Ejecucion del patron judgment-day** (dos jueces ciegos en paralelo, taxonomia de acuerdo confirmado/
   sospechoso/contradiccion/INFO, re-juicio tras cada fix, escalada terminal humana tras 2 iteraciones) como
   mecanismo OPERADO (mas alla del principio de disjuncion-del-maker ya registrado en A.4).
9. **Infra multi-proveedor de jueces** (un segundo modelo frontera, p.ej. Gemini, para el claim de
   independencia grado-publicacion). No se introduce ahora bajo ninguna circunstancia dentro de la ventana
   medida (post-30-jul o experimento aparte, ver A.4).

### C. RECHAZAR (anti-alcance; tan vinculante como lo adoptado)

10. El catalogo de reglas especificas de instancia web/frontend del 4R original (OWASP/React/husky/Sentry/
    globs de auth-payments específicos). No es un patron transferible; es contenido de UNA instancia
    particular (ExperienciasGH), fuera de dominio para el nucleo del protocolo.
11. El framing "recomendacion organica, no gate duro" ("gentle-ai never fires, blocks, or executes") para
    cualquier dominio que este en modo `enforce` atestado (DECISION-0022, B.3 hard-gate). Este framing es
    OPUESTO a la garantia de escritor-unico/gate-duro que diferencia a este protocolo; adoptarlo debilitaria
    esa garantia. Se adopta EN CAMBIO el modelo de coste-por-tier del 4R (tiers de esfuerzo/coste segun
    riesgo del diff) sin el framing advisory.
12. Un orquestador unificado inferido de la resolucion centralizada de skills del 4R. La resolucion de
    skills sigue siendo PER-DOMINIO (cada coordinador de dominio resuelve e inyecta su propio bloque), nunca
    un orquestador global de todas las instancias.
13. Un juez de la misma familia de modelo que el maker (ver A.4, disjuncion-del-maker).

### D. REGISTRAR como rail de publicacion propio (track separado, no bloquea ni gatea nada del estudio)

14. **Proveniencia criptografica de hallazgos de revision** (aplicar DSSE/in-toto/Rekor-o-equivalente a la
    CAPA DE REVISION, no solo al build) queda registrado como CONTRIBUCION DIFERENCIAL potencial, con
    decision de alcance PENDIENTE de juicio humano (impacto reputacional/academico, fuera del alcance de
    esta DECISION operativa). El MVP de bajo costo (emitir un hallazgo ya existente, p.ej. #10, como
    atestacion sobre el ledger `#4` que ya existe via `submit_intent`+sha256) queda como candidato de spike
    de 1 dia para Carril B, sin compromiso de ejecucion aqui.

## Atribucion

- Framework 4R / gentle-pi: Alan Buscaglia, licencia MIT.
- Skill judgment-day: licencia Apache-2.0 (derivacion con atribucion permitida).
- Ambos se citan como TRABAJO RELACIONADO en cualquier material publicable derivado de este hub; no se
  presenta la adopcion parcial como si fuera de autoria propia.

## Alcance y limites

- Esta DECISION es de PROCESO/PRESENTACION: no reabre el sello de la Etapa 1 (DECISION-0091), no cambia
  ninguna asignacion de par baseline/gobernado, no altera el `protocol_version` pineado ni el genesis #4.
- Los items de la seccion A son aplicables de inmediato en reportes/handoffs futuros (documentacion, sin
  cambio de codigo/gate); no son retroactivos sobre hallazgos ya cerrados salvo que se re-emitan
  voluntariamente en el nuevo formato como ejemplo (no obligatorio).
- Los items de la seccion B requieren una tarea de implementacion futura (post-30-jul) con su propio DoR/
  SPEC; esta DECISION autoriza el DISENO, no la construccion.
- Limite declarado de judgment-day/disjuncion-del-maker: dos jueces de la MISMA familia de modelo siguen
  teniendo correlacion residual (comparten corpus de entrenamiento); esto NO sustituye al experto humano de
  dominio pendiente, y no debe presentarse como "problema de correlacion resuelto".

## Consecuencias

- (+) El checker formal atestado del hub gana una ESTRUCTURA de presentacion reconocible externamente
  (lentes con nombre, contrato de salida parseable, carve-outs auditables) sin alterar ninguna garantia ya
  atestada.
- (+) El principio de disjuncion-del-maker queda formalmente registrado como extension citable sobre
  judgment-day (que solo pide "diversificar modelo" sin esta restriccion).
- (+) Narrativa de publicacion reforzada: "lentes estilo-4R, pero atestadas + con proveniencia + disjuntas-
  del-maker -- donde 4R es advisory + fuente-slide, esto es enforce + fuente-estandar + medido + falsable".
- (-) Disciplina de mensaje adicional: cada reporte que adopte el contrato de salida debe declarar
  explicitamente `lenses_run` aunque sea parcial (honestidad de cobertura), lo cual expone que R2/R4 no
  corren aun de forma sistematica hasta que la seccion B se implemente.
- Seguimiento: registrar tarea de implementacion (Sprint 1) para B.7 (`lenses_required`+gate de cobertura) y
  B.8 (judgment-day operado) cuando se abra la ventana post-30-jul.
