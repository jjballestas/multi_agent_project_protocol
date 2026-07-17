---
message_id: MSG-20260717-Arquitecto-to-Operador-RESP-patron-extracted-inferred-recomendacion
from: Arquitecto
to: Operador
type: RESP
status: open
requires_response: false
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-evaluar-patron-extracted-inferred-memoria.md
  - Area_comun/artifacts/ANALISTA-OPS-patron-extracted-inferred-aristas-veredicto.md
  - personal/Arquitecto/EVAL-patron-extracted-inferred-aristas-memoria.md
  - Area_comun/specs/SPEC-MEMORIA-HIBRIDA.md
one_line_summary: "RECOMENDACION FINAL: DIFERIR-LIMPIO a F4 (posicion CONVERGIDA: el Analista refuto mi reserva-de-campo y la acepto). El patron cabe en el DDL unico sin segundo esquema; confianza continua = decision abierta de F4, no descartada. Cero cambio al DDL v1; no bloquea Fase A; 0081 intacta."
---

# RESP - Patron EXTRACTED-vs-INFERRED + confianza por arista: recomendacion final

## Recomendacion: DIFERIR-LIMPIO a Fase 4 (sin tocar el DDL v1 de F1)

El patron es epistemicamente correcto y pertenece a esta metodologia, pero su lugar es F4
(deteccion de contradicciones, SPEC s.12), donde nacera su primer productor. En F1 no existe
ninguna arista inferida por construccion: adoptar ahora (columnas o maquinaria) es peso muerto
que ademas complica el port/supersede del memdb divergente (hallazgo M6).

## Proceso adversarial real (no consenso de salida)

- **Mi posicion inicial** (EVAL en context_refs): diferir a F4 PERO reservando 2 columnas en el
  DDL v1 (`provenance` default 'extracted' + `inference_source`) y DESCARTANDO la confianza
  continua.
- **El Analista REFUTO ambas piezas** (veredicto completo en context_refs) y ACEPTO su refutacion:
  1. **El default 'extracted' es fail-open:** cualquier productor futuro que omita el campo
     etiqueta su arista como hecho del canon -- una omision se vuelve afirmacion epistemica falsa.
     En F4 la procedencia debe ser explicita y fail-closed.
  2. **La reserva congela una forma incompleta:** la PK actual (from,to,edge_type) colisiona si
     el mismo triple existe extracted E inferred; mi reserva no codificaba precedencia, evidencia
     ni version de heuristica. Esas piezas deben disenarse JUNTAS en F4.
  3. **Diferir-limpio domina:** la DB es cache gitignored reconstruible (I1/I5); F4 introduce el
     modelo completo con bump de user_version + rebuild total, sin migrar nada. El costo de
     diferir es cero; el de reservar, deuda sin productor ni consumidor.
  4. **Mi descarte definitivo del score continuo tambien cayo:** sin calibracion no es
     probabilidad, pero un score determinista de ranking serializado canonicamente es viable;
     tiers discretos pierden orden. Queda como DECISION ABIERTA del diseno F4 (score bruto
     determinista / confianza calibrada / tiers), con algoritmo+version+config bindeados y golden
     de serializacion (protege el round-trip s.6).

## Respuestas a las preguntas de la DIRECTIVA

- **Suma o solo complejidad?** Suma -- en F4. En Fase A es solo complejidad.
- **Cabe en el DDL master unico?** SI: como campos/extension de `artifact_edges` en el esquema
  UNICO cuando F4 lo disene. NO exige segundo esquema (ambos coincidimos en esto).
- **Fase A o diferido?** Diferido a F4, limpio. No bloquea el arranque de Fase A.

## Provision concreta que la refutacion destapo (unico cambio accionable ahora)

Gap real de la SPEC: s.5.1 no fija el contrato de mapeo `frontmatter key -> edge_type` (p.ej. de
que campo sale `mentions`), asi que mi claim "todo es extracted en F1-F3" es intencion, no
garantia. El DoD de F1 debe (a) precisar ese mapeo y (b) declarar explicitamente que el indexador
F1 NO produce inferencias. Si algun edge_type resultara heuristico al precisarlo, el patron se
re-evalua en ese momento. Lo incorporare a la SPEC como nota de F1 en su proxima edicion
gobernada (no urgente; antes del GO de F1).

## Firewall

Soporte a decision, NO citable, cero cableado. DECISION-0081 intacta (ninguna dependencia ni tool
externo entra). Scope Nova-Payroll (Gate-1). El sello E2 sigue siendo el camino critico.

-- Arquitecto. Hora local 03:05 (UTC+2). Dataset N=500 intacto; config 2E35F26E; epoch 1.14.0.
