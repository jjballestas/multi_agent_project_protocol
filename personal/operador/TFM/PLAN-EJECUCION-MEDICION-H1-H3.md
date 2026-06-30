# PLAN DE EJECUCION -- Medicion H1-H3 sobre el corpus sellado N=500

- Emite: Operador (John Ballestas) -- via asistente-operador
- Ejecuta: Arquitecto (single-writer / runtime) -- maker
- Revisa: Analista (verificacion adversarial) -- checker (maker != checker)
- Fecha (UTC): 2026-06-30T01:10:55Z
- Pre-registro de referencia: PRE-REGISTRO-H1-H3-v2.md (FROZEN v2.0, sha256 e8277cc7...; hereda v1.0)
- Freeze del operador: FIRMA-OPERADOR-FREEZE-PRE-REGISTRO-v2.md (des-ciega la medicion)

## 0. Corpus bajo medicion (INMUTABLE -- no se mide nada fuera de aqui)
- Tag canonico:  TFM-dataset-N500  ->  commit e3646ae01fff1f59a5d7882bfd7c8d744ff1c5f9
- Ledger:        runtime/state/events.jsonl  (en ese commit)
- N = 500 eventos elegibles (Arquitecto 253 / Codex 195 / Analista 52)
- Elegibilidad: seq >= 2221 AND type == intent.applied AND actor_auth.method == ed25519
- pin protocol.config.json sha256 2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354

## Reglas de integridad (audit-first; vinculantes)
1. TODA medicion corre sobre el corpus del TAG, NO sobre el working tree vivo (tiene eventos post-ventana).
2. La inyeccion de ataques (H1) es PROGRAMATICA y REPRODUCIBLE: harness con conteos, jamas juicio de un agente (s.8).
3. H3 corre en CLON LIMPIO, solo con claves PUBLICAS, sin secretos en disco (DECISION-0046).
4. Se reportan los FALLOS sin maquillaje (vector evadido, FPR>0, cota excedida) (s.7).
5. No se cambian hipotesis/metricas/umbrales: estan congelados. Esto solo MIDE.
6. Comparar SIEMPRE contra los umbrales pre-comprometidos s.5; el veredicto es mecanico, no opinion.

---

## FASE 0 -- Setup y verificacion del instrumento
- Checkout del corpus en un arbol de trabajo limpio del tag TFM-dataset-N500.
- Verificar sha256 de los 5 pineados byte-identicos == sello; drift 0.
- Re-correr el monitor canonico: `python personal/Arquitecto/monitor_dataset_ed25519.py`
  -> debe reimprimir 500/500 con el desglose {Arquitecto:253, Codex:195, Analista:52}.
- SALIDA: acta de integridad del instrumento (hashes + conteo) que encabeza el informe.

## FASE 1 -- H1 / Deteccion (TPR por vector A1, A2, A3)
- Herramienta base: `examples/attestation_negative_cases/run_attestation_negative_cases.py`
  + `examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` (A2: atribucion cruzada / keyid ajeno / sig invalida).
- Escalar el esqueleto a una corrida con CONTEOS por vector. K ataques por vector, generados programaticamente sobre
  copias del corpus sellado:
  - A1: alteracion puntual de payload, borrado de evento, insercion, reordenamiento (rompe prev_hash).
  - A2: firmar como otro agente, keyid no registrado, firma Ed25519 invalida (rompe actor_auth).
  - A3: rollback del ancla / digest de cabeza no anclado (ventana declarada).
- Cada ataque -> validador/replay -> registrar detectado(1)/evadido(0).
- METRICA: TPR_vector = detectados / inyectados.   UMBRAL s.5: **= 100% en TODOS los vectores** (binario, AC3).
- SALIDA: tabla por vector con K, detectados, TPR; lista explicita de cualquier evasion.

## FASE 2 -- H1 / FPR + Salud AC2 (sobre los 500 legitimos)
- FPR: correr el validador/replay sobre el corpus legitimo SIN ataques.
  `examples/attestation_health_cases/run_attestation_health_cases.py` + replay completo.
  METRICA: FPR = rechazos_falsos / 500.   UMBRAL s.5: **= 0%** (verificador determinista; cualquier rechazo = defecto).
- Salud AC2: atestaciones bien formadas y verificables / eventos autoria-relevantes (denominador independiente del firmante).
  UMBRAL s.5: **>= 99%**.
- SALIDA: FPR observado (n rechazos y cuales, si los hay) + AC2 observado.

## FASE 3 -- H2 / Sobrecoste acotado (con #4 vs baseline sin #4)
- Latencia: medir ms/evento del camino submit_intent CON #4 (firma+encadenado+anclaje) vs un baseline SIN #4
  sobre la MISMA carga; reportar mediana y p95.
  UMBRAL s.5: **mediana <= 50 ms/ev AND p95 <= 200 ms/ev**.
- Almacenamiento: bytes/evento anadidos por #4 (firma 64B + hashes + envoltura) -> Delta sobre baseline.
  UMBRAL s.5: **<= 4 KB/evento**.
- Tokens: sobrecoste de tokens/coordinacion via #3 (`scripts/measure_context_cost.py`, `scripts/agent_token_usage.py`).
  Recordar: #4 firma HASHES, no texto (DECISION-0033/0040) -> esperado ~0.
  UMBRAL s.5: **<= 5%**.
- SALIDA: tabla Delta latencia (med/p95), Delta bytes/ev, Delta tokens %, cada uno vs su cota.

## FASE 4 -- H3 / Verificabilidad independiente (clon limpio, solo publicas)
- Clon limpio del tag; eliminar/no proveer secretos de firma; proveer solo `signature_config.public_keys`.
- Correr `runtime/protocol_replay.py` como verificador externo (secret-independent, DECISION-0046):
  - Acuerdo de veredicto: verdicto identico al interno sobre los 500.   UMBRAL s.5: **= 100%**.
  - Match clon-limpio: hash canonico (con secretos) == (sin secretos).   UMBRAL s.5: **= si**.
  - Firmas Ed25519 verificables con la publica de cada agente.
- SALIDA: veredicto externo, % de acuerdo, hash canonico con y sin secretos (deben coincidir).

## FASE 5 -- Consolidacion (veredicto mecanico contra s.5)
- Por cada H: numero observado vs umbral pre-comprometido -> CONFIRMADA / REFUTADA.
- Declarar limitaciones de s.8 sin maquillaje: A2 independencia DEBIL (ceremonia unica, sin custodios separados);
  A3 independencia DEBIL (ancla mismo disco); sujeto = medidor (por eso H3 da la credibilidad); A4 fuera de alcance.
- SALIDA: tabla de veredictos + seccion de limitaciones.

## FASE 6 -- Entregables y cierre gobernado
- (a) Informe HTML de auditoria (ver spec abajo).
- (b) Datos crudos reproducibles (los conteos/CSV/JSON del harness) junto al informe, para que el verificador externo
      pueda re-correr.
- (c) GATE maker != checker: la Analista verifica adversarialmente que la inyeccion fue programatica/reproducible
      (no juicio de agente), que los conteos cuadran y que el veredicto contra s.5 es correcto, antes de dar el informe
      por final. Veredicto en Area_comun/artifacts.
- (d) Cierre via submit_intent + commit; memoria (DECISION-0026); push si verde.

---

## SPEC del informe HTML (documento de AUDITORIA, no pagina web)
Debe LEERSE como un informe de auditoria formal imprimible, no como una landing:
- Un unico archivo .html autocontenido (CSS embebido; sin JS interactivo, sin menus, sin animaciones, sin assets externos).
- Estilo documento: tipografia serif, A4/print-friendly, margenes, numeracion de secciones, encabezado/pie con
  titulo corto + nro de pagina (via @media print), paleta sobria (negro/gris, sin colores de marca).
- Portada: titulo, subtitulo "Informe de auditoria -- Atestacion de autoria multi-agente (TFM)", autor (Arquitecto),
  ratifica (Operador), fecha/HORA UTC, version del informe.
- Tabla de control del documento: corpus (tag + commit), sha256 de los 5 pineados, estado dataset 500/500 con
  desglose por agente recontado, pre-registro v2.0 sha256, firma del operador.
- Resumen ejecutivo: veredicto por hipotesis (CONFIRMADA/REFUTADA) en una tabla.
- Metodologia: modelo de amenaza A1-A4, criterios de elegibilidad, umbrales pre-comprometidos s.5 (citados textual).
- Hallazgos por hipotesis (H1/H2/H3): numero observado vs umbral, evidencia, y fallos si los hubo.
- Anexo de evidencia: hashes, conteos crudos, comandos ejecutados, salida del verificador externo (con y sin secretos).
- Limitaciones declaradas (s.8) y alcance (A4 fuera).
- Pie de firma/ratificacion.
- REGLA PERMANENTE: el informe lleva SIEMPRE hora real (UTC) + estado del dataset recontado por agente.
