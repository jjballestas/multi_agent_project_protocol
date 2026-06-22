# ANALISTA TASK-0153 exec-import - veredicto

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica revisada:
- Producto Zeus-protocol: `8751051581173d88ab2aa6aaa3a99b35ee89bd5f` (`8751051 test(intake): flag child process exec imports`).
- Protocolo: `b5c7e7a294177e2e164fd7ea64ed0d286992ffa8` (`origin/main` igual a HEAD al inicio de la pasada).
- Instruccion: `Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVERIFICAR-TASK-0153-exec-import.md`.

El residual bloqueante que declare en la pasada anterior queda cerrado: imports nombrados o requires
desestructurados de `exec` / `execSync` desde `child_process` / `node:child_process` ahora se marcan como
`cli-exec-import`, sin marcar el token bare `exec(` ni los usos reales de `RegExp.exec`.

## Reproduccion

| Gate | Evidencia | Exit |
|---|---:|---:|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 8751051` | clon limpio en `C:/Users/johnb/AppData/Local/Temp/zeus-task0153-e841ab7fb8164c2ea9f6ef3dadb31b72` | 0 |
| `npm test` en clon limpio del producto | 44 tests, 44 pass, 0 fail | 0 |
| payloads propios contra el guard `sourceEgressViolations` de `tests/staticContract.test.js` | 10/10 checks PASS | 0 |
| `python scripts/validate_collaboration_state.py` con secretos locales | `OK: collaboration state is valid.` | 0 |
| `python scripts/validate_collaboration_state.py --root <clon-sin-secretos>` | `OK: collaboration state is valid.` | 0 |
| drift canonico | `has_drift=false`, `hot_hash == replay_hash`, `up_to_seq=1164` | 0 |
| `python scripts/scan_domain_neutrality.py` | sin hallazgos | 0 |
| `python scripts/scan_encoding.py` | `OK: encoding scan is clean.` | 0 |
| #4 byte-identica antes del veredicto | hashes de `protocol.config.json`, `chain_manifest.json`, `runtime/state/events.jsonl`, `runtime/state/snapshot.json`, `runtime/state/snapshots/*` registrados; no tocados por el cambio de producto | 0 |

## Prueba adversarial por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| `import { exec } from "node:child_process"` | PASA | Payload propio devuelve `cli-exec-import`. |
| `const { execSync } = require("child_process")` | PASA | Payload propio devuelve `cli-exec-import` y, adicionalmente, `unallowlisted-import` para el specifier legacy. |
| `import { exec, execSync } from "child_process"` | PASA | Payload propio devuelve `cli-exec-import` y `unallowlisted-import`. |
| `const { exec: run } = require("node:child_process")` | PASA | Payload propio devuelve `cli-exec-import`. |
| `import { execFile, spawn } from "node:child_process"` | PASA | Payload propio devuelve `[]`. |
| `RegExp.exec` / `/re/.exec(x)` | PASA | Payload propio devuelve `[]`; el guard no marca `exec(` bare. |
| `canonicalReader.js` / src real | PASA | `sourceEgressViolations(collect(src))` devuelve `[]`. |
| `spawn("C:/Windows/.../powershell.exe", ...)` | PASA | Payload propio devuelve `external-cli` con binary absoluto. |
| `eval` / `new Function` | PASA | Payload propio devuelve `dynamic-exec`. |
| cliente HTTP no allowlisted (`needle`) | PASA | Payload propio devuelve `unallowlisted-import`. |
| Carry Fase A/B/C, AC46, AC47, auto commit, mailbox archive, PII gate, atestacion | PASA | `npm test` completo en clon limpio: 44/44. |

## Slips buscados

No encontre escape nuevo dentro del alcance pedido. El fix evita el falso positivo que un patron bare
`\bexec\(` habria introducido sobre `RegExp.exec`, y cubre las formas named import / destructuring require que
permitian usar `exec` / `execSync` como transporte hacia shell.

## Residuales declarados

No bloqueantes:
- `python -c` y `git ext::` siguen siendo gadgets inherentes de binarios allowlisted (`python`, `git`).
- El scan sigue siendo estatico; no equivale a sandbox ni a prueba general de cero egress frente a computacion
  ofuscada.

Esos residuales ya pertenecen a la precondicion del uso vivo: el gate real para esa ventana debe seguir siendo
extractor deterministic-local / cero egress efectivo, no una sobreafirmacion del scan.

## Recomendacion de cierre

OK -> CERRABLE para TASK-0153. No pido otro ciclo de Codex.
