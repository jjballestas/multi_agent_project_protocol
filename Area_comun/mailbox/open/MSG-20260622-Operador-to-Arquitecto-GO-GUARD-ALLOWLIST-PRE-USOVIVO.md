---
message_id: MSG-20260622-Operador-to-Arquitecto-GO-GUARD-ALLOWLIST-PRE-USOVIVO
task_id: none
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Autorar la pieza SDD que el Analista puso como PRECONDICION del GO de uso vivo del extractor: flip del guard de egress de DENYLIST (proveedores nombrados) a ALLOWLIST (deny-all salida de red por defecto; permite solo lo estrictamente necesario) + marcar eval/new Function. Cubre el residual (clientes HTTP no listados + ofuscacion = limite del scan estatico). maker=Codex / checker=Arquitecto + pasada del Analista. ESTO NO ENCIENDE el uso vivo: solo endurece el guard. El GO de uso vivo del extractor LLM va aparte y despues, con su Analista."
question: "Autoras la pieza SDD del guard allowlist (deny-all salida + marcar eval/new Function) como precondicion del uso vivo? El uso vivo sigue OFF; te doy el GO de encendido aparte cuando el guard allowlist este cerrado."
one_line_summary: "GO: autorar el endurecimiento del guard de egress (denylist -> ALLOWLIST deny-all + marcar eval/new Function) como precondicion del uso vivo del extractor, cerrando el residual del scan estatico (clientes HTTP no listados/ofuscacion). NO enciende uso vivo (sigue OFF); el GO de encendido va aparte despues."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0152-v2-faseC-veredicto.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
deadline_or_blocking_level: normal
---

# GO - endurecer el guard a ALLOWLIST (precondicion del uso vivo)

GO para autorar la pieza que el Analista dejo como precondicion del uso vivo del extractor:

- **Flip del guard de egress: denylist -> ALLOWLIST.** Deny-all de salida de red por defecto; permitir solo lo
  estrictamente necesario. El denylist de proveedores nombrados no cubre lo que no conocemos (clientes HTTP no
  listados, ofuscacion) -- residual reconocido por el Analista como limite del scan estatico.
- **Marcar `eval` / `new Function`** (ejecucion dinamica) en el guard.
- maker=Codex / checker=Arquitecto + pasada del Analista, clon limpio + gates.

Importante: **esto NO enciende el uso vivo.** Solo endurece el guard. El extractor LLM sigue OFF-by-default; el
**GO de uso vivo va aparte** y te lo doy cuando el guard allowlist este cerrado y verificado (con su Analista),
porque es ahi donde se abre la ventana de modelo real. Canal ASCII.
