# Registro de cross-atestacion hub -> NOVA (DECISION-0088 punto 5 / DECISION-0093 / DECISION-0050 punto 5)

> Mecanismo (mismo que el registro hub->Aegis, aplicado a la instancia NOVA bajo la frontera de
> DOS TRIOS): el ledger #4 del hub registra aqui (artefacto commiteado en el hub, cubierto por el
> gate de trailers y la historia firmada del hub) el sha256 de las atestaciones de la instancia
> NOVA. El hub-Arquitecto NO escribe el ledger de NOVA (frontera dos-trios, DECISION operador); solo
> LO LEE (clon de NOVA.git/main) para anclar aqui la cross-atestacion. Verificable por terceros
> re-computando contra el repo NOVA.
>
> Formato de cada entrada: fecha UTC, disparador, commit del repo NOVA, seq del head de cadena,
> prev_hash del head, sha256 del events.jsonl completo, sha256 de la ultima linea de evento,
> event_count, config-epoch sha8.

## Reglas

1. **NOVA es una instancia INDEPENDIENTE de modelo 2.A (1-repo), NO una continuacion de la cadena
   del hub.** A diferencia de Aegis (fork con continuidad de hash de la cadena del hub al tag
   v1.18.0), NOVA tiene un `protocol.genesis` FRESCO y propio: su cadena arranca en seq 1 y el
   genesis liga `canonical_hash(protocol.config.json)` de NOVA (config-epoch sha8 5679362F). El
   gobierno vive como SUBCARPETA dentro del repo de producto `github.com/jjballestas/NOVA.git`
   (`Area_comun/` + `runtime/` + `scripts/` + `protocol.config.json`).
2. Una entrada nueva se agrega en cada: (a) checkpoint de reorg/gobernanza de la instancia NOVA,
   (b) gate de una tarea gobernada de NOVA (ademas del journal de medicion cuando aplique),
   (c) re-verificacion periodica que el Arquitecto juzgue necesaria.
3. Las entradas son append-only; una discrepancia entre una entrada y el estado re-computado de
   NOVA es una anomalia DECISION-0018 a investigar, nunca a editar.

## Entradas

### Entrada 0 - Nacimiento de la instancia NOVA (modelo 2.A) - cierre del A2-nominal NOVA
- fecha_utc: 2026-07-13T13:40Z (hora local 15:40, UTC+2)
- disparador: reorg de instancias (una instancia de gobierno por producto). NOVA queda como
  instancia propia LIMPIA de modelo 2.A (1-repo): el gobierno es una subcarpeta del repo de
  producto NOVA.git. Genesis fresco con 5 firmantes; TASK-9310 (proyector Notion) registrado en el
  ledger de NOVA (proposed/backlog). Esta es la 1a cross-atestacion de la instancia NOVA y cierra
  el A2-nominal NOVA (frontera dos-trios: yo LEO NOVA y anclo aqui; el ledger de NOVA lo escribe su
  propio trio).
- nova_repo: https://github.com/jjballestas/NOVA.git (rama main; carpeta de trabajo D:/Agentes/NOVA-Suite/NOVA)
- nova_commit: 5ca2e5c8be8a3470a8931b58143b0a50d66cbc68
- head_seq: 4
- head_prev_hash: 4728a8f14aec4e7fee7401e15d7c8e776a4a750d93a1eafbfa0e67bdd57da142
- sha256_events_jsonl: 4f69a3dc9d76e7dc9d25a41002284ae52a3a0a48c87c6065918741669fd50a39
- sha256_head_line: d2c1a06b8e4069870fcaaf59916061d1415d057c8ce03b7651aa6a644d526f16
- event_count: 4 (seq 1..4; seq 1 = protocol.genesis FRESCO e independiente, NO heredado del hub;
  config-epoch sha8 5679362F)
- firmantes ed25519 (5, en event_state.signature_config.public_keys + agent_registry): arquitecto:v1
  (orchestrator+reviewer), codex:v1 (implementer), analista:v1 (reviewer / checker-only), jball:v1
  (human_owner+implementer, John), jheredia:v1 (implementer, Julian; privada SOLO en su maquina).
- verificacion (re-computada por el Arquitecto sobre el clon de NOVA.git/main en 5ca2e5c):
  validate_collaboration_state.py exit 0; scan_encoding.py exit 0; scan_domain_neutrality.py exit 0;
  local HEAD == origin/main (5ca2e5c). El hub (2E35F26E / 1.14.0, dataset N=500, sello N=6
  DECISION-0094) NO se toco en ningun momento.
- nota: aislamiento maker/checker en NOVA = clon-limpio + posesion de llave (Opcion B: el Analista
  clona NOVA.git fresco para gatear, sin cloneB persistente). Las llaves del trio viven en
  NOVA/protocol-secrets/ (gitignored + .git/info/exclude local); jheredia/jball privadas en SUS
  maquinas. NOVA en 2.A es la demostracion viva de adoptabilidad (gobierno como subcarpeta del repo
  de producto; el rigor #4 + cross-atestacion + maker!=checker NO necesita repo separado).

### Entrada 1 - Encapsulacion del gobierno bajo Aegis/ + ERRATUM del config-epoch sha8 de la Entrada 0
- fecha_utc: 2026-07-13T15:20Z (hora local 17:20, UTC+2)
- disparador: encapsulacion de la instancia de gobierno (DIRECTIVA operador). El gobierno se movio a
  una SUBCARPETA constante `Aegis/` del repo de producto (git mv puro: Area_comun/ runtime/ scripts/
  skills/ personal/ AGENTS.md protocol.config.json event-state.runtime.json -> Aegis/...), dejando la
  raiz del repo SOLO producto (NOVA.sln, src/, apps/, tests/, docs/). El CI (`.github/workflows/
  validate.yml`) queda en la raiz del repo (requisito de GitHub) con `defaults.run.working-directory:
  Aegis`; el tooling se auto-localiza a Aegis/ (root = parents[1] de la ruta del script). Se anadio
  `Aegis/.claude/` + `Aegis/CLAUDE.md` (config de gobernanza aislada: Claude Code enraiza en el CWD).
- nova_commit: 5518b5a10ab4d8123b9cfd38d2f8e8e695133673 (rama main)
- head_seq: 4  (SIN CAMBIOS respecto a Entrada 0 -- el move NO toca el ledger)
- head_prev_hash: 4728a8f14aec4e7fee7401e15d7c8e776a4a750d93a1eafbfa0e67bdd57da142
- sha256_events_jsonl (blob git, ruta nueva Aegis/runtime/state/events.jsonl): 4f69a3dc9d76e7dc9d25a41002284ae52a3a0a48c87c6065918741669fd50a39 (IDENTICO a Entrada 0 -- el move preserva bytes)
- sha256_head_line: d2c1a06b8e4069870fcaaf59916061d1415d057c8ce03b7651aa6a644d526f16
- config-epoch sha8 (blob git, LF, ruta nueva Aegis/protocol.config.json): **C2DE91F9**
- config canonical_hash (JSON parseado, LE-independiente; lo que liga el genesis): C157FE00 (SIN CAMBIOS)
- event_count: 4 (seq 1..4; genesis fresco intacto -- NO hay re-genesis: el genesis liga
  canonical_hash del CONTENIDO del config, no su ruta, asi que mover el archivo no altera el sello).
- verificacion (re-computada por el Arquitecto sobre el clon limpio en 5518b5a):
  validate_collaboration_state.py exit 0 (`--root Aegis` Y estilo-CI `cd Aegis && --root .`);
  scan_encoding.py exit 0; scan_domain_neutrality.py exit 0. El hub (2E35F26E / 1.14.0, dataset N=500,
  sello N=6) NO se toco.
- **ERRATUM de la Entrada 0 (anomalia DECISION-0018, corregida append-only, NO se edita la Entrada 0):**
  la Entrada 0 registro `config-epoch sha8 5679362F`. Ese valor se computo sobre el working copy del
  clon nova-a2, que tenia CRLF (core.autocrlf=true sobrescribio el eol=lf) -> NO es reproducible desde
  un clon limpio. El valor REPRODUCIBLE (blob git, LF) del config en 5ca2e5c es **C2DE91F9** (identico
  al de 5518b5a, el move no cambia el contenido). El `canonical_hash` (C157FE00, lo que liga el genesis)
  es IDENTICO en ambos casos, asi que el sello/genesis NUNCA estuvo afectado -- solo el hash de bytes
  crudos registrado en Entrada 0. LECCION: los hashes crudos de una atestacion se computan sobre el
  BLOB de git (`git show <commit>:<path>`), nunca sobre el working copy (que puede tener CRLF).
