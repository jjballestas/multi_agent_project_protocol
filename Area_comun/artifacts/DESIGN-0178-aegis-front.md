---
artifact_id: DESIGN-0178-aegis-front
task_id: TASK-0178
type: design-spec
author: Arquitecto
created_at: 2026-07-27
status: for_review
supersedes_concept: "consola conversacional Operador<->Arquitecto que activa el runtime (concepto original 2026-06-25)"
---

# DESIGN-0178 -- El Aegis Front (panel soberano de operacion de la metodologia)

> Deliverable de diseno de TASK-0178. REENCUADRA el concepto original (una "consola" para hablar
> directo al Arquitecto y activar su runtime) tras el debate del Operador (2026-07-27). El diseno se
> gobierna DESDE el hub (dataset); el CODIGO se construye en `Zeus-protocol` bajo `D:/Agentes/Zeus/`,
> nunca en el hub. Requiere aprobacion humana; abre DECISIONes de formalizacion (seccion 12).

## 0. Correcciones tras revision adversarial (2026-07-27) -- MANDAN sobre el resto

Una critica adversarial (4 revisores independientes, `docs/critica-adversarial-sintesis.md`) tumbo o
reencuadro parte de la estrategia. Estas correcciones PREVALECEN sobre cualquier seccion posterior:

- **FUERA la certificacion como foso.** No es dificil, es estructuralmente IMPOSIBLE: ISO/IEC 17065
  (el autor de un esquema no puede ser su certificador acreditado) + open-core hace la conformidad
  AUTOVERIFICABLE (cualquiera corre los validadores y ancla en Rekor sin permiso). Reemplazo: la
  PRIMERA CLAUSULA CONTRACTUAL (un cliente que exija "conforme al protocolo vX" en un pliego).
- **El ancla es GRATIS y de tercero neutral: Sigstore/Rekor** (log de transparencia publico), no un
  ancla del vendedor. Cobrar por anclar penaliza registrar-todo (el cliente muestrea y destruye la
  completitud del log). El ancla no es negocio.
- **EL FOSO es el CORPUS de datos normativos** (como se ve una ejecucion conforme, tasas base,
  distribucion de fallos por gate, comparacion entre instancias). Solo lo tiene quien observa muchas
  instancias; crece con la adopcion; no se copia leyendo el repo. Hoy n=1.
- **DOS MODOS de medicion (misma app):** MODO DUENO (instancias del operador -> mide TODO -> su
  dataset global; es su trabajo, sin problema de consentimiento ni soberania) y MODO SOBERANO
  (instancias de cliente -> CERO egreso; el corpus alli solo crece por servicio consentido). Toggle
  duro, OFF por defecto en cualquier instancia no-propia. La soberania es frontera del PRODUCTO-PARA-
  OTROS, no del trabajo propio.
- **Front INTERNO primero, mercado despues (gateado).** Construir AHORA = tooling interno para operar
  las instancias propias + gobernar la migracion T0 + medir. El APARATO DE MERCADO (licencia,
  distribucion, productizacion L2/L3, marca) es fase POSTERIOR, gateada por un reality-check de
  desplegabilidad ("una tarde con una persona") + traccion del servicio. En paralelo: el SERVICIO de
  linea-base (diagnostico) como carril de revenue + corpus.
- **T0 = la migracion Access -> SQL Server AHORA** es el primer trabajo real que el front gobierna;
  arranca el reloj del corpus ya (cada dia sin registrar es dataset tirado, no retrofiteable).
- **Riesgo a respetar:** que el traje comercial coma las horas del T0 (corpus) y del servicio
  (revenue). Disciplina: solo el MVP de operabilidad ahora; difiere la maquinaria de mercado.

Lo que SOBREVIVE intacto: la arquitectura L1/L2/L3, el modelo soberano de ancla, y el open-core
Apache-2.0 del motor+spec (reforzado: como la certificacion cerrada es imposible, open-core es la
unica jugada coherente).

## 1. Proposito y reencuadre

El requisito original de 2026-06-25 pedia un "canal conversacional vivo Operador<->Arquitecto que
activa el runtime del Arquitecto". El debate concluyo que **un canal de control directo usuario->
Arquitecto es el acoplamiento equivocado**: el Arquitecto es un trabajador gobernado que actua sobre
el ledger #4, y no debe firmar ni actuar por el usuario. La autoridad de aprobar/firmar es del dueno
humano y debe ser un acto deliberado, registrado y atribuido al humano.

El Aegis Front se rediseña como **el panel soberano para operar la metodologia**, con tres capas
separadas por diseno, y como una **app descargable auto-provisionable** para nacer instancias de
producto-de-dominio (born-operational, gobernanza encapsulada en `Aegis/`, cross-atestada).

## 2. Invariantes de diseno (no negociables)

- **I1 -- El Arquitecto nunca firma ni actua por el usuario.** El runtime del Arquitecto se dirige por
  el FLUJO GOBERNADO (mailbox / GO / DECISION), no por un chat de usuario.
- **I2 -- Firmar es un acto humano consciente.** El front debe FORZAR que el humano VEA y firme; nunca
  un click que delegue la firma. Estructura la disciplina que hoy el operador pone a mano.
- **I3 -- La privada del humano vive solo en su maquina.** Se genera/importa bajo un acto consciente de
  alta, con respaldo, y JAMAS se exfiltra.
- **I4 -- Soberania por defecto (sin dataset global).** Cada instancia es su propia raiz de confianza;
  ningun dato del cliente sale hacia el vendedor. Tamper-evidence via ancla del cliente o tercero
  neutral, nunca el hub del vendedor.
- **I5 -- El front es NEUTRAL de dominio.** Opera cualquier producto; el dominio vive en la instancia
  que crea, nunca en el front.
- **I6 -- El motor y la spec son abiertos y auditables** (Apache-2.0); el dominio + marca +
  certificacion + soporte son el foso propietario. La cripto/atestacion/ledger NUNCA es cerrada.

## 3. Arquitectura de tres capas

**L1 -- Observacion (read-model).** Vista NO-autoritativa del trabajo vivo del Arquitecto + estado del
ledger/mailbox/tareas, como el operador lo ve hoy en VS Code (streaming del trabajo y el reporte). Es
la parte legitima del requisito original: OBSERVAR, no controlar. Read-only; no muta nada.

**L2 -- Asistente IA no-firmante.** Interlocutor conversacional que ayuda al HUMANO a entender, decidir
y REDACTAR (explica el ledger, prepara un borrador de DECISION/GO/FIRMA), con CERO capability
gobernada. Es el rol Asesor (participante no-firmante ya existente) productizado. Principio: **el
asistente draftea, el humano firma.** Sin dientes: nada que diga el asistente toca el ledger.

**L3 -- Autoridad humana (firma).** Controles EXPLICITOS de aprobacion (botones/formularios tipo "los 5
botones del Operador") que producen un acto REGISTRADO y firmado con la autoridad del HUMANO. El front
muestra exactamente que se va a firmar (diff/impacto) y exige confirmacion consciente (I2). El acto se
atesta al ledger como del humano, nunca del Arquitecto (I1).

Separacion clave: L2 (redactar sin dientes) y L3 (firmar con dientes) son sitios DISTINTOS -- una
conversacion casual nunca se convierte por accidente en un acto gobernado.

## 4. Donde se construye (hub vs producto)

- **Diseno/gobernanza (este SPEC, DECISIONes, tasks, atestacion)** -> en el HUB (dataset permanente
  neutral). Por eso TASK-0178 (design) vive aqui.
- **Codigo del front (UI React+TS, puente de runtime, streaming, controles de firma)** -> en
  `Zeus-protocol` bajo `D:/Agentes/Zeus/`. Nunca el hub (romperia neutralidad + citabilidad +
  acoplaria el hub permanente a un producto).
- **Ancla de cross-atestacion** -> siempre al hub para el trabajo de construccion del propio front
  (DECISION-0095), separado del ancla soberana de las instancias que el front genera (I4).
- Mi rol desde el hub: **disenar, gobernar y orquestar** -- activar/dirigir (DECISION-0057) a los
  agentes que escriben el codigo en `Zeus-protocol`.

## 5. El Aegis Front como app soberana auto-provisionable

La app se descarga y ejecuta y, en el arranque, **nace una instancia** de producto-de-dominio
(born-operational). Reutiliza lo que ya existe: `new_instance.py` (acuna trio + genesis + config +
ledger) + la ceremonia born-operational (DECISION-0096) + el panel encima. La app NO es solo UI: es
runtime + scaffolder + panel empaquetados, firmados y verificables.

### 5.1 Ceremonia de provision (orden estricto)

1. **Alta del humano** -> se generan sus llaves de firma **en su maquina**, como acto consciente, con
   respaldo forzado; la privada nunca sale (I3).
2. **Alta de agentes + asignacion de roles** -> el usuario declara que LLMs tiene y los mapea a roles.
3. **Generacion de firmas de agentes** -> ed25519 + HMAC de los 3 roles, locales.
4. **Genesis soberano** -> canonical_hash del config de ESTA instancia como raiz (epoca propia).
5. **Ancla** -> el usuario elige su store de ancla (propio o tercero neutral) para tamper-evidence.

### 5.2 Separacion LLAVES (roles) vs LLMs (motor) -- resuelve "no todos tienen mas de un LLM"

**Las llaves separan los ROLES (siempre 3: Arquitecto/Codex/Analista -- atribucion + capability +
firma). Los LLMs son el MOTOR, y se mapean 1..N a esos roles.** El usuario mapea lo que tenga; la app
muestra el nivel de garantia resultante (escalera honesta de degradacion):

| LLMs disponibles | Mapeo | Garantia |
|---|---|---|
| 1 | mismo motor "viste los 3 sombreros" | Funciona, pero review adversarial DEBIL (mismo modelo se auto-revisa; riesgo rubber-stamping). La app lo AVISA. |
| 2 | maker en uno, checker en otro | Review con PROVEEDOR DIVERSO preservado (lo importante); orquestador comparte. |
| 3+ / peones locales | trio diverso; peon local draftea (nunca firma), fuerte revisa/firma | Garantia plena. |

`quality_policy.allow_self_review:false` + la diversidad de proveedor son la guarda; con 1 LLM se
relaja la diversidad pero se mantiene la separacion de rol (prompts/contexto distintos). Transparencia
de calidad = diferenciador, no limitacion oculta.

## 6. L1 -- Puente de runtime y streaming (observacion)

El requisito original (ver al Arquitecto trabajar en vivo) se implementa como **puente de runtime en
modo OBSERVACION**: un wrapper interactivo (como los crons pero en vivo) que ejecuta al Arquitecto y
transmite su trabajo/reporte a la UI por streaming. Diferencia con el concepto original: el usuario NO
"activa y dirige" al Arquitecto por chat -- lo dirige el flujo gobernado; el usuario OBSERVA. Para el
dueno, la observacion puede ser cruda (firehose, como VS Code); un read-model curado (paneles de
mailbox/estado) es la vista para terceros si algun dia los hay.

## 7. L2 -- Asistente (el Asesor productizado)

Identidad DISTINTA del Arquitecto, registrada con CERO capability gobernada (o no-actor). Lee el ledger
y el estado, explica, y prepara BORRADORES (de DECISION, GO, FIRMA, o de una directiva al Arquitecto).
El LLM del asistente: para productos con datos sensibles (municipal/financiero), opcion de **modelo
local / cero-egress de PII** (conecta con el carril de peones), no una API cloud a ciegas.

## 8. L3 -- Controles de aprobacion humana

Botones/formularios que producen actos gobernados FIRMADOS por el humano: firmar una DECISION, dar un
GO, aprobar un release. Cada control: (1) muestra el diff/impacto exacto de lo que se firma; (2) exige
confirmacion consciente (I2); (3) atesta el evento como del humano; (4) el borrador puede venir de L2,
pero la firma es un acto separado y deliberado. El runtime del Arquitecto se dispara desde el FLUJO
gobernado que estos actos alimentan (un GO firmado -> el Arquitecto trabaja), no desde un chat.

## 9. Soberania y modelo de ancla (I4)

- **Auto-anclada:** cada instancia descargada es su propia raiz (su genesis). Nada cross-atesta al
  vendedor. NO hay dataset global de clientes (evita responsabilidad de tratamiento de datos sensibles,
  rechazo enterprise/publico a "phone-home", y single-point-of-failure).
- **Tamper-evidence sin centralizar:** `anchor_enabled` ya es configurable -> `anchor_config.remote_url`
  apunta al store del cliente o a un tercero neutral (log de transparencia / timestamping). Un auditor
  verifica integridad SIN confiar en el vendedor. Soberano != no-verificable.
- **Senal de mercado (opcional):** telemetria OPT-IN, anonimizada, agregada (metricas, no el ledger),
  canal separado y consentido. El dataset de INVESTIGACION del vendedor (N=500 propio) queda aparte y no
  se nutre de clientes.

## 10. Monetizacion y actualizacion sin phone-home

- **Actualizar sin romper soberania -- ya resuelto por el versionado de dos ejes (DECISION-0047):** la
  linea de RELEASE (`runtime_version`, CHANGELOG) avanza sin tocar la EPOCA pineada (genesis del
  cliente). Se actualiza el CODIGO, jamas el ledger/genesis del cliente. Updates = paquetes de release
  FIRMADOS que el cliente jala (feed publico de artefactos firmados = descargar, NO egresar datos; o
  air-gap manual). El cliente verifica la firma antes de aplicar.
- **Monetizacion (open-core Apache):** motor neutral + spec **Apache-2.0** (auditables = el foso de
  confianza; norma citada). Foso PROPIETARIO: **profiles de dominio** (Nova-Municipal/Financiero, NO
  bajo Apache), **marca** ("Aegis", "Aegis Certified" -- Apache no concede marca), **certificacion/
  cumplimiento** y **soporte**. Vender el ECOSISTEMA, no el ejecutable. Licencia OFFLINE firmada
  (verificada localmente) para el edge de pago; sin verificacion central de uso.

## 11. Componentes y stack (a construir en Zeus-protocol)

- **Front UI:** React + TS + Vite (paridad con el stack NOVA). Vistas: observacion (L1), asistente
  (L2), controles de aprobacion (L3), provision/onboarding.
- **Puente de runtime:** wrapper interactivo del Arquitecto con streaming a la UI (modo observacion).
- **Provisioner:** envuelve `new_instance.py` + keygen + la ceremonia (seccion 5) en UX.
- **Motor:** el runtime del protocolo (submit_intent, ledger #4, validadores, guardarailes) empaquetado
  -- Apache, auditado.
- **Distribucion:** releases firmados (keyless), updater de feed publico o air-gap, licencia offline.

## 12. Follow-ups de gobernanza (a formalizar tras aprobacion)

- **DECISIONes:** (a) frontera de las 3 capas + I1/I2/I3 (el Arquitecto nunca firma por el usuario;
  firma humana consciente; privada humana solo local); (b) modelo de ancla SOBERANO por defecto (I4,
  sin dataset global); (c) open-core Apache-2.0 para motor+spec + limite propietario dominio/marca/
  certificacion (I6).
- **Tasks (en Zeus-protocol, gobernadas desde el hub):** puente de runtime + streaming; provisioner UX;
  ceremonia de llaves con mapeo LLM->rol; controles L3 de firma consciente; distribucion firmada +
  licencia offline.

## 13. Fases (MVP -> completo)

1. **MVP L1:** panel de observacion (streaming del Arquitecto + estado del ledger). Alto valor,
   bajo riesgo, reemplaza VS Code para OBSERVAR.
2. **Provision:** ceremonia de alta (humano -> agentes -> roles/LLMs -> genesis soberano).
3. **L3:** controles de firma consciente (los actos gobernados desde la UI).
4. **L2:** asistente no-firmante (con opcion de modelo local).
5. **Distribucion:** releases firmados + licencia offline + updater; profiles de dominio de pago.

## 14. Preguntas abiertas

- Sabor exacto de la certificacion ("Aegis Certified") y su proceso.
- Modelo de soporte/servicios (tiers) y como se empaquetan los profiles de dominio.
- Vista curada vs firehose para L1 si aparecen observadores terceros (hoy: solo el dueno).
- Eleccion del tercero-neutral de ancla por defecto (log de transparencia / timestamping).
