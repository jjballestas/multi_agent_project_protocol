# Registro de cross-atestacion hub -> Aegis (DECISION-0088 punto 5 / DECISION-0093 punto 2)

> Mecanismo cableado por el corte de gobernanza hub->Aegis (DECISION-0093). El ledger #4 del hub
> registra aqui (artefacto commiteado en el hub, cubierto por el gate de trailers y la historia
> firmada del hub) el sha256 de las atestaciones de la instancia Aegis. Durante el Sprint 1
> gobernado, las entradas por gate van ADEMAS en el journal de medicion (DECISION-0088 punto 5);
> este registro es el ancla estructural del enlace y el historial de cortes/checkpoints.
>
> Formato de cada entrada: fecha UTC, disparador (gate/checkpoint), commit del repo Aegis,
> seq del head de cadena de Aegis, prev_hash del ultimo evento, sha256 del events.jsonl completo,
> sha256 de la ultima linea de evento. Verificable por terceros re-computando contra el repo Aegis.

## Reglas

1. Aegis NO opera como cadena #4 independiente: su ledger es una continuacion (fork con
   continuidad de hash) de la cadena del hub al tag v1.18.0 (ultimo evento heredado seq 3457),
   y cada checkpoint relevante se ancla aqui.
2. Una entrada nueva se agrega en cada: (a) checkpoint de corte/gobernanza, (b) gate de una
   tarea gobernada de la suite Nova en Aegis (ademas del journal de medicion), (c) re-verificacion
   periodica que el Arquitecto juzgue necesaria.
3. Las entradas son append-only; una discrepancia entre una entrada y el estado re-computado de
   Aegis es una anomalia DECISION-0018 a investigar, nunca a editar.

## Entradas

### Entrada 0 - Baseline del corte (estado heredado, PRE-humo e2e)
- fecha_utc: 2026-07-06T02:55Z (hora local 04:55, UTC+2)
- disparador: corte de gobernanza hub->Aegis (DECISION-0093), estado del ledger Aegis ANTES del
  primer evento propio de la instancia
- aegis_commit: 814365a702ff45752bb68f7b68b9506b41ffafa4
- head_seq: 3457
- head_prev_hash: 9149a3e897955dc9a8ad1f98a1487ad526a9d8cff84bfd58ec8253e141524387
- sha256_events_jsonl: 5aed54be5422a044b981ef263072bcfe274a8a5cc6bcbb84cba1cb5c23d04562
- sha256_head_line: 550ec6dcbf345b6690d025e03ac655c4ad9dce696a92010a3c044a26ff7b19c2
- event_count: 2786 (seq 672..3457, continuacion de la cadena del hub; seq 1..671 sellados
  pre-T0 segun chain_manifest.json de Aegis)
- nota: firmantes ed25519 = MISMAS identidades que el hub (public_keys identicas en
  event_state.signature_config: arquitecto:v1 / codex:v1 / analista:v1). La operatividad local
  (secretos HMAC de instancia + override event-state.runtime.json) requiere aprovisionamiento
  del OPERADOR (frontera DECISION-0057: el Arquitecto no acuna credenciales). La Entrada 1 se
  registrara tras el ciclo e2e de humo post-aprovisionamiento.
