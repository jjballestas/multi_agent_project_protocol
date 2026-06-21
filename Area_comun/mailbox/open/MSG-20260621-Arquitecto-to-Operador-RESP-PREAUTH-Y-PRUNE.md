---
message_id: MSG-20260621-Arquitecto-to-Operador-RESP-PREAUTH-Y-PRUNE
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "Hechas tus 2 directivas. (1) PRE-AUTH ingestion viva REGISTRADA (condicionada: solo tras entrega+cierre de REQ-31100EAF + Analista OK + activacion RUNTIME con versionado OFF; si el Analista pide cambios no aplica). Anotada en el tracker del #9; al cerrar dejare la ingestion runtime-ready sin otro GO. (2) PRUNE gobernado: REQ-984A85C6 (fantasma) y REQ-829CBFCE (duplicado) -> CANCELLED; conservado REQ-40EC863F. validate exit 0, drift 0."
context_refs:
  - Area_comun/tasks/req-31100eaf-requirement-seed.md
  - personal/Arquitecto/carril_A/AUTODRIVE-9req-progress.md
deadline_or_blocking_level: normal
---

# RESP - pre-autorizacion ingestion + prune de junk

## 1. PRE-AUTH ingestion viva (REQ-31100EAF) -> REGISTRADA (condicionada)
Si, registro tu pre-autorizacion condicionada. Al cerrar REQ-31100EAF dejare la carga por archivo lista para
runtime SIN esperar otro GO tuyo, EXCLUSIVAMENTE si se cumplen las 3:
1. feature ENTREGADA y CERRADA;
2. pasada del Analista (ingestion/egress) **OK** (si marca CUALQUIER cambio, la pre-auth NO aplica hasta resolverlo);
3. activacion por **RUNTIME** (env), versionado `enabled:false` OFF-by-default (mismo patron que el push vivo).
No enciendo nada antes de cumplir las 3. Lo anote en el tracker (fila #9) para aplicarlo en el cierre.

## 2. PRUNE de junk del intake -> HECHO (gobernado)
Via submit_intent (proposed -> cancelled, capability orchestrator; el evento queda atestado, el registro #4 es
inmutable asi que "prune" = cancelar, no borrar):
- **REQ-984A85C6** "Conciliar saldos..." (fantasma, narrativa/intencion vacias, no es de NOVA) -> **cancelled**.
- **REQ-829CBFCE** (duplicado del fix de estilo del boton) -> **cancelled**.
- **REQ-40EC863F** (el mas detallado del fix del boton) -> **conservado** (proposed).
El backlog deja de mostrar las 2 basuras. El bug raiz que genero el fantasma lo filas tu como defecto aparte por
el Intake (para que tenga SPEC + fix), como dijiste.

## Nota
Sigo conduciendo el batch de los 9 (autodrive): 5/9 done; #6 TASK-0145 en cola (Codex aun no lo tomo).
validate exit 0, drift 0. Canal ASCII.
