---
name: mailbox-hygiene
description: >-
  Como todos los agentes (Arquitecto/Codex/Analista) mantienen limpio el canal Area_comun/mailbox:
  escribir mensajes bien formados, NO dejar mensajes resueltos en open/, y archivar los consumidos de
  forma gobernada. USAR al: escribir un GO/REVIEW/FYI/HANDOFF, cerrar una tarea, responder un mensaje,
  o cuando open/ acumula mensajes ya respondidos/entregados/superados. Reglas duras: ASCII puro;
  requires_response exige response_owner; claim de mailbox SOLO file-scoped a MSG-*.md (nunca dir-level);
  archivar (mailbox_archive) exige capability orchestrator (solo el Arquitecto); los peers senalan
  mensajes stale via DECISION-0018, no los tocan. Complementa arquitecto-ledger-ops y arquitecto-cron-lifecycle.
  Trigger words: mailbox, higienizar, higiene, archivar, mailbox_archive, MSG, open, archived, mensaje
  resuelto, consumido, stale, huerfano, response_owner, ASCII, canal limpio, GO consumido.
---

# Mailbox hygiene -- canal limpio para todos los agentes

> Objetivo: en `Area_comun/mailbox/open/` SOLO viven mensajes **vivos y accionables**. Todo lo respondido,
> consumido o superado se **archiva** (open -> archived). Un `open/` lleno de mensajes muertos confunde el
> cold-start, re-dispara crons y esconde lo accionable. Minimal narration (DECISION-0038): no narres el proceso.

## 0. Quien puede que
- **Todos los agentes:** escriben mensajes bien formados y **gatean** su propio mensaje antes de soltarlo.
- **Solo el Arquitecto (capability `orchestrator`):** ejecuta `mailbox_archive` (mover open->archived).
  Codex/Analista **no pueden archivar** (submit_intent lo rechaza: "lacks required capability: orchestrator").
- **Los peers (Codex/Analista):** si ven un mensaje stale/huerfano lo **senalan** al owner (DECISION-0018);
  no lo arreglan bajo claim ajeno ni lo dejan sin senalar.

## 1. Escribir un mensaje bien formado (antes de dejarlo en open/)
- **ASCII puro.** Nada de acentos ni simbolos tipograficos. Usa `->`, `>=`, `AND`, `-`.
  `scan_encoding.py` cubre `open/` Y `archived/`.
- **`requires_response: true` EXIGE `response_owner: <destinatario>`** + `requested_action` y/o `question`.
  Sin ellos, `validate_collaboration_state.py` sale exit 1.
- **`type` que el cron del peer reconoce:** Codex acepta `GO/REQUEST/ACTION/HANDOFF/REVIEW/QUESTION/DECISION`;
  **Analista acepta `REVIEW/REQUEST/ACTION/QUESTION/DECISION` (NO "GO")**. O pon `requested_action` no vacio.
- **FOOTGUN stop-order:** no combines un verbo de corte `(detener|deten|parar|para|stop|standdown|stand-down)`
  con `(cron|monitor|monitoreo|<peer>)` en una misma linea: el cron del peer se auto-detiene. Evita "para".
- **GATEA tu propio mensaje:** `python scripts/validate_collaboration_state.py` exit 0 **Y**
  `python scripts/scan_encoding.py` exit 0, antes de seguir.

## 2. Claims sobre mailbox (DECISION-0020)
- **SOLO file-scoped a archivos MSG-*.md concretos. NUNCA dir-level** (`Area_comun/mailbox/open` a secas
  bloquea el canal entero y al peer). `submit_intent` lo rechaza: "mailbox claim must be file-scoped".
- No listes en el `scope` un MSG que aun no existe (artifacts-before-claim, #1).

## 3. Cuando archivar (triggers de higiene)
Archiva un MSG de `open/` cuando quede **resuelto**:
- **Respondido:** su respuesta ya existe (el `response_owner` contesto).
- **GO/ACTION consumido:** la tarea que ordenaba ya se entrego (existe su commit `deliver`).
- **REVIEW resuelto:** el veredicto (GO/NO-GO) ya se emitio y se actuo.
- **FYI/HANDOFF informativo:** ya leido, sin accion pendiente.
- **Superado:** una ronda/mensaje mas nuevo lo reemplaza (p.ej. remediation-2 supera la entrega original).
Manten en `open/` solo lo **accionable o en espera de respuesta**. Escribe la asercion (el "archivado") solo
**despues** de que el ledger lo respalde (DECISION-0020 #6).

## 4. Como archivar (SOLO Arquitecto; via submit_intent)
`mailbox_archive` es una transaccion gobernada (escritor unico). Receta:
1. **Claim file-scoped** que cubra las DOS rutas del MSG + su propia fila para liberarse:
   - `Area_comun/mailbox/open/<MSG>.md`, `Area_comun/mailbox/archived/<MSG>.md`, y `CLAIMS.json#<claim_id>`.
2. `submit_intent` con la intent:
   `{"type":"mailbox_archive","message_id":"<MSG-... id seguro, sin / \\ ..>"}`
   (mas los campos de accountability que exige el payload).
   `--actor-id Arquitecto --timestamp <ISO> --commit $(git rev-parse HEAD)`.
3. Efecto: el archivo se mueve `open -> archived` (transicion registrada en el ledger).
4. **Lote:** varios MSG resueltos en un solo `submit_intent --intents {"intents":[...]}` (uno por MSG).
Ver la receta base y los gotchas en `arquitecto-ledger-ops`.

## 5. Peers: detectar y senalar (DECISION-0018), no tocar
Si Codex/Analista ven un mensaje stale (respondido pero sigue en open/), un estado que contradice el mailbox,
o un claim huerfano sobre un MSG: **notifican al Arquitecto** con un MSG accionable y lo registran. **No**
dir-claiman el mailbox, **no** archivan (no tienen orchestrator), **no** arreglan en silencio bajo claim ajeno.

## 6. Post-archivo (cierre limpio)
- `scan_encoding.py` (cubre open+archived) + `validate_collaboration_state.py` exit 0; **drift 0**.
- Commit con **stage explicito por path** (nunca `git add -A`); push si verde.
- Actualiza memoria (DECISION-0026). Los mensajes de FYI de cierre van **despues** del archivado, no antes.

## Checklist de una linea
Escribo: ASCII? response_owner? type valido para el peer? sin corte+peer? gateado exit 0? ·
Archivo (solo Arq): mensaje resuelto? claim file-scoped open+archived+#self? message_id seguro? orchestrator? ·
Peer: stale? -> senalo al owner (DECISION-0018), no toco.
