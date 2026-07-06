---
message_id: MSG-20260706-Operador-to-Arquitecto-DIRECTIVA-cola-prep-sprint1-no-idle
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/decisions/DECISION-0092-adopcion-selectiva-4r-gentle-ai.md
  - Area_comun/protocol/REVIEW_CONTRACT.md
  - Area_comun/specs/nova/
  - personal/asesor/PIPELINE-cierre-baseline-sprint1.md
one_line_summary: "Drenaste la cola no-idle 4/4 (HTML + REVIEW_CONTRACT/CARVE_OUTS + reconciliacion prep). Re-llenado PREP de Sprint 1 (escribir/disenar, NO construir; linea roja Q4 vigente): SPEC del brazo diferido de DECISION-0092 B + hardening adversarial de las SPECs Sprint-1 ya escritas. Todo dentro del sello."
requested_action: "Trabajar la cola PREP en orden (escribir/disenar, NO construir): (1) SPEC-ar los mecanismos DIFERIDOS de DECISION-0092 seccion B como artefactos Sprint-1-ready; (2) pasada adversarial propia de hardening sobre las SPECs de Sprint 1 ya escritas; (3) preparar el paquete de DEC de dominio P3.x para el operador. Deja senal de progreso cada turno; si algo lo ves fuera de ventana, dilo y sigue."
question: "Confirmas pickup y orden? Marca explicitamente cualquier item que consideres que cruza la linea de 'construir' (para diferirlo) -- la frontera escribir-vs-construir la fijas tu con criterio de sello."
---

# DIRECTIVA - Cola PREP Sprint 1 (no-idle, dentro del sello)

Cerraste la cola anterior 4/4 (HTML operador actualizado, REVIEW_CONTRACT.md + CARVE_OUTS.md materializados,
reconciliacion 26-29 turnkey). El dev baseline esta COMPLETO y los miembros gobernados estan SELLADOS para
post-30-jul: NO se construyen. Pero la PREP (escribir/disenar) SI es trabajo valido de ventana. Cola:

## 1. SPEC-ar los mecanismos DIFERIDOS de DECISION-0092 seccion B (escribir, NO construir)
La DECISION-0092 difirio a Sprint 1 el COMPORTAMIENTO; disenarlo AHORA como SPEC es prep legitima ("escribir,
no construir"). Producir SPEC(s) Sprint-1-ready de:
- **`lenses_required` + gate de cobertura** (`lenses_run` DEBE cubrir `lenses_required`): mecanismo, formato del
  campo en la tarea/handoff, computo desde senales del diff, punto de fallo por cobertura incompleta.
- **Tabla de disparo como PROFILE de instancia** (neutralidad DECISION-0002): el vocabulario de lentes/eventos
  ya esta en REVIEW_CONTRACT.md (core); los globs de instancia (proc mutador, DbsFinanciero, endpoint prod ->
  R4; componente-compartido-por->=2-verticales -> R2) van al profile Nova. Disenar ese profile.
- **Integracion judgment-day** (dual-juez ciego + principio de disjuncion-del-maker cableado): diseno, no
  ejecucion.
Marca cada SPEC como "build en Sprint 1", no antes.

## 2. Hardening adversarial propio de las SPECs de Sprint 1 ya escritas
Las SPECs gobernadas (P4.3, familia P3, pool Q4, BR-C3) ya existen escritas. Pasada propia de endurecimiento
ANTES de que entren a build en Sprint 1: consistencia con el patron congelado de P4.1, aislamiento intra-par
declarado, criterios de aceptacion falsables, y que hereden las restricciones 6i/6j/6k horneadas en P4-006.
Es prep de calidad; no reabre unidades medidas ni construye.

## 3. Preparar el paquete de DEC de dominio P3.x para el operador
El sello Etapa 2 esta bloqueado por (a) la reconciliacion 26-29 y (b) las DEC de dominio P3.x sin cerrar.
(b) necesita al operador. Prepara el paquete: enumera las decisiones de dominio P3.x abiertas, cada una con
opciones + recomendacion, listo para que el operador las resuelva. Eso desbloquea Etapa 2 mas adelante.

## Nota de frontera (sello)
Todo lo anterior es ESCRIBIR/DISENAR/PREPARAR. Ningun item construye una unidad gobernada ni toca lo medido.
Si algun paso te obliga a construir para completarlo, marcalo y difierelo a Sprint 1. NO arrancar el MVP H6
(proveniencia): su alcance esta PENDIENTE de juicio del operador (DECISION-0092 B.14). Re-lleno al drenar.
