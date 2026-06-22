# ANALISTA - RE-VERIFICACION del guard AC45 (Fase C, TASK-0152) tras CAMBIO-REQUERIDO

> Voz: Analista (escepticismo externo). Firma: Analista. Fecha: 2026-06-22. Lente: seguridad / metodologia.
> ANCLADO EN CANONICO: clon limpio Zeus-protocol `3d94f11` (tree limpio); protocolo HEAD==origin `9f91dd4`.
> Verifique el CODIGO, PROBE EL GUARD POR COMPORTAMIENTO y corri la suite YO MISMO. NO promovi, NO mute
> estado, NO encendi nada vivo.

## VEREDICTO: OK -> CERRABLE la Fase C. Los 5 huecos que probe CIERRAN; sin regresion; gates verdes.
## 1 RESIDUAL DECLARADO (inherente al scan estatico, NO bloqueante): allowlist como follow-up del uso vivo.

## Reproduccion (gate por exit code; corrida por mi)
- Zeus clon @ 3d94f11: `npm test` 43/43 (estable). El rework es **test-only** (`git show --stat 3d94f11` =
  solo `tests/staticContract.test.js`, 26 lineas; core/config/#4 SIN tocar -> #4 epoca 1.14.0 byte-identica
  trivial). Protocolo: validate exit 0 CON y SIN secretos; drift 0; neutralidad+encoding exit 0.

## 1) LOS 5 HUECOS CIERRAN (re-probado por mi, misma familia exacta del test aplicada a payloads)
| payload (mi probe previo = SLIPS) | ahora |
|---|---|
| `await import("openai")` (SDK dinamico) | **FLAGGED** [dynamic-import, model-sdk] |
| `await import("undici")` | **FLAGGED** [dynamic-import, http-package] |
| `import net from "net"; net.connect(...)` (bare) | **FLAGGED** [network-call, network-module] |
| `import axios; axios.get(...)` | **FLAGGED** [http-package] |
| `import got; got(...)` | **FLAGGED** [http-package] |
| git push gobernado (allowlist) | SLIPS (correcto: no es primitiva de red) |
La familia nueva agrega `dynamic-import` (marca CUALQUIER `import(`), `network-call`
(`.connect/.request/.get/.createConnection`), `network-module` bare (http/https/net/tls/dgram/dns con o sin
`node:`), model-sdk y http-package estatico Y dinamico. Coincide con la prediccion del Arquitecto.

## 2) CONTROL POSITIVO POR FAMILIA (no solo fetch) -> PASA
El test ejercita 6 familias con asercion por `reason`: fetch, dynamic-import, network-module, network-call,
http-package, model-sdk + el minimo falsable `await import("openai")` -> NO vacio. Un guard que se "afloje"
en cualquiera de esas familias rompe el test. (Nota menor: websocket/http-client/external-cli -- de la
version original -- no tienen positive dedicado en este array; las familias de MIS 5 huecos si.)

## 3) SIN REGRESION en vectores 2-6 -> PASA
- src real -> **[]** (corri la familia sobre todo src/**: cero violaciones, sin falso positivo).
- npm 43/43 (suite completa verde) -> purga/TTL del raw, loop off+consent+deterministic-local+networkEgress
  false, candidatas/estados fuera del ledger, carry AC40/AC43/AC44 siguen verdes.
- core/config/#4 sin tocar (rework test-only).

## 4) GATES -> PASA
validate con/sin secretos exit 0; drift 0; neutralidad+encoding exit 0; #4 byte-identica; npm estable.

---

## RESIDUAL DECLARADO (inherente, NO bloqueante; busque un bypass NUEVO como pidio el operador)
Un scan estatico denylist+regex NO puede cerrar todo. Aun SLIPS (probado):
- **Clientes HTTP no listados:** `import phin from "phin"` / `needle` / `bent` / `ky` -> el nombre no esta en
  http-package y el call no es `.request/.get`. Slips.
- **Ofuscacion deliberada:** `eval("fe"+"tch")(u)`, `globalThis["fe"+"tch"](u)`, `const f=globalThis.fetch; f(u)`
  -> sin `fetch(` literal ni import. Slips.
Estos NO son regresiones ni estaban entre los 5 huecos que marque; son el LIMITE inherente del scan estatico
(enumerar todo cliente HTTP o vencer toda ofuscacion con regex es imposible). La ruta de egress mas REALISTA
para un agente vivo -- `await import("openai"/"@anthropic-ai/sdk")` -- SI queda cerrada (dynamic-import marca
CUALQUIER import()), y los clientes comunes (fetch/axios/got/undici/node-fetch) + sockets + SDKs estan
cubiertos. El operador anticipo este residual ("eval-based, char-encoded, cliente no listado") y fijo el bar
en "no nuevo MATERIAL"; juzgo que NO es material (requiere evasion deliberada, no una regresion accidental).

## RECOMENDACION (follow-up del USO VIVO, NO bloquea este cierre)
Antes del GO de uso vivo del agente (la ventana de modelo real), endurecer a ALLOWLIST: marcar cualquier
`import`/`require` cuyo modulo no este en una lista permitida (fs/path/crypto/url/os/el wrapper git/etc) +
marcar `eval(`/`new Function(`. Eso cierra los clientes-no-listados y la ofuscacion deliberada de raiz. Como
el uso vivo es GO aparte y el extractor entregado es deterministic-local (cero egress), esto es follow-up.

## RECOMENDACION DE CIERRE: OK, CERRABLE la Fase C.
Mi CAMBIO-REQUERIDO previo se resolvio: los 5 huecos cierran, control positivo por familia, src real limpio,
sin regresion, gates verdes, #4 byte-identica. El residual es el limite inherente del scan estatico (allowlist
= follow-up del uso vivo). Con mi OK el Arquitecto puede cerrar la Fase C. Uso vivo = GO aparte del operador.

## Que NO hice
- No promovi, no autore SPEC, no mute estado, no cerre, no encendi nada vivo. Ancle en canonico (3d94f11 /
  9f91dd4). Probes/suite en clones/temporales; no toque el ledger vivo. Scratch limpiado.
