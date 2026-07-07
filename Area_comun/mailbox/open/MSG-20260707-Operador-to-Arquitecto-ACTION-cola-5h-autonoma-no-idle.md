---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-cola-5h-autonoma-no-idle
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - Area_comun/decisions/DECISION-1001-iniciativa-ingenieria-disciplinada-antivibecoding-intake.md
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
  - Area_comun/mailbox/open/MSG-20260707-Operador-to-Arquitecto-ACTION-politica-pii-embeddings-aprobada-formalizar.md
one_line_summary: "El Operador estara con el DBA ~5h; cola PROFUNDA y ORDENADA para trabajar autonomo sin idle. Orden: 1207/1105 -> enmienda PII + F4 FTS-only + t6 runbook -> crear/promover 1001 t3-6 -> PREP Contabilidad (esqueleto sobre patron Presupuesto) -> PREP Etapa 2 avanzable -> higiene. Escala SOLO decisiones del operador (dominio/sello/legal/riesgo). El Asesor coordina re-gates y re-llena."
requested_action: "Trabajar esta cola en orden, sin idle, ~5h autonomo (el Operador esta con el DBA). Una tarea de Codex a la vez por capacidad; usa los huecos entre re-gates para escribir SPECs y prep. Escala al Operador SOLO lo suyo (decision de dominio, cambio de sello, riesgo real, legal). El Asesor sigue coordinando los re-gates y te asigna encima si drenas."
question: "Confirmas la cola de ~5h y que la trabajas autonoma? Reporta avance por hitos (no narres pasos). Si algo te bloquea que sea del operador, escalalo y sigue con el siguiente item de la cola."
---

# ACTION - Cola de ~5h autonoma (el Operador esta con el DBA), sin idle

El Operador estara refinando la BD de Contabilidad con el DBA ~5h. Cola ordenada para que NO quedes idle;
trabaja autonomo y escala solo lo suyo. Una tarea de Codex a la vez; los huecos entre re-gates los llenas
escribiendo SPECs y prep.

## Orden de trabajo
1. **Cerrar pendientes de gate:** ratifica/fix-loop el re-gate de TASK-1207 (si sigue in_review); GO
   TASK-1105 (infra test fixture) a Codex.
2. **Memoria (1002):** formaliza la ENMIENDA PII de embeddings (los 6 puntos aprobados, ver el MSG de
   politica-pii) como enmienda de DECISION-1002 en el ledger de Aegis; crea el SPEC + GO de **F4 FTS-only**
   (embeddings opt-in bajo politica, diferidos); crea + GO **t6** (runbook de operacion de memoria) si falta.
3. **Anti-vibecoding (1001) -- el bloque grande:** CREA los 4 SPECs que faltan y promueve en orden, con gate
   adversarial cada uno: t3 (port de la capa a Zeus-Aegis modo-documentos), t4 (Engineering Quality Panel
   MVP), t5 (registro de excepciones user-facing), t6 (test plan de deteccion de ambiguedad, los 8 casos del
   REQ s.13 como suite ejecutable).
4. **PREP Contabilidad (sin construir, no necesita la base aun):** deja listo el ESQUELETO de SPEC/patron de
   Contabilidad reutilizando el patron de Presupuesto (superficie sobre procs, gates, aislamiento, formato
   NOVA-SPEC), para enchufar la base del Operador+DBA en cuanto llegue. Solo estructura.
5. **PREP Etapa 2 (avanzable):** adelanta los items del sello F3.2 que NO dependen de la reconciliacion
   26-29 ni de las DEC de dominio P3.x (lo que se pueda dejar redactado).
6. **Higiene:** al drenar, poda/archiva consumidos (mailbox limpio, prune si vencido).

## Frontera
Todo pre-30-jul a full; nada toca el estudio medido, el genesis del hub, ni la linea roja Q4. El re-genesis
A2 de Julian sigue esperando su pubkey (no bloquea la cola). El BUILD gobernado de Contabilidad espera a
Julian; solo la PREP/estructura avanza ahora.

## No idle
Re-llena al drenar. El Asesor coordina los re-gates en paralelo y te asigna encima. Reporta por hitos.

-- Operador
