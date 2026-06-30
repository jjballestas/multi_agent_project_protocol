# Re-ejecucion de la medicion H1-H3 (corpus sellado N=500)

Medicion read-only, determinista y reproducible sobre el corpus del tag `TFM-dataset-N500`
(commit `e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9`). No escribe el ledger ni hace commits.

## Requisitos
- Python 3.10+ con el paquete `cryptography` (verificado: 48.0.0).
- Estar en la raiz del repo `multi_agent_project_protocol` con el tag `TFM-dataset-N500` disponible.

## 0. Reconstruir las COPIAS del corpus (no se mide el working tree vivo)
```bash
mkdir -p personal/Arquitecto/TFM-medicion/corpus/runtime/state
git show TFM-dataset-N500:runtime/state/events.jsonl > personal/Arquitecto/TFM-medicion/corpus/events.jsonl
git show TFM-dataset-N500:protocol.config.json   > personal/Arquitecto/TFM-medicion/corpus/protocol.config.json
cp personal/Arquitecto/TFM-medicion/corpus/events.jsonl personal/Arquitecto/TFM-medicion/corpus/runtime/state/events.jsonl
git archive TFM-dataset-N500 runtime/state/snapshots/ | tar -x -C personal/Arquitecto/TFM-medicion/corpus/
# Verificacion del pin (debe imprimir 2e35f26e...):
python -c "import hashlib;print(hashlib.sha256(open('personal/Arquitecto/TFM-medicion/corpus/protocol.config.json','rb').read()).hexdigest())"
```

## 0-bis. Clones para H3 (en cualquier carpeta temporal fuera del repo)
```bash
# Clon LIMPIO sin secretos (git archive nunca incluye secrets/, que no esta trackeado):
git archive --format=tar TFM-dataset-N500 | tar -x -C <DIR>/clean-clone-tag
# Raiz "interna" CON secretos (mismo arbol del tag + las llaves HMAC vivas):
git archive --format=tar TFM-dataset-N500 | tar -x -C <DIR>/internal-with-secrets
mkdir -p <DIR>/internal-with-secrets/secrets
cp secrets/eventauth-*.key <DIR>/internal-with-secrets/secrets/
```

## 1-2. H1 -- Deteccion (A1/A2/A3) + FPR + AC2
```bash
python personal/Arquitecto/TFM-medicion/h1_detection.py \
  --corpus personal/Arquitecto/TFM-medicion/corpus/events.jsonl \
  --config personal/Arquitecto/TFM-medicion/corpus/protocol.config.json \
  --out personal/Arquitecto/TFM-medicion/data --k 50
python personal/Arquitecto/TFM-medicion/h1_fpr_ac2.py \
  --corpus personal/Arquitecto/TFM-medicion/corpus/events.jsonl \
  --config personal/Arquitecto/TFM-medicion/corpus/protocol.config.json \
  --out personal/Arquitecto/TFM-medicion/data
```
`--k` = ataques por subtipo (determinista; indices fijos, no aleatorio). k=50 -> 450 ataques
(A1: 4 subtipos, A2: 4 subtipos, A3: 1 subtipo).

## 3. H2 -- Sobrecoste (latencia / almacenamiento / tokens)
```bash
python personal/Arquitecto/TFM-medicion/h2_overhead.py \
  --corpus personal/Arquitecto/TFM-medicion/corpus/events.jsonl \
  --config personal/Arquitecto/TFM-medicion/corpus/protocol.config.json \
  --out personal/Arquitecto/TFM-medicion/data --repeats 5
```
La latencia es min-of-R por evento; absoluta segun la maquina, pero el VEREDICTO (delta << cota)
es estable. `--repeats` aumenta estabilidad.

## 4. H3 -- Verificabilidad externa (clon limpio, solo publicas)
```bash
python personal/Arquitecto/TFM-medicion/h3_external_verify.py \
  --internal-root <DIR>/internal-with-secrets \
  --external-root <DIR>/clean-clone-tag \
  --out personal/Arquitecto/TFM-medicion/data
```

## 5. Consolidacion
Los JSON de `data/` (`h1_detection.json`, `h1_fpr_ac2.json`, `h2_overhead.json`,
`h3_external_verify.json`, `consolidated_verdicts.json`) + `data/h1_attacks_raw.csv` son los datos
crudos. El informe imprimible es `INFORME-H1-H3-DRAFT.html` (autocontenido).

## Mecanismo real de deteccion (no juicio de agente)
- A1 (integridad/encadenado): `runtime.protocol_replay.validate_chain` (hashes, secret-independiente).
- A2 (no-repudio Ed25519): `runtime.eventlog.verify_actor_auth` (publicas del config).
- A3 (rollback ancla): `runtime.protocol_replay.verify_anchor_monotonicity` + `validate_chain`
  (el ancla efectiva del corpus es el genesis de cadena ligado a `protocol.config.json`, #4).
- Hash de estado secret-independiente: `runtime.protocol_replay.replay_protocol_state`.
