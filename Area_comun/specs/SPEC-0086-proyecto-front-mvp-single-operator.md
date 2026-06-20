---
spec_id: SPEC-0086
task_id: TASK-0124
type: product
status: accepted
linked_decisions:
  - DECISION-0049
  - DECISION-0029
  - DECISION-0047
  - DECISION-0048
created_at: 2026-06-19
updated_at: 2026-06-19
author: Arquitecto
---

# SPEC-0086 - Proyecto-front MVP (UI single-operator) para operar/observar el protocolo

## Context

DECISION-0049: el proyecto-front (UI single-operator) es el proyecto PRIMARIO de tesis y T0. Repo producto
`D:\Agentes\Zeus\Zeus-protocol` (codigo); gobernanza (esta SPEC, tasks, handoffs) en `Area_comun` (atestada
#4 = dataset publicable). Insumos: `D:\Agentes\Zeus\Zeus-protocol\design\front_requirements.html` (RF/RNF) +
`front_pipeline.html` (etapas). El diseno UI de Claude Design (`design\interface\`) alimenta las tareas de
UI; NO bloquea el resto del SPEC. maker=Codex, checker=Arquitecto, de a una etapa.

## Principio rector (RNF-1/RNF-2)

El front **observa** el protocolo por **patron read-only sobre el CANONICO** (objetos git / origin, NO el
working tree volatil que se re-trunca) y **opera SOLO via `submit_intent`** (escritor unico). NUNCA escribe
estado/ledger directo ni bypassa gates/#4/drift. Toda escritura = transaccion atomica idempotente por
`submit_intent`. PII-free; canal ASCII para lo que escribe al protocolo.

## Scope (MVP-T0 = RF-1..RF-10)

- **Observar (read-only):** RF-1 dashboard (TASK_INDEX backlog, CLAIMS, PROJECT_STATE, version/epoca, drift
  verde/rojo), RF-2 mailbox (open/answered/archived, requires_response), RF-3 artefactos navegables
  (decisiones/specs/tasks/handoffs/reports por id + *_refs), RF-4 ledger #4 / procedencia (timeline
  atestado: seq, actor, firma verificada, prev_hash, anclaje; badge atestado).
- **Operar (gobernado via submit_intent):** RF-5 acciones SDD (crear DECISION/SPEC/task, abrir handoff,
  enviar mailbox), RF-6 GO del operador (aprobar / responder requires_response), RF-7 disparar run de agente
  (caps de autonomia supervisada), RF-8 disparar validacion (validate/gates -> drift/cadena/firmas/anclas/
  scans).
- **N-agente (RF-9, MVP-min):** ver el roster (agent_registry + tool_policy + llm_cli_presets); alta/baja/
  edicion de agente o modelo = **flujo de re-genesis-boundary gobernado** + provisioning de clave (A2), NO
  un toggle (ceremonia gobernada; el conjunto de firmantes queda pinned por el genesis). El MVP solo
  EXPONE/prepara el flujo; la ceremonia es gateada por el operador.
- **Kickoff (RF-10):** lanzar un proyecto nuevo bajo `D:\Agentes\Zeus\` (su primer handoff gobernado = su T0).
- **Intake gobernado de requisitos (RF-14; DECISION-0051):** el operador monta una historia/requisito en un
  wizard (titulo, narrativa, intencion de aceptacion en lenguaje llano, proyecto destino) y la emite como
  artefacto GOBERNADO via submit_intent EXECUTE (`task_upsert` de una tarea `type:requirement`, `actorId:
  "Operador"`, idempotente). Es la SEMILLA del pipeline SDD; el Arquitecto la consume para autorar la SPEC
  (handoff explicito). Habilita la PRIMERA superficie de escritura EXECUTE del operador desde el front,
  acotada al intake, con confirmacion visible. Cuelga del patron `governed-action` (un solo writer).

## Out Of Scope (posterior, pull-based, regla 3.4)

RF-11 export del dataset (etapa 4 posterior), RF-12 multi-proyecto rico (etapa 6 MVP-light minimo),
RF-13 coste/observabilidad; **multi-tenant** (RNF-7, su propia DECISION); Fase 4 / discovery. NO meter
producto/dominio en el core neutral.

## Diseno (etapas del pipeline; una a la vez, SDD)

- **Pre-req (floor):** connector **CI** (deny-by-default, DECISION-0048) ANTES del codigo que compila/testea;
  Git ya esta (TASK-0123). Lectura del protocolo por patron read-only (connector / objetos git).
- **Etapa 1 - Andamiaje:** stack web en `Zeus-protocol`; pipeline CI verde (via connector CI); lectura
  read-only del estado/ledger del canonico; esqueleto de navegacion + base de componentes (segun diseno UI).
- **Etapa 2 - Observar (MVP-read):** RF-1..RF-4 sobre el canonico.
- **Etapa 3 - Operar (MVP-governed):** RF-5..RF-8 via `submit_intent` (sin bypass).
- **Etapa 4 (vista) - Atestacion:** RF-4 timeline + estado boundary T0 / sello / manifest (export = posterior).
- **Etapa 5 - Roster N-agente (RF-9):** exponer/preparar el flujo re-genesis-boundary (ceremonia gateada).
- **Etapa 6 - Multi-proyecto (MVP-light):** selector de proyectos bajo Zeus.

## acceptance_criteria

- **AC1 - Read-only sobre canonico.** Las vistas (RF-1..RF-4) leen el estado/ledger del **canonico** (git
  objects/origin), no el working tree; ningun camino de la UI escribe estado/ledger directo. Verificable:
  grep/review = 0 escrituras fuera de `submit_intent`; las vistas funcionan contra un checkout limpio.
- **AC2 - Escritura SOLO via submit_intent.** Toda accion (RF-5..RF-8, RF-10) emite la transicion por
  `submit_intent` (atomica, idempotente, con actor/timestamp); 0 bypass de gates/#4/drift. Prueba negativa:
  intento de escritura directa al ledger desde el front -> rechazado/ausente por diseno.
- **AC3 - Atestacion visible y correcta.** RF-4 muestra seq/actor/firma verificada/prev_hash/anclaje del
  ledger #4; la verificacion de firma coincide con `validate_chain`/`validate_agent_signatures`/
  `verify_anchor`. Drift verde/rojo coincide con `protocol_state_drift`.
- **AC4 - Gobierno / sin bypass (RNF-1).** No existe ruta en el front que altere estado/ledger sin
  `submit_intent`; lecturas read-only; el front no muestra ni almacena secretos (RNF-4); nunca PII al event
  log (RNF-5).
- **AC5 - Integridad de fuente (RNF-2).** Operaciones que escriben corren con disciplina de canonico/clon
  limpio; el front refleja origin, no el working tree volatil.
- **AC6 - Neutralidad / acoplamiento (RNF-6).** El codigo del front vive SOLO en `Zeus-protocol`; cero
  producto en el core neutral / `*.template.*`; el front no escribe el protocolo salvo por `submit_intent`.
  scan_domain_neutrality del core sigue limpio.
- **AC7 - CI verde como gate (RNF-8).** El pipeline CI del producto (via connector CI) corre y queda verde
  como gate de release de cada etapa.
- **AC8 - Roster re-genesis-gobernado (RF-9).** El MVP NO permite alta/baja de agente como toggle; expone el
  flujo y lo encamina por re-genesis-boundary gateado por el operador (RNF-3, DECISION-0047).
- **AC9 - Determinismo / trazabilidad (RNF-9).** Cada accion del operador queda como evento gobernado en el
  ledger (atestado); vistas deterministas (epoca/version/drift).
- **AC10 - Gates del protocolo verdes.** La coordinacion (esta SPEC, tasks, handoffs) en `Area_comun` deja
  `validate_collaboration_state --root .` exit 0 (con y SIN secretos, DECISION-0046), encoding/neutralidad
  limpios, drift 0; el codigo del producto pasa su CI.
- **AC11 - Honestidad de estado regresion-proof (test de COMPORTAMIENTO) [PERMANENTE].** Para TODA pieza del
  front con badges/indicadores derivados de verificacion (chip canonico, atestacion #4, drift, source-state),
  la honestidad no descansa en string-match: existe un **test de comportamiento** que inyecta una
  verificacion-runtime controlada y asevera el render real -- verificacion que FALLA / no-canonico / no
  verificable -> badge **NO-verde** (warn/danger/indeterminate); TODO valido -> verde; payload de texto libre
  -> SIEMPRE redactado. Falla si un refactor repinta verde una verificacion fallida. AC permanente de las
  etapas con UI (4 ya cubierta retro por TASK-0129; 5/6 lo traen de origen). Es la propiedad-tesis (un badge
  que mienta sobre el estado es el pecado capital): nunca verde hardcodeado.

- **AC12 - AC-ROUTING (comportamiento) [PERMANENTE].** Para CADA nav-item del front, un test de comportamiento
  asevera "clic en X -> SOLO el panel X visible (los demas `hidden`/fuera del DOM visible); topbar +
  integrity-band (epoca/drift/atestado/canonico/seq) SIGUEN presentes". Falla si un refactor vuelve a apilar
  las vistas en un solo scroll (regresion-proof de la navegacion; extiende AC11 a la UX). Satisfecho de origen
  por TASK-0131; permanente para toda etapa con UI navegable.
- **AC13 - AC-CONFORMIDAD-DISENO [PERMANENTE].** Las vistas del front EXISTEN, son navegables y cada una
  corresponde a su pantalla del `front_design_brief` (Backlog=kanban con claims+filtro; Projects=selector con
  entity-cards + "+ add project" cableado al kickoff RF-10 gobernado; Ledger #4=vista dedicada). "Verde" pasa a
  significar tambien "coincide con el diseno". (La pantalla Agentes/Roster 4.6 NO cuenta mientras RF-9 etapa5
  este DEFERIDA; la nav lleva 7 vistas a proposito.) Toda etapa con UI sobre un design brief trae de origen un
  AC de conformidad + un test de comportamiento de interaccion (leccion de proceso, runbook).

### Intake gobernado de requisitos (RF-14; DECISION-0051) - AC14..AC17

- **AC14 - Intake -> artefacto gobernado atribuido al Operador, idempotente.** El wizard estructura la
  historia (titulo, narrativa, intencion de aceptacion en lenguaje llano, proyecto destino) y la emite SOLO
  via submit_intent (`task_upsert` de una tarea `type:requirement`, status `proposed`, `author/owner:
  Operador`). Test de comportamiento: el submit de intake produce el requirement con `author=Operador`;
  re-submit con la misma `idempotency_key` NO duplica. El intake es la SEMILLA, no una SPEC.
- **AC15 - EXECUTE: prueba negativa Y camino feliz con WRITE REAL (DECISION-0052; revisado).** (i) Negativo:
  EXECUTE solo escribe con `confirm:SUBMIT_INTENT`; sin confirm -> rechazo (409), sin escritura. (ii) CAMINO
  FELIZ (write REAL, no mock): test de comportamiento PERMANENTE en CI que demuestra `execute+confirm` ->
  escritura REAL por submit_intent: el requirement aterriza en TASK_INDEX/PROJECT_STATE (proposed,
  author=Operador, relayed_by=Arquitecto), runtime ok con seq, drift 0 despues. El front emite el intake con
  actor RELAY=Arquitecto (firmante pinned) determinado SERVER-SIDE (ver AC19); preview(dry_run) != envio. NO
  basta el dry_run ni el 409: hay que probar que el happy path ESCRIBE de verdad. (Cierra el miss de TASK-0133.)
- **AC18 - Atribucion honesta del relay (RENDER).** Test de RENDER: la UI muestra firmante=Arquitecto y
  `author:Operador`; NINGUN verde/elemento afirma que "Operador firmo". El evento lleva
  `author:Operador`+`relayed_by:Arquitecto`.
- **AC19 - ANTI-IMPERSONACION (prueba negativa PERMANENTE) [CRITICO; DECISION-0052].** El servidor NUNCA
  confia en el cliente para autoria ni forma: se elimina `payload.actorId` y los `payload.intents` crudos;
  cada accion = builder SERVER-SIDE con forma estricta. Test de comportamiento permanente en CI: un POST al
  endpoint EXECUTE que intente (a) un actor distinto, o (b) intents/forma arbitrarios (decision/claim/
  task_status/cualquier forma != requirement-intake) para firmarse como Arquitecto -> es RECHAZADO (no
  construye, no firma, no escribe). Solo la forma exacta del requirement-intake se relaya. Falla si un cliente
  local puede forjar un evento atestado firmado como Arquitecto. Remedia la anomalia DECISION-0018 mergeada en
  Zeus 42e7931.
- **AC20 - Accountability del relay [DECISION-0052].** Firma del relay = ORIGEN+TRANSPORTE, NO aval
  (`endorsement:none`); el aval es la SPEC posterior. Test: un evento relayado NO se cuenta/renderiza como
  AUTORADO ni avalado por el Arquitecto.
- **AC4-byte (refuerzo #4).** El relay/intake no toca `protocol.config.json` (signer set), genesis, keys ni
  `protocol_version`: se aserta BYTE-IDENTIDAD antes/despues (drift 0 es necesario, no suficiente).
- **AC22 - Un intake deja el canonico VERDE [PERMANENTE; DECISION-0018].** Tras un intake EXECUTE, el estado
  resultante pasa `validate_collaboration_state` exit 0: el seed file referenciado por el `task_upsert`
  requirement EXISTE (escrito por el builder) y los claim scopes del relay usan selectores VALIDOS para el
  validador (que reconoce ids de requisito `REQ-[0-9A-Fa-f]+` ademas de `TASK-\d{4}`). Test de comportamiento
  PERMANENTE: tras un intake real, validate exit 0 (regresion-proof; un intake nunca rompe el canonico).
  Remedia la anomalia DECISION-0018 (TASK-0136).
- **AC21 - Reset del formulario + confirmacion inequivoca tras EXECUTE exitoso [comportamiento PERMANENTE; REQ-DCC3BC1A].**
  Tras un EXECUTE **exitoso** del intake (respuesta real del runtime: applied true + seq), el wizard: (a) muestra
  un resultado INEQUIVOCO derivado de la respuesta REAL ("enviado - evento gobernado") con el **id del requisito
  (REQ-xxxx)** y el **seq** del evento; (b) **RESETEA el formulario**: campos vacios, vuelve al paso 1 (capturar),
  estado borrador, `piiAck=false`, listo para una historia NUEVA sin texto stale. Honestidad (hereda AC11): la
  confirmacion y el reset SOLO ocurren si el execute REALMENTE aplico (applied true + seq); si el execute **falla**
  o no se confirma -> **NO reset, NO verde, error real visible, borrador conservado** para reintentar. Elimina el
  reenvio accidental y el mangleo de la siguiente submission por campos stale. Test de COMPORTAMIENTO permanente:
  execute OK -> asertar render de id+seq y formulario reseteado (campos vacios, paso 1, borrador, piiAck=false);
  execute FALLIDO -> asertar NO reset, NO verde, error real, borrador conservado. UX read-only: NO nueva superficie
  de escritura (cuelga del submit ya gobernado). Conformidad AC13 contra `components/intake/` (wizard-4-resultado).
- **AC23 - Vista Help: guia navegable de metodologia y consola, read-only, honesta [comportamiento PERMANENTE; REQ-FB27AF72].**
  Un nav item **Help** entra en `NAV_VIEWS` (routing 1:1 con su panel, hereda AC12: al activarlo solo el panel
  Help es visible y el resto queda hidden; vista desconocida -> fallback DEFAULT_VIEW). El panel renderiza una
  guia DETALLADA y NAVEGABLE (secciones + indice/glosario) que cubre: la consola; observar vs operar;
  `submit_intent` como ESCRITOR UNICO; dry_run vs execute/confirmacion; atestacion #4; las vistas; el intake
  gobernado (RF-14); el pipeline SDD; y un glosario. **Fuente unica = `docs/MANUAL-operador.md`** (se REUSA, NO
  se duplica una copia divergente). Honestidad (hereda AC11): refleja lo que la app HACE HOY incluidas sus
  limitaciones; lo no implementado se marca pendiente/fuera-de-alcance, nunca se afirma como activo. **Read-only:**
  la vista NO escribe estado/ledger, NO expone superficie de escritura (sin botones de accion / sin llamadas a
  `/actions/submit`), extiende la prueba negativa de no-bypass (AC17). Conforme al design-system (hereda AC13:
  dark-first, tokens, la vista existe y navega). Test de COMPORTAMIENTO permanente: "help" en NAV_VIEWS ->
  routing solo-su-panel + fallback; el panel deriva su contenido del manual (no placeholder; cubre las secciones
  clave/glosario); el panel no expone superficie de escritura.
- **AC24 - Mailbox-archive gobernado de 1 click, atestado e idempotente [comportamiento PERMANENTE; DECISION-0053; REQ-B65E7802].**
  La vista **Mailbox** muestra los mensajes con su **estado** (open/answered/archived) y marca los consumidos. Un
  **boton "archivar"** por mensaje en `open/` dispara la accion de relay gobernada `mailbox-archive`: el builder
  SERVER-SIDE construye el intent core `mailbox_archive` desde un `message_id` VALIDADO -> `submit_intent` emite un
  evento ATESTADO (author=Operador, relayed_by=Arquitecto, endorsement=none) y el runtime mueve `open/<msg>.md` ->
  `archived/<msg>.md` con `status: archived` (ASCII). **NUNCA edita el mailbox directo:** no hay ruta de escritura
  del front al filesystem; todo pasa por el runtime (escritor unico; extiende la prueba negativa de no-bypass AC17).
  **Idempotente:** re-archivar (mismo idempotency_key / mensaje ya archivado) es no-op, no falla ni duplica.
  **Honestidad (hereda AC11):** el archive y el cambio de estado en la UI SOLO se reflejan si el runtime REALMENTE
  aplico (evento con seq); si falla -> error real visible, el mensaje sigue en open/, NO se pinta como archivado.
  Conforme al design-system (hereda AC13). Un archive REAL deja el canonico VERDE (validate exit 0; el mensaje
  movido casa carpeta/status; regresion-proof, espiritu AC22).
- **AC25 - ANTI-IMPERSONACION de mailbox-archive (prueba negativa PERMANENTE) [CRITICO; DECISION-0053].** El servidor
  NUNCA confia en datos crudos del cliente para esta accion. Test permanente (no reabrir el 403): forjar
  `payload.actorId`/`payload.intents`/llaves extra -> RECHAZADO (assertAllowedKeys; hereda AC19); archivar un
  `message_id` inexistente o una ruta FUERA de `Area_comun/mailbox/open/` (path-traversal) -> RECHAZADO; usar
  `mailbox-archive` para emitir CUALQUIER otro intent que no sea el `mailbox_archive` de forma exacta -> RECHAZADO.
  El hard-gate 403 admite EXACTAMENTE {`requirement-intake`, `mailbox-archive`}; toda otra forma 403. El evento
  relayado NO se cuenta/renderiza como AUTORADO ni avalado por el Arquitecto (hereda AC20). **AC4-byte:** el nuevo
  intent kind y la accion NO tocan `protocol.config.json` (signer set)/genesis/keys/`protocol_version`; se asierta
  BYTE-IDENTIDAD antes/despues (drift 0 necesario, no suficiente). Golden cases negativos PERMANENTES en el core.
- **AC16 - Guarda PII ESTRUCTURAL + ASCII (pasada del Analista).** La guarda NO depende de un detector
  automatico (TASK-0118/DEF-PII = `proposed`, no existe aun): (a) separar la intencion-en-lenguaje-llano
  (plano publicable) del payload sensible; (b) redactar/marcar el texto libre en todo plano
  publicable/exportable; (c) canal ASCII en todo string que el front escriba al protocolo; (d) advertir al
  operador en compose y en confirm ("no incluyas PII de terceros: NIT, razon social, datos SQL"). Coherente
  con DECISION-0040. Test: payload con patrones tipo NIT/razon social/SQL -> el plano publicable no expone el
  literal; el intake NO levanta el gate TASK-0118/DEF-PII antes de captura viva real. NOTA (Analista): la
  redaccion es best-effort por PATRONES (NIT/razon social/SQL); **no se afirma "PII-free" garantizado** (un
  nombre/email/telefono podria pasar) -- DEF-PII (TASK-0118) sigue siendo el gate.
- **AC17 - No-bypass.** Se mantiene `directLedgerWrites:false`; ninguna ruta del front escribe estado/ledger
  fuera de submit_intent (extiende la prueba negativa de superficie de TASK-0127). El intake cuelga del
  patron `governed-action` (un solo writer), no crea un segundo escritor.

> RF-14 se construye CONTRA el diseno ya entregado por Claude Design en
> `Zeus-protocol/design/interface/components/intake/` (lista, wizard-1-capturar, wizard-2-preview,
> wizard-3-confirmar, wizard-4-resultado, detalle, estados, NOTES.md): **AC13 (conformidad de diseno) aplica
> a estas pantallas**.

## test_plan

- **Producto (Zeus-protocol):** suite del front (unit/integration) + CI verde; pruebas de que las vistas
  leen canonico read-only y que toda accion va por `submit_intent` (mock/dry-run del runtime); prueba
  negativa: no hay camino de escritura directa al ledger.
- **Atestacion:** dado un ledger fixture, el front muestra la verificacion de firmas/cadena/anclaje igual
  que las funciones del runtime.
- **Gobernanza (protocolo):** validate/encoding/neutralidad exit 0 en clon limpio (con y sin secretos);
  cada etapa cierra con su evidencia atestada bajo #4.

## closure_criteria

- Por ETAPA (SDD, maker=Codex/checker=Arquitecto): AC aplicables verdes; CI del producto verde; gobernanza
  en Area_comun valida (exit 0); reporte atestado. El MVP-T0 cierra cuando RF-1..RF-10 (etapas 1-3 +
  vista de atestacion + roster-min + kickoff) estan verdes. Sin tocar #4/config pinned (epoca 1.14.0);
  capacidades fuera del config (DECISION-0047). Export/multi-tenant/Fase4 = posterior.

## Risks

- **Bypass del escritor unico.** Mitigacion: AC2/AC4 (toda escritura por submit_intent; prueba negativa);
  review de que no hay ruta directa.
- **Leer working tree volatil en vez del canonico.** Mitigacion: AC1/AC5 (read-only sobre origin/objetos
  git); disciplina de clon limpio para escrituras.
- **Front infla el contexto de los agentes / coste.** Mitigacion: RNF-10 (contexto minimo; digestion de
  skills); el front no entra al hot path de los agentes.
- **Acoplar el core al producto.** Mitigacion: RNF-6 (producto en repo aparte; unidireccional).

## Traceability

| Requirement | Task | Test | Closure |
|-------------|------|------|---------|
| RF-1..RF-4 observar read-only canonico | TASK-0124 (etapas 1-2) | vistas vs canonico; atestacion vs runtime | AC1/AC3/AC5 |
| RF-5..RF-8,RF-10 operar gobernado | TASK-0124 (etapa 3) | toda accion via submit_intent; prueba negativa | AC2/AC4/AC9 |
| RF-9 roster re-genesis-gobernado | TASK-0124 (etapa 5) | flujo gateado, no toggle | AC8 |
| Honestidad de estado regresion-proof | TASK-0129 (badge behavior test) + etapa5/6 | test de comportamiento: verif. falla -> badge no-verde; valido -> verde; PII redactada | AC11 |
| CI verde / neutralidad / gates | TASK-0124 | CI producto + validate/scan protocolo | AC6/AC7/AC10 |
| RF-14 intake gobernado de requisitos | TASK-0133 (DECISION-0051) | wizard -> task_upsert requirement (Operador, idempotente); EXECUTE con confirmacion (prueba negativa); PII estructural+ASCII; no-bypass; conforme al diseno components/intake/ | AC14/AC15/AC16/AC17 + AC11/AC12/AC13 |
| RF-14 remediacion seguridad (relay acotado + anti-impersonacion) | TASK-0134 (DECISION-0052) | builders server-side (sin trust de payload.actorId/intents); relay-como-Arquitecto SOLO para requirement-intake; firma=origen+transporte no aval; write real demostrado; #4 byte-identico | AC15(write-real)/AC18/AC19/AC20/AC4-byte + carry AC11/12/13/14/16/17 |
