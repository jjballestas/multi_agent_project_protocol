# Veredicto Analista - medicion H1-H3

Firma: Analista
Fecha UTC: 2026-06-30
Decision de cierre: GO / CERRABLE para el informe H1-H3.

## Ancla canonica

- Protocolo bajo instruccion REVIEW: `333e1693879fce9dc592c53f2cf55736f672abd3`.
- Corpus sellado: tag `TFM-dataset-N500` -> `e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9`.
- Hash `protocol.config.json` del corpus: `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`.
- Producto: la instruccion no cita commit de producto; por gate general ejecute clon limpio de `D:/Agentes/Zeus/Zeus-protocol` en HEAD `b2b2395da39090109db6de2dc50726dbaab1a11e`.

## Reproduccion

| Gate | Evidencia | Exit |
|---|---:|---:|
| `h1_detection.py --k 50` sobre corpus extraido del tag | 450/450 detectados | 0 |
| `h1_fpr_ac2.py` sobre corpus extraido del tag | FPR 0/500; AC2 500/500 | 0 |
| `h2_overhead.py --repeats 5` | mediana 1.5186 ms; p95 3.2708 ms; store 0.42254 KB/ev; tokens 0.0% | 0 |
| `h3_external_verify.py` con clean clone sin secretos | acuerdo 1.0; hash `dd2fd60eef525589f0ed8f1d581f45bfed584ab3ba2b3dc6c5624fbbbcc10ff0` match | 0 |
| `npm test` en clon limpio de producto | 109 tests; 87 pass; 22 skipped; 0 fail | 0 |
| `python scripts/validate_collaboration_state.py` | canonico valido | 0 |
| `python scripts/validate_collaboration_state.py --root <clean secretless clone>` | canonico valido sin secretos | 0 |
| `python scripts/scan_domain_neutrality.py` | limpio | 0 |
| `python scripts/scan_encoding.py` | limpio | 0 |
| `protocol_state_drift(Path('.'))` | `has_drift=false`, `up_to_seq=2729` antes de claim de review | 0 |

Nota de reproduccion: en Windows no use pipe binario `git archive | tar` ni `git show > file` de PowerShell porque altera/corrompe bytes; use `git archive -o` y extraccion local para conservar el hash byte-identico.

## Vectores

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| H1 A1 integridad/encadenado | PASA | 4 subtipos x 50 = 200 inyectados; 200 detectados; detector real `validate_chain`; evasiones `[]`. |
| H1 A2 no-repudio Ed25519 | PASA | 4 subtipos x 50 = 200 inyectados; 200 detectados; detector real `verify_actor_auth`; evasiones `[]`. |
| H1 A3 rollback/ancla | PASA con residual declarado | 1 subtipo x 50 = 50 inyectados; 50 detectados; detector `verify_anchor_monotonicity` + `validate_chain`; no hay eventos `chain.anchor` en el corpus, asi que el caso medido se reduce al ancla efectiva por genesis/chain hash. |
| H1 FPR | PASA | 0 falsos rechazos sobre 500 elegibles. |
| H1 AC2 | PASA | 500/500 actor_auth Ed25519 verificables = 100%, umbral >=99%. |
| H2 latencia | PASA | Delta mediana 1.5186 ms <=50; p95 3.2708 ms <=200. |
| H2 almacenamiento | PASA | Delta medio 0.42254 KB/evento <=4 KB/evento. |
| H2 tokens | PASA con residual declarado | 0.0% por construccion: #4 firma hashes y no texto; `runtime/state/events.jsonl` no esta en `coldstart_globs`. No es medicion empirica de tokens reales. |
| H3 acuerdo externo | PASA | 500/500 eventos comparados; acuerdo 1.0; discrepancias `[]`. |
| H3 hash clean clone | PASA | Interno y externo: `dd2fd60eef525589f0ed8f1d581f45bfed584ab3ba2b3dc6c5624fbbbcc10ff0`. |
| H3 public-only Ed25519 | PASA | 500/500 firmas verifican con publicas; HMAC sin secretos queda `unresolved_key`/`missing_key`, no tamper. |
| Informe HTML autocontenido | PASA | 0 `<script`; 0 `http://`; 0 `https://`; 0 `src=`; 0 `href=`. |
| Honestidad de limitaciones | PASA | El informe declara A2/A3 independencia debil y que tokens 0% es estructural/by-design, no empirico. |

## Residuales

- A3 no prueba una red externa ni una autoridad de anclaje independiente; el corpus tiene `chain.genesis` y `protocol.genesis`, pero 0 eventos `chain.anchor`. El informe lo trata como limitacion de independencia debil, no como garantia fuerte.
- H2 tokens queda demostrado estructuralmente, no por telemetria de uso real. Esta declarado de forma suficiente y no bloquea.
- El gate de producto se ejecuto porque la orden general lo exige, pero la REVIEW de medicion no cita commit de producto especifico; use HEAD local canonico del producto al momento de la pasada.

## Recomendacion

OK -> CERRABLE. No encontre escape nuevo ni maquillaje material contra los umbrales s.5. El informe puede promoverse como informe final si el Arquitecto conserva las limitaciones anteriores sin endurecer el lenguaje.
