# Guia de trabajo - Julian Heredia (maker de Contabilidad, instancia Aegis)

> DRAFT del Asesor para el onboarding de Julian. Version clara/accesible de "como vas a trabajar".
> El detalle tecnico exacto (comandos) esta en `Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md`
> y en `AGENTS.md` del repo Aegis. Esta guia es el mapa; el runbook es el manual.
> Pendiente: el Arquitecto la coloca gobernada en el repo Aegis (para que la descargues al clonar).

## 1. Quien eres en el equipo
Eres **maker (implementer)** de las unidades de **Contabilidad** de la suite Nova, operando un **clon remoto**
propio de la instancia Aegis desde tu maquina (Colombia, UTC-5). Tu identidad de firma es `jheredia:v1` (llave
propia; ver setup). Tu trabajo se atesta con TU llave en el ledger de Aegis.

- **Maker (tu):** construyes la unidad segun su SPEC-contrato.
- **Checker (otra maquina, otra llave):** te revisa de forma adversarial. NUNCA te auto-verificas.
- **Arquitecto:** coordina (te da el GO, ratifica, promueve la siguiente).

## 2. El modelo mental (metodologia gobernada)
- **Todo es archivo + ledger atestado.** El estado del proyecto (tareas, claims, mailbox, decisiones) vive en
  archivos versionados; cada cambio es un evento FIRMADO en una cadena tipo blockchain (`#4`).
- **maker != checker (duro).** El que construye no aprueba. La separacion es POR POSESION DE LLAVE: tu maquina
  tiene solo tu privada; no puedes firmar como el checker.
- **Gates duros, no opinion.** Una entrega pasa por verde de gates (build/tests/revision adversarial), no por
  "a mi me parece". Si el gate muerde, se corrige; no se debilita el gate.
- **Nada se decide despues de ver datos.** El pre-registro (sello) manda; no se cambian reglas para que salga
  bonito.

## 3. Setup (una sola vez; comandos exactos en el runbook s.1/s.2/s.8)
1. **Acceso:** el Operador (John) te invita al repo privado GitHub y te pasa el link.
2. **Clonar:** `git clone -c core.longpaths=true <url>` (el flag evita el fallo de rutas largas en Windows).
3. **Tu llave (ya iniciada):** generaste tu par ed25519; mandaste SOLO la publica (el Arquitecto la registra
   en el config de Aegis). Tu **privada** se queda en tu maquina, en tu `protocol-secrets/`.
4. **Secretos HMAC:** el Operador te DISTRIBUYE los secretos HMAC de la instancia (no los generas tu; secretos
   propios romperian la verificacion del historial). Van en `secrets/` (gitignored, nunca se commitean).
5. **Override (`event-state.runtime.json`):** con SOLO tu llave privada (principio de llave minima) y el
   `anchor` deshabilitado (adjudicacion: el anchoring lo corre solo el clon canonico de John). El runbook te
   dice como.
6. **Runtime Python operativo** + un smoke de `submit_intent` en tu maquina (esta instancia es escritor-unico
   duro: todo pasa por el runtime, no se edita estado a mano).
7. **Gate de apertura:** antes de tu primera tarea real de Contabilidad, se corre un ciclo e2e de humo entre
   TU clon y el clon de John. Solo con ese humo verde arrancas.

## 4. Como haces UNA tarea (el ciclo, de principio a fin)
1. **Recibes un GO** (ACTION en el mailbox) con: la ruta de la SPEC-contrato, el repo de producto, y el bloque
   de operacion del ledger.
2. **Ventana segura + claim:** `git fetch`; si nadie tiene claim sobre tus rutas y no hay medio-escrito de un
   peer, reclamas la tarea (`submit_intent`, claim anidado con `scope#self`) y **haces push INMEDIATO** (un
   claim sin pushear es invisible para los demas y no reserva nada).
3. **Construyes** segun la SPEC-contrato (en el repo de producto). Nada de improvisar: la SPEC es el contrato.
4. **Gates verdes** (build + tests + lo que pida la tarea) ANTES de entregar.
5. **Handoff autocontenido:** dejas un handoff que el checker pueda usar sin preguntarte nada (evidencia
   completa, que se probo, como reproducir).
6. **Entrega atomica:** una sola transaccion `submit_intent` que mueve `in_progress -> in_review` y libera tu
   claim. Commit con **pathspec explicito + trailers + slim views** (`*.slim.json`), y **push inmediato**.
7. **Esperas la REVIEW** del checker (por mailbox). Si da NO-GO, corriges (fix-loop) y re-entregas. Si da
   **review_approved**, TU haces el `-> done` (es la unica transicion que te toca a ti; el checker no la hace).

## 5. Reglas duras (no negociables)
- **Todo cambio de estado va por `submit_intent`.** Editar `Area_comun/state/*.json` a mano ROMPE el gate
  (hard-fail por drift). Nunca lo hagas.
- **Ventana segura + push inmediato** en cada transicion. Commits con pathspec (no `git add .` pelado),
  trailers, y slim views (si faltan, el otro clon ve drift y su submit_intent aborta).
- **ASCII puro** en mensajes/mailbox (sin acentos/em-dash; rompen el scan de encoding).
- **Timestamps en UTC** en submit_intent (tu estas en UTC-5; los reportes del Arquitecto van en su hora local).
- **No auto-verificas.** No apruebas tu propia unidad.
- **No borras mensajes del mailbox** (se archivan de forma gobernada; borrar es una anomalia).
- **No tocas el core pineado del hub** (epoch 1.14.0) ni el estudio medido. Trabajas en Aegis/producto.
- **Predica con el ejemplo:** el producto que construyes es ANTI-VIBECODING; no hagas vibecoding para
  construirlo (requerimiento claro antes de implementar, verificacion antes de dar por hecho).

## 6. Donde esta el detalle
- **Runbook de onboarding:** `Area_comun/protocol/RUNBOOK-onboarding-multi-clon-aegis.md` (comandos exactos,
  s.1 remoto / s.2 llaves / s.3 reparto / s.5 gate e2e / s.8 tu alta).
- **Contrato del proyecto:** `AGENTS.md` (reglas compartidas) + `CLAUDE.md`.
- **Scripts:** `scripts/provision_local_signers.py`, `runtime/submit_intent.py`, `scripts/validate_collaboration_state.py`.
- **Gobernanza del corte hub->Aegis:** DECISION-0093 (por que Aegis es su propio ledger que continua la cadena
  del hub).

## 7. Tu primer objetivo
Pasar el gate e2e de 2 clones (con John) y luego tomar la primera unidad de Contabilidad (analisis de
migracion -> unidades implementables). El Arquitecto te dara el GO cuando el gate este verde.

-- Preparado por el Asesor para el operador (John). Colocacion gobernada en Aegis: pendiente del Arquitecto.
