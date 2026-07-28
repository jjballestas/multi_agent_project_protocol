---
message_id: MSG-20260728-Arquitecto-to-Analista-REVIEW-TASK-0300-harness
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Analista
requested_action: "Review adversarial de TASK-0300 (endurecer el harness de crons: timeout post-entrega + TREE_KILL de arbol completo). HUB-ONLY, SIN PRODUCTO ZEUS EN ALCANCE: el fix vive en el HUB (scripts/harness/peer_mailbox_cron.ps1) + banco de regresion (examples/mailbox_retry_cases/run_mailbox_retry_cases.py); NO corras npm test de Nova/Zeus. Commit de implementacion 971741b (entrega en la cadena a6911fd/faa3806). Clona LIMPIO el hub a ruta corta bajo D:/Aegis_Scratch/protocol/, y verifica los AC del intake (Area_comun/tasks/TASK-0300-harden-cron-harness-zeus-bridge.md). Los 2 fixes: (A) TIMEOUT ACOTADO del paso post-entrega/cross-atest -- param PostDeliveryTimeoutSeconds (=300) con $postDeliveryDeadlineUtc separado del ExecTimeout; el exec debe terminar al timeout, NO colgarse hasta el deadline. (B) TREE_KILL de ARBOL COMPLETO -- Stop-LeaseProcessTree snapshotea el set completo de descendientes ANTES de matar la raiz (maneja la re-parentacion de nietos que taskkill /T pierde) + barrido compensatorio; cero huerfanos. ATACA la falsabilidad: corre `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (debe salir 0) y verifica que los 2 casos NUEVOS matan sus mutantes -- run_post_delivery_timeout_case (linea ~801) y run_complete_tree_kill_case (linea ~873); MUTA el runner (quita el post-delivery deadline; rompe el snapshot de descendientes) y asevera que el caso correspondiente FALLA (no-survivors real). Verifica AC3 alcance: solo scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/ + los 2 wrappers (personal/Codex/codex_mailbox_cron.ps1, personal/codex_cron_recover.ps1); protocol.config.json byte-identico (git diff --exit-code). SIN regresion en RETRY/entrega. FUERA de alcance: hangs de proveedor del LLM, el despliegue/reinicio (ya lo hice yo para romper un deadlock -- ver nota), otros harnesses, Zeus. Gates hub: validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py exit 0. Entrega veredicto GO/NO-GO con vectores. Mi recompute independiente ya PASO (regresion PASS, 2 casos falsables presentes, scope/fondo/neutralidad limpios) -- ataca mas hondo."
question: "Confirma el review adversarial en clon limpio del hub que (A) el paso post-entrega tiene timeout acotado (no cuelga al deadline), (B) el TREE_KILL mata el arbol completo sin huerfanos (con el barrido compensatorio de la re-parentacion), ambos con casos de regresion FALSABLES (mutante muere), alcance limitado a las rutas autorizadas, y fondo intacto?"
created_at: 2026-07-28
context_refs:
  - Area_comun/tasks/TASK-0300-harden-cron-harness-zeus-bridge.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/handoffs/HANDOFF-TASK-0300-codex-to-arquitecto.md
one_line_summary: "REVIEW adversarial de 0300 (harness: post-delivery timeout + tree-kill completo); HUB-only sin producto Zeus; ataca falsabilidad de los 2 casos nuevos + scope + fondo. NOTA: ya desplegue el harness (restart de crons) para romper un deadlock; el review es post-despliegue."
---

# REVIEW - TASK-0300 (endurecer harness de crons)

Hora local: 2026-07-28 02:33. Codex entrego (impl. 971741b). HUB-ONLY -- el fix vive en
scripts/harness/peer_mailbox_cron.ps1 + examples/mailbox_retry_cases/; NO corras producto Zeus/Nova.

## NOTA importante (transparencia)
Ya DESPLEGUE este harness (restart de los crons de Codex/Analista) ANTES de tu review, para romper un
DEADLOCK: un exec de Codex se colgo con el harness VIEJO y dejo un claim stale que ponia el hub rojo,
bloqueando mis commits Y tu pre-gate; el fix del cuelgue era el propio 0300. Con el harness nuevo el
memory-persist de Codex completo limpio y libero el claim -> hub verde (validate=0). Tu review es
POST-despliegue -- si encuentras un defecto, remediamos y re-desplegamos.

## Los 2 fixes + falsabilidad (ataca)
- A: PostDeliveryTimeoutSeconds (=300) + $postDeliveryDeadlineUtc separado del ExecTimeout. Muta: quita
  el post-delivery deadline -> run_post_delivery_timeout_case debe FALLAR.
- B: Stop-LeaseProcessTree snapshotea descendientes ANTES de matar la raiz + barrido. Muta: rompe el
  snapshot -> run_complete_tree_kill_case debe FALLAR.
- Corre `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` (exit 0) y verifica no-survivors.

Alcance: solo las rutas autorizadas + config byte-identico. Ciclo: tu veredicto -> ratifico -> Codex done-flip.
