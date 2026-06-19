# ANALISTA - TASK-0128 (front etapa 4, vista de atestacion #4) - segunda voz independiente del cierre

> Voz: Analista (checker independiente). Firma: Analista. Fecha: 2026-06-20.
> Encargo del operador: segunda voz independiente sobre el cierre que hizo Codex (maker) de la etapa 4;
> mis dos notas (honestidad de estado + guarda PII) eran los criterios de aceptacion.
> maker != checker: reproduje en CLON LIMPIO, gateando por EXIT CODE, sin leer el detalle del maker antes
> de correr el codigo. Read-only, no muto estado, no consolido, no decido. TASK-0128 ya estaba `done`;
> esto es corroboracion post-cierre, no reapertura.

## Veredicto: CONCURRO con el cierre (done). Los 2 criterios de aceptacion estan REALMENTE en el codigo.

Reproduccion: clon limpio de Zeus-protocol en `C:/tmp/analista-0128/zeus`, checkout `4d9f1b3`, arbol limpio
(0 cambios). Node v24.15 / npm 11.12.

## Criterio 1 - Honestidad de estado (badges DERIVADOS de la verificacion real, no verde estatico): PASA

Verificado leyendo el cableado real, no solo el test:
- **server.js `loadRuntimeVerification`** llama a los MISMOS runtime del protocolo via `python -c`:
  `validate_chain`, `validate_agent_signatures`, `verify_anchor_monotonicity`, `verify_event_auth`
  (per-evento, ultimos 24) y `protocol_state_drift`. El payload del badge sale de esas llamadas, NO de un
  literal.
- **Fail-closed (Promise.allSettled):** si la llamada falla -> drift `{has_drift:true}`, atestacion
  `{error}` (sin verde), fuente `indeterminate`. No verde por defecto.
- **app.js render derivado:** chequeos `=== true` estrictos; `attested = validatorOk && driftOk && chainOk
  && agentSignaturesOk && anchorOk && eventAuthOk` (verde SOLO si TODO verifica); `working_tree`/
  `indeterminate` -> badge `warn` (no verde); firma por-evento en 3 estados reales
  (ok / danger=invalida / warn=indeterminada con su `reason`).
- **Fuente de estado honesta:** `loadSourceState` deriva `canonical` vs `working_tree` de `git status`;
  fallo -> `indeterminate`. El smoke del maker rendea `working_tree` cuando el checkout esta sucio.

## Criterio 2 - Guarda de PII (DECISION-0040): PASA (estructural, no heuristica)

- **canonicalReader.js:260:** `payloadPreview: Object.keys(payload).length ? "[redacted - PII de tercero]" : ""`.
  El preview del payload se redacta SIEMPRE; no es "redacta si parece PII" -> estructuralmente no puede
  filtrar PII de tercero por esa via. Mas fuerte que el mockup (que redactaba selectivo).
- Tests lo aseveran (canonicalReader.test.js:75, staticContract.test.js:50).

## Read-only / no-bypass: PASA

- Unica via de escritura = `POST /api/protocol/actions/submit` con `confirm:"SUBMIT_INTENT"` (409 si falta)
  -> `runtime/submit_intent.py`. Etapa 4 NO anadio ruta de escritura. El test negativo no-bypass pasa.

## Gates reproducidos por mi (EXIT CODE)

Producto (clon limpio Zeus-protocol @ 4d9f1b3):
- `node --check` server.js / canonicalReader.js / app.js -> OK.
- `npm test` (node --test) -> **11/11, exit 0** (incl. "attestation view derives badges from runtime
  verification and redacts payload text").

Protocolo (canonico, origin == HEAD `81e99c2`):
- `validate_collaboration_state.py --root .` -> **exit 0**.
- `scan_encoding.py` -> **exit 0**. `scan_domain_neutrality.py` -> **exit 0**.
- `protocol_state_drift` -> `has_drift=False`, `up_to_seq=764`.
- TASK-0128 `done`; handoff autocontenido; design system citado por hash (`a445d59`).

## Notas honestas (no bloquean el cierre)

1. **El staticContract test es ESTRUCTURAL (string-match):** asevera que el codigo CONTIENE
   `validate_chain`/`signature verified`/`[redacted...]`, etc. Por si solo no atraparia codigo muerto. Lo
   cierro yo leyendo el cableado real (server.js/app.js genuinamente conectados). Sugerencia de
   fortalecimiento (opcional, futuro, NO condicion de cierre): un test de COMPORTAMIENTO que mockee una
   llamada-runtime que falla y asevere que el badge rendea NO-verde -> hace la propiedad de honestidad
   regresion-proof en vez de depender de la presencia del string.
2. **"Sin secretos -> indeterminado" lo verifique por CAMINO DE CODIGO** (allSettled + mapeo a
   indeterminate + per-evento `valid/reason`, consistente con DECISION-0046 unverifiable). NO ejecute el
   server vivo contra un protocolo con secretos ocultos; el maker reporto ese smoke verde. Residual
   declarado: camino verificado, corrida-viva-sin-secretos no reproducida por mi. Si el operador la quiere,
   corro el smoke del server con secretos ocultos.

## Que NO hice
- No reabri TASK-0128 (ya `done`); no muto estado, no promuevo, no consolido.
- No lei el HANDOFF del maker como sustituto de correr el codigo (lo corri yo en clon limpio).
- No toque #4/config (epoca 1.14.0 pinned).
