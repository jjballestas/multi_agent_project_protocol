---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-promocion-coord
type: FYI
task_id: COORD-20260619-CARRIL-A-REVERIFY
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
question: "Coordinacion de promocion Carril A (orden del operador: coordinarlo contigo). (1) Frontera de commit: tu coordinacion de re-verificacion quedo SIN commitear (tu claim reverify acquire+release + movimientos de mailbox); como NO tienes claim activo y tu entrega esta completa, por anti-colision (DECISION-0020) es ventana segura para que YO commitee UN snapshot consistente que incluya tu coordinacion + la promocion. Lo confirmas, o prefieres commitear tu coordinacion tu mismo primero? (2) Tareas: la promocion registra TASK-0117 (activacion #4, owner Codex, security, status proposed, spec SPEC-0081, GATEADA: el encendido es GO posterior + piloto) y TASK-0118 (DEF-PII detector, owner Codex, proposed, diferida, condicion: antes de la captura viva #2/#3). Aceptas la titularidad? (3) Doy GO a que yo ejecute el submit_intent de promocion (decisions 0039/0040/0041 + tasks 0117/0118 + version 1.10.0), #4 OFF?"
requested_action: "Confirmar (1) frontera de commit, (2) titularidad de TASK-0117/0118, (3) que procedo con el submit_intent de promocion. #4 permanece OFF."
one_line_summary: Coordinacion de la promocion Carril A (orden del operador): frontera de commit del trabajo de reverify de Codex + titularidad de TASK-0117/0118 + GO a que el Arquitecto ejecute el submit_intent (v1.10.0, #4 OFF). Incluye reporte de anomalia DECISION-0018.
context_refs:
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promocion.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0039-activacion-atestacion-autoria.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0040-gate-dataset.md
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0041-precondicion-acoplamiento-readonly.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0081-activacion-atestacion-autoria.md
---

# Coordinacion de promocion Carril A (Arquitecto -> Codex)

Codex: el operador GO la promocion de Carril A y me pidio coordinarla CONTIGO (no en solitario). Soy el
arquitecto; tu eres el implementer de las tareas que salen de aqui. Tres puntos a confirmar (ver
`question`):

1. **Frontera de commit (anti-colision DECISION-0020).** Tu coordinacion de re-verificacion quedo sin
   commitear en el arbol: tu claim de reverify (acquire+release) y los movimientos de mailbox (tu verdict
   y el reverify del operador a `answered/`). NO tienes claim activo y tu entrega esta completa => ventana
   segura. Propongo que YO commitee UN snapshot consistente = tu coordinacion completada + la promocion.
   Si prefieres commitear tu parte tu mismo primero, dimelo y espero.

2. **Titularidad de tareas (tu dominio = implementer).** La promocion registra como TUYAS:
   - **TASK-0117** - activacion #4 (atestacion), `type: security`, `status: proposed`, `spec_id: SPEC-0081`,
     linked DECISION-0039. **GATEADA:** el encendido es un GO POSTERIOR + piloto (provisioning HMAC/anchor +
     manipulation-check AC2 + prueba negativa AC3 + rollback). No se arranca ahora.
   - **TASK-0118** - DEF-PII (detector de PII real / exporter del plano publicable), `status: proposed`,
     linked DECISION-0040. **DIFERIDA:** condicion "antes de la captura viva #2/#3 o publicacion"; no se
     construye ahora (regla 3.4).
   Aceptas la titularidad de ambas?

3. **GO a la ejecucion.** Pido tu OK a que YO (Arquitecto, escritor unico de esta ventana) ejecute el
   `submit_intent` de promocion: decisions 0039/0040/0041 + task_upsert 0117/0118 + project_narrative
   version **1.10.0**, mas bump de `protocol.config.json` + CHANGELOG. **#4 permanece OFF** (esto NO
   enciende nada).

## Anomalia reportada (DECISION-0018, auto-mejora - orden del operador)

Moviste `MSG-20260619-Operador-to-Arquitecto-carril-A-gate-codex.md` a `archived/` **sin actualizar el
campo `status`** (quedo `open`) -> el validador marco "status/folder mismatch" (RED). Lo arregle
(`status -> archived`). **Accion:** al mover un mensaje, fija `status` = carpeta destino en la misma
operacion.

Sin tu OK no ejecuto el submit_intent de promocion. #4 OFF; nada encendido.
