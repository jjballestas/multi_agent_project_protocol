# SPEC-0091 - Front: alta de worker de producto enlazado a un modelo (US-4, Q3)

- **Estado:** draft (registrada en el ledger; pendiente GO ejecutado a Codex). Maker: Codex. Checker: Arquitecto
  + **pasada del Analista** (fronteras: no toca #4/genesis/firmantes; clave privada nunca al cliente; write acotado).
- **Fecha:** 2026-06-24. Repo producto: D:/Agentes/Zeus/Zeus-protocol.
- **Origen (REQ del operador):** REQ-4A88ECFFC4 (US-4 del backlog del panel "Operar Agentes" Q3).
- **Relacionada:** SPEC-0086 (front MVP; AC17 no-bypass / AC72 error amable), DECISION-0050 (front=panel),
  DECISION-0047 (versionado por epoca / config pinned), connectors/extractors off-by-default pattern.

## Objetivo

Que el operador de de alta desde el front un **worker de producto** (tipo Extractor) y lo enlace a un **modelo**
(endpoint + nombre del modelo local), para sumar capacidades **sin tocar el nucleo ni la firma del ledger**. El
worker se registra **fuera del config atestado** (en el registro de workers de producto `extractors.config.json`
/ su override de runtime), con su propia clave de PRODUCTO, **apagado por defecto**; el **uso vivo** del worker
exige un permiso aparte (la habilitacion de file-ingestion ya existente, off-by-default). El alta **NO** cambia
`protocol.config.json` (agent_registry / signature_config), ni el genesis, ni el #4.

## Alcance / Out of scope

- En alcance: (1) accion gobernada en el front para registrar un worker {id, role, provider, defaultModel,
  defaultEndpoint} en el registro de workers de producto; (2) provision de la clave del worker (par de PRODUCTO,
  para autoria honesta de sus candidatas), con la **privada solo server-side** (gitignored, nunca al cliente,
  nunca commiteada) y la **publica** en el registro; (3) el worker nace **apagado** (no habilitado para uso vivo).
- Fuera de alcance: alta de **agentes firmantes del ledger** (eso es US-5 = ceremonia re-genesis, GATEADA);
  conceder uso vivo (lo da el gate de file-ingestion aparte); ejecutar el worker; multi-tenant.

## acceptance_criteria

- **AC1 - Alta gobernada del worker.** El front ofrece registrar un worker con campos {id, role, provider,
  defaultModel, defaultEndpoint}; la accion es **server-side gobernada** (preview dry_run -> confirmas -> execute)
  y escribe UNA entrada acotada en el registro de workers de producto (`extractors.config.json` o su override de
  runtime gitignored). Behavior-test: el preview muestra la entrada; el execute la persiste; sin confirmacion no
  escribe.
- **AC2 - Clave de producto, privada nunca al cliente.** El worker recibe su par de claves de PRODUCTO; la
  **privada** se escribe SOLO server-side en una ruta de secretos **gitignored** y **nunca** se envia al cliente
  ni se commitea; en el registro solo va la **publicKeyPem**. (Alternativa valida: el operador provee la publica;
  en ningun caso el front maneja una privada hacia el cliente.) Behavior-test: la respuesta al cliente y el
  registro NO contienen material de clave privada; el commit no incluye la privada.
- **AC3 - Off-by-default / uso vivo aparte.** El worker registrado nace **apagado**: registrarlo NO lo habilita
  para correr; el uso vivo exige el gate de file-ingestion ya existente (off-by-default, enable por runtime). El
  registro escrito refleja el estado apagado (o el master versionado queda enabled:false y el alta va al override
  de runtime). Behavior-test: tras el alta, el worker NO esta habilitado para uso vivo sin el gate aparte.
- **AC4 - No toca #4 / genesis / firmantes (frontera dura, carry AC17).** El alta NUNCA escribe
  `protocol.config.json` (agent_registry / signature_config), ni el genesis, ni el ledger atestado; NO emite
  `submit_intent` (es un config de PRODUCTO, no del protocolo) y NO abre ninguna ruta de escritura al ledger. #4
  byte-identica. Behavior-test (prueba negativa): el alta deja protocol.config.json y el #4 byte-identicos; ningun
  agente firmante nuevo aparece en signature_config.
- **AC5 - Write acotado y validado (carry lecciones 0166).** El server valida estrictamente la entrada: campos
  **typeof string** (rechaza no-string/array/object -> 400 antes de coercion), id no duplicado, sin path-traversal
  ni claves extra, `defaultEndpoint` restringido a loopback/localhost (consistente con el egress guard local-vlm).
  Nunca compone un comando ni escribe fuera del registro permitido. Behavior-test: id duplicado, campo no-string,
  endpoint no-loopback, clave extra -> 400 sin escribir.
- **AC6 - Estado claro + error amable + off-by-default / sin riesgo nuevo (carry AC72).** "registrando" + exito o
  error amable (registro ocupado / invalido), no traceback crudo. La capacidad nace OFF (no expone uso vivo). PII:
  texto libre redactado.

## Carries permanentes (SPEC-0086)
- **AC11 badge-honesto** (indicadores derivados de verificacion real), **AC12 routing-comportamiento**,
  **AC13 conformidad-de-diseno** (tokens del design-system).

## DoD

- AC1-AC6 verdes con behavior-tests deterministas; AC11/AC12/AC13 verdes; carry AC16/AC17/AC72.
- node --test clon limpio exit 0; validate con/sin secretos exit 0; drift 0; neutralidad+encoding 0; **#4
  byte-identica** (prueba negativa AC4). PII redactada; export PII-free. La clave privada del worker NUNCA en el
  cliente ni en git.
- Reproducido por el checker (Arquitecto) DESDE CLON LIMPIO; maker!=checker. **PASADA DEL ANALISTA** (foco: AC4
  no-toca-#4/genesis/firmantes; AC2 privada-nunca-al-cliente; AC5 write acotado/validado sin type-confusion;
  off-by-default).
- REPRO: en el front, registrar un worker {id, role, modelo endpoint+nombre} -> aparece en el registro de workers
  de producto (no en signature_config), apagado, con su publicKeyPem; protocol.config.json y #4 intactos; un alta
  invalida (id dup / no-string / endpoint no-loopback) se rechaza con error amable.

## Notas de diseno

- Construir sobre `loadProductWorkers()` / `extractors.config.json` (registro existente de workers de producto).
  Preferir escribir el alta a un **override de runtime gitignored** (como file-ingestion.runtime.json) dejando el
  master versionado en su estado base, para no commitear workers ni claves.
- Versionado por epoca (DECISION-0047): el registro de workers vive FUERA del config pinned; el alta no requiere
  re-genesis (no toca firmantes). Esa es justamente la diferencia con US-5 (firmante = ceremonia).
