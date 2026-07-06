---
message_id: MSG-20260706-Operador-to-Arquitecto-DIRECTIVA-decision-adopcion-4r
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - personal/asesor/DRAFT-revision-4r-decisiones-v1.md
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
  - personal/operador/Revision/
one_line_summary: "Operador APRUEBA la adopcion de patrones 4R (gentle-ai). Redactar una DECISION (siguiente numero) que ADOPTE lo aplicable-ahora (naming de lentes + contrato de salida + carve-outs + principio disjuncion-del-maker) y DIFIERA los cambios de comportamiento del gate a Sprint 1, respetando la ventana sellada. Fuente autocontenida = el draft del Asesor."
requested_action: "Redactar DECISION-<siguiente> de adopcion selectiva del framework 4R, con el reparto ADOPTAR-AHORA / DIFERIR / RECHAZAR de abajo (fuente completa con evidencia textual archivo:linea = personal/asesor/DRAFT-revision-4r-decisiones-v1.md, aprobado por el operador). Aplicar SOLO lo aplicable-ahora (documentacion/presentacion que NO altera el tratamiento medido); tu fijas el limite exacto respetando el sello. Registrar atribucion (gentle-pi MIT / judgment-day Apache-2.0). Mantener neutralidad de dominio (ver punto NEUTRALIDAD)."
question: "Confirmas el reparto adoptar-ahora/diferir/rechazar y procedes a redactar la DECISION? Si algun item que marque ADOPTAR-AHORA lo lees como cambio-de-tratamiento (y debe diferirse), dimelo con tu criterio de sello."
---

# DIRECTIVA - Operador aprueba adopcion 4R -> redactar DECISION + aplicar lo aplicable-ahora

El operador cerro el debate y APROBO. La fuente completa (Fase A/B/C + contrato de salida + disparo natural
de lentes, toda con evidencia textual archivo:linea) esta en `personal/asesor/DRAFT-revision-4r-decisiones-
v1.md`. Redacta la DECISION sobre ese draft. Reparto pedido:

## ADOPTAR AHORA (documentacion/presentacion; NO cambia el comportamiento del gate; NO toca lo medido)
1. **Vocabulario de lentes R1-R4** nombrado sobre los checkers que YA emitimos (R1 Risk / R2 Readability /
   R3 Reliability / R4 Resilience). Es etiqueta, no nuevo checker.
2. **Contrato de salida uniforme:** cabecera (reviewer_role, provider_family, maker_family, lenses_run,
   verdict) + por-hallazgo (id #N, lens, severity BLOCKER|CRITICAL|WARNING|SUGGESTION, blocking, files:line,
   evidence, why, corrective_criterion, attestation) + cadena limpia canonica (`R{n}: No findings.` /
   `REVIEW CLEAN -- no findings across [R1,R2,R3,R4].`). Mapear la taxonomia a nuestro eje bloqueante.
3. **Carve-outs "do not flag" por lente** (gate-scope AUDITABLE; H7).
4. **Principio de disjuncion-del-maker** (familia-juez != familia-maker) REGISTRADO como diseno sellable, NO
   operado. Regla dura: juez OpenAI PROHIBIDO mientras Codex sea maker.
5. **Convergencia** (H8): nuestra evidencia-obligatoria (F-NOVA-01) ya es "require-evidence"; se cita, no se
   re-implementa.
6. **NEUTRALIDAD (DECISION-0002):** el vocabulario de lentes/eventos y la regla "componente-compartido -> R2"
   son NEUTRALES -> core; los globs de instancia (proc mutador, DbsFinanciero, auth) -> PROFILE de instancia.
   No meter terminos Nova al core.

## DIFERIR a Sprint 1 / post-30-jul (cambios de COMPORTAMIENTO del gate = cambio del brazo gobernado)
7. Computo de `lenses_required` (de las senales del diff) + **gate de cobertura** (`lenses_run` DEBE cubrir
   `lenses_required`; si no, falla por cobertura). Es lo que vuelve NO-decorativas a R2/R4.
8. Ejecucion de los disparadores naturales: **R2** se dispara por COMPONENTE COMPARTIDO por >=2 verticales
   (senal de acople, estructural, neutral -- habria cazado el #10/50212 por diseno); **R4** por superficie que
   CORRE EN PRODUCCION (endpoint/mutador nuevo, error-mapping/retry/rollback/observabilidad).
9. judgment-day dual-juez ciego ejecutandose (H4).

## DIFERIR con condicion (post-experimento / experimento aparte)
10. Infra multi-proveedor de jueces (Claude+Gemini). NO se introduce un 2o modelo frontera a mitad del
    experimento (contamina lo medido; orden del operador). Hoy: maker=Codex vs checker=Claude (cross-family)
    + experto humano pendiente como pata no-LLM.

## RECHAZAR (anti-alcance; tan vinculante como lo adoptado)
11. Instancia web/frontend (OWASP/React/husky/Sentry/globs auth-payments). Framing "recomendacion organica,
    no gate duro" para dominios en enforce atestado. Orquestador unificado (la resolucion de skills es
    per-dominio, H5). Juez OpenAI con Codex de maker.

## REGISTRAR como rail de publicacion (track propio, no bloquea)
12. **H6 proveniencia criptografica de hallazgos** = contribucion diferencial (operador confirma: novedad
    citable). Eje de novedad: atestar la CAPA DE REVISION (no solo el build). MVP de 1 dia = emitir UN
    hallazgo (p.ej. #10) como atestacion sobre el #4 (submit_intent+sha256 ya existen); Rekor/Sigstore fase
    posterior. El campo `attestation` del contrato es el puente natural.

## Cola no-idle (el operador reporta que estas sin trabajo; ademas de la DECISION, pipeline abierto)
Ver `personal/asesor/PIPELINE-cierre-baseline-sprint1.md` seccion 3 (cierre duro 25-jul):
- **3.1** resolver `tokens=NA` de P2.1/P2.2 (err.log volatil) vs real -- integridad, abierto.
- **3.2** mi recomendacion de cadencia de atestacion ya ruteada; confirmar si el `medicion_hashlog.csv` que
  creaste (df6b4c9) la implementa o hay delta.
- **3.6** preparar la reconciliacion 26-29 (mapeo commit/rama -> tarea_id) -- arranca 26-jul, se puede dejar
  listo.
- TASK-0246: el Analista dio OK a la remediacion (2fc9890) -- confirmar si falta done-flip.

Prioridad: (1) esta DECISION 4R; (2) 3.1 token=NA; (3) el resto en paralelo. Re-lleno la cola al drenarse.
