---
message_id: MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-coordina-probe-memoria-hibrida
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
  - personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md
  - Area_comun/decisions/DECISION-0071-engram-memory-backend.md
  - Area_comun/decisions/DECISION-0081-ruta-unica-memoria-hibrida-engram-cerrado.md
one_line_summary: "Marco estrategico del sub-estudio/PROBE de memoria hibrida (debate operador-asesor 14-jul): probe de VALOR ahora (decision del operador, NO evidencia, firewall) sobre vehiculo aislado Nova-Payroll (slice acotado de Nomina), subordinado a Sprint 1; medicion rigurosa post-30 SOLO si el probe da indicios. Coordina con tu SPEC-MEMORIA-HIBRIDA v0.2.0 y confirma la secuencia."
requested_action: "Coordina el marco de abajo con tu trabajo en curso de la SPEC-MEMORIA-HIBRIDA v0.2.0 y responde con la secuencia concreta propuesta (Gate-1 DECISION scopeada AISLADA a la instancia -> nacer Nova-Payroll -> Fase A build + probe), subordinada a Sprint 1. El pre-registro del sub-estudio (fase rigurosa post-30) lo redacta el Asesor como draft cuando toque; no lo hagas tu."
question: "Confirmas la secuencia y el scope AISLADO del Gate-1 (memoria ON solo en Nova-Payroll, OFF en hub e instancias medidas), o ves un mejor mecanismo bajo la frontera dos-trios?"
---

# DIRECTIVA - Coordinacion del PROBE de memoria hibrida (debate operador-asesor, 2026-07-14)

## Marco estrategico (decidido en debate)
- **Objetivo del proyecto = evidencia citable; el ANCLA es Contabilidad** (pre-registro N=6, DECISION-0094).
  La memoria hibrida NO es un ancla citable por ahora.
- **La medicion de la memoria es, AHORA, soporte a la decision del operador:** saber si la memoria hibrida
  aporta valor real a la metodologia, para decidir si se adopta. **NO es evidencia; NO entra al corpus
  citable** (firewall duro: un probe disfrazado de resultado = HARKing, el pecado que evita el pre-registro).

## Secuencia acordada
1. **AHORA:** construir la memoria AISLADA + **probe de valor** = Fase A de tu SPEC (round-trip verde,
   cold-start recall, **REVIVE de peon DEMOSTRABLE**, drift 0) + observacion cualitativa de si ayuda.
   Objetivo = decision del operador, no un numero. Un go/no-go se decide por DEMOSTRACION (un peon que
   muere y revive con su contexto y sigue correcto), no por estadistica. Subordinado a Sprint 1.
2. **Decision del operador:** la metodologia adopta la memoria? (con los indicios del probe).
3. **POST-30-jul, SOLO si el probe da indicios positivos:** medicion RIGUROSA = sub-estudio pre-registrado
   (aislado, control de confound) O folded en las metricas normales (Q1-Q5) de las unidades futuras. Lo que
   cueste menos foco.

## Vehiculo
- **Nova-Payroll** (modulo Nomina), instancia **born-operational PROPIA** (base + store de memoria propios),
  **NO cableada** a Budget/Contabilidad medidos. Nomina integra fuerte con ellos -> riesgo de fuga; aislar duro.
- **Slice ACOTADO** de Nomina (nucleo de liquidacion): empleados/contratos/conceptos + cabecera DbsNom002t /
  detalle 007t / bases 028t + 1 base calc (FindBaseTra) + 1 %concepto + 1 consecutivo + 1 control de periodo +
  1 reporte RO. **NO** el modulo completo de 42 tablas. Nomina es **greenfield** (sin SDD/base/procs; solo
  legacy VB6) -> el diseno del slice es PREP, analogo al kit SPEC-CONT de Contabilidad.

## Gates de gobernanza (tu carril; caveat del asesor)
- **Gate 1 = DECISION que autoriza implementar la memoria** (el REQ v0.3.0 tiene
  `implementation_allowed_before_decision:false`; supersede DECISION-0071; activa la ruta REQ/SPEC).
- **CAVEAT del Asesor:** es el UNICO paso que toca el contrato del protocolo durante la ventana del estudio.
  **Scopea la activacion a la instancia Nova-Payroll AISLADA** (memoria OFF en el hub y en las instancias
  medidas de Contabilidad/Budget), para que NO toque el config pineado del hub (2E35F26E/1.14.0) ni el estudio.
  Asi el probe corre sin riesgo. Si ves un mecanismo mejor bajo la frontera dos-trios, proponlo.
- Frontera dos-trios: el hub-Arquitecto coordina; el ledger de la instancia lo escribe su propio trio.

## Guardrails
- **PII de nomina = SENSIBLE** (salarios/empleados): fuera del store de memoria; se mide el PROCESO de
  desarrollo, jamas los datos de nomina (espejo de la politica PII-embeddings del estudio).
- **Anti-drenaje:** idealmente el probe lo corre mano/ventana SEPARADA de quien lleva Contabilidad; si comparte
  cuello de botella, freno explicito **"Contabilidad gana"**.
- **Angulo citable (si se llega):** centrar en lo que Engram NO tiene y tu SPEC SI = **REVIVE atestado +
  round-trip canon<->DB integro + procedencia firmada**. Recall a secas (Engram) no es citable; esto si.

## Que NO hacer
- No arrancar Fase B (medicion rigurosa) ni pretender un numero citable de la memoria antes del 30.
- No cablear la memoria en las instancias medidas. No tocar el pre-registro de Contabilidad ni el fondo del hub.

-- Operador (via Asesor)
