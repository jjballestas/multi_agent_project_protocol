# DISENO - Probe de coste: el peon local reduce los tokens frontier del maker?

- Fecha: 2026-07-17. Autor: Arquitecto. Estado: DISENO PARA REVISION del operador (no ejecutar
  hasta su OK + cierre de TASK-0005/Fase A). Origen: DIRECTIVA disena-probe-coste-peon-local.
- Clase de evidencia: DEMO / soporte a decision, NO citable (anti-HARKing). Numero riguroso =
  pre-registro en Fase B solo si la demo promete.

## 1. Confirmacion del diseno base (con 4 refinamientos objetables)

CONFIRMO la estructura: sub-tarea mecanica de alto volumen, 2 condiciones (A maker-solo vs B
maker-delega-a-peon), metrica = delta de tokens FRONTIER del maker contando el overhead de
spec + review/integracion. Refinamientos:

1. **Sub-tarea concreta propuesta:** generar el lote de TESTS NEGATIVOS por clave allowlisted
   del gate PII de la memoria (patron ya existente en test_memory_db.py: 20 claves x fixture
   plantado -> rechazo esperado). Es real (endurece F1), mecanica (mismo esqueleto x20),
   verificable automaticamente (suite verde/roja por exit-code) y de volumen suficiente
   (~400-600 lineas). Alternativa B: fixtures markdown de artefactos sinteticos para el
   round-trip (mas volumen, menos juicio). Recomiendo la A porque el checker automatico (la
   suite) da un criterio de correccion DURO sin gastar tokens frontier en evaluar.
2. **Aleatorizacion minima honesta:** las 2 condiciones sobre DOS mitades disjuntas del mismo
   lote (10 claves + 10 claves, asignadas por sorteo simple documentado), no el mismo trabajo
   dos veces (el segundo pase siempre es mas barato por aprendizaje del maker -> sesgo).
3. **Contabilidad de tokens EXPLICITA (la clave del probe):**
   - Condicion A: tokens frontier del maker haciendo la mitad-A directo (lo reporta el CLI).
   - Condicion B: tokens frontier de (spec detallada para el peon + revision/correccion de su
     salida + integracion). Los tokens del peon local (Ollama qwen2.5-coder:7b o
     deepseek-coder:6.7b) se reportan aparte como ~coste-cero monetario pero SI se registra su
     wall-clock (la latencia local es un coste real).
   - Delta neto = A - B(frontier). Umbral de lectura (pre-declarado): B gana si ahorra >=25%
     de tokens frontier CON la suite verde en ambos; empate/perdida tambien es resultado util.
4. **Disciplina DECISION-0099 verificable:** la spec del maker al peon queda como artefacto
   (es la evidencia de "peon subordinado con spec detallada"); el maker responde ante el
   checker por la mitad-B igual que por la A (review adversarial normal de la unidad).

## 2. Mecanica de ejecucion (cuando se autorice)

1. Registrar en Nova-Payroll una tarea gobernada TASK-000X "lote tests NEG PII por clave"
   (owner Codex, reviewer Analista) con las 2 mitades y el protocolo de medicion en el intake.
2. Condicion A: Codex (frontier) implementa mitad-A directo. Registrar tokens del CLI.
3. Condicion B: Codex escribe la spec del peon (artefacto), invoca al peon local via Ollama
   para la mitad-B, revisa/corrige/integra. Registrar tokens frontier de todo el ciclo B +
   tokens/wall-clock del peon.
4. Gates + review adversarial de la unidad completa (las dos mitades juntas).
5. Salida: tabla A-vs-B (tokens frontier, wall-clock, iteraciones de correccion del peon,
   veredicto del checker) + lectura cualitativa: que clase de sub-tarea ahorra y cual no.

## 3. Prerequisitos y riesgos declarados

- Ollama instalado con el modelo elegido y el peon invocable desde el harness del maker
  (cableado minimo; sin tocar el hub). Verificar ANTES de arrancar: 1 smoke del peon.
- Riesgo principal: overhead de spec+review > ahorro en sub-tareas no-mecanicas -- por eso la
  sub-tarea es deliberadamente mecanica; el resultado negativo TAMBIEN es valioso (acota donde
  NO usar peones).
- Contaminacion: el maker no debe ver la salida del peon antes de escribir su condicion A
  (mitades disjuntas lo resuelven).
- PII de nomina fuera de todo el probe; fondo intocable; nada citable.

## 4. Pendiente del operador

(a) OK al diseno (o ajustes); (b) eleccion del modelo local (qwen2.5-coder:7b vs
deepseek-coder:6.7b vs otro que tengas ya en Ollama); (c) GO de ejecucion tras cierre de
TASK-0005/Fase A.
