---
decision_id: DECISION-0102
title: "NO adopcion de peones locales en el flujo NOVA (condicionada a replicar un metodo que ahorre sin sacrificar calidad)"
status: DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR
date: 2026-07-18
deciders: [operador humano]
supersedes: []
supersedes_partial: [DECISION-0099]
superseded_by: []
relates_to: [DECISION-0099, DECISION-0101]
phase: P2
scope: practica-operativa
approval_ref: "PENDIENTE: firma del operador. Relay del Asesor en MSG-20260718-Operador-to-Arquitecto-DECISION-no-adoptar-peones-condicionada (el Asesor relaya, no firma). Este DRAFT vive en personal/Arquitecto/ y NO entra al ledger (intent decision) hasta la firma."
---

# DECISION-0102 (BORRADOR para firma) - NO adopcion de peones, condicionada

> BORRADOR redactado por el Arquitecto a peticion del Operador (via Asesor, 18-jul).
> NO firmado, NO anclado. Al firmarse: mover a Area_comun/decisions/ + intent decision.

## Decision
NO se adoptan peones locales (modelos via Ollama como makers delegados) en el flujo de
desarrollo NOVA, ni por ahorro de coste ni por capacidad.

## Base de evidencia (serie completa, demo privada NO citable, instancia Nova-Payroll,
TASK-0006..0020, 18-jul; manual v1.3 s.1-s.10; sellos 0101 en todas las entregas)
1. Piloto (19 celdas + confirmatorio lote-100): NO-CRUCE; premium delegado ~+7 pct
   constante; delegar no ahorra tokens frontier.
2. Variante QC-barato (3 condiciones + celda marginal): sigue sin cruce (+4.0 pct
   steady-state); el sanitizador mecanico aporta (-3.1pp), el checker LLM local no
   (0 true-positives).
3. Veredicto estructural (4to brazo): el regimen dominado-por-generacion NO existe
   dentro de la clase delegable (mecanicamente especificable + gate duro): la generacion
   frontier es intrinsecamente barata ahi; lo caro de generar no es delegable.
4. Techo de entrega medido: la entrega estructural del 7b es fiable a bloques de 5
   funciones, pero el techo real es de REPARACION (el peon no consume feedback
   correctivo: bounce-noop 4/5) -> la "capacidad" delegada exige correccion frontier
   frecuente: capacidad neta insuficiente.

## Condicion de reapertura (unica via)
Revisar y REPLICAR (con nuestro protocolo de medicion pre-registrado y sellos
adversariales) un metodo de la literatura que demuestre ahorro SIN sacrificio de calidad.
Los metodos conocidos (familia FrugalGPT/RouteLLM) ahorran cediendo ~5 pct de calidad,
que este proyecto no acepta. Sin esa replica exitosa, esta decision permanece.

## Efectos
- Manual NOVA v1.3: s.8/s.9/s.10 marcadas NO ADOPTADO; sus recomendaciones operativas
  quedan como guia condicional ("si algun dia se usan peones"), no como practica.
- DECISION-0099 (politica de roster peones maker-only) queda superseded-parcial en lo
  que asuma uso activo de peones; el conocimiento medido se conserva como evidencia.
- El foco de medicion pivota a la memoria hibrida (Fase B; pre-registro del Asesor en
  redaccion, firma del operador, anclaje del intent por el Arquitecto al sellarse).
- Fondo intocable: N=500 / 2E35F26E / 1.14.0. Nada de esta decision toca el ledger
  atestado hasta la firma.

## Firma
Operador humano: ____________________ (fecha: __________)
