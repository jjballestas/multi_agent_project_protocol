---
message_id: MSG-20260702-Arquitecto-to-Codex-ACTION-TASK-0229-remediacion-branding-4-scope
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/decisions/DECISION-0082-branding-user-visible-scope-ws3.md
  - Area_comun/artifacts/ANALISTA-TASK-0229-remediacion-branding-3-veredicto.md
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
one_line_summary: "TASK-0229: nuevo AC por DECISION-0082 -- el gate cubre SOLO lo renderizado al usuario; rebrandea esa superficie finita y entrega una ALLOWLIST ETIQUETADA del resto (no cero-grep)."
requested_action: "Remediacion final de TASK-0229 bajo el AC de DECISION-0082 (leela). El gate ya NO es 'git grep -i hermes == 0'. (1) Rebrandea a Zeus TODA cadena hermes que se RENDERICE al usuario final del app shipped: UI/JSX/i18n mostrada, onboarding, ayuda/salida de CLI, mensajes de error/toast/notificacion mostrados, URLs/enlaces/paths user-facing. El Analista cito como user-facing: early-access.tsx, hermes-world-landing.tsx, y strings de error/help publicos en claude-agent.ts, gateway-capabilities.ts, mcp/*.ts, swarm-dispatch.ts -- traza cada uno: si se muestra al usuario, rebrandea; si NO se surfacea, va a allowlist. (2) REGENERA electron/server-bundle.cjs desde el src limpio. (3) Entrega una ALLOWLIST ETIQUETADA: por cada hit hermes que quede tras `git grep -i hermes -- vendor/hermes-2.3.0/src vendor/hermes-2.3.0/electron/server-bundle.cjs`, una etiqueta {identificador|import|comentario|dev-log-no-surfaceado|test-fixture|licencia-provenance|env-shim} y una linea de por que no se renderiza. La carga de la prueba de 'no se renderiza' es tuya. Sin regresion: shim, npm test verde por EXIT, binarios/appId no renombrados, NOTICE MIT. Reentrega a in_review con la allowlist adjunta para que el Analista gatee contra ella."
---

# ACTION TASK-0229 - remediacion final acotada (DECISION-0082)

El operador acoto el alcance ante 4 NO-GO: **DECISION-0082** redefine 'user-visible' -- el gate cubre SOLO la
superficie RENDERIZADA al usuario final; los strings internos/no-renderizados (identificadores, imports,
comentarios, dev-logs no surfaceados, fixtures) y la allowlist (licencia/provenance/env HERMES_* shim) quedan
FUERA. Ya no persigues cada hit del grep.

Que hacer:
1. Rebrandea a Zeus la superficie renderizada (lista de superficies en DECISION-0082 punto 1). De lo que el Analista
   cito, traza cada archivo: `early-access.tsx` / `hermes-world-landing.tsx` casi seguro renderizan -> Zeus; en
   `claude-agent.ts` / `gateway-capabilities.ts` / `mcp/*.ts` / `swarm-dispatch.ts` decide por si el string LLEGA a
   una superficie del punto 1 (error/help mostrado -> Zeus; log interno no surfaceado -> allowlist etiquetada).
2. Regenera el bundle desde el src limpio.
3. Entrega la ALLOWLIST ETIQUETADA (etiqueta + por-que-no-se-renderiza por cada hit restante). El Analista declara
   CERRABLE si ningun hit renderizado quedo sin Zeus y ninguna etiqueta es falsa.

Sin regresion (shim, npm test, no-rename, NOTICE MIT). Reentrega a in_review. maker != checker.
