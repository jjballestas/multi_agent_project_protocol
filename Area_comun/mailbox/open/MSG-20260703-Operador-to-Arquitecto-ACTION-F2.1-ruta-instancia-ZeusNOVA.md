---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-F2.1-ruta-instancia-ZeusNOVA
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0230 (F2.1 new_instance, ready)
  - Area_comun/decisions/DECISION-0050 (repos de producto bajo D:/Agentes/Zeus/)
one_line_summary: "La instancia nova-budget de TASK-0230 (F2.1) se crea en D:/Agentes/Zeus/NOVA (ya existe, vacia). Anota la ruta destino en el intake/scope y trasladala a Codex ANTES de que instancie (0230 sigue en ready)."
requested_action: "[DIRECTIVA] (1) La instancia nova-budget de TASK-0230 (F2.1 new_instance) se crea en la ruta D:/Agentes/Zeus/NOVA (ya existe en disco, vacia, lista para recibirla). Es coherente con DECISION-0050: los repos de producto viven bajo D:/Agentes/Zeus/ (hermana de Zeus-protocol y Zeus-Aegis); el hub del protocolo NO se toca. (2) Anota la ruta destino como parametro en el bloque intake/scope de TASK-0230 y trasladala a Codex ANTES de que instancie -- 0230 sigue en ready, la ventana esta abierta. (3) La instancia se genera DESDE el tag v1.18.0 (ya fijado en la orden F2). (4) Si Codex ya hubiera creado la instancia en otra ruta, reubicala a D:/Agentes/Zeus/NOVA y registra el ajuste. [RECOMENDACION] Verifica que el .gitignore/hosting de la instancia sea el suyo propio (repo de producto independiente), no herede rutas del hub."
question: ""
---

# ACTION - Ruta de la instancia F2.1: D:/Agentes/Zeus/NOVA

Directiva del Operador para TASK-0230 (F2.1 new_instance nova-budget): la instancia
se crea en **D:/Agentes/Zeus/NOVA**. El directorio ya existe en disco, vacio, listo.

Encaja exactamente con DECISION-0050 (arquitectura de repos: producto bajo
D:/Agentes/Zeus/, gobernanza en el hub del protocolo). NOVA queda como hermana de
Zeus-protocol y Zeus-Aegis.

0230 esta en `ready` con GO a Codex pero aun sin instanciar: hay ventana para
inyectar la ruta antes de que construya. Si ya hubiera instanciado en otro path,
reubicar. La instancia se genera desde el tag v1.18.0 como fija la orden F2.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
