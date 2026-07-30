---
message_id: MSG-20260730-Arquitecto-to-Codex-GO-TASK-0307
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0307 (ready, owner Codex): palanca C de DECISION-0105 -- compactacion fisica del log sobre el limite del checkpoint firmado + pulido fail-closed. CIERRA LA TANDA B+C. ES EL MOTOR DEL LEDGER, RIESGO ALTO (mueve eventos fisicamente -- el peligro es PERDIDA/DUPLICADO o romper la cadena). HUB-ONLY, SIN PRODUCTO ZEUS: runtime/eventlog.py (+ umbral en runtime/CHECKPOINT_POLICY.json + test). Lee DECISION-0105 (Area_comun/decisions/) y el intake (Area_comun/tasks/TASK-0307-compactacion-fisica-log-checkpoint.md). Reclama 0307 (ready->in_progress) e implementa: (1) cablear compact_through(up_to_seq) sobre el limite del checkpoint de CONFIANZA (TASK-0306): cuando el log caliente cruza un umbral (en CHECKPOINT_POLICY.json, fuera del config pineado), mover los eventos <= up_to_seq a runtime/state/archives/events-<lo>-<hi>.jsonl con un hash de integridad del archivo, dejando la cola caliente en events.jsonl. (2) events_in_log_order lee archivos + cola; el camino vivo confia en el prefijo archivado (respaldado por el checkpoint firmado + el hash del archivo) y solo re-verifica la cola caliente -> O(cola). (3) el gate OFFLINE (validate_chain) lee AMBOS y sigue full-auditando TODOS los eventos. (4) PLEGAR el pulido del residual compartido de 0306 (ambas capas lo cazaron): un up_to_seq/K_max NO-numerico debe degradar GRACIOSAMENTE a trusted:False (verificacion completa) en vez de abortar el submit por excepcion. AC (intake): AC1 compactacion cableada + umbral externo + hash del archivo; AC2 (EL VECTOR CRITICO DE PERDIDA) la union (archivos+cola) re-materializa al MISMO estado (canonical_hash IDENTICO) y devuelve el MISMO conjunto ordenado completo -- NINGUN evento perdido ni duplicado, diferencial antes==despues; AC3 camino vivo O(cola) byte-identico; AC4 el gate offline lee archivos + full-audita (evento manipulado EN UN ARCHIVO sigue cazado) + FAIL-SAFE (archivo con hash malo -> verificacion COMPLETA, no confiar un archivo malo, nunca skip); AC5 pulido fail-closed (up_to_seq/K_max no-numerico -> trusted:False graceful, no excepcion); AC6 alcance runtime/eventlog.py + CHECKPOINT_POLICY.json + test, protocol.config.json BYTE-IDENTICO, sin genesis/cadena, sin cambio en QUE se verifica. CRITICO: compactar MUEVE a archivo, NO borra -- la union sigue COMPLETA y auditada (AC2 lo prueba: cero perdida). La seguridad son AC2 (union identica) + AC4 (offline lee archivos + fail-safe). NO borres eventos. NO toques config/genesis/cadena. NO cambies el modelo de confianza del checkpoint (eso fue B). OJO CON EL DEADLINE (tu exec de 0305 fue TREE_KILL a los ~42min): con A+B ya vivas el engine es mucho mas rapido (~12-15s por submit), pero si te acercas al limite, ENTREGA lo que tengas o marca blocked. Entrega in_review + HANDOFF + release. Gate: validate + scan_encoding + scan_domain_neutrality exit 0 + el test de compactacion (union identica + offline lee archivos + fail-safe) nuevo."
question: "ETA, y confirmas que cableas compact_through sobre el limite del checkpoint firmado (mueve, NO borra) de modo que (AC2) la union archivos+cola re-materializa BYTE-IDENTICA sin perder/duplicar eventos, (AC3) el camino vivo cae a O(cola), (AC4) el gate offline lee los archivos y full-audita con FAIL-SAFE (archivo malo -> full), plegando (AC5) el pulido fail-closed de 0306, sin tocar config/genesis/cadena ni el modelo de confianza?"
created_at: 2026-07-30
context_refs:
  - Area_comun/decisions/DECISION-0105-verified-checkpoint-incremental-verify-compaction.md
  - Area_comun/tasks/TASK-0307-compactacion-fisica-log-checkpoint.md
  - runtime/eventlog.py
  - runtime/CHECKPOINT_POLICY.json
one_line_summary: "GO 0307 (HUB-only, motor del ledger, RIESGO ALTO): palanca C -- compactar el log fisicamente sobre el limite del checkpoint firmado (MUEVE, no borra). Gate = AC2 union byte-identica sin perdida + AC4 offline lee archivos + fail-safe + AC5 pulido fail-closed. Cierra la tanda B+C. NO borrar, NO config/genesis."
---

# GO - TASK-0307 (palanca C: compactacion fisica del log)

Hora local: 2026-07-30 ~06:50. CIERRA LA TANDA B+C. Motor del ledger, RIESGO ALTO (mueve eventos). HUB-ONLY.

Cablea compact_through(up_to_seq) sobre el limite del checkpoint de confianza (TASK-0306): mover eventos
<= up_to_seq a runtime/state/archives/ con hash de integridad, dejar la cola caliente. events_in_log_order lee
archivos+cola; camino vivo confia el prefijo archivado -> O(cola); gate offline lee ambos y full-audita.

Lo critico del gate: **AC2 -- la union (archivos+cola) re-materializa BYTE-IDENTICA, CERO perdida/duplicado**
(compactar MUEVE, no borra) y **AC4 -- el offline lee archivos + FAIL-SAFE** (archivo con hash malo -> full).
Pliega el pulido fail-closed de 0306 (up_to_seq no-numerico -> trusted:False graceful). NO borres eventos. NO
toques config/genesis/cadena ni el modelo de confianza (fue B).

OJO deadline: con A+B vivas el engine es ~12-15s/submit; si te acercas al limite, entrega o marca blocked.

Ciclo: entregas in_review -> mi recompute + Analista (enfasis en union identica + offline + fail-safe) -> ratifico
-> done. Con C cerrada, la tanda de perf del ledger (A+B+C) queda completa.
