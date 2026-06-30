# INSTRUCCION (Operador) -- Alimentar el TFM en el agente Estudio con evidencia nueva del protocolo

- Vigencia: permanente, hasta cierre del TFM.
- Actor: Operador (o asistente-operador en su nombre). NO es regla vinculante del protocolo (no toca
  AGENTS.md, ledger ni decisiones); es un runbook del operador. No requiere submit_intent.
- Caso destino (agente Estudio): `D:\Agentes\Estudio\Formal_Work\TFM_Protocolo_Multiagente\`
  (trabajo formal F5; memoria de continuacion en `02_Agent_Work\memoria\MEMORIA-CONTINUACION-REDACCION.md`).

## Regla de oro: el corpus medido es INMUTABLE
La medicion del TFM esta sellada en N=500 (tag `TFM-dataset-N500`, commit `e3646ae`). Todo evento o dato
GENERADO DESPUES es **post-ventana**: NO altera el experimento medido. Se incorpora al caso como
**material adicional declarado** (contexto, replicacion, trabajo futuro), nunca reescribiendo la evidencia
sellada en `01_Sources/Other/dataset/`.

## Disparadores: que cuenta como evidencia que alimenta el TFM
Cuando en el protocolo (`D:\Agentes\multi_agent_project_protocol`) se produzca cualquiera de:
1. **Nueva corrida de medicion** H1/H2/H3 (re-ejecucion, otra maquina, otro N) o nuevos scripts/data en
   `personal/Arquitecto/TFM-medicion/`.
2. **Crecimiento o nuevo sello del dataset** (otro corpus, p.ej. N>500 o un segundo sello) -> nuevo
   `events.jsonl` + reporte de sello.
3. **Nueva DECISION** que afecte la atestacion (vectores A1-A4, Ed25519/actor_auth, replay
   secret-independiente, GATE-DATASET, anclaje externo, memoria/engram).
4. **Nuevo informe** de auditoria o **veredicto** adversarial (Analista) sobre la medicion.
5. **Cambio del instrumento pineado** (`runtime/eventlog.py`, `scripts/validate_collaboration_state.py`,
   `protocol.config.json`, `event-state.runtime.json`, pre-registro) -> registrar como NUEVA version,
   sin sobreescribir la copia byte-identica ya en el caso.

## Donde cae cada cosa en el caso (01_Sources/)
| Evidencia nueva | Destino en el caso |
|---|---|
| Pre-registro nuevo (v3.0...), firma | `01_Sources/Documents/pre-registro/` |
| Reporte (sello / auditoria HTML) | `01_Sources/Documents/reportes/` |
| Veredicto del checker (Analista) | `01_Sources/Documents/veredictos/` |
| DECISION nueva relevante | `01_Sources/Documents/decisions/` |
| Scripts de medicion / instrumento / golden | `01_Sources/Code/{medicion,instrumento,golden}/` |
| Dataset nuevo + config pin | `01_Sources/Other/dataset/` (nombre versionado, p.ej. `corpus_events_N###.jsonl`) |
| Datos crudos (json/csv) | `01_Sources/Other/resultados_crudos/` |

## Procedimiento (byte-identico y trazable)
1. Copiar el original **sin modificarlo**. Para conservar bytes desde un tag usar:
   `git -C <repo> archive -o <salida>.tar <tag> -- <ruta>` y extraer (NO `git show > file` ni pipe binario
   en PowerShell: corrompe bytes).
2. **Verificar sha256** de lo copiado y anotarlo (corpus sellado de referencia: `a90756d6...`;
   pin config: `2e35f26e...`; hash de estado replay: `dd2fd60e...`).
3. Registrar la fuente en `00_Project_Config/Source_Index.md` y la accion en `Processing_Log.md`.
4. Si cambia algo que afecte la redaccion, anotarlo en
   `02_Agent_Work/memoria/MEMORIA-CONTINUACION-REDACCION.md` y en `MAPA-EVIDENCIA-CAPITULOS.md`.
5. NO editar originales (regla 1 del caso). NO marcar el caso como cerrado sin revision humana.

## Recordatorio de rigor (se hereda del agente Estudio)
Cero cifras inventadas (toda cifra trazable a `01_Sources/`); referencias verificadas (no inventar DOIs);
limitaciones declaradas sin maquillar. Ver skill `rigor-ml-datos` y `Contexto_Redaccion.md` del agente Estudio.
