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

### Entrada 1 - Humo e2e de firmantes VERDE + DECISION-1001/1002 registradas (POST-aprovisionamiento)
- fecha_utc: 2026-07-06T03:58Z (hora local 05:58, UTC+2)
- disparador: gate de corte completado -- el Operador aprovisiono los firmantes
  (provision_local_signers.py, secretos HMAC frescos de instancia + override, ejecutado por el
  Operador 2026-07-06); el Arquitecto ejecuto el ciclo e2e de humo TASK-9301 (ready -> claimed
  -> in_progress -> in_review -> review_approved -> done, 18 intents: Arquitecto upsert+
  decisiones, Codex build-flips+done, Analista ratificacion) y registro DECISION-1001/1002
  (aceptadas por el Operador ~06:00 local) en el ledger de Aegis.
- verificacion de firmas: los 14 eventos del ciclo de humo verificados VALIDOS en actor_auth
  ed25519 (keyids arquitecto:v1 x3, codex:v1 x8, analista:v1 x3) y event_auth HMAC de
  instancia; validate exit 0; drift 0 (re-materializacion comparada).
- aegis_commit: 3e9e90b8 (rama aegis/main del remoto git@github.com:jjballestas/Zeus-Aegis.git)
- head_seq: 3475
- head_prev_hash: 958b06c6cdabf0bfe084c01a0910f3f94e8f3faba12a35e66e9ebe12c9282c5a
- sha256_events_jsonl: 3bfb03ead3d243c28213c62a2d65dc2eda671f82551aa2c7a79c0ed769904edd
- sha256_head_line: e3c7b6ce6a4d46b925ad1c7ea9843ea3b871796142adf5a7e9d7e379f15846e1
- event_count: 2804 (seq 672..3475)
- nota: el gate PENDIENTE del runbook multi-clon (humo e2e entre DOS clones con llaves
  separadas por maquina) corre antes de la primera tarea real de Contabilidad; este humo
  probo la operatividad de los 3 firmantes en el clon canonico.

### Entrada 2 - Gate e2e DOS CLONES VERDE (TASK-9302) - gate de apertura de Contabilidad CUMPLIDO
- fecha_utc: 2026-07-06T04:55Z (hora local 06:55, UTC+2)
- disparador: gate del runbook multi-clon s.5 ejecutado contra el remoto GitHub real
  (git@github.com:jjballestas/Zeus-Aegis.git, rama aegis/main): ciclo TASK-9302 repartido --
  upsert+build-flips en clon A (firmas Arquitecto/Codex), ratificacion in_review->
  review_approved desde clon B FRESCO que solo posee la llave privada del Analista, done-flip
  de vuelta en A; sincronizacion SOLO via git pull/push.
- prueba negativa: intento de firma como Codex en el clon B FALLO ("actor_auth private
  signing key missing") sin escribir estado -- separacion maker/checker por POSESION de llave.
- verificacion: validate exit 0 en AMBOS clones tras el pull final; firmas de los 11 eventos
  del gate verificadas VALIDAS desde el clon B (Codex x8, Analista x3).
- HALLAZGO DE DISENO incorporado: los secretos HMAC de event_auth son DE LA INSTANCIA y deben
  DISTRIBUIRSE a los clones autorizados (el operador los copio); secretos frescos por clon
  rompen la paridad de replay (verificado: el clon B con secretos distintos rechazaba TODO el
  replay historico como invalid_signature). Runbook multi-clon s.2 corregido en esta entrega.
  Tambien: los slim views DEBEN commitearse con cada escritura de ledger o el clon par ve
  drift (mordio una vez en este gate, corregido en b3cd5fc1).
- aegis_commit: 8941efb1 (aegis/main)
- head_seq: 3495
- head_prev_hash: ce9bfc0f2dfae070505cc99d9fb30d6c9667aabdb4b42b54ae78f66f989761fa
- sha256_events_jsonl: e9d8c1f84c48e4b270a1c25d38c73d13e6881f9dabb49c10c44af39bdfc62ac2
- sha256_head_line: 8818097b8d183460727d0e0f3b7b8cd57a54a9b9b3eee49ea2b677821c2c2897
- event_count: 2824 (seq 672..3495)
