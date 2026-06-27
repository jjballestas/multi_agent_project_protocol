# ANALISTA TASK-0201 REGATE1 VERDICT

Firma: Analista.

Veredicto: CAMBIO-REQUERIDO. GATE 1 no es cerrable.

Anclas canonicas:
- Protocolo HEAD/instruccion: 45c90a7697b1f1ed89649a4894c77976bee26244.
- Producto: D:/Agentes/Zeus/Zeus-Aegis.
- Commit producto revisado: de7548b35c941a28c3def79a2650b107961271e5.
- Clon limpio producto: C:/Users/johnb/AppData/Local/Temp/zeus-aegis-review-1166132c0ff24a05b32336979f76383c.

## Reproduccion

| Check | Comando / payload | Exit | Resultado |
|---|---:|---:|---|
| Producto clean clone | git clone D:/Agentes/Zeus/Zeus-Aegis TMP; git checkout de7548b; npm test | 0 | PASA. Primera corrida: exit 0. |
| Producto clean clone repetido | npm test en el mismo clon limpio | 0 | PASA. 80 files, 540 tests, exit 0. |
| Probes propios V1/V2/V3/V4/V5 | tsx contra src/server/governance-readonly.ts en el clon limpio | 0 | PASA salvo V4. |
| Protocolo vivo con secretos | python scripts/validate_collaboration_state.py | 0 | PASA, con warning no bloqueante existente de MSG-20260627-Codex-to-Arquitecto-TASK-0193-in-review.md sin context_refs. |
| Protocolo sin secretos | git clone protocolo a tmp; checkout 45c90a7; python scripts/validate_collaboration_state.py --root TMP | 0 | PASA, mismo warning no bloqueante. |
| Drift vivo | runtime.protocol_replay.protocol_state_drift(Path(".")) | 0 | PASA: has_drift=false, up_to_seq=2294. |
| Neutralidad | python scripts/scan_domain_neutrality.py | 0 | PASA. |
| Encoding | python scripts/scan_encoding.py | 0 | PASA. |
| #4 byte-identica | Get-FileHash protocol.config.json SHA256 | 0 | PASA: 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354. |

## Vectores

| Vector | Estado | Evidencia falsable |
|---|---|---|
| V1 read-only real | PASA | Las 8 rutas governance contienen GET y no exponen POST/PUT/PATCH/DELETE; los sources combinados no contienen submit_intent.py ni Area_comun/state/; la UI governance no contiene fetch/axios con metodo write ni submit_intent. |
| V2 lectura canonica | PASA | En clon temporal del protocolo, tras ensuciar Area_comun/state/PROJECT_STATE.slim.json con JSON invalido en working tree, getGovernanceState siguio leyendo git show HEAD y devolvio el estado commiteado. |
| V3 validador rojo no atesta verde | PASA | Familia de overrides: validate=red drift=green -> failed; green/red -> failed; red/red -> failed; green/green -> verified. En todos los eventos devueltos, event.attestation coincide con ledger.attestation. |
| V4 PII en artifacts | SLIPS | Payload propio: artifact commiteado en clon canonico con filename "ANALISTA-TASK-9999-john.doe@example.com Juan Perez Maria-Garcia-review.md" y body "# Review\\n\\nJuan Perez and Maria-Garcia contacted john.doe@example.com...". getGovernanceArtifacts("TASK-9999") redacted email y "Juan Perez" en id/path, pero devolvio "Maria-Garcia" crudo en id/path/preview y preview parcial "# [NAME-REDACTED] Perez and Maria-Garcia...". Esto refuta la familia "nombre-persona en filename/preview redactada"; el regex cruza el heading "Review" + "Juan" y deja el apellido Perez. |
| V5 aparato #4 intacto | PASA | getGovernanceLedger(20, verifyAttestation=false) devolvio 20 eventos con actorAuthMethod y eventAuthMethod presentes. Protocolo vivo: validator exit 0, drift 0, neutralidad exit 0, encoding exit 0, protocol.config.json SHA256 sin cambio. |
| V6 npm test estable | PASA | Dos corridas consecutivas en clon limpio del producto: exit 0 y exit 0; segunda corrida reporto 80 files / 540 tests. |

## Residuales

- No encontre ruta write nueva en el panel F1.
- La atestacion V3 ya no puede ser verde cuando validate o drift no son verdes bajo la familia de estados ejercitada.
- Bloqueante residual: el redactor de nombres es regex-only y no cubre nombres con guion en filename/body; ademas puede consumir una palabra del encabezado anterior y dejar un apellido. El escape es reproducible sin depender de nombres de tests.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar GATE 1 hasta que V4 redacte nombres personales en filename/id/path/preview sin filtrar variantes con guion y sin dejar apellidos por matches que cruzan saltos de linea/encabezados. Prueba negativa permanente sugerida: artifact con filename que incluya email, "Juan Perez" y "Maria-Garcia", y body con heading antes del nombre.
