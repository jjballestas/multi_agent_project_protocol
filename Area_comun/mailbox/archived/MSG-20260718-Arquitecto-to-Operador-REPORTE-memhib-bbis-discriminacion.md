---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-memhib-bbis-discriminacion
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-RESP-metrica-B-bis-queries-selladas.md
one_line_summary: "B-BIS CERRADA (TASK-0023 ratificada; doneflip en cola): hit 26/26 = 100 y precision 26/26 = 100 vs umbrales congelados, AHORA con los 10 distractores como candidatos reales (88 candidaturas verificadas por replay independiente del sello, identico a 11 decimales). LECTURA SELLADA con dato: (1) DISCRIMINACION DE FLUJO = SI (26 selecciones entre ruido real sin tocar jamas un distractor, target visible hasta posicion 21); (2) RANKING DEL STORE = NO-INFORMATIVO (bm25 da scores IDENTICOS a toda la familia; el orden es tie-break alfabetico; el store garantiza CANDIDACY completa, no relevancia); (3) precision conserva componente trivial declarado (la necesidad del consumidor ES la key: elegir SIN la key no es medible con este corpus -> corpus Fase B con necesidades textuales). CLAIM ENGRAM 'comparte contexto': VERIFICADA a nivel plomeria+candidacy+seleccion-de-flujo; recall semantico NO MEDIDO (limitacion honesta). Sigue metrica A."
---

# REPORTE - B-bis: discriminacion medida (la parte que B no podia medir)

## Los numeros (umbrales congelados hit>=85 / precision>=70)
| dimension | valor | lectura sellada por el 0101 |
|---|---|---|
| hit | 26/26 = 100 pct | FUERTE: bajo query ambigua de familia, el target siempre candidate-visible y recuperado-verificado entre ruido real (hasta en posicion 21 del ranking) |
| precision | 26/26 = 100 pct | valida con componente TRIVIAL declarado: la seleccion es need-aware (el consumidor conoce su key); el harness ademas no podia usar un distractor POR CONSTRUCCION (MENOR del sello) |
| candidaturas de distractores | 88 apariciones, 10/10 distractores | el ruido fue REAL (correccion lograda vs B) |
| ranking bm25 del target | min 1 / mediana 6.5 / max 21 | NO-INFORMATIVO: scores identicos por familia; orden = alfabeto. El store da CANDIDACY completa, no relevancia |
| gate integridad | VERDE re-ejecutado | replay 20/20 identico a 11 decimales en clon limpio al estado de medicion; siembra intacta; 42/42; PII 0 |

## Que queda VERIFICADO con dato (claim de Engram "comparte contexto")
La cadena completa guardar-cross-agente -> query ambigua -> candidatos mixtos ->
seleccion correcta -> retrieve sha-verificado -> uso fiel, 26/26 veces con ruido real y
credenciales distintas (proxy jball trazado). Es compartir-contexto OPERATIVO verificado
en el sistema real con procedencia atestada (lo que Engram manifiesta sin poder atestar).

## Que queda declarado como NO MEDIDO (limitaciones honestas, para Fase B)
- Recall SEMANTICO (necesidad expresada como texto libre): imposible con corpus cuyos
  items solo difieren en numero de serie. Corpus Fase B: descripciones de necesidad.
- Seleccion SIN conocer la key; y calidad de ranking con contenido diferenciado (el
  bm25 actual empata familias enteras).
- Observacion operativa del sello: la propia evidencia del probe entra al search-surface
  en replays posteriores (auto-contaminacion +1 posicion); anotado para celdas futuras.

## Estado
TASK-0023 ratificada (instancia 3932b87 local-only); doneflip en cola; al confirmar
arranca la metrica A (re-derivacion evitada: 10 pares SIN/CON, umbral >=40 pct de ahorro
con gate verde). Frontier B-bis: 191352 (contexto). Demo privada, NO citable. Fondo
intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 21:20 (UTC+2, 18-jul).
