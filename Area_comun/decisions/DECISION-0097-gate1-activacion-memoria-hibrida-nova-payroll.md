---
decision_id: DECISION-0097
title: "Gate-1: activacion SCOPEADA de la memoria hibrida -- implementar REQ v0.3.0 / SPEC v0.2.0 SOLO en la instancia aislada Nova-Payroll (probe de valor, no evidencia)"
status: proposed-pending-operator-signature
date: 2026-07-14
deciders: [operador humano (FIRMA PENDIENTE), Arquitecto (redacta por GO b699996)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0081, DECISION-0095, DECISION-0096, DECISION-0026, DECISION-0040]
phase: P2
derives_from:
  - "personal/operador/requerimientos-futuros/memoria-hibrida-db-archivo-frio/REQ-MEMORIA-HIBRIDA-DB-ARCHIVO-FRIO.md (v0.3.0)"
  - "Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md (v0.2.0, commit 9376bb4)"
  - "Area_comun/mailbox/answered/MSG-20260714-Operador-to-Arquitecto-DIRECTIVA-coordina-probe-memoria-hibrida.md"
  - "Area_comun/mailbox/open/MSG-20260714-Operador-to-Arquitecto-GO-gate1-roster-nova-payroll.md (GO b699996)"
---

# DECISION-0097 - Gate-1: activacion scopeada de la memoria hibrida (probe Nova-Payroll)

> **DRAFT PARA FIRMA DEL OPERADOR** (GO de redaccion: hub b699996; marco: DIRECTIVA del probe,
> hub 9b02e23). Esta DECISION se sella via submit_intent SOLO tras la firma escrita del operador;
> hasta entonces no autoriza nada. NO toca #4: config hub 2E35F26E / epoch 1.14.0 / dataset N=500 /
> sellos intactos (la DECISION vive fuera del config pineado, patron 0095/0096).

## Contexto

El REQ v0.3.0 (ruta UNICA de memoria por DECISION-0081, que ya supersedio a DECISION-0071) gatea su
implementacion con `implementation_allowed_before_decision: false` (s.0.4). La SPEC-MEMORIA-HIBRIDA
v0.2.0 esta escrita y revisada adversarialmente. El operador ordeno (DIRECTIVA 14-jul) un PROBE DE
VALOR aislado -- decision del operador, NO evidencia -- sobre un vehiculo nuevo (Nova-Payroll),
subordinado a Sprint 1. Esta DECISION es el Gate-1 de esa secuencia: la ACTIVACION scopeada.

## Decision (7 clausulas)

1. **ACTIVACION SCOPEADA.** Se AUTORIZA implementar el REQ v0.3.0 / SPEC v0.2.0 **UNICA Y
   EXCLUSIVAMENTE en la instancia Nova-Payroll** (repo `NOVA-Suite/Nova-Payroll`, a nacer
   born-operational bajo DECISION-0096). El gate `implementation_allowed_before_decision:false`
   del REQ queda levantado SOLO para esa instancia. Alcance de la implementacion autorizada:
   Fase A de la SPEC (F1 indexador read-only + round-trip + drift + revive_pack s.5.5; F2 minimo
   si el probe lo requiere). Las fases F3+ (archivo frio real) NO quedan autorizadas por esta
   DECISION (exigiran su propia DECISION conforme al REQ s.0.4).
2. **PROHIBICION DE VENTANA (memoria OFF en hub y medidas).** Mientras dure la ventana del estudio
   (hasta el cierre de la medicion de Etapa 2 y la decision de adopcion), la memoria NO se cablea
   en el hub ni en las instancias medidas (NOVA/Contabilidad/Budget): ni indexador corriendo, ni
   scripts de memoria invocados por sus gates, ni store alguno. El OFF es ESTRUCTURAL (ningun gate
   ni flujo del core lee la DB -- SPEC I5) y esta clausula lo hace ademas VINCULANTE: cablearlo
   antes de tiempo = violacion de frontera (DECISION-0018 anomalia + re-apertura de esta DECISION).
3. **FIREWALL ANTI-HARKING.** NADA del probe es evidencia ni entra al corpus citable del estudio:
   su unico output legitimo son INDICIOS CUALITATIVOS para la decision de adopcion del operador
   (la DEMOSTRACION del REVIVE, s.5.5 de la SPEC). Cualquier medicion rigurosa/citable de la
   memoria exige el PRE-REGISTRO PREVIO del sub-estudio (draft del Asesor, sello del operador,
   patron DECISION-0094) -- Fase B, condicional a indicios positivos.
4. **FRENO "CONTABILIDAD GANA".** La Fase A (build del probe) solo arranca TRAS el sello de Etapa 2
   o con ventana ociosa DECLARADA por el operador; ante cualquier conflicto de recursos
   (trio/maquina/atencion), la cola E2/Contabilidad PREVALECE y el probe se pausa sin ceremonia.
   Esta clausula se copia textual al GO de la Fase A.
5. **UN SOLO DDL MASTER.** La implementacion usa el master del hub (SPEC s.3) via el export
   born-operational (DECISION-0096), ejecutando el PORT/SUPERSEDE del memdb.py ya merged en
   Zeus-protocol-Aegis (hallazgo M6 de la revision adversarial de la SPEC) con diff DDL
   documentado. Queda PROHIBIDO un tercer esquema divergente.
6. **VEHICULO Y ROSTER (del GO b699996).** Nova-Payroll nace born-operational, aislada (base +
   store de memoria PROPIOS; cero cableado a Budget/Contabilidad), con roster: Arquitecto / Codex /
   Analista + jball (operador) + **jheredia (Julian) FIRMANTE DESDE EL GENESIS** (su privada
   ed25519 solo en su maquina; HMAC propio de instancia). **Guardrail PII de nomina desde el
   nacimiento** (clausula en el AGENTS de la instancia): salarios/datos de empleados JAMAS entran
   al store de memoria, resumenes, indices ni embeddings; el probe mide el PROCESO de desarrollo,
   nunca los datos. La cross-atestacion de nacimiento se ancla en el hub (patron NOVA Entrada 0).
7. **FRONTERA DOS-TRIOS (DECISION-0095).** El ledger de Nova-Payroll lo escribe SU trio; el
   hub-Arquitecto ejecuta la ceremonia de nacimiento, ancla cross-atestaciones y coordina por
   prompt -- no opera su ledger dia a dia.

## Efecto al firmar

1. El Arquitecto sella esta DECISION en el ledger del hub (submit_intent intent decision).
2. Arranca la ceremonia de nacimiento de Nova-Payroll (papel/ceremonia; no compite con E2).
3. La Fase A queda pendiente de su GO especifico (clausula 4).

## Firma del operador

**[PENDIENTE-FIRMA-OPERADOR]** -- con la firma (mensaje escrito del operador citando esta DECISION,
o su edicion de este bloque), el Arquitecto ejecuta el sellado y lo reporta.
