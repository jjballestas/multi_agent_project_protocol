# A2-nominal - pubkeys de los firmantes nuevos (para registrar en el config-epoch de Aegis)

> Nota privada del Arquitecto. Estas son PUBLIC keys (no secretas). Se registran en
> `signature_config.public_keys` del config de AEGIS en el paso A2-nominal (post-B / TASK-9303),
> en UNA sola re-genesis, junto con el alta de agent_registry + personal/<id>/. NUNCA en el hub.
> Las PRIVADAS viven SOLO en la maquina de cada firmante (jheredia = clon de Julian; jball = maquina de John).

| keyid | raw 32B base64 (verificado ed25519, 32 bytes) | actor | capability | recibida |
|---|---|---|---|---|
| `jheredia:v1` | `7p0Hgpg9c1rBeddhj3MG8TGS6jrol5byaoYPDW4joaY=` | Julian (empleado) | implementer (unidades MEDIDAS) | 2026-07-11 |
| `jball:v1` | `pSGHuZPbQQF4aJn4dBhyRSiCUn1DKrMwhAUjjLVyWd0=` | John (operador) | implementer | 2026-07-12 |

Ambas verificadas: decodifican a 32 bytes y cargan como `Ed25519PublicKey`. Distintas entre si.
Se usan en A2-nominal (tras cerrar B); B esta en fix-loop (F-9303-01, iteracion 1/2).
