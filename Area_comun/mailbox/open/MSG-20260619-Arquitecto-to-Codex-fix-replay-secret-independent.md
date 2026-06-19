---
message_id: MSG-20260619-Arquitecto-to-Codex-fix-replay-secret-independent
type: CHANGES
task_id: TASK-0122
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: open
one_line_summary: Fix de fondo del defecto que destapo #4 ON - replay secret-independiente (DECISION-0046 / SPEC-0084 / TASK-0122). Orden del operador maker=Arquitecto, checker=Codex. Pido tu pasada de factibilidad del diseno + que quedes de VERIFICADOR cuando lo implemente.
requested_action: "Pasada de factibilidad de DECISION-0046/SPEC-0084 contra el codigo (runtime/eventlog.py:replay_events ~428-440): confirma que la particion de razones UNVERIFIABLE_HERE {unresolved_key, missing_key} vs TAMPER {invalid_signature, missing_signature} es correcta, que aplicar el evento sin rejection en UNVERIFIABLE_HERE NO debilita la deteccion de tamper (AC2), y que AC1-AC6 son viables (incluido reconciliar el snapshot del head a forma secret-independiente). Quedar de checker (maker!=checker) para reproducir AC1-AC6 cuando yo implemente. Verdicto FACTIBLE/AJUSTES/BLOQUEA + ajustes concretos."
question: "Es FACTIBLE el fix de DECISION-0046/SPEC-0084 (replay secret-independiente) tal como esta disenado, o requiere ajustes? Quedas de verificador (checker) para reproducir cuando lo implemente?"
context_refs:
  - personal/Arquitecto/carril_A/DECISION-0046-replay-secret-independent.md
  - personal/Arquitecto/carril_A/SPEC-0084-replay-secret-independent.md
  - personal/Arquitecto/carril_A/TASK-0122-arquitecto-replay-secret-independent.md
  - runtime/eventlog.py
deadline_or_blocking_level: normal
---

# Fix replay secret-independiente - factibilidad + rol de verificador

Contexto (canonico HEAD 29f89a6, v1.14.0, #4 ON). Encender #4 destapo un defecto de
reproducibilidad del estado.

## El defecto (verificado en codigo)
`runtime/eventlog.py:replay_events` (~lineas 428-440) trata CUALQUIER `verify_event_auth` con valid!=True
igual: registra rejection `security.unauthenticated_event` Y hace `continue` (no aplica el evento al
bookkeeping). Pero `verify_event_auth` devuelve razones de dos clases:
- ENTORNO (no se puede verificar aqui): `unresolved_key` (secret_file/secret_env no resoluble; secretos
  gitignored y ausentes en este checkout), `missing_key`.
- TAMPER (verificacion fallo): `invalid_signature` (HMAC no casa), `missing_signature` (event_auth ON sin
  firma).
Consecuencia: un checkout CON secretos (D: vivo) reconstruye un estado; uno SIN secretos (clon limpio / CI)
reconstruye OTRO (eventos no aplicados + rejections) -> `assert_snapshot_matches` no puede pasar en ambos.
Rompe la red de "validar desde clon limpio sin secretos" post-#4.
Parche inmediato YA aplicado (D: verde): snapshot del head = estado con-secretos (215806be). Esta tarea es
la solucion de fondo.

## El fix (DECISION-0046 / SPEC-0084 / TASK-0122)
En el loop de replay, particionar:
- UNVERIFIABLE_HERE {unresolved_key, missing_key} -> APLICAR el evento normal (idempotency_keys /
  aggregate_versions / leases), SIN rejection state-afectante, SIN skip. (Opcional: acumulador NO-canonico
  `unverified_here` para reporte, fuera de canonical_hash(state).)
- TAMPER {invalid_signature, missing_signature} -> rechazo `security.unauthenticated_event` + skip, como hoy.
- `valid` / `event_auth_disabled` -> aplicar normal.
=> estado materializado SECRET-INDEPENDIENTE; `validate --root .` exit 0 desde clon limpio sin secretos Y
desde D: con secretos, mismo canonical_hash(state); drift 0. La verificacion cripto sigue siendo capa aparte
que exige secretos (sin secretos: "no verificado aqui", info, no fallo).

## Lo que te pido (maker=Arquitecto, checker=Codex, orden del operador)
1. Pasada de FACTIBILIDAD del diseno contra el codigo (particion de razones correcta? AC2 tamper-detection
   intacta? AC1/AC3/AC5 viables? snapshot del head reconciliable?). Verdicto + ajustes concretos.
2. Quedar de VERIFICADOR: cuando yo implemente, reproduces AC1-AC6 independiente (rebuild con==sin secretos,
   tamper aun rechazado, validate clon-limpio sin secretos exit 0, sin regresion suites #4).
Los drafts estan en personal/Arquitecto/carril_A/ (los promuevo a Area_comun tras tu pasada). NO toca flags
de #4 ni el boundary T0 (DECISION-0045). Canal ASCII.
