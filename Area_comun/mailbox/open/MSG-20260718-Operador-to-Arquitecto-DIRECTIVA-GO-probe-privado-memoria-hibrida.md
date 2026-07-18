---
message_id: MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-probe-privado-memoria-hibrida
from: Operador
to: Arquitecto
type: DIRECTIVA
status: open
requires_response: false
created_at: 2026-07-18
context_refs:
  - personal/asesor/DRAFT-preregistro-medicion-memoria-hibrida-v0.1.md
one_line_summary: "GO probe PRIVADO (no citable, instancia aislada patron Nova-Payroll) de la memoria hibrida: determinar CON DATO que funciona sobre los AGENTES gobernados (no peones). Prueba empirica de lo que Engram manifiesta (funciona + comparte contexto entre agentes) + nuestros diferenciadores (REVIVE atestado, procedencia firmada). 4 metricas con umbrales ex-ante: A re-derivacion evitada (CON<SIN >=40pct), B recall-hit >=85pct/precision >=70pct, C fidelidad REVIVE >=95pct+drift0, D compartir contexto Codex->Analista (exito via-memoria-sola >=90pct + ahorro >=30pct). Corpus: tareas sinteticas con dependencia cross-agente DISENADA (el N=6 se reserva para la medicion citable). Pre-registra ex-ante como el DISENO-QCBARATO. Autoridad delegada al Asesor."
---

# DIRECTIVA - Probe PRIVADO de la memoria hibrida (determinar que funciona, con dato)

## Marco (patron peones)
Probe PRIVADO, NO citable, decision-support, en instancia AISLADA (patron Nova-Payroll o instancia
nueva a tu criterio). Determinar con DATOS MEDIBLES que la memoria hibrida funciona. Sujeto: los
AGENTES gobernados que trabajan con la metodologia (NO peones) -- la memoria los abarca a todos.
Probamos EMPIRICAMENTE lo que Engram manifiesta (funciona + comparte contexto entre agentes) +
nuestros diferenciadores (REVIVE atestado, procedencia firmada, round-trip, drift 0). Honestidad:
criterios de exito/refutacion CONGELADOS ex-ante (el probe de peones volvio negativo; este igual si
toca). Si da SENAL POSITIVA -> despues se re-mide como estudio SELLADO citable (pre-registro Fase B).

## Diseno (2 factores donde aplique; pre-registra EX-ANTE antes de medir)
- Corpus: TAREAS SINTETICAS con dependencia CROSS-AGENTE disenada (NO el N=6, reservado a la
  medicion citable). Disena cadenas donde un agente deriva contexto que otro necesita.
- Par cross-agente para D: Codex -> Analista (proveedores/roles distintos).
- Gate de integridad TRANSVERSAL en TODAS las metricas: round-trip verde, drift 0, procedencia
  firmada, PII fuera del store. Un ahorro/recall que rompa integridad NO cuenta.

## Metricas + umbrales ex-ante (a congelar; el operador delega su fijacion al Asesor, revisa antes del freeze)
- A RE-DERIVACION EVITADA (intra + cross-agente): SIN memoria (re-deriva) vs CON memoria (recall),
  misma tarea. EXITO: CON < SIN por >= 40 pct tokens en tareas recall-elegibles, gate verde igual.
  REFUTA: CON >= SIN o el recall mete defectos.
- B RECALL-HIT: hit-rate = relevantes recuperadas-y-usadas / existentes; precision = recuperadas
  relevantes / recuperadas. Incluye recall por un agente DISTINTO del que guardo. EXITO: hit >= 85
  pct y precision >= 70 pct. REFUTA: hit bajo o precision baja.
- C FIDELIDAD DEL REVIVE: revivir un agente desde su revive_pack. EXITO: fidelidad >= 95 pct del
  set + drift = 0 (duro) + round-trip verde + firma verificable. REFUTA: diverge / drift!=0.
- D COMPARTIR CONTEXTO (Codex -> Analista, la claim central de Engram): Codex deriva contexto ->
  memoria compartida -> Analista resuelve tarea dependiente usando SOLO la memoria (sin
  re-comunicacion directa). EXITO: Analista correcto via-memoria-sola >= 90 pct + ahorro >= 30 pct
  tokens vs baseline sin-memoria-compartida. REFUTA: no puede sin re-comunicacion, o exito < 90 pct.
- GLOBAL: "funciona con dato" si A+B+C+D superan umbral BAJO el gate de integridad. NO en cualquiera
  se reporta como tal.

## Tamano de muestra
Right-size para un probe CREIBLE pero barato (patron peones): suficientes trials por metrica para
que el numero no sea anecdota (propuesta: >=10 tareas A, >=20 recalls B, >=3-5 REVIVE C, >=10
cadenas cross-agente D). Ajusta a tu criterio de foco y declaralo.

## Claims de Engram a marcar explicitamente en el reporte
Por cada claim (funciona / comparte contexto entre agentes) -> VERIFICADO o REFUTADO con el dato.
Mas nuestros diferenciadores (REVIVE atestado, procedencia firmada) que Engram no tiene.

## Autoridad y flujo
Autoridad delegada al Asesor para resolver dudas de diseno (escenarios sinteticos exactos, N,
ajuste de umbrales antes del freeze). El Asesor escala al Operador solo por firma soberana /
adopcion / stall. Demo PRIVADA, NO citable. Fondo intocable N=500 / 2E35F26E / 1.14.0. Pre-registra
ex-ante y reporta por mailbox al cerrar cada metrica + verdicto global + log de decisiones.

-- Operador (via Asesor). 18-jul.
