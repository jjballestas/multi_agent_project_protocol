---
decision_id: DECISION-0069
title: Ceremonia de instanciacion ATESTADA -- roster por instancia (firmantes + workers keyless + binding LLM), keygen solo a firmantes, invariante de frontera; con guardrail de congelacion del core medido (TFM)
status: proposed
ratified_at: ""
date: 2026-06-29
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0050, DECISION-0064, DECISION-0068, DECISION-0067, DECISION-0057, DECISION-0047, DECISION-0045, DECISION-0040, DECISION-0022, DECISION-0018, DECISION-0016]
phase: P2
---

# DECISION-0069 - Ceremonia de instanciacion atestada (auto-atestacion por instancia)

> PROPOSED (borrador 2026-06-29, a ratificar por el operador). Nace del debate operador<->Arquitecto: el fork de
> Hermes (Zeus-Aegis, DECISION-0064) existe para que la metodologia se APLIQUE; por tanto instanciar deberia poder
> producir una instancia "con todo lo que la metodologia puede hacer" (runtime + atestacion + roster de firmantes),
> no un cascaron coordination-only. Hoy NO es asi y NO hay tooling para lograrlo.

## Contexto (verificado)

- `new_instance.py` instancia en dos tiers: `coordination` (default; ligero) y `runtime` (copia `runtime/`+
  `scripts/`+CI). **Incluso `runtime` nace TODO APAGADO y sin firmantes** (`event_auth.enabled:false`, sin claves,
  sin genesis): "tener los archivos del motor no lo activa". La instancia NOVA (`D:/Agentes/Zeus/NOVA`) se creo en
  tier `coordination` -> sin `runtime/`, sin `scripts/`, `event_state` OFF, 0 firmantes.
- **No existe** ningun script de keygen / alta de firmante / onboarding. Los firmantes vivos del hub
  (Arquitecto/Codex/Analista) se cablearon a MANO: privadas en archivos gitignored referenciados por el override
  `actor_auth_config.private_key_files`, y `event_auth.keys` para la capa HMAC (A1).
- Los **ladrillos SI existen**: `eventlog.py` ya firma/verifica Ed25519 (A2) + HMAC (A1) y mergea el override
  (DECISION-0068/0067); `regenesis.py` ya hace genesis; el override `event-state.runtime.json` ya permite anadir
  firmantes SIN re-genesis. Lo que falta es la **ceremonia** que ate esas primitivas.
- Restriccion de seguridad innegociable: un firmante = una CLAVE PRIVADA. Las plantillas NUNCA traen secretos.
  Por tanto "Analista firmante al instanciar" solo puede significar: la ceremonia GENERA un keypair fresco para
  ese rol EN esa instancia. Cruzando instancias, el agente es un ROL; cada instancia tiene su propia clave.

## Decision

1. **Modelo: auto-atestacion POR INSTANCIA.** Una instancia de metodologia (la que tiene su propio `Area_comun/`)
   PUEDE auto-gobernarse y auto-atestar en su PROPIO ledger firmado, con su propio roster de firmantes y sus
   propias claves. Esto **complementa, no deroga, DECISION-0050**: 0050 sigue rigiendo el CODIGO de producto
   (repos de codigo bajo `D:/Agentes/Zeus/` no llevan governance); lo que se aclara es que una *instancia de
   metodologia* no esta obligada a delegar su atestacion al hub -- puede ser autonoma. El hub
   (`multi_agent_project_protocol`) sigue siendo la instancia canonica y la sede de la medicion del TFM.

2. **Roster por instancia con DOS EJES ortogonales por agente.** La instancia declara un roster parametrizable
   (los agentes que se deseen) y por cada agente fija dos campos INDEPENDIENTES:
   - **`tier`/`signer`** (eje de RESPONSABILIDAD): `firmante` (frontera) o `worker` (peon). Firma e identidad
     criptografica solo para firmantes.
   - **binding de runtime/LLM** (eje de EJECUCION): que CLI/modelo corre los turnos de ese agente. Es
     independiente de si firma; un firmante puede correr cualquier modelo, un worker corre uno barato.
   Registrar un agente NO implica asignarle clave de firma; son ejes separados (hoy `agent_registry` ya no tiene
   campo de modelo y `llm_cli_presets` son presets de CLI genericos -- se anade el binding por-agente, neutral).

3. **Ceremonia de instanciacion atestada** (tier `attested` o paso `init-attestation` en `new_instance.py`, mas un
   script de keygen):
   - **Firmantes (jefes/frontera):** genera keypair Ed25519 (A2) + secreto HMAC (A1); PRIVADAS en
     `protocol-secrets/` (gitignored) referenciadas por el override (`actor_auth_config.private_key_files` +
     `event_auth.keys`); PUBLICAS en sitio COMMITEADO y PORTABLE del config de ESA instancia
     (`signatures.public_keys`) para verificacion por terceros sin secretos.
   - **Workers (peones):** se registran KEYLESS en `agent_registry`/`agent_roles` (sin keypair) para
     trazabilidad/provenance; bajo `enforce` NO pueden escribir el ledger (sin clave -> `submit_intent` los
     rechaza), por diseno.
   - Todos los que ejecutan reciben su **binding de runtime/LLM** (reusando el selector de modelos de Hermes,
     DECISION-0064); el binding es config de instancia, NO core, NO parte de la identidad firmante.
   - Crea `personal/<id>/` para cada agente (DECISION-0016); corre genesis (`regenesis.py`) para anclar la cadena;
     deja `actor_auth_enforce`/`event_state.enforce` DETRAS de un ENABLE EXPLICITO del operador (off-by-default,
     DECISION-0045/0022).
   La ceremonia NO requiere cambios en `eventlog.py` (ya soporta firmar/verificar + merge de override).

4. **Invariante de frontera (delegacion atestada).** El entregable de un agente NO-firmante (worker/peon) entra al
   ledger ATESTADO **solo** a traves del verify+firma de un firmante (jefe). El peon produce en staging/su area
   personal; el jefe revisa y hace el `submit_intent` (close/upsert) -> SU firma atesta. Esto preserva maker!=checker
   (DECISION-0018) y mantiene el set firmante pequeno y confiable. **Provenance OBLIGATORIA:** el evento firmado
   registra como metadata el AUTOR real (id del worker) y el modelo que lo produjo, para no confundir TRABAJO con
   RESPONSABILIDAD en la auditoria/dataset (la provenance es metadata de instancia, no toca el core pineado del hub).

5. **"Firmante" = rol + keypair por instancia.** Las PUBLICAS se publican (commiteadas, portables) para
   verificacion externa; las PRIVADAS jamas se commitean ni viajan en plantillas.

6. **GUARDRAIL TFM (congelacion del core medido) -- VINCULANTE.** Mientras la ventana de medicion siga abierta
   (primeros 500 eventos elegibles seq>=2221, pre-registro v2.0), los archivos PINEADOS de ESTE repo hub NO
   cambian (byte-identicos): `runtime/eventlog.py`, `scripts/validate_collaboration_state.py`,
   `protocol.config.json`, el override `event-state.runtime.json` y el pre-registro v2.0. La ceremonia se
   construye ESTRICTAMENTE fuera de ese core: scripts NUEVOS + extension de `new_instance.py` (scaffolding, NO
   medido) + archivos de instancias NUEVAS (config/override/secrets propios, NO medidos). Si algun subcaso
   exigiera editar un archivo pineado de este repo, se APARCA hasta cerrar la ventana (un cambio asi obligaria a
   un re-baseline pre-resultados, costoso, y queda fuera de alcance de esta decision). El ledger de una segunda
   instancia es OTRO `events.jsonl` y NO entra en el corpus medido.

7. **Efecto sobre el dataset.** Construir esta capacidad es trabajo GOBERNADO (DECISION + tareas + claims +
   cierres via `submit_intent` firmado): sus eventos son elegibles (seq>=2221) y ENGORDAN el corpus, sin
   contaminarlo (igual que TASK-0209/0210/0212). Es aditivo y favorable a la medicion.

8. **Neutralidad de dominio.** La ceremonia, el tier y el tooling son DOMAIN-NEUTRAL (nucleo + `*.template.*`).
   Lo especifico de una instancia aplicada (p.ej. PII/DB de NOVA-Budget) queda FUERA del core (DECISION-0040).

9. **Superficie de producto (Zeus-Aegis).** La accion "instanciar proyecto" del panel que dispara esta ceremonia
   es trabajo de PRODUCTO (repo `Zeus-Aegis`), con su propio SDD; consume el tooling neutral del protocolo. El
   panel **reusa el selector de modelos de Hermes** para fijar el binding LLM por agente del roster (eje de
   ejecucion), mientras el protocolo es dueno de la identidad de firma y el ledger. F2 (write-through al ledger
   vivo) sigue gateado post-TFM (DECISION-0064); esta accion escribe en instancias NUEVAS, no en el ledger medido
   del hub.

10. **PII: DIFERIDO (fuera de alcance de esta decision).** La postura PII por instancia y el detector de
    enforcement (DEF-PII, TASK-0118) se deciden mas adelante; su semantica/base legal sigue en DECISION-0040
    (esquema de dos planos: ledger PII-free siempre; datos reales solo en la DB de la app). 0069 no abre ni cierra
    ese tema; cuando se aborde, se referencia 0040.

## Consecuencias

- Se emite un SDD (SPEC + TASK, maker=Codex/checker=Arquitecto) para: (a) script de keygen por FIRMANTE; (b)
  extension de `new_instance.py` con el tier/ceremonia `attested` y el ROSTER de dos ejes (firmante/worker +
  binding LLM); (c) registro KEYLESS de workers (peones) con provenance; (d) publicacion portable de claves
  PUBLICAS en el config de la instancia; (e) campo de binding runtime/LLM por-agente (slot neutral; el picker lo
  pone Hermes en el panel); (f) provenance (autor real + modelo) como metadata en el evento firmado por el jefe;
  (g) golden tests + prueba de verificacion por un tercero (clon sin secretos verifica el ledger via publicas) +
  prueba de que un worker keyless NO puede escribir el ledger bajo enforce. Gates verdes; off-by-default; enforce
  tras enable explicito.
- El hub queda intacto (guardrail #6): cero deltas en archivos pineados hasta cerrar los 500.
- Rollback: borrar los scripts/tier nuevos; el core del hub no se toco.

## Alternativas consideradas

- **Hub unico (no auto-atestacion por instancia):** mantiene 0050 estricto; mas simple para el TFM pero
  contradice la promesa de reuso del fork (instancias plenamente capaces). Rechazada como modelo, aunque el hub
  sigue siendo canonico durante la medicion.
- **Replicar la MISMA identidad/clave del hub en cada instancia:** rechazada por seguridad (propagar una privada
  multiplica el blast radius y rompe el no-repudio por instancia). El agente es un ROL; cada instancia su keypair.
- **Shippear claves en plantillas:** rechazada de plano (secretos en el repo).
- **Todos los agentes firmantes (sin tier worker):** rechazada -- cada peon necesitaria keypair y entraria al
  set de no-repudio, encareciendo y diluyendo la frontera. El modelo por tiers mantiene el set firmante pequeno y
  confiable; los peones se coordinan keyless y su trabajo lo atesta un jefe (invariante de frontera, #4).
- **Acoplar el LLM a la firma (registrar firmante = asignar modelo):** rechazada -- son ejes ortogonales
  (responsabilidad vs ejecucion). Un firmante puede correr cualquier modelo; un worker corre uno barato sin firmar.

## Guardrail resumido (para no olvidar)

> NO tocar archivos pineados del hub (`eventlog.py`, validador, `protocol.config.json`, override, pre-registro)
> hasta cerrar la ventana de 500. Construir solo en scripts nuevos + `new_instance.py` + instancias nuevas. Una
> 2a instancia atesta en su PROPIO ledger, fuera del corpus medido. Si algo exige tocar el core medido -> APARCAR.
