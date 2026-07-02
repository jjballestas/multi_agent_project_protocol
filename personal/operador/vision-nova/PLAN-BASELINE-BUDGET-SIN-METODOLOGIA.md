# PLAN BASELINE - Implementar Budget SIN metodologia (periodo descriptivo declarado)

- fecha: 2026-07-02
- emite: Asesor a peticion del Operador ("puedo ir implementando Budget sin la
  metodologia y medirlo, y comparar luego?")
- estado: protocolo listo; lo ejecuta el Operador cuando quiera
- veredicto metodologico del Asesor: SI como BASELINE DESCRIPTIVO DECLARADO;
  NO como comparacion confirmatoria (eso es Q4, asignacion por tarea, ya
  pre-registrada). JAMAS repetir las mismas tareas en ambos modos (relearning
  bias: la segunda pasada siempre gana; invalida todo).

## 1. Que compra y que no compra

COMPRA:
- Q3 (descriptiva) gana su "antes" real: retrabajo/defectos/costo sin gobierno.
- Aprendizaje de dominio Budget -> intake blocks MUCHO mejores para el Sprint 1
  (posiblemente el mayor valor real de este periodo).
- Numeros de contexto para el caso de estudio industrial ("periodo pre-adopcion").

NO COMPRA:
- Evidencia causal de que la metodologia funciona. Esa es Q4 (contraste por tarea,
  ITT, hash+semilla) y Q1/Q2. El baseline es contexto, no prueba.

## 2. Reglas duras (las que hacen el baseline publicable en vez de anecdota)

1. TAREAS DISJUNTAS: nada de lo construido aqui se reimplementa en el estudio.
   Las tareas del Sprint 1 / muestra Q4 seran OTRAS features.
2. TODAS las tareas del periodo se registran, incluidas las abandonadas y las que
   salieron mal (la auditoria selectiva fue el riesgo #12 del veredicto ronda 2:
   publicar solo tareas "limpias" mata el estudio).
3. ESTIMAR ANTES de empezar cada tarea (S/M/L). Estimar despues es trampa.
4. NO adoptar practicas de la metodologia en este periodo (ni gates, ni checker,
   ni intake formal, ni claims): el brazo debe ser autentico "como trabajarias
   sin ella". La UNICA intrusion permitida es el registro de la s.3.
5. REPO APARTE: D:/Agentes/Zeus/nova-budget-baseline (producto -> bajo Zeus/,
   DECISION-0050). NO es la instancia que creara F2.1; NO toca el hub. Si codigo
   del baseline se reusa luego en la instancia gobernada, SE DECLARA.
6. DECLARACION EN EL PRE-REGISTRO (F3.4): fechas del periodo, N tareas, repo,
   que se registro, y el destino del codigo. Un baseline no declarado parece
   dato escondido.
7. TIMEBOX: tu atencion es el cuello (R9). Este periodo no compite con tu rol
   en F1->F4; se corta cuando el Sprint 1 arranca.

## 3. Que registrar POR TAREA (misma moneda que medira el estudio)

Archivo `registro/baseline.csv` en el repo baseline, una fila por tarea:

```text
tarea_id, descripcion_corta, estimate_previo(S|M|L), fecha_inicio, fecha_fin,
tiempo_pared_h, tokens_totales, fuente_tokens(dashboard|ccusage|estimado),
modelo_herramienta, reworks(veces_que_volviste), defectos_post(n),
tipo_defectos(D1-D4 cuando exista taxonomia F1-D), estado(entregada|abandonada),
notas_incidentes
```

Practica de tokens: una sesion de la herramienta = una tarea siempre que puedas;
exporta el consumo por sesion del dashboard del proveedor (o ccusage para Claude
Code). Si una sesion mezclo tareas, reparte aproximado y marca fuente=estimado.

Defectos post: cuando un bug aparezca DESPUES de dar la tarea por entregada,
vuelve a su fila y suma defectos_post + tipo. Ese es el dato que Q3 necesita.

## 4. Como se comparara luego (sin trampas)

- Baseline vs periodo gobernado: SOLO descriptivo (tablas lado a lado con la
  advertencia de confounders: aprendizaje, tareas distintas, herramientas).
- La comparacion con fuerza real: Q4 dentro del estudio (misma epoca, asignacion
  aleatoria por tarea, ITT) y Q1/Q2 (peones, defectos atrapados por el checker).
- Regla de redaccion publica: el baseline se presenta como "periodo pre-adopcion
  instrumentado", nunca como brazo experimental.

## 5. Encaje temporal

Puede arrancar HOY (no depende de F1): repo baseline + CSV + primera tarea.
Corre en paralelo mientras los agentes construyen F1. Se corta al arrancar el
Sprint 1 (30-jul) o antes si tu atencion lo pide. Al sellar F3.4 se declara.
