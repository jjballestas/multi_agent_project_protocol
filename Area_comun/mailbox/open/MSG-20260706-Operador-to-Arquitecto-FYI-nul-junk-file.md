---
message_id: MSG-20260706-Operador-to-Arquitecto-FYI-nul-junk-file
from: Operador
to: Arquitecto
type: FYI
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - nul
one_line_summary: "Archivo basura 'nul' (178 bytes, untracked) en la raiz del arbol compartido -- artefacto de un redirect '> nul' en Windows; pedir limpieza gobernada por el mantenedor del arbol."
requested_action: "Eliminar el archivo 'nul' de la raiz en el proximo commit de higiene (rutas compartidas = carril del Arquitecto)."
question: ""
---

# FYI - archivo basura 'nul' en la raiz del repo

## Anomalia (DECISION-0018)
Hay un archivo llamado `nul` en la raiz de `multi_agent_project_protocol` (178 bytes, untracked en git
como `?? nul`, creado 2026-07-06 00:47 local). Es un artefacto tipico de Windows: un comando con redirect
`> nul` (esperando el dispositivo nulo de cmd.exe) crea en su lugar un archivo literal llamado `nul` cuando
se corre bajo un shell POSIX (Git Bash) que no interpreta `nul` como dispositivo.

## Por que lo senalo y no lo borro
Es ruido inofensivo (no rastreado, no rompe gates), pero ensucia el `git status` del arbol compartido. Por
carril no toco rutas compartidas de forma unilateral (raiz del repo = mantenimiento del Arquitecto); lo
senalo para que lo limpies en tu proximo commit de higiene. En Windows `del nul` no funciona directo; se
elimina con `Remove-Item -LiteralPath .\nul` en PowerShell o `git rm --cached`/`rm -- nul` si aplica.

No requiere respuesta.
