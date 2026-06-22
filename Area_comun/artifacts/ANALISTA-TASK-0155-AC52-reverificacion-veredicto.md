# ANALISTA - TASK-0155 AC52 re-verificacion

Firma: Analista
Fecha: 2026-06-22
Ancla producto: Zeus-protocol `6369b5ce688945fa416d22b885718e52dbe9a33b`
Ancla protocolo: `1cb2b40`
Instruccion revisada: `Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVERIFICAR-TASK-0155-AC52.md`

## Veredicto

OK/CERRABLE. El hueco decimal `2130706433` queda cerrado y la familia de notaciones ambiguas/no-loopback
que probe no pasa el guard. No encontre un host no-loopback aceptado por la canonicalizacion estricta.

## Reproduccion

| Gate | Resultado |
|---|---|
| Clon limpio producto, checkout `6369b5c` | PASA |
| `npm test` en clon limpio, corrida 1 | FAIL, exit 1 por `EACCES 127.0.0.1:5040` en test de auto commit push; no toca AC52 |
| `npm test` en clon limpio, corrida 2 | PASA, exit 0, 48/48 |
| Payloads propios contra guard extraido de `src/server.js` | PASA, exit 0 |
| `python scripts/validate_collaboration_state.py` con secretos | PASA, exit 0 |
| `python scripts/validate_collaboration_state.py` sin secretos en clon limpio | PASA, exit 0 |
| Drift #4 | PASA, `has_drift=false`, `up_to_seq=1197` |
| `python scripts/scan_domain_neutrality.py` | PASA, exit 0 |
| `python scripts/scan_encoding.py` | PASA, exit 0 |
| #4 byte-identica | PASA, sin diff en `runtime/state`, `protocol.config.json` ni `Area_comun/state/*.json` |

Nota: la primera corrida de `npm test` fallo por puerto local del test harness (`EACCES` en `127.0.0.1:5040`).
La segunda corrida en el mismo clon limpio paso completa. No lo gateo como AC52 porque el fallo no ejercita
`local-vlm` ni el guard de loopback, pero queda declarado como ruido de entorno reproducible por exit code.

## Vectores AC52

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| Decimal single-number `http://2130706433:11434/api/chat` | PASA | Rechazado por guard extraido; la suite tambien lo cubre en `tests/staticContract.test.js` |
| Octal `0177.0.0.1` | PASA | Rechazado |
| Hex `0x7f.0.0.1` y `0x7f000001` | PASA | Rechazados |
| Any-address `0.0.0.0` | PASA | Rechazado |
| Externo IPv4 `8.8.8.8` | PASA | Rechazado |
| Hostname externo `evil.com` | PASA | Rechazado |
| Sufijo `127.0.0.1.evil.com` | PASA | Rechazado |
| IPv4-mapped externo `[::ffff:8.8.8.8]` | PASA | Rechazado |
| Leading-zero `127.000.000.001`, `0127.0.0.1`, `127.0.0.01` | PASA | Rechazados |
| Userinfo confusion `127.0.0.1@evil.com` / `evil.com@127.0.0.1` | PASA | Rechazados por `extractRawUrlHost` devolviendo host vacio |
| Percent/sufijo `127.0.0.1%2eevil.com` | PASA | Rechazado |
| Octeto fuera de rango `127.0.0.256` y `128.0.0.1` | PASA | Rechazados |
| IPv4-mapped loopback `[::ffff:127.0.0.1]` | PASA | Rechazado; la politica positiva solo acepta `::1` literal |
| `https://127.0.0.1` | PASA | Rechazado por regla HTTPS solo `localhost` |
| Protocolo no HTTP `ftp://127.0.0.1` | PASA | Rechazado |

## Positivos AC52

| Vector | Resultado | Evidencia falsable |
|---|---|---|
| `http://localhost:11434/api/chat` | PASA | Aceptado |
| `https://localhost:11434/api/chat` | PASA | Aceptado |
| `http://127.0.0.1:11434/api/chat` | PASA | Aceptado |
| `http://127.0.0.5:11434/api/chat` | PASA | Aceptado |
| `http://127.255.255.255:11434/api/chat` | PASA | Aceptado |
| `http://[::1]:11434/api/chat` | PASA | Aceptado |

## Carry AC51/AC53

PASA por suite completa en clon limpio: `local-vlm extractor is loopback-only, chunked, robust, and non-ledger`
quedo verde en la corrida 48/48. No reabro AC51/AC53 porque la instruccion era re-verificar el rework AC52
y el carry queda cubierto por comportamiento en la suite.

## Residuales

- No bloqueo: AC52 valida sintaxis/canonicalizacion local, no es sandbox de red. El provider sigue dependiendo
  de que el endpoint configurado sea el VLM local esperado y de que el uso vivo tenga su GO/ceremonia separados.
- No bloqueo: `npm test` puede flaquear por puerto local ocupado o denegado en tests ajenos a AC52; reporte el
  primer exit 1 y gatee la segunda corrida exit 0.

## Recomendacion

CERRABLE para TASK-0155. No requiere cambio adicional antes del cierre.
