---
decision_id: DECISION-0069
title: Ceremonia de instanciacion ATESTADA -- keygen por agente + registro de firmantes por instancia (auto-atestacion por instancia), con guardrail de congelacion del core medido (TFM)
status: proposed
ratified_at: ""
date: 2026-06-29
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0050, DECISION-0064, DECISION-0068, DECISION-0067, DECISION-0047, DECISION-0045, DECISION-0022, DECISION-0016]
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

2. **Nueva ceremonia de instanciacion atestada** (tier `attested` o paso `init-attestation` en `new_instance.py`,
   mas un script de keygen). Por cada agente DECLARADO en la instancia (roster parametrizable; p.ej.
   Arquitecto/Codex/Analista/los que se deseen):
   - genera un keypair Ed25519 (A2) + un secreto HMAC (A1);
   - escribe las PRIVADAS en `protocol-secrets/` (gitignored) de ESA instancia y referencia via override
     `actor_auth_config.private_key_files` + `event_auth.keys`;
   - escribe las PUBLICAS en un sitio COMMITEADO y PORTABLE del config de ESA instancia
     (`signatures.public_keys`) para que un tercero pueda VERIFICAR el ledger sin los secretos;
   - registra el roster en `agent_registry`/`agent_roles` y crea `personal/<id>/` (DECISION-0016);
   - corre genesis (`regenesis.py`) para anclar la cadena;
   - deja `actor_auth_enforce`/`event_state.enforce` DETRAS de un ENABLE EXPLICITO del operador (sigue siendo
     superficie de riesgo, off-by-default, DECISION-0045/0022).
   La ceremonia NO requiere cambios en `eventlog.py` (ya soporta firmar/verificar + merge de override).

3. **"Firmante" = rol + keypair por instancia.** Las PUBLICAS se publican (commiteadas, portables) para
   verificacion externa; las PRIVADAS jamas se commitean ni viajan en plantillas.

4. **GUARDRAIL TFM (congelacion del core medido) -- VINCULANTE.** Mientras la ventana de medicion siga abierta
   (primeros 500 eventos elegibles seq>=2221, pre-registro v2.0), los archivos PINEADOS de ESTE repo hub NO
   cambian (byte-identicos): `runtime/eventlog.py`, `scripts/validate_collaboration_state.py`,
   `protocol.config.json`, el override `event-state.runtime.json` y el pre-registro v2.0. La ceremonia se
   construye ESTRICTAMENTE fuera de ese core: scripts NUEVOS + extension de `new_instance.py` (scaffolding, NO
   medido) + archivos de instancias NUEVAS (config/override/secrets propios, NO medidos). Si algun subcaso
   exigiera editar un archivo pineado de este repo, se APARCA hasta cerrar la ventana (un cambio asi obligaria a
   un re-baseline pre-resultados, costoso, y queda fuera de alcance de esta decision). El ledger de una segunda
   instancia es OTRO `events.jsonl` y NO entra en el corpus medido.

5. **Efecto sobre el dataset.** Construir esta capacidad es trabajo GOBERNADO (DECISION + tareas + claims +
   cierres via `submit_intent` firmado): sus eventos son elegibles (seq>=2221) y ENGORDAN el corpus, sin
   contaminarlo (igual que TASK-0209/0210/0212). Es aditivo y favorable a la medicion.

6. **Neutralidad de dominio.** La ceremonia, el tier y el tooling son DOMAIN-NEUTRAL (nucleo + `*.template.*`).
   Lo especifico de una instancia aplicada (p.ej. PII/DB de NOVA-Budget) queda FUERA del core (DECISION-0040).

7. **Superficie de producto (Zeus-Aegis).** La accion "instanciar proyecto" del panel que dispara esta ceremonia
   es trabajo de PRODUCTO (repo `Zeus-Aegis`), con su propio SDD; consume el tooling neutral del protocolo. F2
   (write-through al ledger vivo) sigue gateado post-TFM (DECISION-0064); esta accion escribe en instancias
   NUEVAS, no en el ledger medido del hub.

## Consecuencias

- Se emite un SDD (SPEC + TASK, maker=Codex/checker=Arquitecto) para: (a) script de keygen por agente; (b)
  extension de `new_instance.py` con el tier/ceremonia `attested`; (c) publicacion portable de claves PUBLICAS en
  el config de la instancia; (d) golden tests + prueba de verificacion por un tercero (clon sin secretos verifica
  el ledger de la instancia via publicas). Gates verdes; off-by-default; enforce tras enable explicito.
- El hub queda intacto (guardrail #4): cero deltas en archivos pineados hasta cerrar los 500.
- Rollback: borrar los scripts/tier nuevos; el core del hub no se toco.

## Alternativas consideradas

- **Hub unico (no auto-atestacion por instancia):** mantiene 0050 estricto; mas simple para el TFM pero
  contradice la promesa de reuso del fork (instancias plenamente capaces). Rechazada como modelo, aunque el hub
  sigue siendo canonico durante la medicion.
- **Replicar la MISMA identidad/clave del hub en cada instancia:** rechazada por seguridad (propagar una privada
  multiplica el blast radius y rompe el no-repudio por instancia). El agente es un ROL; cada instancia su keypair.
- **Shippear claves en plantillas:** rechazada de plano (secretos en el repo).

## Guardrail resumido (para no olvidar)

> NO tocar archivos pineados del hub (`eventlog.py`, validador, `protocol.config.json`, override, pre-registro)
> hasta cerrar la ventana de 500. Construir solo en scripts nuevos + `new_instance.py` + instancias nuevas. Una
> 2a instancia atesta en su PROPIO ledger, fuera del corpus medido. Si algo exige tocar el core medido -> APARCAR.
