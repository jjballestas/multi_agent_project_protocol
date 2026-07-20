# LOG DE DECISIONES DELEGADAS - linea grafo sobre memoria hibrida

> Autoridad delegada por el Operador el 2026-07-20 (~03:40): "quedas autonomo coordina
> con el arquitecto responde sus dudas y tienes autoridad para decidir si hay alguna
> duda, si te toca hacerlo me haces un reporte con las razones de la decision".
> Cada entrada registra QUE se decidio, POR QUE, y que alternativa se descarto.

---

## D1 - Adoptar los umbrales del checker VERBATIM, sin ablandar

**Decision:** los umbrales de la seccion 4 de v0.2 se copian tal cual del veredicto
(delta precision@1 >= 4/26 en CADA cohorte, mediana de mejora de rango >= 2 puestos,
binomial exacto bilateral p <= 0.05, Q3 >= 25/26, tokens totales no peores en +5 %).

**Por que:** los umbrales los diseno un adversario cuyo trabajo es que B NO gane facil.
Cualquier ablandamiento mio -- aunque fuera razonable en aislamiento -- reintroduciria
exactamente el sesgo que el checker acaba de cazarme: que el disenador del experimento
elija el liston despues de intuir el resultado. Si el liston resulta demasiado alto, el
experimento saldra INCONCLUSO, que es un resultado honesto; ablandarlo produciria un
"ADOPTABLE" que no me creeria ni yo.

**Alternativa descartada:** negociar el margen a la baja alegando N pequeno. Descartada
porque el N lo fijo tambien el checker sabiendo el tamano del store.

---

## D2 - Congelar el brazo B EN EL DISENO, no en la implementacion

**Decision:** ontologia (5 tipos de arista), profundidad 2, pesos uniformes 1.0, sin
pruning, K comun, formula de score literal en el manifest. Todo antes de construir.

**Por que:** el confusor "tuning leakage" del veredicto no es hipotetico: si el
implementador elige aristas, pesos, profundidad y K DESPUES de conocer el store, esta
eligiendo el resultado. Dejarlo "a criterio de implementacion" era el agujero mas grande
de v0.1, disfrazado de flexibilidad tecnica.

**Pesos uniformes en particular:** los pesos ajustables son el vector de tuning mas
obvio. Con pesos uniformes, si B gana, gana por la ESTRUCTURA; si necesitara pesos
afinados para ganar, eso es un resultado distinto (y peor) que hay que declarar como tal.

---

## D3 - Tie-break COMUN a ambos brazos: `entry_id` canonico ascendente

**Decision:** ambos brazos desempatan igual, y se reporta el expected rank dentro de
empates.

**Por que:** el checker observo que A ordena familias empatadas con tie-break alfabetico.
Si B usara otro, la diferencia de top-1 mediria **desempate**, no valor del grafo. Elegi
`entry_id` ascendente por ser deterministico, independiente del brazo y verificable.

---

## D4 - Cuarentena del builder MAS ESTRICTA que la exigida

**Decision:** el proceso constructor del grafo no accede **ni a las queries ni al answer
key**. El checker solo exigia negar el answer key.

**Por que:** separar fisicamente ambas cosas cuesta lo mismo que separar una, y elimina
una discusion futura ("las queries no revelan la respuesta"). En el probe anterior la
contaminacion nos mordio DOS veces por la via del harness, no por mala fe. Prefiero un
limite fisico a un argumento.

---

## D5 - Ontologia PROPIA, no la del repo externo

**Decision:** cinco tipos de arista de nuestro dominio (`REFERENCIA`, `CORRIGE`,
`SUPERSEDE`, `MISMO_HILO`, `MISMO_AUTOR`), un solo tipo de nodo (`entrada`).

**Por que:** su ontologia (`CALLS`, `IMPORTS`, `INHERITS`...) describe estructura de
codigo. Nuestro dominio son decisiones y hallazgos: las relaciones que importan son de
correccion y sustitucion, no de invocacion. Copiar su ontologia habria sido adoptar la
forma sin el contenido.

**Un solo tipo de nodo, a proposito:** cualquier sub-tipificacion (decision / hallazgo /
reporte) seria INTERPRETACION mia sobre el contenido, y por tanto otra puerta al tuning.
Que la estructura salga de las referencias explicitas, no de mi clasificacion.

---

## D6 - Restriccion de presupuesto de informacion (aristas solo desde lo que A ya tiene)

**Decision:** las aristas se derivan exclusivamente de contenido, autor, timestamp y
referencias explicitas presentes en el texto. Prohibida la anotacion humana nueva y el
enriquecimiento por LLM que introduzca hechos.

**Por que:** es la unica forma de que la comparacion signifique algo. Si B dispone de
informacion que A no recibe, un resultado favorable no dice "el grafo ordena mejor", dice
"mas informacion ayuda" -- que ya lo sabiamos y no justifica construir nada.

**Consecuencia asumida:** el grafo sera mas pobre de lo que podria ser. Correcto: primero
se demuestra que la estructura aporta, y solo despues se discute enriquecerla.

---

## D7 - Marcadores lexicos congelados y no ampliables

**Decision:** la lista de marcadores que derivan `CORRIGE` y `SUPERSEDE` se congela en el
manifest; si falta alguno, se declara como residual y NO se anade.

**Por que:** ampliar marcadores despues de ver resultados es afinar el brazo B a
posteriori con otro nombre. Un marcador faltante es un dato sobre la cobertura real del
metodo, no un bug a parchear a mitad de medicion.

---

## Pendientes que NO decido yo (van al Operador)

- Horizonte de adopcion economica (el break-even se reporta sobre 100/1.000/10.000
  consultas y 1/10/100 mutaciones; **elegir el horizonte es suyo**, por R5 de la 0104).
- La firma de promocion (R0 de la 0104: el checklist hace elegible, la firma promueve).

-- Asesor, 20-jul-2026.
