---
message_id: MSG-20260718-Arquitecto-to-Operador-REPORTE-smoke-peon-qwen7b-verde
from: Arquitecto
to: Operador
type: FYI
status: archived
requires_response: false
created_at: 2026-07-18
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-GO-probe-coste-peon-qwen7b.md
one_line_summary: "SMOKE del peon qwen2.5-coder:7b = VERDE OPERATIVO (paso 0 del probe). Invocable via Ollama local; micro-tarea representativa (1 test NEG PII al estilo de la suite real) generada en 50s con codigo utilizable; deviaciones menores tipicas de 7b (fences pese a instruccion, assert plano en vez de self.assert) = exactamente lo que la revision del maker pulira y el probe medira. Mecanica A-vs-B arranca con UNA precision de instrumento: el maker correra como worker-revivido (mismo runtime en AMBAS condiciones -> delta internamente valido); si prefieres el Codex CLI como instrumento, relanza su cron y lo uso. Sigo con la mecanica salvo orden contraria en tu proxima ventana."
---

# REPORTE - Smoke del peon (paso 0): VERDE

## Evidencia

- Ollama local operativo; `qwen2.5-coder:7b` presente (4.7 GB, id dae161e2).
- Micro-tarea representativa del lote real: generar 1 metodo de test NEG PII siguiendo un patron
  exacto (fixture con salario/IBAN/nombre en clave allowlisted -> assert de no-aparicion en
  summary_short). Resultado: rc=0, **50s wall-clock**, 612 bytes.
- Calidad: el codigo SIGUE el patron pedido (fixture correcto, _build, query, asserts de
  no-aparicion). Deviaciones tipicas de 7b: envolvio en fences markdown pese a la instruccion
  y uso assert plano en vez de self.assertNotIn -- ambas se pulen en la revision del maker,
  que es exactamente el overhead que el probe mide. VEREDICTO: rinde para la sub-tarea mecanica.
- Nota tecnica: la captura por TTY mete codigos de control de la barra de progreso de ollama;
  la mecanica usara la API HTTP local (localhost:11434/api/generate) para texto limpio y
  conteo de tokens del peon.

## Precision de instrumento para A-vs-B (sigo asi salvo que ordenes lo contrario)

El cron del maker (Codex CLI) esta MUERTO desde la demo REVIVE y su relanzamiento es tu linea
(classifier). Para no bloquear: el maker correra como WORKER-REVIVIDO (subagent modelo fuerte
con pack, el mismo mecanismo ya probado 3x), en AMBAS condiciones A y B con el MISMO runtime --
el delta de tokens frontier queda internamente valido (mismo instrumento en los dos brazos),
que es lo que el umbral >=25% necesita. Los absolutos no seran comparables con el Codex CLI,
y lo declaro en la tabla. Si prefieres el Codex CLI como instrumento, relanza su cron con tu
linea y redirijo la mecanica a el.

## Siguiente

Registro la TASK gobernada en Nova-Payroll (lote 20 claves, sorteo documentado de mitades),
corro A (maker-solo) y B (maker-delega-a-qwen7b), y te reporto la tabla A-vs-B + lectura
cualitativa. Demo NO citable (anti-HARKing); PII de nomina fuera; fondo intocable.

-- Arquitecto. Hora local ~02:55 (UTC+2, ya 18-jul). Fondo: N=500, 2E35F26E, 1.14.0 intactos.
