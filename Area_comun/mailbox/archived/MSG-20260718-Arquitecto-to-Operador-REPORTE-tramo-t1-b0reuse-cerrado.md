---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-tramo-t1-b0reuse-cerrado
from: Arquitecto
to: Operador
type: REPORTE
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260718-Operador-to-Arquitecto-DIRECTIVA-GO-b0reuse-quita-b1literal-sigue-grid.md
  - Area_comun/mailbox/open/MSG-20260718-Arquitecto-to-Operador-FYI-vivo-t1-b0reuse-3b-brillante.md
one_line_summary: "TRAMO T1 CERRADO (TASK-0008 done). Tabla completa T1 lote-10: A directo 84121 | B0 spec-fresca 7b 169881 (peon 10/10) | B1 extractivo 279172 (peon 0/10, REFUTADO) | B0-REUSE 3b 104108 (10/10 SIN correcciones, 15.7s) | B0-REUSE 6.7b 141598 (semantico 10/10, solo normalizacion cosmetica). added-spec-tokens=0 en ambas celdas reuse. LECTURAS: la spec calibrada es la condicion de rendimiento; con spec SUNK la ceremonia marginal cae a ~+24 por ciento del directo YA a lote 10; en peon-swap el MODELO importa mas que el tamano (qwen-3b clavo el patron; el mas barato es el mejor candidato T1). Siguiente: T2 (draft listo) y la celda escala/break-even N."
---

# REPORTE - Tramo T1 cerrado (5 celdas, tabla completa)

## Tabla T1 (lote 10 tests NEG PII; tokens frontier del exec, mismo instrumento Codex CLI)
| Celda | Frontier | Peon (calidad/latencia) | Notas |
|---|---:|---|---|
| A directo | 84121 | - | baseline maker |
| B0 spec fresca (7b) | 169881 | 10/10, 1 llamada, 20.2s | la spec se escribe EN el exec |
| B1 extractivo (7b) | 279172 | 0/10, 3 llamadas | tesis extraccion REFUTADA; numero contaminado por blocker (declarado) |
| B0-reuse (qwen 3b) | 104108 | 10/10 SIN correcciones, 1 llamada, 15.7s cold | added-spec 0; sha del prompt = spec B0 |
| B0-reuse (deepseek 6.7b) | 141598 | semantico 10/10, 1 llamada, 87.7s cold; 10 normalizaciones cosmeticas | added-spec 0; su exec incluye el cierre de la tarea (asimetria declarada, delta real menor) |

## Lecturas del tramo
1. **La spec calibrada es la condicion de rendimiento del peon** (B1 lo refuto; B0/B0-reuse lo
   confirman por ambos lados).
2. **Con la spec SUNK, la ceremonia marginal cae a ~+24 por ciento del directo YA a lote 10**
   (104108 vs 84121). Tu tesis "escribe una vez, delega muchas" queda VIVA y plausible; el
   break-even N lo cuantifica la celda de escala (siguiente bloque tras T2).
3. **Peon-swap: el modelo importa mas que el tamano.** qwen-3b (1.9GB) clavo el patron
   byte-exacto y mas rapido que el 7b; deepseek-6.7b correcto semanticamente pero con ruido
   de formato. Para familias T1-mecanicas, el peon MAS BARATO es el candidato.
4. Operacional: cierre canonico completo (0007 y 0008 done; type=feature aprendido), higiene
   instancia hecha (open/ = hilo vivo), cero cambio de producto persistido en todas las celdas
   (restore-a-HEAD verificado por git status).

## Siguiente (en curso)
- T2 [parser de refs, gate fijo >=12 asserts]: TASK-0009 lista para registrar; celdas
  baseline / 7b-B0 / 3b-B0reuse / 6.7b-B0reuse (misma forma que T1 para curvas comparables).
- Despues: celda ESCALA T1-grande con 7b = curva acumulada B0-reuse vs directo y N de
  break-even; luego T3, T4 ceiling y B2 triage.

Demo privada, NO citable. Fondo intacto: N=500, 2E35F26E, 1.14.0.

-- Arquitecto. Hora local 01:50 (UTC+2, 18-jul).
