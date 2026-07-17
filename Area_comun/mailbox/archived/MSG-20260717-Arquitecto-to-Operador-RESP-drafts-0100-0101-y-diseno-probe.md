---
message_id: MSG-20260717-Arquitecto-to-Operador-RESP-drafts-0100-0101-y-diseno-probe
from: Arquitecto
to: Operador
type: RESP
status: archived
requires_response: true
response_owner: Operador
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0100-adopcion-memoria-hibrida.md
  - Area_comun/decisions/DECISION-0101-checker-formal-proveedor-diverso.md
  - personal/Arquitecto/DISENO-probe-coste-peon-local.md
one_line_summary: "ENTREGA de tus 3 encargos: (1) DRAFT DECISION-0100 adopcion memoria hibrida PARA FIRMA (alcance confirmado: adopta + promocion master hub agendada Fase 3+ post-ventana + re-juicios via 0101 + F2 NO); (2) DRAFT DECISION-0101 checker formal a Claude/Anthropic CLI PARA FIRMA (confirmo destino y alcance hub+espejo 0096; anade regla maker!=checker por PROVEEDOR); (3) DISENO del probe de coste del peon para tu revision (sub-tarea = lote tests NEG PII por clave, mitades disjuntas sorteadas, delta frontier con overhead contado, umbral pre-declarado 25%). Nada se ejecuta sin tu firma/OK."
requested_action: "Revisar y FIRMAR (o ajustar): DECISION-0100 y DECISION-0101 (patron 0091/0099; al firmar las sello via submit_intent). Del probe: OK al diseno + eleccion de modelo local (qwen2.5-coder:7b vs deepseek-coder:6.7b vs el que tengas en Ollama) + GO de ejecucion tras cierre de TASK-0005."
question: "Firmas 0100 y 0101 tal cual (o con ajustes), y das OK al diseno del probe con que modelo local?"
---

# RESP - Drafts 0100 + 0101 para firma y diseno del probe

## (1) DECISION-0100 - Adopcion (confirmo tu alcance)

Draft en context_refs. Recoge exactamente tu decision: adopcion POR DEMOSTRACION (4 criterios
verdes + DEMO REVIVE conductual, que ademas opero una SEGUNDA vez en la remediacion del
runbook); promocion al master hub via export 0096 AGENDADA a Fase 3+ post-ventana-medida (cero
toques a scripts/ del hub durante la ventana); re-juicios formales U3/U4 via 0101; runbook
cierra su ciclo; F2 NO. Firewall integro.

## (2) DECISION-0101 - Checker a proveedor diverso (confirmo destino y alcance)

Draft en context_refs. CONFIRMO tu recomendacion en ambos ejes y la fortalezco: destino
Claude/Anthropic CLI (elimina el falso positivo de raiz, formaliza el fallback que ya opero con
calidad verificada) y alcance capa HUB con espejo 0096. Anadi como regla de roster la
diversidad de PROVEEDOR (maker!=checker por capacidad + llave + proveedor, extension de 0099
r3) y la clausula "los probes no se degradan jamas: se cambia el proveedor, no el mandato".
Implementacion = tarea de configuracion del harness reviewer (el runner generico ya admite
-AgentExe; es cableado, no codigo) tras tu firma.

## (3) Diseno del probe de coste (para tu revision, sin ejecutar)

Diseno completo en context_refs. Confirmo tu estructura con 4 refinamientos: sub-tarea = lote
de tests NEG PII por clave allowlisted (real, mecanica, con criterio de correccion DURO por
exit-code de la suite -- el checker automatico no gasta frontier); mitades DISJUNTAS asignadas
por sorteo (evita el sesgo de segundo-pase); contabilidad explicita con el overhead de
spec+review dentro del coste B y umbral pre-declarado (B gana si ahorra >=25% frontier con
suite verde); la spec del maker al peon queda como artefacto = evidencia de 0099. Espero tu OK
+ modelo local + GO post-cierre-0005.

## Estado del carril (contexto)

TASK-0005: remediacion del byte-exacto ENTREGADA por el maker revivido (2da operacion REVIVE;
prueba sha==blob en clon limpio) -> re-judgement del Analista formal EN CURSO. El nudge de U4
quedo superado por los hechos (U4 done via fallback declarado). Higiene de tu panel en el
siguiente lote.

-- Arquitecto. Hora local ~22:05 (UTC+2). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
