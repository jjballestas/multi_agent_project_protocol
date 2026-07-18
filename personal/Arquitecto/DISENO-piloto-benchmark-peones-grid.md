# DISENO (draft) - Piloto privado benchmark de peones: grid T1-T4 x modelos x escala x modo

Estado: DRAFT con GO del operador al pivote (hub 031b10c): B0-reuse INCORPORADA como celda
CLAVE (amortizacion por repeticion de familia + N de break-even), B1-literal QUITADA, B2 se
mantiene, B1 puro solo control (ya pagado en T1). Fuentes: DIRECTIVA piloto (hub 5f8d88e) +
DIRECTIVA eje modo-delegacion (d44586c) + GO pivote (031b10c) + resultados T1 (TASK-0006 A/B0,
TASK-0007 B1). Demo PRIVADA, NO citable (anti-HARKing). Instrumento maker: Codex CLI
(comparabilidad).
Baseline maquina (Asesor 18-jul): Core 7 250H, 63.7GB RAM, RTX 5060 Laptop 8GB, Ollama 0.32.0
(peones caben en VRAM). PII de nomina: SOLO payloads de fixture. Fondo intocable.

## Lecciones T1 ya incorporadas al diseno
1. B1 puro (extraccion sin spec) MUERE en T1: peon 0/10, frontier 279172 > B0. La spec
   calibrada es la condicion de rendimiento del peon -> el eje modo se re-pondera: B0 y
   B0-reuse (propuesta) son los modos vivos; B2 triage se prueba; B1-literal se descarta
   (pendiente de criterio del operador).
2. Tareas de probe con maker Codex: **type=feature SIEMPRE** (analysis+owner-implementer no
   tiene flip posible en la matriz de capabilities).
3. Registrar por celda: estado warm/cold del peon, asimetrias de ceremonia, y el coste SUNK
   Arquitecto->Codex (intake) declarado como aproximacion.
4. Toda celda delegada conserva: prompt-al-peon como artefacto (DECISION-0099) + salida cruda
   + registro de metricas con placeholder de tokens frontier (los completa el Arquitecto del
   exec log del harness).

## Escalera de tareas (gate DURO pass/fail en todas)
- **T1 mecanica pura (HECHA a lote 10):** tests NEG PII por clave (patron exacto). Gate:
  suite 42 verde por exit-code. Celdas hechas: A=84121, B0=169881, B1=279172.
- **T2 mecanica con variacion:** funcion pura pequena desde spec precisa + edge cases, en
  scratch (no toca producto). Candidata (neutral, autoverificable): parser/normalizador de
  refs de artefacto (p.ej. "TASK-0006#seq-182" -> dict {task, seq}; casos: sin seq, id
  invalido, espacios, mayusculas) con suite de ~12 asserts pre-escrita POR EL MAKER como gate.
  Lote pequeno: 1 funcion + 3 edge cases.
- **T3 juicio moderado (contrato existente):** implementar una funcion que consuma una
  interfaz REAL del repo (leer firma/docstring y ajustarse), p.ej. un formatter de filas
  sobre el dict que devuelve query_memory_db (contrato ya definido en scripts/memory/), con
  suite determinista en scratch. Micro-decision de estructura permitida (orden/agrupacion).
- **T4 ceiling logica dura autoverificable:** algoritmo no trivial multi-paso con suite
  completa pre-definida, p.ej. resolutor de orden topologico con deteccion de ciclos y
  desempate lexicografico sobre un grafo de dependencias sintetico (12-15 casos incl. ciclos,
  huerfanos, estabilidad). NO diseno abierto.

## Celda CLAVE (GO 031b10c): B0-reuse con N de break-even
- Familia GENUINAMENTE repetida y mecanica (misma forma, distinto dato): lotes de ~10 tests
  NEG PII sobre una matriz payload-variante x clave en suite companion de SCRATCH (sin tocar
  la suite de producto entregada). Instancia i de la familia = lote con su variante de datos.
- Una SOLA spec B0 (la de TASK-0006, ya escrita y probada 10/10) sirve a todas las instancias
  sin recalibrar: solo cambia el bloque de datos por instancia.
- Medicion: coste instancia 1 (spec sunk ya pagada -> declarada + delegacion) vs coste
  MARGINAL de instancias 2..N (solo delegacion+review). Brazo directo: 2 instancias arm-A-style
  para la pendiente del baseline. Delegado: 3-4 instancias.
- Entregable: curva acumulada B0-reuse vs acumulada A y el **N de break-even** (donde el
  acumulado delegado cruza por debajo del directo), extrapolado si no cruza en las corridas
  hechas. Ese N informa la decision de adopcion.

## Grid (lean, 1 corrida por celda; ajustado post-GO)
- Escalera base: T1(hecho), T2, T3 x {qwen2.5-coder:3b, deepseek-coder:6.7b, qwen2.5-coder:7b}
  + baseline Codex por tier. Modo por defecto de las celdas delegadas: **B0** (el unico
  probado que rinde). T1 con 3b y 6.7b: reusar la MISMA sub-tarea mitad-B con **B0-reuse**
  (spec constante: mide peon-swap con coste marginal de spec ~0).
- Eje escala: T1 y T2 lote GRANDE (50-100 unidades) x {7b} + baseline Codex; el T1-grande se
  ejecuta COMO la celda B0-reuse de arriba (mata dos pajaros: escala + break-even).
- T4 ceiling: {7b} + baseline. Lote pequeno.
- Celdas de modo (control): B2 (triage) en T1-grande y T2-pequeno. B1-literal QUITADA (GO);
  B1 puro NO se repite (control ya pagado: TASK-0007).
- Total estimado: ~18-20 celdas nuevas = ~18-20 execs frontier + margen re-run.

## Metricas por celda (tabla unica acumulativa en artefacto de instancia)
wall-clock peon (+warm/cold) | llamadas | prompt_eval/eval_count | iteraciones-hasta-verde |
tests corregidos vs aceptados | added-spec-tokens (modo) | tokens frontier exec | pass/fail
del gate | modo de fallo cualitativo | sunk Arquitecto declarado.

## Operacion
- Vehiculo: instancia Nova-Payroll (encapsulada, PII-fixtures ya normalizados alli). Todo en
  scratch/ o tests companion SIN tocar producto entregado; restaurar-a-HEAD como en TASK-0007
  cuando aplique.
- 1 tarea de instancia POR TIER (no por celda): TASK-000X con intake que enumera sus celdas;
  cada celda = un ACTION al cron con la condicion (modelo, modo, escala). Type=feature.
- Analista NO se reactiva (checker = claude per 0101 para los cierres); el gate duro por
  celda es determinista y lo verifica el maker + spot-check del Arquitecto.
- Orden propuesto: (1) T1 B0-reuse con 3b y 6.7b (barato, responde peon-swap); (2) T2 celdas
  pequenas; (3) eje escala T1/T2 con 7b; (4) T3; (5) T4 ceiling; (6) B2 controles; tabla y
  lectura del CRUCE al final. Checkpoint al operador tras cada bloque.
