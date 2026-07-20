---
message_id: MSG-20260720-Analista-to-Arquitecto-REVIEW-TASK-0268-veredicto
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Rutear a Codex la remediacion docs-only del hallazgo H1: README_INSTANCIACION afirma que todo commit materializa el snapshot staged, pero el default acotado entregado no materializa (juzga el arbol de trabajo). Corregida esa frase (1-2 lineas, sin tocar hook ni pin CI), el Analista re-juzga ese commit y TASK-0268 queda CERRABLE. Todo lo funcional PASA."
question: "Ruteas la remediacion H1 a Codex, o decides con el operador aceptar el texto actual como residual documentado y cerrar sin fix?"
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md
  - Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md
  - Area_comun/handoffs/HANDOFF-TASK-0268-Codex-to-Analista.md
one_line_summary: "Veredicto TASK-0268: CAMBIO-REQUERIDO acotado a docs (H1: README promete materializacion staged que el default no ejecuta); funcional todo PASA -- default 0.455-0.483s en commit gobernado real, flags env/config activan v2 intacta (rechazo staged roto, 29-32s), pin CI == hook, suite y espejo born-operational verdes."
---

# REVIEW TASK-0268 -- veredicto del Analista: CAMBIO-REQUERIDO (docs-only)

Hora local: 2026-07-20 05:53 (+0200). Ancla: HEAD f2d07a3 en clon limpio; entrega b37e638.
rr=true. Detalle completo, reproduccion con exit codes y tabla vector por vector en
Area_comun/artifacts/ANALISTA-TASK-0268-reparto-acotado-veredicto.md.

## Lo que PASA (mediciones propias, clon limpio)

- Default acotado en commit gobernado REAL (git commit con hooksPath): 0.455s / 0.482s /
  0.483s (<~2s del AC; reproduce el 0.449s del handoff). Conserva poda (fallo -> bloquea)
  y drift de guia (drift staged -> bloquea).
- Reparto probado por comportamiento: el mismo staged gobernado ROTO que el default
  acepta en 0.494s es rechazado bajo flag con la mecanica v2 completa (HOOK_FULL=1:
  exit 1 en 29.3s; git config hook.full true: exit 1 en 32.4s; env gana sobre config
  false). Mecanica de materializacion intacta respecto a lo ratificado en 0267.
- CI: diff toca SOLO la linea del pin; pin 4dae776c... == sha256 real del hook.
- Suite exit 0 en clon limpio (caso nuevo default-rapido + negativos v2 bajo flag).
- Espejo born-operational: instancia nueva nace con hook byte-identico; tier runtime
  emite CI con el pin nuevo.
- Gates: validate exit 0 con y sin secretos (drift 0); scan_encoding exit 0; neutralidad
  roja en el ancla SOLO por el fixture preexistente de 0271 (0 hits en rutas 0268; ya
  verde a 45eb10f); protocol.config.json 2E35F26E byte-identico.

## Lo que bloquea el cierre: H1 (docs)

README_INSTANCIACION.md: "para todo commit materializa el snapshot staged" es FALSO en el
default entregado. El acotado no materializa nada: inspecciona el arbol de trabajo (el
hook mismo lo declara y lo probe en ambas direcciones: staged roto aceptado en 0.5s;
prune roto solo-en-arbol rechazado). El adoptante leeria una garantia de juicio staged
que solo el flag y el CI dan. Remediacion docs-only de 1-2 frases; hook y pin no cambian.

Fix-loop declarado: Codex corrige README -> re-juicio del Analista sobre ese commit
(lectura + scan_encoding + validate en clon limpio) -> CERRABLE. Maximo 2 iteraciones
antes de escalar al operador.

Residuales no bloqueantes declarados en el artefacto (R1 arranque frio 22.5s ambiental,
R2 via config sin caso de suite, R3 dependencia de arbol en acotado, R4 HOOK_FULL solo
"1", R5 CI como unico detector de auto-borrado del validador).
