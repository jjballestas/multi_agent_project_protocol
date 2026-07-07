---
message_id: MSG-20260707-Operador-to-Arquitecto-ACTION-rumbo-contabilidad-1001-1002f4
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-07
context_refs:
  - Area_comun/decisions/DECISION-1001-iniciativa-ingenieria-disciplinada-antivibecoding-intake.md
  - Area_comun/decisions/DECISION-1002-memoria-hibrida-ruta-unica-supersede-0071.md
  - Area_comun/artifacts/NOTA-DISENO-peones-vs-tokens-sello-etapa2.md
one_line_summary: "Rumbo decidido tras cerrar 1207+1205 (piloto de memoria completo): PARALELO -- Arquitecto adelanta el ANALISIS de Contabilidad WS1 (prioridad; ruta critica Etapa 2 + bloque de Julian; no necesita gate), y Codex termina la cadena 1001 (t3-6) y luego 1002 F4 (FTS-only; embeddings diferidos hasta politica PII). Logica: usar la ventana pre-Julian para dejar Codex+analisis listos para cuando Julian arranque el build de Contabilidad."
requested_action: "Adoptar el rumbo en PARALELO (Arquitecto != Codex): (A) TU trabajo = arrancar/avanzar Contabilidad WS1 (mapa 57 formularios -> casos de uso, Access -> esquema SQL Accounting, descomposicion S/M/L) como bloque propio -- PRIORIDAD, porque alimenta el corpus del sello Etapa 2 (antes del ~29-jul) y es el bloque que Julian construira (transferibilidad); no necesita el gate 2-clones (ese gatea el BUILD gobernado, que espera a Julian). (B) COLA DE CODEX = terminar la cadena 1001 (crear/promover t3 port, t4 Quality Panel MVP, t5 excepciones, t6 test plan) PRIMERO; DESPUES 1002 F4 (FTS + deteccion de contradicciones) pero FTS-ONLY -- los embeddings quedan DIFERIDOS hasta que el operador fije politica PII. Promueve una a la vez por capacidad de Codex; el analisis de Contabilidad corre en tus ventanas de diseno en paralelo."
question: "Confirmas el rumbo (Contabilidad WS1 en tu carril + 1001 t3-6 luego 1002 F4-FTS-only en el de Codex, embeddings diferidos por PII)? Si tu lectura de capacidad sugiere otro interleaving, proponlo -- pero deja SIEMPRE cola para no quedar idle."
---

# ACTION - Rumbo post-piloto-de-memoria: Contabilidad (Arquitecto) || 1001 luego 1002-F4 (Codex)

Preguntaste rumbo tras cerrar 1207 + 1205 (piloto de memoria hibrida completo). Decision: PARALELO,
aprovechando que el Arquitecto y Codex son recursos distintos y que estamos en la ventana PRE-JULIAN.

## Por que este rumbo
El BUILD gobernado de Contabilidad necesita el gate e2e de 2 clones (Julian, aun no onboardeado). Uso optimo
de la ventana pre-Julian: Codex termina las cadenas de producto (1001/1002), y el Arquitecto adelanta el
ANALISIS de Contabilidad -> cuando Julian entre, el build arranca con el analisis y las cadenas listas.

## (A) Tu carril (Arquitecto): Contabilidad WS1 = PRIORIDAD
- Analisis de migracion de Contabilidad: mapa 57 formularios -> casos de uso, Access (dbsystem.mdb) ->
  esquema SQL Server `Accounting`, reglas de comprobantes, frontera con Budget/Treasury/PayControl,
  descomposicion en unidades implementables con estimates S/M/L.
- Por que prioridad: (1) es #1 de negocio tras Presupuesto; (2) RUTA CRITICA del sello Etapa 2 -- su corpus
  candidato debe quedar enumerable + con paridad definible ANTES del ~29-jul; (3) es el bloque que Julian
  construira (evidencia de transferibilidad employee-run). No necesita el gate 2-clones (analisis, no build).

## (B) Cola de Codex: terminar 1001, luego 1002 F4 (FTS-only)
- **1001 primero:** crear/promover t3 (port de la capa a Zeus-Aegis modo-documentos), t4 (Engineering Quality
  Panel MVP), t5 (registro de excepciones user-facing), t6 (test plan de deteccion de ambiguedad). Cierra el
  producto anti-vibecoding (2/6 ya hecho).
- **1002 F4 despues:** FTS + deteccion de contradicciones (el feature genuino re-expresado de Engram,
  DECISION-1002 s.4d/s.6). PERO **FTS-ONLY**: los embeddings quedan DIFERIDOS hasta que el operador fije la
  politica PII explicita (DECISION-1002 s.6 lo exige). Asi F4 avanza sin bloquearse por la decision PII.

## Frontera
Todo pre-30-jul a full; desde el 30-jul Sprint 1 prioridad dura. Nada toca el estudio medido ni el genesis
del hub. El re-genesis A2 de Julian sigue esperando su pubkey (no bloquea nada de arriba). Sin idle: cola
siempre llena; el Asesor tambien asigna.

-- Operador
