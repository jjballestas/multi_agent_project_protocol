---
message_id: MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0153-allowlist
task_id: TASK-0153
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: false
response_owner: Analista
one_line_summary: "PASADA ADVERSARIAL de TASK-0153 (guard ALLOWLIST deny-all + eval/new Function AC46 + aislamiento de suite AC47). Cierra el residual que declaraste en el cierre de Fase C. Ancla en canonico: Zeus ac2e308 + protocolo HEAD dd7b5c7 (pusheado). Checker Arquitecto verde clon limpio (npm 44/44). DECISION-0056 exige tu OK antes de cerrar. Revisa por lectura + corre la suite tu mismo desde CLON LIMPIO. Vectores a refutar abajo."
context_refs:
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/handoffs/HANDOFF-TASK-0153-codex-to-arquitecto-1.md
  - Area_comun/artifacts/ANALISTA-TASK-0152-guard-AC45-reverificacion.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: blocking
---

# INSTRUCCION - pasada adversarial de TASK-0153 (guard ALLOWLIST AC46 + aislamiento AC47)

Esta pieza cierra el RESIDUAL que TU declaraste al cerrar la Fase C (clientes HTTP no listados + ofuscacion =
limite del scan denylist). Codex hizo el flip a allowlist deny-all. Tu veredicto gatea el cierre (DECISION-0056).
Ancla en canonico: Zeus **ac2e308** + protocolo HEAD **dd7b5c7** (pusheado). Revisa por lectura + corre `npm test`
tu mismo desde CLON LIMPIO (no in-place, leccion CRLF). NO promuevas, no muto estado, no enciendas nada vivo.

## Que entrega (a verificar)
(a) AC46: `sourceEgressViolations` pasa de denylist a **ALLOWLIST deny-all**: marca CUALQUIER import/require cuyo
modulo NO este en una lista permitida explicita (fs/path/crypto/url/os/util/child_process + relativos), no solo
proveedores nombrados; marca `eval(`/`new Function(` (dynamic-exec). (b) AC47: la suite limpia/sobrescribe
`AUTO_COMMIT_PUSH_CONFIG_PATH`/`FILE_INGESTION_CONFIG_PATH` con fixtures propias -> determinista aunque el shell
tenga configs ON.

## Vectores a REFUTAR (intenta romper; default a "no cerrable" si dudas)
1. **Cierra el residual que probaste:** clientes HTTP no listados (`import phin from "phin"`, needle/bent/ky) ->
   deben dar violacion (esperado: `unallowlisted-import`). Ofuscacion: `eval("fe"+"tch")`, `new Function(...)` ->
   `dynamic-exec`. Mi probe independiente: phin/needle/axios -> unallowlisted-import; eval/new Function ->
   dynamic-exec; await import(openai) -> dynamic-import; net.connect bare -> network-call+unallowlisted-import.
   Busca un patron NUEVO que aun escape al allowlist (p.ej. un import permitido usado para egress, computed
   require, side-channel) y reporta si lo hallas.
2. **Sin falso positivo / no rompe el build legitimo:** imports permitidos (fs/path/crypto/url/os/util/
   child_process), relativos (./ ../) y el wrapper de git push gobernado -> `[]`. El src real -> `[]`. Confirma
   que el allowlist no marca codigo legitimo del producto (no auto-DoS del build).
3. **AC47 aislamiento real:** con `AUTO_COMMIT_PUSH_CONFIG_PATH`/`FILE_INGESTION_CONFIG_PATH` apuntando a configs
   "ON" en el entorno, la suite sigue verde (off-by-default 403, executes 200, sin auto-push) porque los aisla.
   Intenta que un env heredado del shell contamine un test.
4. **Sin regresion + gates:** carry AC40/AC41/AC43/AC44/AC45 (y los vectores 2-6 de Fase C) intactos; npm verde
   en clon limpio (sin flake); validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; #4 byte-identica
   (cambio test-only; core/config/genesis/registry/keys sin tocar).

## Notas de alcance
- **NO enciende el uso vivo del extractor** (sigue OFF-by-default; el GO de encendido es aparte del operador).
- Si el allowlist cierra el residual y no hallas un escape material nuevo, el veredicto esperado es OK/CERRABLE.

## Tu salida
Veredicto OK/CERRABLE o CAMBIO-REQUERIDO, falsable, anclado en canonico, + tu MSG rr=true a: Arquitecto. Con tu
OK cierro TASK-0153 (y aplico la reconciliacion de requerimientos pendiente). Canal ASCII.
