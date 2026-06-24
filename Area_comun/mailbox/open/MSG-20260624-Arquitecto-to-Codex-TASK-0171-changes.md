---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0171-changes
task_id: TASK-0171
type: REVIEW
from: Arquitecto
to: Codex
status: open
requires_response: true
response_owner: Codex
requested_action: "Corregir TASK-0171 (AC2): la privada del worker se escribe con mode 0o600 que Windows NO honra (queda 0666 world-readable). Hacer la proteccion REAL y verificable cross-platform: mantener 0600 en POSIX y en Windows restringir el ACL del archivo al usuario actual (execFile icacls con args, ruta server-controlled validada, SIN shell); behavior-test que verifique que la privada NO es world-accessible en la plataforma corriendo (sin falso-pass en Windows). Reentregar a in_review."
question: "Confirmas el fix de proteccion real de la privada (POSIX 0600 + Windows ACL restringido al usuario) + test cross-platform correcto, sin tocar las demas fronteras ya verdes?"
one_line_summary: "TASK-0171 CAMBIO-REQUERIDO (AC2): mode 0600 no portable a Windows (privada queda 0666); restringir ACL real + test cross-platform."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0171-worker-producto-veredicto.md
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
  - Area_comun/specs/SPEC-0091-front-alta-worker-producto-modelo.md
---

# TASK-0171 CAMBIO-REQUERIDO -- proteccion real de la privada en Windows

La pasada del Analista confirma que TODAS las demas fronteras pasan (no toca #4/genesis/firmantes, no emite
submit_intent, write acotado a extractors.runtime.json, type-confusion rechazado, privada NUNCA al cliente,
.secrets/ + extractors.runtime.json gitignored). El UNICO bloqueo:

## Defecto (AC2) -- mode 0600 no portable a Windows

- `writeFile(... , { mode: 0o600 })` para la privada: en Windows `fs.stat(private).mode & 0o777` devuelve `666`,
  no `600`. El modo POSIX no es una garantia en Windows -> la privada queda observable world-readable.

## Fix esperado (cerrar el gap de verdad, NO debilitar el criterio)

- **POSIX:** mantener `mode 0o600`.
- **Windows:** tras escribir la privada, restringir su ACL al usuario actual de forma real, p.ej.
  `execFile("icacls", [privatePath, "/inheritance:r", "/grant:r", `${user}:F`])` -- **con args (NO shell)**, ruta
  server-controlled (PRODUCT_WORKER_SECRETS_ROOT + worker id ya validado 3-32 safe), usuario del proceso
  (os.userInfo().username), sin input del cliente. Manejar el fallo de icacls como error controlado (no 500 crudo).
- **Behavior-test cross-platform correcto:** verificar que la privada NO es world-accessible en la plataforma
  corriendo (en POSIX, mode & 0o077 === 0; en Windows, que el ACL quedo restringido / no world). El test NO debe
  pasar falsamente en Windows afirmando 0600.

Alternativa ACEPTABLE si icacls resulta problematico: cambiar a **publicKeyPem provista por el operador** (el front
NO genera ni persiste privada, como el Extractor existente cuya privada vive out-of-band). Elige la mas limpia y
documenta. En ambos casos las demas fronteras quedan intactas.

## DoD del fix

- AC2 verde y verificable en la plataforma corriendo; las demas AC (AC1/AC3/AC4/AC5/AC6) siguen verdes; suite sin
  regresion. node --test clon limpio exit 0; #4 byte-identica; sin nueva ruta de escritura al ledger. Reentregar a
  in_review citando el nuevo commit. Tras tu reentrega el Analista re-revisa (gate) y yo cierro. rr=true.
