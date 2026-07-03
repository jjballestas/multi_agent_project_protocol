# RUNBOOK - Ensayo de atestacion del SELLO Etapa 1 (pre-armado, NADA sellado)

> Directiva Operador MSG-20260704-...-cola-trabajo-ventana-muerta, item PRIMARIO.
> Objetivo: de-riesgar el reloj real del 08-jul dejando el mecanismo de atestacion listo, para que
> el dia del sello sea UN intent atomico limpio. **ESTO ES UN ENSAYO: no sella, no congela, no
> registra ningun intent.** Fecha de ensayo: 2026-07-04 (~22:17Z maquina).

## 1. Manifiesto de corpus - ENSAYO (7 de 9 artefactos; hashes NO congelados)

Computado con el procedimiento del dia-del-sello (SELLO s.1): `sha256sum <archivos> | (clave=basename) sort`.
Salida en `personal/Arquitecto/TFM-medicion/ENSAYO-CORPUS-MANIFEST-etapa1.txt`.

| Artefacto (basename) | sha256 (ENSAYO 2026-07-04) | fuente |
|---|---|---|
| NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md | ef1e56e7c1b950559d8e3952231662040a1008999baf6002eb28d7671b2e2a41 | D:/Agentes/Ingenas/.../NOVA_Budget_Process (fuera del hub) |
| NOVA_ESTUDIO_Protocolo_Medicion.md | de38530acfd927bb9c4683224a85863ca8b6ae85de5b8cd0ab09c172185969b1 | idem |
| NOVA_ESTUDIO_Anexo_Diseno_Completo.json | 4a52ff58f1363f005ee8daaa72800cad065a3d0da3408422fb4c4a59be835c7c | idem |
| schema_medicion.json (v-PILOTO, no v1.0) | 7f9289705981966a69bcbaa9c79324e90333f6bedd74befbaa34f034e11f7626 | hub corpus (gitignored) |
| schema_defectos.json (v-PILOTO, no v1.0) | ec1569ffd8be7278ba61e6d09ff62931c89930257636ab7ca9cc535353aa66cb | hub corpus (gitignored) |
| medicion_ledger.py | 3e92cca5962f88ff3e77286e263ea20d2b5f461e6555454fec776c99e5595344 | hub corpus (gitignored) |
| SELLO-ETAPA-1-nova-budget-DRAFT.md | 58424422c1ea2ca6bdcb120bb6e3f7a94d17e5ce075e42c880ff78a2b68b1a1e | hub personal/operador |
| medicion_journal.csv (GOAL-P1 3-8 jul) | AUSENTE - no existe hasta el piloto | -- |
| this SELLO (auto-hash tras congelar) | se recomputa tras [LLENAR] el dia del sello | -- |
| **HASH DE MANIFIESTO (ensayo, 7 filas)** | **0ef7eab2c72574d36b5b7b3262632d5bacffe9d9eb8b5f3365269b9525d3433c** | -- |

Verificacion: los 7 hashes son reproducibles hoy; el manifiesto real del 08-jul incluira 9 filas y
distintos hashes (freeze v1.0 + journal). Este hash de ensayo NO es el del sello.

## 2. Procedimiento del dia-del-sello (exacto, a ejecutar el 08-jul)

```bash
cd /d/Agentes/multi_agent_project_protocol
NOVA=/d/Agentes/Ingenas/Budget/02_Analysis/Arquitectura/NOVA_Budget_Process
CORP=personal/Arquitecto/TFM-medicion/corpus/medicion
SELLO=personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md   # ya SELLADO (LLENAR resuelto)
JOURNAL=personal/Arquitecto/TFM-medicion/corpus/medicion_journal.csv     # tras GOAL-P1
# 1) manifiesto (9 filas), clave=basename, ordenado
{ for f in "$NOVA"/NOVA_ESTUDIO_*.md "$NOVA"/NOVA_ESTUDIO_*.json \
           "$CORP"/schema_medicion.json "$CORP"/schema_defectos.json "$CORP"/medicion_ledger.py \
           "$SELLO" "$JOURNAL"; do
    echo "$(basename "$f")  $(sha256sum "$f" | cut -d' ' -f1)"; done; } | sort \
  > personal/operador/vision-nova/CORPUS-MANIFEST-etapa1.txt
# 2) hash de manifiesto + hash del doc del sello
sha256sum personal/operador/vision-nova/CORPUS-MANIFEST-etapa1.txt   # -> HASH DE MANIFIESTO (s.1 del sello)
sha256sum "$SELLO"                                                   # -> sha256 del documento
# 3) commitear el sello + manifiesto (rutas gobernadas si viven en Area_comun; ver GAP-4)
# 4) atestacion: UN intent atomico (s.3)
```

## 3. Vehiculo de atestacion en el hub (dry-run VALIDADO 2026-07-04)

Se probo (import `normalize_intent`, sin escribir evento) cual intent del hub sirve para atestar:
- **`decision`: NORMALIZA OK. Vehiculo RECOMENDADO** = permanente, entra a la cadena #4, produce
  `seq`. El SELLO se registra como `DECISION-00XX` (pre-registro); su `.md` contiene el manifiesto
  con los 9 sha256 + el hash de manifiesto + el sha256 del doc. `--commit <sha del commit que
  contiene el sello sellado>` ata el contenido por el arbol git; el intent lo ancla en el event log.
- **`project_narrative`: INADECUADO** - solo admite campos `next_actions/risks/open_questions`
  (narrativa TRANSITORIA que se poda); no es un registro permanente de atestacion.
- **No existe un intent de atestacion/notarizacion de PRIMERA CLASE** (un `attest {sha256, artifact}`
  que registre el hash de un artefacto externo en la cadena #4). Confirmado: campo libre rechazado.
  Ver GAP-5 (candidato de diseno, no bloquea el sello: el vehiculo `decision` cubre la necesidad).

Plantilla exacta del intent del dia-del-sello (rellenar decision_id + timestamp + commit):
```bash
python runtime/submit_intent.py --actor-id Arquitecto \
  --timestamp "<ISO-8601 UTC del sello = T>" \
  --commit "$(git rev-parse HEAD)" \
  --intent-json '{"type":"decision","decision_id":"DECISION-00XX"}'
# Requisitos (arquitecto-ledger-ops s.2b): el .md DECISION-00XX YA creado (artifacts-before-claim);
# claim activo del Arquitecto cubriendo PROJECT_STATE.json (ruta FULL) + el .md de la decision +
# CLAIMS.json#<claim_id>. La seq resultante + idempotency_key -> [LLENAR-AL-SELLAR] s.0 del sello.
```

## 4. GAPS (lo que falta, para no improvisar el 08-jul)

1. **medicion_journal.csv AUSENTE** hasta que corra el piloto GOAL-P1 (3-8 jul). Su fila existira en
   el ledger de medicion cuando el piloto registre; el manifiesto de 9 filas no se cierra sin el.
2. **Freeze schema v-PILOTO -> v1.0** es del dia del sello (editar SOLO el JSON, subir version):
   los sha256 de schema_medicion/defectos CAMBIARAN respecto a este ensayo. Los de hoy son v-piloto.
3. **Campos [LLENAR-AL-SELLAR] del SELLO** (T, pulso NIST, seq/idempotency_key, tabla de sorteo,
   estimates S/M/L, verificacion readonly Q4 una-a-una): entradas del Operador/asesor + del dia-de.
4. **Convencion de ruta del manifiesto:** el hash de manifiesto depende de la CLAVE de cada linea
   (basename vs ruta relativa). Este ensayo usa BASENAME (estable, coincide con la tabla s.1 del
   sello). Congelar la convencion EN el sello para que el hash sea reproducible por terceros.
5. **[DISENO, no bloquea] Sin intent de atestacion de primera clase.** El hub no tiene un primitivo
   `attest {artifact, sha256}`; se usa el vehiculo `decision`. Candidato para Carril B / follow-up
   (se cruza con R-07 atestacion!=observabilidad de F1.6). NO se resuelve para este sello.
6. **Ubicacion del sello para la cadena #4:** si el `.md` del sello vive en `personal/operador/`
   (no gobernado) el commit lo ata igual por sha, pero para que el gate de trailers y la traza sean
   nitidos conviene que el registro formal (DECISION-00XX) viva en `Area_comun/decisions/`. Decidir
   con el asesor/Operador al sellar (no ahora).

## 5. Estado

ENSAYO COMPLETO. Mecanismo probado end-to-end en seco: manifiesto reproducible + vehiculo `decision`
dry-run-validado + gaps enumerados. El dia del sello = 1 commit (sello+manifiesto) + 1 intent
`decision`. NADA sellado ni registrado en este ensayo.
