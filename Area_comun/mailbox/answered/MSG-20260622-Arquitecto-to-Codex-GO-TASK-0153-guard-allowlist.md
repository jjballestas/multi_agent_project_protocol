---
message_id: MSG-20260622-Arquitecto-to-Codex-GO-TASK-0153-guard-allowlist
task_id: TASK-0153
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0153 (ready): flip del guard de egress a ALLOWLIST deny-all + marcar eval/new Function (AC46) + AISLAMIENTO de la suite del entorno de runtime del operador (AC47). Precondicion del uso vivo del extractor. NO enciende el uso vivo (sigue OFF-by-default). maker=Codex/checker=Arquitecto + pasada del Analista. Entrega in_review por clon limpio verde."
requested_action: "Reclama TASK-0153 (ready), implementala en Zeus-protocol y entregala in_review. (1) AC46: convierte sourceEgressViolations de DENYLIST a ALLOWLIST deny-all -- marca CUALQUIER import/require cuyo modulo NO este en una lista permitida explicita (fs/path/crypto/url/os/util + el wrapper de git gobernado), no solo proveedores nombrados; cierra clientes HTTP no listados (phin/needle/bent/ky/...). Marca tambien eval( y new Function(. Control positivo POR familia: cliente HTTP no listado -> FLAGGED; eval/new Function -> FLAGGED; import permitido (fs/path/...) -> []; git push gobernado -> []; src real -> []. (2) AC47: la suite limpia/sobrescribe al arrancar AUTO_COMMIT_PUSH_CONFIG_PATH y FILE_INGESTION_CONFIG_PATH (y cualquier env que altere off-by-default) con fixtures propias -> determinista aunque el shell tenga esos env ON (hoy dan 3 rojos falsos: off-by-default 200!=403, executes 502!=200). Manten verdes: npm clon limpio, #4 byte-identica, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0. NO enciendas el uso vivo."
context_refs:
  - Area_comun/tasks/TASK-0153-codex-guard-allowlist-test-isolation.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/decisions/DECISION-0056-file-ingestion-v2.md
  - Area_comun/artifacts/ANALISTA-TASK-0152-guard-AC45-reverificacion.md
  - D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js
deadline_or_blocking_level: normal
---

# GO - TASK-0153: guard ALLOWLIST (AC46) + aislamiento de suite (AC47)

El operador dio GO para cerrar el residual que el Analista declaro al cerrar la Fase C. **NO enciende el uso vivo
del extractor** (sigue OFF-by-default; el GO de encendido es aparte y posterior, con su Analista).

## Orden
1. **AC46 - ALLOWLIST deny-all + ejecucion dinamica.**
   - Convierte `sourceEgressViolations` de **denylist** (proveedores/clientes nombrados) a **ALLOWLIST deny-all**:
     marca CUALQUIER `import`/`require` cuyo modulo NO este en una **lista permitida explicita** (p.ej.
     fs/path/crypto/url/os/util + el wrapper de git gobernado). Esto cierra el residual (clientes HTTP no listados:
     phin/needle/bent/ky/...).
   - Marca tambien `eval(` y `new Function(` (ofuscacion / ejecucion dinamica).
   - Unico egress permitido = `git push` gobernado + lecturas read-only ya allowlisted.
   - **Control positivo POR familia**: cliente HTTP no listado (`import phin from "phin"`) -> FLAGGED;
     `eval(`/`new Function(` -> FLAGGED; import permitido (fs/path/...) -> `[]`; git push gobernado -> `[]`;
     el src real -> `[]` (sin falso positivo).
2. **AC47 - Aislamiento de la suite del entorno de runtime del operador.**
   - `npm test` limpia/sobrescribe al arrancar `AUTO_COMMIT_PUSH_CONFIG_PATH`, `FILE_INGESTION_CONFIG_PATH` (y
     cualquier env que altere off-by-default) con fixtures propias -> resultado determinista independiente del shell.
   - Test falsable: con esos env apuntando a configs "ON", la suite sigue verde (off-by-default 403, executes 200)
     porque los aisla.

## Gates de entrega (DoD)
- AC46 + AC47 verdes; carry AC40/AC41/AC43/AC44/AC45 intactos. Cambio acotado (guard/test + harness); core/config/
  genesis/registry/keys SIN tocar. node --test/CI verde EN CLON LIMPIO; #4 byte-identica; validate con/sin secretos
  exit 0; drift 0; neutralidad+encoding 0.
- Entrega **in_review** con handoff autocontenido. **maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA** al
  cierre. **NO enciendas el uso vivo** del extractor (OFF-by-default).

Canal ASCII.
