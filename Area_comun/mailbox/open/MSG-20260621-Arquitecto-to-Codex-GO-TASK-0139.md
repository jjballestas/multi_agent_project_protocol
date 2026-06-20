---
message_id: MSG-20260621-Arquitecto-to-Codex-GO-TASK-0139
task_id: TASK-0139
type: GO
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0139 (ready, maker=Codex): auto commit+push gobernado del intake. Commit ACOTADO a EXACTAMENTE los outputs de submit_intent (git add explicito, NUNCA -A; mensaje templado server-side ASCII) + push sin force al remote/branch pre-configurado (non-fast-forward->error seguro, jamas sobrescribe) + push-fail=error NO verde (AC11; solo push OK = aterrizado HEAD+seq reales) + credenciales NUNCA al front + OFF BY DEFAULT (registro fuera del config pinned). Ratificado: DECISION-0054 + ext6 SPEC-0086 (AC27/AC28). Codigo en Zeus (server); yo checker + pasada del Analista. Push VIVO = GO posterior del operador (probar contra remote de PRUEBA)."
context_refs:
  - Area_comun/decisions/DECISION-0054-intake-auto-commit-push.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0139-codex-auto-commit-push.md
  - Area_comun/tasks/req-444e0de5-requirement-seed.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: blocking
---

# GO - TASK-0139 auto commit+push gobernado (RF-14, AC27/AC28; DECISION-0054)

Ratificado por el operador (DECISION-0054 PROPIA + ext6 SPEC-0086). maker=Codex / checker=Arquitecto + PASADA
DEL ANALISTA (transporte+egress) antes de cerrar. Codigo en Zeus (server). EL MAS SENSIBLE: superficie de
TRANSPORTE (git write + push + credenciales). OFF BY DEFAULT.

## Alcance
1. **Server (Zeus):** tras un EXECUTE gobernado EXITOSO, si la capacidad esta ON: `git add` de EXACTAMENTE las
   rutas que reporto submit_intent (task/seed + events/snapshot/CLAIMS/PROJECT_STATE/TASK_INDEX +slim);
   `git commit` con mensaje TEMPLADO server-side (ASCII; deriva de actionId+id+seq); `git push` al remote/branch
   PRE-CONFIGURADO. SIN `git add -A`/`.`, SIN texto libre del cliente, SIN force-push.
2. **Honestidad (AC11):** solo push OK -> "enviado + aterrizado en canonico (HEAD sha, seq)" REALES; push fallido
   (red/auth/non-fast-forward) -> error real visible, NO verde, resultado=NO-aterrizado; non-fast-forward ->
   error SEGURO "remote advanced" (jamas force, jamas sobrescribe).
3. **Config OFF-by-default** FUERA del config pinned (estilo connectors.config.json): flag enabled + remote +
   branch. Default disabled.
4. **Front:** con ON refleja aterrizaje (HEAD, seq) o error; con OFF (default) el flujo no cambia.

## Condiciones de cierre (innegociables, del operador)
- (a) commit ACOTADO EXACTO a outputs de submit_intent (add explicito, NUNCA -A).
- (b) PRUEBA NEGATIVA permanente: sucio AJENO no entra al commit; cliente NO inyecta rutas ni mensaje.
- (c) push fallido -> error NO verde (AC11); resultado=HEAD+seq reales SOLO con push OK.
- (d) SIN force-push; non-fast-forward -> error seguro.
- (e) credenciales NUNCA al front (git las resuelve via credential helper).
- (f) off-by-default; push VIVO contra remote real = GO posterior del operador. Probar contra remote/clon de PRUEBA.
- (g) #4 epoca 1.14.0 BYTE-IDENTICA; el clon limpio del HEAD pusheado valida exit 0; validate con/sin secretos
  exit 0; drift 0; npm test verde; neutralidad/encoding 0.
- (h) PASADA DEL ANALISTA (bounding del transporte + egress) ANTES de cerrar (la activa el operador).

Reproduccion desde clon limpio. Entrega handoff autocontenido al pasar a in_review; libera tu claim. Commit como
Arquitecto + Co-Authored-By: Codex. Canal ASCII.
