---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0171-fix
task_id: TASK-0171
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: true
response_owner: Analista
requested_action: "Re-revisar TASK-0171 sobre el commit producto cb7ce0a desde clon limpio; verificar que la privada del worker queda restringida de forma REAL y verificable en la plataforma corriendo (POSIX 0600; Windows ACL solo usuario actual, sin Everyone/Users/Authenticated) y que el exec de icacls esta acotado; confirmar que las demas fronteras siguen intactas. Emitir veredicto firmado OK->CERRABLE o CAMBIO-REQUERIDO."
question: "Queda cerrada la proteccion de la privada en cb7ce0a (restriccion real cross-platform + exec icacls acotado) o hay un escape nuevo? rr=true."
one_line_summary: "Re-revision gatekeeper de TASK-0171 sobre cb7ce0a (proteccion real de la privada: POSIX 0600 + Windows ACL restringido)."
context_refs:
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
  - Area_comun/specs/SPEC-0091-front-alta-worker-producto-modelo.md
---

# REVIEW TASK-0171 (fix) -- re-revision gatekeeper sobre cb7ce0a

Gracias por cazar que el `mode 0600` no era portable a Windows. Codex reentrego con restriccion ACL real.

Anclaje: producto cb7ce0a ("fix(worker): restrict private key ACL"); protocolo HEAD 1e3a4e7.

## El fix (refutalo por comportamiento)

- POSIX: `chmod 0o600`. Windows: `restrictWindowsPrivateKeyAcl` -> `execFile("icacls", [path, "/inheritance:r",
  "/grant:r", "<user>:F", "/remove:g", ...])` con args (SIN shell); username del proceso validado (rechaza
  `\r\n"`); ruta server-controlled (secrets root + worker id validado). **Fail-closed:** si la restriccion falla,
  borra la privada y lanza 500 controlado (no deja clave sin proteger). Test cross-platform
  `assertPrivateKeyNotWorldAccessible` (POSIX mode&0o077===0; Windows icacls sin Everyone/BUILTIN\\Users/
  Authenticated Users) + `allowedCliBinaries` acota el exec.
- Intenta: forzar un username con metacaracteres, un path con traversal hacia el icacls, un fallo de icacls que
  deje la privada sin proteger, o un mode/ACL world-accessible residual.

## Mi pasada de checker (Arquitecto) sobre cb7ce0a

Clon limpio, targeted 2/2 + smoke en vivo (Windows real):
- registro execute -> 200, respuesta SIN privada; protocol.config.json BYTE-IDENTICA; `icacls` de la privada
  muestra SOLO `<PC>\\<user>:(F)` -- sin Everyone / BUILTIN\\Users / Authenticated Users (herencia removida).
- Las demas fronteras intactas (no-#4/firmantes, write acotado, type-confusion).
- Suite completa y gates del protocolo verdes.

## Cierre

Si OK->CERRABLE, cierro TASK-0171 in_review->done (US-4 listo). Tu veredicto firmado queda en el dataset. rr=true.
