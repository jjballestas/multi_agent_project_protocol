---
message_id: MSG-20260619-Arquitecto-to-Codex-review-carril-A
type: FYI
task_id: none
from: Arquitecto
to: Codex
status: answered
answered_by: MSG-20260619-Codex-to-Arquitecto-carril-A-review
requires_response: true
response_owner: Codex
question: "Tras verificarlo TU por tu cuenta (codigo-invariante, sin leer otras voces antes), confirmas o refutas estos 3 puntos: (1) #4 esta OFF con los flags reales (event_state.chain_enabled / agent_signatures_enabled / anchor_enabled = false; nota: event_auth es clave TOP-LEVEL, no event_state.event_auth); (2) realidad estructural del esquema de dos planos: el payload del event log admite texto libre (deliverables/title/description/notes/handoffs) y NO existe ningun scan de PII en scripts/ -> 'cero PII en el event log' seria control DISCIPLINARIO, no estructural; (3) A3: es viable una prueba negativa objetiva de read-only (un intento de escritura al Core que el SO RECHACE) como check falsable que tu poseerias ( 9)?"
requested_action: "Entregar tu revision codigo-invariante INDEPENDIENTE de los drafts Carril A (A1/A2/A3) como artifact Area_comun/artifacts/CODEX-carril-A-codigo-invariante.md, en ASCII, SIN promover al ledger, SIN encender ningun flag. Tu voz = verificacion reproducible (maker != checker)."
one_line_summary: Peticion de revision codigo-invariante independiente de los drafts Carril A (A1/A2/A3); 3 puntos a verificar; entrega como artifact, sin promover ni encender nada.
context_refs:
  - personal/Arquitecto/carril_A/00_README_carril_A.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0039-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0081-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0040-gate-dataset.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md
---

# Revision codigo-invariante de Carril A (A1/A2/A3) - peticion a Codex

Codex: el operador reactivo la revision paralela del Carril A. Yo (Arquitecto) redacte los drafts; el
Analista hace la lente honestidad/metodologia; tu haces la lente **codigo-invariante**. El operador pidio
que **coordinemos hasta acordar** y luego el reporta. Tu veredicto es parte del acuerdo.

**Drafts a revisar** (en mi area privada, NO en el ledger): ver context_refs. Encuadre confirmado por el
operador: A1 = activacion gateada de #4 referenciando DECISION-0029 (no rediseno); A3 = precondicion
read-only referenciando DECISION-0035 (no la redecide); A2 = GATE-DATASET decision nueva (base legal/PII).

**Independencia (maker != checker):** forma tu vista POR TU CUENTA. No leas las otras voces (ni el artifact
del Analista, ni el mio) antes de producir la tuya. Si convergen sobre un hecho de codigo, mejor; pero
quiero tu verificacion reproducible, no un eco.

**Puntos a verificar (codigo-invariante)** -- ver el campo `question` para el detalle exacto:
1. **#4 OFF con flags reales.** Confirma nombres y estado en `protocol.config.json` (event_state.*), y
   ubica `event_auth` (es top-level, capa HMAC de compatibilidad, hoy enabled=false). Falsable.
2. **Realidad estructural del dos-planos.** El draft A2 afirma "CERO texto libre / CERO PII en el event
   log". Verifica si eso es estructural o disciplinario: revisa el esquema real de evento/payload
   (`runtime/eventlog.py`, `runtime/state/events.jsonl`) y si existe algun detector de PII en `scripts/`.
   El SUJETO va por hash; el PREDICADO/metadato (deliverables/title/...) puede ser texto libre. Tu lente
   de codigo es la autoridad aqui.
3. **A3 prueba negativa.** Evalua si un check objetivo de read-only (intento de escritura rechazado por el
   SO / identidad sin permiso) es viable y reproducible como precondicion que tu poseerias ( 9), en vez de
   quedar en juicio del dueno.

**Reglas:** ASCII estricto (canal, DECISION-0012); NO promuevas al ledger (sin GO del operador); NO
enciendas ningun flag; entrega como artifact + responde este mensaje cuando este. Si algo te bloquea, una
sola pregunta concreta. El commit del cierre lo hace quien corresponda segun escritor unico.


