---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-feasibility-0043
task_id: TASK-0120
from: Arquitecto
to: Codex
type: FYI
status: open
requires_response: true
response_owner: Codex
question: "Pasada de FACTIBILIDAD codigo-invariante sobre DRAFT-DECISION-0043 + DRAFT-SPEC-0082 (resolver el secreto HMAC de event_auth por REFERENCIA: secret_file gitignored / secret_env, no literal), ANTES de promover (toca la ruta de firma). Verifica por tu cuenta: (1) resolve_event_auth_secret en el punto de firma/verificacion (signing_secret/verify_event_auth) SIN alterar el dict de read_protocol_config -> genesis/canonical_json/prev_hash NO dependen del valor del secreto (AC5); (2) precedencia secret(literal)->secret_file->secret_env preserva byte-identidad de los 40+ goldens existentes (AC7); (3) fail-closed real: ref presente irresoluble -> sign_event lanza error de clase, NO escribe evento; verify -> invalido con razon (AC3); (4) gate AC4 (rechazar secret literal de actor vivo en config commiteado; permitir literal solo en examples/) implementable con el scan actual o un check dedicado; (5) seguridad de ruta AC6 (secret_file dentro de SECRET_DIRS gitignored, anti-traversal). Confirmas factible como esta escrito, o levantas algun problema de codigo-invariante? maker!=checker: yo soy autor del diseno, tu revisas el DRAFT; al implementar TASK-0120 se invierten (tu implementas, yo reproduzco). NO promuevas; #4 OFF."
requested_action: "Pasada de factibilidad sobre DRAFT-DECISION-0043 + DRAFT-SPEC-0082 (ruta de firma, AC1-AC8); confirmar factible o levantar problemas concretos. NO promover, NO encender #4. Claims FILE-SCOPED."
one_line_summary: Pasada de factibilidad de Codex sobre el cargador del secreto HMAC (DECISION-0043/SPEC-0082) antes de promover; verifica genesis-intacto/fail-closed/gate-AC4/compat/ruta. NO promover ni encender #4.
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-DECISION-0043-event-auth-secret-resolution.md
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0082-event-auth-secret-resolution.md
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
---

# Pasada de factibilidad - cargador del secreto HMAC (DECISION-0043 / SPEC-0082)

Codex: gracias por el piloto Fase 1 (AC2 20/20, AC3 6/6, AC5 rollback byte-equivalent, flags OFF) -- lo
tomo como **ensayo VERDE** (uso secretos sinteticos inline, que es justo lo prohibido en vivo). El
operador decidio el camino correcto: construir el **cargador del secreto HMAC** (DECISION-0043/SPEC-0082)
ANTES del flip real -- asi el HMAC vive FUERA del repo por referencia. El flip real de #4 ira por ese
camino, no por el piloto sintetico.

Antes de promover, corre tu **pasada de factibilidad** sobre los 2 drafts (ver `question` para los 5
puntos). El diseno ya esta verificado contra codigo por el operador; tu pasada cierra el maker!=checker
del DRAFT (tu revisas; al implementar TASK-0120 te toca implementar y yo reproduzco). **NO promuevas, #4
OFF, claims file-scoped.** Si todo OK, lo promuevo (con confirm del operador) y te paso TASK-0120.
